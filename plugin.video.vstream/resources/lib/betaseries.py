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

POSTER_URL = 'https://image.tmdb.org/t/p/w396'
#FANART_URL = 'https://image.tmdb.org/t/p/w780/'
FANART_URL = 'https://image.tmdb.org/t/p/w1280'

class cBseries:

    CONTENT = '0'

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
  
    def getLoad(self):
        
        #self.getToken()
        oGui = cGui()
        
        if cConfig().getSetting("bstoken") == '':
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'getToken()', '[COLOR khaki]Cliquez ici, pour vous connectez[/COLOR]', 'mark.png', oOutputParameterHandler)
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
            
            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/users/me/watching')
            # oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Actuellement', 'mark.png', oOutputParameterHandler)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/oauth/revoke')
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
            liste.append( ['BoxOffice','https://api.trakt.tv/movies/boxoffice'] )      
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
     
    def getBsout(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
        oGui = cGui()
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        post = {'token': cConfig().getSetting("bstoken")}
        post = json.dumps(post)
        
        req = urllib2.Request(sUrl, post,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        response.close()
        total = len(sHtmlContent)
        
        if (total > 0):
            cConfig().setSetting('bstoken', '')
            oGui.showNofication('Vous avez été déconnecté avec succés')
            xbmc.executebuiltin("Container.Refresh")
            
        return
            

    def getBseries(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
        oGui = cGui()
           
        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        #post = {'extended': 'metadata'}
        # post = json.dumps(post)
        
        req = urllib2.Request(sUrl, None,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        #xbmc.log(str(result))
        
        response.close()
        total = len(sHtmlContent)
        sKey = 0
        if (total > 0):
            for i in result:

                if 'collection' in sUrl:
                    if  'show' in i:
                        sTrakt, sTitle, sYear, sTmdb, sDate = i['show']['ids']['trakt'], i['show']['title'], i['show']['year'], i['show']['ids']['tmdb'], i['last_collected_at']
                        sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                        cBseries.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sYear, sTmdb, sDate = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['year'], i['movie']['ids']['tmdb'], i['collected_at']
                        sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                        cBseries.CONTENT = '1'
                    
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                    sTitle = ('[COLOR white]%s[/COLOR] %s - (%s)') % (sDate, sTitle.encode("utf-8"), int(sYear)) 
                 
                elif 'history' in sUrl:
                #commun
                    sAction, sType, sWatched_at  = i['action'], i['type'], i['watched_at']
                    #2016-11-16T09:21:18.000Z
                    sDate = datetime.datetime(*(time.strptime(sWatched_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if 'episode' in i:
                        sTrakt, sTitle, sTmdb, sSeason, sNumber = i['episode']['ids']['trakt'], i['episode']['title'], i['episode']['ids']['tmdb'], i['episode']['season'],  i['episode']['number']
                        sExtra = ('(S%sEP%s)') % (sSeason, sNumber)
                        cBseries.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['tmdb'], i['movie']['year']
                        sExtra = ('(%s)') % (sYear)
                        cBseries.CONTENT = '1'
                    
                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), sExtra)
                    sTitle = ('[COLOR white]%s - %s %s[/COLOR] - %s %s') % (sDate, sAction, sType, sTitle, sExtra ) 
                    
                    
                elif 'watchlist' in sUrl:
                    #commun
                    sType, sListed_at  = i['type'], i['listed_at']
                    #2016-11-16T09:21:18.000Z
                    sDate = datetime.datetime(*(time.strptime(sListed_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if  'show' in i:
                        sTrakt, sTitle, sYear, sTmdb = i['show']['ids']['trakt'], i['show']['title'], i['show']['year'], i['show']['ids']['tmdb']
                        sExtra = ('(%s)') % (sYear)
                        cBseries.CONTENT = '2'
                    elif 'episode' in i:
                        sTrakt, sTitle, sTmdb, sSeason, sNumber = i['episode']['ids']['trakt'], i['episode']['title'], i['episode']['ids']['tmdb'], i['episode']['season'],  i['episode']['number']
                        sExtra = ('(S%sEP%s)') % (sSeason, sNumber)
                        cBseries.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['tmdb'], i['movie']['year']
                        sExtra = ('(%s)') % (sYear)  
                        cBseries.CONTENT = '1'
                    
                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), sExtra)
                    sTitle = ('[COLOR white]%s - %s[/COLOR] - %s %s') % (sDate, sType, sTitle, sExtra ) 
                    
                    
                elif 'watched' in sUrl:
                #commun
                    sLast_watched_at, sPlays  = i['last_watched_at'], i['plays']
                    #2016-11-16T09:21:18.000Z
                    sDate = datetime.datetime(*(time.strptime(sLast_watched_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if  'show' in i:
                        sTrakt, sTitle, sYear, sTmdb = i['show']['ids']['trakt'], i['show']['title'], i['show']['year'], i['show']['ids']['tmdb']
                        cBseries.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['tmdb'], i['movie']['year'] 
                        cBseries.CONTENT = '1'
                    
                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), sYear)
                    sTitle = ('[COLOR white]%s - %s Lectures[/COLOR] - %s (%s)') % (sDate, sPlays, sTitle, sYear ) 
                    
                
                elif 'recommendations' in sUrl:
                    if 'shows' in sUrl:
                        cBseries.CONTENT = '2'
                    else :
                        cBseries.CONTENT = '1'
                    sTrakt, sTitle, sYear, sTmdb = i['ids']['trakt'], i['title'], i['year'], i['ids']['tmdb']
                    sTitle = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear)) 
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear)) 
                    
                    
                elif 'boxoffice' in sUrl:
                        sTrakt, sTitle, sYear, sTmdb, sRevenue = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['year'], i['movie']['ids']['tmdb'], i['revenue']
                        cBseries.CONTENT = '1'
                        sTitle = ('Revenues [COLOR white](%s)[/COLOR] - %s - (%s)') % (sRevenue, sTitle.encode("utf-8"), int(sYear)) 
                        sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear)) 
                
             
                else: return
            
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('title', sFile)
                oOutputParameterHandler.addParameter('key', sKey)
                self.getFolder(oGui, sTitle, 'getBseasons', sTmdb, oOutputParameterHandler)    
                sKey += 1
        oGui.setEndOfDirectory()
        return
        
    def getBseasons(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('title')
        sKey = oInputParameterHandler.getValue('key')
        
        oGui = cGui()
           
        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        #post = {'extended': 'metadata'}
        # post = json.dumps(post)
        
        req = urllib2.Request(sUrl, None,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        
        response.close()
        total = len(sHtmlContent)
        
        oGui = cGui()
        xbmc.log(str(sKey))
        total = len(result)
        sNum = 0
        if (total > 0):
            for i in result[int(sKey)]['seasons']:

                if 'collection' in sUrl or 'watched' in sUrl:
                    sNumber = i['number']
                    cBseries.CONTENT = '2'
                else: return
                   
                sTitle2 = ('%s - (S%s)') % (sTitle.encode("utf-8"), int(sNumber)) 
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('Key', sKey)
                oOutputParameterHandler.addParameter('sNum', sNum)
                self.getFolder(oGui, sTitle2, 'getBepisodes', '', oOutputParameterHandler)  
                sNum += 1

        oGui.setEndOfDirectory()
        return
        
    def getBepisodes(self):
    
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('title')
        sKey = oInputParameterHandler.getValue('key')
        sNum = oInputParameterHandler.getValue('sNum')
        
        oGui = cGui()
        cBseries.CONTENT = '2'   
        
        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        #post = {'extended': 'metadata'}
        # post = json.dumps(post)
        
        req = urllib2.Request(sUrl, None,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        
        response.close()
        total = len(sHtmlContent)
        
        oGui = cGui()
        xbmc.log(str(sKey))
        total = len(result)
        if (total > 0):
            for i in result[int(sKey)]['seasons'][int(sNum)]['episodes']:

                if 'collection' in sUrl:
                    sNumber, sDate = i['number'],  i['collected_at']
                    sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    
                    sTitle2 = ('[COLOR white]%s [/COLOR] %s - (ep%s)') % (sDate, sTitle.encode("utf-8"), int(sNumber)) 
                    
                elif 'watched' in sUrl:
                    sNumber, sPlays, sDate = i['number'], i['plays'], i['last_watched_at']
                    sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')

                    sTitle2 = ('[COLOR white]%s - %s Lectures[/COLOR] - %s (ep%s)') % (sDate, sPlays, sTitle.encode("utf-8"), int(sNumber)) 
                        
                else: return
                   
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                #oOutputParameterHandler.addParameter('Key', skey)
                self.getFolder(oGui, sTitle2, 'load', '', oOutputParameterHandler)    

        oGui.setEndOfDirectory()
        return
      
    def getFolder(self, oGui, sTitle, sFunction, sTmdb, oOutputParameterHandler):

        oGuiElement = cGuiElement()

        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sTitle)
        oGuiElement.setFileName(sTitle)
        oGuiElement.setIcon("mark.png")
        #oGuiElement.setThumbnail(sThumb)
        oGuiElement.setTmdb(sTmdb)
        oGuiElement.setImdbId(sTmdb)
        #xbmc.log(str(cBseries.CONTENT))
        # if cBseries.CONTENT == '2':
            # oGuiElement.setMeta(2)
        # else:
            # oGuiElement.setMeta(1)
            
        #oGuiElement.setDescription(sDesc)
        #oGuiElement.setFanart(fanart)
            
        #oGui.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)
            
         #oGui.addHost(oGuiElement, oOutputParameterHandler)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
        #oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
       
       
        
        
    def getTmdb(self, sTmdb):
        
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addParameters('api_key', '92ab39516970ab9d86396866456ec9b6')
        oRequestHandler.addParameters('language', 'fr')

        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)
    
        total = len(sHtmlContent)
        if (total > 0):
        
            xbmc.log(str(result))
        
        return
