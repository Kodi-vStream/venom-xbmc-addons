#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Iframe-Secure'
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
        return 'iframe_secure'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('http://www.iframe-secure.com/embed/', '')
        self.__sUrl = sUrl.replace('//iframe-secure.com/embed/', '')
        self.__sUrl = 'http://www.iframe-secure.com/embed/iframe.php?u=%s' % self.__sUrl

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

        from resources.lib.packer import cPacker
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = re.findall(sPattern, sHtmlContent)

        if (aResult):
            sUnpacked = cPacker().unpack(aResult[0])
            sHtmlContent = sUnpacked

            if (sHtmlContent):

                oParser = cParser()
                sPattern = "replace\(.*'(.+?)'"
                aResult = oParser.parse(sHtmlContent, sPattern)

                if (aResult[0] == True):

                    from resources.lib.gui.hoster import cHosterGui

                    sHosterUrl = aResult[1][0]

                    if not sHosterUrl.startswith('http'):
                        sHosterUrl = 'http:%s' % sHosterUrl

                    sHosterUrl = sHosterUrl.replace('\\', '')
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    oHoster.setUrl(sHosterUrl)
                    api_call = oHoster.getMediaLink()

                    if (api_call[0] == True):
                        return True, api_call[1]

        return False, False
