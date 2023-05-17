# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import progress, siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'zone_streaming'
SITE_NAME = 'Zone Streaming'
SITE_DESC = 'Médiathèque de chaînes officielles'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'category/seriesweb/', 'showMovies')
WEB_SERIES = (URL_MAIN + 'category/webseries/', 'showMovies')
SERIE_GENRES = (True, 'showSeriesGenres')

REPLAYTV_REPLAYTV = (True, 'load')
REPLAYTV_NEWS = (URL_MAIN + 'category/emissions/', 'showMovies')
REPLAYTV_GENRES = (True, 'showReplayGenres')
SHOW_SHOWS = (URL_MAIN + 'category/spectaclesweb/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', WEB_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, WEB_SERIES[1], 'Webséries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries & Webséries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Emissions', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SHOW_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, SHOW_SHOWS[1], 'Spectacles', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Replay (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []

    # Catégorie Longs métrages
    liste.append(['[COLOR yellow]Longs métrages[/COLOR]', 'category/films/longs-metrages/'])
    liste.append(['Action', 'category/films/longs-metrages/action-longs-metrages/'])
    liste.append(['Animation', 'category/films/longs-metrages/animation-longs-metrages/'])
    liste.append(['Aventure', 'category/films/longs-metrages/aventure-longs-metrages/'])
    liste.append(['Cinématiques', 'category/films/longs-metrages/cinematiques-jeux-video-longs-metrages/'])
    liste.append(['Comédie', 'category/films/longs-metrages/comedies-longs-metrages/'])
    liste.append(['Documentaires', 'category/films/longs-metrages/documentaires/'])
    liste.append(['Drame', 'category/films/longs-metrages/drame-longs-metrages/'])
    liste.append(['Historique', 'category/films/longs-metrages/historique-longs-metrages/'])
    liste.append(['Horreur', 'category/films/longs-metrages/horreur-longs-metrages/'])
    liste.append(['Romance', 'category/films/longs-metrages/romance-longs-metrages/'])
    liste.append(['Science fiction', 'category/films/longs-metrages/science-fiction-longs-metrages/'])
    liste.append(['Thriller', 'category/films/longs-metrages/thriller-longs-metrages/'])

    # Catégorie Moyens métrages
    liste.append(['[COLOR yellow]Moyens métrages[/COLOR]', 'category/films/moyens-metrages/'])
    liste.append(['Aventure', 'category/films/moyens-metrages/aventure-moyens-metrages/'])
    liste.append(['Comédie', 'category/films/moyens-metrages/comedie-moyens-metrages/'])
    liste.append(['Documentaires', 'category/films/moyens-metrages/documentaire-moyens-metrages/'])
    liste.append(['Horreur', 'category/films/moyens-metrages/horreur-moyens-metrages/'])
    liste.append(['Thriller', 'category/films/moyens-metrages/thriller-moyens-metrages/'])

    # Catégorie Courts métrages
    liste.append(['[COLOR yellow]Courts métrages[/COLOR]', 'category/films/courts-metrages/'])
    liste.append(['Action', 'category/films/courts-metrages/action-courts-metrages/'])
    liste.append(['Aventure', 'category/films/courts-metrages/aventure-courts-metrages/'])
    liste.append(['Comédie', 'category/films/courts-metrages/comedie-courts-metrages/'])
    liste.append(['Documentaires', 'category/films/courts-metrages/documentaires-courts-metrages/'])
    liste.append(['Drame', 'category/films/courts-metrages/drame-courts-metrages/'])
    liste.append(['Fantastique', 'category/films/courts-metrages/fantastique-courts-metrages/'])
    liste.append(['Guerre', 'category/films/courts-metrages/guerre-courts-metrages/'])
    liste.append(['Horreur', 'category/films/courts-metrages/horreur-courts-metrages/'])
    liste.append(['Science fiction', 'category/films/courts-metrages/science-fiction-courts-metrages/'])
    liste.append(['Thriller', 'category/films/courts-metrages/thriller-courts-metrages/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []

    # Catégorie Series
    liste.append(['[COLOR yellow]Séries[/COLOR]', 'category/seriesweb/'])
    liste.append(['Action', 'category/seriesweb/action-series/'])
    liste.append(['Animation', 'category/seriesweb/animation-series/'])
    liste.append(['Aventure', 'category/seriesweb/aventure-series/'])
    liste.append(['Comédie', 'category/seriesweb/comedie-series/'])
    liste.append(['Documentaires', 'category/seriesweb/documentaires-series/'])
    liste.append(['Drame', 'category/seriesweb/drame-series/'])
    liste.append(['Fantastique', 'category/seriesweb/fantastique-series/'])
    liste.append(['Manga', 'category/seriesweb/manga-series/'])
    liste.append(['Romance', 'category/seriesweb/romance-series/'])
    liste.append(['Science fiction', 'category/seriesweb/science-fiction-series/'])
    liste.append(['Thriller', 'category/seriesweb/thriller-series/'])

    # Catégorie Webseries
    liste.append(['[COLOR yellow]WebSéries[/COLOR]', 'category/webseries/'])
    liste.append(['Action', 'category/webseries/action-webseries/'])
    liste.append(['Comédie', 'category/webseries/comedie-webseries/'])
    liste.append(['Documentaires', 'category/webseries/documentaires-webseries/'])
    liste.append(['Drame', 'category/webseries/drame-webseries/'])
    liste.append(['Fantastique', 'category/webseries/fantastique-webseries/'])
    liste.append(['Histoire', 'category/webseries/histoire-webseries/'])
    liste.append(['Musical', 'category/webseries/musical-webseries/'])
    liste.append(['Romance', 'category/webseries/romance-webseries/'])
    liste.append(['Science fiction', 'category/webseries/science-fiction-webseries/'])
    liste.append(['Social', 'category/webseries/social-webseries/'])
    liste.append(['Sport', 'category/webseries/sport-webseries/'])
    liste.append(['Thriller', 'category/webseries/thriller-webseries/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showReplayGenres():
    oGui = cGui()

    liste = []
    # Catégorie emission
    liste.append(['[COLOR yellow]Emissions[/COLOR]', 'category/emissions/'])
    liste.append(['Actualité', 'category/emissions/actualite-emissions/'])
    liste.append(['Automobile', 'category/emissions/automobile-emissions/'])
    liste.append(['Cuisine', 'category/emissions/cuisine-emissions/'])
    liste.append(['Culture', 'category/emissions/culture-emissions/'])
    liste.append(['Découverte', 'category/emissions/decouverte-emissions/'])
    liste.append(['Histoire', 'category/emissions/histoire-emissions/'])
    liste.append(['Investigation', 'category/emissions/investigation-emissions/'])
    liste.append(['Jardinage', 'category/emissions/jardinage-emissions/'])
    liste.append(['Société', 'category/emissions/societe-emissions/'])
    liste.append(['Sport', 'category/emissions/sport-emissions/'])
    liste.append(['Télé-réalité', 'category/emissions/tele-realite-emissions/'])
    liste.append(['Voyage', 'category/emissions/voyage-emissions/'])
    # Catégorie spectacle
    liste.append(['[COLOR yellow]Spectacles[/COLOR]', 'category/spectaclesweb/'])
    liste.append(['Concerts', 'category/spectaclesweb/concerts/'])
    liste.append(['Humour', 'category/spectaclesweb/humour-spectacles/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = 'post-thumbnail".+?href="([^"]+).+?src="(http[^"]+).+?bookmark">([^<]+).+?<p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sDesc = aEntry[3].replace('&#46;', '.')

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    # &raquo; == >> traité dans parser
    sPattern = 'pages\'>Page.+?sur ([^<]+?)<.+?href="([^"]+?)">>><'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            watchUrl = 'https://www.youtube.com/watch?v='

            if 'videoseries?list=' in aEntry:
                idList = re.sub('https:.+?list=', '', aEntry)

                sUrl = 'https://invidious.fdn.fr/playlist?list=' + idList
                oRequestHandler = cRequestHandler(sUrl)
                sHtmlContent = oRequestHandler.request()

                sPattern1 = ' class="thumbnail" src="(.+?)".+?<p dir="auto">(.+?)</p>.+? <a.+?href="(.+?)"'
                aResult1 = oParser.parse(sHtmlContent, sPattern1)

                if aResult1[0] is True:
                    for aEntry in aResult1[1]:
                        sHosterUrl = aEntry[2]
                        sThumb = 'https://invidious.fdn.fr' + aEntry[0]
                        sTitle = aEntry[1].replace('EP.', 'E').replace('Ep. ', 'E').replace('Ep ', 'E')
                        sTitle = sTitle.replace('|', '-')

                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:
                link = re.sub('.+?embed/', '', aEntry)
                link = link.replace('?rel=0', '')
                sHosterUrl = watchUrl + link
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
