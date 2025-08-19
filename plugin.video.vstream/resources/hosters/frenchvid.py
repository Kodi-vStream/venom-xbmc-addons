# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# french-stream /18117-la-frontire-verte-saison-1.html
# liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
import json

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'frenchvid', 'Frenchvid')

    def _getMediaLinkForGuest(self):
        # Get Redirection
        if 'fembed' in self._url:
            oRequest = cRequestHandler(self._url)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.request()
            self._url = oRequest.getRealUrl()

        if 'french-vid' in self._url:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'fembed' in self._url or "femax20" in self._url:
            baseUrl = 'https://www.diasfem.com/api/source/'
        elif 'fem.tohds' in self._url:
            baseUrl = 'https://feurl.com/api/source/'
        else:
            baseUrl = 'https://' + self._url.split('/')[2] + '/api/source/'

        if 'fem.tohds' in self._url:
            oRequestHandler = cRequestHandler(self._url)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe src="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            url = baseUrl + aResult[1][0].rsplit('/', 1)[1]
            postdata = 'r=""' + '&d=' + self._url.split('/')[2]
        else:
            url = baseUrl + self._url.rsplit('/', 1)[1]
            postdata = "r=''" + "&d=" + self._url.split('/')[2]

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParametersLine(postdata)
        
        # Enhanced debugging - log the API request details
        VSlog("FrenchVid Debug - API URL: %s" % url)
        VSlog("FrenchVid Debug - POST data: %s" % postdata)
        VSlog("FrenchVid Debug - Referer: %s" % self._url)
        
        try:
            # First get raw response to check what we're actually receiving
            raw_response = oRequest.request(jsonDecode=False)
            VSlog("FrenchVid Debug - Raw response length: %d" % len(raw_response) if raw_response else 0)
            VSlog("FrenchVid Debug - Raw response preview: %s" % raw_response[:200] if raw_response else "Empty response")
            
            # Check if response looks like JSON
            if not raw_response:
                VSlog("FrenchVid Error - Empty response from API")
                dialog().VSerror("Erreur : Réponse vide de l'API (%s)" % url)
                return False, False
            
            if not raw_response.strip().startswith('{') and not raw_response.strip().startswith('['):
                VSlog("FrenchVid Error - Response is not JSON format: %s" % raw_response[:100])
                dialog().VSerror("Erreur : Réponse invalide de l'API (non-JSON)")
                return False, False
            
            # Try to decode JSON manually with better error handling
            try:
                page = json.loads(raw_response)
                VSlog("FrenchVid Debug - JSON parsed successfully")
            except json.JSONDecodeError as e:
                VSlog("FrenchVid Error - JSON decode error: %s" % str(e))
                VSlog("FrenchVid Error - Failed response content: %s" % raw_response)
                dialog().VSerror("Erreur : Connexion impossible (JSON invalide) %s" % url)
                return False, False
            
            if page and 'data' in page:
                url = []
                qua = []
                for x in page['data']:
                    url.append(x['file'])
                    qua.append(x['label'])
        
                api_call = dialog().VSselectqual(qua, url)
        
                oRequest = cRequestHandler(api_call)
                oRequest.addHeaderEntry('Host', 'fvs.io')
                oRequest.addHeaderEntry('User-Agent', UA)
                oRequest.request()
                api_call = oRequest.getRealUrl()
        
                if api_call:
                    return True, api_call + '|User-Agent=' + UA
            else:
                VSlog("FrenchVid Error - No 'data' key in JSON response: %s" % str(page))
                dialog().VSerror("Erreur : Format de réponse API invalide")
                return False, False
                
        except Exception as e:
            VSlog("FrenchVid Error - General exception: %s" % str(e))
            dialog().VSerror("Erreur : Connexion impossible (%s) %s" % (str(e), url))
            return False, False


        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'var video_source = "([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult:
            return True, aResult[1][0] + '|User-Agent=' + UA

        return False, False
