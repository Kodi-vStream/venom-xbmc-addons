#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.hosters.hoster import iHoster
from resources.lib.util import cUtil #Autres fonctions utiles
#et comaddon, exemple
from resources.lib.comaddon import VSlog

#AAdecoder
#from resources.lib.aadecode import AADecoder
#Cpaker decoder
#from resources.lib.packer import cPacker
#Jdecoder
#from resources.lib.jjdecode import JJDecoder
#Si premium
#from resources.lib.handler.premiumHandler import cPremiumHandler

#Ne garder que celles qui vous servent
import re

UA = 'User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        #Nom a afficher dans Vstream
        self.__sDisplayName = 'Mixcloud'
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
        return 'mixcloud'

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
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        #self.__sUrl = self.__sUrl.replace('https://', 'http://')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Referer','http://www.google.fr/')
        #sHtmlContent = oRequest.request()
        VSlog(sHtmlContent)

        oParser = cParser()
        aResult =  re.findall('https://audiocdn.+?mixcloud.com/previews/(.+?).mp3.+?sections&quot',sHtmlContent)
        #VSlog(str(aResult[0]))

        HosterUrl = 'https://testcdn.mixcloud.com/secure/dash2/' + aResult[0] + '.m4a/manifest.mpd'

        if (aResult[0]):
            api_call = HosterUrl

        if (api_call):
            return True, api_call

        return False, False
