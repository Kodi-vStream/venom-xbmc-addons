#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler

import urllib
import xbmc
import md5

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'cBseries'
SITE_NAME = 'Betaseries'

API_KEY = '56ab1fd1ef57'
API_VERS = '2.4'
API_URL = 'https://api.betaseries.com'

class cBseries:

    def __init__(self):
        #self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        #self.__sFunctionName = ''
      

    def getToken(self):
        
        sUrl = 'https://api.betaseries.com/members/auth'
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        
        oRequestHandler.addParameters('login', 'Dev025')
        passw = md5.new('developer').hexdigest()
        oRequestHandler.addParameters('password', passw)

        sHtmlContent = oRequestHandler.request();
        result = json.loads(sHtmlContent)
        
        xbmc.log(str(result['user']))

        total = len(sHtmlContent)

        if (total > 0):
            #self.__Token  = result['token']
            cConfig().setSetting('bstoken', str(result['token']))
            xbmc.executebuiltin("Container.Refresh")
            return
        return False
        
    def delFavourites(self):
        
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

        meta = {}      
        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['siteurl'] = siteUrl
        try:
            cDb().del_favorite(meta)
        except:
            pass
        
        return
  
    def getLoad(self):
        
        #self.getToken()
        oGui = cGui()
        
        if cConfig().getSetting("bstoken") == '':
            self.getToken()
        else:            
            oRequestHandler = cRequestHandler('https://api.betaseries.com/members/infos')
            oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
            oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
            oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
            #n'affiche pas les infos des films
            oRequestHandler.addParameters('summary', 'false')

            sHtmlContent = oRequestHandler.request();
            result = json.loads(sHtmlContent)
            
            xbmc.log(str(result))
            
            total = len(sHtmlContent)
            
            if (total > 0):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'https://')
                oGui.addText(SITE_IDENTIFIER, '[COLOR khaki]Bonjour, '+result['member']['login']+'[/COLOR]', oOutputParameterHandler)
        
                # for i in result['shows']:
                    # sId, sTitle = i['id'], i['name']
                if (result['member']['stats']['shows'] > 0): 
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', 'https://api.betaseries.com/members/infos')
                    oOutputParameterHandler.addParameter('param', 'shows')
                    oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Series ('+str(result['member']['stats']['shows'])+')', 'mark.png', oOutputParameterHandler)
                    
                if (result['member']['stats']['movies'] > 0): 
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', 'https://api.betaseries.com/members/infos')
                    oOutputParameterHandler.addParameter('param', 'movies')
                    oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Films ('+str(result['member']['stats']['movies'])+')', 'mark.png', oOutputParameterHandler)
        
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://api.betaseries.com/movies/member')
        oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Films (favories)', 'mark.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://api.betaseries.com/shows/member')
        oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Series (favories)', 'mark.png', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()        
     

    def getBseries(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sParam = oInputParameterHandler.getValue('param')
        
        oGui = cGui()
           
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        #api buguer normalement ça affiche que les films et series
        #oRequestHandler.addParameters('only', 'true')

        sHtmlContent = oRequestHandler.request();
        result = json.loads(sHtmlContent)
        
        xbmc.log(str(result['member']['movies']))
        
        total = len(sHtmlContent)
        
        if (total > 0):
            for i in result['member'][sParam]:
                sId, sTitle = i['id'], i['title']
                sTitle = sTitle.encode("utf-8")
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://')
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
               
               
            oGui.setEndOfDirectory()
        return
        
    def getBseries2(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        #aParams = oInputParameterHandler.getAllParameter()

        iPage = 1
        if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')
           
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        #oRequestHandler.addParameters('start', iPage)

        sHtmlContent = oRequestHandler.request();
        result = json.loads(sHtmlContent)
        
        xbmc.log(str(result))
        
        total = len(sHtmlContent)
        
        try:
            row = cDb().get_favorite()

            for data in row:

                title = data[1]
                siteurl = urllib.unquote_plus(data[2])
                site = data[3]
                function = data[4]
                cat = data[5]
                thumbnail = data[6]
                fanart = data[7]
                
                if thumbnail == '':
                    thumbnail = 'False'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteurl)
                oOutputParameterHandler.addParameter('sMovieTitle', title)
                oOutputParameterHandler.addParameter('sThumbnail', thumbnail)
                
                if (function == 'play'):
                    oHoster = cHosterGui().checkHoster(siteurl)
                    oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
                    oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
                    oOutputParameterHandler.addParameter('sMediaUrl', siteurl)

                if (cat == sCat):
                    oGuiElement = cGuiElement()
        
                    oGuiElement.setSiteName(site)
                    oGuiElement.setFunction(function)
                    oGuiElement.setTitle(title)
                    oGuiElement.setIcon("mark.png")
                    oGuiElement.setMeta(0)
                    oGuiElement.setThumbnail(thumbnail)
                    oGuiElement.setFanart(fanart)
                    
                    oGui.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)
                    
                    if (function == 'play'):
                        oGui.addHost(oGuiElement, oOutputParameterHandler)
                    else:
                        oGui.addFolder(oGuiElement, oOutputParameterHandler)
                        
                    #oGui.addFav(site, function, title, "mark.png", thumbnail, fanart, oOutputParameterHandler)
               
            oGui.setEndOfDirectory()
        except: pass
        return
        
    def setFavorite(self):
        oInputParameterHandler = cInputParameterHandler()
        #xbmc.log(str(oInputParameterHandler.getAllParameter()))
        
        if int(oInputParameterHandler.getValue('sCat')) < 1:
            cConfig().showInfo('Error','Mise en Favoris non possible pour ce lien')
            return
        
        meta = {}
        meta['siteurl'] = oInputParameterHandler.getValue('siteUrl')
        meta['site'] = oInputParameterHandler.getValue('sId')
        meta['fav'] = oInputParameterHandler.getValue('sFav')
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        
        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] =  xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            cDb().insert_favorite(meta)
        except:
            pass
