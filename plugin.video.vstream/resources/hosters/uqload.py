# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://uqload.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uqload', 'Uqload')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern1 = 'sources.+?"([^"]+mp4)"'

        aResult = oParser.parse(sHtmlContent, sPattern1)
        if aResult[0] is True:
            api_call = aResult[1][0]
        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\))<'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sUnpacked = cPacker().unpack(aResult[1][0])
                sHtmlContent = sUnpacked
                
                sPattern1 = 'file:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern1)
                if aResult[0] is True:
                    for url in aResult[1]:
                        if "mp4" in url or "m3u8" in url:
                            api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
