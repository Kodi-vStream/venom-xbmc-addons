#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.lib import util
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        if not (util.isKrypton() == True):
            self.__sDisplayName = '(Windows\Android Nécessite Kodi17)' + ' ' + 'Vidlox'
        else:
            self.__sDisplayName = 'Vidlox'        
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
        return 'vidlox'
        
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
    
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern =  '([^"]+\.mp4)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=["HD","SD"] #bidouille evite m3u8
            api_call = ''

            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i))

            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
                #Afichage du tableau
                ret = util.VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]
  
        if (api_call):
            return True, api_call 

        return False, False
