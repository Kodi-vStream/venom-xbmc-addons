#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.kodigoal
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cJheberg
from resources.lib.multihost import cMultiup
from resources.lib.packer import cPacker
import re

SITE_IDENTIFIER = 'robindesdroits'
SITE_NAME = 'Robin des Droits'
SITE_DESC = 'Replay sports'

URL_MAIN = 'http://www.robindesdroits.me/'

SPORT_SPORTS = (True, 'showGenres')
SPORT_NEWS = (URL_MAIN + 'derniers-uploads/', 'showMovies')
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Genres', 'genres.png', oOutputParameterHandler)

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

    liste = []
    liste.append( ['Nouveautés', URL_MAIN + 'derniers-uploads/'] )
    liste.append( ['Football', URL_MAIN + 'football/'] )
    liste.append( ['Sports US', URL_MAIN + 'sports-us/'] )
    liste.append( ['Sports Automobiles', URL_MAIN + 'sports-automobiles/'] )
    liste.append( ['Rugby', URL_MAIN + 'rugby/'] )
    liste.append( ['Tennis', URL_MAIN + 'tennis/'] )
    liste.append( ['Autres Sports', URL_MAIN + 'autres-sports/'] )
    liste.append( ['Divers', URL_MAIN + 'divers/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class="mh-loop-thumb"><a href="([^"]+)"><img src=".+?" style="background:url\(\'(.+?)\'\).+?rel="bookmark">(.+?)</a></h3>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sUrl    = str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sTitle  = (' %s ') % (str(aEntry[2]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail,'', oOutputParameterHandler)

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
    sPattern = '<a class="next page-numbers" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #recup liens clictune
    sPattern = '<a href="(http://www.clictune.+?)".+?<b>(.+?)</b>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sDisplayTitle =  (sMovieTitle + ' [' + aEntry[1] + ']')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    oParser = cParser()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<b><a href=".+?redirect\/\?url\=(.+?)\&id.+?">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sUrl = cUtil().urlDecode(aResult[1][0])
        
        if 'gounlimited' in sUrl:
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern = '{file:"([^"]+)"\,label:"([^"]+)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                for aEntry in aResult[1]:
                    sHosterUrl = str(aEntry[0])
                    sDisplayTitle = ('[%s] %s') % (aEntry[1] + 'p', sMovieTitle)
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sDisplayTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
    
        elif 'jheberg' in sUrl:

            sUrl = sUrl.replace('captcha','mirrors')
            if not 'www.jheberg' in sUrl:
                sUrl = sUrl.replace('jheberg','www.jheberg')
            
            aResult = cJheberg().GetUrls(sUrl)
            for aEntry in aResult:
                sHosterUrl = aEntry
                
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        elif 'multiup' in sUrl:

            aResult = cMultiup().GetUrls(sUrl)
            if (aResult):
                for aEntry in aResult:
                    sHosterUrl = aEntry
                
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                    
        else:
            sHosterUrl = sUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
