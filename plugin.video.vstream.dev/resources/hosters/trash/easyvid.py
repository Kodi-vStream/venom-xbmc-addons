#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import xbmcgui, re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'EasyVid'
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
        return 'easyvid'

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

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        if 'File was deleted' in sHtmlContent:
            return False, False

        api_call = ''

        oParser = cParser()
        sPattern = '{file: *"([^"]+(?<!smil))"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        else:
            from resources.lib.packer import cPacker
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern, sHtmlContent)
            if (aResult):
                sUnpacked = cPacker().unpack(aResult[0])
                sHtmlContent = sUnpacked

                sPattern = '{file:"(.+?)",label:"(.+?)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                #initialisation des tableaux
                    url=[]
                    qua=[]
                #Remplissage des tableaux
                    for i in aResult[1]:
                        url.append(str(i[0]))
                        qua.append(str(i[1]))
                #Si une seule url
                    if len(url) == 1:
                        api_call = url[0]
                #si plus de une
                    elif len(url) > 1:
                #Affichage du tableau
                        dialog2 = xbmcgui.Dialog()
                        ret = dialog2.select('Select Quality', qua)
                        if (ret > -1):
                            api_call = url[ret]

        if (api_call):
            return True, api_call

        return False, False
