# coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import base64


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            aResult1 = base64.b64decode(aResult[1][0])
            if aResult1:
                api_call = aResult1.decode("utf-8")
        else:
            sPattern = " let .+?= '([^']+)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                aResult1 = base64.b64decode(aResult[1][0])
                aResult1 = aResult1[::-1]
                if aResult1:
                    sPattern = '"file":"([^"]+)"'
                    aResult = oParser.parse(aResult1, sPattern)
                    if aResult[0]:
                        api_call = aResult[1][0].replace('\\','')
        
        if api_call:
            return True, api_call

        return False, False
