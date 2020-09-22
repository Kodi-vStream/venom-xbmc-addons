#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Ovni crea
from resources.lib.parser import cParser 
from resources.hosters.hoster import iHoster
import requests
from resources.lib.comaddon import dialog

class cHoster(iHoster):

    def __init__(self):
        
        self.__sDisplayName = 'Gotochus'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'gotochus'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    #Ne sert plus
    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('https://gotochus.com/v/', 'https://gotochus.com/api/source/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        s=requests.Session()
        response = s.post(self.__sUrl)
        result = response.content
        print(result)

        oParser = cParser()
        sPattern = '"file":"([^"]+)","label":"([^"]+)"'
        aResult = oParser.parse(result, sPattern)
        
        
        if (aResult[0] == True):
            url = []
            qua = []
            for aEntry in aResult[1]:
                url.append(str(aEntry[0]))
                qua.append(str(aEntry[1]))
                
                api_call = dialog().VSselectqual(qua, url)
                


            if (api_call):
                s=requests.Session()
                response = s.head(api_call, allow_redirects=True)
                api_call = response.url
                
                return True, api_call
