# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
# import unicodedata

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'topstream'
SITE_NAME = 'TopStream'
SITE_DESC = 'Le meilleur du divertissement en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('movies?type=movie', 'showMenuMovies')
MOVIE_NEWS = ('filmstreaming/', 'showMovies')
MOVIE_GENRES = ('movies?type=movie&genre=%s&sort=created_at', 'showGenres')
MOVIE_NEWS = ('filmstreaming/', 'showMovies')
MOVIE_VIEWS = ('trending?type=movie&sort=like_count', 'showMovies')
MOVIE_ANNEES = ('movies?type=movie&sort=release_date&release=%d', 'showMovieYears')


SERIE_SERIES = ('type=tv', 'showMenuTvShows')
SERIE_NEWS = ('seriestreaming/', 'showMovies')
SERIE_VIEWS = ('trending?type=tv&sort=like_count', 'showMovies')
SERIE_GENRES = ('tv-shows?type=tv&genre=%s&sort=created_at', 'showSeriesGenres')
SERIE_ANNEES = ('tv-shows?type=tv&sort=release_date&release=%d', 'showMovies')

# ANIM_ANIMS = ('genre=15', 'load')
# ANIM_VIEWS = ('tv-shows?type=tv&genre=15&sort=view', 'showMovies')


URL_SEARCH = ('search/%s', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + '?type=movie', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + '?type=tv', 'showMovies')
#URL_SEARCH_ANIMS = (URL_SEARCH[0] + '?genre=15', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showMenuAnimes', 'Japanimes', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# def showMenuAnimes():
#     oGui = cGui()
#
#     oOutputParameterHandler = cOutputParameterHandler()
#     oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
#     oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search-animes.png', oOutputParameterHandler)
#
#     oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
#     oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Populaires', 'popular.png', oOutputParameterHandler)
#
#     oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl %= sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', '1'], ['Animation', '5'], ['Aventure', '16'], ['Comédie', '6'],
             ['Crime', '3'], ['Documentaire', '7'], ['Drame', '8'], ['Familial', '9'],
             ['Fantastique', '10'], ['Guerre', '18'], ['Histoire', '11'], ['Horreur', '4'],
             ['Mystère', '2'], ['Romance', '14'], ['Science-Fiction', '12'], ['Thriller', '13'] ]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, codeGenre in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0] % codeGenre)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesGenres():
    oGui = cGui()

#japanime 15 

    liste = [['Action', '1'], ['Comédie', '6'],
             ['Crime', '3'], ['Documentaire', '7'], ['Drame', '8'], ['Familial', '9'],
             ['Mystère', '2'] ]


    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, codeGenre in liste:
        oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0] % codeGenre)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    import datetime
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for year in reversed(range(1955, int(datetime.datetime.now().year) + 1)):
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0] % year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(year), 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()

    bMovie = bShow = bAnime = False
    if sSearch:
        sUrl = sSearch
        sSearchTerm = re.search('search/(.+?)\?', sSearch).group(1)
        sSearchTerm = sSearchTerm.replace('%20', ' ')
    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = sUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
        if sPage:
            if '?' in siteUrl:
                sUrl += '&page=' + sPage
            else:
                sUrl += '?page=' + sPage

    if 'type=movie' in sUrl:
        bMovie = True
    elif 'type=tv' in sSearch:
        bShow = True
    else:
        bAnime = True

    sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url img title year
    sPattern = '<a href="([^"]+)" *class="aspect-poster.+?data-src="([^"]+)" alt="([^"]+)".+?class="pt-4 transition".+?<span>(\d{4})'
            
    aResult = oParser.parse(sHtmlContent, sPattern)

    # en cas de recherche vide, deuxieme tentative avec le mot le plus long
    if sSearch and not aResult[0]:
        if ' ' in sSearchTerm:
            termes = sSearchTerm.split(' ')
            termes = sorted(termes, key=lambda terme: len(terme))[::-1]
            if bMovie:
                sUrl = URL_MAIN + URL_SEARCH_MOVIES[0] % termes[0]
            else:
                sUrl = URL_MAIN + URL_SEARCH_SERIES[0] % termes[0]
                
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            aResult = oParser.parse(sHtmlContent, sPattern)
            

    if aResult[0]:
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[3]

            # filtre search
            if sSearch and total > 2:
                if not oUtil.CheckOccurence(sSearchTerm, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if bMovie:            
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif bShow:
                sMovieTitle = re.sub('  S\d+', '', sTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                sMovieTitle = re.sub('  S\d+', '', sTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        if sPage:
            sPage = str(int(sPage)+1)
        else:
            sPage = '2'
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', sPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = URL_MAIN + oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = ''

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # id title
    sPattern = 'wire:click="updateSeason\(\'(\d+)\'\)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

#            sUrl = aEntry[0]
            sDisplayTitle = sSaison = aEntry[1].strip()
            sTitle = sMovieTitle
            if 'Saison' in sSaison:
                sTitle = sMovieTitle + ' ' + sSaison
                sDisplayTitle = sMovieTitle + ' ' + sSaison

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    sUrl = ('%sepisode/%s/%s-1') % (URL_MAIN, sUrl.split('/')[-1], sMovieTitle.split(' ')[-1])

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url title
    sPattern = 'href="([^"]+)" *class="flex transition.+?font-medium">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1].replace('n°', '')

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    # zone publicitaire !
    zonePub = oParser.abParse(sHtmlContent, '<div class="container">', '<style>')
    zonePub = zonePub.replace('\\', '')
    sPattern = '/(embed/\d+)'
    aResult = oParser.parse(zonePub, sPattern)
    if not aResult[0]:
        # page sans pub
        sPattern = '<iframe id="video-iframe".+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        url = aResult[1][0]
        if not 'http' in url:
            url = URL_MAIN + url
        oRequestHandler = cRequestHandler(url)
        sHtmlContent = oRequestHandler.request()
        aResult = oParser.parse(sHtmlContent, '<source src="([^"]+)"')

    if aResult[0]:
        oHosterGui = cHosterGui()
        for sHosterUrl in aResult[1]:
            oHoster = oHosterGui.checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



