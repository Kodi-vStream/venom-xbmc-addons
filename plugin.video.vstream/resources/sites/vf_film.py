# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'vf_film'
SITE_NAME = 'VF Film'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = "https://vf-film.org/"

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'les-films-les-mieux-notee/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films-les-plus-vues/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (True, 'showAlpha')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Par ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item cat-item.+?"><a href="([^<]+)">([^<]+)</a>([^<]+)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[1] + aEntry[2]
            sUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    sUrl = URL_MAIN + 'lettre/'

    liste = [['0-9', sUrl + '0-9'], ['A', sUrl + 'a'], ['B', sUrl + 'b'], ['C', sUrl + 'c'], ['D', sUrl + 'd'],
             ['E', sUrl + 'e'], ['F', sUrl + 'f'], ['G', sUrl + 'g'], ['H', sUrl + 'h'], ['I', sUrl + 'i'],
             ['J', sUrl + 'j'], ['K', sUrl + 'k'], ['L', sUrl + 'l'], ['M', sUrl + 'm'], ['N', sUrl + 'n'],
             ['O', sUrl + 'o'], ['P', sUrl + 'p'], ['Q', sUrl + 'q'], ['R', sUrl + 'r'], ['S', sUrl + 's'],
             ['T', sUrl + 't'], ['U', sUrl + 'u'], ['V', sUrl + 'v'], ['W', sUrl + 'w'], ['X', sUrl + 'x'],
             ['Y', sUrl + 'y'], ['Z', sUrl + 'z']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

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

    if'/lettre/' in sUrl:
        sPattern = '</span></td>.+?href="([^"]+).+?src="([^"]+).+?strong>([^<]+).+?<td>([^<]+)'
    else:
        sPattern = 'TPost C.+?href="([^"]+).+?src="([^"]+).+?Title">([^<]+).+?Description"><p>([^<]+)'

    oParser = cParser()
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

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\d+/', '/w342/', 'https:' + aEntry[1])
            sTitle = aEntry[2]
            if'/lettre/' in sUrl:
                sDesc = ''
                sYear = aEntry[3]
            else:
                sDesc = aEntry[3]
                sYear = ''

            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a><a class="next page-numbers" href="([^"]+)">Next'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class="TPlayerTb.+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:

            oRequestHandler = cRequestHandler(aEntry)
            sHtmlContent = oRequestHandler.request()
            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                for aEntry1 in aResult[1]:
                    sHosterUrl = aEntry1
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
