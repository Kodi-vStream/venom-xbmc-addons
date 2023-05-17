# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
return False  # 11/02/22 - Plus de liens

import re
import base64

from resources.lib.comaddon import progress
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'filmstoon_pro'
SITE_NAME = 'Films toon'
SITE_DESC = 'Films en streaming'

URL_MAIN = "https://filmstoon.in/"

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'movies/page/1/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

# on rajoute le tag page/1/ sur les premieres pages, utilisé par la fonction nextpage pas de liens next
SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/page/1/', 'showMovies')
SERIE_NEWS_EPISODE = (URL_MAIN + 'episode/page/1/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

# variables globales
key_search_movies = '#searchsomemovies#'
key_search_series = '#searchsomeseries#'
URL_SEARCH_MOVIES = (key_search_movies, 'showSearch')
URL_SEARCH_SERIES = (key_search_series, 'showSearch')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, URL_SEARCH_SERIES[1], 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODE[1], 'Episodes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl += sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    # https://filmstoon.in/genre/action/

    liste = []
    listegenre = ['action', 'animation', 'aventure', 'comedie', 'crime', 'Documentaire', 'drame', 'familial',
                  'fantastique', 'guerre', 'horreur', 'musique', 'romance', 'thriller', 'science-fiction']

    url1g = URL_MAIN + 'genre/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre + '/page/1/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    # https://filmstoon.in/release-year/2020/
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1935, 2023)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'release-year/' + sYear + '/page/1/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    bSearchMovie = False
    bSearchSerie = False

    if sSearch:
        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True

        elif key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        oUtil = cUtil()
        sSearch = oUtil.CleanName(sSearch)
        sUrl = URL_SEARCH[0] + sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url image alt year desc
    sPattern = 'class="ml-item".+?href="([^"]+).+?src="([^"]+).+?alt="([^"]+).+?(?:|tag">([^<]*).+?)desc">(.*?)</p'
    oParser = cParser()
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

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\d+/', '/w342/', aEntry[1])
            sTitle = aEntry[2]
            if 'episode' in sUrl or '/series/' in sUrl:
                sTitle = sTitle.replace('- Season', ' ').replace('-Season', ' ').replace('Season', '').replace('- Saison', '')
                sTitle = re.sub('\d+', '',sTitle)
            sYear = aEntry[3]
            sDesc = aEntry[4].replace('<p>', '')

            if bSearchMovie:
                if 'series' in sUrl2:
                    continue
            if bSearchSerie:
                if 'series' not in sUrl2:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearch, sTitle):
                    continue


            if sDesc:
                sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', sDesc)

            sDisplayTitle = sTitle
            if sSearch or 'genre/' in sUrl or 'release-year/' in sUrl:
                if 'series' in sUrl2:
                    sDisplayTitle = sDisplayTitle + ' [Série]'
                else:
                    sDisplayTitle = sDisplayTitle + ' [Film]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if 'series' not in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalid, sNextPage, sNumPage = __checkForNextPage(sHtmlContent, sUrl)
        if (bvalid == True):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(shtml, surl):
    # pas de lien next page on crée l'url et on verifie l'index de la derniere page
    sMax = ''
    iMax = 0
    sPattern = 'page/(\d+)/'
    oParser = cParser()
    aResult = oParser.parse(shtml, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sCurrentMax = aEntry
            iCurrentMax = int(sCurrentMax)
            if iCurrentMax > iMax:
                iMax = iCurrentMax
                sMax = sCurrentMax

    sPattern = 'page.(\d+)'
    oParser = cParser()
    aResult = oParser.parse(surl, sPattern)
    if aResult[0]:
        sCurrent = aResult[1][0]
        iCurrent = int(sCurrent)
        iNext = iCurrent + 1
        sNext = str(iNext)
        pCurrent = 'page/' + sCurrent
        pNext = 'page/' + sNext
        sUrlNext = surl.replace(pCurrent, pNext)

    else:
        return False, False, False

    if iMax != 0 and iMax >= iNext:
        return True, sUrlNext, sNext + '/' + sMax

    elif iNext == 0:  # c'est un bug de programmation
        return False, False, False

    return False, False, False

def showSaison():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # permet de couper une partie précise du code html pour récupérer plus simplement les episodes.
    sStart = 'class="les-title"'
    sEnd = '<div class="mvi-content"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<strong>Season.+?(\d+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    sSaison = ''

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sNumSaison = aEntry[0]
            sSaison = 'Saison ' + aEntry[0]
            sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
            sDisplayTitle =  sMovieTitle + ' ' +  sSaison
            sTitle = sMovieTitle 

            oOutputParameterHandler.addParameter('siteUrl', sUrlSaison)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addSeason(SITE_IDENTIFIER, 'showSXE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSXE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    
    sUrl, sNumSaison  = sUrl.split('?sNumSaison=')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # permet de couper une partie précise du code html pour récupéré plus simplement les episodes.
    sStart = '<strong>Season ' + sNumSaison
    sEnd = '<div class="tvseason">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = '<a href="([^"]+).+?Episode.+?(\d+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            Ep = aEntry[1]
            Saison = 'Saison ' + sNumSaison
            sTitle = sMovieTitle + ' ' + Saison + ' Episode' + Ep

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # 1 seul host constaté 10112020 : uqload

    # sHosterUrl = ''
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<div class="movieplay"><iframe src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        if 'embedo' in aResult[1][0]:

            # url1 https://embedo.to/e/QW9RSEhEeEZFUTJXVXo0dzBhdzhVZz09
            # url2 https://embedo.to/s/cTJtdlNDY2J5aGM9
            # url3 https://embedo.to/r/cTJtdlNDY2J5aGM9

            url1 = aResult[1][0]
            oRequestHandler = cRequestHandler(url1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'window.park = "([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                redirect = base64.b64decode(aResult[1][0])
                sPattern = '"page_url":"([^"]+)'
                aResult = oParser.parse(redirect, sPattern)
    
                if aResult[0]:
    
                    url2 = aResult[1][0]
                    url3 = url2.replace('\\', '').replace('/s/', '/r/')
    
                    oRequestHandler = cRequestHandler(url3)
                    oRequestHandler.addHeaderEntry('Referer', sUrl)
                    oRequestHandler.addHeaderEntry('connection', 'keep-alive')
                    sHtmlContent = oRequestHandler.request()
                    getReal = oRequestHandler.getRealUrl()
    
                    if 'http' in getReal:
                        sHosterUrl = getReal
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        sDisplayTitle = sMovieTitle
                        if (oHoster):
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
