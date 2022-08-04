# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re
import xbmc
import xbmcgui

from resources.lib.comaddon import addon, isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'uptobox_live'
SITE_NAME = '[COLOR violet]UpToBox Live[/COLOR]'
SITE_DESC = 'Bibliothèque de liens Uptobox'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = (URL_MAIN + 'search?start-with=&sort=size&order=desc&q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?start-with=&sort=id&order=desc&q=', 'showSeries')


def load():
    oGui = cGui()
    sToken = cPremiumHandler('uptobox').getToken()

    if not sToken:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', '//')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addon().VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oOutputParameterHandler.addParameter('sMovieTitle', 'movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oOutputParameterHandler.addParameter('sMovieTitle', 'tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def opensetting():
    addon().openSettings()


def showSearch(path = '//'):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrlSearch = sUrl + sSearchText
        
        if sTitle == 'movie':
            showMovies(sUrlSearch)
        else:
            showSeries(sUrlSearch)


def getAuthorizedID():
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    oRequest = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequest.request()
    sPattern = "Authorization': '(.+?)'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return False


def getContent(sSearch):
    
    sUrl = sSearch.replace(' ', '%20')
    id = getAuthorizedID()
    
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Authorization', id)
    sHtmlContent = oRequest.request()

    content = json.loads(sHtmlContent)
        
#    if content['status'] == 'unauthorized':
    if content['status'] == 'ok':
        return content['items']

    return [] 


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    sUrl = sSearch.replace(' ', '%20').replace('-', '\-')

    searchGlobal = cInputParameterHandler().getValue('sMovieTitle') == False

    sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
    sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
    sSearchText = oUtil.CleanName(sSearchText)

    movies = set()
    content = getContent(sUrl)
    for movie in content:
        sTitle = movie['title']
        
        # seulement les formats vidéo (ou sans extensions)
        if sTitle[-4] == '.':
            if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]
    
        if '1XBET' in sTitle:
            continue
    
        # recherche des métadonnées
        pos = len(sTitle)
        sYear, pos = getYear(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)

        # enlever les séries
        sTitle = sTitle[:pos]
        sa, ep = getSaisonEpisode(sTitle)
        if sa or ep:
            continue
    
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
        
        sMovieTitle = sTitle[:pos]
        sMovieTitle = oUtil.unescape(sMovieTitle)
        sMovieTitle = oUtil.CleanName(sMovieTitle)

        if not oUtil.CheckOccurence(sSearchText, sMovieTitle):
            continue    # Filtre de recherche

        searchMovie = '%s|%s' % (sMovieTitle, sYear if sYear else '')
        if searchMovie in movies:
            continue                # film déjà proposé
        
        movies.add(searchMovie)

        sDisplayTitle = sMovieTitle
        if sYear:
            sDisplayTitle += ' (%s)' % sYear
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

    if not searchGlobal:
        oGui.setEndOfDirectory()


def showSeries(sSearch = ''):

    oGui = cGui()
    searchGlobal = cInputParameterHandler().getValue('sMovieTitle') == False
    if sSearch:
        sUrl = sSearch.replace(' ', '%20')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    content = getContent(sUrl)

    series = set()
    oUtil = cUtil()

    # Recherche des saisons
    for file in content:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
            
        if sTitle[-4] == '.':
            if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        # recherche des métadonnées
        pos = len(sTitle)
        sYear, pos = getYear(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)

        # Recherche des noms de séries
        sTitle = sTitle[:pos]
        pos = len(sTitle)
        saison, episode, pos = getSaisonEpisode(sTitle, pos)

        if saison:
            if int(saison) > 100:
                continue
            sTitle = sTitle[:pos]
            sMovieTitle = oUtil.unescape(sTitle).strip()
            sMovieTitle = oUtil.CleanName(sMovieTitle)
            series.add(sMovieTitle)

    if len(series) > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle in series:
            sUrl = sUrl #+ '&sTitle=%s' % sTitle
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', '', '', oOutputParameterHandler)

    if not searchGlobal:
        oGui.setEndOfDirectory()


