# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import json

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager, addon
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'french_stream'
SITE_NAME = 'French Stream'
SITE_DESC = 'Films & séries'

MOVIE_NEWS = ('films/', 'showMovies')
MOVIE_GENRES = ('films/', 'showMovieGenres')
MOVIE_VIEWS = ('films/top-film/', 'showMovies')
MOVIE_THEMES = ('films/', 'showMovieThemes')

SERIE_NEWS = ('s-tv/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_DIFFUSEURS = ('s-tv/', 'showSerieDiffuseurs')
SERIE_VIEWS = ('s-tv/sries-du-moment/', 'showMovies')
SERIE_THEMES = ('s-tv/', 'showMovieThemes')

DOC_DOCS = (True, 'showMenuDocs')
DOC_NEWS = (True, 'showMenuDocs')
DOC_FILMS = ('films/documentaires/', 'showMovies')
DOC_SERIES = ('documentaire-serie-/', 'showMovies')

DRAMA_DRAMAS = ('k-drama-/', 'showMovies')
DRAMA_NEWS = ('k-drama-/', 'showMovies')

REPLAYTV_REPLAYTV = ('streaming-tv-realits/', 'showMovies')
REPLAYTV_NEWS = ('streaming-tv-realits/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = ('index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')
URL_SEARCH_DRAMAS = (key_search_series, 'showMovies')
URL_SEARCH_MISC = (key_search_movies, 'showMovies')  # Documentaires
URL_SEARCH_REPLAY = (key_search_series, 'showMovies')

# recherche utilisée quand on utilise directement la source
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

def getUrlMain():
    siteInfo = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'site_info')
    if siteInfo:
        oRequestHandler = cRequestHandler(siteInfo)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'a href="([^"]+)" class="url-display"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sUrl = aResult[1][0]
            if not sUrl.endswith('/'):
                sUrl = sUrl + '/'
            return sUrl
    
    return siteManager().getUrlMain(SITE_IDENTIFIER)
    

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay TV', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], addons.VSlang(30101), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_THEMES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_THEMES[1], 'Thèmes', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], addons.VSlang(30101), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DIFFUSEURS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_DIFFUSEURS[1], addons.VSlang(30467), 'diffuseur.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_THEMES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_THEMES[1], 'Thèmes', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuDocs():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_FILMS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_FILMS[1], 'Films documentaires', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_SERIES[1], 'Séries documentaires', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = []
    listegenre = ['action', 'animation', 'arts+martiaux', 'aventure', 'biopic', 'comedie', 'drame', 'documentaire',
                  'epouvante-horreur', 'espionnage', 'famille', 'fantastique', 'guerre', 'historique', 'policier',
                  'romance', 'science-fiction', 'thriller', 'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize().replace('+',' '), 'xfsearch/genre-1/' + igenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieThemes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    URL_MAIN = getUrlMain()
    oRequest = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequest.request()

    # un cookie est necessaire ?
    sPattern = 'document.cookie="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        cookie = aResult[1][0]
        oRequest.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequest.request()
    
    if 's-tv/' in sUrl:
        sHtmlContent = oParser.abParse(sHtmlContent, 'Par Theme</div>', '</div>')
    else:
        sHtmlContent = oParser.abParse(sHtmlContent, 'Par Thème</div>', '</div>')
    listeTheme = oParser.parse(sHtmlContent, 'href="([^"]+).+?</i> *([^<]+)<')
    if listeTheme[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        themes = sorted(listeTheme[1], key = lambda theme:theme[1]) 
        for theme in themes:
            oOutputParameterHandler.addParameter('siteUrl', theme[0])
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', theme[1], 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'action-serie'], ['Animation', 'animation-serie'], ['Aventure', 'aventure-series'],
             ['Biopic', 'serie-biopic'], ['Comédie', 'comedie-serie'], ['Documentaire', 'documentaire-serie'], ['Drame', 'drame-serie'],
             ['Famille', 'familles-series'], ['Fantastique', 'fantastique-series'], ['Historique', 'serie-historiques'],
             ['Horreur', 'horreur-serie'], ['Judiciaire', 'judiciare-series'], ['K-Drama', 'k-drama'], ['Médical', 'medical-series'],
             ['Policier', 'policier-series'], ['Romance', 'romance-series'], ['Science-fiction', 'science-fiction-series'],
             ['Thriller', 'thriller-series'], ['Western', 'western-series']]


    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '-/')
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieDiffuseurs():
    oGui = cGui()
    liste = [['Amazon Prime', 1024, 's-tv/serie-amazon-prime-videos'],
             ['Apple TV', 2552, 's-tv/series-apple-tv/'],
             ['Disney+', 2739, 's-tv/series-disney-plus/'],
             ['Netflix', 213, 's-tv/netflix-series-']]


    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for networkName, networkId, sUrlDiff in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sUrlDiff)
        oOutputParameterHandler.addParameter('sTmdbId', networkId)  # Utilisé par TMDB
        oGui.addNetwork(SITE_IDENTIFIER, 'showMovies', networkName, 'diffuseur.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()
    URL_MAIN = getUrlMain()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
#        sSearch = sSearch.replace(' ', '+').replace('%20', '+')

        if key_search_movies in sSearch:
#            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
#            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        sUrl = URL_MAIN + 'engine/ajax/search.php'
        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParameters('query', sSearchText)
        sHtmlContent = oRequest.request()

        # un cookie est necessaire ?
        sPattern = 'document.cookie="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            cookie = aResult[1][0]
            oRequest.addHeaderEntry('Cookie', cookie)
            sHtmlContent = oRequest.request()
            
        sPattern = "href='([^']+).+?src='([^']+).+?title *'>([^<]+)"
    else:
        for serieIN in ['-serie', 'serie-', '=series', '-drama', 's-tv', '-tv-', 's-vost', 'sries-', 'xx89']:
            if serieIN in sUrl:
                bSearchSerie = True
                break
        # if '-serie' in sUrl or 'serie-' in sUrl or '-drama' in sUrl or 's-tv' in sUrl or '-tv-' in sUrl or 's-vost' in sUrl or 'sries-' in sUrl or 'xx89' in sUrl:
        #     bSearchSerie = True
        oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()
        
        # un cookie est necessaire ?
        sPattern = 'document.cookie="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            cookie = aResult[1][0]
            oRequestHandler.addHeaderEntry('Cookie', cookie)
            sHtmlContent = oRequestHandler.request()
        
        sPattern = 'with-mask" href="([^"]+).+?src="([^"]*).+?title">([^<]+)'
    
    aResult = oParser.parse(sHtmlContent, sPattern)

    seriesTitle = []

    if aResult[0]:
            
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sThumb = aEntry[1].replace('/red.php?src=', '').replace('&.webp', '')
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = aEntry[2].replace('Saisn', 'Saison').replace('\\', '')
            sTitle = oUtil.unescape(sTitle)
            
            sYear = None
            hasYear = re.search('\((\d{4})\)', sTitle)
            if hasYear:
                sYear = hasYear.group(1)
                sTitle = sTitle.replace('(%s)' % sYear, '')

            if bSearchMovie:  # il n'y a jamais '/serie' dans sUrl2
                if '- Saison' in sTitle:
                    continue
            if bSearchSerie:
                if '- Saison' not in sTitle:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if bSearchSerie:
                sTitle = sTitle.split('- Saison')[0]
                sUniqueTitle = oUtil.CleanName(sTitle)
                if sUniqueTitle in seriesTitle:
                    continue        # une seule fois la série, on choisi la saison ensuite

                seriesTitle.append(sUniqueTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '(\d+)</a>\s*</span><span class="pnext"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        result = re.search('cstart=(\d+)', sNextPage)
        sNumberNext = result.group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oUtil = cUtil()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSaisonThumb = oInputParameterHandler.getValue('sThumb')

    URL_MAIN = getUrlMain()
    if 'http' not in siteUrl:
        sUrl = URL_MAIN + siteUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # un cookie est necessaire ?
    sPattern = 'document.cookie="([^"]+)"'
    cookie = ''
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        cookie = aResult[1][0]
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequestHandler.request()
    
    sPattern = 'class="sd-tagz"><a href=.+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        serieTag = aResult[1][0]
        oRequest = cRequestHandler(URL_MAIN + 'engine/ajax/get_seasons.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addHeaderEntry('Cookie', cookie)
        oRequest.addParameters('serie_tag', serieTag)
        content = oRequest.request()
        if content and '"error"' not in content:
            saisonsList = json.loads(content)
            
            # si pas de saison, au moins la saison 1
            if len(saisonsList) == 0:
                saisonsList.append(json.loads('{"title": "%s Saison 1","full_url": "%s"}' % (sMovieTitle, siteUrl)))
            else: # trie des saisons
                saisonsList = sorted(saisonsList, key=trieSaison)

            oOutputParameterHandler = cOutputParameterHandler()
            for saison in saisonsList:
                sUrl = saison['full_url']
                sDisplayTitle = saison['title']
                sDisplayTitle = oUtil.unescape(sDisplayTitle)
                sThumb = saison.get('affiche', sSaisonThumb)
    
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def trieSaison(item):
    m = re.search(r'aison (\d+)', item['title'])
    if m:
        return int(m.group(1))
    return 0


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    URL_MAIN = getUrlMain()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # un cookie est necessaire ?
    cookie = ''
    sPattern = 'document.cookie="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        cookie = aResult[1][0]
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="fdesc" *> *<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = ''
    if aResult[0]:
        sDesc = aResult[1][0].strip()

    # 1ere méthode
    sPattern = 'data-news-id="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        numEpisodes = []
        sAPIUrl = '%sengine/ajax/sx.php?p=%s' % (URL_MAIN, aResult[1][0])
        oRequestHandler = cRequestHandler(sAPIUrl)
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequestHandler.request()
        episodeList = json.loads(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        for sLang in episodeList:
            if 'info' in sLang:
                continue
            for sEpisode in episodeList[sLang]:
                if sEpisode in numEpisodes:
                    continue
                found = False   # on garde les numéros d'épisodes qui ont au moins un lien, quelque soit la langue
                sHosterList = episodeList[sLang][sEpisode]
                for sHosterName in sHosterList:
                    if sHosterList[sHosterName]:
                        numEpisodes.append(sEpisode)
                        found = True
                        break
                if found:
                    sTitle = sMovieTitle + ' Episode ' + sEpisode
                    sDisplayTitle = sTitle
                    oOutputParameterHandler.addParameter('siteUrl', sUrl + "|" + sEpisode)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodeLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return
            
    # 2eme méthode
    sPatternEps = '<div id="episodes-info-data"'
    aResult= oParser.parse(sHtmlContent, sPatternEps)
    if aResult[0]:
        sHtmlContent = oParser.abParse(sHtmlContent, sPatternEps, '</div></div>')
#        aResult= oParser.parse(sHtmlContent, '<div data-ep="(\d+)"(.+?)</div')
        aResult= oParser.parse(sHtmlContent, '<div data-ep="(\d+)" data-title="([^"]+)" data-synopsis="([^"]*)" data-poster="([^"]*)">')

        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for episode in aResult[1]:
                numEp = episode[0]
                sDisplayTitle = sTitle = '%s Episode %s' % (sMovieTitle, numEp)
                sDesc = episode[2]
                sThumb = episode[3]
                oOutputParameterHandler.addParameter('siteUrl', sUrl + "|" + numEp)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodeLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
        oGui.setEndOfDirectory()
        return
    
    # 3eme méthode
    sPatternEps = 'var episodesData = ({.+?);'
    aResultTab = oParser.parse(sHtmlContent, sPatternEps)
    if aResultTab[0]:
        numEpisodes = []
        # formattage en JSON
        content = '{' + aResultTab[1][0].replace(' ', '') + '}'
        content = aResultTab[1][0].replace(' ', '')
        content = content.replace('=', ':').replace(':{', '":{')
        content = content.replace('{', '{"').replace(',', ',"').replace(':"', '":"')
        content = content.replace('{"}', '{}').replace(',"}', ',}').replace('},}', '}}')
        episodeList = json.loads(content)

        oOutputParameterHandler = cOutputParameterHandler()
        for sLang in episodeList:
            for sEpisode in episodeList[sLang]:
                if sEpisode in numEpisodes:
                    continue
                found = False   # on garde les numéros d'épisodes qui ont au moins un lien, quelque soit la langue
                sHosterList = episodeList[sLang][sEpisode]
                for sHosterName in sHosterList:
                    if sHosterList[sHosterName]:
                        numEpisodes.append(sEpisode)
                        found = True
                        break
                if found:
                    sTitle = sMovieTitle + ' Episode ' + sEpisode
                    sDisplayTitle = sTitle
                    oOutputParameterHandler.addParameter('siteUrl', sUrl + "|" + sEpisode)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodeLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodeLinks():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sUrl, sEpSearch = sUrl.split('|')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # un cookie est necessaire ?
    cookie = ''
    sPattern = 'document.cookie="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        cookie = aResult[1][0]
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequestHandler.request()

    # 1ere méthode
    sPattern = 'data-news-id="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        URL_MAIN = getUrlMain()
        sUrl = '%sengine/ajax/sx.php?p=%s' % (URL_MAIN, aResult[1][0])
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequestHandler.request()
        episodeList = json.loads(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        for sLang in episodeList:
            if 'info' in sLang:
                continue
            for sEpisode in episodeList[sLang]:
                if sEpisode != sEpSearch:
                    continue
                sHosterList = episodeList[sLang][sEpisode]
                for sHosterName in sHosterList:
                    oHoster = oHosterGui.checkHoster(sHosterName)
                    if oHoster:
                        sHosterUrl = sHosterList[sHosterName]
                        
                        if 'uptostream' in sHosterUrl:
                            continue
                        
                        if sHosterUrl:
                            if 'Player.php' in sHosterUrl:
                                sDisplayTitle = '%s (%s) [COLOR skyblue]%s[/COLOR]' % (sMovieTitle, sLang.upper(), sHosterName) 
                                oOutputParameterHandler = cOutputParameterHandler()
                                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                                oOutputParameterHandler.addParameter('sThumb', sThumb)
                                oOutputParameterHandler.addParameter('sLang', sLang)
                                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler)
                            else:
                                sTitle = '%s (%s)' % (sMovieTitle, sLang.upper())
                                oHoster.setDisplayName(sTitle)
                                oHoster.setFileName(sMovieTitle)
                                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)
                break
        oGui.setEndOfDirectory()
        return

    # 2eme méthode
    sPatternEps = '<div id="episodes-vf-data"'
    if sPatternEps in sHtmlContent:
        sPatternLink = 'data-(.+?)="([^"]+)'
        for sLang, patternLang in [('VF', sPatternEps), ('VOSTFR', 'episodes-vostfr-data'), ('VO', 'episodes-vo-data')]:
            sContentLang = oParser.abParse(sHtmlContent, patternLang, '</div></div>')
            aResult= oParser.parse(sContentLang, '<div data-ep="(\d+)"(.+?)>')
            if aResult[0]:
                for numEp, links in aResult[1]:
                    if numEp != sEpSearch:
                        continue
                    if 'http' not in links:
                        break
                    
                    aResultLink = oParser.parse(links, sPatternLink)
                    if aResultLink[0]:
                        oOutputParameterHandler = cOutputParameterHandler()
                        for sHosterName, sHosterUrl in aResultLink[1]:
                            oHoster = oHosterGui.checkHoster(sHosterName)
                            if oHoster :
                                sDisplayTitleLang =  sMovieTitle
                                if sLang:
                                    sDisplayTitleLang +=  ' [%s]' % sLang.upper()
                                
                                if "flixeo" in sHosterUrl:
                                    oRequestHandler = cRequestHandler(sHosterUrl)
                                    oRequestHandler.request()
                                    sHosterUrl = oRequestHandler.getRealUrl()
                
                                if 'Player.php' in sHosterUrl:
                                    sDisplayTitleLang += ' [COLOR skyblue]%s[/COLOR]' % oHoster.getDisplayName() 
                                    oOutputParameterHandler = cOutputParameterHandler()
                                    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitleLang, sThumb, sDesc, oOutputParameterHandler)
                                else:
                                    oHoster.setDisplayName(sDisplayTitleLang)
                                    oHoster.setFileName(sMovieTitle)
                                    oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)
                    
                    break
    
        oGui.setEndOfDirectory()
        return

    # 3eme méthode
    sPatternList = 'var episodesData = ({.+?);'
    aResultTab = oParser.parse(sHtmlContent, sPatternList)
    if aResultTab[0]:

        # formattage en JSON
        content = '{' + aResultTab[1][0].replace(' ', '') + '}'
        content = aResultTab[1][0].replace(' ', '')
        content = content.replace('=', ':').replace(':{', '":{')
        content = content.replace('{', '{"').replace(',', ',"').replace(':"', '":"')
        content = content.replace('{"}', '{}').replace(',"}', ',}').replace('},}', '}}')
        episodeList = json.loads(content)

        for sLang in episodeList:
            for sEpisode in episodeList[sLang]:
                if sEpisode != sEpSearch:
                    continue

                sHosterList = episodeList[sLang][sEpisode]
                for sHosterName in sHosterList:
                    oHoster = oHosterGui.checkHoster(sHosterName)
                    if oHoster:
                        sHosterUrl = sHosterList[sHosterName]
                        if sHosterUrl:
                            if 'Player.php' in sHosterUrl:
                                sDisplayTitle = '%s (%s) [COLOR skyblue]%s[/COLOR]' % (sMovieTitle, sLang.upper(), sHosterName) 
                                oOutputParameterHandler = cOutputParameterHandler()
                                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                                oOutputParameterHandler.addParameter('sThumb', sThumb)
                                oOutputParameterHandler.addParameter('sLang', sLang)
                                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler)
                            else:
                                sTitle = '%s (%s)' % (sMovieTitle, sLang.upper())
                                oHoster.setDisplayName(sTitle)
                                oHoster.setFileName(sMovieTitle)
                                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)
                break

    oGui.setEndOfDirectory()


