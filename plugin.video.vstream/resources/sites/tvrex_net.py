#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import re,urllib2
import base64

SITE_IDENTIFIER = 'tvrex_net'
SITE_NAME = 'Tvrex'
SITE_DESC = 'NBA Live/Replay'

URL_MAIN = 'http://tvrex.net/'
REDDIT = 'https://www.reddit.com/r/nbastreams/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SPORT_SPORTS = ('http://', 'ReplayTV')
REPLAYTV_GENRES = (True, 'showGenres')

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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Live NBA Games (bêta)', 'tv.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showLiveNbatv', 'Live 24/24 Chaine NBA TV (bêta)', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/nba-replays/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA Games', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/2017-nba-playoffs/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA 2017 Playoffs', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/2016-nba-playoffs/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA 2016 Playoffs', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/nba-replays/all-star-weekend/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Replay NBA All Star Week-end', 'tv.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Replay NBA (Par États/Équipes)', 'sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    
    liste = []
    liste.append( ['Atlanta (Hawks)',URL_MAIN + 'category/nba/atlanta-hawks/'] )
    liste.append( ['Boston (Celtics)',URL_MAIN + 'category/nba/boston-celtics/'] )
    liste.append( ['Brooklyn (Nets)',URL_MAIN + 'category/nba/brooklyn-nets/'] )
    liste.append( ['Charlotte (Hornets)',URL_MAIN + 'category/nba/charlotte-hornets/'] )
    liste.append( ['Chicago (Bulls)',URL_MAIN + 'category/nba/chicago-bulls/'] )
    liste.append( ['Cleveland (Cavaliers)',URL_MAIN + 'category/nba/cleveland-cavaliers/'] )
    liste.append( ['Dallas (Mavericks)',URL_MAIN + 'category/nba/dallas-mavericks/'] )
    liste.append( ['Denver (Nuggets)',URL_MAIN + 'category/nba/denver-nuggets/'] )
    liste.append( ['Détroit (Pistons)',URL_MAIN + 'category/nba/detroit-pistons/'] )
    liste.append( ['Golden-state (Warriors)',URL_MAIN + 'category/nba/golden-state-warriors/'] )
    liste.append( ['Houston (Rockets)',URL_MAIN + 'category/nba/houston-rockets/'] )
    liste.append( ['Indiana (Pacers)',URL_MAIN + 'category/nba/indiana-pacers/'] )
    liste.append( ['Los Angeles (Clippers)',URL_MAIN + 'category/nba/los-angeles-clippers/'] )
    liste.append( ['Los Angeles (Lakers)',URL_MAIN + 'category/nba/los-angeles-lakers/'] )
    liste.append( ['Memphis (Grizzlies)',URL_MAIN + 'category/nba/memphis-grizzlies/'] )
    liste.append( ['Miami (Heat)',URL_MAIN + 'category/nba/miami-heat//'] )
    liste.append( ['Milwaukee (Bucks)',URL_MAIN + 'category/nba/milwaukee-bucks//'] )
    liste.append( ['Minnesota (Timberwolves)',URL_MAIN + 'category/nba/minnesota-timberwolves/'] )
    liste.append( ['New-Orléans (Pelicans)',URL_MAIN + 'category/nba/new-orleans-pelicans/'] )
    liste.append( ['New-York (Knicks)',URL_MAIN + 'category/nba/new-york-knicks/'] )
    liste.append( ['Oklahoma City (Thunder)',URL_MAIN + 'category/nba/oklahoma-city-thunder/'] )
    liste.append( ['Orlando (Magic)',URL_MAIN + 'category/nba/orlando-magic//'] )
    liste.append( ['Philadelphia (79ers)',URL_MAIN + 'category/nba/philadelphia-76ers/'] )
    liste.append( ['Phoenix (Suns)',URL_MAIN + 'category/nba/phoenix-suns/'] )
    liste.append( ['Portland (Blazers)',URL_MAIN + 'category/nba/portland-trail-blazers/'] )
    liste.append( ['Sacramento (Kings)',URL_MAIN + 'category/nba/sacramento-kings/'] )
    liste.append( ['San Antonio (Spurs)',URL_MAIN + 'category/nba/san-antonio-spurs/'] )
    liste.append( ['Toronto (Raptors)',URL_MAIN + 'category/nba/toronto-raptors/'] )
    liste.append( ['Utah (Jazz)',URL_MAIN + 'category/nba/utah-jazz/'] )
    liste.append( ['Washington (Wizards)',URL_MAIN + 'category/nba/washington-wizards/'] )
    
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
    
    if 'reddit' in sUrl:

        TimeUTC = TimeET()
        
        sPattern = 'utm_name=nbastreams".+?>Game Thread:(.+?)</a>.+?<ul class=".+?"><li class=".+?"><a href="(.+?)"'
        
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Live NBA Game (@Reddit)[/COLOR]' + '[COLOR gray]' + '  [ Heure Locale ET : ' + '[/COLOR]' + TimeUTC + '[COLOR gray]' + ' ]' + '[/COLOR]')
    
    elif 'category/201' in sUrl:
        sPattern = '<a href="([^"]+)">([^<]+)</a></h2>'
    else:
        sPattern = '<a href="([^"]+)">(?:\s*|)<img src="[^"]+" data-hidpi="(.+?)\?.+?" alt="([^"]+)"(?:width=".+?"|)'

    sDateReplay = ''
    sDate = ''
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            
            #listage game thread via reddit 
            if 'reddit' in sUrl:
                try:  
                   sUrl2 = str(aEntry[1])
                   sTitle = str(aEntry[0])
                   sThumbnail = base64.b64decode(Logo_Reddit)
                   sTitle2= sTitle.split("(")
                   sTitle = sTitle2[0]
                   sTimeLive = sTitle2[1]
                   sTimeLive = sTimeLive.replace(')', '')
                   sTitle = '[COLOR teal]' + sTimeLive + '[/COLOR]' + sTitle

                except:
                      #erreur parse
                      sThumbnail = ' '
                      sTitle = 'Erreur parse'
                      sUrl2 = ''
            
            #listage replay&search
            else:
                
                if ('category/201' in sUrl):
                     
                     sTitle = str(aEntry[1])
                     sUrl2 = str(aEntry[0])
                     sThumbnail = ' '

                else:
                     sTitle = str(aEntry[2])
                     sUrl2 = str(aEntry[0])
                     sThumbnail = str(aEntry[1])

            try:
               if 'category/nba' in sUrl:

                   sTitle2 = sTitle.split(" ")
                   sTitle = sTitle2[0]
                   sDateReplay =  sTitle2[1]

                   if (sDate != sDateReplay):
                       oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Replay[/COLOR]' + '[COLOR teal]' + ' / '+ sDateReplay + '[/COLOR]')
                       sDate = sDateReplay
            
            except:
                  pass

            try:
               if ('category/201' in sUrl) or ('?s=' in sUrl) or ('search/' in sUrl):
                   
                   if 'Game' in sTitle:
                       sTitle2 = sTitle.split(":")
                       sGame = sTitle2[0] + ':'
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

                   sTitle = '[COLOR olive]' + sGame + '[/COLOR]' + sTeam + '[COLOR teal]' + '/' + sDatePlayoff + '[/COLOR]'

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
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
    
    else:
        if  'reddit' in sUrl:
             oGui.addText(SITE_IDENTIFIER,'(Aucun Match disponible via Reddit pour le moment)')
        else:
            oGui.addText(SITE_IDENTIFIER,'(Erreur - Replay non disponible)')

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)"'
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
    sHtmlContent = sHtmlContent.replace(' rel="nofollow"', '')
    
    if sDateReplay:
       sMovieTitle = sMovieTitle + '[COLOR teal]' + ' / ' + sDateReplay + '[/COLOR]'

    if 'reddit' in sUrl:
        
        sPattern = '(?:<td>|)<a href="(http.+?(?:nbastreams|eplstream|yoursportsinhd|247hd).+?)">(?:<strong>.+?</strong>|)([^<]+)</a></td>'
        
        aResult = re.findall(sPattern,sHtmlContent)
        
        sDisplay ='[COLOR olive]Streaming disponibles:[/COLOR]'         

    else:
        
        aResult =[]
        sPattern = '<a href="(https?://(?:wstream|youwa|openlo)[^"]+)" target="_blank">(?:([^<]+)</a>|)'
        sPattern2 = '(?:data\-lazy\-src|src)="(http.+?(?:openload|raptu)\.co[^"]+)"'
        
        aResult1 = re.findall(sPattern,sHtmlContent)
        aResult2 = re.findall(sPattern2,sHtmlContent)
        aResult = aResult1 + aResult2
        
        sDisplay = '[COLOR olive]Qualités disponibles:[/COLOR]'
    
    oGui.addText(SITE_IDENTIFIER,sMovieTitle)
    oGui.addText(SITE_IDENTIFIER,sDisplay)
    
    if (aResult):
        for aEntry in aResult:
            
            if 'reddit' in sUrl: #Live
                
                sThumbnail = base64.b64decode(Logo_Nba)
                sHosterUrl = str(aEntry[0]).replace('&amp;', '&')
                
                if ('yoursport' in aEntry[0]):
                    sTitle = ('[%s] %s') % ('YourSportsinHD', str(aEntry[1]))
                elif ('nbastream' in aEntry[0]):
                      sTitle = ('[%s] %s') % ('NBAstreamspw', str(aEntry[1]))
                elif ('eplstream' in aEntry[0]):
                      sTitle = ('[%s] %s') % ('EPLstreams', str(aEntry[1]))
                elif ('247hd' in aEntry[0]):
                      sTitle = ('[%s] %s') % ('247HD', str(aEntry[1]))
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                
                oGui.addMovie(SITE_IDENTIFIER, 'showLiveHosters', sTitle, '', sThumbnail, sHosterUrl, oOutputParameterHandler)
            
            else: #Replay
                
                if (aEntry[0]):
                    sHosterUrl = str(aEntry[0])
                if ('raptu' in aEntry):
                    sTitle = ('[%s]') % ('720p')
                    sHosterUrl = str(aEntry)
                elif ('openload' in aEntry):
                    sTitle = ('[%s]') % ('720p')
                    sHosterUrl = str(aEntry)
                elif ('youwatch' in aEntry[0]):
                      sTitle = ('[%s]') % ('540p')
                elif ('wstream' in aEntry[0]):
                      sTitle = ('[%s]') % ('720p')
                else:
                    sTitle = ('[%s]') % (str(aEntry[1]))

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
    
    else:

        oGui.addText(SITE_IDENTIFIER,'(Live/Replay non disponible)')

    oGui.setEndOfDirectory()


