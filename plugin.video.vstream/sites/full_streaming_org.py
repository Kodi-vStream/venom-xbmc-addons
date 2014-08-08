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

SITE_IDENTIFIER = 'full_streaming_org'
SITE_NAME = 'full-streaming.org'

URL_MAIN = 'http://full-streaming.org/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    __createMenuEntry(oGui, 'showSearch', 'Recherche', 'search.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/index.php?do=lastnews')
    __createMenuEntry(oGui, 'showMovies', 'Films Nouveautés', 'news.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/films/')
    __createMenuEntry(oGui, 'showMovies', 'Films', 'films.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/index.php?do=search')
    __createMenuEntry(oGui, 'showGenre', 'Films Genre', 'genres.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/index.php?do=search')
    __createMenuEntry(oGui, 'showQlt', 'Films Qualités', 'films.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/series/')
    __createMenuEntry(oGui, 'showMovies', 'Series', 'series.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/series-fr/')
    __createMenuEntry(oGui, 'showMovies', 'Series VF', 'series.png', '', '', 0, oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://full-streaming.org/series-vostfr/')
    __createMenuEntry(oGui, 'showMovies', 'Series VOSTFR', 'series.png', '', '', 0, oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sIcon, sThumbnail, sDesc, sMeta='', oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGuiElement.setIcon(sIcon)
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setDescription(cUtil().removeHtmlTags(sDesc))
    oGuiElement.setMeta(sMeta)
    
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://full-streaming.org/xfsearch/'+sSearchText  
            showMovies(sUrl)
            return  
    oGui.setEndOfDirectory()
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://full-streaming.org/action/'] )
    liste.append( ['Animation','http://full-streaming.org/animation/'] )
    liste.append( ['Arts Martiaux','http://full-streaming.org/arts-martiaux/'] )
    liste.append( ['Aventure','http://full-streaming.org/aventure/'] )
    liste.append( ['Biopic','http://full-streaming.org/biopic/'] )
    liste.append( ['Comedie','http://full-streaming.org/comedie/'] )
    liste.append( ['Comedie Dramatique','http://full-streaming.org/comedie-dramatique/'] )
    liste.append( ['Comedie Musicale','http://full-streaming.org/comedie-musicale/'] )
    liste.append( ['Documentaire','http://full-streaming.org/documentaire/'] )
    liste.append( ['Drame','http://full-streaming.org/drame/'] )
    liste.append( ['Epouvante Horreur','http://full-streaming.org/epouvante-horreur/'] ) 
    liste.append( ['Erotique','http://full-streaming.org/erotique'] )
    liste.append( ['Espionnage','http://full-streaming.org/espionnage/'] )
    liste.append( ['Famille','http://full-streaming.org/famille/'] )
    liste.append( ['Fantastique','http://full-streaming.org/fantastique/'] )  
    liste.append( ['Guerre','http://full-streaming.org/guerre/'] )
    liste.append( ['Historique','http://full-streaming.org/historique/'] )
    liste.append( ['Musical','http://full-streaming.org/musical/'] )
    liste.append( ['Policier','http://full-streaming.org/policier/'] )
    liste.append( ['Peplum','http://full-streaming.org/peplum/'] )
    liste.append( ['Romance','http://full-streaming.org/romance/'] )
    liste.append( ['Science Fiction','http://full-streaming.org/science-fiction/'] )
    liste.append( ['Spectacle','http://full-streaming.org/spectacle/'] )
    liste.append( ['Thriller','http://full-streaming.org/thriller/'] )
    liste.append( ['Western','http://full-streaming.org/western/'] )
    liste.append( ['Divers','http://full-streaming.org/divers/'] ) 
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        __createMenuEntry(oGui, 'showMovies', sTitle, 'genres.png', '', '', 0, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showQlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['HD','http://full-streaming.org/hd/'] )
    liste.append( ['BDrip Dvdrip','http://full-streaming.org/bdrip-dvdrip/'] )
    liste.append( ['DvdScr R5','http://full-streaming.org/dvdscr-r5/'] )
    liste.append( ['TS Cam','http://full-streaming.org/ts-cam/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        __createMenuEntry(oGui, 'showMovies', sTitle, 'films.png', '', '', 0, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showMovies(sUrl = ''):
    oGui = cGui()
    if sUrl:
      sUrl = sUrl
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = 'class="movie movie-block"><img src="([^<]+)" alt=".+?" title="([^<]+)"/>.+?<h2 onclick="window.location.href=\'([^<]+)\'">.+?<div style="color:#F29000">.+?<div.+?>(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            if '/series' in sUrl:
                __createMenuEntry(oGui, 'seriesHosters', sTitle,'', aEntry[0], aEntry[3], 2, oOutputParameterHandler)
            else:
                __createMenuEntry(oGui, 'showHosters', sTitle, '', aEntry[0], aEntry[3], 1, oOutputParameterHandler)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            __createMenuEntry(oGui, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', '', '', 0, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation".+? <span.+? <a href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def __checkiframePage(sUrl):
    sPattern = '<p><!--baslik:.+?--><br />.?<iframe.+?src="(.+?)"'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
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
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
               
        
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
    
def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
               
    sPattern = '<dd><a href="([^<]+)" class="zoombox w630% h450%" title="(.+?)"><button class="btn">.+?</button></a></dd>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sTitle=re.sub(r'\[.*\]',r'',aEntry[1])
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
    