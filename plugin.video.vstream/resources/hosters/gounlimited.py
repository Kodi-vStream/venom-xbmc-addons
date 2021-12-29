# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://gounlimited.to/embed-xxx.html
# top_replay robin des droits
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'gounlimited', 'Gounlimited')

    def _getMediaLinkForGuest(self):
        api_call = False

        if not self._url.endswith('.mp4'):
            oParser = cParser()
            oRequest = cRequestHandler(self._url)
            sHtmlContent = oRequest.request()

            sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern = '{src:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)

                # fh = open('c:\\test.txt', 'w')
                # fh.write(sHtmlContent)
                # fh.close()

                if aResult[0] is True:
                    api_call = aResult[1][0]
        else:
            api_call = self._url

        if api_call.endswith('.mp4'):
            return True, api_call
        else:
            return True, api_call + '|User-Agent=' + UA

        return False, False
