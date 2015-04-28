from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
import urllib
 
class cHoster(iHoster):
 
    def __init__(self):
        self.__sDisplayName = 'RuTube'
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
        self.__sUrl = sUrl.replace('http://rutube.ru/video/embed/', '')
        self.__sUrl = self.__sUrl.replace('http://video.rutube.ru/', '')
        self.__sUrl = self.__sUrl.replace('http://rutube.ru/video/', '')
        self.__sUrl = 'http://rutube.ru/play/embed/' + str(self.__sUrl)
        self.__sUrl = str(self.__modifyUrl(self.__sUrl))
   
    def __getIdFromUrl(self):
        sPattern = "http://rutube.ru/play/embed/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
 
        return ''
       
    def __modifyUrl(self, sUrl):
        api = ('http://rutube.ru/api/play/trackinfo/%s/?format=json') % (self.__getIdFromUrl())
 
        oRequest = cRequestHandler(api)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '').replace('//', '')
       
        sPattern = 'src="(.+?)"'
       
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            self.__sUrl = 'http://' + aResult[1][0]
            return self.__sUrl
           
        return
 
 
    def getPluginIdentifier(self):
        return 'rutube'
 
    def isDownloadable(self):
        return True
 
    def isJDownloaderable(self):
        return True
 
    def getPattern(self):
        return '';
 
    def checkUrl(self, sUrl):
        return True
 
    def getUrl(self):
        return self.__sUrl
 
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
 
    def __getMediaLinkForGuest(self):
       
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
 
        sPattern = '&quot;m3u8&quot;: &quot;(.+?);}, &quot;live_streams&quot;:'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
 
        if (aResult[0] == True):
            cGui().showInfo(self.__sDisplayName, 'Streaming', 5)
            return True, aResult[1][0]
           
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False, False
           
 
        return False, False
