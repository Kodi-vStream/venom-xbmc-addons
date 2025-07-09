# coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import base64

#From https://github.com/Gujal00/ResolveURL/blob/master/script.module.resolveurl/lib/resolveurl/plugins/voesx.py
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'voe', 'Voe')

    def __getHost(self, url):
        parts = url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        url = self._url

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        if 'const currentUrl' in sHtmlContent:
            sPattern = "window\.location\.href\s*=\s*'([^']+)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url = aResult[1][0]
                oRequest = cRequestHandler(aResult[1][0])
                oRequest.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequest.request()

        sPattern = 'json">\["([^"]+)"]</script>\s*<script\s*src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            url2 = self.__getHost(url) + aResult[1][0][1]
            code = aResult[1][0][0]

            oRequest = cRequestHandler(url2)
            oRequest.addHeaderEntry('User-Agent', UA)
            sHtmlContent = oRequest.request()

            sPattern = "(\[(?:'\W{2}'[,\]]){1,9})"
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                s = voe_decode(code, aResult[1][0])
                file = ''
                for i in s:
                    if i == 'file' or i == 'source':
                        file = s[i]
                #VSlog(file)

                api_call = file + '|User-Agent=' + UA # + '&Referer=' + url

        if api_call:
            return True, api_call

        return False, False



def voe_decode(ct, luts):
    import json, re, base64
    lut = [''.join([('\\' + x) if x in '.*+?^${}()|[]\\' else x for x in i]) for i in luts[2:-2].split("','")]
    txt = ''
    for i in ct:
        x = ord(i)
        if 64 < x < 91:
            x = (x - 52) % 26 + 65
        elif 96 < x < 123:
            x = (x - 84) % 26 + 97
        txt += chr(x)
    for i in lut:
        txt = re.sub(i, '', txt)
    ct = base64.b64decode(txt)
    txt = ''.join([chr(i - 3) for i in ct])
    txt = base64.b64decode(txt[::-1])
    return json.loads(txt)
