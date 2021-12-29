#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megadrive', 'Megadrive')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()


        sPattern = "<source.+?src='([^']+)'"
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0] #pas de choix qualité trouvé pour le moment

        if api_call:
            return True, api_call

        return False, False
