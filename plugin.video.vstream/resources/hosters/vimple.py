# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://player.vimple.ru/iframe/XXXXXXXXXXXXXXXXXXXXX

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimple', 'Vimple')

    def _getMediaLinkForGuest(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        req = urllib2.Request(self._url, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        head = response.headers
        response.close()

        oParser = cParser()

        cookies = ''
        if 'Set-Cookie' in head:
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            if aResult[0] is True:
                for cook in aResult[1]:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
        # Get link
        sPattern = '"video":\[{"default":true,"url":"([^"]+?)"}]'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            url = aResult[1][0]
            url = url.replace('\/', '/')

            api_call = url + '|Cookie=' + cookies

            return True, api_call

        return False, False
