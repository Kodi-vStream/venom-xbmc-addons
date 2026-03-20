# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
import time

SITE_IDENTIFIER = 'witv'
SITE_NAME = 'witv'
SITE_DESC = 'Chaines TV en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


SPORT_SPORTS = (True, 'load')
SPORT_TV = ('chaines-live/sport/', 'showTV')
# TV_DOCS = ('chaines-live/documentaire/', 'showTV')

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines sportives', 'tv.png', oOutputParameterHandler)
    # oOutputParameterHandler.addParameter('siteUrl', TV_DOCS[0])
    # oGui.addDir(SITE_IDENTIFIER, TV_DOCS[1], 'Documentaires', 'tv.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    siteUrl = URL_MAIN + siteUrl
    oRequestHandler = cRequestHandler(siteUrl)
    sHtmlContent = oRequestHandler.request()
    
    # url title thumb
    sPattern = 'Live<\/span>    <a href="([^"]+).+?class="ann-short_price">([^<]+).+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    oOutputParameterHandler = cOutputParameterHandler()
    if aResult[0]:

        # on ajoute canal+ dans les chaines sportives
        if SPORT_TV[0] in siteUrl:
            aResult[1].append(['chaines-live/23-canal.html', 'CANAL +', 'images/logo/canal-plus-logo.png'])
        
        result = sorted(aResult[1], key = lambda chaine : chaine[1])
        for aEntry in result:
            sUrl = aEntry[0]
            sTitle = aEntry[1].split('-')[0].strip()
            sThumb = URL_MAIN + aEntry[2]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showLink', sTitle, sThumb, sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oParser = cParser()
    oHosterGui = cHosterGui()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, '<iframe src="([^"]+)')

    if aResult[0]:
        sHosterUrl = aResult[1][0]
        if 'http' not in sHosterUrl:
            sHosterUrl = URL_MAIN[0:-1] + sHosterUrl
        
        oRequestHandler = cRequestHandler(sHosterUrl)
        sHtmlContent = oRequestHandler.request()
        aResult = oParser.parse(sHtmlContent, 'streamUrl = "([^"]+)')
        if aResult[0]:
            sHosterUrl = aResult[1][0]

            # redirection de lien
            oRequestHandler = cRequestHandler(sHosterUrl)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            sHtmlContent = oRequestHandler.request()
            sHosterUrl2 = oRequestHandler.getRealUrl()
            
            # 2eme tentative
            if sHosterUrl2 == sHosterUrl:
                time.sleep(2)
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                sHtmlContent = oRequestHandler.request()
                sHosterUrl2 = oRequestHandler.getRealUrl()
    
                # 3eme tentative
                if sHosterUrl2 == sHosterUrl:
                    time.sleep(2)
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                    sHtmlContent = oRequestHandler.request()
                    sHosterUrl2 = oRequestHandler.getRealUrl()
    
            if sHosterUrl2 != sHosterUrl:
                oHoster = oHosterGui.getHoster('lien_direct')
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)
    
    oGui.setEndOfDirectory()

