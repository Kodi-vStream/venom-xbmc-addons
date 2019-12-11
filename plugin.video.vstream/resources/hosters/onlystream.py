#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'OnlyStream'
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
        return 'onlystream'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '(?:file|src): *"([^"]+)"[^{}<>]+?(?:, *label: *"([^"]+)")*}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            api_call = aResult[1][0][0]

        else:
            sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern =  '(?:file|src): *"([^"]+)"[^{}<>]+?(?:, *label: *"([^"]+)")*}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    url=[]
                    qua=[]
                    for i in aResult[1]:
                        url.append(str(i[0]))
                        if len(i) > 1:
                            q = str(i[1])
                        else:
                            q = "Inconnu"
                            qua.append(q)

                    api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
