# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        # Nom a afficher dans vStream
        self.__sDisplayName = 'NinjaStream'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    # facultatif mais a laisser pour compatibilitee
    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    # facultatif mais a laisser pour compatibilitee
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        # Nom du fichier exact sans .py
        return 'ninjastream'

    # facultatif mais a laisser pour compatibilitee
    def setHD(self, sHD):
        self.__sHD = ''

    # facultatif mais a laisser pour compatibilitee
    def getHD(self):
        return self.__sHD

    # Telechargement possible ou pas sur ce host ?
    def isDownloadable(self):
        return True

    # Ne sert plus
    def isJDownloaderable(self):
        return True

    # facultatif mais a laisser pour compatibilitee
    def getPattern(self):
        return ''

    # facultatif mais a laisser pour compatibilitee
    def __getIdFromUrl(self, sUrl):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0]):
            return aResult[1][0]

        return ''

    # premiere fonction utilisee, memorise le lien
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    # facultatif mais a laisser pour compatibilitee
    def checkUrl(self, sUrl):
        return True

    # facultatif mais a laisser pour compatibilitee
    def __getUrl(self, media_id):
        return

    # Fonction appelle par Vstream pour avoir le lien decode
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    # Extraction du lien et decodage si besoin
    def __getMediaLinkForGuest(self):
        oRequestHandler = cRequestHandler("https://ninjastream.to/api/video/get")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', self.__sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://{0}'.format(self.__sUrl.split('/')[2]))
        oRequestHandler.addJSONEntry('id', self.__sUrl.split('/')[4])
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        api_call = sHtmlContent['result']['playlist']

        if api_call:
            # Rajout d'un header ?
            # api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            return True, api_call

        return False, False
