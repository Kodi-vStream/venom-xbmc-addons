# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://cloudvid.co/embed-xxxx.html
# https://clipwatching.com/embed-xxx.html

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cloudvid', 'Cloudvid')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        if not self._url.endswith('.html'):
            self._url = self._url + '.html'

    def _getMediaLinkForGuest(self, api_call=None):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        if 'File was deleted' in sHtmlContent:
            return False, False

        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent2 = cPacker().unpack(aResult[1][0])

            sPattern = '{file:"([^"]+)",label:"([^"]+)"}'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                # initialisation des tableaux
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url)

            if not api_call:
                sPattern = 'src:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if aResult[0]:
                    api_call = aResult[1][0].replace(',', '').replace('.urlset', '')

        if not api_call:
            sPattern = 'sources: *\[{src: "([^"]+)", *type: "video/mp4"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                api_call = aResult[1][0]

        if not api_call:
            sPattern = 'source src="([^"]+)" type='
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
