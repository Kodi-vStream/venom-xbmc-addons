# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Meme code que thevideo
# https://vidup.me/embed-xxx-703x405.html
# https://vidup.me/embed/xxx-703x405.html
# https://vidup.me/xxx-703x405.html
# https://vidup.io/embed/xxx
# https://vidup.io/xxx

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import json
import ssl

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'VidUp'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'vidup'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def __getIdFromUrl(self, sUrl):
        sPattern = 'https*:\/\/vidup.+?\/(?:embed-)?(?:embed/)?([0-9a-zA-Z]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        # self.__sUrl = str(sUrl).replace('beta.vidup.tv', 'vidup.tv')
        # self.__sUrl = re.sub('(-\d+x\d+\.html)', '', self.__sUrl)
        # self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = False

        request_headers = {"User-Agent": UA
                           }

        req = urllib2.Request(self.__sUrl, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, context=gcontext)
        self.__sUrl = response.geturl()

        response.close()

        Json_url = "https://vidup.io/api/serve/video/" + self.__getIdFromUrl(self.__sUrl)

        req = urllib2.Request(Json_url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, data={}, context=gcontext)
        sHtmlContent = response.read()
        aResult = json.loads(sHtmlContent)

        response.close()

        if (aResult):
            url = []
            qua = []

            for i in aResult['qualities']:
                url.append(aResult['qualities'][i])
                qua.append(str(i))

            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
