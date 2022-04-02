# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom
# Hoster pour les liens https://hd-stream.xyz/embed/
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'hd_stream', 'HDStream')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:

            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file":"([^"]+)".+?"label":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                url = []
                qua = []

                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1])

                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
