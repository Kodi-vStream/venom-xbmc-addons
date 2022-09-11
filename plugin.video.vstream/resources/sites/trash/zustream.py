# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

return False #l'adresse a changé mais plus du tout le meme site, le 06/06/22

import re

from resources.lib.comaddon import progress, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'zustream'
SITE_NAME = 'ZuStream'
SITE_DESC = 'Retrouvez un énorme répertoire de films, de séries et de mangas en streaming VF et VOSTFR complets'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuFilms')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = ('?post_types=tvshows', 'showGenres')
SERIE_MANGAS = (URL_MAIN + 'genre/mangas/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')
SERIE_ANNEES = (True, 'showYearsSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?post_types=movies&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?post_types=tvshows&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuFilms():
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

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MANGAS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MANGAS[1], 'Séries (Mangas)', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/' + sUrl])
    liste.append(['Animation', URL_MAIN + 'genre/animation/' + sUrl])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/' + sUrl])
    liste.append(['Biopic', URL_MAIN + 'genre/biographie/' + sUrl])
    liste.append(['Comédie', URL_MAIN + 'genre/comedie/' + sUrl])
    liste.append(['Comédie musicale', URL_MAIN + 'genre/musique/' + sUrl])
    liste.append(['Comédie romantique', URL_MAIN + 'genre/romance/' + sUrl])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/' + sUrl])
    liste.append(['Drame', URL_MAIN + 'genre/drame/' + sUrl])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/' + sUrl])
    liste.append(['Famille', URL_MAIN + 'genre/familial/' + sUrl])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/' + sUrl])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/' + sUrl])
    liste.append(['Historique', URL_MAIN + 'genre/histoire/' + sUrl])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/' + sUrl])
    liste.append(['Noël', URL_MAIN + 'genre/noel/' + sUrl])
    liste.append(['Science Fiction', URL_MAIN + 'genre/science-fiction/' + sUrl])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/' + sUrl])
    liste.append(['Western', URL_MAIN + 'genre/western/' + sUrl])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
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

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1995, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'sortie/' + Year + '/?post_types=movies')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYearsSeries():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1997, 2022)):
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
    oUtil = cUtil()

    if sSearch:
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
        sPattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)".+?<p>([^<]*)</p>'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = 'article id="post-\d+".+?img src="([^"]+)" alt="([^"]+).+?(?:|class="quality">([^<]+).+?)(?:|class="dtyearfr">([^<]+).+?)href="([^"]+).+?class="texto">(.*?)</div>'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
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

            sLang = ''
            sYear = ''
            sDesc = ''
            if sSearch:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]

                # Filtre de recherche
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue
            else:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                if aEntry[2]:
                    sLang = aEntry[2]
                if aEntry[3]:
                    sYear = aEntry[3]
                sUrl = aEntry[4]
                if aEntry[5]:
                    sDesc = aEntry[5]

            try:
                sDesc = unicode(sDesc, 'utf-8')  # converti en unicode
                sDesc = oUtil.unescape(sDesc).encode('utf-8')    # retire les balises HTML
            except:
                pass

            sDisplayTitle = ('%s (%s) (%s)') % (sTitle, sLang, sYear)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
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
    sPattern = '<span>Page.+?de ([^<]+)</span.+?href="([^"]+)(?:"><i id=\'nextpaginat|" ><span class="icon-chevron-rig)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
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
    sPattern = "<span class='title'>Saisons (.+?) *<i>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sNumSaison = aEntry[0].strip()
            sTitle = sMovieTitle + ' saison ' + sNumSaison
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
            oOutputParameterHandler.addParameter('siteUrl', sUrlSaison)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showSxE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSxE():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "class='numerando'>(\d+) - (\d+)</div><div class='episodiotitle'><a href='([^']+)'"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            s = aEntry[0]
            if s != sNumSaison:
                continue
            e = aEntry[1]
            sUrl = aEntry[2]
#            SxE = re.sub('(\d+) - (\d+)', 'saison \g<1> Episode \g<2>', aEntry[0])
            sTitle = sMovieTitle + ' Saison %s Episode %s' % (s, e)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
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

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    sPattern = "dooplay_player_option.+?data-post='(\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        # trie par numéro de serveur
        sortedList = sorted(aResult[1], key=lambda item: item[2])
        for aEntry in sortedList:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dtype = 'movie'  # fonctionne pour Film ou Série (pour info : série -> dtype = 'tv')
            dpost = aEntry[0]
            dnum = aEntry[1]
            pdata = 'action=doo_player_ajax&post=' + dpost + '&nume=' + dnum + '&type=' + dtype
            sLang = aEntry[2].replace('Serveur', '').replace('Télécharger', '').replace('(', '').replace(')', '')

            if 'VIP - ' in sLang:  # Les liens VIP ne fonctionnent pas
                continue

            sTitle = ('%s [%s]') % (sMovieTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sLang', sLang)
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
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    # 1
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=[\'|"]([^\'"|]+)'
    aResult1 = re.findall(sPattern, sHtmlContent)

    # 2
    sPattern = '<a href="([^"]+)">'
    aResult2 = re.findall(sPattern, sHtmlContent)

    # fusion
    aResult = aResult1 + aResult2

    if aResult:
        for aEntry in aResult:

            sHosterUrl = aEntry
            if 'zustreamv2/viplayer' in sHosterUrl:
                return

            if 're.zu-lien.com' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'https://re.zu-lien.com')
                oRequestHandler.request()
                sUrl1 = oRequestHandler.getRealUrl()
                if not sUrl1 or sUrl1 == sHosterUrl:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.disableRedirect()
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', 'https://re.zu-lien.com')
                    oRequestHandler.request()

                    getreal = sHosterUrl

                    if oRequestHandler.statusCode() == 302:
                        redirection_target = reponse.getResponseHeader()['Location']
                else:
                    sHosterUrl = sUrl1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
