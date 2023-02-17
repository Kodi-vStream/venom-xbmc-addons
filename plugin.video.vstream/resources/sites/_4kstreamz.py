# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = '_4kstreamz'
SITE_NAME = '4kstreamz'
SITE_DESC = 'Films et Séries'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'list-films.html', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

URL_SEARCH = (URL_MAIN + 'recherche/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1921, 2022)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'filmspar?annee=' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<h4 class="head nop">Genre'
    sEnd = '<div class="menu_first">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'a href="([^"]+)" class="an">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            triAlpha.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        for sTitle, sUrl in triAlpha:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '-').replace('%20', '-') + '.html'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'list-films.html' in sUrl or '/films/page' in sUrl:
        sPattern = '<a class="movie_single.+?href="([^"]+).+?img src="([^"]+).+?class="nop">([^<]+).+?class="qualitos">([^<]+).+?class="synopsis nop">([^<]+)'
    else:
        sPattern = '<a class="movie_single.+?href="([^"]+).+?img src="([^"]+).+?class="nop">([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sThumb = aEntry[1]
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2].strip()
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche

            sQual = ''
            sDesc = ''
            if 'list-films.html' in sUrl or '/films/page' in sUrl:
                sQual = aEntry[3]
                sDesc = aEntry[4]

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/series' not in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    if 'suivanthds' in sHtmlContent:  # genre
        sPattern = '>([^<]+)</a><a class="suivanthds.+?href="([^"]+)'
    elif 'CurrentPage' in sHtmlContent:  # film année serie
        sPattern = "CurrentPage.+?href='([^']+).+?>([^<]+)</a></div"
    else:  # film année à partir de la page 8
        sPattern = "</a><span>.+?<a href='([^']+).+?</span>.+?>([^<]+)</a></div></div>\s*</div>\s*</div>"

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        if 'suivanthds' in sHtmlContent:  # genre
            sNumberMax = aResult[1][0][0]
            sNextPage = aResult[1][0][1]
        # elif 'CurrentPage':  # film année serie
            # sNextPage = aResult[1][0][0]
            # sNumberMax = aResult[1][0][1]
        else:  # film année à partir de la page 8
            sNextPage = aResult[1][0][0]
            sNumberMax = aResult[1][0][1]

        sNumberNext = re.search('page-([0-9]+)|([0-9]+)$', sNextPage).group(0)  # page-XX.html ou  annee-aaaa/XX
        sNumberNext = sNumberNext.replace('page-', '')
        sNextPage = URL_MAIN[:-1] + sNextPage
        sPaging = sNumberNext + '/' + sNumberMax

        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'itemprop="description">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    start = sHtmlContent.find('<div class="contentomovies">')
    sHtmlContent = sHtmlContent[start:]
    sPattern = '<a href="([^"]+).+?class="nop">Saison([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl2 = aEntry[0]
            saison = aEntry[1].replace(' ', '')

            sTitle = ("%s %s %s") % (sMovieTitle, 'saison', saison)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
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

    iSaison = ''
    sPattern = 'saison.(.+?)'
    aResult = oParser.parse(sUrl, sPattern)
    if aResult[0]:
        iSaison = ' Saison ' + aResult[1][0].replace(' ', '')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<div class="contentomovies">'
    sEnd = '<div class="keywords"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+).+?class="titverle">.+?class="nop">.+?pisode([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            nEpisode = aEntry[1].replace(' ', '')
            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sTitle = sMovieTitle + iSaison + ' episode' + nEpisode

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'itemprop="description">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = '<img src=".(vf|vostfr).png|data-url="([^"]+).+?data-code="([^"]+).+?<span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sLang = ''

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if aEntry[0]:
                sLang = aEntry[0].upper()

            if aEntry[1]:
                dataUrl = aEntry[1]
                dataCode = aEntry[2]
                if "/thumbnail/" in dataCode :
                    continue
                sHost = aEntry[3].capitalize()
                if not oHosterGui.checkHoster(sHost):
                    continue

                sUrl2 = URL_MAIN + 'Players.php?PPl=' + dataUrl + '&CData=' + dataCode
                sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sTitle, sLang, sHost)
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sLang', sLang)
                oOutputParameterHandler.addParameter('referer', sUrl)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    sPattern = "<img src=\".(vf|vostfr).png|class=.Playersbelba.+?PPl=(.+?)CData=([^']+).+?<.span>.+?<span>([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if aEntry[0]:
                sLang = aEntry[0].upper()

            if aEntry[1]:
                dataUrl = aEntry[1]
                dataCode = aEntry[2]
                sHost = aEntry[3].capitalize()
                if not oHosterGui.checkHoster(sHost):
                    continue

                sUrl2 = URL_MAIN + 'Players.php?PPl=' + dataUrl + 'CData=' + dataCode

                sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sTitle, sLang, sHost)

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sLang', sLang)
                oOutputParameterHandler.addParameter('referer', sUrl)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.request()
    urlReal = oRequest.getRealUrl()
    if URL_MAIN in urlReal:
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', referer)
        oRequest.request()
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'class="DownloadSection.+?href="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0]
            oHoster = oHosterGui.checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sHosterUrl = urlReal
        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
