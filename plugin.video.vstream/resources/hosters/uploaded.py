from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
from resources.lib.gui.gui import cGui

from resources.lib.handler.premiumHandler import cPremiumHandler

import urllib,urllib2
import xbmc

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Uploaded'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uploaded'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self,url):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def __getKey(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):

        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        print self.oPremiumHandler.isPremiumModeAvailable()

        if (not self.oPremiumHandler.isPremiumModeAvailable()):
            oDialog = cConfig().createDialogOK('ATTENTION, Pas de streaming sans premium.')
            return False,False

        cGui().showInfo('Resolve', self.__sDisplayName, 5)

        return self.__getMediaLinkByPremiumUser()


    def __getMediaLinkByPremiumUser(self):

        if not self.oPremiumHandler.Authentificate():
            return False, False

        url = self.__sUrl

        api_call = url + '|' + self.oPremiumHandler.AddCookies()

        #print api_call

        if (api_call):
            return True, api_call

        return False, False

    def GetMedialinkDL(self,sHtmlContent):
        return False
