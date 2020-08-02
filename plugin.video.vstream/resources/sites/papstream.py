# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'papstream'
SITE_NAME = 'PapStream'
SITE_DESC = 'Films, Séries & Mangas'

URL_MAIN = 'https://wvw.papstream.cc/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'rechercher', 'showMovies')

#recherche globale MOVIE/TVSHOWS
key_search_movies='#searchsomemovies'
key_search_series='#searchsomeseries'
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

MOVIE_MOVIE = (URL_MAIN + 'films.html', 'showMoviesMenu')
MOVIE_NEWS = (URL_MAIN + 'dernier-films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (URL_MAIN + 'series.html', 'showSeriesMenu')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

ANIM_ANIMS = (URL_MAIN + 'animes.html', 'showAnimesMenu')
ANIM_NEWS = (URL_MAIN + 'animes.html', 'showMovies')
#ANIM_GENRES = (URL_MAIN + 'animes/', 'showGenres')
ANIM_ANNEES = (True, 'showAnimeYears')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

#     oOutputParameterHandler = cOutputParameterHandler()
#     oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
#     oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action/'])
    liste.append(['Animation', sUrl + 'animation/'])
    liste.append(['Aventure', sUrl + 'aventure/'])
    liste.append(['Biopic', sUrl + 'biopic/'])
    liste.append(['Comédie', sUrl +'comedie/'])
    liste.append(['Comédie Dramatique', sUrl + 'comedie-dramatique/'])
    liste.append(['Comédie Musicale', sUrl + 'comedie-musicale/'])
    liste.append(['Documentaire', sUrl + 'documentaire/'])
    liste.append(['Drame', sUrl + 'drame/'])
    liste.append(['Epouvante Horreur', sUrl + 'epouvante-horreur/'])
    liste.append(['Famille', sUrl + 'famille/'])
    liste.append(['Fantastique', sUrl + 'fantastique/'])
    liste.append(['Guerre', sUrl + 'guerre/'])
    liste.append(['Policier', sUrl + 'policier/'])
    liste.append(['Romance', sUrl +'romance/'])
    liste.append(['Science Fiction', sUrl + 'science-fiction/'])
    liste.append(['Thriller', sUrl + 'thriller/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    for i in reversed(range(1918, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()

    for i in reversed(range(1936, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimeYears():
    oGui = cGui()

    for i in reversed(range(1965, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'animes/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    
    bSearchMovie=False
    bSearchSerie=False 
    if sSearch:
        KeySearch = sSearch
        if key_search_movies in KeySearch  :
            KeySearch =str(KeySearch ).replace( key_search_movies , '')
            bSearchMovie=True
        if key_search_series in KeySearch  :
            KeySearch =str(KeySearch ).replace( key_search_series , '')
            bSearchSerie=True
        sUrl = URL_SEARCH[0]
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine('story=' + KeySearch ) 
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="short-images-link".+?img src="([^"]+)".+?short-link"><a href="([^"]+)".+?>([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sThumb = URL_MAIN[:-1] + aEntry[0]
            sUrl2 = URL_MAIN[:-1] + aEntry[1].replace('/animes/films/', '/films/').replace('/animes/series/', '/series/')
            sTitle = aEntry[2]

            #
            if bSearchMovie :
                if '/series/' in sUrl2 :
                    continue  
            if bSearchSerie :
                if '/films/' in sUrl2 :
                    continue
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            if '/animes/' in sUrl2:
                oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif '/series/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('-([0-9]+).html', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="pages-numbers".+?<span>.+?</span><a href=["\']([^"\']+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sPattern = '</a> :</h2>(.+?)<div'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = aResult[1][0]

    # Decoupage pour cibler la partie des saisons
    sPattern = '<div id="full-video">(.+?)<div class="fstory-info block-p">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult

    sPattern = '<a href="([^"]+)" title=".+?(saison\s\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in reversed(aResult[1]):
            sUrl2 = aEntry[0]
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN[:-1] + sUrl2
            sSaison = aEntry[1]
            sTitle = ("%s %s") % (sMovieTitle, sSaison)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addEpisode(SITE_IDENTIFIER, 'ShowEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="saision_LI2">.*?<a title="Regarder (.+?) en streaming" href=["\']([^"\']+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[0]
            sUrl2 = URL_MAIN[:-1] + aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du synopsis pour les films
    if (not sDesc):
        sPattern = '</a> :</h2>(.+?)<div'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]

    sPattern = 'href="#" rel="([^"]+)".+?id="player".+?<i class="server player-.+?"></i>([^<]+)</span>.+?<img src="([^"]+)".+?<span style=".+?">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sHost = aEntry[1].capitalize()
            sLang = aEntry[2].replace('/images/', '').replace('.png', '')
            sQual = aEntry[3].replace('(', '').replace(')', '')
            sTitle = '%s [%s] (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle, sQual, sLang.upper(), sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('refUrl', sUrl)
            oOutputParameterHandler.addParameter('sUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    refUrl = oInputParameterHandler.getValue('refUrl')
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if sUrl.startswith('/'):
        sUrl = URL_MAIN[:-1] + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', refUrl)
    oRequestHandler.request()
    vUrl = oRequestHandler.getRealUrl()

    if vUrl:
        sHosterUrl = vUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
