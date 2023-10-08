# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://cloudvid.co/embed-xxxx.html
# https://clipwatching.com/embed-xxx.html

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'darkibox', 'DarkiBox')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self, api_call=None):

        file_code = self._url.split('/')[-1].split('.')[0]

        postdata = 'op=embed&auto=1&file_code=%s' % file_code

        oRequest = cRequestHandler("https://darkibox.com/dl")
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()
        oParser = cParser()
        sPattern = 'sources: *\[{src: "([^"]+)"'#, *type: "video/mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]

        return api_call != None, api_call
