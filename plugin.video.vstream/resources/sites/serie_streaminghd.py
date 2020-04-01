#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
#from resources.lib.util import cUtil


SITE_IDENTIFIER = 'serie_streaminghd'
SITE_NAME = 'Série-StreamingHD'
SITE_DESC = 'Séries en streaming vf, vostfr'

URL_MAIN = 'https://www.serie-streaminghd.org/'

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = (URL_MAIN, 'showMovies')
SERIE_HD = (URL_MAIN + 'saison-complete/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'regarder-series/vf-hd/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'regarder-series/vostfr-hd/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

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
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<div class="fullstream fullstreaming"><img src="([^"]+)".+?alt="([^"]+)".+?<h3 class="mov-title"><a href="([^"]+)'

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

            sTitle = aEntry[1]
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
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^<>"]+)">Suivant &#8594;<\/a>'
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

    #On separe liens vostfr - vf
    sPattern = '<div class="VOSTFR-tab">(.+?)<div class="VF-tab">'
    sPattern2 ='<div class="VF-tab">(.+?)<div id="fsElementsContainer">'

    aResult = oParser.parse(sHtmlContent, sPattern)
    aResult2 = oParser.parse(sHtmlContent, sPattern2)

    #pour total3 si pas liens vostfr
    total = 0

    #Liens VOSTFR
    if (aResult[0] == True):

        sPattern = '<a href="([^"]+)".+?<\/i> EPS ([0-9]+)'
        aResult = oParser.parse(aResult[1][0], sPattern)

        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)

            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VOSTFR[/COLOR]')

            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                sHosterUrl = aEntry[0]
                sMovieTitle2 = sMovieTitle + 'episode ' + aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    #Liens VF
    if (aResult2[0] == True):

        sPattern = '<a href="([^"]+)".+?<\/i> EPS ([0-9]+)'
        aResult = oParser.parse(aResult2[1][0], sPattern)

        if (aResult[0] == True):
                total2 = len(aResult[1])
                #update total dialog si liens vostfr puis vf
                total3 = total + total2
                progress_ = progress().VScreate(SITE_NAME)

                oGui.addText(SITE_IDENTIFIER, '[COLOR red]Langue VF[/COLOR]')

                for aEntry in aResult[1]:
                    progress_.VSupdate(progress_, total3)
                    if progress_.iscanceled():
                        break

                    sHosterUrl = aEntry[0]
                    sMovieTitle2 = sMovieTitle + 'episode ' + aEntry[1]

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle2)
                        oHoster.setFileName(sMovieTitle2)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
