#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
# Ne marche pas, ne marchera que sous kodi V17
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

#import ssl,urllib2
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'RapidVideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'rapidvideo'
        
    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
    
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        #VSlog(self.__sUrl)
        api_call = False
          
        oRequest = cRequestHandler(self.__sUrl)
        #oRequest.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
        #oRequest.addHeaderEntry('Upgrade-Insecure-Requests','1')
        #oRequest.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        #oRequest.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        oParser = cParser()
        sPattern =  '"file":"([^"]+)","label":"([0-9]+)p"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0]):
            url=[]
            qua=[]
            
            for aEntry in aResult[1]:
                url.append(aEntry[0])
                qua.append(aEntry[1])

            #tableau
            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call
        
        return False, False
