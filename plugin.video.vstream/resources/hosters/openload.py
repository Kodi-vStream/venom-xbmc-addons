#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.jjdecode import JJDecoder
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.aadecode import AADecoder
import re,urllib2

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Openload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'openload'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
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
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        #Debut des tests de decodage
        oParser = cParser()
        string = ''
       
        #"aaencode - Encode any JavaScript program to Japanese style emoticons (^_^)"
        sPattern = "<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)<\/script"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            string = AADecoder(aResult[1][0]).decode()
                
        if not (string): 
            #Dean Edwards Packer
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sUnpacked = cPacker().unpack(aResult[1][0])
                string = JJDecoder(sUnpacked).decode()
        
        
        if (string):
            sContent = string.replace('\\','')
            
            api_call = ''

            sPattern = 'src=\s*?"(.*?)\?'
            aResult = oParser.parse(sContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]
                
            if not api_call:
                sPattern = 'window\.vr="(.+?)"'
                aResult = oParser.parse(sContent, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]

        if (api_call):
            return True, api_call
            
        return False, False
