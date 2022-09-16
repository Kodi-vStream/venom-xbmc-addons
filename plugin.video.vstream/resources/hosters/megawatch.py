# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megawatch', 'Megawatch')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        if 'File was deleted' in sHtmlContent:
            return False, False

        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = '{file:"(http.+?mp4)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]  # pas de choix qualité trouvé pour le moment

        if api_call:
            return True, api_call

        return False, False
