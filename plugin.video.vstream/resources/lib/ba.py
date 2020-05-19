# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
from resources.lib.comaddon import addon, dialog
from resources.lib.tmdb import cTMDb
from resources.lib.util import QuotePlus
import urllib2
import ssl
import re

try:
    import json
except:
    import simplejson as json

SITE_IDENTIFIER = 'cBA'
SITE_NAME = 'BA'


class cShowBA:

    def __init__(self):
        self.sTrailerUrl = ''    # fournie par les metadata
        self.search = ''
        self.year = ''
        self.metaType = 'movie'
        self.key = 'AIzaSyC5grY-gOPMpUM_tn0sfTKV3pKUtf9---M'

    def SetSearch(self, search):
        self.search = search

    def SetYear(self, year):
        if year:
            self.year = year

    def SetTrailerUrl(self, sTrailerUrl):
        if sTrailerUrl:
            try:
                trailer_id = sTrailerUrl.split('=')[2]
                self.sTrailerUrl = 'http://www.youtube.com/watch?v=' + trailer_id
            except:
                pass

    def SetMetaType(self, metaType):
        self.metaType = str(metaType).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'movie')

    def SearchBA_old(self):
            url = 'https://www.googleapis.com/youtube/v3/search?part=id,snippet&q=%s&maxResults=1&relevanceLanguage=fr&key=%s' % (self.search, self.key)
            req = urllib2.Request(url)

            try:
                gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
                response = urllib2.urlopen(req, context=gcontext)
            except:
                response = urllib2.urlopen(req)
            sHtmlContent = response.read()
            result = json.loads(sHtmlContent)
            response.close()

            try:
                ids = result['items'][0]['id']['videoId']

                url = 'http://www.youtube.com/watch?v=%s' % ids
                from resources.hosters.youtube import cHoster
                hote = cHoster()
                hote.setUrl(url)
                api_call = hote.getMediaLink()[1]
                if not api_call:
                    return

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setTitle(self.search.replace('+', ' '))
                oGuiElement.setMediaUrl(api_call)
                oGuiElement.setThumbnail(oGuiElement.getIcon())

                oPlayer = cPlayer()
                oPlayer.clearPlayList()
                oPlayer.addItemToPlaylist(oGuiElement)
                oPlayer.startPlayer()

            except:
                dialog().VSinfo(addon().VSlang(30204))
                return
            return

    def SearchBA(self):

        sTitle = self.search + ' - Bande Annonce'

        # Le lien sur la BA est déjà connu
        urlTrailer = self.sTrailerUrl

        # sinon
        if not urlTrailer:
            # si c'est un film, rcherche de la BA officielle dans TMDB
            if self.metaType == 'movie':
                meta = cTMDb().get_meta(self.metaType, self.search, year=self.year)
                if meta and 'trailer_url' in meta:
                    urlTrailer = meta['trailer_url']

            # sinon recherche dans youtube
            if not urlTrailer:
                urlTrailer = 'https://www.youtube.com/results?q=' + QuotePlus(sTitle) + '&sp=EgIYAQ%253D%253D'

                oRequestHandler = cRequestHandler(urlTrailer)
                sHtmlContent = oRequestHandler.request()

                listResult = re.findall('"url":"\/watch\?v=([^"]+)"', sHtmlContent)
                if listResult:
                    # Premiere video trouvée
                    urlTrailer = 'http://www.youtube.com/watch?v=' + listResult[0]

        # BA trouvée
        if urlTrailer:
            exec('from resources.hosters.youtube import cHoster')
            hote = cHoster()
            hote.setUrl(urlTrailer)
            api_call = hote.getMediaLink()[1]
            if not api_call:
                return

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(sTitle)
            oGuiElement.setMediaUrl(api_call)
            oGuiElement.setThumbnail(oGuiElement.getIcon())

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()

        return
