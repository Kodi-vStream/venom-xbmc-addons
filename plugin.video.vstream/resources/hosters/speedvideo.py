# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'speedvideo', 'Speedvideo')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        sPattern = 'https*:\/\/speedvideo.[a-z]{3}\/(?:embed-)?([0-9a-zA-Z]+)'
        oParser = cParser()
        aResult = oParser.parse(url, sPattern)
        if aResult[0] is True:
            url = 'https://speedvideo.net/embed-' + aResult[1][0] + '.html'
        else:
            VSlog('ID error')
        super(cHoster, self).setUrl(url)

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern = 'var linkfile\s*=\s*"([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sUrl = aResult[1][0]

            class NoRedirection(urllib2.HTTPErrorProcessor):
                def http_response(self, request, response):
                    return response

                https_response = http_response

            opener = urllib2.build_opener(NoRedirection)
            opener.addheaders = [('User-Agent', UA)]
            opener.addheaders = [('Referer', self._url)]
            response = opener.open(sUrl)
            if response.code == 301 or response.code == 302:
                api_call = response.headers['Location']

            response.close()

        if api_call:
            return True, api_call

        return False, False
