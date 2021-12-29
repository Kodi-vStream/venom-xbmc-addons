#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamango', 'Streamango')

    def decode(self, encoded, code):
        #from https://github.com/jsergio123/script.module.urlresolver
        _0x59b81a = ""
        k = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        k = k[::-1]

        count = 0

        for index in range(0, len(encoded) - 1):
            while count <= len(encoded) - 1:
                _0x4a2f3a = k.index(encoded[count])
                count += 1
                _0x29d5bf = k.index(encoded[count])
                count += 1
                _0x3b6833 = k.index(encoded[count])
                count += 1
                _0x426d70 = k.index(encoded[count])
                count += 1

                _0x2e4782 = ((_0x4a2f3a << 2) | (_0x29d5bf >> 4))
                _0x2c0540 = (((_0x29d5bf & 15) << 4) | (_0x3b6833 >> 2))
                _0x5a46ef = ((_0x3b6833 & 3) << 6) | _0x426d70
                _0x2e4782 = _0x2e4782 ^ code

                _0x59b81a = str(_0x59b81a) + chr(_0x2e4782)

                if _0x3b6833 != 64:
                    _0x59b81a = str(_0x59b81a) + chr(_0x2c0540)
                if _0x3b6833 != 64:
                    _0x59b81a = str(_0x59b81a) + chr(_0x5a46ef)

        return _0x59b81a

    def _getMediaLinkForGuest(self):
        api_call = False
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        r1 = re.search("{type:\"video/mp4\",src:\w+\('([^']+)',(\d+)", sHtmlContent)
        if (r1):
            api_call = self.decode(r1.group(1), int(r1.group(2)))
            if api_call.endswith('@'):
               api_call = api_call[:-1]

            api_call = 'http:' + api_call

        if api_call:
            return True, api_call

        return False, False
