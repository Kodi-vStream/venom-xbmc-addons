# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
import base64
import re

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, addon
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser
from resources.lib.util import QuoteSafe, Unquote

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Uptobox'
        self.__sFileName = self.__sDisplayName
        self.oPremiumHandler = None
        self.stream = True

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

    def checkSubtitle(self, sHtmlContent):
        oParser = cParser()

        # On ne charge les sous titres uniquement si vostfr se trouve dans le titre.
        if not re.search("<h1 class='file-title'>[^<>]+(?:TRUEFRENCH|FRENCH)[^<>]*</h1>", sHtmlContent, re.IGNORECASE):

            sPattern = '<track type=[\'"].+?[\'"] kind=[\'"]subtitles[\'"] src=[\'"]([^\'"]+).vtt[\'"] srclang=[\'"].+?[\'"] label=[\'"]([^\'"]+)[\'"]>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
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

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        ADDON = addon()
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if (self.oPremiumHandler.isPremiumModeAvailable()):

            try:
                mDefault = int(ADDON.getSetting("hoster_uptobox_mode_default"))
            except AttributeError:
                mDefault = 0

            if mDefault is 0:
                ret = dialog().select('Choissisez votre mode de fonctionnement', ['Passer en Streaming (via Uptostream)', 'Rester en direct (via Uptobox)'])
            else:
                # 0 is ask me, so 1 is uptostream and so on...
                ret = mDefault - 1

            # mode DL
            if ret == 1:
                self.stream = False
            # mode stream
            elif ret == 0:
                self.__sUrl = self.__sUrl.replace('uptobox.com/', 'uptostream.com/')
            else:
                return False

            return self.__getMediaLinkByPremiumUser()

        else:
            VSlog('no premium')
            return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        self.stream = True
        self.__sUrl = self.__sUrl.replace('uptobox.com/', 'uptostream.com/')

        # On redirige vers le hoster uptostream
        from resources.hosters.uptostream import cHoster
        oHoster = cHoster()
        oHoster.setUrl(self.__sUrl)
        return oHoster.__getMediaLinkForGuest()

    def __getMediaLinkByPremiumUser(self):

        if not self.oPremiumHandler.Authentificate():
            return self.__getMediaLinkForGuest()

        else:
            sHtmlContent = self.oPremiumHandler.GetHtml(self.__sUrl)
            # compte gratuit ou erreur auth
            if 'you can wait' in sHtmlContent or 'time-remaining' in sHtmlContent:
                VSlog('no premium')
                return self.__getMediaLinkForGuest()
            else:
                SubTitle = ''
                SubTitle = self.checkSubtitle(sHtmlContent)

                if (self.stream):
                    api_call = self.GetMedialinkStreaming(sHtmlContent)
                else:
                    api_call = self.GetMedialinkDL(sHtmlContent)

                if api_call:
                    if SubTitle:
                        return True, api_call, SubTitle
                    else:
                        return True, api_call

                return False, False

    def GetMedialinkDL(self, sHtmlContent):

        oParser = cParser()

        sPattern = '<a href *=[\'"](?!http:\/\/uptostream.+)([^<>]+?)[\'"] *class=\'big-button-green-flat mt-4 mb-4\''
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            return QuoteSafe(aResult[1][0])

        return False

    def GetMedialinkStreaming(self, sHtmlContent):

        oParser = cParser()

        # Parfois codée
        sPattern =  "window\.sources = JSON\.parse\(atob\('([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = base64.b64decode(aResult[1][0])

        sPattern =  'src":[\'"]([^<>\'"]+)[\'"],"type":[\'"][^\'"><]+?[\'"],"label":[\'"]([0-9]+p)[\'"].+?"lang":[\'"]([^\'"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        stream_url = ''

        if (aResult[0] == True):
            url=[]
            qua=[]

            for aEntry in aResult[1]:
                url.append(aEntry[0])
                tmp_qua = aEntry[1]
                if (aEntry[2]):
                    if 'unknow' not in aEntry[2]:
                        tmp_qua = tmp_qua + ' (' + aEntry[2] + ')'
                qua.append(tmp_qua)

            # Si une seule url
            if len(url) == 1:
                stream_url = url[0]
            # si plus de une
            elif len(url) > 1:
            # tableau qualitée
                select = dialog().VSselectqual(qua, url)
                if (select):
                    stream_url = select
                else:
                    return False
            else:
                return False

            stream_url = Unquote(stream_url)
            if not stream_url.startswith('http'):
                stream_url = 'http:' + stream_url

            return stream_url
        else:
            return False

        return False
