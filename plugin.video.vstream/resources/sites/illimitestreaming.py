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

SITE_IDENTIFIER = 'illimitestreaming'
SITE_NAME = 'Illimitestreaming'
SITE_DESC = 'Regarder Les Films & Séries VF. VOSTFR .VO'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tvshows/', 'showMovies')

SERIE_NETFLIX = (URL_MAIN + 'networks/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'networks/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'networks/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'networks/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'networks/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'networks/youtube-premium/', 'showMovies')
SERIE_ARTE = (URL_MAIN + 'networks/arte/', 'showMovies')
#SERIE_ANNEES = (True, 'showSeriesYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?sType=movie&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?sType=tvshow&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche films', 'search.png', oOutputParameterHandler)

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
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oParser = cParser()

    sUrl = URL_MAIN
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<a>genres</a>'
    sEnd = '</ul><div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'taxonomy.+?href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            triAlpha.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle, sUrl in triAlpha:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showNetwork():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oOutputParameterHandler.addParameter('sTmdbId', 213)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_NETFLIX[1], 'Séries (Netflix)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CANAL[0])
    oOutputParameterHandler.addParameter('sTmdbId', 285)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_CANAL[1], 'Séries (Canal+)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AMAZON[0])
    oOutputParameterHandler.addParameter('sTmdbId', 1024)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_AMAZON[1], 'Séries (Amazon Prime)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DISNEY[0])
    oOutputParameterHandler.addParameter('sTmdbId', 2739)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_DISNEY[1], 'Séries (Disney+)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_APPLE[0])
    oOutputParameterHandler.addParameter('sTmdbId', 2552)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_APPLE[1], 'Séries (Apple TV+)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_YOUTUBE[0])
    oOutputParameterHandler.addParameter('sTmdbId', 1436)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_YOUTUBE[1], 'Séries (YouTube Originals)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ARTE[0])
    oOutputParameterHandler.addParameter('sTmdbId', 1628)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_ARTE[1], 'Séries (Arte)', 'host.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<a>Anneés</a>'
    sEnd = '<a>genres</a>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    aResult[1].insert(2, (URL_MAIN + 'release-year/2020/', '2020'))

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            sType = 'movie'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sType', sType)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showSeriesYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<a>Anneés</a>'
    sEnd = '<a>genres</a>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    aResult[1].insert(2, (URL_MAIN + 'release-year/2020/', '2020'))
    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            sType = 'tvshow'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sType', sType)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()

    sType = ''
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
        sType = re.search('sType=(.+?)&', sUrl).group(1)
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sType = oInputParameterHandler.getValue('sType')

    sPattern = 'data-movie-id="\d+".+?href="([^"]+).+?oldtitle="([^"]+).+?data-original="([^ "]+).+?desc"><p>([^<]+)'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            if sType and 'movie' in sType and '/series' in sUrl:
                continue
            elif sType and 'tvshow' in sType and '/series' not in sUrl:
                continue
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue    # Filtre de recherche

            sThumb = aEntry[2]
            sThumb = re.sub('/w\d+', '/w342', sThumb)

            sDesc = aEntry[3]
            try:
                sDesc = unicode(sDesc, 'utf-8')  # converti en unicode
                sDesc = oUtil.unescape(sDesc).encode('utf-8')    # retire les balises HTML
            except:
                pass

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies',  'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li class=\'active\'>.+?href=\'([^\']+).+?/(\d+)/\'>Dernière'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    # for the tvshows and the last page of movies
    sPattern = "class=''>\d+</a></li><li><a rel='nofollow' class='page larger' href='([^']+).+?>(\d+)</a></li></ul"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    oParser = cParser()
    oRequestHandler = cRequestHandler(siteUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<div class="tvseason">'
    sEnd = '<!-- Micro data -->'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<div class="tvseason">.+?<strong>(.+?)<'

    aResult = oParser.parse(sHtmlContent, sPattern)

    sSaison = ''
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for sSaison in aResult[1]:
            sTitle = sMovieTitle + ' ' + sSaison
            sUrl = siteUrl + '&season=' + sSaison
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl, sSearchSeason = oInputParameterHandler.getValue('siteUrl').split('&season=')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<div class="tvseason">'
    sEnd = '<!-- Micro data -->'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<div class="tvseason">.+?<strong>(.+?)<|href="([^"]+)">([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    sSaison = ''
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sSaison = aEntry[0]
                continue

            if sSaison != sSearchSeason:
                continue

            sUrl = aEntry[1]
            SxE = aEntry[2]
            sTitle = sMovieTitle #+ ' ' + sSaison
            sTitle += ' ' + SxE

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sPattern = '<div class="movieplay">([^<]+)|lnk lnk-dl"><h6>([^<]*)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:

        tab = aResult[1]
        n = len(tab)//3

        for i in range(n):

            sHosterUrl = tab[i][0]
            sLang = tab[2*i+n][1]
            sQual = tab[2*i+(n+1)][1]

            sTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

            # Petit hack pour conserver le nom de domaine du site
            # necessaire pour userload.
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
        
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
