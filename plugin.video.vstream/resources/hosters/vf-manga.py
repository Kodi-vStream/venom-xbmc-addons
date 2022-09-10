#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# import base64
import codecs

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vf-manga', 'vf-manga')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'unescape\("(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            s = aResult[1][0].replace('%', '')
            chain = codecs.decode(s, "hex")

            sPattern = '<script type="text\/javascript">(eval\(function\(p,a,c,k,e,d.+?)<\/script>'
            aResult = oParser.parse(chain, sPattern)
            if not aResult[0]:
                return False, False

            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern =  '<iframe src=.+?"([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if aResult[0]:
                api_call = aResult[1][0].replace('\\', '')
    
                if not api_call.startswith('http'):
                    api_call = 'https://vf-manga.cc/player/' + api_call
    
                oRequest = cRequestHandler(api_call)
                oRequest.addHeaderEntry('Referer', self._url)
                sHtmlContent = oRequest.request()
                api_call = oRequest.getRealUrl()

        if api_call:
            return False, api_call  # redirection

        return False, False
