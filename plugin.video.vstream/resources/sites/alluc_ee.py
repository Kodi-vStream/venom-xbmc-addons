#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import re
    
SITE_IDENTIFIER = 'alluc_ee'
SITE_NAME = '[COLOR orange]Alluc.ee[/COLOR]'
SITE_DESC = 'Moteur de recherche alluc'

URL_MAIN = 'http://www.alluc.ee/'

URL_SEARCH = ('http://www.alluc.ee/stream/lang%3Afr+', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
    
def load():
   
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory() 

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN+ 'stream/lang%3Afr+' + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    

def showMovies(sSearch = ''):
    
    if sSearch:
      sUrl = sSearch
      sSearch = sSearch.replace(' ','+')

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oGui = cGui()
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sHtmlContent = sHtmlContent.replace('<div class="ifabh clickable" onclick="window.location','')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    oParser = cParser()
    
    #first scan to optimise
    sPattern = 'onclick="window\.location(.+?)(?:<div class="clickable|<br\/>)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        return

    sPattern1 = '<img.+?src="\/(thumbnail\/.+?)" *\/>'
    #sPattern2 = 'class="forstar.+?>(.+?)<\/a>.+?<a title="(.+?)" href="/(.+?)" class="source" >.+?<img  src=".+?" title="(.+?)"'
    sPattern2 = 'class="forstar.+?>(.+?)<\/a>.+?<a title="(.+?)" href="/(.+?)".+?>.+?<img *src=".+?" title="(.+?)"'
    #sPattern = '(?:' + sPattern1 + ').+?'+ sPattern2
    
    for aEntry in aResult[1]:
        
        #ici je sais pas, pas moyen de faire tourner le regex
        if 'src="/thumbnail/' in aEntry:
            sPattern = '(?:' + sPattern1 + ').+?'+ sPattern2
        else:
            sPattern = '(.)' + sPattern2
                
        aResult2 = oParser.parse(aEntry, sPattern)
        
        if (aResult2[0] == True):
            total = len(aResult2[1])
            dialog = cConfig().createDialog(SITE_NAME)
            for aEntry in aResult2[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break
                
                sthumb = aEntry[0]
                sHost = aEntry[1]
                sCom = aEntry[2]
                sUrl = aEntry[3]
                sFlag = aEntry[4]
                
                if len(sthumb) < 2:
                    sthumb = 'put1debug'
                else:
                    sthumb = URL_MAIN + sthumb
                
                sTitle = re.sub('l\/(.+?)\/.+$','\\1',sUrl)
                
                sUrl = URL_MAIN + sUrl
                
                sLang = 'FR'              
                if 'vostfr' in sCom or 'vostfr' in sUrl:
                    sLang = 'VOSTFR'
                    
                sQual = 'SD'
                if 'HD' in sCom or 'HD' in sUrl:
                    sQual = 'HD'                                
                
                sDisplaytitle = '[COLOR coral]' + sHost + '[/COLOR] ' + '[B](' + sLang + '/' + sQual + ')[/B] ' + sTitle
                
                #ne pas l'afficher si host special
                if sHost not in 'freakshare.com':
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                    oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                    oOutputParameterHandler.addParameter('sThumbnail', str(sthumb))
                    oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, '', sthumb,'', oOutputParameterHandler)
            
            cConfig().finishDialog(dialog)
            
    sNextPage = __checkForNextPage(sHtmlContent)
    if (sNextPage != False):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            
    if not sSearch:
        oGui.setEndOfDirectory()
           
        

def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a rel="" href="\/([^<>"]+?)"(?: rel=\'next\')*>Next<\/a><\/li>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN+aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()           
     
    oParser = cParser()
    
    sPattern = '<iframe.+?src="(.+?)".+?<\/iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True) and aResult[1][0].startswith('/'):
        sUrl = URL_MAIN + aResult[1][0][1:]

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()           
                          
        sPattern = '<a href="([^<>"]+?)" rel="nofollow" target="_blank">Click to Open The Full Video<\/a>'
        
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            sUrl = aResult[1][0]
            
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            
            sPattern = '<iframe.+?src="(.+?)".+?<\/iframe>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
        else:
            return
            
        
    
    if (aResult[0] == True):
            
        aEntry = aResult[1]
        
        sTitle = sMovieTitle
        
        sHosterUrl = str(aEntry[0])
        
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
            
    oGui.setEndOfDirectory()
    
