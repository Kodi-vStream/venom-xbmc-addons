# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re

from resources.lib.comaddon import addon, isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote


SITE_IDENTIFIER = 'uptobox_live'
SITE_NAME = '[COLOR violet]UpToBox Live[/COLOR]'
SITE_DESC = 'Bibliothèque de liens Uptobox'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = (URL_MAIN + 'search?sort=size&order=desc&q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?sort=id&order=asc&q=', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + 'search?sort=id&order=asc&q=', 'showAnims')


def load():
    oGui = cGui()
    sToken = cPremiumHandler('uptobox').getToken()
    oOutputParameterHandler = cOutputParameterHandler()

    if not sToken:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
        oOutputParameterHandler.addParameter('siteUrl', '//')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addon().VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return

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
            showMovies(sUrlSearch, True)
        else:
            showSeries(sUrlSearch, True)


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


def showMovies(sSearch='', searchLocal = False):
    oGui = cGui()
    oUtil = cUtil()

    sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
    sSearchText = Unquote(sSearchText)
    sSearchText = oUtil.CleanName(sSearchText)

    sUrl = sSearch.replace(' ', '%20').replace('-', '\-')
    content = getContent(sUrl)
    
    oOutputParameterHandler = cOutputParameterHandler()
    movies = set()
    for movie in content:
        sTitle = movie['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
        
        # seulement les formats vidéo (ou sans extensions)
        if sTitle[-4] == '.':
            if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]
    
        sTitle = sTitle.replace('CUSTOM', '')
        if '1XBET' in sTitle:  # or 'HDCAM'
            continue

        # recherche des métadonnées
        pos = len(sTitle)
        sYear, pos = getYear(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)
        sa, ep = getSaisonEpisode(sTitle)

        # enlever les séries
        if not sa or not ep:
            sTitle = sTitle[:pos]
            sa, ep = getSaisonEpisode(sTitle)
        if sa or ep:
            continue
    
        sMovieTitle = sTitle[:pos]
        sMovieTitle = oUtil.unescape(sMovieTitle)
        sMovieTitle = sMovieTitle.replace('.', ' ')
        
        if not oUtil.CheckOccurence(sSearchText, sMovieTitle):
            continue    # Filtre de recherche

        # lien de recherche spécifique à chaque film
        siteUrl = URL_SEARCH_MOVIES[0] + sMovieTitle.replace('-', '\-')
        startWith = sMovieTitle[0].upper()
        if startWith.isnumeric():
            startWith = 'number'
        siteUrl += '&start\-with=' + startWith

        if sYear:
            sMovieTitle += ' (%s)' % sYear

        sSearchTitle = oUtil.CleanName(sMovieTitle)
        if sSearchTitle in movies:
            continue                # film déjà proposé
        
        movies.add(sSearchTitle)
        
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sSearchTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sMovieTitle, 'films.png', '', '', oOutputParameterHandler)

    if searchLocal:
        oGui.setEndOfDirectory()


def showAnims(sSearch = ''):
    showSeries(sSearch, False, True)


def showSeries(sSearch = '', searchLocal = False, isAnime = False):
    oGui = cGui()
    oUtil = cUtil()

    sSearchTitle = sSearch.replace(URL_SEARCH_SERIES[0], '')
    sSearchTitle = Unquote(sSearchTitle)
    sSearchTitle = oUtil.CleanName(sSearchTitle)
    
    sUrl = sSearch.replace('-', '\-')
    content = getContent(sUrl)

    # Recherche des saisons
    series = set()
    for file in content:
        sTitle = file['title']
        if not isMatrix():
            sTitle = sTitle.encode('utf-8')
            
        if sTitle[-4] == '.':
            if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        # recherche des métadonnées
        pos = len(sTitle)
        sYear, pos = getYear(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)
        saison, episode, pos = getSaisonEpisode(sTitle, pos)

        # Recherche des noms de séries
        if not saison or not episode:
            sTitle = sTitle[:pos]
            pos = len(sTitle)
            saison, episode, pos = getSaisonEpisode(sTitle, pos)

        if saison:
            if int(saison) > 100:
                continue
            sTitle = sTitle[:pos]
            sMovieTitle = oUtil.unescape(sTitle).strip()
            sMovieTitle = oUtil.CleanName(sMovieTitle)

            if not oUtil.CheckOccurence(sSearchTitle, sMovieTitle):
                continue    # Filtre de recherche
            
            series.add(sMovieTitle)

    if len(series) > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle in series:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            if isAnime:
                oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sTitle, '', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', '', '', oOutputParameterHandler)

    if searchLocal:
        oGui.setEndOfDirectory()


