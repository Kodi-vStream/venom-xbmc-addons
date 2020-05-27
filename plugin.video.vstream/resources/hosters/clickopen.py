# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
import json
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
# meme code frenchvid etc.. fvsio


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'ClickOpen'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'clickopen'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        url = 'https://clickopen.win/api/source/' + self.__sUrl.rsplit('/', 1)[1]

        postdata = 'r=&d=clickopen.win'

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Accept', '*/*')
        # oRequest.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
        # oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequest.addHeaderEntry('Referer', self.__sUrl)
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
