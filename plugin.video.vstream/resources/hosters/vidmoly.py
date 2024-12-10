# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib import util


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidmoly', 'VidMoly')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = 'sources: *\[{file:"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]
            api_call = api_call.replace(',', '').replace('.urlset', '')
            api_call = api_call + '|Referer=' + util.urlHostName(self._url)
            return True, api_call

        return False, False
