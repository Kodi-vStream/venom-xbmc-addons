#-*- coding: utf-8 -*-
#johngf
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.lib.config import cConfig 
from resources.lib.gui.gui import cGui 
from resources.hosters.hoster import iHoster

import xbmcgui

class cHoster(iHoster):

    def __init__(self):
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
        sPattern = 'http://vidlox.tv/([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)

        if (aResult[0] == True):
            return aResult[1][0]

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

        #recuperation de l'id et reformatage du lien
        id = self.__getIdFromUrl(self.__sUrl)
        sUrl = 'http://vidlox.tv/' + id

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sPattern =  ',{file:"(.+?)",label:"(.+?)"}'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            api_call = ''

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
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]
                else: 
                    return False, False
     
            
            if (api_call):
                return True, api_call 

            return False, False
