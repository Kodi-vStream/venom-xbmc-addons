#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#french-stream /18117-la-frontire-verte-saison-1.html
#liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.util import QuotePlus
import json


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Frenchvid'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'frenchvid'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        if 'yggseries.com' in self.__sUrl:
            baseUrl = 'https://yggseries.com/api/source/'
        elif 'french-vid' in self.__sUrl:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'fembed' in self.__sUrl:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'feurl' in self.__sUrl:
            baseUrl = 'https://feurl.com/api/source/'
        elif 'vfsplayer' in self.__sUrl:
            baseUrl = 'https://vfsplayer.xyz/api/source/'
        elif 'fsimg' in self.__sUrl:
            baseUrl = 'https://www.fsimg.info/api/source/'
        elif 'fem.tohds' in self.__sUrl:
            baseUrl = 'https://feurl.com/api/source/'
        elif 'core1player' in self.__sUrl:
            baseUrl = 'https://www.core1player.com/api/source/'
        elif 'gotochus' in self.__sUrl:
            baseUrl = 'https://www.gotochus.com/api/source/'
            
        if 'fem.tohds' in self.__sUrl:
            oRequestHandler = cRequestHandler(self.__sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe src="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            url = baseUrl + aResult[1][0].rsplit('/', 1)[1]

            postdata = 'r=' + QuotePlus(self.__sUrl) + '&d=' + baseUrl.replace('https://', '').replace('/api/source/', '')

        else:
            url = baseUrl + self.__sUrl.rsplit('/', 1)[1]
            postdata = 'r=' + QuotePlus(self.__sUrl) + '&d=' + baseUrl.replace('https://', '').replace('/api/source/', '')

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        oRequest.addParametersLine(postdata)
        sHtmlContent = oRequest.request()

        page = json.loads(sHtmlContent)
        if page:
            url = []
            qua = []
            for x in page['data']:
                url.append(x['file'])
                qua.append(x['label'])

            if (url):
                api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            oRequest = cRequestHandler(api_call)
            oRequest.addHeaderEntry('Host','fvs.io')
            oRequest.addHeaderEntry('User-Agent', UA)
            sHtmlContent = oRequest.request()
            api_call = oRequest.getRealUrl()
            if '::/' in api_call:
                dialog().VSinfo('Desactiver l\'IPV6 sur votre appareil', 'Lecture impossible', 4)
            return True, api_call  + '|User-Agent=' + UA

        return False, False
