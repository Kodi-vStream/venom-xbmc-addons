# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 2 hoster giga & 2gigalink
# from resources.lib.handler.requestHandler import cRequestHandler

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import ssl

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'giga', 'Giga')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        myContext = ssl._create_unverified_context()

        req = urllib2.Request(self._url)
        handle = urllib2.urlopen(req, context=myContext)
        sHtmlContent = handle.read()
        handle.close()

        oParser = cParser()
        sPattern = "var mp4v = '(.+?)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            return True, aResult[1][0]
        else:
            # streamgk
            sPattern = '<a id="downloadb" class="btn btn-default.+?href="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                return True, aResult[1][0]

        return False, False
