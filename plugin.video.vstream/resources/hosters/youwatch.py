#-*- coding: utf8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Youwatch'
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
        return 'youwatch'

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
        sPattern = "http://youwatch.org/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        if 'embed' not in sUrl:
            self.__sUrl = str(self.__getIdFromUrl(sUrl))
            self.__sUrl = 'http://youwatch.org/embed-'+str(self.__sUrl)+'.html'
            if not re.match('[0-9]+x[0-9]+.html',self.__sUrl,re.IGNORECASE):
                 self.__sUrl =  self.__sUrl.replace('.html','-640x360.html')
        else:
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
        
        oParser = cParser()
        
        sPattern ='<iframe[^<>]+?src="(.+?)" [^<>]+?> *<\/iframe>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
            oRequestHandler = cRequestHandler(aResult[1][0])
            oRequestHandler.addHeaderEntry('User-Agent',UA)
            oRequestHandler.addHeaderEntry('Referer',aResult[1][0])
            sHtmlContent = oRequestHandler.request()


        sPattern ='\[{file:"(.+?)",label:"(.+?)"}\]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return True , aResult[1][0][0] + '|Referer=' + self.__sUrl

        return False, False
        
        
