#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://vidoza.net/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.hosters.hoster import iHoster
from resources.lib.util import VScreateDialogSelect

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vidoza'        
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'vidoza'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern =  'sources: *\[{file:"([^"]+)",label:"([^"]+)"}'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Afichage du tableau
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]
  
        if (api_call):
            return True, api_call 

        return False, False
