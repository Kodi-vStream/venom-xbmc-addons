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
#from resources.lib.util import cUtil


SITE_IDENTIFIER = 'tvrex_net' 
SITE_NAME = 'Tvrex.net'
SITE_DESC = 'NBA Live/Replay'

URL_MAIN = 'http://tvrex.net'
REDDIT = 'https://www.reddit.com/r/nbastreams/'
    
URL_SEARCH = ('http://tvrex.net/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


SPORT_SPORTS = ('http://', 'ReplayTV')

def load():
    
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Replay NBA Games', 'news.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  


def TimeET():
    #Temp
    sUrl = 'http://www.worldtimeserver.com/time-zones/est/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
    sPattern = '<span id="theTime" class="fontTS">\s*(.+?)\s*</span>'
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        return aResult[1][0]
        
    timeError = ''
    return timeError

def ReplayTV():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REDDIT)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Live NBA Games', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/nba/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA Games', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/2016-nba-playoffs/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA 2016 Playoffs', 'tv.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/2015-nba-playoffs/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA 2015 Playoffs', 'tv.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/nba/all-star-weekend/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA All Star Weekend', 'tv.png', oOutputParameterHandler)
            
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
    
    
    if 'reddit' in sUrl:

        TimeUTC = TimeET()
        
        sPattern = 'utm_name=nbastreams".+?>Game Thread:(.+?)</a>.+?<ul class=".+?"><li class=".+?"><a href="(.+?)"'  
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Live NBA Game (@Reddit)[/COLOR]' + '[COLOR teal]' + ' / '+ '[Utc ET: ' +TimeUTC+ ']' + '[/COLOR]')
    
    
    elif '?s=' in sUrl:
        
        sPattern = '<a href="([^"]+)"><img src="[^"]+" data-hidpi="(.+?)\?.+?" alt="(.+?)"'

    else:

        sPattern = '<a href="([^"]+)">\s*<img src="[^"]+" data-hidpi="(.+?)\?.+?" alt="(.+?)" width=".+?"'

    
    
    sDateReplay = ''
    sDate = ''
    
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            
            #game thread sur reddit 
            if 'reddit' in sUrl:
                try:  
                   sUrl2 = aEntry[1]
                   sTitle = aEntry[0]
                   sThumbnail = ''
                   
                   sTitle2= sTitle.split("(")
                   sTitle = sTitle2[0]
                   sTimeLive = sTitle2[1]
                   sTimeLive = sTimeLive.replace(')', '')
                   sTitle = '[COLOR teal]' + sTimeLive + '[/COLOR]' + sTitle

                except:
                      #temp test
                      sThumbnail = ''
                      sTitle = 'Erreur parse'
                      sUrl2 = ''
            else:

                sTitle = aEntry[2]
                sUrl2 = aEntry[0]
                sThumbnail = aEntry[1]
          
            try:

               if 'category/nba' in sUrl:
                   sTitle2 = sTitle.split(" – ")
                   sTitle = sTitle2[0]
                   sDateReplay =  sTitle2[1]

                   if (sDate != sDateReplay):
                       oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Replay[/COLOR]' + '[COLOR teal]' + ' / '+ sDateReplay + '[/COLOR]')
                       sDate = sDateReplay
            
            except:
                  pass  

            try:
               if ('category/2016' in sUrl) or ('?s=' in sUrl):
                   if 'Game' in sTitle:
                       sTitle2 = sTitle.split(":")
                       sGame = sTitle2[0] +':'
                       sTitle3 = sTitle2[1]
                   else:
                       sGame = 'Game: '
                       sTitle3 = sTitle

                   sTitle3 = sTitle3.replace('\xe2\x80\x93', '-')
                   sTitle = sTitle3.split("-")
                   sTeam = sTitle[0]
                   if sTitle[1]:
                       sDatePlayoff = sTitle[1]
                   else: 
                       sDatePlayoff = ''
   
                   sTitle = '[COLOR olive]' + sGame + '[/COLOR]' + sTeam + '[COLOR teal]' +'/' + sDatePlayoff + '[/COLOR]'  

            except:
                  pass
            
            sTitle = sTitle.replace(' vs ', '[COLOR gray] vs [/COLOR]').replace('@', '[COLOR gray] vs [/COLOR]')
            
                   
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oOutputParameterHandler.addParameter('sDateReplay', sDateReplay)
            
           

  
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sUrl2, oOutputParameterHandler)
    
                
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    
    oParser = cParser()
    
    sPattern = "<span class='current'>.+?</span><a href='(.+?)' class='inactive'"
    
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
    sDateReplay = oInputParameterHandler.getValue('sDateReplay')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
          
    
    oParser = cParser()

    
    if sDateReplay:
       sMovieTitle = sMovieTitle + '[COLOR teal]' + ' / ' + sDateReplay +'[/COLOR]'

    
    #Test 
    if 'nbastreams' in sUrl:

        sPattern = '<a href="(http://nbastreams.pw/.+?)">(.+?)</a>'   
        sDisplay ='[COLOR olive]Streaming disponibles:[/COLOR]'         
        sThumbnail = ''
   
    else:  
  
        sPattern = '<a href="(https://open.+?)" target="_blank">(.+?)</a>'
    
        
        sDisplay = '[COLOR olive]Qualités disponibles:[/COLOR]'   
    
    aResult = oParser.parse(sHtmlContent, sPattern)  
    
    oGui.addText(SITE_IDENTIFIER,sMovieTitle)
    
    
    oGui.addText(SITE_IDENTIFIER,sDisplay)  
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry[0]
            sTitle = aEntry[1]
            
            #Pour affichage test reddit
            if 'nbastreams' in sUrl:
                sTitle = '[nbastreamspw] ' + sTitle
                sHosterUrl ='http://lol.m3u8'
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
            
 
    oGui.setEndOfDirectory()
