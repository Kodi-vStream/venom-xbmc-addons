# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

SITE_IDENTIFIER = 'fullmatchtv'
SITE_NAME = 'Fullmatchtv'
SITE_DESC = 'Sports Replay'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

#SPORT_SPORTS = (True, 'load')
SPORT_REPLAY = (True, 'load')
REPLAYTV_REPLAYTV = (True, 'load')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

MOVIE_AFL = (URL_MAIN + 'afl/', 'showMovies')
MOVIE_MOTOR = (URL_MAIN + 'motorsports/', 'showMovies')
MOVIE_NBA = (URL_MAIN + 'nba/', 'showMovies')
MOVIE_NFL = (URL_MAIN + 'nfl/', 'showMovies')
MOVIE_NHL = (URL_MAIN + 'nhl/', 'showMovies')
MOVIE_MLB = (URL_MAIN + 'mlb/', 'showMovies')
MOVIE_RUGBY = (URL_MAIN + 'rugby/', 'showMovies')
MOVIE_MMA = (URL_MAIN + 'wwe-mma/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AFL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_AFL[1], 'AFL', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOTOR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOTOR[1], 'MOTORSPORT', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NBA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NBA[1], 'NBA', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NFL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NFL[1], 'NFL', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NHL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NHL[1], 'NHL', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MLB[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MLB[1], 'MLB', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_RUGBY[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_RUGBY[1], 'RUGBY', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MMA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MMA[1], 'WWE-MMA', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
        sPattern = '(?:<div class="td_module_16 td_module_wrap td-animation-stack">|<div class="td-module-container td-category-pos-image">.+?<div class="td-module-thumb">).+?href="([^"]+).+?title="([^"]+).+?.+?(?:src="([^"]+)|url.+?([^\']+))'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = '(?:<div class="td_module_mx7 td_module_wrap td-animation-stack">|<div class="td-module-container td-category-pos-image">.+?<div class="td-module-thumb">).+?href="([^"]+).+?title="([^"]+).+?.+?(?:src="([^"]+)|url.+?([^\']+))'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

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
            sThumb = aEntry[2]
            sTitle = aEntry[1]
            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = '<div class="td-post-content tagdiv-type">'
    sEnd = '<div class="td-post-source-tags">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'Part (\d).+?<iframe.+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'https:' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        if not aResult[0]:
            oGui.addText(SITE_IDENTIFIER)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                sPartie = aEntry[0]
                sHosterUrl = aEntry[1]
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'https:' + sHosterUrl
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle + ' Partie' + sPartie)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
