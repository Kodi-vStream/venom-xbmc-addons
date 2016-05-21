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
    
SITE_IDENTIFIER = 'videobuzzy_com'
SITE_NAME = 'Videobuzzy.com'
SITE_DESC = 'Selection des vidéos les plus populaires de Videobuzzy'

URL_MAIN = 'http://www.videobuzzy.com/'

MOVIE_NETS = ('http://www.videobuzzy.com/top-video.php', 'showMovies')

MOVIE_NETS = ('http://', 'load')
NETS_NEWS =  ('http://www.videobuzzy.com/top-video.php', 'showMovies')
NETS_GENRES = (True, 'load')

#URL_SEARCH = ('http://www.notre-ecole.net/?s=', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
    
def load():
   
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    liste = []
    liste.append( ["Top Vidéo","http://www.videobuzzy.com/top-video.php"] )
    liste.append( ["Insolite","http://www.videobuzzy.com/Insolite.htm"] )
    liste.append( ["Football","http://www.videobuzzy.com/Football.htm"] )
    liste.append( ["Humour","http://www.videobuzzy.com/Humour.htm"] )
    liste.append( ["Animaux","http://www.videobuzzy.com/Animaux.htm"] )
    liste.append( ["Télévision","http://www.videobuzzy.com/Television.htm"] )
    liste.append( ["Music","http://www.videobuzzy.com/Musique.htm"] )
    liste.append( ["Sport","http://www.videobuzzy.com/Sport.htm"] )
    liste.append( ["Cinema","http://www.videobuzzy.com/Cinema.htm"] )
    
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'doc.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.videobuzzy.com/'+sSearchText  
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

    sPattern = "<a class='titre_news_index' href='(.+?)' title='(.+?)'>.+?<img class=\"thumbnail\" src='(.+?)'.+?>.+?<span class='corps_news_p2'>(.+?)</span>"
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?</span><a href="(.+?)" title=\'.+?\'>.+?</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        print aResult[1][0]
        return URL_MAIN+aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
               
        
    sPattern = 'file: "(.+?)", label: "(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry[0])
            sTitle = sMovieTitle+' | '+aEntry[1]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
    