# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
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
        base_url = "https://%s/" % host
        
        try:
            # 1. Obtention des cookies initiaux de la page
            oRequest = cRequestHandler(url)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.request()
            cookie = oRequest.GetCookies()
            
            time.sleep(1.5)
            
            # 2. Requête POST vers l'API
            oRequest = cRequestHandler(api_url)
            oRequest.setRequestType(1) 
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', base_url)
            oRequest.addHeaderEntry('Origin', base_url.rstrip('/'))
            oRequest.addHeaderEntry('Accept', 'application/json, text/plain, */*')
            if cookie:
                oRequest.addHeaderEntry('Cookie', cookie)
            oRequest.addHeaderEntry('Content-Type', 'application/json;charset=utf-8')
            oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            
            post_data = {"filecode": filecode, "device": "ios"}
            oRequest.addParametersLine(json.dumps(post_data))
            
            json_response = oRequest.request()
            
            if json_response:
                result = json.loads(json_response)
                
                if 'streaming_url' in result:
                    stream_url = result['streaming_url']
                    
                    # 3. Formatage du lien final avec le bon Referer de base racine
                    final_link = stream_url + '|User-Agent=' + UA + '&Referer=' + base_url + '&Content-Type=application/vnd.apple.mpegurl&verifypeer=false'
                    return True, final_link
                    
        except Exception:
            pass
            
        return False, False

    def getMediaLink(self):
        return self._getMediaLinkForGuest()