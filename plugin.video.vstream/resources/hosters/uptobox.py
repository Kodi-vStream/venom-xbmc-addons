# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#

from resources.hosters.hoster import iHoster
from resources.hosters.uptostream import cHoster as uptostreamHoster
from resources.lib.comaddon import dialog, VSlog, addon, siteManager
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.sites import siteuptobox


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uptobox', 'Uptobox', 'violet')
        self.oPremiumHandler = None

    def setUrl(self, url):
        url = str(url).replace('iframe/', '')
        url = url.replace('http:', 'https:')
        url = url.split('?aff_id')[0]
        super(cHoster, self).setUrl(url)

    def checkUrl(self, sUrl):
        return True

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if self.oPremiumHandler.isPremiumModeAvailable():
            ADDON = addon()

            try:
                mDefault = int(ADDON.getSetting("hoster_uptobox_mode_default"))
            except AttributeError:
                mDefault = 0

            if mDefault == 0:
                ret = dialog().VSselect(['Passer en Streaming (via Uptostream)', 'Rester en direct (via Uptobox)'],
                                        'Choissisez votre mode de fonctionnement')
            else:
                # 0 is ask me, so 1 is uptostream and so on...
                ret = mDefault - 1

            # mode stream
            if ret == 0:
                return self._getMediaLinkForGuest()
            # mode DL
            if ret == 1:
                return self._getMediaLinkByPremiumUser()

            return False

        else:
            VSlog('UPTOBOX - no premium')
            return self._getMediaLinkForGuest()

    def _getMediaLinkForGuest(self):
        URL_MAIN = siteManager().getUrlMain(siteuptobox.SITE_IDENTIFIER)
        site_extension = '.' + URL_MAIN.split('.')[1]

        self._url = self._url.replace('uptobox.com/', 'uptostream' + site_extension)
        self._url = self._url.replace('uptobox.eu/', 'uptostream' + site_extension)
        self._url = self._url.replace('uptobox.link/', 'uptostream' + site_extension)
        self._url = self._url.replace('/uptobox.', '/uptostream.')

        # On redirige vers le hoster uptostream
        oHoster = uptostreamHoster()
        oHoster.setUrl(self._url)
        return oHoster.getMediaLink()

    def _getMediaLinkByPremiumUser(self):

        token = self.oPremiumHandler.getToken()
        if not token:
            return self._getMediaLinkForGuest()

        URL_MAIN = siteManager().getUrlMain(siteuptobox.SITE_IDENTIFIER)
        site_extension = '.' + URL_MAIN.split('.')[1]
        fileCode = self._url.split('/')[-1].split('?')[0]
        url1 = URL_MAIN + "api/link?token=%s&file_code=%s" % (token, fileCode)
        try:
            oRequestHandler = cRequestHandler(url1)
            dict_liens = oRequestHandler.request(jsonDecode=True)
            statusCode = dict_liens["statusCode"]
            if statusCode == 0:  # success
                sUrl = dict_liens["data"]["dlLink"]
                sUrl = sUrl.replace('.com/', site_extension)
                return True, sUrl

            if statusCode == 16:  # Waiting needed
                status = "Pas de compte Premium"  # dict_liens["data"]["waiting"]
            elif statusCode == 7:  # Invalid parameter
                status = dict_liens["message"] + ' : ' + dict_liens["data"]
            else:
                status = 'Erreur inconnue : %s, message = %s : %s' % (str(statusCode), dict_liens["message"], str(dict_liens["data"]))
        except Exception as e:
            status = e

        VSlog('UPTOBOX - ' + str(status))

        return False
