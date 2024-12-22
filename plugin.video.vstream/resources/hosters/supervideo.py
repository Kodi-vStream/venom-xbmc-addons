# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'supervideo', 'SuperVideo')

    def _getMediaLinkForGuest(self):
        api_call = False

        if self._url.startswith('/'):
            self._url = 'https:' + self._url
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"([^<>"]+?\.mp4).+?label:"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))
    
                # Choix des qualités
                api_call = dialog().VSselectqual(qua, url)
            else:
                sPattern = 'file:"([^"]+)'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    api_call = aResult[1][0]
        if api_call:
            return True, api_call

        return False, False
