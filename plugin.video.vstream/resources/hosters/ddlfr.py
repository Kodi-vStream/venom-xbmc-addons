# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# import re
import base64

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
# from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'ddlfr', 'ddlfr')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', self._url)
        sHtmlContent = oRequest.request()
        # VSlog(sHtmlContent)
        oParser = cParser()
        sPattern = 'JuicyCodes\.Run\("(.+?)"\);'
        aResult = oParser.parse(sHtmlContent, sPattern)
        # VSlog(aResult)
        if aResult[0] is True:

            media = aResult[1][0].replace('+', '')
            media = base64.b64decode(media)

            # cPacker decode
            media = cPacker().unpack(media)
            # VSlog(media)
            if media:

                sPattern = '{"file":"(.+?)","label":"(.+?)"'
                aResult = oParser.parse(media, sPattern)
                # VSlog(aResult)

                # initialisation des tableaux
                if aResult[0] is True:
                    url = []
                    qua = []
                # Remplissage des tableaux
                    for i in aResult[1]:
                        url.append(str(i[0] + '|Referer=' + self._url))
                        qua.append(str(i[1]))
                # Si une seule url
                    api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
