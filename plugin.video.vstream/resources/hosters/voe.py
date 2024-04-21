# coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import base64


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        aResult1 = base64.b64decode(aResult[1][0])

        if aResult1:

            api_call = aResult1.decode("utf-8")

        if api_call:
            return True, api_call

        return False, False
