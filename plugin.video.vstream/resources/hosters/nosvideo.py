#-*- coding: utf8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import urllib, urllib2, re
import base64

from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'NosVideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'nosvideo'

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
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        url = ''
        url2 = re.findall('var\stracker\s*=\s*[\'|\"](.+?)[\'|\"]',sHtmlContent)
        if (url2):
            url = url + url2[0]
        url2 = re.findall("tracker *: *[\'|\"](.+?)[\'|\"]",sHtmlContent)
        if (url2):
            url = url + url2[0]
        
        url3 = base64.b64decode(url)
        
        if (url3):
            #UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
            #url3 = url3 + '|User-Agent=' + UA + '&Referer=' + self.__sUrl
            return True , url3
        
        cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
        
        return False, False
