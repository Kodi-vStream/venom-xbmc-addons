# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'kvid', 'Kvid')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        r2 = re.search('file: *"([^"]+)",', sHtmlContent)
        if r2:
            api_call = r2.group(1)

        if api_call:
            return True, api_call

        return False, False
