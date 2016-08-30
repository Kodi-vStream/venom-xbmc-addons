#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import re, json

SITE_IDENTIFIER = 'youtube_fr'
SITE_NAME = 'Youtube.fr'
SITE_DESC = 'Youtube'

URL_MAIN = 'http://www.youtube.fr/'
#DOC_DOCS = 'http://www.docspot.fr/?cat=0'

#URL_SEARCH = 'http://www.docspot.fr/?s='
#FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS)
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0&orderby=views')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires Les plus vues', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0&orderby=comments')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires Les plus commentés', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0&orderby=likes')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires Les mieux notés', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://frenchstream.org/les-plus-vues')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Documentaires Genres', 'genres.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://gdata.youtube.com/feeds/api/videos?q='+sSearchText+'.&orderby=relevance&start-index=1&max-results=20&v=2&alt=json'  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["90° enquêtes","http://www.docspot.fr/?cat=15"] )
    liste.append( ["Arte","http://www.docspot.fr/?cat=2"] )
    liste.append( ["C'est pas sorcier","http://www.docspot.fr/?cat=3"] )
    liste.append( ["Education","http://www.docspot.fr/?cat=4"] )
    liste.append( ["Faites entrer l'accusé","http://www.docspot.fr/?cat=14"] )
    liste.append( ["Histoire","http://www.docspot.fr/?cat=7"] )
    liste.append( ["L'hombre d'un doute","http://www.docspot.fr/?cat=42"] )
    liste.append( ["L'univers et ses mystères","http://www.docspot.fr/?cat=44"] )
    liste.append( ["Nature & Animaux","http://www.docspot.fr/?cat=8"] )
    liste.append( ["Politique & Société","http://www.docspot.fr/?cat=12"] )
    liste.append( ["Question à la Une","http://www.docspot.fr/?cat=17"] )
    liste.append( ["Reportages","http://www.docspot.fr/?cat=9"] )
    liste.append( ["Sciences","http://www.docspot.fr/?cat=11"] )
    liste.append( ["Sciences Humaines","http://www.docspot.fr/?cat=13"] )
    liste.append( ["Technologies","http://www.docspot.fr/?cat=1"] )
    liste.append( ["Univers","http://www.docspot.fr/?cat=5"] )
    
                
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
    sHtmlContent = oRequestHandler.request();
    Result = json.loads(sHtmlContent)


    if (len(Result) > 0):
        total = len(Result)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in Result['feed']['entry']:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #print aEntry['title']['$t'].encode("utf-8")
            #print aEntry['link'][0]['href']
            #print aEntry['author'][0]['name']['$t']
            #sUrl = aEntry['media$group']['media$player']['url']
            sTitle =  aEntry['media$group']['media$title']['$t'].encode("utf-8")
            sThumb =  aEntry['media$group']['media$thumbnail'][1]['url']
            sAutor =  aEntry['media$group']['media$credit'][0]['$t']
            sDesc =  aEntry['media$group']['media$description']['$t'].encode("utf-8")

            sId = aEntry['media$group']['yt$videoid']['$t']

            sUrl = 'www.youtube.com/embed/'+sId


            oHoster = cHosterGui().checkHoster(sUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

            #oOutputParameterHandler = cOutputParameterHandler()
            #oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            #oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            #oOutputParameterHandler.addParameter('sThumbnail', str(sThumb))
            #oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='(.+?)' class='page larger'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
        
    sPattern = '<iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
    