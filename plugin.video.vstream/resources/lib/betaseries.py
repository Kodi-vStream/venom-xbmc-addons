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

import urllib, urllib2, re
import xbmc
import time, md5
import unicodedata

import datetime, time

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'cBseries'
SITE_NAME = 'Betaseries'

API_KEY = '7139b7dace25c7bdf0bd79acf46fb02bd63310548b1f671d88832f75a4ac3dd6'
API_SECRET = 'bb02b2b0267b045590bc25c21dac21b1c47446a62b792091b3275e9c4a943e74'
API_VERS = '2'
API_URL = 'https://api.betaseries.com'

class cBseries:

    def __init__(self):
        #self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        #self.__sFunctionName = ''


    def getToken(self):
        
        headers = {'Content-Type': 'application/json'}
        post = {'client_id': API_KEY}
        post = json.dumps(post)
        
        
        req = urllib2.Request('https://api.trakt.tv/oauth/device/code', post,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
       # xbmc.log(str(result))
        response.close()
        
        #{"device_code":"a434135042b5a76159628bc974eed2f266fb47df9f438d5738ce40396d531490","user_code":"EBDFD843","verification_url":"https://trakt.tv/activate","expires_in":600,"interval":5}

        total = len(sHtmlContent)
        
        xbmc.log(str(sHtmlContent))

        if (total > 0):
            #self.__Token  = result['token']
            sText = ('Rendez vous sur [COLOR teal]%s[/COLOR] \nEntrer le code [COLOR teal]%s[/COLOR]') % (result['verification_url'], result['user_code'])
            dialog = cConfig().createDialog('vStream')
            dialog.update(0, sText)
            
            for i in range(0, result['expires_in']):
                try:
                    dialog.update(i)
                    time.sleep(1)
                    if dialog.iscanceled():
                        break
                     
                    headers = {'Content-Type': 'application/json'}
                    post = {'client_id': API_KEY, 'client_secret': API_SECRET, 'code': result['device_code']}
                    post = json.dumps(post)
                    
                    req = urllib2.Request('https://api.trakt.tv/oauth/device/token', post,headers)
                    response = urllib2.urlopen(req)
                    sHtmlContent = response.read()
                    result = json.loads(sHtmlContent)
                    response.close()
                    
                    if result['access_token']:
                        cConfig().setSetting('bstoken', str(result['access_token']))
                        break
                
                except:
                    pass
            cConfig().finishDialog(dialog)
            
            #xbmc.executebuiltin("Container.Refresh")
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

            #nom de luser
            headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
            #post = {'client_id': API_KEY, 'client_secret': API_SECRET, 'code': result['device_code']}
            #post = json.dumps(post)
            
            req = urllib2.Request('https://api.trakt.tv/users/me', None,headers)
            response = urllib2.urlopen(req)
            sHtmlContent = response.read()
            result = json.loads(sHtmlContent)
            response.close()
            total = len(sHtmlContent)
            
            #stats user
            req2 = urllib2.Request('https://api.trakt.tv/users/me/stats', None,headers)
            response2 = urllib2.urlopen(req2)
            sHtmlContent2 = response2.read()
            result2 = json.loads(sHtmlContent2)
            response2.close()
            total2 = len(sHtmlContent2)
            #xbmc.log(str(result2))
            
            
            if (total > 0):
                sUsername = result['username']
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'https://')
                oGui.addText(SITE_IDENTIFIER, '[COLOR khaki]Bonjour, '+sUsername+'[/COLOR]', oOutputParameterHandler)
                    
            sTitle = ('Films (%s/%s) regarder pour %s minutes / Series regarder (%s) / Episodes (%s/%s) regarder pour %s minutes') % (result2['movies']['plays'], result2['movies']['watched'], result2['movies']['minutes'], result2['shows']['watched'], result2['episodes']['plays'], result2['episodes']['watched'], result2['episodes']['minutes']) 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oGui.addText(SITE_IDENTIFIER, '[COLOR white]'+sTitle+'[/COLOR]', oOutputParameterHandler)
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'getLists', 'Films', 'mark.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'show')
            oGui.addDir(SITE_IDENTIFIER, 'getLists', 'Séries', 'mark.png', oOutputParameterHandler)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/users/me/history')
            oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Historique', 'mark.png', oOutputParameterHandler)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/users/me/watching')
            oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Actuellement', 'mark.png', oOutputParameterHandler)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.betaseries.com/members/destroy')
            oGui.addDir(SITE_IDENTIFIER, 'getBsout', 'Deconnection', 'mark.png', oOutputParameterHandler)
        

        
        oGui.setEndOfDirectory()  

    def getLists(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')
        
        oGui = cGui()
        
        liste = []
        if sType == 'movie':
            liste.append( ['Collection','https://api.trakt.tv/users/me/collection/movies'] )
            liste.append( ['Surveiller','https://api.trakt.tv/users/me/watchlist/movies'] )
            liste.append( ['Regarder','https://api.trakt.tv/users/me/watched/movies'] )
            liste.append( ['Recommender','https://api.trakt.tv/recommendations/movies'] )
        elif sType == 'show':
            liste.append( ['Collection','https://api.trakt.tv/users/me/collection/shows'] )
            liste.append( ['Surveiller','https://api.trakt.tv/users/me/watchlist/shows'] )
            liste.append( ['Surveiller (saisons)','https://api.trakt.tv/users/me/watchlist/seasons'] )
            liste.append( ['Surveiller (episodes)','https://api.trakt.tv/users/me/watchlist/episodes'] )
            liste.append( ['Regarder','https://api.trakt.tv/users/me/watched/shows'] )
            liste.append( ['Recommender','https://api.trakt.tv/recommendations/shows'] )
                    
        for sTitle,sUrl in liste:
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'getBseries', sTitle, 'genres.png', oOutputParameterHandler)

        
        oGui.setEndOfDirectory()         

    def getBtimeline(self):
        
        
        #self.getToken()
        oGui = cGui()
        
        oInputParameterHandler = cInputParameterHandler()
        userID = oInputParameterHandler.getValue('userID')
        
        #timeline
        oRequestHandler = cRequestHandler('https://api.betaseries.com/timeline/member')
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        oRequestHandler.addParameters('id', userID)
        
        sHtmlContent = oRequestHandler.request();
        result = json.loads(sHtmlContent)
            
        #xbmc.log(str(result))
        
        total = len(sHtmlContent)
        if (total > 0):
            for i in result['events']:
                sHtml = unicodedata.normalize('NFD',  i['html']).encode('ascii', 'ignore').decode("unicode_escape")
                sHtml.encode("utf-8") #on repasse en utf-8
                titre = re.sub('<a href(.+?)>|<\/a>','', sHtml)
                
                xbmc.log(str(i['date']))
                #2016-11-14 09:50:35
                #date = datetime.datetime.strptime("2016-11-14", "%Y-%m-%d")
                date = datetime.datetime(*(time.strptime(i['date'], "%Y-%m-%d %H:%M:%S")[0:6])).strftime('%d-%m-%Y %H:%M')

                
                sTitle = ('%s - %s') % (date, titre)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://')
                oGui.addText(SITE_IDENTIFIER, sTitle, oOutputParameterHandler)
        
        oGui.setEndOfDirectory()              
     
    def getBsout(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
        oGui = cGui()
           
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Key', API_KEY)
        oRequestHandler.addHeaderEntry('X-BetaSeries-Version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', cConfig().getSetting("bstoken"))
        #api buguer normalement รงa affiche que les films et series
        oRequestHandler.addParameters('token', cConfig().getSetting("bstoken"))
        

        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        sHtmlContent = oRequestHandler.request();
        result = json.loads(sHtmlContent)
        total = len(sHtmlContent)
        if (total > 0):
            cConfig().setSetting('bstoken', '')
            oGui.showNofication('Vous avez ?t? d?connect? avec succ?s')
            xbmc.executebuiltin("Container.Refresh")
            
        return
            

    def getBseries(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sType = oInputParameterHandler.getValue('type')
        
        oGui = cGui()
           
        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        #post = {'extended': 'metadata'}
        # post = json.dumps(post)
        
        req = urllib2.Request(sUrl, None,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        xbmc.log(str(result))
        response.close()
        total = len(sHtmlContent)
        
        if (total > 0):
            for i in result:

                if 'collection' in sUrl:
                    if  'show' in i:
                        sTrakt, sTitle, sYear, sTmdb = i['show']['ids']['trakt'], i['show']['title'], i['show']['year'], i['show']['ids']['tmdb']
                    else:
                        sTrakt, sTitle, sYear, sTmdb = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['year'], i['movie']['ids']['tmdb']
                    sTitle = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear)) 
                 
                elif 'history' in sUrl:
                #commun
                    sAction, sType, sWatched_at  = i['action'], i['type'], i['watched_at']
                    #2016-11-16T09:21:18.000Z
                    sDate = datetime.datetime(*(time.strptime(sWatched_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if 'episode' in i:
                        sTrakt, sTitle, sTmdb, sSeason, sNumber = i['episode']['ids']['trakt'], i['episode']['title'], i['episode']['ids']['tmdb'], i['episode']['season'],  i['episode']['number']
                        sExtra = ('(S%sEP%s)') % (sSeason, sNumber)
                    else:
                        sTrakt, sTitle, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['tmdb'], i['movie']['year']
                        sExtra = ('(%s)') % (sYear)  
                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    sTitle = ('[COLOR white]%s - %s %s[/COLOR] - %s %s') % (sDate, sAction, sType, sTitle, sExtra ) 
                    
                elif 'watchlist' in sUrl:
                    #commun
                    sType, sListed_at  = i['type'], i['listed_at']
                    #2016-11-16T09:21:18.000Z
                    sDate = datetime.datetime(*(time.strptime(sListed_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if  'show' in i:
                        sTrakt, sTitle, sYear, sTmdb = i['show']['ids']['trakt'], i['show']['title'], i['show']['year'], i['show']['ids']['tmdb']
                        sExtra = ('(%s)') % (sYear) 
                    elif 'episode' in i:
                        sTrakt, sTitle, sTmdb, sSeason, sNumber = i['episode']['ids']['trakt'], i['episode']['title'], i['episode']['ids']['tmdb'], i['episode']['season'],  i['episode']['number']
                        sExtra = ('(S%sEP%s)') % (sSeason, sNumber)
                    else:
                        sTrakt, sTitle, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['tmdb'], i['movie']['year']
                        sExtra = ('(%s)') % (sYear)  
                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    sTitle = ('[COLOR white]%s - %s[/COLOR] - %s %s') % (sDate, sType, sTitle, sExtra ) 
                
                
                
                else: return
                
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://')
                
                oGuiElement = cGuiElement()
    
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('load')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setIcon("mark.png")
                oGuiElement.setMeta(0)
                #oGuiElement.setThumbnail(sThumb)
                oGuiElement.setTmdb(sTmdb)
                #oGuiElement.setDescription(sDesc)
                #oGuiElement.setFanart(fanart)
                    
                #oGui.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)
                    
                 #oGui.addHost(oGuiElement, oOutputParameterHandler)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
                #oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
               
               
            oGui.setEndOfDirectory()
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
