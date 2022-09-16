# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'downace', 'Downace')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        # sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        # aResult = oParser.parse(sHtmlContent,sPattern)
        # if aResult[0] is True:
        #    sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = 'controls preload="none" src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]  # pas de choix qualité trouvé pour le moment

        if api_call:
            return True, api_call

        return False, False
