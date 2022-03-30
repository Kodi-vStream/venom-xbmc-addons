# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'stream_complet'
SITE_NAME = 'Stream Complet'
SITE_DESC = 'Voir les meilleurs films en version française'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?keymovies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'series-streaming/?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SERIES_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIES_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


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

    # ajout: documentaire, fantastique, western
    listegenre = ['action', 'animation', 'aventure', 'comedie', 'documentaire', 'drame', 'fantastique', 'guerre',
                  'historique', 'horreur', 'musical', 'policier', 'romance', 'science-fiction', 'thriller', 'western']

    url1g = URL_MAIN + 'film/'

    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in listegenre:
        sUrl = url1g + igenre + '/'
        sTitle = igenre.capitalize()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="moviefilm">.+?href="([^"]+).+? src="([^"]+).+?alt="([^"]+)'
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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sTitle = sTitle.replace('streaming VF', '')

            if URL_SEARCH_MOVIES[0] in sUrl:
                if '/serie' in sUrl2:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'serie' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPagination = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies',  sPagination, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="nextpostslink.+?href="([^"]+).+?class="last.+?href=.*?page.([0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][1]
        sNextPage = aResult[1][0][0]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPagination = sNumberNext + '/' + sNumberMax
        return sNextPage, sPagination
    return False, False


def showSaison():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    oParser = cParser()
    sPattern = 'film-poster.*?Synopsis :([^<]+)'
    aResultDesc = oParser.parse(sHtmlContent, sPattern)
    if aResultDesc[0] is True:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResultDesc[1][0])

    sPattern = '(\d+)<\/a><\/h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sSaison = ''

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sNumSaison = aEntry[0]
            sSaison = 'Saison ' + aEntry[0]
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison

            sTitle = sMovieTitle + sSaison
            sDisplayTitle = sTitle + '' + sSaison
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

    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = 'id="saison-'+ sNumSaison
    sEnd = '<div id="alt">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">épisode (\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            Ep = aEntry[1]
            Saison = 'Saison ' + sNumSaison
            sTitle = sMovieTitle + Saison + ' Episode ' + Ep

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    oParser = cParser()
    sPattern = 'film-poster.*?Synopsis :([^<]+)'
    aResultDesc = oParser.parse(sHtmlContent, sPattern)
    if aResultDesc[0] is True:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', aResultDesc[1][0])

    sPattern = 'class="player link" data-player="([^"]+).+?langue-s">([^<]+).+?<span class="p-name">([^"]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sLang = aEntry[1]
            sHostname = aEntry[2].capitalize()
            sDisplayName = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sTitle, sLang, sHostname)
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteReferer', sUrl)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHostname)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

    sPattern = '(?:class="players">|</a>)\s*<a href="([^"]+).+?<li class="player".+?langue-s">([^<]+).+?<span class="p-name">([^"]+)</span>'
    # avec href="([^"]+)"; '"' à garder  pour éviter oublie avec test reg101
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sLang = aEntry[1]
            sHostname = aEntry[2].lower()
            # ou à revoir : on ne prend que 1 Fichier et Uptobox
            if not ('uptobox' in sHostname or 'fichier' in sHostname):
                continue
            sHostname = sHostname.capitalize()

            sDisplayTitle = '%s (%s) [COLOR coral]%s[/COLOR]' % (sTitle, sLang, sHostname)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteReferer', sUrl)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHostname)
            oGui.addLink(SITE_IDENTIFIER, 'showHostersDL', sDisplayTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    siteReferer = oInputParameterHandler.getValue('siteReferer')

    if 'sstatic' in sUrl:
        sUrl1 = sUrl + '/ajax'
        oRequestHandler = cRequestHandler(sUrl1)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'url":"([^"]+)'  # tjrs doodstream
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHosterUrl = aResult[1][0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Referer', siteReferer)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'url=([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHostersDL():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sLang = oInputParameterHandler.getValue('sLang')

    sDisplayName = ('%s (%s)') % (sMovieTitle, sLang)

    if 'shortn.co' in sUrl:
        bvalid, shost = Hoster_shortn(sUrl)
        if bvalid:
            sHosterUrl = shost
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if oHoster != False:
                oHoster.setDisplayName(sDisplayName)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sHosterUrl = sUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster != False:
            oHoster.setDisplayName(sDisplayName)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()


def Hoster_shortn(url):
    shost = ''
    url = url.replace('%22', '')
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    cookies = oRequestHandler.GetCookies()
    sPattern = "type.*?name=.*?value='([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        token = aResult[0]
        data = '_token=' + token
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParametersLine(data)
        sHtmlContent = oRequestHandler.request()

        sPattern = 'href="([^"]+).+?target="_blank'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            shost = aResult[0]
            if '?' in shost and 'uptobox' in shost:
                shost = shost.split('?')[0]
    if shost:
        return True, shost

    return False, False
