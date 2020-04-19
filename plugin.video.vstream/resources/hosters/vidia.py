#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

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
        self.__sDisplayName = 'Vidia'
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
        return 'vidia'

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
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        

        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = '{file:"([^"]+)"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
             
            api_call = aResult[1][0].replace(',','').replace('master.m3u8','index-v1-a1.m3u8')
            
            

        if (api_call):
            return True, api_call

        return False, False