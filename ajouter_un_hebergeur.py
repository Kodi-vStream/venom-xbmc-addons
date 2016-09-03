#-*- coding: utf-8 -*-
#Auteur
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster

#AAdecoder
#from resources.lib.aadecode import AADecoder
#Cpaker decoder
#from resources.lib.packer import cPacker
#Jdecoder
#from resources.lib.jjdecode import JJDecoder
#Si premium
#from resources.lib.handler.premiumHandler import cPremiumHandler

import re,urllib2,utllib
import xbmcgui,xmbc

class cHoster(iHoster):

    def __init__(self):
        #Nom a afficher
        self.__sDisplayName = 'Nouvel hebergeur'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]''

    #facultatif mais a laisser pour compatibilitee
    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    #facultatif mais a laisser pour compatibilitee
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        #Nom du fichier exact
        return 'ajouter_un_hebergeur'
        
    #facultatif mais a laisser pour compatibilitee
    def setHD(self, sHD):
        self.__sHD = ''
        
    #facultatif mais a laisser pour compatibilitee
    def getHD(self):
        return self.__sHD

    #Telechargement possible ou pas sur ce host ?
    def isDownloadable(self):
        return True

    #Ne sert plus
    def isJDownloaderable(self):
        return True

    #facultatif mais a laisser pour compatibilitee
    def getPattern(self):
        return ''
    
    #facultatif mais a laisser pour compatibilitee
    def __getIdFromUrl(self, sUrl):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    #premiere fonction utilisee, memorise le lien
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    #facultatif mais a laisser pour compatibilitee
    def checkUrl(self, sUrl):
        return True

    #facultatif mais a laisser pour compatibilitee
    def __getUrl(self, media_id):
        return
    
    #Fonction appelle par Vstream pour avoir le lien decode
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        #oRequest.addHeaderEntry('Referer','http://www.google.fr/') #Rajoute un header
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'file: *"([^<>"]+?mp4)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            return True, aResult[1][0]
        
        return False, False
