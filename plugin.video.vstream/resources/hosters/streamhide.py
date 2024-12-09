# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamhide', 'StreamHide')

    def _getMediaLinkForGuest(self):
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = '{file:"([^"]+)"}]'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                return True, aResult[1][0]

        return False, False
