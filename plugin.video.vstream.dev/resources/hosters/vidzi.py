#-*- coding: utf-8 -*-
#https://vidzi.tv/xxx.html
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vidzi'
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
        return 'vidzi'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('http://vidzi.tv/', '')
        self.__sUrl = self.__sUrl.replace('https://vidzi.tv/', '')
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl= re.sub(r'\-.*\.html', r'', self.__sUrl)
        self.__sUrl = self.__sUrl.replace('.html', '')
        self.__sUrl = 'https://vidzi.tv/' + str(self.__sUrl) + '.html'

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
        oParser = cParser()

        #lien direct
        sPattern = ',{file: *"([^"]+)"}\]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        #2 test Dean Edwards Packer
        else:
            sPattern = "<script type='text/javascript'>(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sUnpacked = cPacker().unpack(aResult[1][0])
                sPattern =  'file:"([^"]+\.mp4)'
                aResult = oParser.parse(sUnpacked, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]

        if (api_call):
            return True, api_call

        return False, False
