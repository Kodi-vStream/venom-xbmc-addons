#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#test sur http://vshare.eu/embed-wuqinr62cpn6-703x405.html
#         http://vshare.eu/embed-cxmr4o8l2waa-703x405.html
#         http://vshare.eu/embed-cxmr4o8l2waa703x405.html erreur code streambb
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vshare', 'Vshare')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        self._url = re.sub('-*\d{3,4}x\d{3,4}', '', self._url)
        self._url = self._url.replace('https', 'http')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        if '<div id="deleted">' in sHtmlContent:
            return False, False

        oParser = cParser()
        sPattern = '<source src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]
        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern = '{file:"(http.+?vid.mp4)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] is True:
                    api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
