# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#

from resources.hosters.hoster import iHoster
from resources.hosters.uptostream import cHoster as uptostreamHoster
from resources.lib.comaddon import dialog, VSlog, addon
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser
from resources.lib.util import QuoteSafe


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uptobox', 'Uptobox', 'violet')
        self.oPremiumHandler = None

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('iframe/', '')
        self._url = self._url.replace('http:', 'https:')
        self._url = self._url.split('?aff_id')[0]

    def checkSubtitle(self, sHtmlContent):
        oParser = cParser()

        # On ne charge les sous titres uniquement si vostfr se trouve dans le titre.
        # if not re.search("<h1 class='file-title'>[^<>]+(?:TRUEFRENCH|FRENCH)[^<>]*</h1>",
        #   sHtmlContent, re.IGNORECASE):
        if "<track type='vtt'" in sHtmlContent:

            sPattern = '<track type=[\'"].+?[\'"] kind=[\'"]subtitles[\'"] src=[\'"]([^\'"]+).vtt[\'"] ' + \
                'srclang=[\'"].+?[\'"] label=[\'"]([^\'"]+)[\'"]>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                Files = []
                for aEntry in aResult[1]:
                    url = aEntry[0]
                    label = aEntry[1]
                    url = url + '.srt'

                    if not url.startswith('http'):
                        url = 'http:' + url
                    if 'Forc' not in label:
                        Files.append(url)
                return Files

        return False



    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if (self.oPremiumHandler.isPremiumModeAvailable()):
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
        self._url = self._url.replace('uptobox.com/', 'uptostream.com/')

        # On redirige vers le hoster uptostream
        oHoster = uptostreamHoster()
        oHoster.setUrl(self._url)
        return oHoster.getMediaLink()

    def _getMediaLinkByPremiumUser(self):
        if not self.oPremiumHandler.Authentificate():
            return self._getMediaLinkForGuest()

        else:
            sHtmlContent = self.oPremiumHandler.GetHtml(self._url)
            # compte gratuit ou erreur auth
            if 'you can wait' in sHtmlContent or 'time-remaining' in sHtmlContent:
                VSlog('no premium')
                return self._getMediaLinkForGuest()
            else:
                SubTitle = self.checkSubtitle(sHtmlContent)
                api_call = self.getMedialinkDL(sHtmlContent)
                if api_call:
                    if SubTitle:
                        return True, api_call, SubTitle
                    else:
                        return True, api_call

                return False, False

    def getMedialinkDL(self, sHtmlContent):
        oParser = cParser()

        sPattern = '<a href *=[\'"](?!http:\/\/uptostream.+)([^<>]+?)[\'"] *class=\'big-button-green-flat mt-4 mb-4\''
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            return QuoteSafe(aResult[1][0])

        return False
