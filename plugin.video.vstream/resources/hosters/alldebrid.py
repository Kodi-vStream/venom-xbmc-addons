# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import json

from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, addon


class cHoster(iHoster):
    
    def __init__(self):
        iHoster.__init__(self, 'alldebrid', 'Alldebrid', 'violet')
    
    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + "/" + self.getRealHost() + '[/COLOR]'

    def _getMediaLinkForGuest(self):
        token_Alldebrid = cPremiumHandler(self.getPluginIdentifier()).getToken()
        if token_Alldebrid:
            sUrl_Bypass = addon().getSetting('hoster_alldebrid_url')
            if not sUrl_Bypass:
                sUrl_Bypass = "https://api.alldebrid.com/v4/link/unlock?agent=vStream&apikey=%s&link=%s"
            sUrl_Bypass %= (token_Alldebrid, self._url)
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

    def testPremium(self):
        token_Alldebrid = cPremiumHandler(self.getPluginIdentifier()).getToken()
        if not token_Alldebrid:
            return

        from resources.lib.comaddon import dialog
        from datetime import datetime
        sUrl = "https://api.alldebrid.com/v4/user?agent=myAppName&apikey=%s" % token_Alldebrid
        oRequest = cRequestHandler(sUrl)
        reponse = json.loads(oRequest.request())
        if 'error' in reponse:
            dialog().VSok(reponse['error']['message'])
        elif reponse['status'] == 'success':
            userData = reponse['data']['user']
            timestamp = userData['premiumUntil']
            premiumUntil = datetime.fromtimestamp(timestamp)

            if userData['isTrial']:
                msg = "Version d'essai"
                msg += "\r\nDate fin= %s" % premiumUntil
                msg += "\r\nSouscription = %s" % userData['isSubscribed']
                if 'remainingTrialQuota' in userData:
                    msg += "\r\nQuota disponible (MB) = %d" % userData['remainingTrialQuota']
                dialog().VSok(msg)
                return

            msg = 'Compte premium = %s\r\nDate fin = %s' % (userData['isPremium'], premiumUntil)
            dialog().VSok(msg)
        return
