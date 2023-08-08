# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.aadecode import decodeAA
from resources.lib.util import cUtil


import binascii
import base64


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidguard', 'Vidguard')

    def __getHost(self):
        parts = self._url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '<script\s*src="(/assets/videojs/ad/[^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0] is True:
            url = self.__getHost() + aResult[1][0]
            
            oRequest = cRequestHandler(url)
            oRequest.addHeaderEntry('Referer', self._url)
            sHtmlContent = oRequest.request()
            
            sPattern = '(ﾟωﾟ.+?\(\'_\'\);)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                sHtmlContent = decodeAA(aResult[1][0], True)
                
                sPattern = 'Label":"([^"]+)","URL":"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
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
