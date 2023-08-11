# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tomacloud', 'tomacloud')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = "jwplayer\(\"myElement\"\).setup\({.+?file: \"([^\"]+)"
        aResult = cParser().parse(sHtmlContent, sPattern)

        if aResult[0]:
            return True, aResult[1][0] + '|Referer=' + self._url

        return False, False
