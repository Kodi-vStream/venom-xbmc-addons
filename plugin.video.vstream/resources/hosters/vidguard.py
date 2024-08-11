# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.aadecode import decodeAA
from resources.lib.util import cUtil


import binascii
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidguard', 'Vidguard')

    def __getHost(self):
        parts = self._url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '<script\s*src="(/assets/videojs/ad/[^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #Surement inutile mais je laisse pour compatibilité
        if aResult[0] is True:
            url = self.__getHost() + aResult[1][0]
            
            oRequest = cRequestHandler(url)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self._url)
            sHtmlContent = oRequest.request()

        #with open('c:\\test.txt', 'w', encoding='utf-8') as f:
        #    f.write(sHtmlContent)

        sPattern = 'n(ﾟωﾟ.+?);"\);<\/script'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            
            code = aResult[1][0]
            code = code.replace('\\u002b', '+')
            code = code.replace('\\u0027', "'")
            code = code.replace('\\u0022', '"')
            code = code.replace('\\/', '/')
            code = code.replace('\\\\', '\\')
            code = code.replace('\\"', '"')
            sHtmlContent = decodeAA(code, True)
            
            sPattern = 'Label":"([^"]+)","URL":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            #Plusieurs liens
            if aResult[0]:
                # initialisation des tableaux
                url = []
                qua = []
                for i in aResult[1]:
                    url2 = str(i[1])
                    url2 = url2.encode().decode('unicode-escape')
                    url.append(sig_decode(url2))
                    qua.append(str(i[0]))

                api_call = dialog().VSselectqual(qua, url) + '|Referer=' + self._url
 
            #1 seul lien
            sPattern = '"stream":"([^"]+)".+?"hash":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url2 = str(aResult[1][0][0])
                url2 = url2.encode().decode('unicode-escape')

                api_call = sig_decode(url2) + '|Referer=' + self._url

        if api_call:
            return True, api_call

        return False, False


# Adapted from PHP code by vb6rocod
# Copyright (c) 2019 vb6rocod
def sig_decode(url):
    sig = url.split('sig=')[1].split('&')[0]
    t = ''
    
    for v in binascii.unhexlify(sig):
        t += chr((v if isinstance(v, int) else ord(v)) ^ 2)
    t = list(base64.b64decode(t + '==')[:-5][::-1])
    
    for i in range(0, len(t) - 1, 2):
        t[i + 1], t[i] = t[i], t[i + 1]
        
    t = ''.join(chr(i) for i in t)
    url = url.replace(sig, ''.join(str(t))[:-5])
    return url
