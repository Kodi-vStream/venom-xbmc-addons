#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
import json


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Dustreaming'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'dustreaming'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def getMediaLink(self):
        
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''

        sUrl = self.__sUrl.replace('/v/', '/api/source/')
        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addHeaderEntry('Referer', self.__sUrl)
        oRequest.addParameters('r', '')
        oRequest.addParameters('d', 'dustreaming.fr')
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
