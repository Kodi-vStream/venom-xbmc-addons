#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#https://gounlimited.to/embed-xxx.html
#top_replay robin des droits
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Gounlimited'
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
        return 'gounlimited'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        if not self.__sUrl.endswith('.mp4'):
            oParser = cParser()
            oRequest = cRequestHandler(self.__sUrl)
            sHtmlContent = oRequest.request()

            sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern =  '{src:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)

                # fh = open('c:\\test.txt', 'w')
                # fh.write(sHtmlContent)
                # fh.close()

                if (aResult[0] == True):
                    api_call = aResult[1][0]
        else:
            api_call = self.__sUrl

        if (api_call).endswith('.mp4'):
            return True, api_call
        else:
            return True, api_call + '|User-Agent=' + UA

        return False, False
