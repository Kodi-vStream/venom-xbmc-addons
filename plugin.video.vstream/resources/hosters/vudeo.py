#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
#from resources.lib.util import cUtil #Autres fonctions utiles
#et comaddon, exemple
#from resources.lib.comaddon import addon, dialog, VSlog, xbmcgui, xbmc

#AAdecoder
#from resources.lib.aadecode import AADecoder
#Cpaker decoder
#from resources.lib.packer import cPacker
#Jdecoder
#from resources.lib.jjdecode import JJDecoder
#Si premium
#from resources.lib.handler.premiumHandler import cPremiumHandler

#Ne garder que celles qui vous servent
import re, urllib2, urllib

class cHoster(iHoster):

    def __init__(self):
        #Nom a afficher dans Vstream
        self.__sDisplayName = 'Vudeo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    #facultatif mais a laisser pour compatibilitee
    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    #facultatif mais a laisser pour compatibilitee
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        #Nom du fichier exact sans .py
        return 'vudeo'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern1 = 'sources.+?"([^"]+mp4)"'
        
        aResult = oParser.parse(sHtmlContent, sPattern1)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        if (api_call):
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False
