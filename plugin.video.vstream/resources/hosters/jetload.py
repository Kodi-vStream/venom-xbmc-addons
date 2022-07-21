# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 2 methode play
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'jetload', 'Jetload')

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR skyblue]' + self._defaultDisplayName + '[/COLOR]' + \
            ' ' + '(Il faut pairer son ip au site https://jlpair.net/ tous les 3h)'

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('/e/', '/api/fetch/')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        # type 1

        sPattern = '{"src":"([^"]+)","type":"video/mp4"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        # type 2

        # sPattern1 = 'src: *"(.+?.mp4)",'
        # aResult1 = oParser.parse(sHtmlContent, sPattern1)
        # if (aResult1[0] == True):
            # return True, aResult1[1][0]

        # #type ?
        # sPattern1 = '<input type="hidden" id="file_name" value="([^"]+)">'
        # aResult1 = oParser.parse(sHtmlContent, sPattern1)
        # if (aResult1[0] == True):
            # FN = aResult1[1][0]

        # sPattern = '<input type="hidden" id="srv_id" value="([^"]+)">'
        # aResult = oParser.parse(sHtmlContent, sPattern)
        # if aResult[0] is True:
            # SRV = aResult[1][0]

            # pdata = 'file_name=' + FN + '.mp4&srv=' + SRV

            # oRequest = cRequestHandler('https://jetload.net/api/download')
            # oRequest.setRequestType(1)
            # #oRequest.addHeaderEntry('User-Agent', UA)
            # oRequest.addHeaderEntry('Referer', self._url)
            # oRequest.addHeaderEntry('Accept', 'application/json, text/plain, */*')
            # oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            # oRequest.addParametersLine(pdata)

            # api_call = oRequest.request()

        # #type ?
        # else:
            # sPattern = '<input type="hidden" id="srv" value="([^"]+)">'
            # aResult = oParser.parse(sHtmlContent, sPattern)
            # if (aResult1[0] == True):
                # Host = aResult[1][0]
                # api_call = Host + '/v2/schema/' + FN + '/master.m3u8'

        if api_call:
            return True, api_call

        return False, False
