# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons.
import json

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'darkiworld'
SITE_NAME = 'DarkiWorld'
SITE_DESC = 'Séries en illimité'


URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = URL_MAIN + 'api/v1/download/'


MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = ('movies?order=popularity%3Adesc?type=movie', 'showMovies')
MOVIE_VIEWS = ('trending-movies?type=movie', 'showMovies')
MOVIE_GENRES = ('movies?order=popularity%3Adesc&filters=%s?type=movie', 'showMovieGenres')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = ('series?order=popularity%3Adesc?type=series', 'showMovies')
SERIE_GENRES = ('series?order=popularity%3Adesc&filters=%s?type=series', 'showTvGenres')

ANIM_ANIMS = (True, 'showMenuAnimes')
ANIM_NEWS = ('animes?order=popularity%3Adesc?type=animes', 'showMovies')
ANIM_GENRES = ('animes?order=popularity%3Adesc&filters=%s?type=animes', 'showAnimGenres')

DOC_DOCS = (True, 'showMenuDivers')
DOC_DOC = ('docs?filters=W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls2XSwib3BlcmF0b3IiOiJoYXNBbGwifV0&order=popularity%3Adesc?type=movie', 'showMovies')
DOC_SERIE = ('docs?filters=W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls2XSwib3BlcmF0b3IiOiJoYXNBbGwifV0&order=popularity%3Adesc?type=serie', 'showMovies')
DOC_SPECTACLE = ('docs?filters=W3sia2V5IjoiY2F0ZWdvcnkiLCJ2YWx1ZSI6NzYsIm9wZXJhdG9yIjoiPSIsInZhbHVlS2V5Ijo3Nn1d&order=popularity%3Adesc?type=movie', 'showMovies')
DOC_REALITY = ('docs?filters=W3sia2V5IjoiY2F0ZWdvcnkiLCJ2YWx1ZSI6NzgsIm9wZXJhdG9yIjoiPSIsInZhbHVlS2V5Ijo3OH1d&order=popularity%3Adesc?type=serie', 'showMovies')


URL_SEARCH = ('search/', 'showSearch')
URL_SEARCH_MOVIES = ('search/%s?type=movie', 'showMovies')
URL_SEARCH_SERIES = ('search/%s?type=series', 'showMovies')
URL_SEARCH_ANIMS = ('search/%s?type=animes', 'showMovies')
URL_SEARCH_MISC = ('search/%s?type=doc', 'showMovies')



