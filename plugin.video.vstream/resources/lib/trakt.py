# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import datetime
import re
import time
import unicodedata
import xbmc

from resources.lib.comaddon import addon, dialog, progress, VSlog
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import Quote

SITE_IDENTIFIER = 'cTrakt'
SITE_NAME = 'Trakt'

URL_API = 'https://api.trakt.tv/'

API_KEY = '7139b7dace25c7bdf0bd79acf46fb02bd63310548b1f671d88832f75a4ac3dd6'
API_SECRET = 'bb02b2b0267b045590bc25c21dac21b1c47446a62b792091b3275e9c4a943e74'
API_VERS = '2'

MAXRESULT = addon().getSetting('trakt_number_element')


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
                        return
                except:
                    pass

            return
        return

    def search(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://')
        oOutputParameterHandler.addParameter('type', 'movie')
        oGui.addDir('themoviedb_org', 'showSearchMovie', self.ADDON.VSlang(30423), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('type', 'show')
        oGui.addDir('themoviedb_org', 'showSearchSerie', self.ADDON.VSlang(30424), 'series.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getLoad(self):
        # pour regen le token()
        # self.getToken()
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        if self.ADDON.getSetting('bstoken') == '':
            VSlog('bstoken invalid')
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
                oGui.addText(SITE_IDENTIFIER, (self.ADDON.VSlang(30306)) % sUsername)

            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'search', self.ADDON.VSlang(30330), 'search.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('type', 'movie')
            oGui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30120), 'films.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('type', 'show')
            oGui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30121), 'series.png', oOutputParameterHandler)

            if self.ADDON.getSetting('trakt_show_lists') == 'true':
                oOutputParameterHandler.addParameter('type', 'custom-lists')
                oGui.addDir(SITE_IDENTIFIER, 'menuList', "Listes", 'trakt.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('siteUrl', URL_API + 'users/me/history?page=1&limit=' + str(MAXRESULT))
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', self.ADDON.VSlang(30308), 'trakt.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('siteUrl', URL_API + 'oauth/revoke')
            oGui.addDir(SITE_IDENTIFIER, 'getCalendrier', self.ADDON.VSlang(30331), 'trakt.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('siteUrl', URL_API + 'oauth/revoke')
            oGui.addDir(SITE_IDENTIFIER, 'getBsout', self.ADDON.VSlang(30309), 'trakt.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def menuList(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://')
        oOutputParameterHandler.addParameter('type', 'lists-tendances')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', "Listes tendances", 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('type', 'lists-pop')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', "Listes populaires", 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('type', 'custom-lists')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', self.ADDON.VSlang(30360), 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('type', 'liked-lists')
        oGui.addDir(SITE_IDENTIFIER, 'getLists', 'Mes listes aimées', 'trakt.png', oOutputParameterHandler)  

        oGui.setEndOfDirectory() 

    def getCalendrier(self):
        oGui = cGui()

        today_date = str(datetime.datetime.now().date())

        # DANGER ca rame, freeze
        liste = []
        liste.append(['Mes sorties sur les 7 jours à venir', URL_API + 'calendars/my/shows/' + today_date + '/7'])
        liste.append(['Mes sorties sur les 30 jours à venir', URL_API + 'calendars/my/shows/' + today_date + '/30'])
        liste.append(['Nouveautées sur 7 jours', URL_API + 'calendars/all/shows/new/' + today_date + '/7'])

        for sTitle, sUrl in liste:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getLists(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

        # stats user
        oRequestHandler = cRequestHandler(URL_API + 'users/me/stats')
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        liste = []
        if sType == 'movie':
            liste.append(['%s (%s)' % (self.ADDON.VSlang(30310), sHtmlContent['movies']['collected']), URL_API + 'users/me/collection/movies'])

            if self.ADDON.getSetting('trakt_movies_show_watchlist') == 'true':
                liste.append([self.ADDON.VSlang(30311), URL_API + 'users/me/watchlist/movies?page=1&limit=' + str(MAXRESULT)])

            if self.ADDON.getSetting('trakt_movies_show_watched') == 'true':
                liste.append(['%s (%s)' % (self.ADDON.VSlang(30312), sHtmlContent['movies']['watched']), URL_API + 'users/me/watched/movies'])

            if self.ADDON.getSetting('trakt_movies_show_recommended') == 'true':
                liste.append([self.ADDON.VSlang(30313), URL_API + 'recommendations/movies'])

            if self.ADDON.getSetting('trakt_movies_show_boxoffice') == 'true':
                liste.append([self.ADDON.VSlang(30314), URL_API + 'movies/boxoffice'])

            if self.ADDON.getSetting('trakt_movies_show_popular') == 'true':
                liste.append([self.ADDON.VSlang(30315), URL_API + 'movies/popular'])

            if self.ADDON.getSetting('trakt_movies_show_most_weekly') == 'true':
                liste.append([self.ADDON.VSlang(30316), URL_API + 'movies/played/weekly'])

            if self.ADDON.getSetting('trakt_movies_show_most_monthly') == 'true':
                liste.append([self.ADDON.VSlang(30317), URL_API + 'movies/played/monthly'])

        elif sType == 'show':
            liste.append(['%s (%s)' % (self.ADDON.VSlang(30310), sHtmlContent['shows']['collected']), URL_API + 'users/me/collection/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_watchlist') == 'true':
                liste.append([self.ADDON.VSlang(30311), URL_API + 'users/me/watchlist/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_watchlist_seasons') == 'true':
                liste.append([self.ADDON.VSlang(30318), URL_API + 'users/me/watchlist/seasons'])

            if self.ADDON.getSetting('trakt_tvshows_show_watchlist_episodes') == 'true':
                liste.append([self.ADDON.VSlang(30319), URL_API + 'users/me/watchlist/episodes'])

            if self.ADDON.getSetting('trakt_tvshows_show_watched') == 'true':
                liste.append(['%s (%s)' % (self.ADDON.VSlang(30312), sHtmlContent['shows']['watched']), URL_API + 'users/me/watched/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_recommended') == 'true':
                liste.append([self.ADDON.VSlang(30313), URL_API + 'recommendations/shows'])

            if self.ADDON.getSetting('trakt_tvshows_show_popular') == 'true':
                liste.append([self.ADDON.VSlang(30315), URL_API + 'shows/popular'])

            if self.ADDON.getSetting('trakt_tvshows_show_most_weekly') == 'true':
                liste.append([self.ADDON.VSlang(30316), URL_API + 'shows/played/weekly'])

            if self.ADDON.getSetting('trakt_tvshows_show_most_monthly') == 'true':
                liste.append([self.ADDON.VSlang(30317), URL_API + 'shows/played/monthly'])

        elif sType == 'custom-lists':
            oRequestHandler = cRequestHandler(URL_API + 'users/me/lists')
            oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
            oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
            oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
            oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
            sHtmlContent = oRequestHandler.request(jsonDecode=True)

            for List in sHtmlContent:
                url = URL_API + 'users/me/lists/' + List['ids']['slug'] + '/items'
                liste.append([self.decode((List['name'] + ' (' + str(List['item_count']) + ')')), url])

        elif sType == 'liked-lists' or sType == 'lists-tendances' or sType == 'lists-pop':
            if sType == 'liked-lists':
                URL = URL_API + '/users/likes/lists'
            elif sType == "lists-tendances":
                URL = URL_API + '/lists/trending'
            elif sType == 'lists-pop':
                URL = URL_API + 'lists/popular'

            oRequestHandler = cRequestHandler(URL)
            oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
            oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
            oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
            oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
            sHtmlContent = oRequestHandler.request(jsonDecode=True)

            for List in sHtmlContent:
                if sType == 'liked-lists':
                    url = URL_API + 'users/' + List['list']['user']['ids']['slug'] + '/lists/' + List['list']['ids']['slug'] + '/items'
                else:
                    url = URL_API + '/lists/' + List['list']['ids']['slug'] + '/items'

                liste.append([self.decode((List['list']['name'] + ' (' + str(List['list']['item_count']) + ')')), url])

        for sTitle, sUrl in liste:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'getTrakt', sTitle, 'genres.png', oOutputParameterHandler)

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

    def getTrakt(self, url2=None):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        if url2:
            sUrl = url2
        else:
            sCurrentLimit = oInputParameterHandler.getValue('limite') 
            sUrl = oInputParameterHandler.getValue('siteUrl')

        sUrl = sUrl + "?page=1&limit=" + MAXRESULT

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        sHtmlContent = oRequestHandler.request(jsonDecode=True)
        sHeaders = oRequestHandler.getResponseHeader()

        # Fonctionnement specifique au calendrier.
        if 'X-Pagination-Page-Count' not in sHeaders:
            if sCurrentLimit == False:
                sCurrentLimit = 0
            else:
                # Supprimer les elements deja afficher.
                sHtmlContent = sHtmlContent[int(sCurrentLimit):]

            if len(sHtmlContent) > 20:
                total = int(MAXRESULT)
            else:
                total = len(sHtmlContent)
        else:
            total = len(sHtmlContent)

        if 'X-Pagination-Page' in sHeaders:
            sPage = sHeaders['X-Pagination-Page']
        if 'X-Pagination-Page-Count' in sHeaders:
            sMaxPage = sHeaders['X-Pagination-Page-Count']

        sKey = 0
        sFunction = 'getLoad'
        sId = SITE_IDENTIFIER
        searchtext = ''
        sTitle = ''
        sOldDate = None
        
        if (total > 0):
            progress_ = progress().VScreate(SITE_NAME)

            for i in sHtmlContent:
                # Limite les elements du calendrier
                if not 'X-Pagination-Page-Count' in sHeaders:
                    if progress_.getProgress() >= int(MAXRESULT):
                        break

                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                if 'collection' in sUrl:

                    try:
                        sDate = i['last_collected_at']
                    except:
                        sDate = ""

                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sYear, sImdb, sTmdb = show['ids']['trakt'], show['year'], show['ids']['imdb'], show['ids']['tmdb']

                        cTrakt.CONTENT = '2'
                        sFunction = 'getBseasons'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sYear, sImdb, sTmdb = movie['ids']['trakt'], movie['year'], movie['ids']['imdb'], movie['ids']['tmdb']
                        
                        cTrakt.CONTENT = '1'
                        sFunction = 'showSearch'
                        sId = 'globalSearch'

                    sTitle = self.decode(sTitle)
                    searchtext = ('%s') % (sTitle)

                    if sYear:
                        sFile = ('%s - (%s)') % (sTitle, int(sYear))
                        sTitle = ('%s - (%s)') % (sTitle, int(sYear))
                    else:
                        sFile = ('%s') % (sTitle)
                        sTitle = ('%s') % (sTitle)

                elif 'history' in sUrl:
                    # commun
                    sFunction = 'showSearch'
                    sId = 'globalSearch'
                    if 'episode' in i:
                        sType = 'Episode'
                        eps = i['episode']
                        sTitle = self.getLocalizedTitle(i, 'episodes')
                        sTrakt, sImdb, sTmdb, sSeason, sNumber = eps['ids']['trakt'], eps['ids']['imdb'], eps['ids']['tmdb'], eps['season'], eps['number']
                        sExtra = ('(S%02dE%02d)') % (sSeason, sNumber)
                        cTrakt.CONTENT = '2'
                    else:
                        sType = 'Film'
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year']
                        sExtra = ('(%s)') % (sYear)
                        cTrakt.CONTENT = '1'

                    sTitle = self.decode(sTitle, Unicode=True)
                    searchtext = ('%s') % (sTitle)
                    sFile = ('%s - (%s)') % (sTitle, sExtra)
                    sTitle = ('[COLOR gold]%s %s [/COLOR]- %s %s') % (sType, 'vu', sTitle, sExtra)

                elif 'watchlist' in sUrl:
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
                    searchtext = ('%s') % (sTitle)
                    sFile = ('%s %s') % (sTitle, sExtra)
                    sTitle = ('%s %s') % (sTitle, sExtra)

                elif 'watched' in sUrl:
                    # commun
                    sPlays = i['plays']
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

                    if sTitle:
                        sTitle = self.decode(sTitle, Unicode=True)
                        searchtext = ('%s') % (sTitle)
                        sFile = ('%s - %s') % (sTitle, sYear)
                        sTitle = ('%s Lectures - %s (%s)') % (sPlays, sTitle, sYear)

                elif 'played' in sUrl:
                    # commun
                    sWatcher_count, sPlay_count, sCollected_count = i['watcher_count'], i['play_count'], i['collected_count']
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
                    searchtext = ('%s') % (sTitle)
                    sFile = ('%s - (%s)') % (sTitle, int(sYear))
                    sTitle = ('%s - (%s)') % (sTitle, int(sYear))

                elif 'calendars' in sUrl:
                    if 'show' in i:
                        show = i['show']
                        sTitle = self.getLocalizedTitle(show, 'shows')
                        sTrakt, sImdb, sTmdb, sYear, sFirst_aired = show['ids']['trakt'], show['ids']['imdb'], show['ids']['tmdb'], show['year'], i['first_aired']
                        sSaison, sEpisode = i['episode']['season'], i['episode']['number']
                        cTrakt.CONTENT = '2'
                    else:
                        movie = i['movie']
                        sTitle = self.getLocalizedTitle(movie, 'movies')
                        sTrakt, sImdb, sTmdb, sYear, sFirst_aired = movie['ids']['trakt'], movie['ids']['imdb'], movie['ids']['tmdb'], movie['year'], i['first_aired']
                        cTrakt.CONTENT = '1'

                    if sTitle:
                        sDate = datetime.datetime(*(time.strptime(sFirst_aired, '%Y-%m-%dT%H:%M:%S.%fZ')[0:6])).strftime('%d-%m-%Y')
                        if sOldDate != sDate:
                            sOldDate = sDate
                            oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Episode prévu pour le :' + sOldDate + '[/COLOR]')

                        sTitle = self.decode(sTitle)
                        searchtext = ('%s') % (sTitle)
                        sFile = sTitle
                        if sYear:
                            sFile += ' - (%s)' % sYear
                        sTitle = ('%s S%02dE%02d') % (self.decode(sTitle,  Unicode=True), sSaison, sEpisode)

                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif 'search' in sUrl:
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
                    searchtext = ('%s') % (sTitle)
                    sFile = ('%s - (%s)') % (sTitle, sYear)
                    sTitle = ('%s (%s)') % (sTitle, sYear)

                elif 'recommendations' in sUrl or 'popular' in sUrl:
                    if 'shows' in sUrl:
                        sTitle = self.getLocalizedTitle(i, 'shows')
                        cTrakt.CONTENT = '2'
                    else:
                        sTitle = self.getLocalizedTitle(i, 'movies')
                        cTrakt.CONTENT = '1'
                    sTrakt, sYear, sImdb, sTmdb = i['ids']['trakt'], i['year'], i['ids']['imdb'], i['ids']['tmdb']
                    sTitle = self.decode(sTitle)
                    searchtext = ('%s') % (sTitle)
                    if sYear:
                        sFile = ('%s - (%s)') % (sTitle, int(sYear))
                        sTitle = ('%s - (%s)') % (sTitle, int(sYear))
                    else:
                        sFile = ('%s') % (sTitle)
                        sTitle = ('%s') % (sTitle)

                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif 'boxoffice' in sUrl:
                    movie = i['movie']
                    sTitle = self.getLocalizedTitle(movie, 'movies')
                    sTrakt, sYear, sImdb, sTmdb = movie['ids']['trakt'], movie['year'], movie['ids']['imdb'], movie['ids']['tmdb']
                    cTrakt.CONTENT = '1'

                    sTitle = self.decode(sTitle)
                    searchtext = ('%s') % (sTitle)
                    sFile = ('%s - (%s)') % (sTitle, int(sYear))
                    sTitle = ('%s - (%s)') % (sTitle, int(sYear))
                    sFunction = 'showSearch'
                    sId = 'globalSearch'

                elif 'lists' in sUrl:

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
                    searchtext = ('%s') % (sTitle)
                    sFile = ('%s %s') % (sTitle, sExtra)
                    sTitle = ('%s %s') % (sTitle, sExtra)

                else:
                    return

                if sTitle:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl + str(sTrakt))
                    oOutputParameterHandler.addParameter('file', sFile)
                    oOutputParameterHandler.addParameter('key', sKey)
                    oOutputParameterHandler.addParameter('searchtext', searchtext)
                    self.getFolder(oGui, sId, sTitle, sFile, sFunction, sImdb, sTmdb, oOutputParameterHandler)
                    sKey += 1

            progress_.VSclose(progress_)

            try:
                if (sPage != sMaxPage):
                    sNextPage = sUrl.replace('page=' + str(sPage), 'page=' + str(int(sPage) + 1))
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                    oGui.addNext(SITE_IDENTIFIER, 'getTrakt', 'Page ' + str(int(sPage) + 1) + '/' + sMaxPage, oOutputParameterHandler)
            except:
                pass

            if not 'X-Pagination-Page-Count' in sHeaders and len(sHtmlContent) > int(MAXRESULT):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('limite', int(sCurrentLimit) + int(MAXRESULT))
                oGui.addNext(SITE_IDENTIFIER, 'getTrakt', 'Page suivante', oOutputParameterHandler)  

        oGui.setEndOfDirectory()

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
                    cTrakt.CONTENT = '2'
                else:
                    return

                sTitle2 = ('%s - (S%02d)') % (self.decode(sFile), int(sNumber))
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl + str(sNumber))
                oOutputParameterHandler.addParameter('Key', sKey)
                oOutputParameterHandler.addParameter('sNum', sNum)
                oOutputParameterHandler.addParameter('file', sFile)
                oOutputParameterHandler.addParameter('title', sTitle2)
                oOutputParameterHandler.addParameter('searchtext', searchtext)
                self.getFolder(oGui, SITE_IDENTIFIER, sTitle2, sFile, 'getBepisodes', '', '', oOutputParameterHandler)
                sNum += 1

        oGui.setEndOfDirectory()

    def getLocalizedTitle(self, item, what):
        try:
            if 'episode' not in what:
                oRequestHandler = cRequestHandler(URL_API + '%s/%s/translations/fr' % (what, item['ids']['slug']))
                oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
                oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
                oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
                oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                sHtmlContent = oRequestHandler.request(jsonDecode=True)
            else:
                show_title = self.getLocalizedTitle(item['show'], 'shows')
                t_values = (item['show']['ids']['slug'], item['episode']['season'], item['episode']['number'])

                oRequestHandler = cRequestHandler(URL_API + 'shows/%s/seasons/%s/episodes/%s/translations/fr' % t_values)
                oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
                oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
                oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
                oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
                sHtmlContent = oRequestHandler.request(jsonDecode=True)

            title = next((title for title in sHtmlContent if title['language'].lower() == 'fr'), item)['title']

            if title is None:
                return item['title']
            else:
                return title if 'episode' not in what else show_title + ' - ' + title

        except:
            try:
                return item['title']
            except:
                return item['show']['title']

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

                    sTitle2 = ('%s (E%02d)') % (self.decode(sTitle), int(sNumber))

                elif 'watched' in sUrl:
                    sNumber, sPlays = i['number'], i['plays']

                    sTitle2 = ('%s Lectures - %s(E%02d)') % (sPlays, self.decode(sTitle), int(sNumber))

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

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sTitle)
        oGuiElement.setFileName(sFile)
        oGuiElement.setIcon('trakt.png')
        oGuiElement.setImdbId(sImdb)
        oGuiElement.setTmdbId(sTmdb)

        if self.ADDON.getSetting('meta-view') == 'false':
            oGuiElement.setMetaAddon('true')

        if cTrakt.CONTENT == '2':
            oGuiElement.setMeta(2)
            oGuiElement.setCat(2)
            cGui.CONTENT = 'tvshows'
        else:
            oGuiElement.setMeta(1)
            oGuiElement.setCat(1)
            cGui.CONTENT = 'movies'

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def getContext(self):

        disp = []
        lang = []
        disp.append(URL_API + 'sync/collection')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30310))

        disp.append(URL_API + 'sync/collection/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]')

        disp.append(URL_API + 'sync/watchlist')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30311))

        disp.append(URL_API + 'sync/watchlist/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]')

        disp.append(URL_API + 'sync/history')
        lang.append(self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30312))

        disp.append(URL_API + 'sync/history/remove')
        lang.append('[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]')

        ret = self.DIALOG.VSselect(lang, 'Trakt')

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

    def getAction(self, Action='', sEpisode = ''):

        if self.ADDON.getSetting('bstoken') == '':
            self.DIALOG.VSinfo('Vous devez être connecté')
            return

        oInputParameterHandler = cInputParameterHandler()

        if not Action == "SetWatched":
            sAction = oInputParameterHandler.getValue('sAction')
            if not sAction:
                sAction = self.getContext()
            if not sAction:
                return

        sType = oInputParameterHandler.getValue('sCat')
        if not sType:
            sType = self.getType()
        # entrer imdb ? venant d'ou?
        sImdb = oInputParameterHandler.getValue('sImdbId')
        sTMDB = oInputParameterHandler.getValue('sTmdbId')
        sSeason = False
        sEpisode = False

        # Film, serie, anime, saison, episode
        if sType not in ('1', '2', '3', '4', '8'):
            return
        
        sType = sType.replace('1', 'movies').replace('2', 'shows').replace('3', 'shows').replace('4', 'shows').replace('8', 'shows')

        # Mettre en vu automatiquement.
        if Action == "SetWatched":
            sFileName = oInputParameterHandler.getValue('sFileName')

            if sType == "shows":
                if self.ADDON.getSetting('trakt_tvshows_activate_scrobbling') == 'false':
                    return
                
                sTitle = oInputParameterHandler.getValue('tvshowtitle')
                sSeason = oInputParameterHandler.getValue('sSeason')
                if not sSeason:
                    sSeason = re.search('(?i)( s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))', sTitle).group(2)
                if not sEpisode:
                    sEpisode = oInputParameterHandler.getValue('sEpisode')
                if not sEpisode:
                    sEpisode = re.search('(?i)(?:^|[^a-z])((?:E|(?:\wpisode\s?))([0-9]+(?:[\-\.][0-9\?]+)*))', sFileName).group(2)
            else:
                if self.ADDON.getSetting('trakt_movies_activate_scrobbling') == 'false':
                    return
                sTitle = sFileName

            sAction = URL_API + 'sync/history'

            if not sTitle:
                sTitle = oInputParameterHandler.getValue('sMovieTitle')
        else:
            sTitle = oInputParameterHandler.getValue('sMovieTitle')

        if not sImdb:
            if not sTMDB:
                sTMDB = int(self.getTmdbID(sTitle, sType))

            if not sTMDB:
                return
            sPost = {sType: [{'ids': {'tmdb': sTMDB}}]}
            if sSeason:
                sPost = {sType: [{'ids': {'tmdb': sTMDB}, 'seasons': [{'number': int(sSeason)}]}]}
            if sEpisode:
                sPost = {sType: [{'ids': {'tmdb': sTMDB}, 'seasons': [{'number': int(sSeason), 'episodes': [{'number': int(sEpisode)}]}]}]}
        else:
            sPost = {sType: [{'ids': {'imdb': sImdb}}]}
            
        oRequestHandler = cRequestHandler(sAction)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/json')
        oRequestHandler.addHeaderEntry('trakt-api-key', API_KEY)
        oRequestHandler.addHeaderEntry('trakt-api-version', API_VERS)
        oRequestHandler.addHeaderEntry('Authorization', 'Bearer %s' % self.ADDON.getSetting('bstoken'))
        for a in sPost:
            oRequestHandler.addJSONEntry(a, sPost[a])
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        try:
            if sHtmlContent['added']['movies'] == 1 or sHtmlContent['added']['episodes'] > 0 or sHtmlContent['added']['shows'] > 0:
                sText = 'Ajouté avec succès'
        except:
            pass

        try:
            if sHtmlContent['updated']['movies'] == 1 or sHtmlContent['updated']['episodes'] > 0 or sHtmlContent['updated']['shows'] > 0:
                sText = 'Mise à jour avec succès'
        except:
            pass

        try:
            if sHtmlContent['deleted']['movies'] == 1 or sHtmlContent['deleted']['episodes'] > 0:
                sText = 'Supprimé avec succès'
        except:
            pass

        try:
            if sHtmlContent['existing']['movies'] > 0 or sHtmlContent['existing']['episodes'] > 0 or sHtmlContent['existing']['seasons'] > 0 or sHtmlContent['existing']['shows'] > 0:
                sText = 'Entrée déjà présente'
        except:
            pass

        try:
            self.DIALOG.VSinfo(sText, 'trakt')
        except UnboundLocalError:
            self.DIALOG.VSinfo("Erreur")

        if (oInputParameterHandler.exist('sReload')):
            xbmc.executebuiltin('Container.Refresh')
        return

    def createContexTrakt(self, oGui, oGuiElement, oOutputParameterHandler=''):

        liste = []
        liste.append(['[COLOR teal]' + self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]', URL_API + 'sync/collection'])
        liste.append(['[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30310) + '[/COLOR]', URL_API + 'sync/collection/remove'])
        liste.append(['[COLOR teal]' + self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]', URL_API + 'sync/watchlist'])
        liste.append(['[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30311) + '[/COLOR]', URL_API + 'sync/watchlist/remove'])
        liste.append(['[COLOR teal]' + self.ADDON.VSlang(30221) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]', URL_API + 'sync/history'])
        liste.append(['[COLOR red]' + self.ADDON.VSlang(30222) + ' ' + self.ADDON.VSlang(30312) + '[/COLOR]', URL_API + 'sync/history/remove'])

        for sTitle, sUrl in liste:
            oOutputParameterHandler = cOutputParameterHandler()
            if cTrakt.CONTENT == '2':
                oOutputParameterHandler.addParameter('sType', 'shows')
            else:
                oOutputParameterHandler.addParameter('sType', 'movies')
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sAction', sUrl)
            oOutputParameterHandler.addParameter('sReload', True)
            # oOutputParameterHandler.addParameter('sImdb', oGuiElement.getImdbId())
            oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cTrakt', 'cTrakt', 'getAction', sTitle)
        return

    def showHosters(self):

        oInputParameterHandler = cInputParameterHandler()
        sMovieTitle = oInputParameterHandler.getValue('file')
        sMovieTitle = self.decode(sMovieTitle, Unicode=True).lower()  # on repasse en utf-8
        sMovieTitle = Quote(sMovieTitle)
        sMovieTitle = re.sub('\(.+?\)', ' ', sMovieTitle)  # vire les tags entre parentheses

        # modif venom si le titre comporte un - il doit le chercher
        sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)  # vire les caracteres a la con qui peuvent trainer

        sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)', ' ', sMovieTitle)  # vire les articles

        # vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +
        sMovieTitle = re.sub(' +', ' ', sMovieTitle)

        self.vStreamSearch(sMovieTitle)

    def vStreamSearch(self, sMovieTitle):
        oGui = cGui()

        oHandler = cRechercheHandler()
        oHandler.setText(sMovieTitle)
        aPlugins = oHandler.getAvailablePlugins()

        oGui.setEndOfDirectory()

    def getTmdbInfo(self, sTmdb, oGuiElement):

        return

        if not sTmdb:
            VSlog('Problème sTmdb')
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

    def getTmdbID(self, sTitle, sType):

        oInputParameterHandler = cInputParameterHandler()

        from resources.lib.tmdb import cTMDb
        grab = cTMDb()

        if sType == 'shows':
            sType = 'tv'
        elif sType == 'movies':
            sType = 'movie'

        meta = 0
        year = ''
        # on cherche l'annee
        r = re.search('(\([0-9]{4}\))', sTitle)
        if r:
            year = str(r.group(0))
            sTitle = sTitle.replace(year, '')

        meta = grab.get_idbyname(sTitle, year, sType)

        return int(meta)
