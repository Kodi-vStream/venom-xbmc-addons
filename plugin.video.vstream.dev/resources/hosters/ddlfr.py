#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import progress, VSlog
import re
import base64

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'ddlfr'
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
        return 'ddlfr'

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
        VSlog("getMediaLink")
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        sHtmlContent = oRequest.request()
        #VSlog(sHtmlContent)
        oParser = cParser()
        sPattern = 'JuicyCodes\.Run\("(.+?)"\);'
        aResult = oParser.parse(sHtmlContent, sPattern)
        #VSlog(aResult)
        if (aResult[0] == True):

            media =  aResult[1][0].replace('+', '')
            media = base64.b64decode(media)

            #cPacker decode
            from resources.lib.packer import cPacker
            media = cPacker().unpack(media)
            #VSlog(media)
            if (media):

                sPattern = '{"file":"(.+?)","label":"(.+?)"'
                aResult = oParser.parse(media, sPattern)
                #VSlog(aResult)
                if (aResult[0] == True):
                #initialisation des tableaux
                    url=[]
                    qua=[]
                #Remplissage des tableaux
                    for i in aResult[1]:
                        url.append(str(i[0]+ '|Referer=' + self.__sUrl))
                        qua.append(str(i[1]))
                #Si une seule url
                    api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
