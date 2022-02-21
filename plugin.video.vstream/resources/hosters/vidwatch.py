#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidwatch', 'VidWatch')

    def _getMediaLinkForGuest(self):
        api_call =''

        #VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'file:"([^"]+.mp4)",label:"([0-9]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        #VSlog(str(aResult))
        if aResult[0] is True:
            api_call = aResult[1][0][0]

        #VSlog(api_call)

        if api_call:
            return True, api_call

        return False, False
