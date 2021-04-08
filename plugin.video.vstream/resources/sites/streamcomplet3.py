# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 42 14012021
return False  # Cloudflare
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress


# le 24122020  memes films que streamiz sans redirections (considéré comme clone et avec code differents)
# le 14012020 url de redirection streamiz (mais pas toujours)
SITE_IDENTIFIER = 'streamcomplet3'
SITE_NAME = 'Streamcomplet3'
SITE_DESC = 'Films en streaming.'

URL_MAIN = 'https://streamcomplet3.org/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + '6/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_BOXOFFICE = (URL_MAIN + 'film/box-office/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film/vostfr/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BOXOFFICE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BOXOFFICE[1], 'Films (Box Office)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    listegenre = ['action', 'animation', 'aventure', 'comedie', 'drame', 'guerre', 'historique', 'horreur', 'musical',
                  'policier', 'romance', 'fiction', 'thriller', 'western', 'documentaire', 'spectacle']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'film/' + igenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:

        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        pData = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + sSearch
        sUrl = URL_MAIN + 'index.php?do=search'
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParametersLine(pData)
        sHtmlContent = oRequestHandler.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="th-item">.+?href="([^"]*).+?src="([^"]*).+?alt="([^"]*)'
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
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '</span>\s*<a href="([^"]+).+?">(\d+)</a>\s*</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'full-text clearfix">\s*<p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'streamcomplet3'
    if (aResult[0] == True):
        sDesc = aResult[1][0].replace('Résumé du Film :', '')
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', sDesc)

    sPattern = '<iframe.+?src="([^"]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry

            oHoster = cHosterGui().checkHoster(sUrl)
            if (oHoster != False):
                hostName = oHoster.getDisplayName()
            else:
                hostName = getHostName(sUrl)

            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, hostName)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def getHostName(url):

    try:
        if 'www' not in url:
            sHost = re.search('http.*?\/\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\/\/(?:www).([^.]*)', url).group(1)
    except:
        sHost = url

    return sHost.capitalize()
