from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VideoWeed'
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
        return 'videoweed'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return 'flashvars.file=\"([^\"]+)\"';
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "v=([^&]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        if 'embed' in sUrl:
            self.__sUrl = str(self.__getIdFromUrl(sUrl))
            self.__sUrl = 'http://www.videoweed.es/file/' + str(self.__sUrl)
        else:
            self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        cGui().showInfo('Resolve', self.__sDisplayName, 5)
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
       
        sPattern = 'flashvars.file=\"([^<]+)\";.+?flashvars.filekey=\"([^"]+)\";';
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            api_call = ('http://www.videoweed.es/api/player.api.php?user=undefined&codes=1&file=%s'+'&pass=undefined&key=%s') % (aResult[1][0][0], aResult[1][0][1])
            
            oRequest = cRequestHandler(api_call)
            sHtmlContent = oRequest.request()
            
            sPattern =  'url=(.+?)&title='
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                return True, aResult[1][0]
            
            
        return False, False
        
        