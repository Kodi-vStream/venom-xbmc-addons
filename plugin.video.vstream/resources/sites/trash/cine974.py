# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import progress, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'cine974'
SITE_NAME = 'Ciné 974'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'streaming/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'src="([^"]+)" alt="([^"]+)" class="sc.+?synop">([^<]*).+?href="([^"]+)">Regarder'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
        oGui.setEndOfDirectory()
        return

    total = len(aResult[1])
    progress_ = progress().VScreate(SITE_NAME)
    oOutputParameterHandler = cOutputParameterHandler()
    for aEntry in aResult[1]:
        progress_.VSupdate(progress_, total)
        if progress_.iscanceled():
            break

        sThumb = aEntry[0]
        if sThumb.startswith('/'):
            sThumb = URL_MAIN[:-1] + sThumb
        sTitle = aEntry[1]
        sDesc = aEntry[2]
        sUrl2 = aEntry[3]
        if sUrl2.startswith('/'):
            sUrl2 = URL_MAIN[:-1] + sUrl2

        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)

        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    progress_.VSclose(progress_)

    sNextPage, sPaging = __checkForNextPage(sHtmlContent)
    if sNextPage != False:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>(\d+)</a></li><li><a href="([^"]+)"><i class="fa fa-angle-right'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('p=([0-9]+)', aResult[1][0][1]).group(1)
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
    sPattern = '<iframe width="100%" height="400" src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        for aEntry in aResult[1]:

            link = re.sub('.+?embed/', '', aEntry)
            link = link.replace('?rel=0', '')
            sHosterUrl = 'https://www.youtube.com/watch?v=' + link

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
