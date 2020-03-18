#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#2 methode play
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Jetload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]' + ' ' + '(Il faut pairer son ip au site https://jlpair.net/ tous les 3h)'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'jetload'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('/e/', '/api/fetch/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        #type 1

        sPattern = '{"src":"([^"]+)","type":"video/mp4"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        # #type 2
        # sPattern1 = 'src: *"(.+?.mp4)",'
        # aResult1 = oParser.parse(sHtmlContent, sPattern1)
        # if (aResult1[0] == True):
            # return True, aResult1[1][0]

        # #type ?
        # sPattern1 = '<input type="hidden" id="file_name" value="([^"]+)">'
        # aResult1 = oParser.parse(sHtmlContent, sPattern1)
        # if (aResult1[0] == True):
            # FN = aResult1[1][0]


        # sPattern = '<input type="hidden" id="srv_id" value="([^"]+)">'
        # aResult = oParser.parse(sHtmlContent, sPattern)
        # if (aResult[0] == True):
            # SRV = aResult[1][0]

            # pdata = 'file_name=' + FN + '.mp4&srv=' + SRV

            # oRequest = cRequestHandler('https://jetload.net/api/download')
            # oRequest.setRequestType(1)
            # #oRequest.addHeaderEntry('User-Agent', UA)
            # oRequest.addHeaderEntry('Referer', self.__sUrl)
            # oRequest.addHeaderEntry('Accept', 'application/json, text/plain, */*')
            # oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            # oRequest.addParametersLine(pdata)

            # api_call = oRequest.request()

        # #type ?
        # else:
            # sPattern = '<input type="hidden" id="srv" value="([^"]+)">'
            # aResult = oParser.parse(sHtmlContent, sPattern)
            # if (aResult1[0] == True):
                # Host = aResult[1][0]


                # api_call = Host + '/v2/schema/' + FN + '/master.m3u8'


        if (api_call):
            return True, api_call

        return False, False
