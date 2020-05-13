# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'zonefilms'
SITE_NAME = 'Zone Films'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = 'https://www.zone-films1.stream/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_CLASSICS = (URL_MAIN + 'vieux-films.html', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

MOVIE_2020 = (URL_MAIN + 'films-2020.html', 'showMovies')
MOVIE_2019 = (URL_MAIN + 'films-2019.html', 'showMovies')
MOVIE_2010 = (URL_MAIN + 'films-2010-2018.html', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009.html', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999.html', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989.html', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979.html', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969.html', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959.html', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1920-1949.html', 'showMovies')

# Pas de recherche sur cette source
# URL_SEARCH = (URL_MAIN + 'index.php?do=', 'showMovies')
# URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
# FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    # Pas de recherche sur cette source
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSICS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASSICS[1], 'Films (Classiques)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# def showSearch():
    # oGui = cGui()

    # sSearchText = oGui.showKeyBoard()
    # if (sSearchText != False):
        # sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        # showMovies(sUrl)
        # oGui.setEndOfDirectory()
        # return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'action.html'])
    liste.append(['Animation', URL_MAIN + 'animation.html'])
    liste.append(['Aventure', URL_MAIN + 'aventure.html'])
    liste.append(['Biopic', URL_MAIN + 'biopic.html'])
    liste.append(['Comédie dramatique', URL_MAIN + 'comedie-dramatique.html'])
    liste.append(['Comédie musicale', URL_MAIN + 'comedie-musicale.html'])
    liste.append(['Comédie', URL_MAIN + 'comedie.html'])
    liste.append(['Divers', URL_MAIN + 'divers.html'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire.html'])
    liste.append(['Drame', URL_MAIN + 'drame.html'])
    liste.append(['Epouvante-horreur', URL_MAIN + 'epouvante-horreur.html'])
    liste.append(['Espionnage', URL_MAIN + 'espionnage.html'])
    liste.append(['Famille', URL_MAIN + 'famille.html'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique.html'])
    liste.append(['Guerre', URL_MAIN + 'guerre.html'])
    liste.append(['Historique', URL_MAIN + 'historique.html'])
    liste.append(['Musical', URL_MAIN + 'musique.html'])
    liste.append(['Péplum', URL_MAIN + 'peplum.html'])
    liste.append(['Policier', URL_MAIN + 'policier.html'])
    liste.append(['Romance', URL_MAIN + 'romance.html'])
    liste.append(['Science fiction', URL_MAIN + 'science-fiction.html'])
    liste.append(['Thriller', URL_MAIN + 'thriller.html'])
    liste.append(['Western', URL_MAIN + 'western.html'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2020[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2020[1], 'Films (2020)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2019[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2019[1], 'Films (2019)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2010[1], 'Films (2010 à 2018)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2000[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2000[1], 'Films (2000 à 2009)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1990[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1990[1], 'Films (1990 à 1999)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1980[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1980[1], 'Films (1980 à 1989)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1970[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1970[1], 'Films (1970 à 1979)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1960[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1960[1], 'Films (1960 à 1969)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1950[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1950[1], 'Films (1950 à 1959)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1900[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1900[1], 'Films (Avant 1950)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<!-- END HEADER -->'
    sEnd = '<!-- END CONTENT -->'
    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'class="th-in" href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)".+?(?:|<span><span>([^<]+)<.+?)<span class="ribbon'
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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN + sThumb
            sTitle = aEntry[2]
            sYear = aEntry[3]

            sDisplayTitle = sTitle + ' ' + sYear

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation">.*?<span>\d+</span>\s*<a href="([^"]+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
