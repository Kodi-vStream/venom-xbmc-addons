#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'turbovid', 'Turbovid.net')

    def __getIdFromUrl(self, url):
        sPattern = "http://turbovid.net/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(url, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        if 'embed' not in sUrl:
            self._url = str(self.__getIdFromUrl(sUrl))
            self._url = 'http://turbovid.net/embed-'+str(self._url)+'.html'
        else:
            self._url = sUrl

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        if not sHtmlContent:
            return False, False

        sPattern = 'var/type/(.+?)/.+?/provider/mp4/([^<]+)/flash/';

        oParser = cParser()
        sHtmlContent=sHtmlContent.replace('|','/')
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = ('http://178.33.122.207:%s/%s/v.mp4') % (aResult[1][0][0], aResult[1][0][1])
            return True, api_call

        return False, False
