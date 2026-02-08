# -*- coding: utf-8 -*-
# https://vidzi.tv/xxx.html
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidzy', 'Vidzy')

    def _getMediaLinkForGuest(self):
        api_call = ''

        oRequest = cRequestHandler(self._url)
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
                    # https://v4.vidzy.org/hls2/03/00024/hyjs6o5v8hct_n/master.m3u8?t=WCz8e4sUtTyDoLaTT9uHLMql01Z1QnclnTnRXrKI5UI&s=1764809497&e=172800&f=123080&i=0.0&sp=0

        if api_call:
            return True, api_call

        return False, False
