# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
# meme code que gorillavid


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'daclips', 'Daclips')

    def __getIdFromUrl(self):
        sPattern = 'http://daclips.in/embed-([^<]+)-'
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0] is True:
            return aResult[1][0]
        return ''

    def _getMediaLinkForGuest(self, api_call=None):
        oParser = cParser()

        sId = self.__getIdFromUrl()

        url = 'http://daclips.in/' + sId
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        sPattern = '<input type="hidden" name="([^"]+)" value="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])
            oRequest.addParameters('referer', url)
            sHtmlContent = oRequest.request()
            r2 = re.search('file: "([^"]+)",', sHtmlContent)
            if r2:
                api_call = r2.group(1)

        if api_call:
            return True, api_call

        return False, False
