#-*- coding: utf-8 -*-
#Venom.
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import xbmc
import re
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'zone_telechargement_eu'
SITE_NAME = '[COLOR violet]Zone-Telechargement.ru (Kodi V17)[/COLOR]'
SITE_DESC = 'Films en DDL et streaming'

URL_MAIN = 'https://www.zone-telechargement.ru/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'trending/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Tendances', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'ratings/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Evaluations', 'films_comments.png', oOutputParameterHandler)

    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Genres', 'films_genres.png', oOutputParameterHandler)

    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Année de sortie', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item.+?<a href="(.+?)">(.+?)</a>.+?</li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    liste = []
    if aResult[0]:
        for aEntry in aResult[1]:
            liste.append([aEntry[1], aEntry[0]])

    for sTitle,sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<a href="(https://www.zone-telechargement.ru/release/(\d+?)/)">.+?</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    liste = []
    if aResult[0]:
        for aEntry in aResult[1]:
            liste.append([aEntry[1], aEntry[0]])

    for sTitle,sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'searchtmdb.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = '', page = 1):
    oGui = cGui()
    bGlobal_Search = False

    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    if URL_SEARCH[0] in sSearch:
        bGlobal_Search = True

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')

    sPattern = '<article.+?<img src="(.+?)".+?<a href="(.+?)">(.+?)</a>.+?</article>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sTitle = aEntry[2]
            sUrl = aEntry[1]
            sThumbnail = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            result = re.search('ru/series', sUrl)
            if result:
                oGui.addMovie(SITE_IDENTIFIER, 'showSeriesHosters', sTitle, '', sThumbnail, sUrl, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sUrl, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+?)"><span class="icon-chevron-right'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<li>.+?<a href="(.+?)".+?<img src="(.+?)".+?<div class="numerando">(.+?)</div>.+?<a href=".+?">(.+?)</a>.+?</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sNumber = aEntry[2]
            parts = sNumber.split('-')
            if len(parts) == 2:
                sNumber = 'S%02dE%02d' % (int(parts[0]), int(parts[1]))
            sTitle = aEntry[3]
            sDisplayTitle = '[COLOR yellow][' + sNumber + '][/COLOR] ' + sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            title = sMovieTitle + ' [' + sNumber + '] ' + sTitle
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', title)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sUrl, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<tr id=.+?<td><a .+?href="(.+?)".+?</td>.*?<td><img.+?>(.+?)</td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.+?</tr>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]' + sMovieTitle + '[/COLOR]')

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sHoster = aEntry[1]
            sType = aEntry[2]
            sLang = aEntry[3]
            sSize = aEntry[4]

            sDisplayTitle = '[COLOR teal][' + sType + '][' + sLang + '][' + sSize + '] ' + sHoster + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'decodeLink', sDisplayTitle, '', '', '', oOutputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER,'[COLOR red]Pas de liens disponibles[/COLOR]')
            
    oGui.setEndOfDirectory()

def decodeLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = 'window.location.href=\'(.+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
