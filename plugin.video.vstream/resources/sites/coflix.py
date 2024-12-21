# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#Nouvelle source de streaming FILMS ET SÉRIES
import re
import base64

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'coflix'
SITE_NAME = 'coflix'
SITE_DESC = 'Films et Séries en Streaming VF Complet Qualite HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

# sort
# 1 - derniers ajouts
# 5 - année (<2022)
# 6 - année (<2022)
# 9 - alpha
# 10 - antealpha

# Pour les Films
MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = ('wp-json/apiflix/v1/options/?post_type=movies&sort=1&page=', 'showMoviesAPI')
MOVIE_VIEWS = ('film', 'showMovies')
MOVIE_GENRES = ('wp-json/apiflix/v1/options/?post_type=movies&genres=%d&sort=1&page=', 'showMovieGenres')
MOVIE_ANNEES = ('wp-json/apiflix/v1/options/?post_type=movies&years=%d&sort=1&page=', 'showYears')

# Pour les Series
SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = ('wp-json/apiflix/v1/options/?post_type=series&sort=1&page=', 'showMoviesAPI')
SERIE_VIEWS = ('serie', 'showMovies')
SERIE_GENRES = ('wp-json/apiflix/v1/options/?post_type=series&genres=%d&sort=1&page=', 'showSeriesGenres')
SERIE_ANNEES = ('wp-json/apiflix/v1/options/?post_type=series&years=%d&sort=1&page=', 'showYears')

# Pour les Animes
ANIM_ANIMS = (True, 'showMenuAnimes')
ANIM_NEWS = ('wp-json/apiflix/v1/options/?post_type=animes&sort=1&page=', 'showMoviesAPI')
ANIM_GENRES = ('wp-json/apiflix/v1/options/?post_type=animes&genres=%d&sort=1&page=', 'showAnimesGenres')
ANIM_ANNEES = ('wp-json/apiflix/v1/options/?post_type=animes&years=%d&sort=1&page=', 'showYears')

