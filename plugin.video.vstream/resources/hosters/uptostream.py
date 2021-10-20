# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.config import GestionCookie
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, isMatrix, CountdownDialog, xbmc
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote
import json, requests, re

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
                    Files.append(url.replace('.vtt','.srt'))
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

        s = requests.Session()
        s.headers.update({"Cookie": cookies})

        r = s.get('https://uptobox.com/api/streaming?file_code=' + self.__sUrl.split('/')[-1]).json()
        
        if r["statusCode"] != 0: # Erreur
            dialog().VSinfo(r["data"])
            return False, False

        r1 = s.get(r["data"]["user_url"]).text
        tok = re.search('token.+?;.+?;(.+?)&', r1).group(1)

        if not xbmc.getCondVisibility('system.platform.android'):
            # Si possible on ouvre la page automatiquement dans un navigateur internet.
            import webbrowser
            webbrowser.open(r['data']['user_url'])
            with CountdownDialog("Autorisation nécessaire", "Pour voir cette vidéo, veuillez vous connecter", "Allez sur ce lien : " + r['data']['user_url'], "Et valider le pin : " + r['data']['pin'], True, r["data"]['expired_in'], 10) as cd:
                js_result = cd.start(self.__check_auth, [r["data"]["check_url"]])["data"]
        else:
            from resources.lib import pyqrcode
            from resources.lib.librecaptcha.gui import cInputWindowYesNo
            qr = pyqrcode.create(r['data']['user_url'])
            qr.png('special://home/userdata/addon_data/plugin.video.vstream/qrcode.png', scale=5)
            oSolver = cInputWindowYesNo(captcha='special://home/userdata/addon_data/plugin.video.vstream/qrcode.png', msg="Scanner le QRCode pour acceder au lien d'autorisation", roundnum=1)
            retArg = oSolver.get()
            DIALOG = dialog()
            if retArg == "N":
                return False

            js_result = s.get(r["data"]["check_url"]).json()["data"]

        #Deux modes de fonctionnement different.
        if js_result.get("streamLinks").get('src'):
            api_call = js_result['streamLinks']['src'].replace(".m3u8",".mpd")
        else:
            sPattern = "'(.+?)': {(.+?)}"

            oParser = cParser()
            aResult = oParser.parse(js_result["streamLinks"], sPattern)

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

        try:
            SubTitle = self.checkSubtitle(js_result["subs"])
        except:
            VSlog("Pas de sous-titre")

        if (api_call):
            if SubTitle:
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False

    def __check_auth(self, url):
        try:
            js_result = json.loads(requests.get(url).content)
        except ValueError:
            raise ResolverError('Unusable Authorization Response')

        if js_result.get('statusCode') == 0:
            if js_result.get('data') == "wait-pin-validation":
                return False
            else:
                return js_result

        raise ResolverError('Error during check authorisation.')
