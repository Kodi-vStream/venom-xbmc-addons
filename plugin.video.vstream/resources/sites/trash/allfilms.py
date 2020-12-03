# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
return False
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'allfilms'
SITE_NAME = 'All Films'
SITE_DESC = 'Films'

URL_MAIN = 'https://wvvw.allfilms.co/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'recherche-', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-1.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

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


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'recherche-Action-1.html'])
    liste.append(['Animation', URL_MAIN + 'recherche-Animation-1.html'])
    liste.append(['Aventure', URL_MAIN + 'recherche-aventure-1.html'])
    liste.append(['Biopic', URL_MAIN + 'recherche-Biopic-1.html'])
    liste.append(['Comédie', URL_MAIN + 'recherche-Comedie-1.html'])
    liste.append(['Comédie Dramatique', URL_MAIN + 'recherche-Comedie-dramatique-1.html'])
    liste.append(['Comédie Musicale', URL_MAIN + 'recherche-Comedie-musicale.html'])
    liste.append(['Divers', URL_MAIN + 'recherche-Divers-1.html'])
    liste.append(['Documentaire', URL_MAIN + 'recherche-Documentaire-1.html'])
    liste.append(['Drame', URL_MAIN + 'recherche-Drame-1.html'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'recherche-Epouvante-horreur-1.html'])
    liste.append(['Famille', URL_MAIN + 'recherche-Famille-1.html'])
    liste.append(['Fantastique', URL_MAIN + 'recherche-Fantastique-1.html'])
    liste.append(['Guerre', URL_MAIN + 'recherche-Guerre-1.html'])
    liste.append(['Opéra', URL_MAIN + 'recherche-Opera-1.html'])
    liste.append(['Policier', URL_MAIN + 'recherche-Policier-1.html'])
    liste.append(['Romance', URL_MAIN + 'recherche-romance-1.html'])
    liste.append(['Science Fiction', URL_MAIN + 'recherche-science-fiction-1.html'])
    liste.append(['Thriller', URL_MAIN + 'recherche-thriller-1.html'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    from itertools import chain
    generator = chain([1922, 1929, 1934, 1936, 1939, 1942, 1943, 1944, 1945, 1947, 1950, 1952]
                      , range(1953, 1956), [1957], range(1960, 2021))

    for i in reversed(list(generator)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'recherche-' + Year + '-1.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(' ', '-') + '.html'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="movie-card".+?src="([^"]+)".+?title">([^<]+).+?href="([^"]+)">([^<]+).+?label>([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0].replace(' ', '%20')
            if sThumb.startswith('poster'):
                sThumb = URL_MAIN + sThumb
            sTitle = aEntry[1]
            sUrl2 = aEntry[2]
            sQual = aEntry[3].upper()
            sLang = aEntry[4].upper()

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if aResult:
            sPattern = '-(\d+).html'
            aResult = oParser.parse(sUrl, sPattern)
            if (aResult[0] == True):
                number = int(aResult[1][0]) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', re.sub('-(\d+).html', '-' + str(number) + '.html', sUrl))

                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(number) + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
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
    sPattern = 'class="lectt " src=["\']([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    # fh = open('c:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
