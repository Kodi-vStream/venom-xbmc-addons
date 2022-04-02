# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'mixdrop', 'Mixdrop')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace("/f/", "/e/")

    def _getMediaLinkForGuest(self):
        api_call = ''

        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Cookie', 'hds2=1')
        sHtmlContent = oRequest.request()

        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'wurl="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0]

            if api_call.startswith('//'):
                api_call = 'https:' + aResult[1][0]

            if api_call:
                return True, api_call

        return False, False
