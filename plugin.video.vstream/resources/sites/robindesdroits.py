#-*- coding: utf-8 -*-
#Kodigoal
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re 
 
SITE_IDENTIFIER = 'robindesdroits'
SITE_NAME = 'RobindesDroits'
SITE_DESC = 'Replay sports'
 
URL_MAIN = 'http://www.robindesdroits.me'
 
SPORT_SPORTS = (True, 'showGenre')
 
def load(): 
    oGui = cGui() 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/derniers-uploads/') 
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Nouveautés', 'news.png', oOutputParameterHandler)  
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Genres', 'genres.png', oOutputParameterHandler)
               
    oGui.setEndOfDirectory()

def showGenre():
    oGui = cGui()
  
    liste = []
    liste.append( ['Nouveautés', URL_MAIN + '/derniers-uploads/'] )
    liste.append( ['Football', URL_MAIN + '/football/'] )
    liste.append( ['Sports US', URL_MAIN + '/sports-us/'] )
    liste.append( ['Sports Automobiles', URL_MAIN + '/sports-automobiles/'] )
    liste.append( ['Rugby', URL_MAIN + '/rugby/'] )
    liste.append( ['Tennis', URL_MAIN + '/tennis/'] )
    liste.append( ['Autres Sports', URL_MAIN + '/autres-sports/'] )
    liste.append( ['Divers', URL_MAIN + '/divers/'] )
                 
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

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
         
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
             
            sUrl    = str(aEntry[0])
            sTitle  = str(aEntry[2])
            sThumbnail = str(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                 
                 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail,'', oOutputParameterHandler)
                
               
        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]',
                        'next.png',  oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
 
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next page-numbers" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def __showLink(url):
    
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request();

    #recup le lien clictune pour stream Watchvideo
    sPattern = '<a href="(http://www.clictune.+?)".+?<b>WatchVideo</b>'
    aResult = re.findall(sPattern,sHtmlContent)

    
    #recup le lien Watchvideo sans delai X secondes
    if (aResult):
        for aEntry in aResult:

            sUrl = aEntry
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request();
            sPattern = '<b><a href\="http\:\/\/www\.clictune\.com\/link\/redirect\/\?url\=(.+?)\&id.+?">'
            aResult = re.findall(sPattern,sHtmlContent)

            #decode url & retourne lien a showHosters
            for a in aResult:
                sUrl = cUtil().urlDecode(a)
                return sUrl
    return False

def showHosters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler() 
    sUrl = oInputParameterHandler.getValue('siteUrl') 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #recup lien Watchvideo par showLink()
    link = __showLink(sUrl)
    aResult = []
    aResult.append(link)
    
    #recup lien direct mp4
    if (aResult):
        for aEntry in aResult:
            sUrl = aEntry
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request();
            oParser = cParser()
            sPattern = '{file:"([^"]+)"\,label:"([^"]+)"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            #affichage lien mp4
            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    sHosterUrl = str(aEntry[0])
                    sQual = '[' + str(aEntry[1]) + ']'
                    sDisplayTitle = cUtil().DecoTitle(sQual + sMovieTitle)

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):

                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sDisplayTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

    oGui.setEndOfDirectory()
