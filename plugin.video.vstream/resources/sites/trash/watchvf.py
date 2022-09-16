# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

SITE_IDENTIFIER = 'watchvf'
SITE_NAME = 'WatchVF'
SITE_DESC = 'Films en streaming.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'movies/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Aventure', 'aventure'], ['Comédie', 'comedie'], ['Drame', 'drame'],
             ['Epouvante Horreur', 'epouvante-horreur'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Thriller', 'thriller']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'film-genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        oUtil = cUtil()
        sUrl = sSearch.replace(' ', '+') + '&post_type=movie'
        sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH[0], ''))
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent, '', 'class="widget-area sidebar-area movie-sidebar')
    sPattern = 'poster"><a href="([^"]+).+?src="([^"]+).+?title">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
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
            sTitle = re.sub('^Voir', '', aEntry[2].replace(' Film en streaming complet', ''))

            # Si recherche et trop de résultat, on nettoie
            if sSearch and total > 3:
                if not oUtil.CheckOccurence(sSearch, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>(\d+)</a></li>\s*<li><a class="next page-numbers" href="([^"]+)">Next Page'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNextPage = aResult[1][0][1]
        sNumberMax = aResult[1][0][0]
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

    oParser = cParser()
    sPattern = '<iframe.+?src=["\'](.+?)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
