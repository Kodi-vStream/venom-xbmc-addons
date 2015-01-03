from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Azerfile'
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
        return 'azerfile'

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
        sPattern = "http://azerfile.com/embed-([^<]+)-640x340.html"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):        
        self.__sUrl = str(sUrl)
        
        sPattern =  'http://(?:www.|embed.|)azerfile.(?:com)/(?:video/|embed\-|)?([0-9a-z]+)'
         
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        self.__sUrl = 'http://azerfile.com/'+str(aResult[1][0])


    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        
        sPattern = 'file=([^<]+)&image';
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)


        if (aResult[0] == True):
            file = aResult[1][0]

            liste = file.split('/')

            #api_call = ('http://azerfile.com:%s/d/%s/video.mp4') % (liste[-1], liste[-2])
            api_call = aResult[1][0]
            return True, api_call
            
        return False, False
        
        