# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import urlEncode
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster
import urllib.parse
import ast  

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'filelions', 'FileLions')

    def _getMediaLinkForGuest(self):
        oParser = cParser()
        
        sBaseUrl = '/'.join(self._url.split('/')[:3]) + '/'
        sOrigin = sBaseUrl.rstrip('/')
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

        if not aResult[0] is True:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\s*)<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                sHtmlContent2 = cPacker().unpack(aResult[1][0])
                
                sPattern = '"hls2":"([^"]+)"'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                
                if not aResult[0] is True:
                    sPattern = '"hls4":"([^"]+)"'
                    aResult = oParser.parse(sHtmlContent2, sPattern)
                    
                    if aResult[0] is True:
                        api_call_raw = aResult[1][0]
                        api_call = sOrigin + api_call_raw

                    else:
                        api_call = None
                else:
                    api_call = aResult[1][0]

        if api_call:
            headers = {
                'User-Agent': UA,
                'Referer': self._url,
                'Origin': sOrigin,
                'Accept': '*/*',
                'Accept-Language': 'fr-FR,fr;q=0.9',
                'Cookie': cookies  
            }

            return True, api_call + '|' + urlEncode(headers) + '&verifypeer=false'

        return False, False
