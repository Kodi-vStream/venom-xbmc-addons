# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser 
from resources.hosters.hoster import iHoster
import json

from resources.lib.comaddon import VSlog


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Alldebrid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'alldebrid'

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
        # self.__sUrl = self.__sUrl.replace('https://', 'http://')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        Token_Alldebrid = cPremiumHandler(self.getPluginIdentifier()).getToken()
        if Token_Alldebrid:
            sUrl_Bypass = "https://api.alldebrid.com/v4/link/unlock?agent=service&version=1.0-&apikey=" + Token_Alldebrid + "&link=" + self.__sUrl
        else:
            return False, False

        oRequest = cRequestHandler(sUrl_Bypass)
        sHtmlContent = json.loads(oRequest.request())
        
        if 'error' in sHtmlContent:
            if sHtmlContent['error']['code'] == 'LINK_HOST_NOT_SUPPORTED':
                return False, self.__sUrl # si alldebrid ne prend pas en charge ce type de lien, on retourne le lien pour utiliser un autre hoster
            else:
                VSlog('Hoster Alldebrid - Error: ' + sHtmlContent["error"]['code'])
                return False, False
        
        api_call = HostURL = sHtmlContent["data"]["link"]
        try:
            mediaDisplay = HostURL.split('/')
            VSlog('Hoster Alldebrid - play : %s/ ... /%s' % ('/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog('Hoster Alldebrid - play : ' + HostURL)
        
        if (api_call):
            # api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            return True, api_call

        return False, False
