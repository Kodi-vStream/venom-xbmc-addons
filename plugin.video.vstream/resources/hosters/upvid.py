# -*- coding: utf-8 -*-
# https://upvid.co/embed-xxx.html
# https://upvid.co/xxx.html

import base64
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.aadecode import AADecoder
from resources.lib.comaddon import isMatrix, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upvid', 'UpVid')

    def setUrl(self, url):
        # lien embed obligatoire
        if 'embed-' not in url:
            url = url.rsplit('/', 1)[0] + '/embed-' + url.rsplit('/', 1)[1]
        super(cHoster, self).setUrl(url)


    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()
        sUrl = self._url
        
        sPattern1 = '<iframe id="iframe" src="([^"]+)"'
        sPattern2 = '<input type="hidden" id="link" value="([^"]+)'
        
        referer = self._url

        # Max 3 fois
        for i in range(0, 3):
            
            oRequest = cRequestHandler(sUrl)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', referer)
            sHtmlContent = oRequest.request()
            sHtmlContent = sHtmlContent.replace('\n', '')
            
            referer = sUrl
            
            #ok c'est fini, on a la bonne page
            if 'ﾟωﾟﾉ' in sHtmlContent:
                break

            aResult = oParser.parse(sHtmlContent, sPattern1)
            
            if aResult[0] is True:
                sUrl = aResult[1][0]
            else:
                aResult = oParser.parse(sHtmlContent, sPattern2)
                if aResult[0] is True:
                    sUrl = aResult[1][0]
                    
        aResult = re.search('id="code".+?value="(.+?)"', sHtmlContent, re.DOTALL)
            
        if aResult:
            
            sFunc = base64.b64decode(aResult.group(1))

            aResult = re.search('(ﾟωﾟ.+?\(\'_\'\);)', sHtmlContent, re.DOTALL | re.UNICODE)
            if aResult:
                sHtmlContent = AADecoder(aResult.group(1)).decode()
                if sHtmlContent:
                    aResult = re.search("func.innerHTML.+?\('(.+?)',", sHtmlContent, re.DOTALL)
                    if aResult:
                        chars = aResult.group(1)
                        final = sDecode(chars, sFunc)
                        sPattern = "source\.setAttribute\('src', '([^']+)'\)"
                        aResult = oParser.parse(final, sPattern)
                        if aResult[0] is True:
                            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False


def sDecode(r, o):
    t = []
    e = []
    n = 0
    a = ""
    for f in range(256):
        e.append(f)

    for f in range(256):
        n = (n + e[f] + ord(r[f % len(r)])) % 256
        t = e[f]
        e[f] = e[n]
        e[n] = t

    f = 0
    n = 0
    for h in range(len(o)):
        f = f + 1
        n = (n + e[f % 256]) % 256
        if f not in e:
            f = 0
        t = e[f]
        e[f] = e[n]
        e[n] = t

        if isMatrix():
            a += chr(o[h] ^ e[(e[f] + e[n]) % 256])
        else:
            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])
    return a
