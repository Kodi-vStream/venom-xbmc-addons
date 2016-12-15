#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui

from resources.lib.packer import cPacker
import urllib, urllib2, re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Streamin.to'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName
    
    def setUrl(self, sUrl):
        self.__sUrl = sUrl
    
    def __getIdFromUrl(self,sUrl):
        sPattern = 'v=([^-]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        return

    def getPluginIdentifier(self):
        return 'streaminto'

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://streamin.to/', '')
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = 'http://streamin.to/embed/?v=' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        sId = self.__getIdFromUrl(self.__sUrl)

        web_url = 'http://streamin.to/embed-%s.html' % sId

        api_call =''

        oRequest = cRequestHandler(web_url)
        html = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(html)
        #fh.close()

        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e.+?)<\/script>'
        aResult = oParser.parse(html, sPattern)
        if (aResult[0] == True):
            html = cPacker().unpack(aResult[1][0])


        sPattern = 'file:"([^"]+)"'
        aResult = oParser.parse(html, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

            
        if (api_call):
            return True, api_call
            
        return False, False
 
