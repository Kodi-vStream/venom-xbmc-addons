from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import xbmcgui, re, time

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vidzi'
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
        return 'vidzi'

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
        self.__sUrl = sUrl.replace('http://vidzi.tv/', '')
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl=re.sub(r'\-.*\.html',r'',self.__sUrl)
        self.__sUrl = self.__sUrl.replace('.html', '')
        self.__sUrl = 'http://vidzi.tv/' + str(self.__sUrl)+'.html'

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        #Dexieme test Dean Edwards Packer
        oParser = cParser()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
                sUnpacked = cPacker().unpack(aResult[1][0])
                
                sPattern =  'file:"([^"]+\.mp4)'
                aResult = oParser.parse(sUnpacked, sPattern)

                if (aResult[0] == True):
                    api_call = aResult[1][0]
              
                return True, api_call
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False, False
        
        return False, False