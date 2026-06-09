# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker
import re

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'swish', 'Swish')

    def _getMediaLinkForGuest(self):
        web_url = self._url
        sBaseUrl = '/'.join(web_url.split('/')[:3]) + '/'
        
        oRequest = cRequestHandler(web_url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', sBaseUrl)
        
        sHtmlContent = oRequest.request()
        sPattern = r"(\s*eval\s*\(\s*function(?:.|\s)+?)\s*<\/script>"
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            sHtmlContent = cPacker().unpack(aResult[0])
            
        source = None
        match = re.search(r'["\'](https?://[^"\']+\.m3u8[^"\']*)["\']', sHtmlContent)
        if match:
            source = match.group(1)
        
        if source:
            sHeaderAppend = '|User-Agent=' + UA + '&Referer=' + sBaseUrl
            return True, source + sHeaderAppend
            
        return False, False
