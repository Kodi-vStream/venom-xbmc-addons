# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'smoothpre', 'SmoothPre')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        sHtmlContent = cRequestHandler(self._url).request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult_1 = re.findall(sPattern, sHtmlContent)
        if aResult_1:
            sHtmlContent = cPacker().unpack(aResult_1[0])
            aResult = cParser().parse(sHtmlContent, '"hls2":"([^"]+)"')
            if aResult[0] is True:
                return True, aResult[1][0]

        return False, False
