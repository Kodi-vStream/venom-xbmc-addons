# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False  # NPAI 04/02/2022

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films, Séries & Mangas en Streaming'

URL_MAIN = "https://www.film-streamingk.biz/"

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_EXCLUS = (URL_MAIN + 'tendance/', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_EPISODES = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Films (Populaire)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # Inutilisable
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_EPISODES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_EPISODES[1], 'Séries (Episodes)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NETFLIX[1], 'Séries (Netflix)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AMAZON[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_AMAZON[1], 'Séries (Amazon Prime)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CANAL[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CANAL[1], 'Séries (Canal+)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DISNEY[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_DISNEY[1], 'Séries (Disney+)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_APPLE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_APPLE[1], 'Séries (Apple TV+)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_YOUTUBE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_YOUTUBE[1], 'Séries (Youtube Originals)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['Crime', 'crime'], ['Drame', 'drame'], ['Familial', 'familial'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Horreur', 'horreur'], ['Histoire', 'histoire'], ['Romance', 'romance'],
             ['Thriller', 'thriller'], ['Science-Fiction', 'science-fiction'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch
        oUtil = cUtil()
        sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH[0], ''))
        sPattern = 'class="image">.*?<a href="([^"]+)">\s*<img src="([^"]+)" alt="([^"]+)".+?<p>([^<]*)'
    elif 'episodes' in sUrl:
        sPattern = 'class="poster">.*?<img src="([^"]+)" alt="([^"]+)".+?<a href="([^"]+)'
    else:
        sPattern = 'class="poster"> *<img src="([^"]+)".+?<a href="([^"]+)" *title="([^"]+)".+?class="texto">([^<]*)'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # for the first sThumb in the movies "featured movies"
    if 'class="archive_post">' in sHtmlContent:
        sHtmlContent = oParser.abParse(sHtmlContent, 'class="archive_post">', '')
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Si recherche et trop de resultat, on filtre
            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, aEntry[2]):
                    continue

            if sSearch:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]
            elif 'episodes' in sUrl:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sUrl = aEntry[2]
                sDesc = ''
            else:
                sThumb = aEntry[0]
                sUrl = aEntry[1]
                sTitle = aEntry[2].replace('streaming', ' ')
                sDesc = aEntry[3]

            # si utile il faut retirer oOutputParameterHandler.addParameter(sDesc)
            # if sDesc:  # désactivé le 17/06/2020,
                # try:
                    # sDesc = cUtil().unescape(sDesc.decode('utf8'))
                # except AttributeError:
                    # sDesc = cUtil().unescape(sDesc)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSxE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'episodes' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'Page \d+ de ([^<]+).+?arrow_pag\' *href="([^"]+)"><i id=\'nextpagination'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
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
    sPattern = '<span class="title">(.+?)<|class="numerando">([^"]+)</div><div class="episodiotitle"><a href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub('(\d+) - (\d+)', 'saison \g<1> Episode \g<2>', aEntry[1])
                sTitle = sMovieTitle + ' ' + SxE

                sDisplaytitle = sTitle # "MARQUER LU" à besoin de la saison et de l'épisode # sMovieTitle + ' ' + re.sub('saison \d+ ', '', SxE)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    if 'episodes' in sUrl:
        sPattern = 'dooplay_player_option.+?data-post="(\d+)".+?data-nume="([^"]+).+?title">([^<]+)'
    else:
        sPattern = "dooplay_player_option.+?data-post='(\d+)'.+?data-nume='([^']+).+?title'>([^<]+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if ('trailer' in aEntry[1]):
                continue
            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            if 'episodes' in sUrl:
                dtype = 'tv'
            else:
                dtype = 'movie'
            dpost = aEntry[0]
            dnum = aEntry[1]
            pdata = 'action=doo_player_ajax&post=' + dpost + '&nume=' + dnum + '&type=' + dtype

            # trie des hosters
            sHoster = aEntry[2].capitalize()
            oHoster = cHosterGui().checkHoster(sHoster)
            if not oHoster:
                continue

            sDisplaytitle = '%s [COLOR coral]%s[/COLOR]' % (sMovieTitle, sHoster)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('pdata', pdata)
            oOutputParameterHandler.addParameter('sHost', sHoster)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, sThumb, sDesc, oOutputParameterHandler)

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
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()
    sPattern = "<iframe.+?src='(.+?)'"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        for aEntry in aResult:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