def showSaisons():
    oGui = cGui()
    saisons = set()
    oUtil = cUtil()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchTitle = oInputParameterHandler.getValue('sMovieTitle')

    content = getContent(sUrl)

    # Recherche des saisons
    for file in content:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')

        if sTitle[-4] == '.':
            if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        # recherche des métadonnées
        pos = len(sTitle)
        sYear, pos = getYear(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)

        # Recherche des noms de séries
        sTitle = sTitle[:pos]
        pos = len(sTitle)
        saison, episode, pos = getSaisonEpisode(sTitle, pos)

        if saison:
            sTitle = sTitle[:pos]
            sMovieTitle = oUtil.unescape(sTitle).strip()
            sMovieTitle = oUtil.CleanName(sMovieTitle)
            if sMovieTitle != sSearchTitle:
                continue
            saisons.add(saison)

    if len(saisons) > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for saison in sorted(saisons):
            #sUrl = sSiteUrl #+ '&sTitle=%s' % sTitle
            sDisplayTitle = '%s S%s' % (sSearchTitle, saison)
            siteUrl = '%s|%s' % (sUrl, saison)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            sSaisonTitle = '%s S%s' % (sSearchTitle, saison)
            oOutputParameterHandler.addParameter('sMovieTitle', sSaisonTitle)
