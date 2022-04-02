# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'wstream', 'WStream')

    def _getMediaLinkForGuest(self):
        api_call = False

        # VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        # Dean Edwards Packer
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sUnpacked = cPacker().unpack(aResult[1][0])
            sHtmlContent = sUnpacked

        sPattern = '{file:"(.+?)",label:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        # print(aResult)

        if aResult[0] is True:
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # tableau
            api_call = dialog().VSselectqual(qua, url)
        # print(api_call)

        if api_call:
            return True, api_call

        return False, False
