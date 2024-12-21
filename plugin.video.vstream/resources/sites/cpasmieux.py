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
SITE_NAME = 'cpasmieux'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('filmstreaming/', 'showMenuMovies')
MOVIE_NEWS = ('filmstreaming/', 'showMovies')
MOVIE_GENRES = (MOVIE_MOVIE[0] + 'genre/', 'showGenres')

SERIE_SERIES = ('seriestreaming/', 'showMenuTvShows')
SERIE_NEWS = ('seriestreaming/', 'showMovies')
SERIE_GENRES = (SERIE_SERIES[0] + 'genre/', 'showSeriesGenres')

URL_SEARCH = ('search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + 'film', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + 'serie', 'showMovies')
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
        sUrl += sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comédie', 'comédie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'familial'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Horreur', 'horreur'],
             ['Musique', 'musique'], ['Mystère', 'mystère'], ['Téléfilm', 'telefilm'],
             ['Romance', 'romance'], ['Science-Fiction', 'science_fiction'], ['Sport', 'sport'], ['Thriller', 'thriller'],
             ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0] + sUrl + '/')
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'adventure'], ['Comédie', 'comédie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'familial'],
             ['Fantastique', 'science_fiction-&-fantastique'], ['Guerre', 'war'], ['Horreur', 'horreur'],
             ['Enfants', 'kids'], ['Musique', 'musique'], ['Mystère', 'mystère'],
             ['Romance', 'romance'], ['Science-Fiction', 'science_fiction'], ['Soap', 'soap'], ['Thriller', 'thriller'],
             ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0] + sUrl + '/')
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()
    bMovie = bShow = isSerie = False
    if sSearch:
        if URL_SEARCH_MOVIES[0] in sSearch:
            bMovie = True
            sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH_MOVIES[0], ''))
        else:
            isSerie = bShow = True
            sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH_SERIES[0], ''))
        sUrl = URL_SEARCH[0] + sSearch.replace(' ', '%20')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        isSerie = SERIE_SERIES[0] in sUrl

    sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url img title
    sPattern = 'mi2-in-link" href="\/([^"]*).+?<img src="\/([^"]*)" *alt="([^"]+)'
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
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2]

            # tri des doublons
            cleanTitle = oUtil.CleanName(sTitle).replace(' ', '')
            if cleanTitle in titles:
                continue
            titles.add(cleanTitle)

            # non fonctionnel
            if 'F1 2024' in sTitle:
                continue

            # filtre search
            if bMovie and 'saison' in sThumb:
                continue
            if bShow and not 'saison' in sThumb:
                continue
            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            if isSerie:
                sMovieTitle = re.sub('  S\d+', '', sTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="navigation">.+?<span>\d+<\/span><a href="\/([^"]+)">.+?>(\d+)<\/a><\/span>'
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
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sDesc = ''

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="seasons">', '<div class="kino-related">')

    # url  /  thumb  /  title
    sPattern = 'href="([^"]+).+?<img src="\/([^"]+).+?figcaption>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            sUrl = aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = sMovieTitle + ' ' + aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="floats clearfix">', '</div></div>')

    # url numEp
    sPattern = 'href="([^"]+).+?span>(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = sMovieTitle + " E" + aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'data-url="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



