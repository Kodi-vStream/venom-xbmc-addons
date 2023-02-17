# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
return False  # Sous Cloudflare 14/10/2021

import re
import xbmc

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'enstream'
SITE_NAME = 'Enstream'
SITE_DESC = 'Regarder tous vos films streaming complets, gratuit et illimité'

URL_MAIN = "https://www.enstream.club/"

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = ('', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_LIST = (True, 'showAlpha')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Comédie Dramatique', 'comedie-dramatique'],
             ['Comédie Musicale', 'comedie-musical'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Guerre', 'guerre'],
             ['Historique', 'historique'], ['Judiciaire', 'judiciaire'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1942, 2023)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'Annee/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()

    liste = [['0-9', ''], ['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D'], ['E', 'E'], ['F', 'F'], ['G', 'G'],
             ['H', 'H'], ['I', 'I'], ['J', 'J'], ['K', 'K'], ['L', 'L'], ['M', 'M'], ['N', 'N'], ['O', 'O'],
             ['P', 'P'], ['Q', 'Q'], ['R', 'R'], ['S', 'S'], ['T', 'T'], ['U', 'U'], ['V', 'V'], ['W', 'W'],
             ['X', 'X'], ['Y', 'Y'], ['Z', 'Z']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'ABC/' + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = URL_MAIN + 'search.php'
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('q', Unquote(sSearch))
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)

    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    if sSearch:
        sPattern = '<a href="([^"]+).+?url\((.+?)\).+?<div class="title"> (.+?) </div>'
    elif 'Annee/' in sUrl or '/ABC' in sUrl:
        sPattern = '<div class="table-movies-content.+?href="([^"]+).+?url\((.+?)\).+?<.i>.([^<]+)'
    elif 'genre/' in sUrl:
        sPattern = 'film-uno.+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+)'
    else:
        sPattern = 'class="film-uno".+?href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+).+?min.+?·([^<]+).+?short-story">([^<]*)'

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

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sDesc = ''
            if len(aEntry) > 3:
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sQual = aEntry[3].split('·')[1].replace('Â', '').strip()
                    sLang = aEntry[3].split('·')[2].strip()
                else:
                    sQual = aEntry[3].split('·')[1].strip()
                    sLang = aEntry[3].split('·')[2].strip()

                sDesc = aEntry[4]

                sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            else:
                sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            # sNumPage = re.search('(page|genre).*?[-=\/]([0-9]+)', sNextPage).group(2)  # ou replace'.html',''; '([0-9]+)$'
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class=\'Paginaactual\'.+?a href=\'([^"]+?)\'.+?>([^<]+)</a></li></ul'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('(page|genre).*?[-=\/]([0-9]+)', sNextPage).group(2)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    sPattern = '<span>\d+</span>.+?href=\'([^"]+?)\'.+?>([^<]+)</a></li></ul'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('(page|genre).*?[-=\/]([0-9]+)', sNextPage).group(2)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-url="([^"]+)".+?data-code="([^"]+)".+?mobile">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sDataUrl = aEntry[0]
            sDataCode = aEntry[1]
            sHost = aEntry[2].capitalize()

            # filtrage des hosters
            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            lien = URL_MAIN + 'video/' + sDataCode + '/recaptcha/' + sDataUrl

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', lien)
            oOutputParameterHandler.addParameter('referer', sUrl)

            oGui.addLink(SITE_IDENTIFIER, 'showHostersLinks', sTitle, sThumb, sDesc, oOutputParameterHandler)

    sPattern = "class=.download.+?href='/([^']*).+?mobile.>([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            lien = URL_MAIN + aEntry[0]
            sHost = aEntry[1].capitalize()
            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', lien)
            oOutputParameterHandler.addParameter('referer', sUrl)

            oGui.addLink(SITE_IDENTIFIER, 'showHostersLinks', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHostersLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', referer)

    oRequestHandler.request()
    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = cHosterGui().checkHoster(sHosterUrl)

    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
