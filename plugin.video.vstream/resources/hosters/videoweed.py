#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.util import VScreateDialogSelect

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VideoWeed'
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
        return 'videoweed'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://www.videoweed.es/', '')
        self.__sUrl = self.__sUrl.replace('http://www.bitvid.sx/', '')
        self.__sUrl = self.__sUrl.replace('http://embed.videoweed.es/', '')
        self.__sUrl = self.__sUrl.replace('file/', '')
        self.__sUrl = self.__sUrl.replace('embed.php?v=', '')
        self.__sUrl = self.__sUrl.replace('embed/?v=', '')
        self.__sUrl = self.__sUrl.replace('&width=711&height=400', '')
        self.__sUrl = 'http://www.bitvid.sx/embed/?v=' + str(self.__sUrl)


    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern =  '<source src="([^"]+)" type=\'(.+?)\'>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            url=[]
            qua=[]

            for aEntry in aResult[1]:
                url.append(aEntry[0])
                qua.append(aEntry[1])

            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
                #Afichage du tableau
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]
                    
        if (api_call):
            return True,api_call + '|User-Agent=' + UA 
            
        return False, False
 
