# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import json

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.util import cUtil


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Ok.ru'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'ok_ru'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def getHostAndIdFromUrl(self, sUrl):
        sPattern = 'https*:\/\/((?:(?:ok)|(?:odnoklassniki))\.ru)\/.+?\/([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        v = self.getHostAndIdFromUrl(self.__sUrl)
        sId = v[1]
        sHost = v[0]
        web_url = 'http://' + sHost + '/videoembed/' + sId

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

        req = urllib2.Request(web_url, headers=HEADERS)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        response.close()

        oParser = cParser()

        sHtmlContent = oParser.abParse(sHtmlContent, 'data-options=', '" data-player-container', 14)
        sHtmlContent = cUtil().removeHtmlTags(sHtmlContent)
        sHtmlContent = cUtil().unescape(sHtmlContent)  # .decode('utf-8'))

        page = json.loads(sHtmlContent)
        page = json.loads(page['flashvars']['metadata'])
        if page:
            url = []
            qua = []
            for x in page['videos']:
                url.append(x['url'])
                qua.append(x['name'])

            # Si au moins 1 url
            if (url):
                # dialogue qualité
                api_call = dialog().VSselectqual(qua, url)


        if (api_call):
            api_call = '%s|User-Agent=%s&Accept=%s' % (api_call, HEADERS['User-Agent'], HEADERS['Accept'])
            api_call = api_call + '&Referer=' + self.__sUrl + '&Origin=http://ok.ru'
            return True, api_call

        return False, False
