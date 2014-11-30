from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vk'
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

    def setHD(self, sHD):
        if 'hd' in sHD:
            self.__sHD = 'HD'
        else: 
            self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def getPluginIdentifier(self):
        return 'vk'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "?([^<]+)"
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
        
    def __getKey(self):
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'fkzd="(.+?)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.','%2E')
            return aResult

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        url=[]
        qua=[]
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern =  '"url.+?":"(.+?)\.(\d+).mp4'
              
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            cConfig().showInfo(self.__sDisplayName, 'Streaming')
            for aEntry in aResult[1]:
                 url.append(aEntry[0])
                 qua.append(str(aEntry[1]))
             
            dialog2 = xbmcgui.Dialog()
            ret = dialog2.select('Select Quality',qua)
            #sUrl = url[ret]+'.'+qua[ret]+'.mp4'
            api_call = ('%s.%s.mp4') % (url[ret], qua[ret])
            return True, api_call
        else:
            cConfig().showInfo(self.__sDisplayName, 'Fichier introuvable')
            return False, False
        
        return False, False