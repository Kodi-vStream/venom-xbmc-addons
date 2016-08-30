from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
import xbmcgui, re, time

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'V-Vids'
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
        return 'v_vids'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        return ''
        
    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):       
        self.__sUrl = sUrl.replace('http://v-vids.com/', '')
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl=re.sub(r'\-.*\.html',r'',self.__sUrl)
        self.__sUrl = 'http://v-vids.com/' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern =  '<input type="hidden" name="(.+?)" value="(.*?)">'
              
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True): 
            time.sleep(7)
            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])

            
            oRequest.addParameters('referer', self.__sUrl)
            sHtmlContent = oRequest.request()
            
            sPattern =  "file: '(.+?)'"
            
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                cGui().showInfo(self.__sDisplayName, 'Streaming', 5)
                return True, aResult[1][0]
            else:
                cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
                return False, False

        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False, False
        
        return False, False
