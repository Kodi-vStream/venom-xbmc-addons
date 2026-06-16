# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.parser import cParser
import json
import time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vidara', 'Vidara')

    def _getMediaLinkForGuest(self):
        url = self._url
        filecode = url.split('/')[-1]
        host = url.split('/')[2]
        api_url = "https://%s/api/stream" % host
        
        try:
            oRequest = cRequestHandler(url)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.request()
            cookie = oRequest.GetCookies()
            
            time.sleep(1.5)
            
            oRequest = cRequestHandler(api_url)
            oRequest.setRequestType(1) 
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', url)
            oRequest.addHeaderEntry('Cookie', cookie)
            oRequest.addHeaderEntry('Content-Type', 'application/json')
            oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            
            post_data = {"filecode": filecode, "device": "android"}
            oRequest.addParametersLine(json.dumps(post_data))
            
            json_response = oRequest.request()
            
            result = json.loads(json_response)
            
            if 'streaming_url' in result:
                final_link = result['streaming_url'] + '|User-Agent=' + UA + '&Referer=' + url + '&Cookie=' + cookie
                return True, final_link
            else:
                return False, False
                
        except:
            pass
            
            return False, False

    def getMediaLink(self):
        return self._getMediaLinkForGuest()
