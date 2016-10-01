from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import urllib,xbmc

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Cloudy'
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
        return 'cloudy'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        return sUrl;
        
    def __getKey(self):
        
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = 'key: "(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            return urllib.quote_plus(aResult[1][0].replace('.', '%2E'))

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('https://www.cloudy.ec/', '')
        self.__sUrl = self.__sUrl.replace('embed.php?id=', '')
        self.__sUrl = 'https://www.cloudy.ec/embed.php?id=' + str(self.__sUrl)
        #Patch en attendant kodi V17
        self.__sUrl = self.__sUrl.replace('https','http')

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        Key = self.__getKey()
        File = urllib.quote_plus(';' + self.__getIdFromUrl())
   
        api_call = 'http://www.cloudy.ec/api/player.api.php?user=undefined&codes=1&file=' + File + '&pass=undefined&key=' + Key
        
        oRequest = cRequestHandler(api_call)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        sPattern =  'url=(.+?)&title='
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            stream_url = urllib.unquote(aResult[1][0])
            #stream_url = stream_url + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
            return True, stream_url
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False, False
        
        return False, False
