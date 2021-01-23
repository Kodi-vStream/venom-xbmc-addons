#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser 
from resources.hosters.hoster import iHoster
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import addon, VSlog, dialog

import json

URL_HOST = "https://debrid-link.fr"

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Debrid Link'
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
        return 'debrid_link'

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

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        Token_debrid_link = "Bearer " + addon().getSetting('hoster_debridlink_token')
        
        oRequestHandler = cRequestHandler(URL_HOST + '/api/downloader/add')
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept','application/json')
        oRequestHandler.addHeaderEntry('Authorization', Token_debrid_link)
        oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
        oRequestHandler.addParameters("link", self.__sUrl)
        text = json.loads(oRequestHandler.request())

        if (text["result"] == "KO"):
            if text["ERR"] == 'badToken':
                New_token = RenewToken()

                oRequestHandler = cRequestHandler(URL_HOST + '/api/downloader/add')
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Accept','application/json')
                oRequestHandler.addHeaderEntry('Authorization', New_token)
                oRequestHandler.addHeaderEntry('Content-Type',"application/x-www-form-urlencoded")
                oRequestHandler.addParameters("link", self.__sUrl)
                text = json.loads(oRequestHandler.request())

        api_call = text["value"]["downloadLink"]

        if (text):
            return True, api_call

        return False, False


def RenewToken():
    refreshTok = addon().getSetting('hoster_debridlink_tokenrefresh')
    if refreshTok == "":
        oRequestHandler = cRequestHandler(URL_HOST + "/api/oauth/device/code")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        oRequestHandler.addParameters('client_id',addon().getSetting('hoster_debridlink_ID'))
        r = json.loads(oRequestHandler.request())

        dialog().VSok('Allez sur la page : https://debrid-link.fr/device\n et rentrer le code ' + r["user_code"]  + ' pour autorisez la connection')

        oRequestHandler = cRequestHandler(URL_HOST + "/api/oauth/token")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        oRequestHandler.addParameters('client_id',addon().getSetting('hoster_debridlink_ID'))
        oRequestHandler.addParameters("code",r["device_code"])
        oRequestHandler.addParameters("grant_type","http://oauth.net/grant_type/device/1.0")
        r = json.loads(oRequestHandler.request())

        addon().setSetting('hoster_debridlink_tokenrefresh', r["refresh_token"])
        addon().setSetting('hoster_debridlink_token', r["access_token"])
        return r["access_token"]

    else:
        oRequestHandler = cRequestHandler(URL_HOST + "/api/oauth/token")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        oRequestHandler.addParameters('client_id',addon().getSetting('hoster_debridlink_ID'))
        oRequestHandler.addParameters("refresh_token",refreshTok)
        oRequestHandler.addParameters("grant_type","refresh_token")
        r = json.loads(oRequestHandler.request())

        addon().setSetting('hoster_debridlink_token', r["access_token"])
        return r["access_token"]
