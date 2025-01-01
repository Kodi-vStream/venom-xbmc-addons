# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib import util

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidmoly', 'VidMoly')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addHeaderEntry('Sec-Fetch-Dest', "iframe")
        sHtmlContent = oRequest.request()

        sPattern = 'sources: *\[{file:"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]
            api_call = api_call.replace(',', '').replace('.urlset', '')
            api_call = api_call + '|Referer=' + util.urlHostName(self._url)
            return True, api_call

        return False, False
