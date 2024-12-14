# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import datetime
import re
import time
import unicodedata
import xbmc

from resources.lib.comaddon import addon, dialog, addonManager, VSlog
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.lib.viewing import cViewing


SITE_IDENTIFIER = 'cTrakt'
SITE_NAME = 'Trakt'

URL_API = 'https://api.trakt.tv/'

API_KEY = '7139b7dace25c7bdf0bd79acf46fb02bd63310548b1f671d88832f75a4ac3dd6'
API_SECRET = 'bb02b2b0267b045590bc25c21dac21b1c47446a62b792091b3275e9c4a943e74'
API_VERS = '2'

MAXRESULT = addon().getSetting('trakt_number_element')


'''
API

Matrice des actions
https://github.com/vankasteelj/trakt.tv/blob/master/docs/available_methods.md

'''

class cTrakt:
    CONTENT = '0'
    ADDON = addon()
    DIALOG = dialog()

    def __init__(self):
        self.__sTitle = ''
        self.__sAction = ''
        self.__sType = ''

    def getToken(self):
        oRequestHandler = cRequestHandler(URL_API + 'oauth/device/code')
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addJSONEntry('client_id', API_KEY)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        total = len(sHtmlContent)

        if (total > 0):
            sText = (self.ADDON.VSlang(30304)) % (sHtmlContent['verification_url'], sHtmlContent['user_code'])

            oDialog = self.DIALOG.VSyesno(sText)
            if (oDialog == 0):
                return False

            if (oDialog == 1):

                try:
                    oRequestHandler = cRequestHandler(URL_API + 'oauth/device/token')
                    oRequestHandler.setRequestType(1)
                    oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
                    oRequestHandler.addJSONEntry('client_id', API_KEY)
                    oRequestHandler.addJSONEntry('client_secret', API_SECRET)
                    oRequestHandler.addJSONEntry('code', sHtmlContent['device_code'])
                    sHtmlContent = oRequestHandler.request(jsonDecode=True)

                    if sHtmlContent['access_token']:
                        self.ADDON.setSetting('bstoken', str(sHtmlContent['access_token']))
                        self.DIALOG.VSinfo(self.ADDON.VSlang(30000))

                        # si l'addon est installé, le lier et désactiver le suivi vStream  
                        if addonManager().isAddonExists('script.trakt'):
                            self.ADDON.setSetting('install_trakt_addon', 'true')
                            self.ADDON.setSetting('trakt_movies_activate_scrobbling', 'false')
                            self.ADDON.setSetting('trakt_tvshows_activate_scrobbling', 'false')
                        else:
                            self.ADDON.setSetting('install_trakt_addon', 'false')
                            self.ADDON.setSetting('trakt_movies_activate_scrobbling', 'true')
                            self.ADDON.setSetting('trakt_tvshows_activate_scrobbling', 'true')
                        return
                except:
                    pass

            return
        return

    def getLoad(self):
        # pour regen le token()
        # self.getToken()
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        if self.ADDON.getSetting('bstoken') == '':
            VSlog('TRAKT - bstoken invalid')
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'getToken', self.ADDON.VSlang(30305), 'trakt.png', oOutputParameterHandler)
        else:
            # nom de l'user
            try:
                oRequestHandler = cRequestHandler(URL_API + 'users/me')
                oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
                oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
                oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
                oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                sHtmlContent = oRequestHandler.request(jsonDecode=True)
            except:
                return self.getToken()

            total = len(sHtmlContent)

            if (total > 0):
                sUsername = sHtmlContent['username']
                oOutputParameterHandler.addParameter('siteUrl', 'https://')
                oGui.addText(SITE_IDENTIFIER, (self.ADDON.VSlang(30306)) % sUsername, 'profile.png')

            oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', self.ADDON.VSlang(30120), 'films.png', oOutputParameterHandler)

            oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', self.ADDON.VSlang(30121), 'series.png', oOutputParameterHandler)

            # oOutputParameterHandler.addParameter('type', 'custom-lists')
            # oGui.addDir(SITE_IDENTIFIER, 'showMenuList', "Listes", 'listes.png', oOutputParameterHandler)

            # Menu inutile - oOutputParameterHandler.addParameter('siteUrl', URL_API + 'users/me/history?page=1&limit=' + str(MAXRESULT))
            # Menu inutile - oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30308), 'search.png', oOutputParameterHandler)

            # oOutputParameterHandler.addParameter('siteUrl', URL_API + 'oauth/revoke')
            # oGui.addDir(SITE_IDENTIFIER, 'getCalendrier', self.ADDON.VSlang(30331), 'annees.png', oOutputParameterHandler)
            
            oOutputParameterHandler.addParameter('siteUrl', URL_API + 'oauth/revoke')
            oGui.addDir(SITE_IDENTIFIER, 'getBsout', self.ADDON.VSlang(30309), 'trakt.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMenuList(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'users/me/lists')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30360), 'listes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'users/likes/lists')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', 'Mes listes aimées', 'listes.png', oOutputParameterHandler)  

        oOutputParameterHandler.addParameter('siteUrl', 'lists/popular')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', "Listes populaires", 'listes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'lists/trending')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', "Listes tendances", 'listes.png', oOutputParameterHandler)

        oGui.setEndOfDirectory() 

