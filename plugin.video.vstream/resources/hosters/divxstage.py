#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# site clone auroravid|novamov
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import urllib
from resources.lib.util import VScreateDialogSelect
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DivxStage'
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
        return 'divxstage'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.rsplit('/', 1)[1] 
        self.__sUrl = self.__sUrl.replace('?v=', '')
        self.__sUrl = 'http://www.cloudtime.to/embed/?v=' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '<source src="(.+?)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            #tableau choix de serveur
            url=[]
            serv=[]
            
            No = 1
            for i in aResult[1]:
                url.append(str(i))
                serv.append('Liens '+str(No))
                No += 1
            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Afichage du tableau
                ret = VScreateDialogSelect(serv)
                if (ret > -1):
                    api_call = url[ret]

        if (api_call):
            return True, api_call + '|User-Agent=' + UA 

        return False, False
