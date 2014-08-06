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

SITE_IDENTIFIER = 'full_stream_net'
SITE_NAME = 'full-stream.net'

URL_MAIN = 'http://full-stream.net'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    __createMenuEntry(oGui, 'showSearch', 'Recherche', 'search.png', '', '', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-stream.net/lastnews/')
    __createMenuEntry(oGui, 'showMovies', 'Films Nouveautés', 'news.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-stream.net/films-en-vk-streaming/')
    __createMenuEntry(oGui, 'showMovies', 'Films', 'films.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    __createMenuEntry(oGui, 'showGenre', 'Films Genre', 'genres.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-stream.net/seriestv/')
    __createMenuEntry(oGui, 'showMovies', 'Séries', 'series.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-stream.net/seriestv/vf/')
    __createMenuEntry(oGui, 'showMovies', 'Séries VF', 'series.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-stream.net/seriestv/vostfr/')
    __createMenuEntry(oGui, 'showMovies', 'Séries VOSTFR', 'series.png', '', '', oOutputParameterHandler)
            
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
 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            #sSearchText = cUtil().urlEncode(sSearchText)
            sUrl = 'http://full-stream.net/xfsearch/'+sSearchText+'/'  
            showMovies(sUrl)
            return  
    oGui.setEndOfDirectory()
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['HD/HQ','http://full-stream.net/films-en-vk-streaming/haute-qualite/'] )
    liste.append( ['Action','http://full-stream.net/films-en-vk-streaming/action/'] )
    liste.append( ['Aventure','http://full-stream.net/films-en-vk-streaming/aventure/'] )
    liste.append( ['Animation','http://full-stream.net/films-en-vk-streaming/animation/'] )
    liste.append( ['Arts Martiaux','http://full-stream.net/films-en-vk-streaming/arts-martiaux/'] )
    liste.append( ['Biopic','http://full-stream.net/films-en-vk-streaming/biopic/'] )
    liste.append( ['Comedie','http://full-stream.net/films-en-vk-streaming/comedie/'] )
    liste.append( ['Comedie Dramatique','http://full-stream.net/films-en-vk-streaming/comedie-dramatique/'] )
    liste.append( ['Comedie Musicale','http://full-stream.net/films-en-vk-streaming/comedie-musicale/'] )
    liste.append( ['Drame','http://full-stream.net/films-en-vk-streaming/drame/'] )
    liste.append( ['Documentaire','http://full-stream.net/films-en-vk-streaming/documentaire/'] ) 
    liste.append( ['Horreur','http://full-stream.net/films-en-vk-streaming/horreur/'] )
    liste.append( ['Fantastique','http://full-stream.net/films-en-vk-streaming/fantastique/'] )
    liste.append( ['Guerre','http://full-stream.net/films-en-vk-streaming/guerre/'] )
    liste.append( ['Policier','http://full-stream.net/films-en-vk-streaming/policier/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        __createMenuEntry(oGui, 'showMovies', sTitle, 'genres.png', '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
    

def showMovies(sUrl = ''):
    print sUrl
    oGui = cGui()
    if sUrl:
      sUrl = sUrl
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&amp;w=210&amp;h=280','')
    sPattern = 'full-stream-view-hover"><img src=".+?src=(.+?)" alt="(.+?)".+?<h2><a href="(.+?)">.+?</a></h2>.+?<b>Résumé</b>(.+?)</div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/seriestv/' in sUrl  or 'saison' in aEntry[2]:
                __createMenuEntry(oGui, 'serieHosters', aEntry[1], '', aEntry[0], aEntry[3], oOutputParameterHandler)
            else:
                __createMenuEntry(oGui, 'showHosters', aEntry[1], '', aEntry[0], aEntry[3], oOutputParameterHandler)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            __createMenuEntry(oGui, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation".+? <span.+? <a href="(.+?)">'
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


    sPattern = '<iframe src="(.+?)"'
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
    
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)" title="([^<]+)" target="seriePlayer" class="ilink sinactive">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                sTitle = aEntry[1]
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)    

    oGui.setEndOfDirectory()