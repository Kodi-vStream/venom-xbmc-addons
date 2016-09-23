#-*- coding: utf-8 -*-
#Auteur
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.config import cConfig #config
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.hosters.hoster import iHoster
#from resources.lib.util import cUtil #Autres fonctions utiles

#AAdecoder
#from resources.lib.aadecode import AADecoder
#Cpaker decoder
#from resources.lib.packer import cPacker
#Jdecoder
#from resources.lib.jjdecode import JJDecoder
#Si premium
#from resources.lib.handler.premiumHandler import cPremiumHandler

#Ne garder que celles qui vous servent
import re,urllib2,urllib
import xbmcgui,xbmc

class cHoster(iHoster):

    def __init__(self):
        #Nom a afficher dans Vstream
        self.__sDisplayName = 'Nouvel hebergeur'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    #facultatif mais a laisser pour compatibilitee
    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    #facultatif mais a laisser pour compatibilitee
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        #Nom du fichier exact sans .py
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
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    #premiere fonction utilisee, memorise le lien
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        #self.__sUrl = self.__sUrl.replace('https://', 'http://')

    #facultatif mais a laisser pour compatibilitee
    def checkUrl(self, sUrl):
        return True

    #facultatif mais a laisser pour compatibilitee
    def __getUrl(self, media_id):
        return
    
    #Fonction appelle par Vstream pour avoir le lien decode
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    #Extraction du lien et decodage si besoin
    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        #oRequest.addHeaderEntry('Referer','http://www.google.fr/') #Rajoute un header
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'file: *"([^<>"]+?mp4)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = ''
        
        if (aResult[0]):
            api_call = aResult[1][0]
            
        if (api_call):
            #Rajout d'un header ?
            #api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            return True, api_call
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
        
        return False, False

        
#Attention : Pour fonctionner le nouvel hebergeur doit etre rajoute dans le corps de Vstream, fichier Hosters.py.
#----------------------------------------------------------------------------------------------------------------
#
#Code pour selection de plusieurs liens
#--------------------------------------
#
#            url=[]
#            qua=[]
#            
#            for aEntry in aResult[1]:
#                url.append(aEntry[0])
#                qua.append(aEntry[1])
#                
#            #Si une seule url
#            if len(url) == 1:
#                stream_url = url[0]
#            #si plus de une
#            elif len(url) > 1:
#                #Afichage du tableau
#                dialog2 = xbmcgui.Dialog()
#                ret = dialog2.select('Select Quality',qua)
#                if (ret > -1):
#                    stream_url = url[ret]
#                else:
#                    return False, False
#            else:
#                return False, False
#
