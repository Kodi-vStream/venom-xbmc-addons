# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# ==>vikki
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
# from resources.lib.comaddon import VSlog
import xbmcgui


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Viki'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'viki'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self, api_call=None):

        sUrl = self.__sUrl
        # srtsubs_path = xbmc.translatePath('special://temp/vikir.English.srt')
        # Methode 1 on recoit une liste sUrl=[ urlstream,sub,q1,q2...urlq1,urlq2
        # if false sub=french
        bSelectSub=True

        # https://manifest-viki.viki.io/v1/1159945v/limelight/domain_4/mpd/normal/viki/high/mpd_mob/ww/na/manifest.mpd?
        bsupportedMdp = False  # manifest.mpd

        url = []
        qual = []
        pathsub = []
        namesub = ['French', 'English']

        oParser = cParser()
        sPattern = ".'([^']*)"
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            sub1 = aResult[1][0]
            sub2 = aResult[1][1]
            pathsub.append(sub1)
            pathsub.append(sub2)

            offset = 2
            numberQ = (len(aResult[1])-offset)/2
            for i in range(offset, offset + numberQ):
                if 'mpd' in aResult[1][i]:
                    if bsupportedMdp:
                        qual.append(aResult[1][i] + ' !')
                    continue

                qual.append(aResult[1][i])
            for i in range(offset + numberQ, len(aResult[1])):
                if 'manifest.mpd' in aResult[1][i]:
                    if bsupportedMdp:
                        url.append(aResult[1][i])
                    continue
                url.append(aResult[1][i])

            sub = sub1
            if bSelectSub:
                pathsub.append('')
                namesub.append('None')
                sub = self.mydialog().VSselect(namesub, pathsub, 'Viki Select subtile :')

            api_call = self.mydialog().VSselect(qual, url, 'Viki Select quality :')
            # api_call = self.VSselectsub(qual, url)

            if api_call:
                if sub:
                    return True,api_call, sub
                else:
                    return True, api_call

            else:  # user canceled !# file not found
                return False, False

        # Methode 2 on recoit une chaine sUrl=urlstream + ';' urlsub
        if ';' in sUrl:
            sUrl, sub = sUrl.split(';')
            api_call = sUrl
            if api_call:
                return True, api_call, sub
        else:

            # VSlog('hoster vikki no find sub : use ";" to split url and sub')
            api_call = sUrl
            if api_call:
                return True, api_call

        # api_call = "https://cloudfront.viki.net/1133753v/dash/1133753v_dash_high_480p_2d3e72_1809180448_track1_dashinit.mp4"

        # jamais atteint
        return False, False

    class mydialog(xbmcgui.Dialog):
        def VSselect(self, list_alias, list_toreturn, sTitle):

            if len(list_toreturn) == 0:
                return ''
            if len(list_toreturn) == 1:
                return list_toreturn[0]

            ret = self.select(sTitle, list_alias)
            if ret > -1:
                return list_toreturn[ret]
            return ''
