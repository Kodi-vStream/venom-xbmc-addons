from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import xbmcgui, re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vid.ag'
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
        return 'vid_ag'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "ref=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl;

    def setUrl(self, sUrl):       
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self,url):
        r = re.search('\/\/((?:www\.)?vid\.ag)\/(?:embed-)?([0-9A-Za-z]+)', url)
        if r:
            return 'http://%s/embed-%s.html' % (r.groups()[0], r.groups()[1])
        else:
            return False

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        web_url = self.getUrl(self.__sUrl)
        
        oRequest = cRequestHandler(web_url)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        #Dean Edwards Packer
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sUnpacked = cPacker().unpack(aResult[1][0])
            sHtmlContent = sUnpacked
            
        sPattern = 'file\s*:\s*"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]
            return True, api_call
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False, False
        
        return False, False
