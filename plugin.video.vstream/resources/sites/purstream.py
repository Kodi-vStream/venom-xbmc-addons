# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import siteManager, addon

SITE_IDENTIFIER = 'purstream'
SITE_NAME = 'purstream'
SITE_DESC = 'Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_api')


# pour l'addon
MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_LAST = ('catalog/movies?types=movie&page=1', 'showMovies')
MOVIE_VIEWS = ('catalog/movies?types=movie&sortBy=best-rated&page=1', 'showMovies')
MOVIE_NEWS = ('catalog/movies?types=movie&sortBy=recently-added&page=1', 'showMovies')
MOVIE_GENRES = (MOVIE_LAST[0], 'showGenres')

SERIE_SERIES = (True, 'showMenuTV')
SERIE_LAST = ('catalog/movies?types=tv&page=1', 'showMovies')
SERIE_VIEWS = ('catalog/movies?types=tv&sortBy=best-rated&page=1', 'showMovies')
SERIE_NEWS = ('catalog/movies?types=tv&sortBy=recently-added&page=1', 'showMovies')
SERIE_GENRES = (SERIE_NEWS[0], 'showSerieGenres')

ANIM_ANIMS = (True, 'showMenuAnime')
ANIM_VIEWS = ('catalog/movies?types=anime&sortBy=best-rated&page=1', 'showMovies')
ANIM_NEWS = ('catalog/movies?types=anime&sortBy=recently-added&page=1', 'showMovies')


DOC_DOCS = (True, 'showMenuDivers')
DOC_NEWS = (URL_MAIN, 'showMovies')
SHOW_SHOWS = (URL_MAIN, 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('search-bar/search/%s?types=movie', 'showMovies')
URL_SEARCH_SERIES = ('search-bar/search/%s?types=tv', 'showMovies')
URL_SEARCH_ANIMS = ('search-bar/search/%s?types=anime', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'anime.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LAST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LAST[1], addons.VSlang(30101), 'boxoffice.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    

def showMenuTV():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LAST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LAST[1], addons.VSlang(30101), 'boxoffice.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnime():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        showMovies(sUrl % sSearchText)
        oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = {
        'Action': 1,
        'Animation': 3,
        'Aventure': 2,
        'Comédie': 4,
        'Crime': 5,
        'Documentaire': 6,
        'Drame': 7,
        'Famille': 8,
        'Fantastique': 9,
        'Guerre': 18,
        'Histoire': 10,
        'Horreur': 11,
        'Musique': 12,
        'Mystère': 13,
        'Romance': 14,
        'Science Fiction': 15,
        'Téléfilm': 22,
        'Thriller': 16,
        'Western': 19
    }

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, iGenre in sorted(liste.items()):
        sGenreUrl = '%s&categoriesIds=%d' % (sUrl, iGenre)
        oOutputParameterHandler.addParameter('siteUrl', sGenreUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = {
        'Action & Aventure': 23,
        'Animation': 3,
        'Comédie': 4,
        'Crime': 5,
        'Documentaire': 6,
        'Drame': 7,
        'Enfants': 27,
        'Famille': 8,
        'Guerre & Politique': 25,
        'Mystère': 13,
        'Réalité': 26,
        'Science Fiction & Fantastique': 24,
        'Soap': 29,
        'Téléfilm': 22,
        'Western': 19
    }

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, iGenre in sorted(liste.items()):
        sGenreUrl = '%s&categoriesIds=%d' % (sUrl, iGenre)
        oOutputParameterHandler.addParameter('siteUrl', sGenreUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    searchType = None
    isAnime = False
    if sSearch:
        sUrl = sSearch.lower()
        searchType = sUrl.split('?')[1].split('types=')[1]
        if searchType == 'anime':
            searchType = 'tv'
            isAnime = True

    oRequestHandler = cRequestHandler(URL_API + sUrl)
    data = oRequestHandler.request(True)
    if data['type'] != 'success':
        if not sSearch:
            oGui.setEndOfDirectory()
        return
    
    data = data['data']
    if data['count'] == 0:
        if not sSearch:
            oGui.setEndOfDirectory()
        return

    
    oOutputParameterHandler = cOutputParameterHandler()
    items = data['items']
    if sSearch:
        movies = items['movies']['items']
    else:
        movies = items['data']
    for movie in movies:
        sType = movie['type']
        if searchType and searchType != sType:
            continue
        if isAnime and not movie['isAnime']:
            continue
        movieId = movie['id']
        sTitle = movie['title']
        sYear = movie['release_date'][:4]
        sThumb = movie['large_poster_path']
        oOutputParameterHandler.addParameter('siteUrl', movieId)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        if sType == 'movie':
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)
        else:
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        currentPage = items['current_page']
        lastPage = items['last_page']
        if currentPage < lastPage:
            currentPage += 1
            sNextPage = 'page=%d' % currentPage
            sUrl = re.sub('(page=\d+)', sNextPage, sUrl)
            sTitle = 'Page %d/%d' % (currentPage, lastPage)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    movieId = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sUrl = '%smedia/%s/sheet' % (URL_API, movieId)
    oRequestHandler = cRequestHandler(sUrl)
    data = oRequestHandler.request(True)
    if data['type'] != 'success':
        oGui.setEndOfDirectory()
        return

    tmdbId = data['data']['items'].get('tmdbId', '')
    nbSaisons = data['data']['items']['seasons']
    oOutputParameterHandler = cOutputParameterHandler()
    for numSaison in range(1, nbSaisons+1):
        sDisplayTitle = '%s Saison %d' % (sMovieTitle, numSaison)
        sUrl = '%s/season/%d' % (movieId, numSaison)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', tmdbId)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, 'no-image.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(URL_API + 'media/' + sUrl)
    data = oRequestHandler.request(True)
    if data['type'] != 'success':
        oGui.setEndOfDirectory()
        return

    urlSaison = sUrl.replace('season/', 'episode?season=') + '&episode=%d'
    oOutputParameterHandler = cOutputParameterHandler()
    numSaison = data['data']['items']['season']
    episodes = data['data']['items']['episodes']
    for episode in episodes:
        numEp = episode['episode']
        sThumb = episode['poster']
        sDisplayTitle = 'S%dE%d %s' % (numSaison, numEp, sMovieTitle)#episode['formattedName'] # contient la saison et l'episode
        sDesc = episode['overview']
        sUrl = urlSaison % numEp
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'no-image.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

    
def showHosters():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    movieId = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sUrl = URL_API + 'stream/' + movieId
    oRequestHandler = cRequestHandler(sUrl)
    data = oRequestHandler.request(True)

    if data['type'] != 'success':
        oGui.setEndOfDirectory()
        return

    oHoster = oHosterGui.getHoster('lien_direct')
    for link in data['data']['items']['sources']:
        streamUrl = link['stream_url']
        sourceName = link['source_name'].replace('pulse ', '')
        if sourceName.startswith('|'):
            sourceName = sourceName[2:]
        if not 'Source' in sourceName:
            sDisplayTitle = '%s - [COLOR yellow][%s][/COLOR]' % (sMovieTitle, sourceName)
        else:
            sDisplayTitle = sMovieTitle
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, streamUrl, sThumb)

    oGui.setEndOfDirectory()    