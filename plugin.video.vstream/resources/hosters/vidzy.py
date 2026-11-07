# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0'
class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidzy', 'Vidzy')

    def __getHost(self):
        parts = self._url.split('//', 1)
        host = parts[1].split('/', 1)[0]
        return host

    def __getIdFromUrl(self):
        sPattern = "vidzy.[a-z]+/(?:embed-|)([0-9a-zA-Z]+)(?:.html|)"
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0]:
            return aResult[1][0]

        return ''  

    def _getMediaLinkForGuest(self):
        api_call = ''
        ID = self.__getIdFromUrl()
        if not ID:
            return False, False

        url = ('https://%s/d/%s_n.html' % (self.__getHost(), ID))
        host = self.__getHost()
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', host)
        
        sHtmlContent = oRequest.request()
        oParser = cParser()

        sPattern = '<input type="hidden"\s*name="([^"]+)"\s*value="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oRequest = cRequestHandler(url)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', host)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])
                
            sHtmlContent = oRequest.request()
            sPattern = '<a\s*href="([^"]+)"\s*class="main-button"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                #VSlog(aResult)
                api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
