# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, isKrypton


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidlox', 'Vidlox')
        if not isKrypton():
            self._defaultDisplayName = '(Windows\Android Nécessite Kodi17)' + ' Vidlox'

    def setUrl(self, url):
        url = url.replace('embed-dlox.me/', 'embed-')
        super(cHoster, self).setUrl(url)

    def _getMediaLinkForGuest(self):
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', "https://vidlox.me/8m8p7kane4r1.html")
        sHtmlContent = oRequest.request()

        # accelère le traitement
        sHtmlContent = oParser.abParse(sHtmlContent, 'var player', 'vvplay')

        sPattern = '([^"]+\.mp4)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        api_call = ''
        if aResult[0] is True:
            # initialisation des tableaux
            url = []
            qua = ["HD", "SD"]  # sd en 2eme pos generalement quand sd

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i))

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
