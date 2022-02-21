# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
    'Chrome/83.0.4103.116 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamlare', 'Streamlare')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequestHandler = cRequestHandler("https://streamlare.com/api/video/get")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://{0}'.format(self._url.split('/')[2]))
        oRequestHandler.addJSONEntry('id', self._url.split('/')[4])
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        api_call = sHtmlContent['result']['Original']['src']

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
