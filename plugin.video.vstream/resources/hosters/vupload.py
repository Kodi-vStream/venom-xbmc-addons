# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vupload', 'Vupload')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = '{src:\s*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
