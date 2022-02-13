#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#french-stream /18117-la-frontire-verte-saison-1.html
#liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog


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
        #Peut-etre une redirection.
        if 'fembed' in self.__sUrl:
            oRequestHandler = cRequestHandler(self.__sUrl)
            sHtmlContent = oRequestHandler.request()
            self.__sUrl = oRequestHandler.getRealUrl()

        if 'french-vid' in self.__sUrl:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'fembed' in self.__sUrl or "femax20" in self.__sUrl:
            baseUrl = 'https://www.diasfem.com/api/source/'
        elif 'fem.tohds' in self.__sUrl:
            baseUrl = 'https://feurl.com/api/source/'
        else:
            baseUrl = 'https://' + self.__sUrl.split('/')[2] + '/api/source/'

        if 'fem.tohds' in self.__sUrl:
            oRequestHandler = cRequestHandler(self.__sUrl)
            oRequestHandler.disableIPV6()
            sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe src="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            url = baseUrl + aResult[1][0].rsplit('/', 1)[1]

            postdata = 'r=' + self.__sUrl + '&d=' + baseUrl.replace('https://', '').replace('/api/source/', '')

        else:
            url = baseUrl + self.__sUrl.rsplit('/', 1)[1]
            postdata = 'r=' + self.__sUrl + '&d=' + baseUrl.replace('https://', '').replace('/api/source/', '')

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.disableSSL()
        oRequest.disableIPV6()
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        oRequest.addParametersLine(postdata)
        page = oRequest.request(jsonDecode=True)

        url = []
        qua = []
        for x in page['data']:
            url.append(x['file'])
            qua.append(x['label'])

        api_call = dialog().VSselectqual(qua, url)

        oRequest = cRequestHandler(api_call)
        oRequest.disableSSL()
        oRequest.disableIPV6()
        oRequest.addHeaderEntry('Host','fvs.io')
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        api_call = oRequest.getRealUrl()

        if (api_call):
            return True, api_call  + '|User-Agent=' + UA + '&verifypeer=false'

        return False, False
