#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster

import xbmc,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidUp'
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
        return 'vidup'
        
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

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        url=[]
        qua=[]
        stream_url = ''

        oParser = cParser()
        
        sPattern =  "label: '([0-9]+)p', file: '([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            for aEntry in aResult[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])
        else:
            sPattern = '"file":"([^"]+)","label":"([0-9]+)p"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0]):
                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1])            
                
        
        #Si une seule url
        if len(url) == 1:
            stream_url = url[0]
        #si plus de une
        elif len(url) > 1:
            #Afichage du tableau
            dialog2 = xbmcgui.Dialog()
            ret = dialog2.select('Select Quality',qua)
            if (ret > -1):
                stream_url = url[ret]
            else:
                return False, False
        else:
            return False, False

        if (stream_url):
            return True, stream_url
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
        
        return False, False
