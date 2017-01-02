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
from resources.lib.player import cPlayer
import urllib,re,urllib2
import base64,sys,xbmc

SITE_IDENTIFIER = 'tvrex_net' 
SITE_NAME = 'Tvrex.net'
SITE_DESC = 'NBA Live/Replay'

URL_MAIN = 'http://tvrex.net'
REDDIT = 'https://www.reddit.com/r/nbastreams/'
  
URL_SEARCH = ('http://tvrex.net/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SPORT_SPORTS = ('http://', 'ReplayTV')

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Chrome/47.0'

headers = { 'User-Agent' : UA }

Logo_Reddit = 'aHR0cHM6Ly9iLnRodW1icy5yZWRkaXRtZWRpYS5jb20va1c5ZFNqRFlzUDhGbEJYeUUyemJaaEFCaXM5eS0zVHViSWtic0JfUDlBay5wbmc='
Logo_Nba = 'aHR0cDovL3d3dy5vZmZpY2lhbHBzZHMuY29tL2ltYWdlcy90aHVtYnMvSS1sb3ZlLXRoaXMtZ2FtZS1uYmEtbG9nby1wc2Q2MDQwNy5wbmc='

def load():
    
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Live/Replay NBA Games', 'news.png', oOutputParameterHandler)
    
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
    
    sUrl = 'http://www.worldtimeserver.com/current_time_in_CA-ON.aspx'
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Live NBA Games [beta]', 'search.png', oOutputParameterHandler)
    
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
  

def showLive():
   
      oGui = cGui()
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')

      sTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumbnail = oInputParameterHandler.getValue('sThumbnail')  
      
      try:
         request = urllib2.Request(sUrl,None,headers)
         reponse = urllib2.urlopen(request)
         sHtmlContent = reponse.read()
         reponse.close()
      except urllib2.HTTPError:
                              sHtmlContent = ''
                              pass
      
      sPattern = 'player.html\#(.+?)"'
      
      oParser = cParser()
      aResult = oParser.parse(sHtmlContent, sPattern)
      
      if (aResult[0] == True):
          
          sUrl = aResult[1][0]
          
          sDisplayTitle = sTitle + '[COLOR skyblue]' + '  Lien Direct' + '[/COLOR]'

     
          oOutputParameterHandler = cOutputParameterHandler()
          oOutputParameterHandler.addParameter('siteUrl', sUrl)
          oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
          oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

          oGui.addMovie(SITE_IDENTIFIER, 'play__', sDisplayTitle, '', sThumbnail, sUrl, oOutputParameterHandler)
     
      else:
          oGui.addText(SITE_IDENTIFIER, '(Lien non disponible)')
  
      oGui.setEndOfDirectory()


def play__():
    
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sTitle)
    oGuiElement.setMediaUrl(sUrl)
    oGuiElement.setThumbnail(sThumbnail)

    oPlayer = cPlayer()
    oPlayer.clearPlayList()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return
        
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
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Live NBA Game (@Reddit)[/COLOR]' + '[COLOR gray]' + '  [ utc ET: ' + '[/COLOR]' +TimeUTC+ '[COLOR gray]' + ' ]' + '[/COLOR]')
    
    
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
            
            #Listage game thread sur reddit 
            if 'reddit' in sUrl:
                try:  
                   sUrl2 = aEntry[1]
                   sTitle = aEntry[0]
                   sThumbnail = base64.b64decode(Logo_Reddit)
                   sTitle2= sTitle.split("(")
                   sTitle = sTitle2[0]
                   sTimeLive = sTitle2[1]
                   sTimeLive = sTimeLive.replace(')', '')
                   sTitle = '[COLOR teal]' + sTimeLive + '[/COLOR]' + sTitle

                except:
                      #temp erreur test
                      sThumbnail = ' '
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
    
    else:
        if  'reddit' in sUrl:

             oGui.addText(SITE_IDENTIFIER,'Thread liens matchs non disponible pour le moment')
        else:

            oGui.addText(SITE_IDENTIFIER,'(Replay non disponible/Erreur)')

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

    
    if 'nbastream' in sUrl:
    
        sPattern = '<a href="(http://nbastreams.pw/.+?)">(.+?)</a>'
        
        sDisplay ='[COLOR olive]Streaming disponibles:[/COLOR]'         
        
   
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
            xbmc.log('NBASTREAMPW: ' +str(sHosterUrl))
            #On ouvre liens nbastreams via showLive&play__
            #todo lien youtube a rajouter via hoster
            
            if 'nbastreams' in sHosterUrl:
                sTitle = '[NBAstreamspw] ' + sTitle
                sUrl = sHosterUrl
                sThumbnail = base64.b64decode(Logo_Nba)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl) 
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMovie(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumbnail, sUrl, oOutputParameterHandler)

            else:

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
            
 
    oGui.setEndOfDirectory()
