from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import re,xbmcgui
import urllib
#Novamov Auroravid
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Auroravid'
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
        return 'auroravid'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def __getIdFromUrl(self,sUrl):
        sPattern = '(novamov.com|auroravid.to)([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def __getKey(self,sUrl):
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'flashvars.filekey="([^"]+)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.','%2E')
            return aResult

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://www.auroravid.to/', '')
        self.__sUrl = self.__sUrl.replace('embed/?v=', '')
        self.__sUrl = 'http://www.auroravid.to/embed/?v=' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
         #cGui().showInfo('Resolve', self.__sDisplayName, 5)

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '<source src="(.+?)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            #tableau choix de serveur
            url=[]
            serv=[]

            for i in aResult[1]:
                url.append(str(i))
                serv.append(str(i[0:11]))
            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Serveur',serv)
                if (ret > -1):
                    api_call = url[ret]

        if (api_call):
            return True, api_call

        return False, False
