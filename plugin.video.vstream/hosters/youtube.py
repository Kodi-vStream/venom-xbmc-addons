from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from hosters.hoster import iHoster
import xbmcaddon

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Youtube'
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
        return 'youtube'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://.+?/.+?/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        if 'embed' not in sUrl:
            self.__sUrl = str(self.__getIdFromUrl(sUrl))
            self.__sUrl = 'http://www.youtube.com/embed/' + str(self.__sUrl)
        else:
            self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        if xbmcaddon.Addon('plugin.video.youtube'):
            print 'passe'
            videoID = str(self.__getIdFromUrl(self.__sUrl))
            api_call = 'plugin://plugin.video.youtube/?action=play_video&videoid='+videoID
            return True, api_call
        else:
            cGui().showInfo(self.__sDisplayName, 'Vous devez installer l\'addon video youtube' , 5)
            return False, False
        