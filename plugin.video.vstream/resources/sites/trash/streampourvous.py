# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streampourvous'
SITE_NAME = 'StreampourVous'
SITE_DESC = 'films,'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film-streaming/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film-streaming/', 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'film-streaming/', 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie-streaming/', 'showMovies')
# SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_MANGAS = (URL_MAIN + 'genre/animation/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')
SERIE_ANNEES = (URL_MAIN + 'serie-streaming/', 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?post_types=tvshows&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MANGAS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MANGAS[1], 'Séries (Animations)', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche film', 'search.png', oOutputParameterHandler)

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
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MANGAS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MANGAS[1], 'Séries (Animations)', 'animes.png', oOutputParameterHandler)

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

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<ul class="genres scrolling">'
    sEnd = '><nav class="releases"><h2>Année de production</h2>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+).+?<i>(\d*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            sNumber = aEntry[2]  # + ' Films'
            if sNumber < '2':
                sNumber = sNumber + ' Film'
            else:
                sNumber = sNumber + ' Films'
            sDisplayTitle = ('%s (%s)') % (sTitle, sNumber)
            TriAlpha.append((sDisplayTitle, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        oOutputParameterHandler = cOutputParameterHandler()
        for sDisplayTitle, sUrl in TriAlpha:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<h2>Année de production</h2><ul class="releases scrolling">'
    sEnd = 'class="primary"><div class="columenu">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showYearsSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1997, 2021)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'sortie/' + Year + '/?post_types=tvshows')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="image">.+?<a href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?<p>(.+?)</p>'

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sStart = 'class="animation-2 items">'
        sEnd = '<div class=\'resppages\'>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = 'class="item.+?"><div class="poster.+?src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)href="([^"]+).+?<span>([0-9]{4}).+?texto">(.*?)</div'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        utils = cUtil()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sQual = ''
            sYear = ''
            sDesc = ''
            if sSearch:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]
            else:
                sThumb = aEntry[0]
                sTitle = re.sub('\([0-9]{4}\)', '', aEntry[1])
                if aEntry[2]:
                    sQual = aEntry[2]  # parfois sLang
                sUrl = aEntry[3]
                sYear = aEntry[4]
                if aEntry[5]:
                    sDesc = aEntry[5].replace('Voir', '').replace('Film complet streaming VF HD', '')\
                                     .replace('streaming VF HD', '')

            try:
                sDesc = unicode(sDesc, 'utf-8')  # converti en unicode
                sDesc = utils.unescape(sDesc).encode('utf-8')  # retire les balises HTML
            except:
                pass

            sDisplayTitle = ('%s %s (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSxE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sPattern = 'class="pagination">.+?de (\d*).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSxE():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "<span class='title'>(.+?)<i>|class='numerando'>(.+?)</div><div class='episodiotitle'><a href='([^']+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0].replace('Regarder', '') + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub('(\d+) - (\d+)', 'saison \g<1> Episode \g<2>', aEntry[1])
                sTitle = sMovieTitle + ' ' + SxE

                sDisplayTitle = sMovieTitle + ' ' + re.sub('saison \d+ ', '', SxE)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sPattern = "data-type='([^']+)' data-post='([^']+)' data-nume='([^']+).+?title'>([^<]+).+?server'>(.+?)<.+?flags/(\w+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        # trie par numéro de serveur
        sortedList = sorted(aResult[1], key=lambda item: item[2])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sortedList:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dtype = aEntry[0]
            dpost = aEntry[1]
            dnum = aEntry[2]
            pdata = dpost + '.' + dtype + '.' + dnum
            sTitle = aEntry[3].replace('Serveur', '').replace('Télécharger', '').replace('(', '')\
                              .replace(')', '').replace('[', '').replace(']', '')
            sServer = aEntry[4]
            sLang = aEntry[5].replace('fr', 'VF').replace('en', 'VOSTFR')

            if 'freebiesforyou.net' in sServer or 'youtube.com' in sServer:
                continue
            sTitle = ('%s [%s] (%s)') % (sMovieTitle, sTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('pdata', pdata)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    pdata = oInputParameterHandler.getValue('pdata')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParameters("action", "doo_player_ajax")
    oRequest.addParameters("post", pdata.split('.')[0])
    oRequest.addParameters("type", pdata.split('.')[1])
    oRequest.addParameters("nume", pdata.split('.')[2])
    sHtmlContent = oRequest.request(jsonDecode=True)

    if 'dood' in sHtmlContent or 'evoload' in sHtmlContent:
        sPattern = '(http.+?)$'
    else:
        sPattern = '(http.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if 'zustreamv2/viplayer' in sHosterUrl:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
