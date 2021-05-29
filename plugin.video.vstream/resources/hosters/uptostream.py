# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import re
import json

from resources.lib.config import GestionCookie
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, isMatrix
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'UpToStream'
        self.__sFileName = self.__sDisplayName
        self.oPremiumHandler = None

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uptostream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        if self.__sUrl[-4:] in '.mp4.avi.mkv':
            return self.__sUrl.split('/')[3]
        return self.__sUrl.split('/')[-1]

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('iframe/', '')
        self.__sUrl = self.__sUrl.replace('http:', 'https:')

    def checkSubtitle(self, sHtmlContent):
        if sHtmlContent:
            Files = []
            lab = []
            for aEntry in sHtmlContent:
                if aEntry["label"] == "French":
                    url = aEntry["src"]
                    if not url.startswith('http'):
                        url = 'http:' + url
                    Files.append(url)
                else:
                    continue

            return Files
        return False

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler('uptobox')
        premium = self.oPremiumHandler.isPremiumModeAvailable()
        api_call = False
        SubTitle = ""

        if premium:
            self.oPremiumHandler.Authentificate()
        else:
            dialog().VSok('Ce hoster demande un login, meme gratuit.')
            return False, False

        cookies = GestionCookie().Readcookie("uptobox")
        import requests, re

        s = requests.Session()
        s.headers.update({"Cookie": cookies})

        r = s.get('https://uptobox.com/api/streaming?file_code=' + self.__sUrl.split('/')[-1]).json()
        
        if r["statusCode"] != 0: # Erreur
            dialog().VSinfo(r["data"])
            return False, False

        r1 = s.get(r["data"]["user_url"]).text
        tok = re.search('token.+?;.+?;(.+?)&', r1).group(1)

        r1 = s.post("https://uptobox.com/api/user/pin/validate?token=" + tok,json={"pin":r["data"]["pin"]}).json()
        s.headers.update({"Referer": "https://uptobox.com/pin?pin=" + r["data"]["pin"]})

        r = s.get(r["data"]["check_url"]).json()["data"]

        sPattern = "'(.+?)': {(.+?)}"

        oParser = cParser()
        aResult = oParser.parse(r["streamLinks"], sPattern)

        url = []
        qua = []
        api_call = False

        for aEntry in aResult[1]:
            QUAL = aEntry[0]
            d = re.findall("'u*(.+?)': u*'(.+?)'",aEntry[1])
            for aEntry1 in d:
                url.append(aEntry1[1])
                qua.append(QUAL  + ' (' + aEntry1[0] + ')')

        # Affichage du tableau
        api_call = dialog().VSselectqual(qua, url)

        SubTitle = self.checkSubtitle(r["subs"])

        if (api_call):
            if SubTitle:
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
