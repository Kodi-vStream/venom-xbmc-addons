# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import requests

from resources.hosters.youtube import cHoster
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
from resources.lib.config import GestionCookie

UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

try:
    import json
except:
    import simplejson as json

SITE_IDENTIFIER = 'cBA'
SITE_NAME = 'BA'


class cShowBA:
    def __init__(self):
        self.sTrailerUrl = ''  # fournie par les metadata
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
                trailer_id = sTrailerUrl.split('=')[1]
                self.sTrailerUrl = 'http://www.youtube.com/watch?v=' + trailer_id
            except:
                pass

    def SetMetaType(self, metaType):
        self.metaType = str(metaType).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'movie')\
                                     .replace('4', 'tvshow').replace('5', 'tvshow').replace('6', 'tvshow')

    def SearchBA(self, window=False):

        sSearchTitle = self.search + ' - Bande Annonce VF'
        if self.year:
            sSearchTitle += ' (%s)' % self.year

        # Le lien sur la BA est déjà connu
        urlTrailer = self.sTrailerUrl

        # Sinon recherche de la BA officielle dans TMDB
        if not urlTrailer:
            from resources.lib.tmdb import cTMDb
            meta = cTMDb().get_meta(self.metaType, self.search, year=self.year)
            if 'trailer' in meta and meta['trailer']:
                self.SetTrailerUrl(meta['trailer'])
                urlTrailer = self.sTrailerUrl

        # Sinon recherche dans youtube
        if not urlTrailer:
            headers = {'User-Agent': UA}

            url = 'https://www.youtube.com/results'

            sHtmlContent = requests.get(url,
                                        params={'search_query': sSearchTitle},
                                        cookies={'CONSENT': GestionCookie().Readcookie("youtube")},
                                        headers=headers).text

            try:
                result = re.search('{"videoRenderer":{"videoId":"([^"]+)', str(sHtmlContent)).group(1)
            except:
                result = re.search('{"videoRenderer":{"videoId":"([^"]+)', sHtmlContent.encode('utf-8')).group(1)

            if result:
                # Premiere video trouvée
                urlTrailer = 'https://www.youtube.com/watch?v=' + result

        # BA trouvée
        if urlTrailer:
            hote = cHoster()
            hote.setUrl(urlTrailer)
            # hote.setResolution('720p') Pas utilisé
            api_call = hote.getMediaLink()[1]

            if not api_call:
                return

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(sSearchTitle)
            oGuiElement.setMediaUrl(api_call)
            oGuiElement.setThumbnail(oGuiElement.getIcon())

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer(window)

        return
