# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'wilifilm'
SITE_NAME = 'Wilifilm'
SITE_DESC = 'Films'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = ('', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films-populaires', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films-box-office', 'showMovies')
MOVIE_SAGA = (URL_MAIN + 'collection-saga', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Derniers ajouts)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Nouveautés)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Populaires)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAGA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAGA[1], 'Films (Collection/Saga)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    listeGenre = [['Action', 'action'], ['Action & Adventure', 'action-adventure'], ['Animation', 'animation'],
                  ['Aventure', 'aventure'], ['Comédie', 'comedie'], ['Comedy', 'comedy'], ['Crime', 'crime'],
                  ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Drama', 'drama'],
                  ['Familial', 'familial'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
                  ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Horreur', 'horreur'], ['Horror', 'horror'],
                  ['Kids', 'kids'], ['Musique', 'musique'], ['Mystère', 'mystere'], ['Mystery', 'mystery'],
                  ['Reality', 'reality'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
                  ['Science-Fiction & Fantastique', 'science-fiction-fantastique'], ['Thriller', 'thriller'],
                  ['Soap', 'soap'], ['Talk', 'talk'], ['western', 'western'], ['War', 'war'],
                  ['War & Politics', 'war-politics']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'categories/' + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    import datetime
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(2010, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        bvalid, stoken, scookie = getTokens()
        if bvalid:
            oUtil = cUtil()
            sSearchText = oUtil.CleanName(sSearch)
            sSearch = sSearch.replace(' ', '+').replace('%20', '+')
            pdata = '_token=' + stoken + '&search=' + sSearch
            sUrl = URL_MAIN + 'search'

            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
            oRequestHandler.addHeaderEntry('Cookie', scookie)
            oRequestHandler.addParametersLine(pdata)
            sHtmlContent = oRequestHandler.request()
        else:
            oGui.addText(SITE_IDENTIFIER)
            return

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    if '/collection-saga' in sUrl:
        sPattern = 'img-fluid" data-src="([^"]+).+?result" href="([^"]+)"><h2>([^<]+)'
    else:
        sPattern = '<img class="lazyload" data-src="([^"]+).+?class="name"><a href="([^"]+)" title="[^"]+">([^<]+)'
    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent, 'title yellow', '')
    aResult = oParser.parse(sHtmlContent.replace('<br>', ''), sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sThumb = aEntry[0]
            sThumb = re.sub('/w\d+/', '/w342/', sThumb)
            # si 'no-poster.svg' dans sThumb lien invalide
            if 'no-poster.svg' in sThumb:
                continue
            sUrl = aEntry[1]
            sTitle = aEntry[2]
            if '/collection/' in sUrl:
                sTitle = re.sub(' Collection', '', sTitle)

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/collection/' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showSaga', sTitle, '', sThumb, "", oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, "", oOutputParameterHandler)

    if not sSearch:  # une seule page par recherche
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<>]+)<\/a><\/li><li class="page-item"><a class="page-link" href="([^"]+)">Next<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][1]
        sNumberMax = aResult[1][0][0]
        sNumberNext = sNextPage.split("=")[-1]
        sPaging = str(sNumberNext) + '/' + str(sNumberMax)
        return sNextPage, sPaging

    return False, 'none'


def showSaga():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    # sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    # sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sStart = '> Accueil <'
    sEnd = '<div class="col-lg-4 col-md-12">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'lazyload" data-src="([^"]+).+?href="([^"]+).+?title="[^"]+">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        
        # films des sagas dans l'ordre chronologique
        for aEntry in aResult[1][::-1]:

            sThumb = aEntry[0]
            sThumb = re.sub('/w\d+/', '/w342/', sThumb)
            sUrl = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

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
    sPattern = '<li class="part" data-url="([^"]+).+?<div class="part-name">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sDataUrl = aEntry[0]
            sHost = aEntry[1].strip()

            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, oHoster.getPluginIdentifier().capitalize())
            lien = URL_MAIN + "ll/captcha?hash=" + sDataUrl

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', lien)

            oGui.addLink(SITE_IDENTIFIER, 'showHostersLinks', sTitle, sThumb, "", oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHostersLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'src=([^ ]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)

        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def getTokens():
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN + 'accueil1')
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = 'name="_token" value="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?wilifilm_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if not aResult[0]:
        return False, 'none', 'none'

    if aResult[0]:
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; wilifilm_session=' + site_session + ';'
    return True, token, cook
