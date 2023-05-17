# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.hosters.hoster import iHoster
# from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamhide', 'StreamHide')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        # VSlog(sHtmlContent)

        sPattern = '{file:"([^"]+)"}]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]
            return True, api_call

        return False, False
