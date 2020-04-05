#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#french-stream /18117-la-frontire-verte-saison-1.html
#liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'SendVid'
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
        return 'sendvid'

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
        
        api_call = ''

        data = 'r=&d='+self.__sUrl.split('/')[2]
        oRequest = cRequestHandler("https://sendvid.net/api/source/" + self.__sUrl.split('/')[4])
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Content-Length', len(str(data)))
        oRequest.addParametersLine(data)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  '"file":"([^"]+)","label":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        from resources.lib.comaddon import dialog

        url=[]
        qua=[]
        api_call = False

        for aEntry in aResult[1]:
           url.append(aEntry[0])
           qua.append(aEntry[1])

        api_call = dialog().VSselectqual(qua, url)

        if (api_call):
             return True, api_call

        return False, False
