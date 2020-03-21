#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom
#Hoster pour les liens https://hd-stream.xyz/embed/
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'HDStream'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'hd_stream'

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

        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()

        oParser = cParser()
        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):

            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'file":"([^"]+)".+?"label":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                url=[]
                qua=[]

                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1])

                api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
