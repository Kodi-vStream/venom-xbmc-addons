#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'telecharger_streaming'
SITE_NAME = '[COLOR violet]Telecharger-streaming[/COLOR]'
SITE_DESC = 'films en streaming, Emissions en streaming'

URL_MAIN = 'https://telecharger-streaming.org/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_NEWS = (URL_MAIN + 'category/emissions-tv/', 'showMovies')
REPLAYTV_DIVERTISSEMENT = (URL_MAIN + 'category/emissions-tv/divertissements-telerealite/', 'showMovies')
REPLAYTV_INVESTIGATION = (URL_MAIN + 'category/emissions-tv/reportages-investigations/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Toutes les emissions', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_DIVERTISSEMENT[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_DIVERTISSEMENT[1], 'Emissions de Divertissements/Téléréalité', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_INVESTIGATION[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_INVESTIGATION[1], 'Emissions de Reportages/Investigations', 'tv.png', oOutputParameterHandler)

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

    if sSearch:
        sPattern = '<h1 class="title"><a href="([^"]+)" title="([^"]+)">.+?<p>.+?Synopsis :([^"]+)</p>'
    else:
        sPattern = '<h1 class="title"><a href="([^"]+)" title="([^"]+)".+?<img class="alignleft".+?src="([^"]+)".+?Synopsis :(.+?)<\/p>'

    oParser = cParser()
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

            if sSearch:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]
                sThumb = ""
                sDesc = aEntry[2].replace('</strong>', '')
            else:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]
                sThumb = aEntry[2]
                sDesc = aEntry[3].replace('</strong>', '')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next" href="([^"]+)"'
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
    sHtmlContent = GetAllLink(oRequestHandler.request())

    oParser = cParser()
    sPattern = '<span style="color: #ff00ff;">([^<]+?)</span>|<a href="([^"]+)"'

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

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sHosterUrl = aEntry[1]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def GetAllLink(sHtmlContent):
    oParser = cParser()
    sPattern = '<p><span id="more-.+?"></span></p>(.+?)(?:<p><strong><span style="color: #00ffff;">|<h3><strong>)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''
