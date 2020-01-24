#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://mixloads.com/embed-xxx.html sur topreplay
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Mixloads'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + ' [/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'mixloads'

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

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '{file:"([^"]+)",label:"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            if len(url) == 1:
                api_call = url[0]

            elif len(url) > 1:
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality', qua)
                if (ret > -1):
                    api_call = url[ret]

        if (api_call):
            return True, api_call

        return False, False
