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
import re

SITE_IDENTIFIER = 'docspot_fr'
SITE_NAME = 'Docspot.fr'
SITE_DESC = 'docspot.fr + 3000 Documentaires et reportages en Streaming gratuit !'

URL_MAIN = 'http://www.docspot.fr/'
DOC_DOCS = ('http://www.docspot.fr/?cat=0', 'showMovies')

URL_SEARCH = ('http://www.docspot.fr/search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://frenchstream.org/les-plus-vues')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Documentaires Genres', 'genres.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.docspot.fr/search/'+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["Arte","http://www.docspot.fr/search/documentaire+arte"] )
    liste.append( ["National - Geographic","http://www.docspot.fr/search/documentaire+national+geographic"] )
    liste.append( ["Archéologie","http://www.docspot.fr/search/documentaire+arch%C3%A9ologie"] )
    liste.append( ["Astronomie","http://www.docspot.fr/search/documentaire+astronomie"] )
    liste.append( ["Animaux","http://www.docspot.fr/search/reportage+animaux"] )
    liste.append( ["Climat","http://www.docspot.fr/search/documentaire+climat"] )
    liste.append( ["Découverte","http://www.docspot.fr/search/documentaire+d%C3%A9couverte"] )
    liste.append( ["Démographie","http://www.docspot.fr/search/documentaire+d%C3%A9mographie"] )
    liste.append( ["Economie","http://www.docspot.fr/search/documentaire+%C3%A9conomie"] )
    liste.append( ["Education","http://www.docspot.fr/search/documentaire+education"] )
    liste.append( ["Enquete","http://www.docspot.fr/search/reportage+enquete"] )
    liste.append( ["Géopolitique","http://www.docspot.fr/search/documentaire+geopolitique"] )
    liste.append( ["Guerre","http://www.docspot.fr/search/documentaire+guerre"] )
    liste.append( ["Histoire","http://www.docspot.fr/search/documentaire+histoire"] )
    liste.append( ["Paranormal","http://www.docspot.fr/search/documentaire+paranormal"] )
    liste.append( ["Reportage","http://www.docspot.fr/search/reportage"] )
    
    liste.append( ["Santé","http://www.docspot.fr/search/documentaire+sant%C3%A9"] )
    liste.append( ["Science","http://www.docspot.fr/search/documentaire+science"] )
    liste.append( ["Technologie","http://www.docspot.fr/search/documentaire+technologie+science"] )
    liste.append( ["Sport","http://www.docspot.fr/search/documentaire+sport"] )
    liste.append( ["Societe","http://www.docspot.fr/search/documentaire+societe"] )
    
                
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
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = "<div class='mediathumb'>.*?<a href='([^<]+)' title='([^<]+)'>.*?<img src='([^<]+)' alt='(.+?)'>.*?</a>"
    
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
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[3]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[3], '', aEntry[2], aEntry[1], oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<li class='next'><a href='(.+?)' class='next'>.+?</a></li>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        print aResult[1][0]
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
    