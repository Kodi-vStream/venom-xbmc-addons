#-*- coding: utf-8 -*-
#Venom
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
 
SITE_IDENTIFIER = 'malaisetv'
SITE_NAME = 'MalaiseTV.com'
SITE_DESC = 'Les séquences les plus embarrassantes de la télévision française'
 
URL_MAIN = 'http://www.malaisetv.com'
 
URL_SEARCH = (URL_MAIN + '/ajax/data.php?query=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN + '/ajax/data.php?category=59&start=0', 'showMovies')
NETS_GENRES = (True, 'showGenre')
 
def load(): 
    oGui = cGui() 
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0]) 
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Videos Nouveautes', 'news.png', oOutputParameterHandler)  
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Videos Genres', 'genres.png', oOutputParameterHandler)
               
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return
 
 
def showGenre():
    oGui = cGui()
  
    liste = []
    liste.append( ['Top vidéo', URL_MAIN + '/ajax/data.php?category=58&start=0'] )
    liste.append( ['Politique', URL_MAIN + '/ajax/data.php?category=0&start=0'] )
    liste.append( ['Tv', URL_MAIN + '/ajax/data.php?category=1&start=0'] )
    liste.append( ['LipDup', URL_MAIN + '/ajax/data.php?category=2&start=0'] )
    liste.append( ['International', URL_MAIN + '/ajax/data.php?category=3&start=0'] )
    liste.append( ['Divers', URL_MAIN + '/ajax/data.php?category=4&start=0'] )

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
    
    cConfig().log(sUrl)
    
    sPattern = 'div class="imgContainer"><img alt="([^"]+)" height=".+?" src="([^"]+)"><div data-video="([^"]+)"'
     
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        
        for aEntry in aResult[1]:
            
            sHosterUrl   = str(aEntry[2])
            sThumbnail = str(aEntry[1])
            
            sTitle  = str(aEntry[0])
            sTitle = sTitle.replace('Image prévisionnelle: ', '')
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
             
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)            
            
        sNextPage = __checkForNextPage(sUrl)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]',
                        'next.png',  oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
 
 
def __checkForNextPage(url):
    if 'start' not in url:
        return url + '&start=10'

    sPattern = '&start=([0-9]+)'
    aResult = re.search(sPattern,url)
    if (aResult):
        V1 = aResult.group(1)
        V2 = str( int(V1) + 10)
        url = url.replace('&start=' + V1,'&start=' + V2)
        
    return url
