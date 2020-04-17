# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
from resources.lib.comaddon import addon, dialog
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
        self.search = ''
        self.key = 'AIzaSyC5grY-gOPMpUM_tn0sfTKV3pKUtf9---M'

    def SetSearch(self, search):
        self.search = search.replace(' ', '+')
        self.search =  self.search + '+bande+annonce'

    def SearchBA_old(self):

            url = 'https://www.googleapis.com/youtube/v3/search?part=id,snippet&q=%s&maxResults=1&relevanceLanguage=fr&key=%s' % (self.search, self.key)

            req = urllib2.Request(url)

            try:
                gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
                response = urllib2.urlopen(req, context = gcontext)
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
        self.url = 'https://www.youtube.com/results?q=' + self.search + '&sp=EgIYAQ%253D%253D'

        oRequestHandler = cRequestHandler(self.url)
        sHtmlContent = oRequestHandler.request()

        list = re.findall('"url":"\/watch\?v=([^"]+)"', sHtmlContent)

        if list:
            url = 'http://www.youtube.com/watch?v=' + list[0]
            exec 'from resources.hosters.youtube import cHoster'
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

        return
