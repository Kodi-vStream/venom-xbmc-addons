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
        
        # Enhanced debugging - log the API request details
        VSlog("DustStreaming Debug - API URL: %s" % url)
        VSlog("DustStreaming Debug - Referer: %s" % self._url)
        
        try:
            sHtmlContent = oRequest.request()
            VSlog("DustStreaming Debug - Raw response length: %d" % len(sHtmlContent) if sHtmlContent else 0)
            VSlog("DustStreaming Debug - Raw response preview: %s" % sHtmlContent[:200] if sHtmlContent else "Empty response")
            
            # Check if response is empty or invalid
            if not sHtmlContent:
                VSlog("DustStreaming Error - Empty response from API")
                dialog().VSerror("Erreur : Réponse vide de l'API (%s)" % url)
                return False, False
            
            if not sHtmlContent.strip().startswith('{') and not sHtmlContent.strip().startswith('['):
                VSlog("DustStreaming Error - Response is not JSON format: %s" % sHtmlContent[:100])
                dialog().VSerror("Erreur : Réponse invalide de l'API (non-JSON)")
                return False, False
            
            # Try to parse JSON with better error handling
            try:
                page = json.loads(sHtmlContent)
                VSlog("DustStreaming Debug - JSON parsed successfully")
            except json.JSONDecodeError as e:
                VSlog("DustStreaming Error - JSON decode error: %s" % str(e))
                VSlog("DustStreaming Error - Failed response content: %s" % sHtmlContent)
                dialog().VSerror("Erreur : Connexion impossible (Expecting value line 1 column 1 (char 0)) %s" % url)
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
                dialog().VSerror("Erreur : Format de réponse API invalide")
                return False, False

        except Exception as e:
            VSlog("DustStreaming Error - General exception: %s" % str(e))
            dialog().VSerror("Erreur : Connexion impossible (%s) %s" % (str(e), url))
            return False, False

        if api_call:
            return True, api_call

        return False, False
