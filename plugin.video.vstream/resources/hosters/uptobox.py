# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, addon
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import QuoteSafe


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Uptobox'
        self.__sFileName = self.__sDisplayName
        self.oPremiumHandler = None

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uptobox'

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('iframe/', '')
        self.__sUrl = self.__sUrl.replace('http:', 'https:')
        self.__sUrl = self.__sUrl.split('?aff_id')[0]

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if (self.oPremiumHandler.isPremiumModeAvailable()):
            ADDON = addon()

            try:
                mDefault = int(ADDON.getSetting("hoster_uptobox_mode_default"))
            except AttributeError:
                mDefault = 0

            if mDefault == 0:
                ret = dialog().VSselect(['Passer en Streaming (via Uptostream)', 'Rester en direct (via Uptobox)'], 'Choissisez votre mode de fonctionnement')
            else:
                # 0 is ask me, so 1 is uptostream and so on...
                ret = mDefault - 1

            # mode stream
            if ret == 0:
                return self.__getMediaLinkForGuest()
            # mode DL
            if ret == 1:
                return self.__getMediaLinkByPremiumUser()
            
            return False

        else:
            VSlog('UPTOBOX - no premium')
            return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        self.__sUrl = self.__sUrl.replace('uptobox.com/', 'uptostream.com/')

        # On redirige vers le hoster uptostream
        from resources.hosters.uptostream import cHoster
        oHoster = cHoster()
        oHoster.setUrl(self.__sUrl)
        return oHoster.getMediaLink()

    def __getMediaLinkByPremiumUser(self):

        token = self.oPremiumHandler.getToken()
        if not token:
            return self.__getMediaLinkForGuest()

        fileCode = self.__sUrl.split('/')[-1].split('?')[0]
        url1 = "https://uptobox.com/api/link?token=%s&file_code=%s" % (token, fileCode)
        try:
            oRequestHandler = cRequestHandler(url1)
            dict_liens = oRequestHandler.request(jsonDecode=True)
            statusCode = dict_liens["statusCode"]
            if statusCode == 0:  # success
                return True, dict_liens["data"]["dlLink"]
    
            if statusCode == 16:  # Waiting needed
                status = "Pas de compte Premium" #dict_liens["data"]["waiting"]
            elif statusCode == 7:  # Invalid parameter 
                status = dict_liens["data"]["message"]
                status += ' - ' + dict_liens["data"]["data"]
            else:
                status = "Erreur inconnue : " + str(statusCode)
        except Exception as e:
            status = e
            
        VSlog('UPTOBOX - ' + status)

        return False
