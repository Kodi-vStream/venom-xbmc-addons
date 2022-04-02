#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
#Ne pas passer par la version de téléchargement.
#Tout les liens ne sont pas téléchargeable.
import random
import base64
import time

try: # Python 2
    import urllib2 as urllib
except ImportError: # Python 3
    import urllib.request as urllib

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, isMatrix, xbmc


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

def compute(s):
    a = s.replace("/","1")
    a = base64.b64decode(a)
    a = a.replace("/","Z")
    a = base64.b64decode(a)
    a = a.replace("@","a")
    a = base64.b64decode(a)
    return a

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dood', 'Dood')

    def setUrl(self, url):
        self._url = str(url).replace('/d/','/e/').replace('doodstream.com','dood.la')

    def _getMediaLinkForGuest(self):
        api_call = False

        headers = {'User-Agent': UA}

        req = urllib.Request(self._url, None, headers)
        with urllib.urlopen(req) as response:
            sHtmlContent = response.read()
            urlDonwload = response.geturl()

        try:
            sHtmlContent = sHtmlContent.decode('utf8')
        except:
            pass

        oParser = cParser()

        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        fin_url = ''.join(random.choice(possible) for _ in range(10))

        sPattern = 'return a\+"(\?token=[^"]+)"'
        d = oParser.parse(sHtmlContent, sPattern)[1][0]

        fin_url = fin_url + d + str(int(1000*time.time()))

        sPattern = "\$\.get\('(\/pass_md5[^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        url2 = 'https://' + urlDonwload.split('/')[2] + aResult[1][0]

        headers.update({'Referer': urlDonwload})

        req = urllib.Request(url2, None, headers)
        with urllib.urlopen(req) as response:
            sHtmlContent = response.read()

        try:
            sHtmlContent = sHtmlContent.decode('utf8')
        except:
            pass

        api_call = sHtmlContent + fin_url

        #VSlog(api_call)

        if api_call:
            api_call = api_call + '|Referer=' + urlDonwload
            return True, api_call

        return False, False