#    def getCalendrier(self):
#        oGui = cGui()
#
#        today_date = str(datetime.datetime.now().date())
#
#        # DANGER ca rame, freeze
#        liste = []
#        liste.append(['En diffusion cette semaine', URL_API + 'calendars/my/shows/' + today_date + '/7'])
#        # Menu inutile - liste.append(['Mes sorties sur les 30 jours à venir', URL_API + 'calendars/my/shows/' + today_date + '/30'])
#        # Menu inutile - liste.append(['Nouveautées sur 7 jours', URL_API + 'calendars/all/shows/new/' + today_date + '/7'])
#
#        for sTitle, sUrl in liste:
#
#            oOutputParameterHandler = cOutputParameterHandler()
#            oOutputParameterHandler.addParameter('siteUrl', sUrl)
#            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'listes.png', oOutputParameterHandler)
#
#        oGui.setEndOfDirectory()


    def showMenuMovies(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        # visionnage en cours
        oOutputParameterHandler.addParameter('siteUrl', 'sync/playback/movies?type=movies')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30125), 'vod.png', oOutputParameterHandler)

        # historique
        oOutputParameterHandler.addParameter('siteUrl', 'sync/history/movies?type=movies')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30321), 'history.png', oOutputParameterHandler)

        # favoris
        oOutputParameterHandler.addParameter('siteUrl', 'sync/favorites/movies/added')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30430), 'mark.png', oOutputParameterHandler)

        # watchlist
        oOutputParameterHandler.addParameter('siteUrl', 'sync/watchlist/movies/added')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30311), 'pin.png', oOutputParameterHandler)

        # Collection
        oOutputParameterHandler.addParameter('siteUrl', 'sync/collection/movies')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30310), 'listes.png', oOutputParameterHandler)

        # Listes personnelles
        oOutputParameterHandler.addParameter('siteUrl', 'users/me/lists')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30360), 'listes.png', oOutputParameterHandler)

        # Listes aimées
        oOutputParameterHandler.addParameter('siteUrl', 'users/likes/lists')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', 'Mes listes aimées', 'listes.png', oOutputParameterHandler)  

        # recommandés
        oOutputParameterHandler.addParameter('siteUrl', 'recommendations/movies?ignore_collected=true&ignore_watchlisted=true&limit=100')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30313), 'announce.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def showMenuTvShows(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        # Visionnage en cours, NON, pas interessant d'avoir la liste des épisodes non terminés
        # liste.append([self.ADDON.VSlang(30125), URL_API + 'sync/playback/episodes?type=episodes'])
        
        # visionnage en cours
        oOutputParameterHandler.addParameter('siteUrl', 'sync/watched/shows?type=show')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30125), 'vod.png', oOutputParameterHandler)
#            liste.append([self.ADDON.VSlang(30125), URL_API + 'sync/watched/shows?type=show'])

        # # historique de visionnage
        #     liste.append([self.ADDON.VSlang(30321), URL_API + 'sync/watched/shows?extended=noseasons'])
#            liste.append(['%s (%s)' % (self.ADDON.VSlang(30310), sHtmlContent['shows']['collected']), URL_API + 'users/me/collection/shows'])

        # favoris
        oOutputParameterHandler.addParameter('siteUrl', 'sync/favorites/shows/added')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30430), 'mark.png', oOutputParameterHandler)
#            liste.append([self.ADDON.VSlang(30430), URL_API + 'sync/favorites/shows/added'])

        # watchlist
        oOutputParameterHandler.addParameter('siteUrl', 'sync/watchlist/shows/added')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30311), 'pin.png', oOutputParameterHandler)
#            liste.append([self.ADDON.VSlang(30311), URL_API + 'users/me/watchlist/shows'])

        # Collection
        oOutputParameterHandler.addParameter('siteUrl', 'sync/collection/shows')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30310), 'listes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'users/me/lists')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30360), 'listes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'users/likes/lists')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', 'Mes listes aimées', 'listes.png', oOutputParameterHandler)  

        # liste.append([self.ADDON.VSlang(30318), URL_API + 'users/me/watchlist/seasons'])
        # liste.append([self.ADDON.VSlang(30319), URL_API + 'users/me/watchlist/episodes'])

        # calendrier des sorties
        today_date = str(datetime.datetime.now().date())
        oOutputParameterHandler.addParameter('siteUrl', 'calendars/my/shows/' + today_date + '/7')
        oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30331), 'annees.png', oOutputParameterHandler)


        # # recommandés
        # oOutputParameterHandler.addParameter('siteUrl', 'recommendations/shows?ignore_collected=true&ignore_watchlisted=true&limit=100')
        # oOutputParameterHandler.addParameter('sCat', '2')
        # oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30313), 'announce.png', oOutputParameterHandler)
        #
        # # populaire
        # oOutputParameterHandler.addParameter('siteUrl', 'shows/trending')
        # oOutputParameterHandler.addParameter('sCat', '2')
        # oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30315), 'popular.png', oOutputParameterHandler)
        #
        # # les mieux notés
        # oOutputParameterHandler.addParameter('siteUrl', 'shows/popular')
        # oOutputParameterHandler.addParameter('sCat', '2')
        # oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30104), 'notes.png', oOutputParameterHandler)
        # # Chercher une liste
        # oOutputParameterHandler.addParameter('sCat', '2')
        # oGui.addDir(SITE_IDENTIFIER, 'showSearchList', 'Chercher une liste', 'notes.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def showSearchList(self):
        oGui = cGui()
    
        sSearchText = oGui.showKeyBoard()
        if sSearchText:
            oInputParameterHandler = cInputParameterHandler()
            sCat = oInputParameterHandler.getValue('sCat')
            self.searchList(sSearchText, sCat)
            return


    def searchList(self, sSearchText="", sCat=""):
        
        oGui = cGui()

        if not sSearchText:
            oInputParameterHandler = cInputParameterHandler()
            sSearchText = oInputParameterHandler.getValue('searchtext')
            sCat = oInputParameterHandler.getValue('sCat')
        sUrl = URL_API + 'search/list?query=' + sSearchText
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        
        listes = oRequestHandler.request(jsonDecode=True)
        oOutputParameterHandler = cOutputParameterHandler()
        
        listes = sorted(listes, key=lambda liste: liste['list']['likes'])

        
        for item in listes[::-1]:
            liste = item['list']
            itemCount = liste['item_count']
            if itemCount < 3:
                continue
            sTitle = '%s (%s)' % (liste['name'], itemCount)
            desc = liste['description']
            sUrl = '/lists/%d/items' % liste['ids']['trakt']
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sCat', sCat)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'library.png', oOutputParameterHandler, desc)
            
        oGui.setEndOfDirectory()


    def getLists(self, count = 0, sPage=None):
        oGui = cGui()
        bNext = count==0
        oInputParameterHandler = cInputParameterHandler()
        sCat = oInputParameterHandler.getValue('sCat')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        if not sPage:
            sPage = oInputParameterHandler.getValue('sPage') 
        if not sPage:
            sPage = '1'

        # Pagination
        sUrl = '%s?page=%s&limit=%s' % (siteUrl, sPage, MAXRESULT)

        oRequestHandler = cRequestHandler(URL_API + sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        if 'users/' in sUrl or '/sync/' in sUrl:
            oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        listes = oRequestHandler.request(jsonDecode=True)
        
        if len(listes):

            # trie de la liste par alpha
            if '/me/' in sUrl:
                listes = sorted(listes, key=lambda liste: liste['name'])
            # elif 'likes/' in sUrl:
            #     listes = sorted(listes, key=lambda liste: liste['list']['name'])
            
            for liste in listes:
                if '/me/' in sUrl:
                    sUrl = 'users/me/lists/' + liste['ids']['slug'] + '/items'
                elif '/likes/' in sUrl:
                    liste = liste['list']
                    sUrl = 'users/' + liste['user']['ids']['slug'] + '/lists/' + liste['ids']['slug'] + '/items'
                else:
                    liste = liste['list']
                    sUrl = '/lists/%d/items' % liste['ids']['trakt']

                listName = liste['name']
                listNameUpper = listName.upper()

                # détecter si liste de films ou séries selon le nom
                found = False
                if sCat == '1':
                    searchTypeMovie = ('FILM', 'MOVIE', 'OSCAR', 'CESAR', 'CÉSAR', 'BLOCKBUSTER', 'CINEMA', 'CINÉMA', 'TUEURS EN SERIES', 'CRITERION')
                    for movieType in searchTypeMovie:
                        if movieType in listNameUpper:
                            found = True
                            break
                
                # détecter si liste de films ou séries selon le nom
                if sCat == '2':
                    searchTypeMovie = ('SERIE', 'SÉRIE')
                    for movieType in searchTypeMovie:
                        if movieType in listNameUpper:
                            found = True
                            break
                
                
                # détecter si liste de films ou séries selon le contenu
                if not found:
                    oRequestHandler = cRequestHandler(URL_API + sUrl)
                    oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
                    oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
                    oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
                    oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                    sHtmlContent = oRequestHandler.request(jsonDecode=True)
                    if len(sHtmlContent):
                        searchMedia = 'movie' if sCat == '1' else 'show'
#                        media = sHtmlContent[0]
                        for media in sHtmlContent:
                            if searchMedia in media:
                                found = True
                                break

                if found:
                    count += 1
                    sTitle = '%s (%d)' % (self.decode(listName), liste['item_count'])
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sCat', sCat)
                    oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'library.png', oOutputParameterHandler, liste['description'])
    
    
            if 'me/' not in siteUrl:
                iPage = int(sPage)
