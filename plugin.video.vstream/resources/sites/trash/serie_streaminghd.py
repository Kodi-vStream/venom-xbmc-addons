# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

return False  # 13/02/21 WAAW en hoster

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress


SITE_IDENTIFIER = 'serie_streaminghd'
SITE_NAME = 'Série-StreamingHD'
SITE_DESC = 'Séries en streaming vf, vostfr'

URL_MAIN = "https://planet-serie.com/"

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_TOP = (URL_MAIN + 'top-serie/', 'showSeries')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showSeries')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TOP[1], 'Séries (Populaire)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSeries(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'fullstreaming"><img src="([^"]+).+?alt="([^"]+).+?xqualitytaftaf"><strong>([^<]+).+?href="([^"]+)" *>([^<]+)'
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

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb

            sTitle = aEntry[1]
            saison = aEntry[2]
            siteUrl = aEntry[3]
            sLang = aEntry[4]

            if '{title}' in sTitle:
                sTitle = sLang
                sLang = ''
            elif 'VF - VOSTFR' in sLang:
                sLang = 'VF/VOSTFR'
            elif 'VF' in sLang:
                sLang = 'VF'
            elif 'VOSTFR' in sLang:
                sLang = 'VOSTFR'

            sDisplayTitle = ('%s %s (%s)') % (sTitle, saison, sLang)

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a>  <a href="([^"]+)">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
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

    oParser = cParser()

    # Liens VF
    sHtmlTab = oParser.abParse(sHtmlContent, '<div class="VF-tab">', '<div id="fsElementsContainer">')
    if sHtmlTab:
        sPattern = '<a href="([^"]+)".+?</i> Episode *([0-9]+)'
        aResult = oParser.parse(sHtmlTab, sPattern)

        if aResult[0]:
            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VF[/COLOR]')

            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + ' Episode ' + aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # Liens VOSTFR
    sHtmlTab = oParser.abParse(sHtmlContent, '<div class="VOSTFR-tab">', '<div class="VF-tab">')
    if sHtmlTab:

        sPattern = '<a href="([^"]+)".+?</i> Ep *([0-9]+)'
        aResult = oParser.parse(sHtmlTab, sPattern)

        if aResult[0]:
            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VOSTFR[/COLOR]')

            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + ' Episode ' + aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
