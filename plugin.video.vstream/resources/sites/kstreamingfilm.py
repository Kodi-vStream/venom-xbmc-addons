# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'kstreamingfilm'
SITE_NAME = 'K Streaming Film'
SITE_DESC = 'Films en streaming français sur internet.'

URL_MAIN = 'https://kstreamingfilm.com/'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'action/'])
    liste.append(['Afro', URL_MAIN + 'afro/'])
    liste.append(['Animation', URL_MAIN + 'animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'art-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'aventure/'])
    liste.append(['Biographique', URL_MAIN + 'biographique/'])
    liste.append(['Biopic', URL_MAIN + 'biopic/'])
    liste.append(['Comédie', URL_MAIN + 'comedie/'])
    liste.append(['Comédie dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Comédie musicale', URL_MAIN + 'comedie-musicale/'])
    liste.append(['Crime', URL_MAIN + 'crime/'])
    liste.append(['Divers', URL_MAIN + 'divers/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire/'])
    liste.append(['Drame', URL_MAIN + 'drame/'])
    liste.append(['Epouvante-horreur', URL_MAIN + 'epouvante-horreur/'])
    liste.append(['Erotique', URL_MAIN + 'erotique/'])
    liste.append(['Espionnage', URL_MAIN + 'espionnage/'])
    liste.append(['Famille', URL_MAIN + 'famille/'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique/'])
    liste.append(['Film-musical', URL_MAIN + 'film-musical/'])
    liste.append(['Guerre', URL_MAIN + 'guerre/'])
    liste.append(['Historique', URL_MAIN + 'historique/'])
    liste.append(['Horreur', URL_MAIN + 'horreur/'])
    liste.append(['Judiciaire', URL_MAIN + 'judiciaire/'])
    liste.append(['Musical', URL_MAIN + 'musical/'])
    liste.append(['Mystère', URL_MAIN + 'mystere/'])
    liste.append(['Non classé', URL_MAIN + 'non-classe/'])
    liste.append(['Policier', URL_MAIN + 'policier/'])
    liste.append(['Romance', URL_MAIN + 'romance/'])
    liste.append(['Science fiction', URL_MAIN + 'science-fiction/'])
    liste.append(['Slasher', URL_MAIN + 'slasher/'])
    liste.append(['Sport', URL_MAIN + 'sport-event/'])
    liste.append(['Terreur', URL_MAIN + 'thriller/terreur/'])
    liste.append(['Thriller', URL_MAIN + 'thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

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
    oParser = cParser()

    if 'Derniers films ajoutés' in sHtmlContent:
        sStart = 'Derniers films ajoutés'
        sEnd = 'Film streaming les plus populaires'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+).+?movie-release">([^<]*).+?(?:|story\'>([^<]+).+?)movie-cast'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sTitle = aEntry[1]
            sUrl = aEntry[2]
            sYear = aEntry[3]
            sDesc = aEntry[4]
            sDisplayTitle = sTitle + '(' + sYear + ')'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a></div><div class="naviright"><a href="([^"]+?)" >Suivant'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        list_hoster = []
        for aEntry in aResult[1]:

            sHosterUrl = aEntry.strip()
            if sHosterUrl not in list_hoster:
                list_hoster.append(sHosterUrl)
            else:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