#                ratio = 5+count/ iPage  # pour arreter si trop de pages sans résultats  
                sNextPage =str(iPage + 1)
                
                if count < int(MAXRESULT):# and ratio > 3.0:
                    self.getLists(count, sNextPage)
                else:  
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sCat', sCat)
                    oOutputParameterHandler.addParameter('sPage', sNextPage)
                    oGui.addNext(SITE_IDENTIFIER, 'getLists', 'Page suivante', oOutputParameterHandler)
    

        if bNext:
            oGui.setEndOfDirectory()


    def getBsout(self):
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        oRequestHandler.addJSONEntry('client_id', API_KEY)
        oRequestHandler.addJSONEntry('client_secret', API_SECRET)
        oRequestHandler.addJSONEntry('token', self.ADDON.getSetting('bstoken'))
        sHtmlContent = oRequestHandler.request()

        total = len(sHtmlContent)

        if (total > 0):
            self.ADDON.setSetting('bstoken', '')
            self.DIALOG.VSinfo(self.ADDON.VSlang(30320))
            xbmc.executebuiltin('Container.Refresh')

        return


    def decode(self, elem, Unicode=False):
        if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
            return elem
        else:
            if Unicode == True:
                try:
                    elem = unicodedata.normalize('NFD', unicode(elem)).encode('ascii', 'ignore').decode('unicode_escape')
                except UnicodeDecodeError:
                    elem = elem.decode('utf-8')
                except:
                    pass

            return elem.encode('utf-8')


    def getTrakt(self, count = 0, sPage=None):
        oGui = cGui()
        maxResult = int(MAXRESULT)
        bNext = count==0
        oInputParameterHandler = cInputParameterHandler()
        sCurrentLimit = oInputParameterHandler.getValue('limite')
        sCat = oInputParameterHandler.getValue('sCat')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        traktUrl = sUrl = URL_API + siteUrl
        if not sPage:
            sPage = oInputParameterHandler.getValue('sPage') 
        if not sPage:
            sPage = 1

        if 'limit' not in siteUrl:
            traktUrl += ("%spage=%s&limit=%d") % ('&' if '?' in sUrl else '?', sPage, maxResult)

        oRequestHandler = cRequestHandler(traktUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        if '/users/' in sUrl or '/sync/' in sUrl or '/my/' in sUrl or '/recommendations/' in sUrl:
            oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        sHtmlContent = oRequestHandler.request(jsonDecode=True)
        sHeaders = oRequestHandler.getResponseHeader()

        # tri inverse pour certaines listes
        if 'sync/collection/movies' in sUrl:
            sHtmlContent = sHtmlContent[::-1] 


        if 'X-Pagination-Page' in sHeaders:
            sPage = sHeaders['X-Pagination-Page']
        iPage = int(sPage)

        # Pour les API sans pagination, on pagine le resultat complet
        total = len(sHtmlContent)
        iMaxPage = 1
        if 'X-Pagination-Page-Count' not in sHeaders:
            if not sCurrentLimit:
                sCurrentLimit = 0
            else:
                # Se déplacer derriere les elements deja affichés
                sHtmlContent = sHtmlContent[int(sCurrentLimit):]
            if total > maxResult:
                total = maxResult
        else:
            iMaxPage = int(sHeaders['X-Pagination-Page-Count'])


        sKey = 0
        sFunction = 'getLoad'
        sId = SITE_IDENTIFIER
        searchtext = ''
        sTitle = ''
        sTmdb = None
        sOldDate = None
        tmdbIds = set()
        saisonsWatched = list()
        
        if (total > 0):
            
            # synchroniser avec trakt les medias entamés seulement lorsqu'on arrive sur la premiere page
            if '/watched/' in sUrl:
                if sCurrentLimit == 0 and iPage == 1 :
                    self.setEpisodeProgress()

            for i in sHtmlContent:

                progress = 0

                if '/collection/' in sUrl:

                    try:
                        sDate = i['last_collected_at']
                    except:
                        sDate = ""

                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sYear, sImdb, sTmdb = show['ids']['trakt'], show['year'], show['ids']['imdb'], show['ids']['tmdb']

                        cTrakt.CONTENT = '2'
                        sFunction = 'showSearch'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sYear, sImdb, sTmdb = movie['ids']['trakt'], movie['year'], movie['ids']['imdb'], movie['ids']['tmdb']
                        
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    sTitle = self.decode(sTitle)
                    searchtext = sTitle
                    sFile = sTitle
# NON, pour les skins
#                   if sYear:
#                        sTitle = ('%s - (%s)') % (sTitle, int(sYear))

                elif '/history/' in sUrl:
                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    if 'episode' in i:
                        eps = i['episode']
                        # Utiliser le titre de la série et récupérer les images associées
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sPoster = show['images']['poster']['full'] if 'images' in show and 'poster' in show['images'] else None
                        sFanart = show['images']['fanart']['full'] if 'images' in show and 'fanart' in show['images'] else None
                        sTrakt, sImdb, sTmdb, sSeason, sNumber = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], eps['season'], eps['number']
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sPoster = movie['images']['poster']['full'] if 'images' in movie and 'poster' in movie['images'] else None
                        sFanart = movie['images']['fanart']['full'] if 'images' in movie and 'fanart' in movie['images'] else None
                        sTrakt, sYear, sImdb, sTmdb = movie['ids']['trakt'], movie['year'], movie['ids']['imdb'], movie['ids']['tmdb']
                        cTrakt.CONTENT = '1'

                    # masquer les doublons
                    if sTmdb in tmdbIds:
                        count = count +1    # compte quand même pour ne pas passer à la page suivante
                        continue
                    tmdbIds.add(sTmdb)
                    
                    sTitle = self.decode(sTitle, Unicode=True)
                    searchtext = sTitle
                    sFile = sTitle
                    oOutputParameterHandler = cOutputParameterHandler()
                    if sPoster:
                        oOutputParameterHandler.addParameter('poster', sPoster)
                    if sFanart:
                        oOutputParameterHandler.addParameter('backdrop', sFanart)

                elif '/watchlist/' in sUrl or '/favorites/' in sUrl:
                    # commun
                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year']
                        sExtra = ('(%s)') % (sYear)
                        cTrakt.CONTENT = '2'
                    elif 'episode' in i:
                        eps = i['episode']
                        sTitle = self.getLocalizedTitle(i, 'episodes')
                        sTrakt, sImdb, sTmdb, sSeason, sNumber = eps['ids']['trakt'], eps['ids']['imdb'], eps['ids']['tmdb'], eps['season'], eps['number']
                        sExtra = ('(S%02dE%02d)') % (sSeason, sNumber)
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                        sExtra = ('(%s)') % (sYear)
                        cTrakt.CONTENT = '1'

                    sTitle = self.decode(sTitle, Unicode=True)
                    searchtext = sTitle
                    sFile = sTitle

                # Lecture en progression
                elif '/playback/' in sUrl :
                    sSeason = sEpisode = None

                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year']
                        cTrakt.CONTENT = '2'
                        sSeason = i['episode']['season']
                        sEpisode = i['episode']['number']
                        sFunction = 'showSearch'
                        sId = 'globalSearch'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    # récuperer les points de lecture
                    progress = i['progress']
                    
                    # au moins 5% de lecture pour proposer le film
                    if progress < 5:
                        continue
                    
                    self.setMediaProgress(sTmdb, sTitle, sSeason, sEpisode, progress)

                    if sTitle:
                        sTitle = self.decode(sTitle, Unicode=True)
                        searchtext = sTitle
                        sFile = sTitle

                # historique de lecture
                elif '/watched/' in sUrl:
                    # commun
                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year']
                        cTrakt.CONTENT = '2'
