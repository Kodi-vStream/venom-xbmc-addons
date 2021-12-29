#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'stagevu', 'Stagevu')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '<embed type=".+?" src="([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)


        if aResult[0] is True:
            api_call = aResult[1][0]
            return True, api_call

        return False, False
