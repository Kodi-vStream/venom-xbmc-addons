# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://vidplayer.cz/v/xxxxxxx
import json

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vidplayer', 'Vidplayer')

    def _getMediaLinkForGuest(self):
        req = self._url.replace('/v/', '/api/source/')
        pdata = 'r'
        oRequestHandler = cRequestHandler(req)
        oRequestHandler.setRequestType(1)

        oRequestHandler.addParametersLine(pdata)
        
        try:
            sHtmlContent = oRequestHandler.request()
            # Check if response is empty or invalid
            if not sHtmlContent:
                VSlog("VidPlayer Error - Empty response from API")
                return False, False
            
            sHtmlContent = sHtmlContent.strip()
            if not sHtmlContent.startswith('{') and not sHtmlContent.startswith('['):
                VSlog("VidPlayer Error - Response is not JSON format: %s" % sHtmlContent[:100])
                return False, False
            
            # Try to parse JSON with better error handling
            try:
                jsonrsp = json.loads(sHtmlContent)
            except json.JSONDecodeError as e:
                VSlog("VidPlayer Error - JSON decode error: %s" % str(e))
                VSlog("VidPlayer Error - Failed response content: %s" % sHtmlContent)
                return False, False

            if not jsonrsp or 'data' not in jsonrsp:
                VSlog("VidPlayer Error - No 'data' key in JSON response: %s" % str(jsonrsp))
                return False, False

            list_url = []
            list_q = []

            for idata in range(len(jsonrsp['data'])):
                url = jsonrsp['data'][idata]['file']
                stype = jsonrsp['data'][idata]['type']
                q = jsonrsp['data'][idata]['label']
                list_url.append(url + '.' + stype)
                list_q.append(q)

            if list_url:
                api_call = dialog().VSselectqual(list_q, list_url)

            if api_call:
                return True, api_call

        except Exception as e:
            VSlog("VidPlayer Error - General exception: %s" % str(e))
            return False, False

        return False, False