def showSaisons():
    # deux url pour plus de résultats
    oGui = cGui()
    saisons = {}
    oUtil = cUtil()

    oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchTitle = oInputParameterHandler.getValue('sMovieTitle')

    # recherche depuis le titre sélectionné, pas depuis les mots clefs recherchés
    sUrl = URL_SEARCH_SERIES[0] + sSearchTitle.replace('-', '\-')
    startWith = sSearchTitle[0].upper()
    if startWith.isnumeric():
        startWith = 'number'
    sUrl += '&start\-with=' + startWith

    # deux url pour plus de résultats
    urls = [sUrl, sUrl.replace('order=asc', 'order=desc')]

    for sUrl in urls:
        content = getContent(sUrl)
    
        # Recherche des saisons
        for file in content:
            sTitle = file['title']
            if not isMatrix():
                sTitle = sTitle.encode('utf-8')
    
            if sTitle[-4] == '.':
                if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                    continue
                # enlever l'extension
                sTitle = sTitle[:-4]
    
            # recherche des métadonnées
            pos = len(sTitle)
            sYear, pos = getYear(sTitle, pos)
            sRes, pos = getReso(sTitle, pos)
            sLang, pos = getLang(sTitle, pos)
            saison, episode, pos = getSaisonEpisode(sTitle, pos)
    
            # Recherche des noms de séries
            if not saison or not episode:
                sTitle = sTitle[:pos]
                pos = len(sTitle)
                saison, episode, pos = getSaisonEpisode(sTitle, pos)
    
            if saison:
                sTitle = sTitle[:pos]
                sMovieTitle = oUtil.unescape(sTitle).strip()
                sMovieTitle = oUtil.CleanName(sMovieTitle)
                if sMovieTitle == sSearchTitle:
                    saisons[saison] = sUrl

    oOutputParameterHandler = cOutputParameterHandler()
    for saison, sUrl in sorted(saisons.items(), key=lambda s: s[0]):
        sDisplayTitle = '%s S%s' % (sSearchTitle, saison)
        siteUrl = '%s|%s' % (sUrl, saison)
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        sSaisonTitle = '%s S%s' % (sSearchTitle, saison)
        oOutputParameterHandler.addParameter('sMovieTitle', sSaisonTitle)
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
            if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        # recherche des métadonnées
        pos = len(sTitle)
        sLang, pos = getLang(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sYear, pos = getYear(sTitle, pos)
        saison, episode, pos = getSaisonEpisode(sTitle, pos)

        # Recherche des noms de séries
        if not saison or not episode:
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
        
    oOutputParameterHandler = cOutputParameterHandler()
    for episode in sorted(episodes):
        sDisplayTitle = '%s S%sE%s' % (sSearchTitle, sSearchSaison, episode)

        siteUrl = '%s|%s|%s' % (sUrl, sSearchSaison, episode)
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        sEpTitle = '%s S%sE%s' % (sSearchTitle, sSearchSaison, episode)
        oOutputParameterHandler.addParameter('sMovieTitle', sEpTitle)
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
    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    
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
            if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

        sTitle = sTitle.replace('CUSTOM', '')
        if '1XBET' in sTitle:
            continue

        # Recherche des metadonnées
        pos = len(sTitle)
        sLang, pos = getLang(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sYear, pos = getYear(sTitle, pos)

        # identifier une série
        saison, episode, pos = getSaisonEpisode(sTitle, pos)
        if not saison or not episode:
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

            # vérifier l'année pour les homonymes, seulement pour les films
            if sSearchYear:
                if sYear:
                    if sSearchYear != sYear:
                        continue
                else:
                    continue
            elif sYear:
                continue

        sTitle = sTitle[:pos]
        sMovieTitle = oUtil.unescape(sTitle).strip()
        sMovieTitle = sMovieTitle.replace('.', ' ')
        if oUtil.CleanName(sMovieTitle) != sSearchTitle:
            continue

        sDisplayTitle = sMovieTitle
        if saison:
            sDisplayTitle += ' S%sE%s' % (saison, episode)
        if sRes:
            sDisplayTitle += ' [%s]' % sRes
        if sLang:
            sDisplayTitle += ' (%s)' % sLang
        if sYear:
            sDisplayTitle += ' (%s)' % sYear
        sHosterUrl = file['link']

        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sDisplayTitle)
        oHosterGui.showHoster(oGui, oHoster, sHosterUrl, '')


    oGui.setEndOfDirectory()

    
# Recherche saisons et episodes
def getSaisonEpisode(sTitle, pos = 0):
    sTitle = sTitle.replace('x264', '').replace('x265', '').strip()
    sa = ep = terme = ''
    m = re.search('( S|\.S|saison)(\s?|\.)(\d+)( - |\s?|\.)(E|Ep|x|\wpisode|Épisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
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
            m = re.search('( S|\.S|saison)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''
                else:
                    terme = m.group(0)

    if terme:
        p = sTitle.index(terme)
        if p<pos and p>5: # au début, on retire directement l'élement recherché
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
    sPattern = ['HDCAM', '[^\w](CAM)[^\w]', '[^\w](R5)[^\w]', 'DVDSCR', 'TVRIP', 'HDLIGHT', '\d{3,4}P', '4K', 'UHD', 'BDRIP', 'BRRIP', 'DVDRIP', 'HDTV', 'BLURAY', 'WEB-DL', 'WEBRIP', '[^\w](WEB)[^\w]']
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
            if p<pos and p> 2: # si ce n'est pas au début
                pos = p
            return ret.upper(), pos
    return False, pos
