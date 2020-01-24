#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://vidtodo.com/embed-xxx.html
#http://vidtodo.com/xxx
#http://vidtodo.com/xxx.html
#com,me
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:69.0) Gecko/20100101 Firefox/69.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidToDo'
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
        return 'vidtodo'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        if 'embed-' in self.__sUrl:
            self.__sUrl = self.__sUrl.replace('embed-','')
#        if not 'embed-' in self.__sUrl:
#            self.__sUrl = self.__sUrl.rsplit('/', 1)[0] + '/embed-' + self.__sUrl.rsplit('/', 1)[1]

        if not self.__sUrl.startswith('https'):
            self.__sUrl = self.__sUrl.replace('http', 'https')

        if not self.__sUrl.endswith('.html'):
            self.__sUrl = self.__sUrl + '.html'

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def extractSmil(self,smil):
        import re
        oRequest = cRequestHandler(smil)
        oRequest.addParameters('referer', self.__sUrl)
        sHtmlContent = oRequest.request()
        Base = re.search('<meta base="(.+?)"', sHtmlContent)
        Src = re.search('<video src="(.+?)"', sHtmlContent)
        return Base.group(1) + Src.group(1)

    def __getMediaLinkForGuest(self):
        api_call = ''
        
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Referer', self.__sUrl)
        oRequest.addParameters('User-Agent', UA)
        sHtmlContent = oRequest.request()

        sPattern = 'sources:* \[(?:{file:)*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                from resources.lib.packer import cPacker
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern = '{file: *"([^"]+smil)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    api_call = self.extractSmil(aResult[1][0])
                else:
                    sPattern = 'src:"([^"]+.mp4)"'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if (aResult[0] == True):
                        api_call = aResult[1][0] #.decode('rot13')

        if (api_call):
            return True, api_call

        return False, False
