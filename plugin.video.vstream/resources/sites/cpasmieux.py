# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'cpasmieux'
SITE_NAME = 'Cpasmieux'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('filmstreaming/', 'showMenuMovies')
MOVIE_NEWS = ('filmstreaming/', 'showMovies')
MOVIE_GENRES = (MOVIE_MOVIE[0] , 'showMovieGenres')

SERIE_SERIES = ('seriestreaming/', 'showMenuTvShows')
SERIE_NEWS = ('seriestreaming/', 'showMovies')
SERIE_GENRES = (SERIE_SERIES[0] , 'showSerieGenres')

URL_SEARCH = (False, 'showMovies')
URL_SEARCH_MOVIES = ('search/%s&cat=movie', 'showMovies')
URL_SEARCH_SERIES = ('search/%s&cat=tv', 'showMovies')
URL_SEARCH_ANIMS = ('search/%s&cat=anime', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl %= sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts martiaux', 'arts-martiaux'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Histoire', 'historique'], ['Horreur', 'horreur'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0] + '/genre/' + sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'],
             ['Comédie', 'comedie'], ['Documentaire', 'documentaire'], ['Drame', 'drame'],
             ['Familial', 'familial'], ['Fantastique', 'fantastique'], ['Guerre', 'war'], ['Horreur', 'horreur'], ['Enfants', 'kids'],
             ['Policier', 'crime'], ['Romance', 'romance'], ['Science-Fiction', 'science_fiction'],
             ['Talk', 'talk'], ['Télé réalité', 'reality'], ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0] + '/genre/' + sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()
    bMovie = bShow = False
    if sSearch:
        sUrl, cat = sSearch.replace(' ', '%20').split('&cat=')
        bMovie = 'movie' in cat
        bShow = 'tv' in cat
        bAnime = 'anime' in cat
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        bShow = SERIE_SERIES[0] in sUrl
        bMovie = not bShow
        bAnime = False

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url img title
    sPattern = 'link" href="([^"]+).+?<img src="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # en cas de recherche vide, deuxieme tentative avec le mot le plus long
    if sSearch and not aResult[0]:
        if ' ' in sSearch:
            termes = sSearch.split(' ')
            termes = sorted(termes, key=lambda terme: len(terme))[::-1]
            sUrl = URL_MAIN + URL_SEARCH[0] + termes[0]
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        titles = set()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            # tri des doublons
            cleanTitle = oUtil.CleanName(sTitle).replace(' ', '')
            if cleanTitle in titles:
                continue
            titles.add(cleanTitle)

            # non fonctionnel
            if 'F1 2024' in sTitle or 'F1 2025' in sTitle:
                continue

            # filtre search
            if 'saison' in sThumb:
                if bMovie:
                    continue
            else:
                if bShow or bAnime:
                    continue

            if not 'http' in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            
            if bShow:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif bAnime:
                oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="navigation">.+?<a href="([^"]+)">>><.+?">(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = ''
    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, 'class="seasons"', 'smart-text-s')

    # url  /  thumb  /  title
    sPattern = '<a href="([^"]+).+?img src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            if not 'http' in sThumb:
                sThumb = URL_MAIN + sThumb
            sTitle = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showMovieHosters()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, 'class="seasons"', 'class="seasons"')

    # url numEp
    sPattern = 'href="([^"]+).+?span>(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = sMovieTitle + " E%s" % aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showMovieHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showMovieHosters()


def showMovieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'data-url="([^"]+)".+?"serv">([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oHosterGui = cHosterGui()
        for aEntry in aResult[1]:
            sHosterUrl = aEntry[0]
            sHosterName = aEntry[1]

            oHoster = oHosterGui.checkHoster(sHosterName)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)
            
    oGui.setEndOfDirectory()
