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
        
        # Enhanced debugging - log the API request details
        VSlog("VidPlayer Debug - API URL: %s" % req)
        VSlog("VidPlayer Debug - POST data: %s" % pdata)
        
        try:
            sHtmlContent = oRequestHandler.request()
            VSlog("VidPlayer Debug - Raw response length: %d" % len(sHtmlContent) if sHtmlContent else 0)
            VSlog("VidPlayer Debug - Raw response preview: %s" % sHtmlContent[:200] if sHtmlContent else "Empty response")
            
            # Check if response is empty or invalid
            if not sHtmlContent:
                VSlog("VidPlayer Error - Empty response from API")
                dialog().VSerror("Erreur : Réponse vide de l'API (%s)" % req)
                return False, False
            
            if not sHtmlContent.strip().startswith('{') and not sHtmlContent.strip().startswith('['):
                VSlog("VidPlayer Error - Response is not JSON format: %s" % sHtmlContent[:100])
                dialog().VSerror("Erreur : Réponse invalide de l'API (non-JSON)")
                return False, False
            
            # Try to parse JSON with better error handling
            try:
                jsonrsp = json.loads(sHtmlContent)
                VSlog("VidPlayer Debug - JSON parsed successfully")
            except json.JSONDecodeError as e:
                VSlog("VidPlayer Error - JSON decode error: %s" % str(e))
                VSlog("VidPlayer Error - Failed response content: %s" % sHtmlContent)
                dialog().VSerror("Erreur : Connexion impossible (Expecting value line 1 column 1 (char 0)) %s" % req)
                return False, False

            if not jsonrsp or 'data' not in jsonrsp:
                VSlog("VidPlayer Error - No 'data' key in JSON response: %s" % str(jsonrsp))
                dialog().VSerror("Erreur : Format de réponse API invalide")
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
            dialog().VSerror("Erreur : Connexion impossible (%s) %s" % (str(e), req))
            return False, False

        return False, False
