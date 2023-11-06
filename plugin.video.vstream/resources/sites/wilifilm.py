# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import siteManager, VSlog
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

MOVIE_MOVIE = (URL_MAIN + 'films-streaming', 'showMovies')
MOVIE_BOX = (URL_MAIN + 'films-box-office', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Derniers ajouts)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BOX[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BOX[1], 'Films (Populaires)', 'star.png', oOutputParameterHandler)

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

    liste = []
    listegenre = ['action', 'animation', 'aventure', 'biopic', 'comedie', 'drame', 'documentaire', 'epouvante-horreur',
                  'espionnage', 'famille', 'fantastique', 'guerre', 'historique', 'policier', 'romance',
                  'science-fiction', 'thriller', 'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + "categories/" + igenre])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(2010, 2023)):
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
        
    sPattern = '<img class="lazyload" data-src="([^"]+)".+?<div class="movie-details existing-details"><div class="name"><a href="([^"]+)" title="[^"]+">([^<>]+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[1]
            sTitle = aEntry[2]
            sThumb = aEntry[0]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

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

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<li class="part" data-url="([^"]+)">.+?<div class="part-name">([^<>]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sDataUrl = aEntry[0]
            sHost = aEntry[1].capitalize().strip()

            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, oHoster.getPluginIdentifier())
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
    sPattern = 'src="([^"]+)'
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
