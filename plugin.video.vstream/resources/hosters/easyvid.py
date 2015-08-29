from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
import xbmcgui, re, time

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'EasyVid'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'easyvid'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        return ''
        
    def __modifyUrl(self, sUrl):
        return '';

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
        
        sPattern = 'file: "([^{}<>]+?\.mp4)"}'
        
        oParser = cParser()
        #sHtmlContent=sHtmlContent.replace('|','/')
        aResult = oParser.parse(sHtmlContent, sPattern)


        if (aResult[0] == True):
            api_call = aResult[1][0]
            return True, api_call
            
        return False, False
        
