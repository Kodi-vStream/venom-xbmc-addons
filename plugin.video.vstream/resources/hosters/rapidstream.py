#-*- coding: utf-8 -*-
#https://rapidstream.co/embed-zxxx-635x445.html tfarjo twd
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rapidstream', 'Rapidstream')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = '"(http[^"]+(?:.m3u8|.mp4))"'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][1]

        if api_call:
            return True, api_call

        return False, False