#            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():

    oGui = cGui()
    oUtil = cUtil()

    oInputParameterHandler = cInputParameterHandler()
    sUrl, sSearchSaison  = oInputParameterHandler.getValue('siteUrl').split('|')
    sSearchTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSearchTitle = sSearchTitle.replace(' S%s' % sSearchSaison, '')

    content = getContent(sUrl)

    # Recherche des épisodes
    episodes = set()
    for file in content:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')

        if sTitle[-4] == '.':
            if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        # recherche des métadonnées
        pos = len(sTitle)
        sLang, pos = getLang(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sYear, pos = getYear(sTitle, pos)

        # Recherche des noms de séries
        sTitle = sTitle[:pos]
        pos = len(sTitle)
        saison, episode, pos = getSaisonEpisode(sTitle, pos)
        if not saison or saison != sSearchSaison:
            continue

        sMovieTitle = sTitle[:pos]
        sMovieTitle = oUtil.unescape(sMovieTitle).strip()
        sMovieTitle = oUtil.CleanName(sMovieTitle)

        if sMovieTitle != sSearchTitle:
            continue

        episodes.add(episode)
        
        
    for episode in sorted(episodes):
        sDisplayTitle = '%s S%sE%s' % (sSearchTitle, sSearchSaison, episode)

        oOutputParameterHandler = cOutputParameterHandler()
        siteUrl = '%s|%s|%s' % (sUrl, sSearchSaison, episode)
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        sEpTitle = '%s S%sE%s' % (sSearchTitle, sSearchSaison, episode)
        oOutputParameterHandler.addParameter('sMovieTitle', sEpTitle)
#            oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():

    from resources.lib.gui.hoster import cHosterGui
    oGui = cGui()
    oHosterGui = cHosterGui()
    hoster = oHosterGui.getHoster('lien_direct')
    oUtil = cUtil()

    oInputParameterHandler = cInputParameterHandler()
    sSearchTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchSaison = ''
    if '|' in sUrl:
        sUrl, sSearchSaison, sSearchEpisode = sUrl.split('|')
        sSearchTitle = sSearchTitle.replace(' S%sE%s' % (sSearchSaison, sSearchEpisode), '')
    

    content = getContent(sUrl)
    oHoster = oHosterGui.getHoster('uptobox')

    # Recherche des saisons
    for file in content:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')

        if sTitle[-4] == '.':
            if sTitle[-4:] not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        # Recherche des metadonnées
        pos = len(sTitle)
        sLang, pos = getLang(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sYear, pos = getYear(sTitle, pos)

        # identifier une série
        sTitle = sTitle[:pos]
        pos = len(sTitle)
        saison, episode, pos = getSaisonEpisode(sTitle, pos)

        if sSearchSaison:   # recherche de série
            if not saison or saison != sSearchSaison:
                continue
            if not episode or episode != sSearchEpisode:
                continue
        else: # recherche de film
            if saison or episode:
                continue

        sTitle = sTitle[:pos]
        sMovieTitle = oUtil.unescape(sTitle).strip()
        sMovieTitle = oUtil.CleanName(sMovieTitle)
        if sMovieTitle != sSearchTitle:
            continue

        sDisplayTitle = sSearchTitle
        if saison:
            sDisplayTitle += 'S%sE%s' % (saison, episode)
        if sRes:
            sDisplayTitle += ' [%s]' % sRes
        if sLang:
            sDisplayTitle += ' (%s)' % sLang
        sHosterUrl = file['link']

        oOutputParameterHandler = cOutputParameterHandler()
        #sUrl = sSiteUrl #+ '&sTitle=%s' % sTitle
        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sDisplayTitle)
        oHosterGui.showHoster(oGui, oHoster, sHosterUrl, '')


    oGui.setEndOfDirectory()

    
# Recherche saisons et episodes
def getSaisonEpisode(sTitle, pos = 0):
    sa = ep = terme = ''
    m = re.search('(|S|saison)(\s?|\.)(\d+)(\s?|\.| - )(E|Ep|x|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
    if m:
        sa = m.group(3)
        if int(sa) <100:
            ep = m.group(7)
            terme = m.group(0)
        else:
            sa = ''
    else:  # Juste l'épisode
        m = re.search('(^|\s|\.)(E|Ep|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
        if m:
            ep = m.group(4)
            sa = '01' # si la saison n'est pas précisée, c'est qu'il n'y a sans doute qu'une saison
            terme = m.group(0)
        else:  # juste la saison
            m = re.search('( S|.S|saison)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''
                else:
                    terme = m.group(0)

    if terme:
        p = sTitle.index(terme)
        if p<pos:
            if p<5: # au début, on retire directement l'élement recherché
                sTitle = sTitle.replace(terme, '')
                pos -= len(terme)
            else:
                pos = p

    if pos == 0:
        return sa, ep
    return sa, ep, pos


def getYear(sTitle, pos):
    sPattern = ['[^\w]([0-9]{4})[^\w]']
    return _getTag(sTitle, sPattern, pos)


def getLang(sMovieTitle, pos):
    sPattern = ['VFI', 'VFF', 'VFQ', 'SUBFRENCH', 'TRUEFRENCH', 'FRENCH', 'VF', 'VOSTFR', '[^\w](VOST)[^\w]', '[^\w](VO)[^\w]', 'QC', '[^\w](MULTI)[^\w]']
    return _getTag(sMovieTitle, sPattern, pos)


def getReso(sMovieTitle, pos):
    sPattern = ['HDLIGHT', '\d{3,4}P', '4K', 'UHD', 'BDRIP', 'BRRIP', 'DVDRIP', 'DVDSCR', 'TVRIP', 'HDTV', 'BLURAY', '[^\w](R5)[^\w]', '[^\w](CAM)[^\w]', 'WEB-DL', 'WEBRIP', '[^\w](WEB)[^\w]']
    sRes, pos = _getTag(sMovieTitle, sPattern, pos)
    if sRes:
        sRes = sRes.replace('2160P', '4K')
    return sRes, pos


def _getTag(sMovieTitle, tags, pos):
    for t in tags:
        aResult = re.search(t, sMovieTitle, re.IGNORECASE)
        if aResult:
            l = len(aResult.groups())
            ret = aResult.group(l)
            if not ret and l > 1:
                ret = aResult.group(l-1)
            terme = aResult.group(0)
            p = sMovieTitle.index(terme)
            if p<pos:
                if p<5: # au début, on retire directement l'élement recherché
                    sMovieTitle = sMovieTitle.replace(terme, '')
                    pos -= len(terme)
                else:
                    pos = p
            return ret.upper(), pos
    return False, pos
