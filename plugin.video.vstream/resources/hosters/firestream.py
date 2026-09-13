# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

import json

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'firestream', 'Firestream')

    def __getHost(self, url):
        parts = url.split('//', 1)
        host = parts[1].split('/', 1)[0]
        return host

    def __getId(self, url):
        return url.split('/')[-1]

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'id="token-blob"[^>]+>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:

            host = self.__getHost(self._url)
            id = self.__getId(self._url)
            url = "https://" + host + "/api/videos/" + id + "/resolve"
            
            oRequest = cRequestHandler(url)
            oRequest.setRequestType(1)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self._url)
            oRequest.addHeaderEntry('Origin', "https://" + host)
            oRequest.addHeaderEntry('Accept', 'application/json, text/plain, */*')
            oRequest.addHeaderEntry('Content-Type', 'application/json;charset=utf-8')
            
            post_data = {"blob": aResult[1][0]}
            oRequest.addParametersLine(json.dumps(post_data))
            
            json_response = oRequest.request()
            
            if json_response:
                result = json.loads(json_response)
                
                if 'signedVideoUrl' in result:
                    api_call = result['signedVideoUrl']# + '|User-Agent=' + UA + "&Referer=" + self._url + "&Origin=" + "https://" + host

        if api_call:
            return True, api_call

        return False, False
