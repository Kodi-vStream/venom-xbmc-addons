# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'coflix'
SITE_NAME = 'Coflix'
SITE_DESC = 'Films et Séries en Streaming VF Complet Qualite HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_api')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = ('content?types=movies&orderby=date&order=desc&per_page=20&page=', 'showMovies')
MOVIE_VIEWS = ('movies/top?per_page=20&page=', 'showMovies')
MOVIE_GENRES = ('content/category/%d?types=movies&per_page=30&page=', 'showMovieGenres')
#MOVIE_ANNEES = ('content?types=movies&year=%d&per_page=20&page=', 'showYears')

# Pour les Series
SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = ('content?types=series&orderby=date&order=desc&per_page=20&page=', 'showMovies')
SERIE_VIEWS = ('series/top?per_page=20&page=', 'showMovies')
SERIE_GENRES = ('content/category/%d?types=series&per_page=30&page=', 'showSeriesGenres')

# Pour les Animes
ANIM_ANIMS = (True, 'showMenuAnimes')
ANIM_NEWS = ('content?types=animes&orderby=date&order=desc&per_page=20&page=', 'showMovies')

URL_SEARCH = ('suggest.php?query=', 'showMovies')
URL_SEARCH_MOVIES = ('content?types=movies&per_page=20&search=', 'showMovies')
URL_SEARCH_SERIES = ('content?types=series&per_page=20&search=', 'showMovies')
URL_SEARCH_ANIMS = ('content?types=animes&per_page=20&search=', 'showMovies')


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAnimes', 'Japanimes', 'animes.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Par années', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnimes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = siteUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()
    listegenre = [['Action', 6410], ['Animation', 6914], ['Aventure', 6411],
                  ['Comédie', 6427], ['Crime', 6520], ['Documentaire', 8882],
                  ['Drame', 6414], ['Famille', 7182], ['Fantastique', 6412],
                  ['Guerre', 6521], ['Historique', 6807], ['Horreur', 6509],
                  ['Musique', 8502], ['Mystère', 6415], ['Romance', 43],
                  ['Science-Fiction', 7357], ['Telefilm', 6576], ['Thriller', 6416], ['western', 51]]

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, genreID in listegenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % genreID)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    import datetime
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    dateStart = 1950

    oOutputParameterHandler = cOutputParameterHandler()
    for iYear in reversed(range(dateStart, int(datetime.datetime.now().year) + 1)):
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % iYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(iYear), 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesGenres():
    oGui = cGui()
    listegenre = [['Action & Aventure', 2930], ['Animation', 6914], ['Comédie', 6427],
                  ['Crime', 6520], ['Documentaire', 8882], ['Drame', 6414],
                  ['Famille', 7182], ['Feuilleton', 2919], ['Guerre & Politique', 3021],
                  ['Kids', 50], ['Mystère', 6415], ['Science-Fiction & Fantastique', 8194],
                  ['Télé réalité', 3213], ['western', 51]]

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listegenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oUtil = cUtil()
    if sSearch:
        sSearchText = sSearch.split('=')[-1]
        siteUrl = sSearch
        sUrl = URL_API + siteUrl
        mediaType = None
    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
        if not sPage:
            sPage = '1'
        sUrl = URL_API + siteUrl + sPage

        args = siteUrl.split('?')[1].split('&')
        params = dict(item.split('=', 1) for item in args)
        mediaType = params.get('types', None)

    oRequestHandler = cRequestHandler(sUrl)
    responses = oRequestHandler.request()
    movies = json.loads(responses)

    # if 'results' in responses:
    oOutputParameterHandler = cOutputParameterHandler()
    #     movies = responses['results']
    for movie in movies:
        sCat = movie['type']
        if mediaType and mediaType != sCat:
            continue

        sTitle = oUtil.unescape(movie['titles']['name'])

        # Filtre de recherche
        if sSearch:
            if not oUtil.CheckOccurence(sSearchText, sTitle):
                continue

        movieId = movie['_meta']['id']
        slug = movie['_meta']['slug']
        sUrl = movie['link']
        sYear = movie['releaseDate'].split('-')[0]
        sDesc = movie['overview'].replace('<p>', '').replace('</p>', '')
        sTmdbId = movie['TMDbId']
        sThumb = movie['images']['poster']

        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        oOutputParameterHandler.addParameter('sYear', sYear)

        if sCat == 'movies':
            sUrl = 'resolve?tmdb=%s&type=%s&pid=%s' % (sTmdbId, sCat, movieId)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addMovie(SITE_IDENTIFIER, 'showMovieHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        elif sCat == 'series':
            sUrl = 'content/%s?type=series&pid=%s' % (slug, movieId)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        else:
            sUrl = 'content/%s?pid=%s' % (slug, movieId)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        iPage = int(sPage) + 1
        sPage = str(iPage)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', sPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()



# afficher les Saisons
def showSaisons():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    serie = oRequestHandler.request(True)
    
    if not 'code' in serie:
        serie = serie.get('serie', serie.get('anime'))
        sTmdbId = serie['TMDbId']
        serieId = serie['id']
        
        for saison in sorted(serie['seasons'], key=lambda saison : saison['number']):
            numSaison = saison['number']
            sTitle = ("%s - S%d") % (sMovieTitle, numSaison)
            sUrl = 'content/%d/episodes?per_page=300' % serieId
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sSaison', numSaison)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sDesc = oInputParameterHandler.getValue('sDesc')
    saisonSearch = oInputParameterHandler.getValue('sSaison')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    episodes = oRequestHandler.request(True)

    saisonSearch = int(saisonSearch)
    episodeSaison = []
    for episode in episodes:
        numSaison = episode['season_number']
        if numSaison != saisonSearch:
            continue
        episodeSaison.append(episode)

    for episode in episodeSaison:
        numEp = episode['episode_number']
        epID = episode['id']
        sDisplayTitle = episode['name']
        # sTitle = '%s S%dE%d' % (sMovieTitle, saisonSearch, numEp)
        if sTmdbId:
            sUrl = 'resolve?tmdb=%s&type=tv&season=%d&episode=%d&tid=%s' % (sTmdbId, saisonSearch, numEp, epID)
        else:
            sUrl = 'resolve?title=%s&type=tv&season=%d&episode=%d&tid=%s' % (sMovieTitle, saisonSearch, numEp, epID)
        
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addEpisode(SITE_IDENTIFIER, 'showMovieHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    oGui.setEndOfDirectory()


def showMovieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    response = oRequestHandler.request(jsonDecode=True)

    isOK = response.get('ok', False)
    key = response.get('key', False)
    if isOK and key:
        oOutputParameterHandler = cOutputParameterHandler()
        sThumb = response.get('poster', '')
        for server in response['servers']:
            host = server.get('host')
            oHoster = cHosterGui().checkHoster(host)
            if not oHoster:
                continue
            lang = server.get('lang')
#            sDisplayTitle = '%s [%s] - %s' % (response.get('display', sTitle), lang, host)
            sDisplayTitle = '%s [%s] - %s' % (sTitle, lang, host)

            sUrl = 'wp-json/coflix/v1/play?k=%s&i=%d' % (key, server['i'])
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
    
def showHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    response = oRequestHandler.request(jsonDecode=True)

    isOK = response.get('ok', False)
    if isOK:
        #host = response.get('host')
        sHosterUrl = response.get('play', response.get('url', ''))
        if sHosterUrl:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
    oGui.setEndOfDirectory()