#Live 24/24 chaine nbatv

def showLiveNbatv():

    oGui = cGui()
    
    sThumbnail = base64.b64decode(Logo_Nba)
    sUrl = [('aHR0cDovL3d3dy4yNDdoZC5wdy9uYmEucGhwP2V4dGlkPTEmdmlldz1OQkFUVg=='), ('aHR0cDovL3lzaWhkLm1lL25iYXR2Lw==')]
    
    for aEntry in sUrl:

        sUrl = base64.b64decode(aEntry)
        if '247hd' in sUrl:
            sTitle = ('[%s] %s') % ('247HD', 'NBA TV')
        else:
            sTitle = ('[%s] %s') % ('YourSportsinHD', 'NBA TV')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl',sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

        oGui.addMovie(SITE_IDENTIFIER, 'showLiveHosters', sTitle, '', sThumbnail, sUrl, oOutputParameterHandler)

    oGui.setEndOfDirectory()


#recuperation lecture m3u8 nba livestream - ok sauf si geo ip ou lien secu ou regex a maj

def showLiveHosters():

      oGui = cGui()
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumbnail = oInputParameterHandler.getValue('sThumbnail')  

      UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
      
      try:
         
         request = urllib2.Request(sUrl)
         request.add_header('User-agent', UA)

         response = urllib2.urlopen(request)
         sHtmlContent = response.read()
         response.close()
      except urllib2.HTTPError:
                              sHtmlContent = ''
                              pass

      sPattern = '(?:\"|\')(.+?m3u8.+?)(?:\"|\')'

      aResult = re.findall(sPattern,sHtmlContent)

      if (aResult):
          for aEntry in aResult:
              #playoff2017 live ok avec UA ipad 
              sHosterUrl = aEntry + '|User-Agent=Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.1'

              oHoster = cHosterGui().checkHoster('m3u8')
              oHoster.setDisplayName(sTitle)
              oHoster.setFileName(sTitle)
              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

      else:
          oGui.addText(SITE_IDENTIFIER, '(Erreur connection ou stream non disponible : UA pas bon/Lien protégé/code soluce à trouver)')

      oGui.setEndOfDirectory()
