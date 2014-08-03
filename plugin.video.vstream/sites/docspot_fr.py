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
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'docspot_fr'
SITE_NAME = 'Docspot.fr'

URL_MAIN = 'http://www.docspot.fr/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0')
    __createMenuEntry(oGui, 'showMovies', 'Documentaires', 'doc.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0&orderby=views')
    __createMenuEntry(oGui, 'showMovies', 'Documentaires Les plus vues', 'doc.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0&orderby=comments')
    __createMenuEntry(oGui, 'showMovies', 'Documentaires Les plus commentés', 'doc.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.docspot.fr/?cat=0&orderby=likes')
    __createMenuEntry(oGui, 'showMovies', 'Documentaires Les mieux notés', 'doc.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://frenchstream.org/les-plus-vues')
    __createMenuEntry(oGui, 'showGenres', 'Documentaires Genres', 'genres.png', '', '', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGuiElement.setIcon(sIcon)
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setDescription(cUtil().removeHtmlTags(sDesc))
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
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
        __createMenuEntry(oGui, 'showMovies', sTitle, 'genres.png', '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 


def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = '<a class="clip-link" data-id=".+?" title="([^<]+)" href="([^<]+)">.+?<img src="(.+?)" alt=".+?" />'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            __createMenuEntry(oGui, 'showHosters', aEntry[0], '', aEntry[2], '', oOutputParameterHandler)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            __createMenuEntry(oGui, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', '', '', oOutputParameterHandler)

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
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
    