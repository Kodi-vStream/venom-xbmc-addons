# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'o1streaming'
SITE_NAME = '01 Streaming'
SITE_DESC = 'Films & Séries'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = ('?type=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = ('?type=series', 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films & Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_MAIN + 'accueil/')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="btn sm" href="([^"]+)">([^<]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl = aEntry[0]
            Year = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(URL_MAIN + 'accueil/')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item cat-item-.+?href="([^"]+)">([^<]+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0] + siteUrl
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sUrl = sSearch
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'entry-header"> *<h2 class="entry-title">([^<]+).+?src="([^"]+).+?class="year">([^<]+).+?href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb
            sYear = aEntry[2]
            sUrl2 = aEntry[3]
            sTitle = aEntry[0]
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche
            sDisplayTitle = sTitle
            if '/release/' in sUrl or sSearch:
                if '/serie' in sUrl2:
                    sDisplayTitle += ' {Série}'
                else:
                    sDisplayTitle += ' {Film}'

            if sYear:
                sDisplayTitle += ' (%s)' % sYear

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/serie' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a><a href="([^"]+)"\s*>SUIVANT</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        if sNextPage.startswith('/'):
            return URL_MAIN[:-1] + sNextPage, sPaging
        else:
            return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = 'description"><p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = 'choose-season"><a href="([^"]+).+?inline">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sDisplayTitle = sMovieTitle + ' Saison ' + aEntry[1]

            # oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'wp-admin/admin-ajax.php')
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'h2 class="entry-title">([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[0].replace(' Streaming', '')
            sUrl = aEntry[1]
            # if sUrl.startswith('/'):
                # sUrl = URL_MAIN + sUrl

            # sTitle = re.sub('- Saison \d+', '', sTitle)  # double affichage de la saison

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    numUrl = 0

    # récupération du Synopsis
    if sDesc is False:
        try:
            sPattern = 'description">\s*<p>(.+?)</p>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            pass

    sPatternUrl = '<iframe (?:data-)*src="([^"]+)'
    aResultUrl = oParser.parse(sHtmlContent, sPatternUrl)
    if aResultUrl[0]:
        sPatternHost = 'class="btn(| on)" href="([^"]+).+?class="server">([^<]+)<'
        aResultHost = oParser.parse(sHtmlContent, sPatternHost)
        if aResultHost[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResultHost[1]:

                sUrl2 = aResultUrl[1][numUrl]
                numUrl += 1
                sHost = aEntry[2]
                sLang = 'VF'
                if '-VOSTFR' in sHost:
                    sLang = 'VOSTFR'
                sHost = sHost.replace('VF', '').replace('VOSTFR', '').replace(' -', '').replace(' ', '').capitalize().strip()

                if sHost:
                    oHoster = cHosterGui().checkHoster(sHost)
                else:
                    oHoster = cHosterGui().checkHoster(sUrl2)
                if oHoster:
                    sHost = oHoster.getDisplayName()
                    sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
                    oOutputParameterHandler.addParameter('sHost', sHost)
                    oOutputParameterHandler.addParameter('sLang', sLang)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if sUrl:
        sHosterUrl = sUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
