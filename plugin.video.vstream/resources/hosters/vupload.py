# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vupload', 'Vupload')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent2 = cPacker().unpack(aResult[1][0])

            sPattern = '{src:"([^"]+)",type:"video\/mp4",res:([^:,<>]+)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                # initialisation des tableaux
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
