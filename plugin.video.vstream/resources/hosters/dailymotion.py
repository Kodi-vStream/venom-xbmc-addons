#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DailyMotion'
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

    def setHD(self, sHD):
        if 'hd' in sHD:
            self.__sHD = 'HD'
        else:
            self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def getPluginIdentifier(self):
        return 'dailymotion'

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://dai.ly/', '')
        self.__sUrl = self.__sUrl.replace('http://www.dailymotion.com/', '')
        self.__sUrl = self.__sUrl.replace('https://www.dailymotion.com/', '')
        self.__sUrl = self.__sUrl.replace('embed/', '')
        self.__sUrl = self.__sUrl.replace('video/', '')
        self.__sUrl = self.__sUrl.replace('sequence/', '')
        self.__sUrl = self.__sUrl.replace('swf/', '')
        self.__sUrl = 'http://www.dailymotion.com/embed/video/' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False
        url=[]
        qua=[]

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Cookie', "ff=off")
        sHtmlContent = oRequest.request()


        oParser = cParser()

        sPattern =  '{"type":"application.+?mpegURL","url":"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            oRequest = cRequestHandler(aResult[1][0])
            oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
            oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sHtmlContent = oRequest.request()

            sPattern = 'NAME="([^"]+)",PROGRESSIVE-URI="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                for aEntry in reversed(aResult[1]):
                    if aEntry[0] not in qua:
                        qua.append(aEntry[0])
                        url.append(aEntry[1])


            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
