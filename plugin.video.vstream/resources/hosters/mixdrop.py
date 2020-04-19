#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
# from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Mixdrop'
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
        return 'mixdrop'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace("/f/","/e/")

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''

        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Cookie', 'hds2=1')
        sHtmlContent = oRequest.request()

        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)

        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'wurl="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]

            #else:
                #sPattern = 'vsrc\d+="([^"]+)"'
                #aResult = oParser.parse(sHtmlContent, sPattern)
                #if (aResult[0] == True):
                #    api_call = aResult[1][0]

                #else:
                #    sPattern = 'furl="([^"]+)"'
                #    aResult = oParser.parse(sHtmlContent, sPattern)
                #    if (aResult[0] == True):
                #        api_call = aResult[1][0]

            if api_call.startswith('//'):
                api_call = 'https:' + aResult[1][0]

            if (api_call):
                return True, api_call

        return False, False
