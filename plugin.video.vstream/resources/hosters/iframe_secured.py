#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#stream elite
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Iframe-Secured'
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
        return 'iframe_secured'

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):

        #http://iframe-secured.com/embed/evovinec
        #http://iframe-secured.com/embed/iframe.php?u=evovinec
        self.__sUrl = sUrl.replace('http://iframe-secured.com/embed/', '')
        self.__sUrl = self.__sUrl.replace('//iframe-secured.com/embed/', '')
        self.__sUrl = 'http://iframe-secured.com/embed/iframe.php?u=%s' % self.__sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''

        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self.__sUrl.replace('iframe.php?u=', ''))
        sHtmlContent = oRequest.request()

        sPattern = '<input  id=".+?name="([^"]+)" type="hidden" value="([^"]+)"/><input  id="challenge" name="([^"]+)" type="hidden" value="([^"]+)"/>'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            postdata = aResult[1][0][0] + '=' + aResult[1][0][1] + '&' + aResult[1][0][2] + '=' + aResult[1][0][3]

            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(1)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self.__sUrl)
            oRequest.addParametersLine(postdata)

            sHtmlContent = oRequest.request()

            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern, sHtmlContent)

            if (aResult):
                sUnpacked = cPacker().unpack(aResult[0])
                sHtmlContent = sUnpacked
                if (sHtmlContent):
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
