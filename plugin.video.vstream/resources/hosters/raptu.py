#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Rapidvideo'
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
        return 'raptu'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        
    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False
        
        sUrl = self.__sUrl

        oParser = cParser()
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        if 'rapidvideo' in sUrl:#qual site film illimite
            sPattern = '<a href="([^"]+&q=\d+p)"'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if (aResult[0] == True):
                url=[]
                qua=[]
                for i in aResult[1]:
                    url.append(str(i))
                    qua.append(str(i.rsplit('&q=', 1)[1]))
                
                if len(url) == 1:
                    api_call = url[0]

                elif len(url) > 1:
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality',qua)
                    if (ret > -1):
                        oRequest = cRequestHandler(url[ret])
                        sHtmlContent = oRequest.request()
                        sPattern = '<source src="([^"]+)" type="video/.+?"'
                        aResult = oParser.parse(sHtmlContent,sPattern)
                        if (aResult[0] == True):
                            api_call = aResult[1][0]
        else:
            sPattern = '{"file":"([^"]+)","label":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent,sPattern)
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
                    ret = dialog2.select('Select Quality',qua)
                    if (ret > -1):
                        api_call = url[ret]
       
        if (api_call):
            return True, api_call
            
        return False, False
