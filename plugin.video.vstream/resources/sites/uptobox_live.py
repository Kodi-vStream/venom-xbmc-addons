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
SITE_NAME = '[COLOR violet]Uptobox Live[/COLOR]'
SITE_DESC = 'Bibliothèque de liens Uptobox'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH_MOVIES = ('search?sort=size&order=desc&q=', 'showMovies')
URL_SEARCH_SERIES = ('search?sort=id&order=asc&q=', 'showSeries')
URL_SEARCH_ANIMS = ('search?sort=id&order=asc&q=', 'showAnims')

MOVIE_MOVIE = ('films', 'load')
SERIE_SERIES = ('series', 'load')


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if not 'series' in sUrl:
        oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
        oOutputParameterHandler.addParameter('sMovieTitle', 'movie')
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

    if not 'films' in sUrl:
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
    if sSearchText:
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


def getContent(sUrl):

    sUrl = sUrl.replace(' ', '%20')
    videoId = getAuthorizedID()

    oRequest = cRequestHandler(URL_MAIN + sUrl)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Authorization', videoId)
    sHtmlContent = oRequest.request()

    content = json.loads(sHtmlContent)

#    if content['status'] == 'unauthorized':
    if content['status'] == 'ok':
        return content['items']

    return []


def showMovies(sSearch='', searchLocal = False):
    oGui = cGui()
    oUtil = cUtil()

    if not sSearch:
        searchLocal = True
        oInputParameterHandler = cInputParameterHandler()
        sSearch = oInputParameterHandler.getValue('siteUrl')
    sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
    sSearchText = Unquote(sSearchText)
    sSearchText = oUtil.CleanName(sSearchText)

    sUrl = sSearch.replace('-', '\-').replace('.', '%20')
    content = getContent(sUrl)

    oOutputParameterHandler = cOutputParameterHandler()
    movies = set()
    bMatrix = isMatrix()
    for movie in content:
        sTitle = movie['title']
        if not bMatrix:
            sTitle = sTitle.encode('utf-8')

        # seulement les formats vidéo
        if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
            continue
        # enlever l'extension
        sTitle = sTitle[:-4]

        sTitle = sTitle.replace('CUSTOM', '')
        if '1XBET' in sTitle:  # or 'HDCAM'
            continue

        # recherche des métadonnées
        pos = len(sTitle)
        sTmdbId, pos = getIdTMDB(sTitle, pos)
        if sTmdbId:
            sTitle = sTitle.replace('.TM%sTM.' % sTmdbId, '')
            pos = len(sTitle)

        sYear, pos = getYear(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)
        sTitle, sa, ep = getSaisonEpisode(sTitle)

        # enlever les séries
        if not sa or not ep:
            sTitle = sTitle[:pos]
            sTitle, sa, ep = getSaisonEpisode(sTitle)
        if sa or ep:
            continue

        sMovieTitle = sTitle[:pos]
        sMovieTitle = oUtil.unescape(sMovieTitle).strip()
        sMovieTitle = sMovieTitle.replace('.', ' ')

        if not oUtil.CheckOccurence(sSearchText, sMovieTitle):
            continue    # Filtre de recherche

        # lien de recherche spécifique à chaque film
        siteUrl = URL_SEARCH_MOVIES[0] + sMovieTitle.replace('-', '\-')
        startWith = sMovieTitle[0].upper()
        if startWith.isdigit():
            startWith = 'number'
        siteUrl += '&start\-with=' + startWith

        sSearchTitle = oUtil.CleanName(sMovieTitle)
        if sYear:
            sSearchTitle += ' (%s)' % sYear

        if sSearchTitle in movies:
            continue                # film déjà proposé

        movies.add(sSearchTitle)
        
        oOutputParameterHandler.clearParameter()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sSearchTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
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

    series = set()
    oOutputParameterHandler = cOutputParameterHandler()
    
    # deux url pour plus de résultats
    urls = [sUrl, sUrl.replace('order=asc', 'order=desc')]
    bMatrix = isMatrix()
    for sUrl in urls:
        content = getContent(sUrl)
        for file in content:
            sTitle = file['title']
            if not bMatrix:
                sTitle = sTitle.encode('utf-8')

            if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                continue
            # enlever l'extension
            sTitle = sTitle[:-4]

            # recherche des métadonnées
            pos = len(sTitle)
            sTmdbId, pos = getIdTMDB(sTitle, pos)
            if sTmdbId:
                sTitle = sTitle.replace('.TM%sTM.' % sTmdbId, '')
                pos = len(sTitle)
            sYear, pos = getYear(sTitle, pos)
            sRes, pos = getReso(sTitle, pos)
            sLang, pos = getLang(sTitle, pos)
            sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)

            # Recherche des noms de séries
            if not saison or not episode:
                sTitle = sTitle[:pos]
                pos = len(sTitle)
                sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)

            if saison:
                if int(saison) > 100:
                    continue
                sTitle = sTitle[:pos]
                sDisplayTitle = oUtil.unescape(sTitle).strip()
                sDisplayTitle = sDisplayTitle.replace('.', ' ')
                
                if not oUtil.CheckOccurence(sSearchTitle, sDisplayTitle):
                    continue    # Filtre de recherche
                
                sMovieTitle = oUtil.CleanName(sDisplayTitle)
                if sYear:
                    sMovieTitle += ' (%s)' % sYear
                if sMovieTitle in series:
                    continue
                series.add(sMovieTitle)
    
                oOutputParameterHandler.clearParameter()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)  # Utilisé par TMDB
                if isAnime:
                    oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', '', '', oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', '', '', oOutputParameterHandler)

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
    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    else:
        sSearchYear = oInputParameterHandler.getValue('sYear')

    # recherche depuis le titre sélectionné, pas depuis les mots clefs recherchés
    sUrl = URL_SEARCH_SERIES[0] + sSearchTitle.replace('-', '\-')
    startWith = sSearchTitle[0].upper()
    if startWith.isdigit():
        startWith = 'number'
    sUrl += '&start\-with=' + startWith

    # deux url pour plus de résultats
    urls = [sUrl, sUrl.replace('order=asc', 'order=desc')]

    bMatrix = isMatrix()
    for sUrl in urls:
        content = getContent(sUrl)

        # Recherche des saisons
        for file in content:
            sTitle = file['title']
            if not bMatrix:
                sTitle = sTitle.encode('utf-8')

            if sTitle[-4] == '.':
                if sTitle[-4:].lower() not in '.mkv.avi.mp4.m4v.iso':
                    continue
                # enlever l'extension
                sTitle = sTitle[:-4]

            # recherche des métadonnées
            pos = len(sTitle)
            sTmdbId, pos = getIdTMDB(sTitle, pos)
            if sTmdbId:
                sTitle = sTitle.replace('.TM%sTM.' % sTmdbId, '')
                pos = len(sTitle)
            sYear, pos = getYear(sTitle, pos)
            sRes, pos = getReso(sTitle, pos)
            sLang, pos = getLang(sTitle, pos)
            sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)

            # vérifier l'année pour les homonymes
            if sSearchYear:
                if sYear:
                    if sSearchYear != sYear:
                        continue
                else:
                    continue
            elif sYear:
                continue

            # Recherche des noms de séries
            if not saison or not episode:
                sTitle = sTitle[:pos]
                pos = len(sTitle)
                sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)

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
        if sSearchYear:
            sSaisonTitle = '%s (%s)' % (sSaisonTitle, sSearchYear)
            oOutputParameterHandler.addParameter('sYear', sSearchYear)
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

    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    else:
        sSearchYear = oInputParameterHandler.getValue('sYear')

    content = getContent(sUrl)

    # Recherche des épisodes
    bMatrix = isMatrix()
    episodes = set()
    for file in content:
        sTitle = file['title']
        if not bMatrix:
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
        sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)

        # Vérifier la saison
        if not saison or not episode:
            sTitle = sTitle[:pos]
            pos = len(sTitle)
            sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)
        if not saison or saison != sSearchSaison:
            continue

        # Vérifier l'année
        if sSearchYear:
            if sYear:
                if sSearchYear != sYear:
                    continue
            else:
                continue
        elif sYear:
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
        oOutputParameterHandler.addParameter('sYear', sSearchYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():

    from resources.lib.gui.hoster import cHosterGui
    oGui = cGui()
    oHosterGui = cHosterGui()
    hoster = oHosterGui.getHoster('lien_direct')
    oUtil = cUtil()

    oInputParameterHandler = cInputParameterHandler()
    # sSearchTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sSearchTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSearchYear, pos = getYear(sSearchTitle, len(sSearchTitle))
    if sSearchYear:
        sSearchTitle = sSearchTitle[:pos].strip()
    else:
        sSearchYear = oInputParameterHandler.getValue('sYear')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchSaison = ''
    if '|' in sUrl:
        sUrl, sSearchSaison, sSearchEpisode = sUrl.split('|')
        sSearchTitle = sSearchTitle.replace(' S%sE%s' % (sSearchSaison, sSearchEpisode), '')
    sSearchTitle = oUtil.CleanName(sSearchTitle)

    content = getContent(sUrl)
    oHoster = oHosterGui.checkHoster('uptobox') # retourne le bon débrideur en fonction de son compte premmium

    # Recherche les liens
    bMatrix = isMatrix()
    for file in content:
        sTitle = file['title']
        if not bMatrix:
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
        sTmdbId, pos = getIdTMDB(sTitle, pos)
        sLang, pos = getLang(sTitle, pos)
        sRes, pos = getReso(sTitle, pos)
        sYear, pos = getYear(sTitle, pos)

        # identifier une série
        sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)
        if not saison or not episode:
            sTitle = sTitle[:pos]
            pos = len(sTitle)
            sTitle, saison, episode, pos = getSaisonEpisode(sTitle, pos)

        if sSearchSaison:   # recherche de série
            if not saison or saison != sSearchSaison:
                continue
            if not episode or episode != sSearchEpisode:
                continue
        else: # recherche de film
            if saison or episode:
                continue

        # vérifier l'année pour les homonymes
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
        sMovieTitle = sMovieTitle.replace('.', ' ').lower()
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
            sMovieTitle += ' (%s)' % sYear
        sHosterUrl = file['link']

        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        oHosterGui.showHoster(oGui, oHoster, sHosterUrl, '')


    oGui.setEndOfDirectory()


