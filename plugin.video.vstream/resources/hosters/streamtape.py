# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamtape', 'Streamtape')

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        self._url = self._url.replace('streamtape', 'tapepops')

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        cookie = oRequest.GetCookies()

        sPattern1 = 'ById\(\'ideoo.+?=\s*["\']([^"\']+)[\'"].+?["\']([^"\']+)\'\)'
        aResult = oParser.parse(sHtmlContent, sPattern1)

        if aResult[0] is True:
            url = aResult[1][0][1]
            if '?' in url:
                api_call = 'https://tapepops.com/get_video' + url[url.find('?'):] + "&stream=1"
            else:
                api_call = 'https://tapepops.com/get_video?id=' + url + "&stream=1"

            api_call = getLocation(api_call, cookie)
            if api_call:
                return True, api_call + '|Referer=' + api_call

        return False, False
    
    
def getLocation(url, c):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.disableRedirect()
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Cookie', c)
    oRequestHandler.request()
    
    response = oRequestHandler.getResponseHeader()
    if 'location' in response:
        return response['Location']
    return False