URL_SEARCH = ('index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = ('?post_type=movies&s=', 'showMovies')
URL_SEARCH_SERIES = ('?post_type=series&s=', 'showMovies')
URL_SEARCH_ANIMS = ('?post_type=animes&s=', 'showMovies')

API_EPISODES = 'wp-json/apiflix/v1/series/%s/%s' # serieID, numSaison
API_EPISODE_LINK = 'wp-json/apiflix/v1/playerepisode?post_id=%s'
API_MOVIE_LINK = 'wp-json/apiflix/v1/playermovie?post_id=%s'


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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Par années', 'annees.png', oOutputParameterHandler)

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

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Par années', 'annees.png', oOutputParameterHandler)
     
    oGui.setEndOfDirectory()


def showMenuAnimes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Par années', 'annees.png', oOutputParameterHandler)
     
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
    for sTitle, sUrl in listegenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMoviesAPI', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    import datetime
    oGui = cGui()
    
    # 1950 -> 2024
    yearsId = [43696, 86919, 43747, 67554, 27830, 29143, 13802, 30442, 47916, 50822, 
               21584, 76706, 43717, 45627, 34587, 26675, 14471, 106570, 30200, 19435, 
               30131, 21220, 21155, 22468, 28989, 40512, 21640, 22377, 58748, 33405, 
               23100, 25211, 9124, 32527, 37815, 10127, 22817, 27291, 23932, 17898, 
               21098, 27539, 28149, 19388, 15750, 21137, 19773, 9834, 13770, 21079, 
               19465, 8798, 2757, 18038, 13687, 9755, 429, 14119, 14482, 14255, 8906, 
               1426, 4372, 5590, 11223, 9201, 1843, 3321, 414, 2123, 60, 374, 99, 9272, 120358]

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    dateStart = 1950
    
    if 'series' in siteUrl:
        yearsId = yearsId[50:]  # > 2000
        dateStart = 2000
    
    yearsId = yearsId[::-1]
    yearIdx=0
    oOutputParameterHandler = cOutputParameterHandler()
    for iYear in reversed(range(dateStart, int(datetime.datetime.now().year) + 1)):
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % yearsId[yearIdx])
        oGui.addDir(SITE_IDENTIFIER, 'showMoviesAPI', str(iYear), 'annees.png', oOutputParameterHandler)
        yearIdx += 1

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
        oGui.addGenre(SITE_IDENTIFIER, 'showMoviesAPI', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimesGenres():
    oGui = cGui()
    listegenre = [['Action & Aventure', 2930], ['Animation', 6914], ['Comédie', 6427],
                  ['Crime', 6520], ['Drame', 6414], ['Famille', 7182], ['Guerre & Politique', 3021],
                  ['Kids', 50], ['Mystère', 6415], ['Science-Fiction & Fantastique', 8194]]

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listegenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMoviesAPI', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesAPI():
    oGui = cGui()
    oUtil = cUtil()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sPage = oInputParameterHandler.getValue('sPage')
    
    if not sPage:
        sPage= '1'
    
    oRequestHandler = cRequestHandler(URL_MAIN + siteUrl + sPage)
    responses = oRequestHandler.request(jsonDecode=True)
    oOutputParameterHandler = cOutputParameterHandler()

    if 'results' in responses:
        oOutputParameterHandler = cOutputParameterHandler()
        movies = responses['results']
        for movie in movies:
            sTitle = oUtil.unescape(movie['name'])
            movie_id = movie['uuid']
            sUrl = movie['url']
            sCat = movie['ts']
            sYear = movie['release']
            sDesc = re.search('>([^<]+)', movie['excerpt']).group(1)
            sThumb = 'https:' + re.search('src="([^"]+)', movie['path']).group(1)
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if sCat == 'movies':
                sUrl = API_MOVIE_LINK % movie_id
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    iPage = int(sPage) + 1
    sPage = str(iPage)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
    oOutputParameterHandler.addParameter('sPage', sPage)
    oGui.addNext(SITE_IDENTIFIER, 'showMoviesAPI', 'Page ' + sPage, oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    bSearchMovie = False
    bSearchSerie = False
    bSearchAnimes = False
    
    if sSearch:
        oUtil = cUtil()
        if URL_SEARCH_MOVIES[0] in sSearch:
            bSearchMovie = True
        elif URL_SEARCH_SERIES[0] in sSearch:
            bSearchSerie = True
        elif URL_SEARCH_ANIMS[0] in sSearch:
            bSearchAnimes = True
        sSearchText = oUtil.CleanName(sSearch.split('=')[-1])
        sUrl = URL_MAIN + sSearch
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequest.request()
        sHtmlContent = oParser.abParse(sHtmlContent, '<main id="content"', 'wdgt_lateral_movies-')

        # id thumb titre year desc url
        sPattern = '"bx por" data-uuid="(\d+).+?src="([^"]+).+?class="fg1">.+?fz14">([^<]+)<.+?fwb"><span>(|\d+)<.+?mb1">([^<]+).+?<a href="([^"]+)'
    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = URL_MAIN + siteUrl
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequest.request()
        
        if siteUrl == 'film':
            sHtmlContent = oParser.abParse(sHtmlContent, 'wdgt_lateral_movies-', 'wdgt_lateral_movies-')
        else:   # séries populaires
            sHtmlContent = oParser.abParse(sHtmlContent, 'wdgt_lateral_movies-7')
        
        # titre year desc url
        sPattern = '<img loading="lazy" src="([^"]+).+?class="fg1">.+?fz14">([^<]+)<.+?fwb"><span>(\d+)<.+?mb1">([^<]+).+?href="([^"]+)'
        
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if aResult[0]:
        titles = set()
        sThumb = ''
        idx = 1 if sSearch else 0
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = aEntry[idx]
            sTitle = aEntry[idx + 1]
            sYear = aEntry[idx + 2]
            sDesc = aEntry[idx + 3]
            sUrl2 = aEntry[idx + 4]

            if sSearch:
                if bSearchMovie and not '/film/' in sUrl2:
                    continue
                if bSearchSerie and not '/serie/' in sUrl2:
                    continue
                if bSearchAnimes and not '/animes/' in sUrl2:
                    continue
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche
            else:
                if sTitle in titles:    # passer les doublons
                    continue
                titles.add(sTitle)
                
            sDisplayTitle = sTitle
            if 'http' not in sThumb:
                sThumb = 'https:' + sThumb

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/film/' in sUrl2:
                if sSearch:
                    oOutputParameterHandler.addParameter('siteUrl', API_MOVIE_LINK % aEntry[0])
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/animes/' in sUrl2:
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        oGui.setEndOfDirectory()


# afficher les Saisons
def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'name="seasons" data-season="(\d+)" data-id="\d+" post-id="(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = API_EPISODES % (aEntry[1], aEntry[0]) 
            sTitle = ("%s - S%s") % (sMovieTitle, aEntry[0])
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    oRequestHandler = cRequestHandler(sUrl)
    responses = oRequestHandler.request(jsonDecode=True)

    if 'episodes' in responses and responses['episodes']:
        oOutputParameterHandler = cOutputParameterHandler()
        episodes = responses['episodes']
        for episode in episodes:
            episode_id = episode['id']
            # numEp = episode['number']
            # numSaison = episode['season']
            # epUrl = episode['links']
            sTitle = episode['title']
            epUrl = API_EPISODE_LINK % episode_id
            sThumb = re.search('src="([^"]+)', episode['image']).group(1)
            if 'http' not in sThumb:
                sThumb = 'https:' + sThumb

            oOutputParameterHandler.addParameter('siteUrl', epUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    responses = oRequestHandler.request(jsonDecode=True)

    if 'links' in responses:
        links = responses['links']
        if 'online' in links:
            for hosters in links['online']:
                oRequestHandler = cRequestHandler(hosters['link'])
                sHtmlContent = oRequestHandler.request()
                sPattern = '<li onclick="showVideo\(\'([^\']+)'
                aResult = oParser.parse(sHtmlContent, sPattern)
            
                if aResult[0]:
                    for sHosterUrl in aResult[1]:
                        
                        sHosterUrl = base64.b64decode(sHosterUrl).decode("utf-8")
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if not oHoster:
                            continue
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showMovieLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe src=\"([^\"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = aResult[1][0]
        oRequestHandler = cRequestHandler(sHosterUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<li onclick="showVideo\(\'([^\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if aResult[0]:
            for sHosterUrl in aResult[1]:
                sHosterUrl = base64.b64decode(sHosterUrl).decode("utf-8")
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if not oHoster:
                    continue
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


