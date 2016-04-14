from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import urlresolver

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'RSLVR-'
        self.__sRealHost = '???'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]'+ self.__sDisplayName + self.__sRealHost + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'resolver'

    def setRealHost(self, sName):
        self.__sRealHost = sName
        
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
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self,media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        sUrl = self.__sUrl
        
        hmf = urlresolver.HostedMediaFile(url=sUrl)
        if hmf.valid_url():
            stream_url = hmf.resolve()
            cConfig().log(stream_url)
            if stream_url:
                return True,stream_url
            
        return False, False
        
       
        
