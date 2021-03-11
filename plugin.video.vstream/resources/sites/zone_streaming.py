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
from resources.lib.comaddon import progress  # , VSlog

SITE_IDENTIFIER = 'zone_streaming'
SITE_NAME = 'Zone Streaming'
SITE_DESC = 'Médiathèque de chaînes officielles'

URL_MAIN = 'http://www.zone-streaming.fr/'

MOVIE_MOVIE = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'category/seriesweb/', 'showMovies')
WEB_SERIES = (URL_MAIN + 'category/webseries/', 'showMovies')
SERIE_GENRES = (True, 'showSeriesGenres')

REPLAYTV_NEWS = (URL_MAIN + 'category/emissions/', 'showMovies')
REPLAYTV_GENRES = (True, 'showReplayGenres')
SHOW_SHOWS = (URL_MAIN + 'category/spectaclesweb/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
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
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []

    # Categorie Longs métrages
    liste.append(['[COLOR yellow]Longs métrages[/COLOR]', URL_MAIN + 'category/films/longs-metrages/'])
    liste.append(['Action', URL_MAIN + 'category/films/longs-metrages/action-longs-metrages/'])
    liste.append(['Animation', URL_MAIN + 'category/films/longs-metrages/animation-longs-metrages/'])
    liste.append(['Aventure', URL_MAIN + 'category/films/longs-metrages/aventure-longs-metrages/'])
    liste.append(['Cinématiques', URL_MAIN + 'category/films/longs-metrages/cinematiques-jeux-video-longs-metrages/'])
    liste.append(['Comédie', URL_MAIN + 'category/films/longs-metrages/comedies-longs-metrages/'])
    liste.append(['Documentaires', URL_MAIN + 'category/films/longs-metrages/documentaires/'])
    liste.append(['Drame', URL_MAIN + 'category/films/longs-metrages/drame-longs-metrages/'])
    liste.append(['Historique', URL_MAIN + 'category/films/longs-metrages/historique-longs-metrages/'])
    liste.append(['Horreur', URL_MAIN + 'category/films/longs-metrages/horreur-longs-metrages/'])
    liste.append(['Romance', URL_MAIN + 'category/films/longs-metrages/romance-longs-metrages/'])
    liste.append(['Science fiction', URL_MAIN + 'category/films/longs-metrages/science-fiction-longs-metrages/'])
    liste.append(['Thriller', URL_MAIN + 'category/films/longs-metrages/thriller-longs-metrages/'])

    # Categorie Moyens métrages
    liste.append(['[COLOR yellow]Moyens métrages[/COLOR]', URL_MAIN + 'category/films/moyens-metrages/'])
    liste.append(['Aventure', URL_MAIN + 'category/films/moyens-metrages/aventure-moyens-metrages/'])
    liste.append(['Comédie', URL_MAIN + 'category/films/moyens-metrages/comedie-moyens-metrages/'])
    liste.append(['Documentaires', URL_MAIN + 'category/films/moyens-metrages/documentaire-moyens-metrages/'])
    liste.append(['Horreur', URL_MAIN + 'category/films/moyens-metrages/horreur-moyens-metrages/'])
    liste.append(['Thriller', URL_MAIN + 'category/films/moyens-metrages/thriller-moyens-metrages/'])

    # Categorie Courts métrages
    liste.append(['[COLOR yellow]Courts métrages[/COLOR]', URL_MAIN + 'category/films/courts-metrages/'])
    liste.append(['Action', URL_MAIN + 'category/films/courts-metrages/action-courts-metrages/'])
    liste.append(['Aventure', URL_MAIN + 'category/films/courts-metrages/aventure-courts-metrages/'])
    liste.append(['Comédie', URL_MAIN + 'category/films/courts-metrages/comedie-courts-metrages/'])
    liste.append(['Documentaires', URL_MAIN + 'category/films/courts-metrages/documentaires-courts-metrages/'])
    liste.append(['Drame', URL_MAIN + 'category/films/courts-metrages/drame-courts-metrages/'])
    liste.append(['Fantastique', URL_MAIN + 'category/films/courts-metrages/fantastique-courts-metrages/'])
    liste.append(['Guerre', URL_MAIN + 'category/films/courts-metrages/guerre-courts-metrages/'])
    liste.append(['Horreur', URL_MAIN + 'category/films/courts-metrages/horreur-courts-metrages/'])
    liste.append(['Science fiction', URL_MAIN + 'category/films/courts-metrages/science-fiction-courts-metrages/'])
    liste.append(['Thriller', URL_MAIN + 'category/films/courts-metrages/thriller-courts-metrages/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []

    # Categorie Series
    liste.append(['[COLOR yellow]Séries[/COLOR]', URL_MAIN + 'category/seriesweb/'])
    liste.append(['Action', URL_MAIN + 'category/seriesweb/action-series/'])
    liste.append(['Animation', URL_MAIN + 'category/seriesweb/animation-series/'])
    liste.append(['Aventure', URL_MAIN + 'category/seriesweb/aventure-series/'])
    liste.append(['Comédie', URL_MAIN + 'category/seriesweb/comedie-series/'])
    liste.append(['Documentaires', URL_MAIN + 'category/seriesweb/documentaires-series/'])
    liste.append(['Drame', URL_MAIN + 'category/seriesweb/drame-series/'])
    liste.append(['Fantastique', URL_MAIN + 'category/seriesweb/fantastique-series/'])
    liste.append(['Manga', URL_MAIN + 'category/seriesweb/manga-series/'])
    liste.append(['Romance', URL_MAIN + 'category/seriesweb/romance-series/'])
    liste.append(['Science fiction', URL_MAIN + 'category/seriesweb/science-fiction-series/'])
    liste.append(['Thriller', URL_MAIN + 'category/seriesweb/thriller-series/'])

    # Categorie Webseries
    liste.append(['[COLOR yellow]WebSéries[/COLOR]', URL_MAIN + 'category/webseries/'])
    liste.append(['Action', URL_MAIN + 'category/webseries/action-webseries/'])
    liste.append(['Comédie', URL_MAIN + 'category/webseries/comedie-webseries/'])
    liste.append(['Documentaires', URL_MAIN + 'category/webseries/documentaires-webseries/'])
    liste.append(['Drame', URL_MAIN + 'category/webseries/drame-webseries/'])
    liste.append(['Fantastique', URL_MAIN + 'category/webseries/fantastique-webseries/'])
    liste.append(['Histoire', URL_MAIN + 'category/webseries/histoire-webseries/'])
    liste.append(['Musical', URL_MAIN + 'category/webseries/musical-webseries/'])
    liste.append(['Romance', URL_MAIN + 'category/webseries/romance-webseries/'])
    liste.append(['Science fiction', URL_MAIN + 'category/webseries/science-fiction-webseries/'])
    liste.append(['Social', URL_MAIN + 'category/webseries/social-webseries/'])
    liste.append(['Sport', URL_MAIN + 'category/webseries/sport-webseries/'])
    liste.append(['Thriller', URL_MAIN + 'category/webseries/thriller-webseries/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showReplayGenres():
    oGui = cGui()

    liste = []
    # Categorie emission
    liste.append(['[COLOR yellow]Emissions[/COLOR]', URL_MAIN + 'category/emissions/'])
    liste.append(['Actualité', URL_MAIN + 'category/emissions/actualite-emissions/'])
    liste.append(['Automobile', URL_MAIN + 'category/emissions/automobile-emissions/'])
    liste.append(['Cuisine', URL_MAIN + 'category/emissions/cuisine-emissions/'])
    liste.append(['Culture', URL_MAIN + 'category/emissions/culture-emissions/'])
    liste.append(['Découverte', URL_MAIN + 'category/emissions/decouverte-emissions/'])
    liste.append(['Histoire', URL_MAIN + 'category/emissions/histoire-emissions/'])
    liste.append(['Investigation', URL_MAIN + 'category/emissions/investigation-emissions/'])
    liste.append(['Jardinage', URL_MAIN + 'category/emissions/jardinage-emissions/'])
    liste.append(['Société', URL_MAIN + 'category/emissions/societe-emissions/'])
    liste.append(['Sport', URL_MAIN + 'category/emissions/sport-emissions/'])
    liste.append(['Télé-réalité', URL_MAIN + 'category/emissions/tele-realite-emissions/'])
    liste.append(['Voyage', URL_MAIN + 'category/emissions/voyage-emissions/'])
    # Categorie spectacle
    liste.append(['[COLOR yellow]Spectacles[/COLOR]', URL_MAIN + 'category/spectaclesweb/'])
    liste.append(['Concerts', URL_MAIN + 'category/spectaclesweb/concerts/'])
    liste.append(['Humour', URL_MAIN + 'category/spectaclesweb/humour-spectacles/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = 'class="post-thumbnail".+?href="([^"]+).+?src="(http[^"]+).+?title="Permalink.+?>([^<]+)<.+?<p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
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

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    # &raquo; == >> traité dans parser
    sPattern = 'pages\'>Page.+?sur ([^<]+?)<.+?href="([^"]+?)">>><'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
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

    sPattern = '<iframe src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'videoseries?list=' in aEntry:

                idList = aEntry.replace('https://www.youtube-nocookie.com/embed/videoseries?list=', '')\
                               .replace('&cc_load_policy=1', '')

                sUrl = 'https://www.youtube-nocookie.com/list_ajax?style=json&action_get_list=1&list=' + idList
                oRequestHandler = cRequestHandler(sUrl)
                sHtmlContent = oRequestHandler.request()

                page = json.loads(sHtmlContent)
                List_video = page["video"]
                for i in List_video:
                    # VSlog(i["encrypted_id"])
                    # VSlog(i["thumbnail"])
                    # VSlog(i["title"])

                    sUrl = 'https://www.youtube.com/watch?v='
                    sHosterUrl = sUrl + i["encrypted_id"]
                    sThumb = i["thumbnail"]
                    sTitle = i["title"].encode('utf-8').replace('EP.', 'E').replace('Ep. ', 'E').replace('Ep ', 'E')
                    sTitle = sTitle.replace('|', '-')

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:
                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
