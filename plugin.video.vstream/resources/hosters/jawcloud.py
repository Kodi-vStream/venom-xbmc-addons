#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
# from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Jawcloud'
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
        return 'jawcloud'

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

    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call =''

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        #VSlog(str(self.__sUrl))

        oParser = cParser()
        sPattern = '<source.+?src="(.+?)"'

        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            api_call = aResult[1][0]

        #VSlog(str(api_call))

        if (api_call):
            return True, api_call

        return False, False
