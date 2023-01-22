# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import progress, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streaminz'
SITE_NAME = 'Streaminz'
SITE_DESC = ' films, de séries et de mangas en streaming VF et VOSTFR complets'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
# MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_NETFLIX = (URL_MAIN + 'reseau/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'reseau/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'reseau/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'reseau/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'reseau/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'reseau/youtube-premium/', 'showMovies')
SERIE_ARTE = (URL_MAIN + 'reseau/arte/', 'showMovies')
# SERIE_ANNEES = (True, 'showSeriesYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')# l'url ne permet pas de filtrer directement les films des séries mais est utilisée pour filtrer dans showmovies
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

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

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

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '</i>Genres</a>'
    sEnd = '</i>Demandes</a>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if aResult[0]:
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
    oOutputParameterHandler.addParameter('sTmdbId', 1436)    # Utilisé par TMDB
    oGui.addNetwork(SITE_IDENTIFIER, SERIE_ARTE[1], 'Séries (Arte)', 'host.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<span>Années</span>'
    sEnd = '<span>Connexion</span>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            sTypeYear = 'movies'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sTypeYear', sTypeYear)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showSeriesYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '<span>Années</span>'
    sEnd = '<span>Connexion</span>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1].capitalize()
            sTypeYear = 'tvshows'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sTypeYear', sTypeYear)
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    if sSearch:
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        sUrl = sSearch.replace(' ', '+')
        sPattern = 'class="image">.+?<a href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?span class="([^"]+).+?<p>(.*?)<\/p'
        sType = oParser.parseSingleResult(sUrl, '\?post_types=(.+?)&')  # pour filtrage entre film et série
    else:
        sTypeYear = oInputParameterHandler.getValue('sTypeYear')
        if sTypeYear:
            sPattern = '<article id="post-\d+".+?class="item ([^"]+).+?img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)<a href="([^"]+).+?class="texto">(.*?)</div>'
        else:
            sPattern = '<article id="post-\d+".+?img src="([^"]+).+?alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)<a href="([^"]+).+?class="texto">(.*?)</div'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
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
                sTitle = aEntry[2].replace('Streaming VF', '').replace('en', '').replace('Regarder', '')
                sType1 = aEntry[3]
                sDesc = aEntry[4]
                if sType1 != sType[1]:  # pour différencier la recherche entre films et séries
                    continue
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche
            elif sTypeYear:
                sType1 = aEntry[0]
                if sType1 != sTypeYear:  # pour différencier la recherche entre films et séries
                    continue
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                if aEntry[3]:
                    sQual = aEntry[3]
                if aEntry[4]:
                    sYear = aEntry[4]
                sUrl = aEntry[5]
                if aEntry[6]:
                    sDesc = aEntry[6]
            else:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                if aEntry[2]:
                    sQual = aEntry[2]
                if aEntry[3]:
                    sYear = aEntry[3]
                sUrl = aEntry[4]
                if aEntry[5]:
                    sDesc = aEntry[5]

            try:
                sDesc = unicode(sDesc, 'utf-8')  # converti en unicode
                sDesc = oUtil.unescape(sDesc).encode('utf-8')  # retire les balises HTML
            except:
                pass

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSxE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sPattern = 'span>Page .+?de (\d+).+?href="([^"]+)"><i id='
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, False


def showSxE():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = ">([^<]+)</span><span class='title|numerando'>(.+?)</div><div class='episodiotitle'><a href='([^']+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]Saison ' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub('(\d+) - (\d+)', ' Saison \g<1> Episode \g<2>', aEntry[1])
                sTitle = sMovieTitle + SxE

                sDisplayTitle = sMovieTitle + ' ' + re.sub('saison \d+ ', '', SxE)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    if '/films/' in sUrl:
        sPattern = "dooplay_player_option.+?data-post='(\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    else:
        sPattern = "dooplay_player_option.+?data-post='(\d+)'.+?data-nume='(.+?)'>.+?flags/(.+?).png"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        # trie par numéro de serveur
        sortedList = sorted(aResult[1], key=lambda item: item[2])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sortedList:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dtype = 'movie'  # fonctionne pour Film ou Série (pour info: série -> dtype = 'tv')
            dpost = aEntry[0]
            dnum = aEntry[1]

            pdata = 'action=doo_player_ajax&post=' + dpost + '&nume=' + dnum + '&type=' + dtype
            sLang = aEntry[2].replace('Serveur', '').replace('Télécharger', '').replace('(', '').replace(')', '')
            if '|' in sLang:
                sLang = sLang.split('|')[1].strip().replace('FRENCH', 'FR')

            if 'VIP - ' in aEntry[2]:  # Les liens VIP ne fonctionnent pas
                continue

            sTitle = ('%s (%s)') % (sMovieTitle, sLang.upper())
            sTitle = sTitle + '[COLOR coral] Serveur#' + dnum + '[/COLOR]'

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
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=(?:\'|")(.+?)(?:\'|")'
    aResult1 = re.findall(sPattern, sHtmlContent)

    sPattern = 'embed_url":"([^"]+)"'
    aResult2 = re.findall(sPattern, sHtmlContent)

    aResult = aResult1 + aResult2

    if aResult:
        for aEntry in aResult:

            sHosterUrl = aEntry.replace("\\", '')
            if 'youtube' in sHosterUrl:
                continue
            if 'dood' in sHosterUrl:
                sHosterUrl = sHosterUrl

            if 'club' in sHosterUrl:
                sHosterUrl = sHosterUrl
                oRequest = cRequestHandler(sHosterUrl)
                oParser = cParser()
                sHtmlContent2 = oRequest.request()

                sPattern = "if.+?self.+?== top.+?replace\('([^']+)"
                aResult = oParser.parse(sHtmlContent2, sPattern)
                for aEntry2 in aResult[1]:
                    sHosterUrl = 'https://waaw.to' + aEntry2

            # voir si filtrage ou non, car parfois le lien mp4 créé un blocage
            if 'streaminz.ml' in sHosterUrl:
                sid = sHosterUrl.split('/')[-1]
                sHosterUrl = sHosterUrl
                postdata = 'r=&d=streaminz.ml'
                urlapi = 'https://streaminz.ml/api/source/' + sid
                oRequest = cRequestHandler(urlapi)
                oRequest.setRequestType(1)
                oRequest.addHeaderEntry('Referer', sHosterUrl)
                oRequest.addParametersLine(postdata)
                sHtmlContent2 = oRequest.request()
                oParser = cParser()
                sPattern = '"data".+?file.+?"([^"]*).+?type.+?"([^"]*)'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if aResult[0]:
                    sHosterUrl = aResult[1][0][0] + '.' + aResult[1][0][1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
