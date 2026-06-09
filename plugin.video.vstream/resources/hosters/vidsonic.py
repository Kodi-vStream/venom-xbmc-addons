# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
import re
import binascii

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vidsonic', 'Vidsonic')

    def _getMediaLinkForGuest(self):
        url = self._url.replace('/embed-', '/e/')       
        base_url = re.search(r'(https?://[^/]+)', url).group(1)
        ref = base_url + '/'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Referer': ref,
            'Origin': ref[:-1] 
        }

        oRequest = cRequestHandler(url)
        for key, value in headers.items():
            oRequest.addHeaderEntry(key, value)
            
        sHtmlContent = oRequest.request()

        r = re.search(r"const\s*_0x1\s*=\s*'([^']+)", sHtmlContent)
        
        if r:
            try:
                hex_data = r.group(1).replace('|', '')
                src = binascii.unhexlify(hex_data).decode()[::-1]
                
                final_link = src + '|' + '&'.join(['%s=%s' % (k, v) for k, v in headers.items()])
                return True, final_link
            except:
                pass
            
        return False, False

    def getMediaLink(self):
        return self._getMediaLinkForGuest()
