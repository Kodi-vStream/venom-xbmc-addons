from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import urllib
#Novamov Auroravid
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'NovaMov'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'novamov'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def __getIdFromUrl(self,sUrl):
        sPattern = '(novamov.com|auroravid.to)([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def __getKey(self,sUrl):
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'flashvars.filekey="([^"]+)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.','%2E')
            return aResult

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://embed.novamov.com/', '')
        self.__sUrl = self.__sUrl.replace('http://novamov.com/', '')
        self.__sUrl = self.__sUrl.replace('/video/', '')
        self.__sUrl = self.__sUrl.replace('embed.php?v=', '')
        self.__sUrl = self.__sUrl.replace('&width=711&height=400', '')

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        cGui().showInfo('Resolve', self.__sDisplayName, 5)

        id = self.__getIdFromUrl(self.__sUrl)
        sUrl = 'http://www.auroravid.to/embed/?v=' + id
        cKey =  self.__getKey(sUrl)

        api_call = 'http://www.auroravid.to/api/player.api.php?key=' + cKey + '&file=' + id

        oRequest = cRequestHandler(api_call)
        sHtmlContent = oRequest.request()

        sPattern =  'url=(.+?)&title'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stream_url = urllib.unquote(aResult[1][0])
            return True, stream_url
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable', 5)
            return False, False

        return False
