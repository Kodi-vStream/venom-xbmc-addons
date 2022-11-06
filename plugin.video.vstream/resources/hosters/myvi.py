# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.myvi.tv/embed/xxxxxxxxx
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import Unquote

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'myvi', 'Myvi')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request().replace('\\u0026', '&')
        cookies = oRequest.GetCookies()# + ";"
        
        sPattern = 'CreatePlayer.+?v=(.+?)&tp'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = Unquote(aResult[1][0])
        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&Cookie=' + cookies

        return False, False
