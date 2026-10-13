# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'seefrench'
SITE_NAME = 'SeeFrench'
SITE_DESC = 'Bienvenue sur SeeFrench'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

API_MOVIE_URL = 'api/movie/m/%d/player'
API_TV_URL = 'api/series/s/%d'
API_SAISON_URL = 'api/series/s/%d/season/%d'
API_EPISODE_URL = 'api/series/s/%d/season/%d/episode/%d/player'



MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = ('api/movie/upcoming', 'showMovies')
MOVIE_VIEWS = ('api/movie/discover', 'showMovies')
URL_SEARCH_MOVIES = ('api/movie/search?page=1&q=', 'showMovies')
#api/movie/toprated

# pas de hoster connus
# SERIE_SERIES = (True, 'showMenuTvShows')
# SERIE_NEWS = ('api/series/upcoming', 'showMovies')
# SERIE_VIEWS = ('api/series/toprated', 'showMovies')
# URL_SEARCH_SERIES = ('api/series/search?page=1&q=', 'showMovies')



def load():
    oGui = cGui()
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png')
# pas de hosters traités    oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', 'Séries', 'series.png')
    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# def showMenuTV():
#     oGui = cGui()
#
#     oOutputParameterHandler = cOutputParameterHandler()
#     oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
#     oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-series.png', oOutputParameterHandler)
#
#     oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
#     oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)
#
#     oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
#     oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)
#
#     oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        showMovies(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.split('=')[-1].replace('%20', ' ')
        siteUrl = sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = sUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
        if not sPage:
            sPage = '1'
        sUrl += '?page=' + sPage

    bSerie = '/series/' in siteUrl
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    responses = oRequestHandler.request(jsonDecode=True)
    oOutputParameterHandler = cOutputParameterHandler()
    if not 'detail' in responses:
        for response in responses:
            sTitle = response['title']
            if sSearch:            # Filtre de recherche
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue
    
            sTmdbID = response['id']
            sThumb = response['poster_url']
            sDesc = response['overview']
            sUrl = (API_TV_URL if bSerie else API_MOVIE_URL) % sTmdbID
    
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbID)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
    
            if bSerie:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        iPage = int(sPage) + 1
        sPage = str(iPage)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', sPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSaison():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    response = oRequestHandler.request(jsonDecode = True)

    if 'seasons' in response:
        oOutputParameterHandler = cOutputParameterHandler()
        sTmdbID = response['id']
        saisons = response['seasons']
        for saison in saisons:
            sSaisonTitle = saison['title']
            sSaisonThumb = saison['poster_url']
            sDesc = saison['overview']
            numSaison = saison['number']
            if not sSaisonThumb:
                sSaisonThumb = sThumb

            if numSaison == 0:
                sDisplayTitle = 'S0 %s - %s' % (sMovieTitle, sSaisonTitle)
            else:
                sDisplayTitle = 'S%d %s' % (numSaison, sMovieTitle)
                
            sUrl = API_SAISON_URL % (sTmdbID, numSaison)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbID)
            oOutputParameterHandler.addParameter('sThumb', sSaisonThumb)
    
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sSaisonThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSaisonUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sSaisonUrl)
    response = oRequestHandler.request(jsonDecode = True)

    if 'episodes' in response:
        oOutputParameterHandler = cOutputParameterHandler()
        episodes = response['episodes']
        for episode in episodes:
            sTmdbID = episode['series_id']
            sEpisodeTitle = episode['title']
            sDesc = episode['overview']
            numSaison = episode['season']
            numEp = episode['number']
            sEpisodeThumb = episode['still_url']
            if not sEpisodeThumb:
                sEpisodeThumb = sThumb

            sDisplayTitle = 'S%dE%d %s' % (numSaison, numEp, sEpisodeTitle)
                
            sUrl = API_EPISODE_URL % (sTmdbID, numSaison, numEp)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbID)
            oOutputParameterHandler.addParameter('sThumb', sEpisodeThumb)
    
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    responses = oRequestHandler.request(jsonDecode=True)

    if responses['available']:
        links = responses['links']
        for link in links:
    
            sHosterUrl = link['link']
            sLang = link['language']
 
            # redirection
            if 'sources-green' in sHosterUrl:
                sHosterUrl = sHosterUrl.replace('https://sources-green.vercel.app/hq?hls=https%3A', 'https:')
                sHosterUrl = sHosterUrl.split('&')[0]
                
            sDisplayTitle = sMovieTitle
            if 'VF' not in sLang:
                sDisplayTitle = '%s [%s]' % (sMovieTitle, sLang)
                
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
