# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import urlEncode

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lulustream', 'Lulustream')

    def _getMediaLinkForGuest(self):
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9')
        oRequest.addHeaderEntry('Sec-Fetch-Dest', 'document')
        oRequest.addHeaderEntry('Sec-Fetch-Mode', 'navigate')
        oRequest.addHeaderEntry('Sec-Fetch-Site', 'none')
        oRequest.addHeaderEntry('Sec-Fetch-User', '?1')
        sHtmlContent = oRequest.request()

        cookies = oRequest.GetCookies()

        sPattern = 'sources:\\s*\\[\\{file:\\s*["\']([^"\']+\\.m3u8[^"\']*)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = aResult[1][0].replace('&', '&')

            headers = {
                'User-Agent': UA,
                'Referer': self._url,
                'Origin': 'https://luluvdo.com',
                'Accept': '*/*',
                'Accept-Language': 'fr-FR,fr;q=0.9',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'sec-ch-ua': '"Chromium";v="138", "Google Chrome";v="138", "Not(A:Brand";v="8"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Cookie': cookies
            }

            return True, api_call + '|' + urlEncode(headers)

        return False, False
