#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Razorex.TmpName
#voir redirection vers regarder film et episode avec ex: 2 x 1 au lieu de 2 - 1
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import re

SITE_IDENTIFIER = 'streamzzz_com'
SITE_NAME = 'Streamzzz'
SITE_DESC = 'Séries VF & VOSTFR en streaming.'

URL_MAIN = 'http://streamzzz.top/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'movies/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'movies/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'trending/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'ratings/', 'showMovies')
SERIE_LIST = (URL_MAIN + 'series-list/', 'showAlpha')
SERIE_GENRES = (True, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'series_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux notés)', 'series_notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'series_az.png', oOutputParameterHandler)


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

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
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item cat-item.+?"><a href="([^<]+)" *>([^<]+)</a>.+?<i>([^<]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[1] + ' (' + (aEntry[2]) + ')'
            sUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(SERIE_LIST[0])
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span style="color: red;">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sLetter = str(aEntry).replace('=', '')
            dAZ = str(aEntry)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('dAZ', dAZ)
            oGui.addDir(SITE_IDENTIFIER, 'showList', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'series_az.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showList():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    dAZ = oInputParameterHandler.getValue('dAZ')
    oRequestHandler = cRequestHandler(SERIE_LIST[0])
    sHtmlContent = oRequestHandler.request()

    #Decoupage pour cibler une partie Film
    sPattern = '<span style="color: red;">' + dAZ + '<(.+?)<(span style="color: red;">|/tbody>)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #regex pour listage films sur la partie decoupée
    sPattern = '<a href="([^<]+)" *target="_blank">(.+?)<\/a>'
    aResult = oParser.parse(aResult, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = str(aEntry[1]).decode("unicode_escape").encode("latin-1")#.replace('&#8217;', '\'').replace('&#8212;', '-')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showSerieSaisons', sTitle, 'series_az.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
        sPattern = '<div class="result-item">.+?<img src="([^"]+)" alt="(.+?)".+?<a href="([^"]+)">'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = '<div class="poster".+?img src="([^"]+)" alt="(.+?)".+?<a href="([^"]+)">'


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sThumb = str(aEntry[0])
            sTitle = str(aEntry[1]).replace(':', '')
            sUrl2 = str(aEntry[2])
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )

            if '/episodes/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/movies/' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sPattern = '<span class="current">.+?</span><a href=\'(.+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSerieSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="numerando">(.+?)<\/div>.+?<a href="([^<]+)">(.+?)<\/a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl2 = str(aEntry[1])
        #a voir
            if 'x' in aEntry[0]:
                sSXXEXX = str(aEntry[0]).replace(' ', '').split('x')
            else:
                sSXXEXX = str(aEntry[0]).replace(' ', '').split('-')

            sTitle = "saison " + sSXXEXX[0]  + 'episode' + sSXXEXX[1] + ' ' + str(aEntry[2])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )

            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    oParser = cParser()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "domain=(.+?)\".+?document.getElementsByName\(\'iframe\'\).+?src\'.+?\'(.+?)\'\);.+?<\/td><td>(.+?)<\/td>"

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHost = str(aEntry[0]).replace('.com', '').replace('.co', '').replace('.tv', '').replace('.sx', '').replace('.org', '').replace('.ch', '')
            if 'nowvideo' in sHost or 'youvid' in sHost:
                continue
            sHost = sHost.capitalize()
            sUrl2 = str(aEntry[1])
            sLang = str(aEntry[2])

            sTitle = sMovieTitle + ' (' + sLang + ')' + ' (' + sHost + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHosterUrl = oRequestHandler.getRealUrl()

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
