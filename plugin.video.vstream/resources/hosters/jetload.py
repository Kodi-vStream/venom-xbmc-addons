#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        #Nom a afficher dans Vstream
        self.__sDisplayName = 'Jetload'
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
        return 'jetload'

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
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        #oRequest.addHeaderEntry('Referer', 'http://www.google.fr/') #Rajoute un header
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '<input type="hidden" id="srv" value="([^"]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        host = ''.join(aResult[1])

        sPattern1 = '<input type="hidden" id="file_name" value="([^"]+)">'
        aResult1 = oParser.parse(sHtmlContent, sPattern1)
        fileName = ''.join(aResult1[1])

        api_call = host+'/v2/schema/'+fileName+'/master.m3u8'

        if (api_call):
            #Rajout d'un header ?
            #api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
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
#            #Affichage du tableau
#            api_call = dialog().VSselectqual(qua, url)
#
#             if (api_call):
#                  return True, api_call

#             return False, False
#
