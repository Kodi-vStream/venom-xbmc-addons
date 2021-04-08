#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.pstream.net/e/xxxxx
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSPath, isMatrix
from resources.lib.parser import cParser


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

        api_call = ''
        url = self.__sUrl

        pathfile = 'special://temp/video_pstream.m3u8'
        if not isMatrix():
            video_pstream_path = VSPath(pathfile).decode('utf-8')
        else:
            video_pstream_path = VSPath(pathfile)

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'vstype.+?var.+?= "(.+?)";'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url2 = aResult[1][0].replace('" + "',"")

            oRequest = cRequestHandler(url2)
            oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sHtmlContent = oRequest.request()

            sPattern = "NAME=.([^\"']+).+?https([^#]+)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                url = []
                qua = []
                for aEntry in aResult[1]:
                    urls = 'https' + aEntry[1].strip()
                    qua.append(aEntry[0])
                    url.append(urls.strip())

                sUrlselect = dialog().VSselectqual(qua, url)

                sUrlselect = sUrlselect.strip()
                oRequest = cRequestHandler(sUrlselect)
                oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
                sHtmlContent = oRequest.request()

                if '#EXT' not in sHtmlContent:
                    return False, False

                with open(video_pstream_path, "w") as subfile:
                    subfile.write(sHtmlContent)

                api_call = video_pstream_path

        if (api_call):
            return True, api_call

        return False, False
