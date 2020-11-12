#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog ,xbmc #,VSlog#
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Pstream'
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
        return 'pstream'

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
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        video_pstream_path = xbmc.translatePath('special://temp/video_pstream.m3u8')

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Accept', '*/*')
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = "v(?:k|s)uri.*?'([^\']+)';" 
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):

            url2 = aResult[1][0]
            oRequest = cRequestHandler(url2)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Accept', '*/*')
            sHtmlContent = oRequest.request()
            oParser = cParser()
            sPattern =  '"([^"]+)":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0]):
                url = []
                qua = []
                for aEntry in aResult[1]:
                    url.append(aEntry[1])
                    qua.append(aEntry[0])

                api_call = dialog().VSselectqual(qua, url)

            else :
                oParser = cParser()
                sPattern ="NAME=.([^\"']+).+?https([^#]+)"
                aResult = oParser.parse(sHtmlContent, sPattern)

                if (aResult[0]==True):

                    url = []
                    qua = []

                    for aEntry in aResult[1]:

                        urls = 'https' + aEntry[1].strip()
                        qua.append(aEntry[0])
                        url.append(urls.strip())

                    sUrlselect = dialog().VSselectqual(qua, url)

                    oRequest = cRequestHandler(sUrlselect)
                    oRequest.addHeaderEntry('User-Agent', UA)
                    oRequest.addHeaderEntry('Accept', '*/*')
                    sHtmlContent = oRequest.request()

                    with open(video_pstream_path , "w") as subfile:
                        subfile.write(sHtmlContent )

                    xbmc.sleep(200)
                    api_call = video_pstream_path

        if (api_call):
            return True, api_call

        return False, False
