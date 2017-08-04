#-*- coding: utf-8 -*-
#https://www.cloudy.ec/embed.php?id=etc...
#http://www.cloudy.ec/v/etc...
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.util import VSlog,VScreateDialogSelect

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Cloudy'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

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
        
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        oParser = cParser()
        sPattern =  'id=([a-zA-Z0-9]+)'
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            self.__sUrl = 'https://www.cloudy.ec/embed.php?id=' + aResult[1][0] + '&playerPage=1'
            #Patch en attendant kodi V17
            self.__sUrl = self.__sUrl.replace('https','http')
        else:
            VSlog(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        sPattern =  '<source src="([^"]+)" type=\'(.+?)\'>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url = []
            qua = []
            for x in aResult[1]:
                url.append(x[0])
                qua.append(x[1])

            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Affichage du tableau
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]
                    
        if (api_call):
            return True, api_call + '|User-Agent=' + UA 
            
        return False, False
