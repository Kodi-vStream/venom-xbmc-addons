#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):

        self.__sDisplayName = 'Dood'
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
        return 'dood'

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
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('/e/','/d/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  '<a href="([^"]+)" class="btn btn-primary d-flex align-items-center justify-content-between">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            urlDonwload = "https://" + self.__sUrl.split('/')[2] + "/" + aResult[1][0]

            oRequest = cRequestHandler(urlDonwload)
            sHtmlContent = oRequest.request()

            oParser = cParser()
            sPattern =  "window.open\('(.+?)\'"
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0]):
                api_call = aResult[1][0]

        if (api_call):
            api_call = api_call + '|Referer=' + urlDonwload
            return True, api_call

        return False, False
