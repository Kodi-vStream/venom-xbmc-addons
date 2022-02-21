#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
#from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbom', 'Vidbom')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = 'sources: *\[{file:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]
        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\))'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern = '{file:"([^"]+.mp4)"'
                aResult = oParser.parse(sHtmlContent,sPattern)
                if aResult[0] is True:
                    api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