#                        sFunction = 'getBseasons'
                        #media['episode']['season'], media['episode']['number']
                        sFunction = 'showSearch'
                        sId = 'globalSearch'
                        
                        # Indicateur VU
                        saisonsWatched.append(i)

                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    if sTitle:
                        sTitle = self.decode(sTitle, Unicode=True)
                        searchtext = sTitle
                        sFile = sTitle

                elif '/played/' in sUrl:
                    # commun
                    #sWatcher_count, sPlay_count, sCollected_count = i['watcher_count'], i['play_count'], i['collected_count']
                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year']
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                        cTrakt.CONTENT = '1'

                    sTitle = self.decode(sTitle)
                    searchtext = sTitle
                    sFile = sTitle

                elif '/calendars/' in sUrl:
                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear, sFirst_aired = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year'], i['first_aired']
                        sSaison, sEpisode = i['episode']['season'], i['episode']['number']
                        searchtext = sTitle
                        sFile = sTitle
                        sTitle = 'S%sE%s - %s' % (sSaison, sEpisode, sTitle)
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        searchtext = sTitle
                        sFile = sTitle
                        sTrakt, sImdb, sTmdb, sYear, sFirst_aired = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year'], i['first_aired']
                        cTrakt.CONTENT = '1'

                    if sTitle:
                        sDate = datetime.datetime(*(time.strptime(sFirst_aired, '%Y-%m-%dT%H:%M:%S.%fZ')[0:6])).strftime('%d-%m-%Y')
                        if sOldDate != sDate:
                            sOldDate = sDate
                            oGui.addText(SITE_IDENTIFIER, '[COLOR orange]En diffusion le : %s[/COLOR]' % sOldDate, 'annees.png')

                        sTitle = self.decode(sTitle)

                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif '/search/' in sUrl:
                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year']
                        cTrakt.CONTENT = '2'
                        sFunction = 'getBseasons'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    sTitle = self.decode(sTitle, Unicode=True)
                    searchtext = sTitle
                    sFile = sTitle

                elif '/recommendations/' in sUrl or '/popular' in sUrl:
                    if 'shows' in sUrl:
                        sTitle = self.getLocalizedTitle(i, 'shows')
                        cTrakt.CONTENT = '2'
                    else:
                        sTitle = self.getLocalizedTitle(i, 'movies')
                        cTrakt.CONTENT = '1'
                    sTrakt, sYear, sImdb, sTmdb = i['ids']['trakt'], i['year'], i['ids']['imdb'], i['ids']['tmdb']
                    sTitle = self.decode(sTitle)
                    searchtext = sTitle
                    sFile = sTitle

                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif '/boxoffice' in sUrl or '/trending' in sUrl:
                    if 'movie' in sUrl:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sYear, sImdb, sTmdb = movie['ids']['trakt'], movie['year'], movie['ids']['imdb'], movie['ids']['tmdb']
                        cTrakt.CONTENT = '1'
                    else:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sYear, sImdb, sTmdb = show['ids']['trakt'], show['year'], show['ids']['imdb'], show['ids']['tmdb']
                        cTrakt.CONTENT = '2'
                        
                    sTitle = self.decode(sTitle)
                    searchtext = sTitle
                    sFile = sTitle
                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif '/lists' in sUrl:

                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    sTitle = None

                    if sCat == '2':
                        if 'show' in i:
                            show = i['show']
                            sTitle = self.getLocalizedTitle(show, 'shows')
                            sTrakt, sImdb, sTmdb, sYear = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year']
                            sExtra = ('(%s)') % (sYear)
                            cTrakt.CONTENT = '2'
                        elif 'episode' in i:
                            eps = i['episode']
                            sTitle = self.getLocalizedTitle(i, 'episodes')
                            sTrakt, sImdb, sTmdb, sSeason, sNumber = eps['ids']['trakt'], eps['ids']['imdb'], eps['ids']['tmdb'], eps['season'], eps['number']
                            sExtra = ('(S%02dE%02d)') % (sSeason, sNumber)
                            cTrakt.CONTENT = '2'
                    else:
                        if 'movie' in i:
                            movie = i['movie']
                            sTitle = self.getLocalizedTitle(movie, 'movies')
                            sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                            sExtra = ('(%s)') % (sYear)
                            cTrakt.CONTENT = '1'

                    if sTitle:
                        sTitle = self.decode(sTitle, Unicode=True)
                        searchtext = sTitle
                        sFile = sTitle

                else:
                    return

                # Appeler la méthode getFolder avec les paramètres configurés
                if sTitle:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl +'/' + str(sTrakt))
                    oOutputParameterHandler.addParameter('sID', str(i['id']) if 'id' in i else None)
                    oOutputParameterHandler.addParameter('sTmdbId', sTmdb)
                    oOutputParameterHandler.addParameter('sCat', sCat)
                    oOutputParameterHandler.addParameter('file', sFile)
                    oOutputParameterHandler.addParameter('key', sKey)
                    oOutputParameterHandler.addParameter('searchtext', searchtext)

                    if progress > 0:
                        oOutputParameterHandler.addParameter('ResumeTime', progress)
                        oOutputParameterHandler.addParameter('TotalTime', '100')

                    
                    self.getFolder(oGui, sId, sTitle, sFile, sFunction, sImdb, sTmdb, oOutputParameterHandler)
                    sKey += 1
                    count = count +1
                    if count >= maxResult:
                        break
    


            # indicateur VU sur les saisons
            for saisonWtached in saisonsWatched[::-1]:
                self.setSaisonWatched(saisonWtached)


            if iPage < iMaxPage:
                sNextPage =str((iPage) + 1)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sCat', sCat)
                oOutputParameterHandler.addParameter('sPage', sNextPage)
                
                if count < maxResult:
                    self.getTrakt(count, sNextPage)
                else:
                    oGui.addNext(SITE_IDENTIFIER, 'getTrakt', 'Page suivante', oOutputParameterHandler)  
                
            elif not 'X-Pagination-Page-Count' in sHeaders and len(sHtmlContent) > maxResult:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sCat', sCat)
                oOutputParameterHandler.addParameter('limite', int(sCurrentLimit) + maxResult)
                oGui.addNext(SITE_IDENTIFIER, 'getTrakt', 'Page suivante', oOutputParameterHandler)  

        if bNext:
            oGui.setEndOfDirectory()


    # Récupérer les épisodes qui n'ont pas été lus jusqu'au bout
    def setEpisodeProgress(self):
        #https://api.trakt.tv/sync/playback/type
        # oRequestHandler = cRequestHandler(URL_API + 'sync/playback/' + ('movies' if sCat == '1' else 'episodes'))
        oRequestHandler = cRequestHandler(URL_API + 'sync/playback/episodes')
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        playbackHistory = oRequestHandler.request(jsonDecode=True)
        
        if len(playbackHistory) == 0:
            return


        util = cUtil()
        with cDb() as db:

            titleList = set()

            for media in playbackHistory:
                # if media['show']['ids']['tmdb'] != int(sTmdb):
                #     continue
                
                sTitle = media['show']['title']
                sSaison = media['episode']['season']
                tvShowTitleWatched = util.titleWatched(sTitle)
                sTitleWatched = '%s_S%02dE%02d' % (tvShowTitleWatched, sSaison, media['episode']['number'])
                progress = media['progress']


                # Point de reprise vidéo d'un épisode
                       
                # il faut au moins 5% de lecture pour proposer la reprise
                if progress < 5:
                    continue

                # en pourcentage                
                totalTime = 1
                progress = progress/100

                meta = {}
                meta['title'] = sTitle
                meta['titleWatched'] = sTitleWatched
                meta['site'] = 'globalSearch'
                meta['point'] = progress
                meta['total'] = totalTime
                db.insert_resume(meta)
                
                # On met la saison "En cours de lecture"
                if tvShowTitleWatched not in titleList:
                    titleList.add(tvShowTitleWatched)
                
                    sTmdbId = media['show']['ids']['tmdb']
                    meta['cat'] = '4'  # saison
                    meta['tmdbId'] = sTmdbId
                    if sSaison:
                        meta['season'] = sSaison
                        meta['title'] = '%s S%d' % (sTitle ,sSaison)
                        meta['titleWatched'] = '%s_S%d' % (tvShowTitleWatched ,sSaison)
                    else:
                        meta['title'] = sTitle
                        meta['titleWatched'] = tvShowTitleWatched
                    meta['siteurl'] = 'showSearch'
                    meta['fav'] = 'showSearch'

                    # saison "EN COURS"
                    # NON, on n'a pas d'url de reprise db.insert_viewing(meta)

                    # On met la saison "VU"
                    db.insert_watched(meta)
            
        return


    # Marquer les saisons EN COURS dont des épisodes sont VU
    def setSaisonWatched(self, watchedShow):
        util = cUtil()
        show = watchedShow['show']
        saisons = watchedShow['seasons']
        sTitle = show['title']
        tvShowTitleWatched = util.titleWatched(sTitle)
        sTmdbId = show['ids']['tmdb']

        meta = {}
        meta['tmdbId'] = sTmdbId
        meta['site'] = 'globalSearch'
        meta['siteurl'] = 'showSearch'
        meta['fav'] = 'showSearch'
        meta['seasonUrl'] = 'showSearch'
        meta['seasonFunc'] = 'showSearch'


        with cDb() as db:
            for saison in saisons:
                numSaison = saison['number']
                saisonTitle = '%s S%02d' % (sTitle, numSaison)
                saisonTitleWatched = '%s_S%02d' % (tvShowTitleWatched, numSaison)
                meta['cat'] = '4'  # saison
                meta['season'] = numSaison
                meta['title'] = saisonTitle
                meta['titleWatched'] = saisonTitleWatched

                # On met la saison "EN COURS" et "VU" (pour l'indicateur)
                # NON, on n'a pas d'url de reprise db.insert_viewing(meta)
                
                # On met la saison "VU" (pour l'indicateur)
                db.insert_watched(meta)
            
                episodes = saison['episodes']
                for episode in episodes:
                    numEp = episode['number']
                    meta['cat'] = '8'  # episode
                    meta['title'] = '%sE%02d' % (saisonTitle, numEp)
                    meta['titleWatched'] = '%sE%02d' % (saisonTitleWatched, numEp)
                    # On met l'épisode "VU"
                    db.insert_watched(meta)
            
        return


    # progression dans le cache vStream selon l'état dans trakt
    def setMediaProgress(self, sTmdb, sTitle, sSeason, sEpisode, progress):
        # il faut au moins 5% de lecture pour proposer la reprise
        if progress < 5:
            return

        util = cUtil()
        # en pourcentage                
        totalTime = 1
        progress = progress/100

        sTitleWatched = util.titleWatched(sTitle)
        if sSeason or sEpisode:
            sTitleWatched = '%s_S%02dE%02d' % (sTitleWatched, sSeason, sEpisode)

        meta = {}
        meta['title'] = sTitle
        meta['titleWatched'] = sTitleWatched
        meta['site'] = 'globalSearch'
        meta['point'] = progress
        meta['total'] = totalTime
        with cDb() as db:
            db.insert_resume(meta)

        # On met le media "EN COURS"
        
        
        return


    def getBseasons(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sFile = oInputParameterHandler.getValue('file')
        sKey = oInputParameterHandler.getValue('key')
        searchtext = oInputParameterHandler.getValue('searchtext')

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        total = len(sHtmlContent)
        sNum = 0
        if (total > 0):
            for i in sHtmlContent[int(sKey)]['seasons']:

                if 'collection' in sUrl or 'watched' in sUrl:
                    sNumber = i['number']
                    cTrakt.CONTENT = '5'
                else:
                    return

                sTitle2 = ('%s - S%02d') % (self.decode(sFile), int(sNumber))
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl + str(sNumber))
                oOutputParameterHandler.addParameter('key', sKey)
                oOutputParameterHandler.addParameter('sNum', sNum)
                oOutputParameterHandler.addParameter('file', sFile)
                oOutputParameterHandler.addParameter('title', sTitle2)
                oOutputParameterHandler.addParameter('searchtext', searchtext)
                self.getFolder(oGui, SITE_IDENTIFIER, sTitle2, sFile, 'getBepisodes', '', '', oOutputParameterHandler)
                sNum += 1

        oGui.setEndOfDirectory()


    def getLocalizedTitle(self, item, what):
        from resources.lib.tmdb import cTMDb
        grab = cTMDb()
        if what == 'shows':
            sType = 'tv'
