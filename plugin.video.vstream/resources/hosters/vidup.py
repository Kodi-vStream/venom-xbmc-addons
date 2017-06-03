#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.util import VScreateDialogSelect
import re

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
    
    def __getIdFromUrl(self, sUrl):
        sPattern = 'https*://vidup.me/([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __getKey(self,sHtmlContent):
        oParser = cParser()
        sPattern = "var mpri_Key='([^']+)';"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
            
        return ''
        
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl).replace('beta.vidup.me','vidup.me')
        self.__sUrl = re.sub('(-\d+x\d+\.html)','',self.__sUrl)
        self.__sUrl = self.__sUrl.replace('embed-', '')

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        sId = self.__getIdFromUrl(self.__sUrl)
        
        sUrl = 'http://vidup.me/embed-' + sId + '.html'

        stream_url = ''
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        key = self.__getKey(sHtmlContent)
        
        getCode = 'http://vidup.me/jwv/' + key
        oRequest = cRequestHandler(getCode)
        sHtmlContent2 = oRequest.request()
        unPacked = cPacker().unpack(sHtmlContent2)
        
        oParser = cParser()
        sPattern =  'vt=([^"]+)"'
        aResult = oParser.parse(unPacked, sPattern)
        if (aResult[0] == True):
            code = aResult[1][0]
            url=[]
            qua=[]
        
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
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    stream_url = url[ret]

        if (stream_url):
            return True, stream_url + '?direct=false&ua=1&vt=' + code
        
        return False, False
