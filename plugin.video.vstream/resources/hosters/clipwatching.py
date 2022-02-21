# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'clipwatching', 'ClipWatching')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, api_call=None):
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        # accelère le traitement
        sHtmlContent = oParser.abParse(sHtmlContent, 'var holaplayer', 'vvplay')
        # Traitement pour les liens m3u8
        sHtmlContent = sHtmlContent.replace(',', '').replace('master.m3u8', 'index-v1-a1.m3u8')
        sPattern = '"(http[^"]+(?:.m3u8|.mp4))"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            # initialisation des tableaux
            url = []
            qua = []
            n = 1

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i))
                qua.append('Lien ' + str(n))
                n += 1

            # dialogue Lien si plus d'une url
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
