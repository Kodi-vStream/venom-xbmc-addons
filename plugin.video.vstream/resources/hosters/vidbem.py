# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.vidbem.com/embed-xxx.html

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import AADecoder
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbem', 'VidBEM')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        list_url = []
        list_q = []
        oParser = cParser()

        sPattern = '(?:[>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:  # 1 seul à vérifier ici ?
            sdec = AADecoder(aResult[1][0]).decode()
            sPattern = 'file:"([^"]+).+?label:"([^"]+)'
            aResult = oParser.parse(sdec, sPattern)

            if aResult[0] is True:
                for aentry in aResult[1]:  # ou là
                    list_url.append(aentry[0])
                    list_q.append(aentry[1])

                api_call = dialog().VSselectqual(list_q, list_url)

        if api_call:
            return True, api_call

        return False, False