def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'series.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'films.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAnimes', 'Japanimes', 'animes.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuDivers', 'Autres', 'doc.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH[1], 'Rechercher', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH[1], 'Rechercher', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnimes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH[1], 'Rechercher', 'search-animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Par genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuDivers():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH[1], 'Rechercher', 'search-divers.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_DOC[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOC[1], 'Documentaires Films', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIE[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_SERIE[1], 'Documentaires Series', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_SPECTACLE[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_SPECTACLE[1], 'Spectacles', 'spectacle.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_REALITY[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_REALITY[1], 'Télé-Réalité', 'genres/Tele-Realite.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = siteUrl % sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    listeGenre = [
                  ['Action', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxXSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Animation', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlszXSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Aventure', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsyXSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Comédie', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls0XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Documentaire', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls2XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Drame', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls3XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Famille', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls4XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Fantastique', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls5XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Guerre', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxOF0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Historique', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxMF0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Horreur', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxMV0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Musique', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxMl0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Mystère', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxM10sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Romance', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxNF0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Policier', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls1XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Science-Fiction', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxNV0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Téléfilm', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxNl0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Thriller', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxN10sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Western', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxOV0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTvGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    listeGenre = [['Action & Aventure', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxOTQ2NF0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Animation', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlszXSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Comédie', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls0XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Documentaire', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls2XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Drame', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls3XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Enfants', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsyMjBdLCJvcGVyYXRvciI6Imhhc0FsbCJ9XQ'],
                  ['Famille', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls4XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Feuilleton', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls0NDhdLCJvcGVyYXRvciI6Imhhc0FsbCJ9XQ'],
                  ['Guerre & Politique', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls0ODFdLCJvcGVyYXRvciI6Imhhc0FsbCJ9XQ'],
                  ['Mystère', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxM10sIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Télé-Réalité', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsyOTJdLCJvcGVyYXRvciI6Imhhc0FsbCJ9XQ'],
                  ['Policier', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls1XSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Science-Fiction & Fantastique', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxODVdLCJvcGVyYXRvciI6Imhhc0FsbCJ9XQ'],
                  ['Western', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxOV0sIm9wZXJhdG9yIjoiaGFzQWxsIn1d']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    listeGenre = [['Action & Aventure', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsyMTFdLCJpc0luYWN0aXZlIjpmYWxzZSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Comédie', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls0XSwiaXNJbmFjdGl2ZSI6ZmFsc2UsIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Crime', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls1XSwiaXNJbmFjdGl2ZSI6ZmFsc2UsIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Documentaire', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls2XSwiaXNJbmFjdGl2ZSI6ZmFsc2UsIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Drame', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls3XSwiaXNJbmFjdGl2ZSI6ZmFsc2UsIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Enfants', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsyMjBdLCJpc0luYWN0aXZlIjpmYWxzZSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Famille', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls4XSwiaXNJbmFjdGl2ZSI6ZmFsc2UsIm9wZXJhdG9yIjoiaGFzQWxsIn1d'],
                  ['Guerre', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOls0ODFdLCJpc0luYWN0aXZlIjpmYWxzZSwib3BlcmF0b3IiOiJoYXNBbGwifV0'],
                  ['Mystère', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxM10sImlzSW5hY3RpdmUiOmZhbHNlLCJvcGVyYXRvciI6Imhhc0FsbCJ9XQ'],
                  ['Science-Fiction & Fantastique', 'W3sia2V5IjoiZ2VucmVzIiwidmFsdWUiOlsxODVdLCJpc0luYWN0aXZlIjpmYWxzZSwib3BlcmF0b3IiOiJoYXNBbGwifV0']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', siteUrl % sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()




def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    results =  []
     
    if sSearch:
        oUtil = cUtil()
        siteUrl, sType = sSearch.split('?type=')
        sSearchText = siteUrl.replace(URL_SEARCH[0],'')
        sSearchText = oUtil.CleanName(sSearchText)
        oRequestHandler = cRequestHandler(URL_MAIN + siteUrl)
        sHtmlContent = oRequestHandler.request()
        startJson = '{"searchPage":'
        endJson = ',"rendered_ssr"'
        aResult = oParser.abParse(sHtmlContent, startJson, endJson)
        aResult = json.loads(aResult)
        if aResult and 'results' in aResult['searchPage']:
            results = aResult['searchPage']['results']

    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl, sType = siteUrl.split('?type=')
        sPage = oInputParameterHandler.getValue('sPage')
        if not sPage:
            sPage = '1'
        else:
            sUrl += '&page=' + sPage
#        sType = 'series' if 'series?' in siteUrl else 'movie' if 'movie' in siteUrl else 'doc' if siteUrl.startswith('doc') else 'animes'
        oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
        sHtmlContent = oRequestHandler.request()
        startJson = '"data":'
        endJson = '},"loader":'
        aResult = oParser.abParse(sHtmlContent, startJson, endJson)
        aResult = json.loads('{'+aResult)
        results = aResult['data']
        
    oOutputParameterHandler = cOutputParameterHandler()
    for item in results:
        if not 'is_series' in item:     # ce n'est pas une vidéo
            continue
        is_series = item['is_series']
        itemType = item['type'] if 'type' in item else item['categorie']['model']
        
        typeOK = False
        if sType == itemType:
            typeOK = True
        elif sType == 'movie' and itemType == 'animes' and not is_series:
            typeOK = True       # anime film accepté pour la recherche de films
        if itemType == 'doc':
            if sType == 'movie' and not is_series:
                typeOK = True
            elif sType == 'serie' and is_series:
                typeOK = True
        if typeOK and sType == 'animes'and not is_series:
            typeOK = False      # anime film refusé pour la recherche d'animes
        
        if not typeOK:
            continue

        sTitle = item['name']
#            sTitle = cUtil().ASCIIDecode(sTitle)
        if sSearch:
            if not oUtil.CheckOccurence(sSearchText, sTitle):
                continue  # Filtre de recherche

        videoID = item['id']
        tmdbID = item['tmdb_id'] if 'tmdb_id' in item else ''
        sYear = item['year'] if 'year' in item else item['release_date'][:4]
        sThumb = item['poster']
        sDesc = item['description']
        sDisplayTitle = sTitle

        oOutputParameterHandler.addParameter('siteUrl', videoID)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sTmdbId', tmdbID)
        oOutputParameterHandler.addParameter('sYear', sYear)

        if sType == 'series':
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        elif sType == 'movie':
            oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        else:
            oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        iPage = int(sPage) + 1
        sPage = str(iPage)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', sPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showMovieLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    videoID = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    sUrl = URL_MAIN + 'download-page/' + videoID
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    
    # liens darkibox
    sHtmlContent = oParser.abParse(sHtmlContent, 'class="fi-ta-table', 'class="fi-ta-table')
    sPattern = 'type="checkbox".+?span class="truncate">(.+?)<.+?key=".+?record\.(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sorted(aResult[1]):
            sQual = aEntry[0].strip()
            videoId = aEntry[1]
            sDisplayTitle = '%s (%s)' % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', str(videoId))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'showMovieHoster', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    videoID = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = '%stitles/%s/series' % (URL_MAIN, videoID)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    startJson = '"seasons":{"current_page":1,'
    endJson = '},"rendered_ssr":'
    aResult = oParser.abParse(sHtmlContent, startJson, endJson)
    aResult = json.loads('{' + aResult)
    aResult = aResult['seasons']
    saisons = aResult['data']
    nbSaisons = aResult['total']

    oOutputParameterHandler = cOutputParameterHandler()
    if (len(saisons)==nbSaisons):       # la liste des saisons est donnée
        for saison in saisons[::-1]:
            numSaison = saison['number']
            sUrl2 = '%s/series/season/%d' % (videoID, numSaison)
            sDisplayTitle = ("%s Saison %d") % (sMovieTitle, numSaison)
    
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '',sThumb,'', oOutputParameterHandler)
    else: # sinon, utiliser le numéro de la derniere saison comme valeur max
        # ne pas prendre le max, car il peut manquer des saisons
        nbSaisons = saisons[0]['number']
        for numSaison in range(1, nbSaisons+1):
            sUrl2 = '%s/series/season/%d' % (videoID, numSaison)
            sDisplayTitle = ("%s Saison %d") % (sMovieTitle, numSaison)
    
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '',sThumb,'', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sPage = oInputParameterHandler.getValue('sPage')
    if sPage:
        sUrl += '?staleTime=300000&perPage=30&query=&page=' + sPage

    oRequestHandler = cRequestHandler(URL_MAIN + 'titles/' + sUrl)
    sHtmlContent = oRequestHandler.request()

    startJson = '"loader":"seasonPage","episodes":'
    endJson = '},"set_seo'
    aResult = oParser.abParse(sHtmlContent, startJson, endJson)
    aResult = aResult[len(startJson):] + '}'

    aResult = json.loads(aResult)
    episodes = aResult['data']
    
    oOutputParameterHandler = cOutputParameterHandler()
    for episode in episodes:
        if not 'primary_video' in episode:
            continue
        sUrl2 = episode['primary_video']['lien']
        iSeason = episode['season_number']
        iEp = episode['episode_number']
        sDisplayTitle = '%s S%dE%d' % (sMovieTitle, iSeason, iEp)
        sThumb = episode['poster']
        sDesc = episode['description']
        if not sDesc :
            sDesc = episode['name']
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addEpisode(SITE_IDENTIFIER, 'showSerieHoster', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    next_page = aResult['next_page']
    if next_page:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', next_page)
        oGui.addNext(SITE_IDENTIFIER, 'showEpisodes', 'Page %d' % next_page, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    videoID = oInputParameterHandler.getValue('siteUrl')
    sDisplayTitle = sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(URL_API + videoID)
    oRequest.addHeaderEntry('Referer', URL_MAIN + '/download/' + videoID)
    oRequest.addHeaderEntry('Accept', 'application/json')
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')
    oRequest.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    reponse = oRequest.request(jsonDecode=True)
    
    if not 'video' in reponse:
        oGui.setEndOfDirectory()
        return

    video = reponse['video']

    qual = None
    if 'qual' in video:
        qual = video['qual']['qual']

    sUrl = video['lien']
    oHoster = cHosterGui().checkHoster(sUrl)
    if not oHoster:
        oGui.setEndOfDirectory()
        return
        
    # Media info
    # langues = set()
    mediaInfo = ''
    if 'langues' in video:
        langues = []
        mediaInfo = 'Langues : '
        for langue in video['langues']:
            langues.append(langue['lang'])
        mediaInfo +=  ', '.join(langues)

    # sous-titres
    # if 'multilang' in video:
    #     multi = video['multilang']
    #     if multi and 'sub' in multi:
    #         subs = []
    #         for sub in multi['sub']:
    #             subs.append(sub.replace('4', 'FR').replace('5', 'EN'))
    #         mediaInfo += '\r\nSous-titres : ' + ', '.join(subs)

    if 'qual' in video:
        sDisplayTitle = '%s [%s]' % (sMovieTitle, qual)
        mediaInfo += '\r\nQualité : ' + video['qual']['qual']

    if 'taille' in video and video['taille'] >0:
        taille = video['taille']/1024/1024/1024
        mediaInfo += '\r\nTaille : %0.2f Go' % taille
    
    oHoster.setDisplayName(sDisplayTitle)
    oHoster.setFileName(sMovieTitle)
    if mediaInfo:
        oHoster.setMediaInfo(mediaInfo)
    cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)
    
    oGui.setEndOfDirectory()


def showSerieHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sUrl)
    if oHoster:
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

    oGui.setEndOfDirectory()

