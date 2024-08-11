# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.pstream.net/e/xxxxx
import base64
import json

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import isMatrix
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import urlEncode

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"

headers = {"User-Agent": UA,
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'pstream', 'Pstream')

    def _getMediaLinkForGuest(self):
        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '<script src="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)[1][1]

        oRequest = cRequestHandler(aResult)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequest.request()

        sPattern = 'atob.+?\}\("(.+?)"'
        code = oParser.parse(sHtmlContent, sPattern)

        for i in code[1]:
            try:
                if isMatrix():
                    code = base64.b64decode(i).decode('ascii')
                else:
                    code = base64.b64decode(i)
                break
            except:
                pass

        jsonCall = json.loads(code[code.rfind("{"):])

        for a in jsonCall:
            try:
                if isMatrix():
                    d = base64.b64decode(jsonCall[a].split('/')[4].split('.')[0]).decode('ascii')
                else:
                    d = base64.b64decode(jsonCall[a].split('/')[4].split('.')[0])
                api_call = jsonCall[a]
                break
            except:
                pass

        if api_call:
            return True, api_call + '|' + urlEncode(headers)

        return False, False
