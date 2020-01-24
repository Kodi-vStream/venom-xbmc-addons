#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#french-stream /18117-la-frontire-verte-saison-1.html
#liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
import urllib
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
        elif 'fembed.' in self.__sUrl:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'sendvid' in self.__sUrl:
            baseUrl = 'https://sendvid.net/api/source/'
        elif 'vfsplayer' in self.__sUrl:
            baseUrl = 'https://vfsplayer.xyz/api/source/'
        elif 'fsimg' in self.__sUrl:
            baseUrl = 'https://www.fsimg.info/api/source/'

        url = baseUrl + self.__sUrl.rsplit('/', 1)[1]


        postdata = 'r=' + urllib.quote_plus(self.__sUrl) + '&d=' + baseUrl.replace('https://','').replace('/api/source/','')

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Accept', '*/*')
        # oRequest.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
        # oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
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
            return True, api_call

        return False, False
