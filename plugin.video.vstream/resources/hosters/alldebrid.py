# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import json

from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog


class cHoster(iHoster):
    
    def __init__(self):
        iHoster.__init__(self, 'alldebrid', 'Alldebrid', 'violet')
    
    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + "/" + self.getRealHost() + '[/COLOR]'

    def _getMediaLinkForGuest(self):
        token_Alldebrid = cPremiumHandler(self.getPluginIdentifier()).getToken()
        if token_Alldebrid:
            sUrl_Bypass = "https://api.alldebrid.com/v4/link/unlock?agent=service&version=1.0-&apikey=" + \
                token_Alldebrid + "&link=" + self._url
        else:
            return False, False

        oRequest = cRequestHandler(sUrl_Bypass)
        sHtmlContent = json.loads(oRequest.request())

        if 'error' in sHtmlContent:
            if sHtmlContent['error']['code'] in ('LINK_HOST_NOT_SUPPORTED', 'LINK_DOWN'):
                # si alldebrid ne prend pas en charge ce type de lien, on retourne le lien pour utiliser un autre hoster
                return False, self._url
            else:
                VSlog('Hoster Alldebrid - Error: ' + sHtmlContent["error"]['code'])
                return False, self._url   # quelque soit l'erreur, on retourne le lien pour utiliser un autre hoster

        api_call = HostURL = sHtmlContent["data"]["link"]
        try:
            mediaDisplay = HostURL.split('/')
            VSlog('Hoster Alldebrid - play : %s/ ... /%s' % ('/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog('Hoster Alldebrid - play : ' + HostURL)

        if api_call:
            # api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) ' + \
            #     'Gecko/20100101 Firefox/39.0'
            return True, api_call

        return False, False
