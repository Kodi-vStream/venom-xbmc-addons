# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import unicodedata
import requests
import xbmc

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, siteManager
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'buzzmonclick_com'
SITE_NAME = 'BuzzMonClick'
SITE_DESC = 'Films & Séries en Streaming de qualité entièrement gratuit.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

DOC_DOCS = ('http://', 'load')
DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')

URL_SEARCH = ('https://buzzmonclick.net/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay TV', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'divertissement/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Divertissement', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'infos-magazine/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Infos/Magazines', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'tele-realite/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Télé-Réalité', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Documentaires', 'documentaires'], ['Divertissement', 'divertissement'],
             ['Infos/Magazines', 'infos-magazine'], ['Télé-Réalité', 'tele-realite']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
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

    sPattern = '<div id="post-[0-9]+".+?<a class="clip-link.+?title="([^"]+)" href="([^"]+).+?img src="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            try:
                sTitle = unicode(aEntry[0], 'utf-8')  # converti en unicode
                sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')  # vire accent
                # sTitle = unescape(str(sTitle))
                sTitle = sTitle.encode("utf-8")
            except NameError:
                sTitle = aEntry[0]

            # mise en page
            sTitle = sTitle.replace('Permalien pour', '').replace('&prime;', '\'')
            sTitle = re.sub('(?:,)* (?:Replay |Video )*du ([0-9]+ [a-zA-z]+ [0-9]+)', ' (\\1)', sTitle)
            sTitle = re.sub(', (?:Replay|Video)$', '', sTitle)
            sUrl = aEntry[1]
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, 'doc.png', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'class="nextpostslink" rel="next" href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return aResult[1][0]

    return False


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'wp-block-button.+?(?:href=|src=)"([^"]+)".+?>(?:([^<]+)|)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sHost = aEntry[1]
            if sHost == "":
                sHost = aEntry[0].split('/')[2].split('.')[0]

            sUrl = aEntry[0]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'forum-tv' in sUrl:
        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        s = requests.Session()

        response = s.get(sUrl, headers={'User-Agent': UA})
        sHtmlContent = str(response.content)
        cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in s.cookies.items()])

        oParser = cParser()
        sPattern = '<input type="hidden".+?value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            data = "_method=" + aResult[1][0] + "&_csrfToken=" + aResult[1][1] + "&ad_form_data=" + Quote(aResult[1][2])
            data += "&_Token%5Bfields%5D=" + Quote(aResult[1][3]) + "&_Token%5Bunlocked%5D=" + Quote(aResult[1][4])
            # Obligatoire pour validé les cookies.
            xbmc.sleep(6000)
            oRequestHandler = cRequestHandler('https://forum-tv.org/adslinkme/links/go')
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Length', len(data))
            oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded; charset=UTF-8")
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Cookie', cookie_string)
            oRequestHandler.addParametersLine(data)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'url":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
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


