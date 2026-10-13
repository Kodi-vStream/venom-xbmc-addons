# -*- coding: utf-8 -*-
# https://vidzi.tv/xxx.html
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidzy', 'Vidzy')

    def __getHost(self,url):
        parts = self._url.split('//', 1)
        host = parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self):
        api_call = ''
        host = self.__getHost(self._url)

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        
        sHtmlContent = oRequest.request()
        
        oParser = cParser()

        # essai un unpack
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            try:
                pack = aResult[1][0]
                sHtmlContent = cPacker().unpack(pack)
                sPattern = '{src:\s*"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    api_call = aResult[1][0] + '|Referer=' + self._url
            except:
                pass
            
            if not api_call:
                # unpack manuel en cas d'erreur
                sPattern = 'div\|data\|(\d+)\|(\d+).+?contextMenu\|(\d+)\|(\d+)\|([^\|]+)\|mp4\|.+?sp\|([^\|]+)\|(.+?)\|m3u8\|master\|([^\|]+)\|([^\|]+)'
                aResult = oParser.parse(pack, sPattern)
                if aResult[0]:
                    p = aResult[1][0]
                    hashCode = p[6]
                    
                    if '|' in hashCode:
                        hashCode = hashCode.split('|')
                        hashCode = '-'.join(hashCode[::-1])
                    
                    api_call = 'https://%s.vidzy.org/%s/%02d/%05d/%s/master.m3u8?t=%s&s=%s&e=%s&f=%s&i=0.0&sp=0' % (p[4], p[8], int(p[3]), int(p[2]), p[7], hashCode, p[0], p[5], p[1])

        # New method ?
        if not api_call:
            sPattern = 'try{\(function\(\){var .="([^"]+).+?if\(BC!==([0-9]+)\)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                #VSlog(aResult[1][0][0])
                #VSlog(aResult[1][0][1])

                api_call = decode_source(aResult[1][0][0], host, int(aResult[1][0][1]))
                #VSlog(api_call)

        if api_call:
            api_call = api_call + '|User-Agent=' + UA + '&referer=https://' + self.__getHost(self._url)
            #api_call = api_call + '&Cookie=' + cookies
            return True, api_call

        return False, False


#From https://github.com/Gujal00/ResolveURL
def decode_source(blob, host, dec):
    # the player keeps the source reversed, xored and base64 encoded, with
    # the xor key seeded from the hostname the page is served from, so the
    # seed has to be taken from the host instead of being hardcoded
    
    if len(blob) % 4 != 0:
        blob += '=' * (-len(blob) % 4)
        
    seed = 0
    for c in host:
        seed = (seed + ord(c)) & 255
    #raw = helpers.b64decode(blob, binary=True)[::-1]
    raw = base64.b64decode(blob)[::-1]
    source = ''
    for i in range(len(raw)):
        b = raw[i] if isinstance(raw[i], int) else ord(raw[i])
        source += chr(b ^ ((0x3d + i * 89 + seed + dec) & 255))
    return source
