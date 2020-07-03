# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

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

URL_MAIN = 'https://www.streaminghd-serie.com/'

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_HD = (URL_MAIN + 'saison-complete/', 'showSeries')
SERIE_VFS = (URL_MAIN + 'regarder-series/vf-hd/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'regarder-series/vostfr-hd/', 'showSeries')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Séries (Saisons Complète)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
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
    sPattern = 'fullstream fullstreaming"><img src="([^"]+)".+?alt="([^"]+)".+?class="mov-title"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = re.sub('- Saison', 'Saison', aEntry[1])
            siteUrl = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^"]+)">Suivant &#8594;'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    # On separe liens vostfr - vf
    sPattern = '<div class="VOSTFR-tab">(.+?)<div class="VF-tab">'
    sPattern2 = '<div class="VF-tab">(.+?)<div id="fsElementsContainer">'

    aResult = oParser.parse(sHtmlContent, sPattern)
    aResult2 = oParser.parse(sHtmlContent, sPattern2)

    # Liens VOSTFR
    if (aResult[0] == True):

        sPattern = '<a href="([^"]+)".+?</i> EPS ([0-9]+)'
        aResult = oParser.parse(aResult[1][0], sPattern)

        if (aResult[0] == True):

            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VOSTFR[/COLOR]')

            for aEntry in aResult[1]:

                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + 'episode ' + aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # Liens VF
    if (aResult2[0] == True):

        sPattern = '<a href="([^"]+)".+?</i> EPS ([0-9]+)'
        aResult = oParser.parse(aResult2[1][0], sPattern)

        if (aResult[0] == True):

            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VF[/COLOR]')

            for aEntry in aResult[1]:

                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + 'episode ' + aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