# cache tmdb           sType = 'tvshow'
        elif what == 'movies':
            sType = 'movie'

        # avec gestion du cache tmdb
        # meta = grab.get_meta(sType, item['title'], tmdb_id = item['ids']['tmdb'])
        # if 'title' in meta and meta['title']:
        #     return meta['title']
        # if 'name' in meta and meta['name']:
        #     return meta['name'] # titre de série
#        return item['title']

        # demander à TMDB
        title = grab.get_namebyid(sType, item['ids']['tmdb'])
        return title if title else item['title']

    
    def getBepisodes(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('title')
        sFile = oInputParameterHandler.getValue('file')
        sKey = oInputParameterHandler.getValue('key')
        sNum = oInputParameterHandler.getValue('sNum')
        searchtext = oInputParameterHandler.getValue('searchtext')

        cTrakt.CONTENT = '2'

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        total = len(sHtmlContent)

        sNumber = 0
        if (total > 0):
            for i in sHtmlContent[int(sKey)]['seasons'][int(sNum)]['episodes']:

                if 'collection' in sUrl:
                    sNumber = i['number']
                    # Utiliser uniquement le titre de la s�rie pour sTitle2
                    sTitle2 = self.decode(sTitle)

                elif 'watched' in sUrl:
                    sNumber, sPlays = i['number'], i['plays']
                    # Utiliser uniquement le titre de la s�rie pour sTitle2
                    sTitle2 = ('%s Lectures - %s') % (sPlays, self.decode(sTitle))

                else:
                    return

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl + str(sNumber))
                oOutputParameterHandler.addParameter('file', sFile)
                oOutputParameterHandler.addParameter('searchtext', searchtext)
                self.getFolder(oGui, 'globalSearch', sTitle2, sFile, 'showSearch', '', '', oOutputParameterHandler)

        oGui.setEndOfDirectory()
        return

    def getFolder(self, oGui, sId, sTitle, sFile, sFunction, sImdb, sTmdb, oOutputParameterHandler):
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdb)
        sPoster = oOutputParameterHandler.getValue('poster')

        if cTrakt.CONTENT == '1':
            oGui.addMovie(sId, sFunction, sTitle, 'no-image.png', sPoster, '', oOutputParameterHandler)
        elif cTrakt.CONTENT == '2':
            oGui.addTV(sId, sFunction, sTitle, 'no-image.png', sPoster, '', oOutputParameterHandler)
        elif cTrakt.CONTENT == '5':
            oGui.addSeason(sId, sFunction, sTitle, 'no-image.png', sPoster, '', oOutputParameterHandler)
        else:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(sId)
            oGuiElement.setFunction(sFunction)
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sFile)
            oGuiElement.setIcon('trakt.png')
            oGuiElement.setImdbId(sImdb)
            oGuiElement.setTmdbId(sTmdb)
            
            # Récupérer les valeurs des images si elles sont définies
            sPoster = oOutputParameterHandler.getValue('poster')
            sFanart = oOutputParameterHandler.getValue('backdrop')  # Utiliser 'backdrop' pour l'arrière-plan
            
            if sPoster:
                oGuiElement.setThumbnail(sPoster)
            if sFanart:
                oGuiElement.setFanart(sFanart)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)


    def getContext(self):
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('sMovieTitle')

        disp = []
        lang = []

        # Favoris
        if 'sync/favorites' not in sUrl:
            # Ajout favoris
            disp.append(URL_API + 'sync/favorites')
            lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30430))
        # Ajout dans suivis
        if 'sync/watchlist' not in sUrl:
            disp.append(URL_API + 'sync/watchlist')
            lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30311))
        # Ajout Collection
        if 'sync/collection' not in sUrl:
            disp.append(URL_API + 'sync/collection')
            lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30310))

        # Marqué VU
        disp.append(URL_API + 'sync/history')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30312))

        if 'sync/favorites' in sUrl:
            # Retrait favoris
            disp.append(URL_API + 'sync/favorites/remove')
            lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30430) + '[/COLOR]')
        if 'sync/watchlist' in sUrl:
            # Retrait des suivis
            disp.append(URL_API + 'sync/watchlist/remove')
            lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]')
        if 'sync/collection' in sUrl:
            # Retrait favoris
            disp.append(URL_API + 'sync/collection/remove')
            lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]')

        # Marqué NON-VU
        disp.append(URL_API + 'sync/history/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]')

        ret = self.DIALOG.VSselect(lang, 'Trakt - %s' % sTitle)

        if ret > -1:
            self.__sAction = disp[ret]
        return self.__sAction

    def getType(self):

        disp = ['movies', 'shows']
        dialog2 = self.DIALOG.Dialog()
        dialog_select = 'Films', 'Series'

        ret = dialog2.select('Trakt', dialog_select)

        if ret > -1:
            self.__sType = disp[ret]
        return self.__sType

    def convertCatToType(self, sCat):
        # Film, serie, anime, saison, episode
        if sCat not in ('1', '2', '3', '4', '8'):
            return -1

        sType = sCat.replace('1', 'movies').replace('2', 'shows').replace('3', 'shows').replace('4', 'shows').replace('8', 'shows')
        return sType


    def getAction(self, Action='', sEpisode = '', progress=0, requestType = cRequestHandler.REQUEST_TYPE_POST):

        if self.ADDON.getSetting('bstoken') == '':
            self.DIALOG.VSinfo('Vous devez être connecté')
            return

        oInputParameterHandler = cInputParameterHandler()
        if Action:
            sAction = Action
        else:
            sAction = oInputParameterHandler.getValue('sAction')
            if not sAction:
                sAction = self.getContext()
            if not sAction:
                return

        sType = oInputParameterHandler.getValue('sCat')
        if not sType:
            sType = self.getType()

        sSeason = False

        sTraktType = self.convertCatToType(sCat=sType)
        if sTraktType == -1:
            return

        # Mettre en vu automatiquement.
        if Action == "SetWatched" or Action == "SetProgress":

            if sTraktType == "shows":
                if self.ADDON.getSetting('trakt_tvshows_activate_scrobbling') == 'false':
                    return
                
                sTitle = oInputParameterHandler.getValue('tvShowTitle')
                sSeason = oInputParameterHandler.getValue('sSeason')
                if not sSeason:
                    sSeason = re.search('(?i)( s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))', sTitle).group(2)
                if not sEpisode:
                    sEpisode = oInputParameterHandler.getValue('sEpisode')
                if not sEpisode:
                    sFileName = oInputParameterHandler.getValue('sFileName')
                    sEpisode = re.search('(?i)(?:^|[^a-z])((?:E|(?:\wpisode\s?))([0-9]+(?:[\-\.][0-9\?]+)*))', sFileName).group(2)
            else:
                if self.ADDON.getSetting('trakt_movies_activate_scrobbling') == 'false':
                    return
                sTitle = oInputParameterHandler.getValue('sFileName')

            if Action == "SetProgress":
                sAction = URL_API + 'scrobble/stop'
            else:
                sAction = URL_API + 'sync/history'

            if not sTitle:
                sTitle = oInputParameterHandler.getValue('sMovieTitle')
        else:
            sTitle = oInputParameterHandler.getValue('sMovieTitle')

        # entrer imdb ? venant d'ou?
        sImdb = oInputParameterHandler.getValue('sImdbId')
        sTMDB = oInputParameterHandler.getValue('sTmdbId')
        if not sImdb:
            if not sTMDB:
                sTMDB = int(self.getTmdbID(sTitle, sTraktType))

            if not sTMDB:
                return
            
            sPost = {sTraktType: [{'ids': {'tmdb': sTMDB}}]}
            if sSeason:
                sPost = {sTraktType: [{'ids': {'tmdb': sTMDB}, 'seasons': [{'number': int(sSeason)}]}]}
            if sEpisode:
                sPost = {sTraktType: [{'ids': {'tmdb': sTMDB}, 'seasons': [{'number': int(sSeason), 'episodes': [{'number': int(sEpisode)}]}]}]}
        else:
            sPost = {sTraktType: [{'ids': {'imdb': sImdb}}]}


        if Action == "SetProgress":
            if progress == 0:
                return
            progress *= 100
            if sSeason:
                sPost = {'progress':progress, sTraktType[:-1]: {'ids': {'tmdb': sTMDB}, 'seasons': [{'number': int(sSeason)}]}}
            else:
                sPost = {'progress':progress, sTraktType[:-1]: {'ids': {'tmdb': sTMDB}}}


        oRequestHandler = cRequestHandler(sAction)
        oRequestHandler.setRequestType(requestType)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        for a in sPost:
            oRequestHandler.addJSONEntry(a, sPost[a])
        
        jsonDecode = requestType in [cRequestHandler.REQUEST_TYPE_POST, cRequestHandler.REQUEST_TYPE_GET]
        sHtmlContent = oRequestHandler.request(jsonDecode = jsonDecode)

        sText = "Aucune action réalisée"
        
        if sHtmlContent == '':
            sText = ''
            
        try:
            # point de reprise
            if sHtmlContent['action'] == 'pause':
                sText = 'Progression enregistrée'
        except:
            pass

        try:
            if sHtmlContent['added']['movies'] > 0 or sHtmlContent['added']['episodes'] > 0 or sHtmlContent['added']['shows'] > 0:
                sText = 'Ajouté avec succès'
        except:
            pass

        try:
            if sHtmlContent['updated']['movies'] > 0 or sHtmlContent['updated']['episodes'] > 0 or sHtmlContent['updated']['shows'] > 0:
                sText = 'Mise à jour avec succès'
        except:
            pass

        try:
            if sHtmlContent['deleted']['movies'] > 0 or sHtmlContent['deleted']['episodes'] > 0:
                sText = 'Supprimé avec succès'
        except:
            pass

        try:
            if sHtmlContent['existing']['movies'] > 0 or sHtmlContent['existing']['episodes'] > 0 or sHtmlContent['existing']['seasons'] > 0 or sHtmlContent['existing']['shows'] > 0:
                sText = 'Entrée déjà présente'
        except:
            pass


        bReload = oInputParameterHandler.exist('sReload')

        # Supprimé des VUS
        if 'sync/history/remove' in sAction:
            sID = oInputParameterHandler.getValue('sID')
            if sID:
                # suppression du point de reprise dans trakt
                self.getAction(URL_API + 'sync/playback/' + sID, requestType = cRequestHandler.REQUEST_TYPE_DELETE)
                sText = 'Supprimé avec succès'
           
            # suppression du point de reprise dans vStream
            cViewing().delViewing()
                
            # suppression de l'indicateur VU dans vStream
            meta = {}
            meta['titleWatched'] = oInputParameterHandler.getValue('sTitleWatched')
            meta['tmdbId'] = sTMDB
            with cDb() as db:
                db.del_watched(meta)
            
        elif 'sync/history' in sAction:    # ajout du marqueur VU
            # Ajout de l'indicateur VU dans vStream
            if sType == '1':    # seulement pour les films
                bReload = True

                meta = {}
                meta['title'] = sTitle
                meta['titleWatched'] = oInputParameterHandler.getValue('sTitleWatched')
                meta['tmdbId'] = sTMDB
                meta['site'] = 'globalSearch'
                meta['siteurl'] = 'showSearch'
                meta['fav'] = 'showSearch'
                meta['seasonUrl'] = 'showSearch'
                meta['seasonFunc'] = 'showSearch'
                meta['cat'] = sType
                with cDb() as db:
                    db.insert_watched(meta)
            
        if sText:
            self.DIALOG.VSinfo(sText, 'trakt')

        if bReload:
            xbmc.executebuiltin('Container.Refresh')
        return
    

    def getTmdbInfo(self, sTmdb, oGuiElement):

        return

        if not sTmdb:
            VSlog('TRAKT - Pas de TmdbID')
            return

        oRequestHandler = cRequestHandler('https://api.themoviedb.org/3/movie/' + str(sTmdb))
        oRequestHandler.addParameters('api_key', '92ab39516970ab9d86396866456ec9b6')
        oRequestHandler.addParameters('language', 'fr')

        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        # format
        meta = {}
        meta['imdb_id'] = sHtmlContent['id']
        meta['title'] = sHtmlContent['title']
        meta['tagline'] = sHtmlContent['tagline']
        meta['rating'] = sHtmlContent['vote_average']
        meta['votes'] = sHtmlContent['vote_count']
        meta['duration'] = sHtmlContent['runtime']
        meta['plot'] = sHtmlContent['overview']
        if sHtmlContent['poster_path']:
            oGuiElement.setThumbnail('https://image.tmdb.org/t/p/w396' + sHtmlContent['poster_path'])
        if sHtmlContent['backdrop_path']:
            oGuiElement.setFanart('https://image.tmdb.org/t/p/w1280' + sHtmlContent['backdrop_path'])

        for key, value in meta.items():
            oGuiElement.addItemValues(key, value)

        return

    def getTmdbID(self, sTitle, sType, sYear = ''):
        from resources.lib.tmdb import cTMDb
        grab = cTMDb()

        if sType == 'shows':
            sType = 'tv'
        elif sType == 'movies':
            sType = 'movie'

        # on cherche l'annee
        year = sYear
        if year == '':
            r = re.search('(\([0-9]{4}\))', sTitle)
            if r:
                year = str(r.group(0))
                sTitle = sTitle.replace(year, '')

        meta = grab.get_idbyname(sTitle, year, sType)

        try:
            return int(meta)
        except:
            return 0
