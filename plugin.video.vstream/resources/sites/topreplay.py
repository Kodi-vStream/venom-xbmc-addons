# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# plus vraiment le meme site
import re
import requests
import xbmc

from resources.lib.comaddon import dialog, progress, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'topreplay'
SITE_NAME = 'TopReplay'
SITE_DESC = 'Replay TV'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_GENRES = (True, 'showGenres')
REPLAYTV_TVSHOWS = (True, 'showTvShows')
REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Nouveautés', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Genres', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_TVSHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_TVSHOWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = 'main-menu'
    sEnd = '/ul'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            if 'Accueil' in sTitle: continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTvShows():
    oGui = cGui()
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = 'ÉMISSIONS TV'
    sEnd = '</div></div> </aside>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1]
            if 'Contactez' in sTitle:
                continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'replay.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<article.+?href="([^"]+)">([^<]+).+?img.+?src="([^"]+).+?<div class="entry"><p>(.+?)Vous pouvez toujours regarder'#&hellip'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            sDesc = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, 'replay.png', sThumb, sDesc, oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'title>TopReplay - Page [\d+] sur (\d+).+?href="([^"]+)"\s*>Chargez plus'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    # premiere page
    sPattern = 'href="([^"]+)"\s*>Chargez plus'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="myButton" href="([^<]+)" target="_blank"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for sHosterUrl in aResult[1]:
            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sMovieTitle, 'replay.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'mon-tele' in sUrl:
        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        s = requests.Session()

        response = s.get(sUrl, headers={'User-Agent': UA})
        sHtmlContent = str(response.content)
        cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in s.cookies.items()])

        oParser = cParser()
        sPattern = '<input type="hidden".+?value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        from resources.lib import librecaptcha
        test = librecaptcha.get_token(
            api_key="6LezIsIZAAAAABMSqc7opxGc3xyCuXtAtV4VlTtN",
            site_url="https://mon-tele.com/",
            user_agent=UA,
            gui=False,
            debug=False
        )

        if aResult[0]:
            data = "_method=" + aResult[1][0] + "&_csrfToken=" + aResult[1][1] + "&ref=&f_n=" + aResult[1][2]\
                              + "&g-recaptcha-response=" + test + "&_Token%5Bfields%5D=" + Quote(aResult[1][3])\
                              + "&_Token%5Bunlocked%5D=" + Quote(aResult[1][4])

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Length', len(data))
            oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
            oRequestHandler.addHeaderEntry('Cookie', cookie_string)
            oRequestHandler.addParametersLine(data)
            sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = '<input type="hidden".+?value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            data = "_method=" + aResult[1][0] + "&_csrfToken=" + aResult[1][1] + "&ad_form_data="\
                              + Quote(aResult[1][2]) + "&_Token%5Bfields%5D=" + Quote(aResult[1][3])\
                              + "&_Token%5Bunlocked%5D=" + Quote(aResult[1][4])

            # Obligatoire pour validé les cookies.
            xbmc.sleep(15000)
            oRequestHandler = cRequestHandler('https://mon-tele.com/obtenirliens/links/go')
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Length', len(data))
            oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded; charset=UTF-8")
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Cookie', cookie_string)
            oRequestHandler.addParametersLine(data)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'url":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        sHosterUrl = sUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster != False:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
