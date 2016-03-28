from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
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
        
        if 'plugin' not in sUrl:
            self.__sUrl = sUrl
            self.__sUrl = self.__sUrl.replace('http:', '')
            self.__sUrl = self.__sUrl.replace('https:', '')
            self.__sUrl = self.__sUrl.replace('//', '')
            self.__sUrl = self.__sUrl.replace('www.youtube.com', '')
            self.__sUrl = self.__sUrl.replace('www.youtube-nocookie.com', '')
            self.__sUrl = self.__sUrl.replace('youtu.be/', '')
            self.__sUrl = self.__sUrl.replace('/embed/', '')
            self.__sUrl = self.__sUrl.replace('/watch?v=', '')
            self.__sUrl = str(self.__sUrl)
        else:
            self.__sUrl = sUrl            

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        if 'plugin'  in self.__sUrl:
            return self.__getMediaLinkForPluging()
        else:
            return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        if xbmcaddon.Addon('plugin.video.youtube'):
            videoID = self.__sUrl
            
            #api_call = 'plugin://plugin.video.youtube/?action=play_video&videoid='+videoID
            api_call = 'plugin://plugin.video.youtube/play/?video_id='+videoID
            return True, api_call
        else:
            cGui().showInfo(self.__sDisplayName, 'Vous devez installer l\'addon video youtube' , 5)
            return False, False
            
    def __getMediaLinkForPluging(self):
        
        if xbmcaddon.Addon('plugin.video.youtube'):
            return True, self.__sUrl
        else:
            cGui().showInfo(self.__sDisplayName, 'Vous devez installer l\'addon video youtube' , 5)
            return False, False
        
