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

SITE_IDENTIFIER = 'streamizseries'
SITE_NAME = 'Streamiz Séries'
SITE_DESC = 'Films & Séries en streaming.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = ('search', 'showMovies')
URL_SEARCH_MOVIES = ('searchMovie=', 'showMovies')
URL_SEARCH_SERIES = ('searchTV=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = ('films-streaming', 'showMovies')
MOVIE_VIEWS = ('film-boxoffice', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = ('series-en-streaming', 'showMovies')
SERIE_GENRES = (True, 'showGenresTVShow')
SERIE_ANNEES = (True, 'showTVShowYears')



def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Par années', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Par années', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        showMovies(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    listegenre = ['action', 'action-adventure', 'animation', 'aventure', 'comedie', 'crime', 'documentaire', 'drame',
                  'familial', 'fantastique', 'guerre', 'histoire', 'horreur', 'musique', 'mystere',
                  'science-fiction', 'science-fiction-fantastique', 'romance',
                  'telefilm', 'thriller', 'war-politics', 'western']

    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in listegenre:
        sTitle = igenre.capitalize()
        oOutputParameterHandler.addParameter('siteUrl', 'categories/' + igenre)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenresTVShow():
    oGui = cGui()

    listegenre = ['action', 'action-adventure', 'animation', 'aventure', 'comedie', 'crime', 'documentaire', 'drame',
                  'familial', 'fantastique', 'guerre', 'histoire', 'horreur', 'kids', 'musique', 'mystere',
                  'science-fiction', 'science-fiction-fantastique', 'reality', 'romance', 'soap',
                  'talk', 'thriller', 'war-politics', 'western']

    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in listegenre:
        sTitle = igenre.capitalize()
        oOutputParameterHandler.addParameter('siteUrl', 'categories/' + igenre + '/series')
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTVShowYears():
    showMovieYears(sTypeSerie='/series')


def showMovieYears(sTypeSerie=''):
    import datetime
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(2001, int(datetime.datetime.now().year) + 1)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', 'annee/' + Year + sTypeSerie)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        bvalid, stoken, scookie = getTokens()
        if not bvalid:
            oGui.setEndOfDirectory()
            return

        oUtil = cUtil()
        catSearch, sSearchText = sSearch.split('=')
        sSearchText = oUtil.CleanName(sSearchText)
        pdata = '_token=' + stoken + '&search=' + sSearchText
        sUrl = URL_MAIN + URL_SEARCH[0]
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addHeaderEntry('Cookie', scookie)
        oRequestHandler.addParametersLine(pdata)
        sHtmlContent = oRequestHandler.request()

        catSearch = 'Films' if catSearch in URL_SEARCH_MOVIES[0] else 'Séries'
        sHtmlContent = oParser.abParse(sHtmlContent, 'dans : <span>' + catSearch, '<h1 class="section-title"')
            
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        if not 'http' in sUrl:
            sUrl = URL_MAIN + sUrl
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # img url title year description
    sPattern = 'lazyload" src=([^ ]+).+?href="([^"]+).+?.+?serif;">([^<]+).+?>\s*(\d+)\s*<.+?<p>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = re.sub('/w\d+/', '/w342/', aEntry[0])
            sUrl2 = aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDesc = aEntry[4]

            # Titre recherché
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if sSearch:
                if catSearch == 'Films':
                    oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+?)</a><a href="([^"]+?)" class="next page-numbers'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaison():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = '</figure><div><p>Saison<span>(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sorted(aResult[1]):

            sNumSaison = aEntry
            sSaison = 'Saison ' + sNumSaison
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
            sDisplayTitle = sMovieTitle + ' ' + sSaison
            sTitle = sMovieTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrlSaison)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addSeason(SITE_IDENTIFIER, 'showSXE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSXE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    # sStart = '</figure><div><p>Saison<span>' + sNumSaison
    # sEnd = 'id="season-'
    # sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = '<span>S' + sNumSaison + '-([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            Ep = aEntry[0]
            sUrl2 = aEntry[1]
            Saison = 'Saison' + ' ' + sNumSaison
            sTitle = sMovieTitle + ' ' + Saison + ' ' + Ep

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = 'content">([^<]+)<br>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # # dans le cas d'une erreur si serie (pas de controle année et genre)
    # if False and 'class="num-epi">' in sHtmlContent and 'episode' not in sUrl:
    #
    #     oOutputParameterHandler = cOutputParameterHandler()
    #     oOutputParameterHandler.addParameter('siteUrl', sUrl)
    #     oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    #     oOutputParameterHandler.addParameter('sThumb', sThumb)
    #     oOutputParameterHandler.addParameter('sDesc', sDesc)
    #     oGui.addTV(SITE_IDENTIFIER, 'showSXE', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)
    #
    #     oGui.setEndOfDirectory()
    #     return

    sPattern = 'data-link="([^"]+).+?option"> ([^<]+).+?flag/([^\.]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oHosterGui = cHosterGui()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sKey = aEntry[0]
            sHost = aEntry[1].strip()
            hoster = oHosterGui.checkHoster(sHost)
            if not hoster:
                continue
            sHost = hoster.getPluginIdentifier()

            sLang = aEntry[2].upper()
            sUrl2 = URL_MAIN + 'll/captcha?hash=' + sKey
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost.capitalize())

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "href = '([^\']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if not aResult:
        sPattern = 'iframe" src="([^"]+)'
        aResult = re.findall(sPattern, sHtmlContent)

    if not aResult:
        aResult = [oRequestHandler.getRealUrl()]

    if aResult:
        sHosterUrl = aResult[0]

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def getTokens():
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = 'name=_token value="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?, (\w+_session)=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        XSRF_TOKEN = aResult[1][0][0]
        site_name = aResult[1][0][1]
        site_session = aResult[1][0][2]

    cook = 'XSRF-TOKEN=%s; %s=%s;' % (XSRF_TOKEN, site_name, site_session)
    
    return True, token, cook