# Recherche saisons et episodes
def getSaisonEpisode(sTitle, pos = 0):
    sTitle = sTitle.replace('x264', '').replace('x265', '').strip()
    sa = ep = terme = ''
    m = re.search('(^S| S|\.S|\[S|saison|\s+|\.)(\s?|\.)(\d+)( *- *|\s?|\.)(E|Ep|x|\wpisode|Épisode)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
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
            m = re.search('( S|\.S|\[S|saison)(\s?|\.)(\d+)', sTitle, re.UNICODE | re.IGNORECASE)
            if m:
                sa = m.group(3)
                if int(sa) > 100:
                    sa = ''
                else:
                    terme = m.group(0)

    if terme:
        p = sTitle.index(terme)
        
        if p<5:             # au début, on retire directement l'élement recherché
            sTitle = sTitle.replace(terme, '')
            if pos:
                pos -= len(terme)
            if sTitle.startswith(']'):
                sTitle = sTitle[1:]
                pos -= 1
        elif p < pos:
            pos = p

    if pos == 0:
        return sTitle, sa, ep
    return sTitle, sa, ep, pos


def getYear(sTitle, pos):
    sPattern = ['[^\w]([0-9]{4})[^\w]']
    return _getTag(sTitle, sPattern, pos)


def getLang(sMovieTitle, pos):
    sPattern = ['VFI', 'VFF', 'VFQ', 'SUBFRENCH', 'TRUEFRENCH', 'FRENCH', 'VF', 'VOSTFR', '[^\w](VOST)[^\w]', '[^\w](VO)[^\w]', 'QC', '[^\w](MULTI)[^\w]', 'FASTSUB']
    return _getTag(sMovieTitle, sPattern, pos)


def getReso(sMovieTitle, pos):
    sPattern = ['HDCAM', '[^\w](CAM)[^\w]', '[^\w](R5)[^\w]', '.(3D)', '.(DVDSCR)', '.(TVRIP)', '.(FHD)', '.(HDLIGHT)', '\d{3,4}P', '.(4K)', '.(UHD)', '.(BDRIP)', '.(BRRIP)', '.(DVDRIP)', '.(HDTV)', '.(BLURAY)', '.(WEB-DL)', '.(WEBRIP)', '[^\w](WEB)[^\w]', '.(DVDRIP)']
    sRes, pos = _getTag(sMovieTitle, sPattern, pos)
    if sRes:
        sRes = sRes.replace('2160P', '4K')
    return sRes, pos

def getIdTMDB(sMovieTitle, pos):
    sPattern = ['.TM(\d+)TM.']
    return _getTag(sMovieTitle, sPattern, pos)

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
            if pos > p > 2: # si ce n'est pas au début
                pos = p
            return ret.upper(), pos
    return False, pos
