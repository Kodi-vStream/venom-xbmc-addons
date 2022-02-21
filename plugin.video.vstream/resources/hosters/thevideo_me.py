# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://www.video.tt/embed/xxx
# http://thevideo.me/embed-xxx-xxx.html

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import json
import ssl

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"


# Meme code que vidup
class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'thevideo_me', 'TheVideo')

    def __getIdFromUrl(self, sUrl):
        """ URL trouvées:
            https://thevideo.me/1a2b3c4e5d6f
            https://thevideo.me/embed-1a2b3c4e5d6f.html
            http(s)://thevideo.me/embed-1a2b3c4e5d6f-816x459.html
        """
        sPattern = '\/(?:embed-)?(\w+)(?:-\d+x\d+)?(?:\.html)?$'
        aResult = cParser().parse( sUrl, sPattern )
        if aResult[0] is True:
            return aResult[1][0]
        return ''

    def setUrl(self, url):
        sId = self.__getIdFromUrl(url)
        # anciens lien
        if 'video.' in url:
            self._url = 'http://thevideo.me/embed-' + sId + '.html'
        else:
            self._url = "https://vev.io/embed/" + sId


    def _getMediaLinkForGuest(self):
        api_call = False
        aResult = False

        request_headers = {"User-Agent": UA}

        # thevideo.me doesn't exist so take redirection
        req = urllib2.Request(self._url,headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, context=gcontext)
        # sHtmlContent = response.read()
        self._url = response.geturl()
        response.close()

        Json_url = 'https://vev.io/api/serve/video/' + self.__getIdFromUrl(self._url)

        req = urllib2.Request(Json_url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, data={}, context=gcontext)
        sHtmlContent = response.read()
        aResult = json.loads(sHtmlContent)
        response.close()

        # VSlog(aResult['qualities'])

        if (aResult):
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in aResult['qualities']:
                url.append(aResult['qualities'][i])
                qua.append(str(i))

            # dialog qualiter
            api_call = dialog().VSselectqual(qua, url)

        # xbmc.sleep(5000)

        if api_call:
            return True, api_call

        return False, False
