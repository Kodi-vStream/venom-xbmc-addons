# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'facebook', 'Facebook')

    def _getMediaLinkForGuest(self):

        qua = []
        url = []
        api_call = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = '((?:h|s)d)_src:"([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            for aEntry in aResult[1]:
                qua.append(str(aEntry[0]))
                url.append(str(aEntry[1]))

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
