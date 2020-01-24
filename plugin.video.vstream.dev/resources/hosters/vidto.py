from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re, time, xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidTo'
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
        return 'vidto'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('http://vidto.me/', '')
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl= re.sub(r'\-.*\.html', '', self.__sUrl)
        self.__sUrl = 'http://vidto.me/' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '<input type="hidden" name="([^"]+)" value="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            time.sleep(7)
            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])

            oRequest.addParameters('referer', self.__sUrl)
            sHtmlContent = oRequest.request()
            sHtmlContent = sHtmlContent.replace('file:""', '')

            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern =  ',file:"([^"]+)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    return True, aResult[1][0]
            else:
                sPattern = '{file:"([^"]+)",label:"(\d+p)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    url=[]
                    qua=[]
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                if len(url) == 1:
                    return True, url[0]

                elif len(url) > 1:
                    return True, url[0] #240p de nos jours serieux dialog choix inutile max vue 360p pour le moment

        return False, False
