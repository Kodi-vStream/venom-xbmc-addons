# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://letsupload.co/plugins/mediaplayer/site/_embed.php?u=1r0c1&w=770&h=320
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'letsupload', 'Letsupload')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        api_call = ''
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'file: *"([^"]+)",*'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
