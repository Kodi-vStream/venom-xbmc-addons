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
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'notre_ecole_net'
SITE_NAME = 'Notre-Ecole.net'
SITE_DESC = 'Un blog qui traite de notre rapport avec l\'argent, de la consommation, de notre modèle économique et qui s\'interroge sur l\'avenir de notre planète'

URL_MAIN = 'http://www.notre-ecole.net/'

DOC_DOCS = ('http://www.notre-ecole.net/?s=.', 'showMovies')

URL_SEARCH = ('http://www.notre-ecole.net/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
   
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    liste = []
    liste.append( ["Films Documentaires Reportages Enquetes","http://www.notre-ecole.net/c/documentaires/"] )
    liste.append( ["Ecologie - Environnement","http://www.notre-ecole.net/c/ecologie-environnement/"] )
    liste.append( ["Economie - Finance","http://www.notre-ecole.net/c/economie-finance/"] )
    liste.append( ["Histoire","http://www.notre-ecole.net/c/histoire/"] )
    liste.append( ["Philosophie","http://www.notre-ecole.net/c/philosophie/"] )
    liste.append( ["Politique","http://www.notre-ecole.net/c/politique/"] )
    liste.append( ["Politique - France","http://www.notre-ecole.net/c/politique/politique-france/"] )
    liste.append( ["Politique - Union Européenne","http://www.notre-ecole.net/c/politique/union-europeenne/"] )
    liste.append( ["Médias - Publicité","http://www.notre-ecole.net/c/medias-publicite/"] )
    liste.append( ["Société","http://www.notre-ecole.net/c/societe/"] )
    liste.append( ["Santé et sanitaire","http://www.notre-ecole.net/c/sante-sanitaire/"] )
    liste.append( ["Guerres","http://www.notre-ecole.net/c/guerres/"] )
    liste.append( ["Pétitions","http://www.notre-ecole.net/c/petition/"] )
    
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'doc.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.notre-ecole.net/?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = '<img.+?src="([^<]+)".+?/>.+?<a href="([^<]+)" rel="bookmark">([^<]+)</a>.+?</div>(.+?)<p class="quick-read-more">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[0], aEntry[3], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page larger" href="(.+?)">.+?</a>'
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
    