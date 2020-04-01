#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidzStore'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'vidzstore'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = '<iframe src="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    #Extraction du lien et decodage si besoin
    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'file: "([^"]+)\"'
        aResult = oParser.parse(sHtmlContent, sPattern)


        if (aResult[0]):
            api_call = aResult[1][0]

        if (api_call):
            return True, api_call

        return False, False


#Attention : Pour fonctionner le nouvel hebergeur doit etre rajoute dans le corps de Vstream, fichier Hosters.py.
#----------------------------------------------------------------------------------------------------------------
#
#Code pour selection de plusieurs liens
#--------------------------------------
#
#            from resources.lib.comaddon import dialog
#
#            url=[]
#            qua=[]
#            api_call = False
#
#            for aEntry in aResult[1]:
#                url.append(aEntry[0])
#                qua.append(aEntry[1])
#
#            #Afichage du tableau
#            api_call = dialog().VSselectqual(qua, url)
#
#             if (api_call):
#                  return True, api_call

#             return False, False
#
