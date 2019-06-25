#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

from resources.lib.aadecode import AADecoder
import re

from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MyStream'
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
        return 'mystream'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

        # sPattern =  '(?:https*:\/\/|\/\/)(?:www.|embed.|)mystream.(?:la|com|to)\/(?:video\/|external\/|embed-|)([0-9a-zA-Z]+)'
        # oParser = cParser()
        # aResult = oParser.parse(sUrl, sPattern)
        # self.__sUrl = 'https://mysembed.net/' + str(aResult[1][0])

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        #VSlog(self.__sUrl)
        url = self.__sUrl
        
        #url = self.__sUrl.replace('embed.mystream.to','mstream.cloud')
        #url = 'https://mstream.cloud/gfa35ebu1nt1'

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Encoding', 'identity')
        sHtmlContent = oRequest.request()

        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        oParser = cParser()
        
        api_call = False
        
        sPattern =  '(?:[>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = AADecoder(i).decode()
                
                #VSlog(decoded)
                
                r = re.search("\('src', '([^']+)'\);", decoded, re.DOTALL | re.UNICODE)
                if r:
                    api_call = r.group(1)
                    break
        
        #VSlog(api_call)
        
        if 'qziqcysljv' in api_call:
            api_call = ''

        if (api_call):
            return True, api_call

        return False, False
