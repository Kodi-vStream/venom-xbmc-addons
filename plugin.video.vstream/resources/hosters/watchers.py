#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
from resources.lib.packer import cPacker
import re,xbmcgui

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Watchers'
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
        return 'watchers'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return False

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
    
        sUrl = self.__sUrl
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            
        sPattern =  '{file:"(http.+?m3u8)"}' #sPattern = '{file:"([^"]+)",label:"(\d+)"}'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            m3url = aResult[1][0]
            oRequest = cRequestHandler(m3url)
            oRequest.addHeaderEntry('User-Agent',UA)
            oRequest.addHeaderEntry('Referer','http://watchers.to/player7/jwplayer.flash.swf')
            sHtmlContent = oRequest.request()

        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
   
        sPattern =  ',RESOLUTION=(.+?),.+?(http.+?m3u8)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))   
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
                    
        # ne fonctionne pas a partir des fichiers mp4 (video de 3 minutes) meme sur firefox ???      
        api_call = api_call + '|User-Agent='+ UA
        api_call = api_call + '&Referer=http://watchers.to/player7/jwplayer.flash.swf'
        
        if (api_call):
            return True, api_call
            
        return False, False