def showMovieLinks():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oParser = cParser()

    URL_MAIN = getUrlMain()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # un cookie est necessaire ?
    cookie = ''
    sPattern = 'document.cookie="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        cookie = aResult[1][0]
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    # premiere méthode
    sPattern = 'data-newsid="(\d+)"'
    # data-newsid="15124374"
    # data-title="F- la Saint-Valentin"
    # data-fulllink="/films/15124374-f-la-saint-valentin.html"
    aResultId = oParser.parse(sHtmlContent, sPattern)
    if aResultId[0]:
        urlAPI = '%sengine/ajax/film_api.php?id=%s' % (URL_MAIN, aResultId[1][0])
        oRequestHandler = cRequestHandler(urlAPI)
        oRequestHandler.addHeaderEntry('Cookie', cookie)
        jsonContent = oRequestHandler.request()
        hostersLink = json.loads(jsonContent).get('players', [])
        for hosterName, hosterLinks in hostersLink.items():
            # hoster FSVID, non géré 
            if 'premium' in hosterName:
                #hosterName = aEntry[0].replace('premium', 'fsvid')
                continue    # hoster fsvid à revoir

            oHoster = oHosterGui.checkHoster(hosterName)
            if not oHoster :
                continue

            links = [] # filtre des urls en double
            for sLang, sHosterUrl in hosterLinks.items():
            
                if sHosterUrl in links:
                    continue
                links.append(sHosterUrl)
                    
                sDisplayTitleLang =  sMovieTitle
                if sLang and 'default' not in sLang:
                    sDisplayTitleLang +=  ' [%s]' % sLang.upper()
                
                if "flixeo" in sHosterUrl:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()

                if 'Player.php' in sHosterUrl:
                    sDisplayTitleLang += ' [COLOR skyblue]%s[/COLOR]' % oHoster.getPluginIdentifier() 
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitleLang, sThumb, '', oOutputParameterHandler)
                else:
                    oHoster.setDisplayName(sDisplayTitleLang)
                    oHoster.setFileName(sMovieTitle)
                    oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

        oGui.setEndOfDirectory()
        return

    sHtmlContent = oParser.abParse(sHtmlContent, '<div id="film-data"', 'div>')
    sPattern = 'data-([^=]+)="(https[^"]+)'
    aResultHoster = oParser.parse(sHtmlContent, sPattern)
    
    # deuxieme méthode
    if aResultHoster[0]:
        links = [] # filtre des urls en double
        for aEntry in aResultHoster[1]:
            hosterName = aEntry[0]
            if 'premium' in hosterName:
                #hosterName = aEntry[0].replace('premium', 'fsvid')
                continue    # hoster fsvid à revoir
            if 'affiche' in hosterName:
                continue

            sHosterUrl = aEntry[1]
            if sHosterUrl in links:
                continue
            links.append(sHosterUrl)
                    
            sLang = None
            for lang in ('vfq', 'vff', 'vostfr'):
                if lang in hosterName:
                    sLang = lang
                    hosterName = hosterName.replace(lang, '')
                    break

            oHoster = oHosterGui.checkHoster(hosterName)
            if oHoster :
                sDisplayTitleLang =  sMovieTitle
                if sLang:
                    sDisplayTitleLang +=  ' [%s]' % sLang.upper()
                
                if "flixeo" in sHosterUrl:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()

                if 'Player.php' in sHosterUrl:
                    sDisplayTitleLang += ' [COLOR skyblue]%s[/COLOR]' % oHoster.getDisplayName() 
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitleLang, sThumb, '', oOutputParameterHandler)
                else:
                    oHoster.setDisplayName(sDisplayTitleLang)
                    oHoster.setFileName(sMovieTitle)
                    oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

        oGui.setEndOfDirectory()
        return

    # troisieme méthode
    sHtmlContent = oParser.abParse(sHtmlContent, 'playerUrls = {', '};')
    sPattern = '"([^"]+)": {([^}]+)'
    aResultHoster = oParser.parse(sHtmlContent, sPattern)
    
    if aResultHoster[0]:
        for aEntry in aResultHoster[1]:
            hosterName = aEntry[0]
            if 'Premium' in hosterName:
                #hosterName = aEntry[0].replace('Premium', 'fsvid')
                continue    # hoster fsvid à revoir

            oHoster = oHosterGui.checkHoster(hosterName)
            if oHoster :
                links = aEntry[1]
                sPattern = '([^"]+)": "([^"]+)"'
                aResultLink = oParser.parse(links, sPattern)
                if aResultLink[0]:
                    links = []
                    for aEntry in aResultLink[1]:
                        sLang = aEntry[0].replace('Default', '')
                        sHosterUrl = aEntry[1]
                        if not sHosterUrl:
                            continue
                        if sHosterUrl in links:
                            continue
                        links.append(sHosterUrl)
                        sDisplayTitleLang =  '%s [%s]' % (sMovieTitle, sLang.upper())
                        
                        if "flixeo" in sHosterUrl:
                            oRequestHandler = cRequestHandler(sHosterUrl)
                            oRequestHandler.request()
                            sHosterUrl = oRequestHandler.getRealUrl()

                        if 'Player.php' in sHosterUrl:
                            sDisplayTitleLang += ' [COLOR skyblue]%s[/COLOR]' % hosterName 
                            oOutputParameterHandler = cOutputParameterHandler()
                            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitleLang, sThumb, '', oOutputParameterHandler)
                        else:
                            oHoster.setDisplayName(sDisplayTitleLang)
                            oHoster.setFileName(sMovieTitle)
                            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    if '.php?' in sUrl:
        url, params = sUrl.split('?')
        key, value = re.split('=|:', params)
        
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParameters(key, value)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        sHtmlContent = oRequestHandler.request()
        realUrl = oRequestHandler.getRealUrl()
        
        if sHtmlContent and 'ID manquant' not in sHtmlContent and 'Aucun ID' not in sHtmlContent :
            oHoster = cHosterGui().checkHoster(realUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, realUrl, sThumb)

    oGui.setEndOfDirectory()
