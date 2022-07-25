# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamax', 'Streamax')

    def __getIdFromUrl(self, sUrl):
        sPattern = 'id=([a-zA-Z0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)

        if aResult[0] is True:
            return aResult[1][0]
        return ''

    def _getMediaLinkForGuest(self):
        oParser = cParser()

        urlId = self.__getIdFromUrl(self._url)

        sUrl = 'https://streamax.club/hls/' + urlId + '/' + urlId + '.playlist.m3u8'

        url = []
        qua = []

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', 'https://streamax.club/public/dist/index.html?id=' + urlId)
        sHtmlContent = oRequest.request()

        sPattern = 'RESOLUTION=(\d+x\d+)(.+?.m3u8)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            for aEntry in aResult[1]:
                url.append('https://streamax.club' + aEntry[1])
                qua.append(aEntry[0])

            if url:
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
