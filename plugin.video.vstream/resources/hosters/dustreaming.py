# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dustreaming', 'Dustreaming')

    def _getMediaLinkForGuest(self):
        api_call = ''

        url = self._url.replace('/v/', '/api/source/')
        oRequest = cRequestHandler(url)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParameters('r', '')
        oRequest.addParameters('d', 'dustreaming.fr')
        
        try:
            sHtmlContent = oRequest.request()
            # Check if response is empty or invalid
            if not sHtmlContent:
                VSlog("DustStreaming Error - Empty response from API")
                return False, False
            
            sHtmlContent = sHtmlContent.strip()
            if not sHtmlContent.startswith('{') and not sHtmlContent.startswith('['):
                VSlog("DustStreaming Error - Response is not JSON format: %s" % sHtmlContent[:100])
                return False, False
            
            # Try to parse JSON with better error handling
            try:
                page = json.loads(sHtmlContent)
            except json.JSONDecodeError as e:
                VSlog("DustStreaming Error - JSON decode error: %s" % str(e))
                VSlog("DustStreaming Error - Failed response content: %s" % sHtmlContent)
                return False, False

            if page and 'data' in page:
                url_list = []
                qua = []
                for x in page['data']:
                    url_list.append(x['file'])
                    qua.append(x['label'])

                if url_list:
                    api_call = dialog().VSselectqual(qua, url_list)
            else:
                VSlog("DustStreaming Error - No 'data' key in JSON response: %s" % str(page))
                return False, False

        except Exception as e:
            VSlog("DustStreaming Error - General exception: %s" % str(e))
            return False, False

        if api_call:
            return True, api_call

        return False, False
