# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre pseudo
# Ne pas passer par la version de téléchargement.
# Tous les liens ne sont pas téléchargeables.
import random
import base64
import time

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'


def compute(s):
    a = s.replace("/", "1")
    a = base64.b64decode(a)
    a = a.replace("/", "Z")
    a = base64.b64decode(a)
    a = a.replace("@", "a")
    a = base64.b64decode(a)
    return a


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dood', 'Dood')

    def setUrl(self, url):
        super(cHoster, self).setUrl(url.replace('/d/', '/e/').replace('doodstream.com', 'dood.la'))

    def _getMediaLinkForGuest(self):
        oParser = cParser()
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.request()
        urlDownload = oRequestHandler.getRealUrl()
        if urlDownload != self._url:
            self._url = urlDownload

        sHtmlContent = cRequestHandler(self._url).request()

        # redirection
        sPattern = '<iframe class="embed-responsive-item" src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            self._url = aResult[1][0]
            return self._getMediaLinkForGuest()
        
        sPattern = 'return a\s*\+\s*"(\?token=[^"&]+)["&]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if not aResult[0]:
            return False, False

        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        fin_url = ''.join(random.choice(possible) for _ in range(10))

        d = aResult[1][0]

        fin_url = fin_url + d + str(int(1000*time.time()))

        sPattern = "\$\.get\('(\/pass_md5[^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        url2 = 'https://' + urlDownload.split('/')[2] + aResult[1][0]

        oRequestHandler = cRequestHandler(url2)
        oRequestHandler.addHeaderEntry('Referer', urlDownload)
        sHtmlContent = oRequestHandler.request()

        api_call = sHtmlContent + fin_url

        if api_call:
            api_call = api_call + '|Referer=' + urlDownload
            return True, api_call

        return False, False
