from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import urllib2,urllib,re
import base64

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Speedvideo'
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
        return 'speedvideo'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        try:
            oRequest = cRequestHandler(self.__sUrl)
            sHtmlContent = oRequest.request()
            
            linkfile=re.compile('var linkfile\s*=\s*"([A-Za-z0-9=]+)"').findall(sHtmlContent)[0]
            linkfileb=re.compile('var linkfile\s*=\s*base64_decode\(linkfile,\s*([A-Za-z0-9]+)\);').findall(sHtmlContent)[0]
            linkfilec=re.compile('var '+linkfileb+'\s*=\s*(\d+);').findall(sHtmlContent)[0]
            linkfilec=int(linkfilec)
            linkfilez=linkfile[:linkfilec]+linkfile[(linkfilec+10):]
            stream_url=base64.b64decode(linkfilez)
        except:
            stream_url = False

        if not(stream_url == False):
            api_call = stream_url
            return True, api_call
            
        return False, False
        
        
