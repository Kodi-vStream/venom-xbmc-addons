#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Ovni-crea
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser 
from resources.hosters.hoster import iHoster
import json
import xbmc
import xbmcaddon
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import addon, dialog, VSlog, xbmcgui, xbmc
#Si premium
from resources.lib.handler.premiumHandler import cPremiumHandler

from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Alldebrid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''
        self.oPremiumHandler = None

    def getDisplayName(self):
        return  self.__sDisplayName

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
        #self.__sUrl = self.__sUrl.replace('https://', 'http://')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        ADDON = addon()
        Token_Alldebrid = ADDON.getSetting('token_alldebrid')
        if Token_Alldebrid:
            sUrl_Bypass = "https://api.alldebrid.com/v4/link/unlock?agent=service&version=1.0-&apikey=" + Token_Alldebrid + "&link=" + self.__sUrl
        else:
            return False

        oRequest = cRequestHandler(sUrl_Bypass)
        sHtmlContent = json.loads(oRequest.request())
        
        HostURL = sHtmlContent["data"]["link"]
        VSlog(HostURL) #Garder le en cas que alldebrid change le fonctionnement
        api_call = HostURL
        

        if (api_call):
            #api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            return True, api_call

        return False, False