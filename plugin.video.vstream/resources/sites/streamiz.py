# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 37 https://streamiz-filmze.org/ 06122020

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'streamiz'
SITE_NAME = 'Streamiz'
SITE_DESC = 'Films en streaming.'

URL_MAIN = 'https://streamiz-filmze.org/'


MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'streaming/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'streaming/box-office/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'streaming/vostfr/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
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
                  'policier', 'romance', 'science-fiction', 'thriller', 'western', 'documentaire', 'spectacle']

    # href="/streaming/action/
    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'streaming/' + igenre + '/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:

        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        pdata = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + sSearch
        sUrl = 'https://streamiz-filmze.org/streaming/index.php?do=search'

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParametersLine(pdata)
        sHtmlContent = oRequestHandler.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class="th-item">.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]*).+?<span>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sDesc = aEntry[3]  # <span>Thriller / Horreur / Sous-titre</span>

            if 'Sous-titre' in sDesc:
                sTitle = sTitle + ' (VOST)'

            sDesc = sDesc.replace('/ Sous-titre', '').replace('/ Box Office', '')
            sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Genre :  ', sDesc.replace('/', ','))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalid, sUrlNextPage, pagination = __checkForNextPage(sHtmlContent, sUrl)
        if (bvalid == True):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(shtml, surl):
    # pas de lien next page
    smax = ''
    imax = 0
    # scurrent = ''
    # icurrent = 0
    inext = 0
    snext = ''
    surlnext = ''

    sPattern = 'page/(\d+)/'

    # max page
    oParser = cParser()
    aResult = oParser.parse(shtml, sPattern)
    if (aResult[0] == True):
        for aresult in aResult[1]:
            scurrentmax = aresult
            icurentmax = int(scurrentmax)
            if icurentmax > imax:
                imax = icurentmax
                smax = scurrentmax
    # next page
    oParser = cParser()
    aResult = oParser.parse(surl, sPattern)
    if (aResult[0] == False):
        # la premiere page ne contient pas d'index
        if smax > 1:  # mais il faut au moins deux pages
            inext = 2
            snext = '2'
            surlnext = surl + 'page/2/'
        else:
            return False, False, False

    if (aResult[0] == True):
        scurrent = aResult[1][0]
        icurrent = int(scurrent)
        inext = icurrent + 1
        snext = str(inext)
        pcurrent = 'page/' + scurrent
        pnext = 'page/' + snext
        surlnext = surl.replace(pcurrent, pnext)

    if imax != 0 and imax >= inext:
        return True, surlnext, snext + '/' + smax

    elif inext == 0:
        return False, False, False

    return False, False, False


def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'Synopsis.+?clearfix">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'streamiz-filmze.org'
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = '<iframe.+?src="([^"]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry

            oHoster = cHosterGui().checkHoster(sUrl)
            if (oHoster != False):
                Hostname = oHoster.getDisplayName()
            else:
                Hostname = GetHostname(sUrl)

            sDisplayName = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, Hostname)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

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


def GetHostname(url):

    try:
        if 'www' not in url:
            sHost = re.search('http.*?\/\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\/\/(?:www).([^.]*)', url).group(1)
    except:
        sHost = url

    return sHost.capitalize()
