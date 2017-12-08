#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import xbmcgui,re
import base64

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
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return '';

    def setUrl(self, sUrl):
        #http://iframe-secured.com/embed/evovinec
        #http://iframe-secured.com/embed/iframe.php?u=evovinec
        self.__sUrl = sUrl.replace('http://iframe-secured.com/embed/','')
        self.__sUrl = 'http://iframe-secured.com/embed/iframe.php?u=%s' % self.__sUrl

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
        aResult = re.findall(sPattern,sHtmlContent)

        if (aResult):
            sUnpacked = cPacker().unpack(aResult[0])
            sHtmlContent = sUnpacked

            if (sHtmlContent):

                #window.location.replace(\'//rutube.ru/play/embed/10622163?p=gaY1LJ7uN2y6xhfO2mUCoA\');

                oParser = cParser()
                sPattern = "replace\(.*'(.+?)'"
                aResult = oParser.parse(sHtmlContent, sPattern)

                if (aResult[0] == True):

                    from resources.lib.gui.hoster import cHosterGui

                    sHosterUrl = aResult[1][0]

                    if not sHosterUrl.startswith('http:') and not sHosterUrl.startswith('https:'):
                        sHosterUrl = 'http:%s' % sHosterUrl

                    sHosterUrl = sHosterUrl.replace('\\', '')


                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    oHoster.setUrl(sHosterUrl)
                    api_call = oHoster.getMediaLink()

                    if (api_call[0] == True):
                        return True, api_call[1]


        return False, False
