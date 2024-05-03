# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'filmsetvideos'
SITE_NAME = 'Films et Videos'
SITE_DESC = ' Bibliothèque illimitée de Films en Streaming VF'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = ('films/genre/recemment-ajoute', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

URL_SEARCH = ('index.php?do=search', 'showSearch')
URL_SEARCH_MOVIES = ('films/search/__data.json?x-sveltekit-trailing-slash=1&x-sveltekit-invalidated=1001&k=', 'showSearchMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH[1], 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showSearchMovies(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    listeGenre = ['Action', 'Animation', 'Aventure', 'Comedie', 'Crime', 'Documentaire', 'Drame',
                  'Familial', 'Fantastique', 'Guerre', 'Histoire', 'Horreur', 'Musique', 'Mystere', 'Romance',
                  'Science-fiction', 'Telefilm', 'Thriller', 'Western']

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', 'films/genre/' + genre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oUtil = cUtil()

    if sSearch:
        sSearchText = sSearch.split('=')[-1]
        sSearchText = oUtil.CleanName(sSearchText)

        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        sUrl = sSearch
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'rounded-t-lg" src="([^"]+)" alt="([^"]+)"><\/a> <div class="p-5"><a href="/([^"]+)">.+?Sortie en: (\d+)'

    series_noms = []

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sDesc = ''
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace(' streaming vf', '').strip()
            sTitle = oUtil.unescape(sTitle).replace('and#', "&#")
            sYear = aEntry[3]
            sUrl = aEntry[2]
            sThumb = URL_MAIN + aEntry[0]

            if '/tv' in sUrl:
                if sTitle in series_noms:  # une seule fois la série, filtrer les saisons
                    continue
                series_noms.append(sTitle)

            # Titre recherché
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sDisplayTitle = sTitle
            sTmdbId = sThumb.split('/')[-1].split('.')[0]

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addMovie(SITE_IDENTIFIER, 'showMovieHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '"font-semibold text-gray-900 dark:text-white">([^<]+)<\/span>nombre.+?Précédente.+?href="/([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = sNextPage.split('_')[-1]
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'

def showSearchMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()

    sSearchText = sSearch.split('=')[-1]
    sSearchText = oUtil.CleanName(sSearchText)

    sSearch = sSearch.replace(' ', '+').replace('%20', '+')
    sUrl = URL_MAIN + sSearch
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    result = json.loads(sHtmlContent)
    data = result['nodes'][3]
    
    tmdbIds = set()
    
    if 'data' in data:
        data = data['data']

        oOutputParameterHandler = cOutputParameterHandler()
        
        try:
            idx = 5
            for i in range(5, len(data)):
                ids = data[idx]
                idVideo = ids['id']
                idTitle = ids['title']
                idThumb = ids['poster_path']
                idYear = ids['release_year']
                idUrl = ids['url']
                
                if idUrl<idx:
                    break
                
                idx = idUrl+1
                if idx > len(data):
                    break

                video = data[idVideo]
                sTitle = data[idTitle]
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche
                
                sThumb = data[idThumb]
                sYear = str(data[idYear])
                sUrl = '%d/%s.html' % (video, data[idUrl])
                idTmdb = sThumb.replace('.jpg', '')

                if 'noThumbs' not in sThumb:
                    idTmdb = sThumb.replace('.jpg', '')
                    uniqueID = idTmdb
                else: 
                    idTmdb = ''
                    uniqueID = sTitle + sYear
                if uniqueID in tmdbIds:
                    continue
                tmdbIds.add(uniqueID)

                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', ('%sthumbs/%s') % (URL_MAIN, sThumb))
                oOutputParameterHandler.addParameter('sTmdbId', idTmdb)
                oOutputParameterHandler.addParameter('sYear', sYear)
    
                if '/tv' in sUrl:
                    sUrl2 = URL_MAIN + 'tv/?filter=year&q=' + sTitle
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
                else:
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oGui.addMovie(SITE_IDENTIFIER, 'showMovieHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        except:
            pass    # pour sortir de la lecture des reponses
        

def showMovieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = 'iframe:"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for sHosterUrl in aResult[1]:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
