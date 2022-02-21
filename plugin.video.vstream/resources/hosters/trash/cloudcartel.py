#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#https://cloudcartel.net/embed/video/xxx
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

sPattern1 = '"url":"([^"]+)",'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cloudcartel', 'CloudCartel')

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('cloudcartel.net/embed/video/', 'cloudcartel.vnadigital.com/download/link/')
        #suivre

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        aResult = oParser.parse(sHtmlContent, sPattern1)
        if aResult[0] is True:
            api_call = aResult[1][0]


        if api_call:
            return True, api_call

        return False, False
