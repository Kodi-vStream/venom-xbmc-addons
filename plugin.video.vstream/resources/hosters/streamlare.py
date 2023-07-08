# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
    'Chrome/83.0.4103.116 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'streamlare', 'Streamlare')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False

        oRequestHandler = cRequestHandler("https://sltube.org/api/video/stream/get")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addParameters('id', self._url.split('/')[4])
        sHtmlContent = oRequestHandler.request()
        
        oParser = cParser()
        sPattern = 'label":"([^"]+).*?file":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            url=[]
            qua=[] 
            for aEntry in aResult[1]:
                qua.append(aEntry[0])
                url.append(aEntry[1])

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
