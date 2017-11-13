#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.db import cDb
from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler


import urllib, urllib2, re
import xbmc, xbmcgui
import time, md5 ,math
import unicodedata

import datetime, time

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'cTrakt'
SITE_NAME = 'Trakt'

API_KEY = '7139b7dace25c7bdf0bd79acf46fb02bd63310548b1f671d88832f75a4ac3dd6'
API_SECRET = 'bb02b2b0267b045590bc25c21dac21b1c47446a62b792091b3275e9c4a943e74'
API_VERS = '2'

POSTER_URL = 'https://image.tmdb.org/t/p/w396'
#FANART_URL = 'https://image.tmdb.org/t/p/w780/'
FANART_URL = 'https://image.tmdb.org/t/p/w1280'

MAXRESULT = 10

class cTrakt:

    CONTENT = '0'

    def __init__(self):
        #self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        self.__sAction = ''
        self.__sType = ''
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

        if (total > 0):
            #self.__Token  = result['token']
            sText = (cConfig().getlanguage(30304)) % (result['verification_url'], result['user_code'])
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
                        cGui().showNofication(cConfig().getlanguage(30000))
                        return

                except:
                    pass
            cConfig().finishDialog(dialog)

            #xbmc.executebuiltin("Container.Refresh")
            return
        return

    def search(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://')
        oOutputParameterHandler.addParameter('type', 'movie')
        oGui.addDir('themoviedb_org', 'showSearchMovie', 'Recherche de film', 'films.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://')
        oOutputParameterHandler.addParameter('type', 'show')
        oGui.addDir('themoviedb_org', 'showSearchSerie', 'Recherche de serie', 'series.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def getLoad(self):
        #pour regen le token()
        #self.getToken()
        oGui = cGui()


        if cConfig().getSetting("bstoken") == '':
            xbmc.log('er')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'getToken()', cConfig().getlanguage(30305), 'trakt.png', oOutputParameterHandler)
        else:
            #nom de luser
            headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
            #post = {'client_id': API_KEY, 'client_secret': API_SECRET, 'code': result['device_code']}
            #post = json.dumps(post)

            try:
                req = urllib2.Request('https://api.trakt.tv/users/me', None,headers)
                response = urllib2.urlopen(req)
            except:
                return self.getToken()
            sHtmlContent = response.read()
            result = json.loads(sHtmlContent)
            response.close()
            total = len(sHtmlContent)


            if (total > 0):
                sUsername = result['username']
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'https://')
                oGui.addText(SITE_IDENTIFIER, (cConfig().getlanguage(30306)) % (sUsername))


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'search', cConfig().getlanguage(30330), 'search.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'getLists', cConfig().getlanguage(30120), 'films.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'show')
            oGui.addDir(SITE_IDENTIFIER, 'getLists', cConfig().getlanguage(30121), 'series.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/users/me/history')
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', cConfig().getlanguage(30308), 'trakt.png', oOutputParameterHandler)

            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/users/me/watching')
            # oGui.addDir(SITE_IDENTIFIER, 'getBseries', 'Actuellement', 'mark.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/oauth/revoke')
            oGui.addDir(SITE_IDENTIFIER, 'getCalendrier', cConfig().getlanguage(30331), 'trakt.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://api.trakt.tv/oauth/revoke')
            oGui.addDir(SITE_IDENTIFIER, 'getBsout', cConfig().getlanguage(30309), 'trakt.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    #def search(self):
        # oGui = cGui()
        # sSearchText = oGui.showKeyBoard()
        # if (sSearchText != False):
            # oInputParameterHandler = cInputParameterHandler()
            # sType = oInputParameterHandler.getValue('type')
            # sUrl = 'https://api.trakt.tv/search/' + sType + '?query=' + urllib.quote_plus(sSearchText)
            # self.getTrakt(sUrl)
            # return
        # oGui.setEndOfDirectory()

    def getCalendrier(self):
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

        oGui = cGui()

        today_date = str(datetime.datetime.now().date())

        #DANGER ca rame, freeze
        liste = []
        liste.append( ['Mes sorties sur les 7 jours a venir','https://api.trakt.tv/calendars/my/shows/' + today_date + '/7'] )
        liste.append( ['Mes sorties sur les 30 jours a venir','https://api.trakt.tv/calendars/my/shows/' + today_date + '/30'] )
        liste.append( ['Nouveautes sur 7 jours','https://api.trakt.tv/calendars/all/shows/new/' + today_date + '/7'] )
        #liste.append( ['Freeze - Nouveautees sur la journee a venir','https://api.trakt.tv/calendars/all/shows/' + today_date + '/1'] )

        for sTitle,sUrl in liste:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def getLists(self):

        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')


        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        #stats user
        req2 = urllib2.Request('https://api.trakt.tv/users/me/stats', None,headers)
        response2 = urllib2.urlopen(req2)
        sHtmlContent2 = response2.read()
        result2 = json.loads(sHtmlContent2)
        response2.close()
        total2 = len(sHtmlContent2)



        oGui = cGui()

        liste = []
        if sType == 'movie':
            liste.append( [ '%s (%s)' % (cConfig().getlanguage(30310), result2['movies']['collected'] ),'https://api.trakt.tv/users/me/collection/movies?page=1&limit=' + str(MAXRESULT)] )
            liste.append( [cConfig().getlanguage(30311),'https://api.trakt.tv/users/me/watchlist/movies?page=1&limit=' + str(MAXRESULT) ] )
            liste.append( ['%s (%s)' % (cConfig().getlanguage(30312), result2['movies']['watched'] ),'https://api.trakt.tv/users/me/watched/movies?page=1&limit=' + str(MAXRESULT)] )
            liste.append( [cConfig().getlanguage(30313),'https://api.trakt.tv/recommendations/movies'] )
            liste.append( [cConfig().getlanguage(30314),'https://api.trakt.tv/movies/boxoffice'] )
            liste.append( [cConfig().getlanguage(30315),'https://api.trakt.tv/movies/popular'] )
            liste.append( [cConfig().getlanguage(30316),'https://api.trakt.tv/movies/played/weekly'] )
            liste.append( [cConfig().getlanguage(30317),'https://api.trakt.tv/movies/played/monthly'] )
            #liste.append( ['historique de Films','https://api.trakt.tv/users/me/history/movies'] )

        elif sType == 'show':
            liste.append( ['%s (%s)' % (cConfig().getlanguage(30310), result2['shows']['collected'] ),'https://api.trakt.tv/users/me/collection/shows?page=1&limit=' + str(MAXRESULT)] )
            liste.append( [cConfig().getlanguage(30311),'https://api.trakt.tv/users/me/watchlist/shows?page=1&limit=' + str(MAXRESULT) ] )
            liste.append( [cConfig().getlanguage(30318),'https://api.trakt.tv/users/me/watchlist/seasons?page=1&limit=' + str(MAXRESULT)] )
            liste.append( [cConfig().getlanguage(30319),'https://api.trakt.tv/users/me/watchlist/episodes?page=1&limit=' + str(MAXRESULT)] )
            liste.append( ['%s (%s)' % (cConfig().getlanguage(30312), result2['movies']['watched'] ),'https://api.trakt.tv/users/me/watched/shows?page=1&limit=' + str(MAXRESULT)] )
            liste.append( [cConfig().getlanguage(30313),'https://api.trakt.tv/recommendations/shows'] )
            liste.append( [cConfig().getlanguage(30315),'https://api.trakt.tv/shows/popular'] )
            liste.append( [cConfig().getlanguage(30316),'https://api.trakt.tv/shows/played/weekly'] )
            liste.append( [cConfig().getlanguage(30317),'https://api.trakt.tv/shows/played/monthly'] )
            #liste.append( ['Historique de séries','https://api.trakt.tv/users/me/history/shows'] )

        for sTitle,sUrl in liste:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'genres.png', oOutputParameterHandler)


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
            oGui.showNofication(cConfig().getlanguage(30320))
            xbmc.executebuiltin("Container.Refresh")

        return


    def getTrakt(self,url2 = None):

        oInputParameterHandler = cInputParameterHandler()
        if url2:
            sUrl = url2
        else:
            sUrl = oInputParameterHandler.getValue('siteUrl')

        oGui = cGui()

        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}
        #post = {'extended': 'metadata'}
        # post = json.dumps(post)
        req = urllib2.Request(sUrl, None,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        sHeaders = response.headers
        response.close()

        result = json.loads(sHtmlContent)

        #xbmc.log(str(result))

        sPage = '1'
        sMaxPage = '1'
        if 'X-Pagination-Page' in sHeaders:
            sPage = sHeaders['X-Pagination-Page']
        if 'X-Pagination-Page-Count' in sHeaders:
            sMaxPage = sHeaders['X-Pagination-Page-Count']

        total = len(result)
        sKey = 0
        sFunction = 'getLoad'
        sId = SITE_IDENTIFIER
        searchtext = ''
        if (total > 0):
            dialog = cConfig().createDialog(SITE_NAME)
            for i in result:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break

                if 'collection' in sUrl:
                    if  'show' in i:
                        sTrakt, sTitle, sYear, sImdb, sTmdb, sDate = i['show']['ids']['trakt'], i['show']['title'], i['show']['year'], i['show']['ids']['imdb'], i['show']['ids']['tmdb'], i['last_collected_at']
                        #sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                        cTrakt.CONTENT = '2'
                        sFunction = 'getBseasons'
                    else:
                        sTrakt, sTitle, sYear, sImdb, sTmdb, sDate = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['year'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['collected_at']
                        #sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    searchtext = ('%s') % (sTitle.encode("utf-8"))

                    if sYear:
                        sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                        sTitle = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                    else:
                        sFile = ('%s') % (sTitle.encode("utf-8"))
                        sTitle = ('%s') % (sTitle.encode("utf-8"))

                elif 'history' in sUrl:
                #commun
                    sAction, sType, sWatched_at  = i['action'], i['type'], i['watched_at']
                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    #2016-11-16T09:21:18.000Z
                    #sDate = datetime.datetime(*(time.strptime(sWatched_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y')
                    if 'episode' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sSeason, sNumber = i['episode']['ids']['trakt'], i['episode']['title'], i['episode']['ids']['imdb'], i['episode']['ids']['tmdb'], i['episode']['season'],  i['episode']['number']
                        sExtra = ('(S%02dE%02d)') % (sSeason, sNumber)
                        cTrakt.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['movie']['year']
                        sExtra = ('(%s)') % (sYear)
                        cTrakt.CONTENT = '1'

                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), sExtra)
                    sTitle = ('%s %s - %s %s') % (sAction, sType, sTitle, sExtra)


                elif 'watchlist' in sUrl:
                    #commun
                    sType, sListed_at  = i['type'], i['listed_at']
                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    #2016-11-16T09:21:18.000Z
                    #sDate = datetime.datetime(*(time.strptime(sListed_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if  'show' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['show']['ids']['trakt'], i['show']['title'], i['show']['ids']['imdb'], i['show']['ids']['tmdb'], i['show']['year']
                        sExtra = ('(%s)') % (sYear)
                        cTrakt.CONTENT = '2'
                    elif 'episode' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sSeason, sNumber = i['episode']['ids']['trakt'], i['episode']['title'], i['episode']['ids']['imdb'], i['episode']['ids']['tmdb'], i['episode']['season'],  i['episode']['number']
                        sExtra = ('(S%02dE%02d)') % (sSeason, sNumber)
                        cTrakt.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['movie']['year']
                        sExtra = ('(%s)') % (sYear)
                        cTrakt.CONTENT = '1'

                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s %s') % (sTitle.encode("utf-8"), sExtra)
                    sTitle = ('%s %s') % (sTitle, sExtra )


                elif 'watched' in sUrl:
                #commun
                    sLast_watched_at, sPlays  = i['last_watched_at'], i['plays']
                    #2016-11-16T09:21:18.000Z
                    #sDate = datetime.datetime(*(time.strptime(sLast_watched_at, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')
                    if  'show' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['show']['ids']['trakt'], i['show']['title'], i['show']['ids']['imdb'], i['show']['ids']['tmdb'], i['show']['year']
                        cTrakt.CONTENT = '2'
                        sFunction = 'getBseasons'
                    else:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['movie']['year']
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s - %s') % (sTitle.encode("utf-8"), sYear)
                    sTitle = ('%s Lectures - %s (%s)') % (sPlays, sTitle, sYear )

                elif 'played' in sUrl:
                #commun
                    sWatcher_count, sPlay_count, sCollected_count = i['watcher_count'], i['play_count'], i['collected_count']
                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    if  'show' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['show']['ids']['trakt'], i['show']['title'], i['show']['ids']['imdb'], i['show']['ids']['tmdb'], i['show']['year']
                        cTrakt.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['movie']['year']
                        cTrakt.CONTENT = '1'
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                    sTitle = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))

                elif 'calendars' in sUrl:
                    #xbmc.log(str(i))
                    #sRajout = ''
                    if  'show' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sYear, sFirst_aired = i['show']['ids']['trakt'], i['show']['title'], i['show']['ids']['imdb'], i['show']['ids']['tmdb'], i['show']['year'],i['first_aired']
                        sSaison,sEpisode = i['episode']['season'],i['episode']['number']
                        #sRajout = " S" + str(sSaison) + "E" + str(sEpisode)
                        cTrakt.CONTENT = '2'
                    else:
                        sTrakt, sTitle, sImdb, sTmdb, sYear, sFirst_aired  = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['movie']['year'],i['first_aired']
                        cTrakt.CONTENT = '1'

                    sDate = datetime.datetime(*(time.strptime(sFirst_aired, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y')
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), sYear)
                    sTitle = ('%s - %s (S%02dE%02d)') % (sDate, sTitle.encode('utf-8').decode('ascii','ignore'), sSaison,sEpisode)

                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif 'search' in sUrl:
                    if  'show' in i:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['show']['ids']['trakt'], i['show']['title'], i['show']['ids']['imdb'], i['show']['ids']['tmdb'], i['show']['year']
                        cTrakt.CONTENT = '2'
                        sFunction = 'getBseasons'
                    else:
                        sTrakt, sTitle, sImdb, sTmdb, sYear = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['movie']['year']
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    sTitle = unicodedata.normalize('NFD',  sTitle).encode('ascii', 'ignore').decode("unicode_escape")
                    sTitle.encode("utf-8")
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), sYear)
                    sTitle = ('%s (%s)') % ( sTitle, sYear )

                elif 'recommendations' in sUrl or 'popular' in sUrl:
                    if 'shows' in sUrl:
                        cTrakt.CONTENT = '2'
                    else :
                        cTrakt.CONTENT = '1'
                    sTrakt, sTitle, sYear, sImdb, sTmdb = i['ids']['trakt'], i['title'], i['year'], i['ids']['imdb'], i['ids']['tmdb']
                    searchtext = ('%s') % (sTitle.encode("utf-8"))
                    sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                    sTitle = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif 'boxoffice' in sUrl:
                        sTrakt, sTitle, sYear, sImdb, sTmdb, sRevenue = i['movie']['ids']['trakt'], i['movie']['title'], i['movie']['year'], i['movie']['ids']['imdb'], i['movie']['ids']['tmdb'], i['revenue']
                        cTrakt.CONTENT = '1'
                        searchtext = ('%s') % (sTitle.encode("utf-8"))
                        sFile = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                        sTitle = ('%s - (%s)') % (sTitle.encode("utf-8"), int(sYear))
                        sFunction = 'showSearch'
                        sId = 'globalSearch'


                else: return

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('file', sFile)
                oOutputParameterHandler.addParameter('key', sKey)
                oOutputParameterHandler.addParameter('searchtext', searchtext)
                self.getFolder(oGui, sId, sTitle, sFile, sFunction, sImdb, sTmdb, oOutputParameterHandler)
                sKey += 1

            cConfig().finishDialog(dialog)

            if (sPage < sMaxPage):
                sNextPage = sUrl.replace('page=' + str(sPage),'page=' + str(int(sPage)+1))
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addDir(SITE_IDENTIFIER, 'getTrakt', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
        return

    def getBseasons(self):

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sFile = oInputParameterHandler.getValue('file')
        sKey = oInputParameterHandler.getValue('key')
        searchtext = oInputParameterHandler.getValue('searchtext')

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

        total = len(result)
        sNum = 0
        if (total > 0):
            for i in result[int(sKey)]['seasons']:

                if 'collection' in sUrl or 'watched' in sUrl:
                    sNumber = i['number']
                    cTrakt.CONTENT = '2'
                else: return

                sTitle2 = ('%s - (S%02d)') % (sFile.encode("utf-8"), int(sNumber))
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('Key', sKey)
                oOutputParameterHandler.addParameter('sNum', sNum)
                oOutputParameterHandler.addParameter('file', sFile)
                oOutputParameterHandler.addParameter('title', sTitle2)
                oOutputParameterHandler.addParameter('searchtext', searchtext)
                self.getFolder(oGui, SITE_IDENTIFIER, sTitle2, sFile, 'getBepisodes', '','' ,oOutputParameterHandler)
                sNum += 1

        oGui.setEndOfDirectory()
        return

    def getBepisodes(self):

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('title')
        sFile = oInputParameterHandler.getValue('file')
        sKey = oInputParameterHandler.getValue('key')
        sNum = oInputParameterHandler.getValue('sNum')
        searchtext = oInputParameterHandler.getValue('searchtext')

        oGui = cGui()
        cTrakt.CONTENT = '2'

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
        #xbmc.log(str(sKey))
        total = len(result)
        if (total > 0):
            for i in result[int(sKey)]['seasons'][int(sNum)]['episodes']:

                if 'collection' in sUrl:
                    sNumber, sDate = i['number'],  i['collected_at']
                    #sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')

                    sTitle2 = ('%s (E%02d)') % (sTitle.encode("utf-8"), int(sNumber))

                elif 'watched' in sUrl:
                    sNumber, sPlays, sDate = i['number'], i['plays'], i['last_watched_at']
                    #sDate = datetime.datetime(*(time.strptime(sDate, "%Y-%m-%dT%H:%M:%S.%fZ")[0:6])).strftime('%d-%m-%Y %H:%M')

                    sTitle2 = ('%s Lectures - %s(E%02d)') % (sPlays, sTitle.encode("utf-8"), int(sNumber))

                else: return

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('file', sFile)
                #oOutputParameterHandler.addParameter('Key', skey)
                oOutputParameterHandler.addParameter('searchtext', searchtext)
                self.getFolder(oGui, 'globalSearch', sTitle2, sFile, 'showSearch', '', '', oOutputParameterHandler)

        oGui.setEndOfDirectory()
        return

    def getFolder(self, oGui, sId, sTitle, sFile, sFunction, sImdb, sTmdb, oOutputParameterHandler):

        oGuiElement = cGuiElement()

        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sTitle)
        oGuiElement.setFileName(sFile)
        oGuiElement.setIcon("trakt.png")

        #oGuiElement.setThumbnail(sThumb)
        oGuiElement.setImdbId(sImdb)
        oGuiElement.setTmdbId(sTmdb)

        if cConfig().getSetting("meta-view") == 'false':
            #self.getTmdbInfo(sTmdb, oGuiElement)
            oGuiElement.setMetaAddon('true')

        #xbmc.log(str(cTrakt.CONTENT))
        if cTrakt.CONTENT == '2':
            oGuiElement.setMeta(2)
            oGuiElement.setCat(2)
            cGui.CONTENT = "tvshows"
        else:
            oGuiElement.setMeta(1)
            oGuiElement.setCat(1)
            cGui.CONTENT = "movies"

        #oGuiElement.setDescription(sDesc)
        #oGuiElement.setFanart(fanart)

        #oGui.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)

         #oGui.addHost(oGuiElement, oOutputParameterHandler)
        self.createContexTrakt(oGui, oGuiElement, oOutputParameterHandler)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
        #oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)


    def getContext(self):

        import xbmcgui
        disp = ['https://api.trakt.tv/sync/collection/','https://api.trakt.tv/sync/history','https://api.trakt.tv/sync/watchlist']
        dialog2 = xbmcgui.Dialog()
        dialog_select = cConfig().getlanguage(30321), cConfig().getlanguage(30322), cConfig().getlanguage(30323)

        ret = dialog2.select('Trakt',dialog_select)

        if ret > -1:
            self.__sAction = disp[ret]
        return self.__sAction

    def getType(self):

        import xbmcgui
        disp = ['movies','shows']
        dialog2 = xbmcgui.Dialog()
        dialog_select = 'Films', 'Series'

        ret = dialog2.select('Trakt',dialog_select)

        if ret > -1:
            self.__sType = disp[ret]
        return self.__sType

    def getAction2(self):
        sAction = 'https://api.trakt.tv/search/movie?query=tron'
        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS}

        req = urllib2.Request(sAction, None ,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        xbmc.log(str(result))
        for i in result:
            xbmc.log(str(i['movie']['title'].encode('utf-8')) + '=' + str(i['movie']['ids']['imdb']))

    def getAction(self):

        if cConfig().getSetting("bstoken") == "":
            cGui().showNofication("Vous devez être connecté")
            return

        oInputParameterHandler = cInputParameterHandler()

        sAction = oInputParameterHandler.getValue('sAction')
        if not sAction:
            sAction = self.getContext()
        if not sAction:
            return

        #xbmc.log(str(oInputParameterHandler.getAllParameter()))

        sType = oInputParameterHandler.getValue('sType')
        if not sType:
            sType = self.getType()
        #entrer imdb ? venant d'ou?
        sImdb = oInputParameterHandler.getValue('sImdbId')
        sTMDB = oInputParameterHandler.getValue('sTmdbId')
        sSeason = oInputParameterHandler.getValue('sSeason')
        sEpisode = oInputParameterHandler.getValue('sEpisode')

        if not sImdb:
            sPost = {}
            if not sTMDB:
                sTMDB = int(self.getTmdbID(oInputParameterHandler.getValue('sMovieTitle'),sType))

            sPost = {sType: [ {"ids": {"tmdb": sTMDB}} ]}
            if sSeason:
                sPost = {sType: [ {"ids": {"tmdb": sTMDB} , "seasons": [ { "number": int(sSeason) }] } ]}
            if sEpisode:
                sPost = {sType: [ {"ids": {"tmdb": sTMDB} , "seasons": [ { "number": int(sSeason) , "episodes": [ { "number": int(sEpisode) } ] } ] } ]}
        else:
            sPost = {sType: [{"ids": {"imdb": sImdb}}]}

        headers = {'Content-Type': 'application/json', 'trakt-api-key': API_KEY, 'trakt-api-version': API_VERS, 'Authorization': 'Bearer %s' % cConfig().getSetting("bstoken")}

        sPost = json.dumps(sPost)

        req = urllib2.Request(sAction, sPost,headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        result = json.loads(sHtmlContent)
        #xbmc.log(str(result))

        sText = "Erreur"
        try:
            if result["added"]['movies'] == 1 or result["added"]['episodes'] > 0 or result["added"]['shows'] > 0:
                sText = "Ajouté avec succes"
        except: pass

        try:
            if result["updated"]['movies'] == 1 or result["updated"]['episodes'] > 0 or result["updated"]['shows'] > 0:
                sText = "Mise à jour avec succes"
        except: pass

        try:
            if result["deleted"]['movies'] == 1 or result["deleted"]['episodes'] > 0:
                sText = 'Supprimé avec succes'
        except: pass

        try:
            if result["existing"]['movies'] >0  or result["existing"]['episodes'] > 0 or result["existing"]['seasons'] > 0  or result["existing"]['shows'] > 0:
                sText = 'Entree deja presente'
        except: pass

        cGui().showNofication(sText)

        #{u'not_found': {u'movies': [], u'seasons': [], u'people': [], u'episodes': [], u'shows': []}, u'updated': {u'movies': 0, u'episodes': 0}, u'added': {u'movies': 1, u'episodes': 0}, u'existing': {u'movies': 0, u'episodes': 0}}
        #{u'deleted': {u'movies': 0, u'episodes': 55}, u'not_found': {u'movies': [], u'seasons': [], u'people': [], u'episodes': [], u'shows': []}}

        if (oInputParameterHandler.exist('sReload')):
            xbmc.executebuiltin("Container.Refresh")
        return

    def createContexTrakt(self, oGui, oGuiElement, oOutputParameterHandler= ''):

        liste = []
        liste.append( ['[COLOR teal]Ajouter: '+cConfig().getlanguage(30310)+'[/COLOR]','https://api.trakt.tv/sync/collection'] )
        liste.append( ['[COLOR red]Supprimer: '+cConfig().getlanguage(30310)+'[/COLOR]','https://api.trakt.tv/sync/collection/remove'] )
        liste.append( ['[COLOR teal]Ajouter: '+cConfig().getlanguage(30311)+'[/COLOR]','https://api.trakt.tv/sync/watchlist'] )
        liste.append( ['[COLOR red]Supprimer: '+cConfig().getlanguage(30311)+'[/COLOR]','https://api.trakt.tv/sync/watchlist/remove'] )
        liste.append( ['[COLOR teal]Ajouter: '+cConfig().getlanguage(30312)+'[/COLOR]','https://api.trakt.tv/sync/history'] )
        liste.append( ['[COLOR red]Supprimer: '+cConfig().getlanguage(30312)+'[/COLOR]','https://api.trakt.tv/sync/history/remove'] )
        for sTitle,sUrl in liste:
            oOutputParameterHandler = cOutputParameterHandler()
            if cTrakt.CONTENT == '2':
                oOutputParameterHandler.addParameter('sType', 'shows')
            else:
                oOutputParameterHandler.addParameter('sType', 'movies')
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sAction', sUrl)
            oOutputParameterHandler.addParameter('sReload', True)
            #oOutputParameterHandler.addParameter('sImdb', oGuiElement.getImdbId())
            oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cTrakt','cTrakt','getAction',sTitle)
        return

    def showHosters(self):

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sMovieTitle = oInputParameterHandler.getValue('file')
        #sThumbnail = oInputParameterHandler.getValue('sThumbnail')
        #ancien decodage
        sMovieTitle = unicode(sMovieTitle, 'utf-8')#converti en unicode pour aider aux convertions
        sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'replace').decode("unicode_escape")#vire accent et '\'
        sMovieTitle = sMovieTitle.encode("utf-8").lower() #on repasse en utf-8

        sMovieTitle = urllib.quote(sMovieTitle)

        sMovieTitle = re.sub('\(.+?\)',' ', sMovieTitle) #vire les tags entre parentheses

        #modif venom si le titre comporte un - il doit le chercher
        sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle) #vire les caracteres a la con qui peuvent trainer

        sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)',' ', sMovieTitle) #vire les articles

        sMovieTitle = re.sub(' +',' ',sMovieTitle) #vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +


        dialog3 = xbmcgui.Dialog()
        ret = dialog3.select('Selectionner un Moteur de Recherche',['Vstream (Fiable mais plus complexe)','Alluc (Simple mais resultats non garantis)'])

        if ret == 0:
            self.VstreamSearch(sMovieTitle)
        elif ret == 1:
            #AllucSearch(sMovieTitle + sExtraTitle)
            #modif test préfére les accent supprimer é = e
            sMovieTitle = sMovieTitle.replace('%C3%A9','e').replace('%C3%A0','a')
            self.AllucSearch(sMovieTitle)

    def VstreamSearch(self, sMovieTitle):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oHandler = cRechercheHandler()
        oHandler.setText(sMovieTitle)
        #oHandler.setDisp(sDisp)
        aPlugins = oHandler.getAvailablePlugins()

        oGui.setEndOfDirectory()

    def AllucSearch(self, sMovieTitle):
        oGui = cGui()

        exec "from resources.sites import alluc_ee as search"
        sUrl = 'http://www.alluc.ee/stream/lang%3Afr+' + sMovieTitle
        #xbmc.log(str(sUrl))
        searchUrl = "search.%s('%s')" % ('showMovies', sUrl)
        exec searchUrl

        oGui.setEndOfDirectory()

    def getTmdbInfo(self, sTmdb, oGuiElement):

        return

        if not sTmdb:
            xbmc.log('Probleme sTmdb')
            return

        oRequestHandler = cRequestHandler('https://api.themoviedb.org/3/movie/'+str(sTmdb))
        oRequestHandler.addParameters('api_key', '92ab39516970ab9d86396866456ec9b6')
        oRequestHandler.addParameters('language', 'fr')

        sHtmlContent = oRequestHandler.request()

        try:
            #xbmc.log(sHtmlContent)
            result = json.loads(sHtmlContent)
            #xbmc.log(str(result))
        except:
            return

        total = len(sHtmlContent)
        #format
        meta = {}
        meta['imdb_id'] = result['id']
        meta['title'] = result['title']
        meta['tagline'] = result['tagline']
        meta['rating'] = result['vote_average']
        meta['votes'] = result['vote_count']
        meta['duration'] = result['runtime']
        meta['plot'] = result['overview']
        #meta['mpaa'] = result['certification']
        #meta['premiered'] = result['released']
        #meta['director'] = result['director']
        #meta['writer'] = result['writer']
        # if (total > 0):
        if result['poster_path']:
            oGuiElement.setThumbnail('https://image.tmdb.org/t/p/w396'+result['poster_path'])
        if result['backdrop_path']:
            oGuiElement.setFanart('https://image.tmdb.org/t/p/w1280'+result['backdrop_path'])

        for key, value in meta.items():
            oGuiElement.addItemValues(key, value)

        return
    def getTmdbID(self,sTitle,sType):

        oInputParameterHandler = cInputParameterHandler()

        from resources.lib.tmdb import cTMDb
        grab = cTMDb(api_key=cConfig().getSetting('api_tmdb'))

        if sType == 'show' or sType == 'shows':
            sType = 'tv'

        if sType == 'movies':
            sType = 'movie'

        meta = 0
        annee = ''
        #on cherche l'annee
        r = re.search('(\([0-9]{4}\))', sTitle)
        if r:
            annee = str(r.group(0))
            sTitle = sTitle.replace(annee,'')

        # xbmc.log('Recherche de : ' + sTitle)
        # xbmc.log('Saison/episode : ' + SaisonEpisode)
        # xbmc.log('Annee : ' + annee)
        # xbmc.log('Type : ' + sType)

        meta = grab.get_idbyname(oInputParameterHandler.getValue('sFileName'), annee, sType)

        return int(meta)

    def getTmdbID_old(self,sTitle,sType):

        if sType == 'show' or sType == 'shows':
            sType = 'tv'

        if sType == 'movies':
            sType = 'movie'

        ret = 0
        SaisonEpisode = ''
        annee = ''

        if sType == 'tv':
            sTitle = cUtil().FormatSerie(sTitle)
            r = re.search('((?:[S|E][0-9\.\-\_]+){1,2})', sTitle)
            if r:
                SaisonEpisode = r.group(0)
                sTitle = sTitle.replace(SaisonEpisode,'')

        #on cherche l'annee
        r = re.search('(\([0-9]{4}\))', sTitle)
        if r:
            annee = str(r.group(0))
            sTitle = sTitle.replace(annee,'')

        #Nettoyage nom
        sTitle = sTitle.replace('-','')
        sTitle = sTitle.replace(':','')
        sTitle = re.sub(' +',' ',sTitle)
        sTitle = sTitle.strip()

        xbmc.log('Recherche de : ' + sTitle)
        xbmc.log('Saison/episode : ' + SaisonEpisode)
        xbmc.log('Annee : ' + annee)
        xbmc.log('Type : ' + sType)

        url = 'http://api.themoviedb.org/3/search/'+ sType +'?query=' + urllib.quote_plus(sTitle)

        if annee:
            url = url + '&year=' + str(annee)

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addParameters('api_key', '92ab39516970ab9d86396866456ec9b6')
        oRequestHandler.addParameters('language', 'fr')

        sHtmlContent = oRequestHandler.request()
        result = json.loads(sHtmlContent)
        #xbmc.log(str(result))

        n = 0
        d = 100

        n3 = sTitle.count(' ') + 1
        for i in result['results']:
            #xbmc.log( i['title'].encode("utf-8") + ' ' + str(i['id'] ))
            #compare le nombre de mot identique ET le nombre de mot total
            if 'title' in i:
                sTitle2 = i['title'].encode("utf-8")
            else:
                sTitle2 = i['name'].encode("utf-8")

            #xbmc.log(sTitle2 + ' = ' + str(i['id']))

            #nombre de mots identiques
            n2 = cUtil().CheckOccurence(sTitle,sTitle2)
            #nombre de mot different entre les 2 titres, doit etre le plus petit possible
            d2 = math.fabs( sTitle2.count(' ') + 1 - n3 ) - n2

            if  (n2 >= n) and (d2 < d):
                n = n2
                d = d2
                ret = i['id']

        xbmc.log('Id trouve : ' + str(ret))
        return ret
