#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidfast', 'Vidfast')

    def _getMediaLinkForGuest(self):
        api_call = ''

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '{file:"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0].replace(',','').replace('master.m3u8','index-v1-a1.m3u8')

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=https://vidfast.co'

        return False, False
