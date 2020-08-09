#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
# import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Lien direct'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'lien_direct'

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
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl).replace('+', '%20') # un lien direct n'est pas forcement urlEncoded

    def gethost(self, sUrl):
        sPattern = 'https*:\/\/(.+?)\/.+?'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = self.__sUrl

        if ('hds.' in api_call) or ('bidzen' in api_call):
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'
            api_call = api_call + '|User-Agent=' + UA + '&referer=' + self.__sUrl

        #full moviz lien direct final nowvideo
        if 'zerocdn.to' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
            api_call = api_call + '|User-Agent=' + UA

        #Special pour mangacity
        if 'pixsil' in api_call:
            api_call = api_call.split('|')[0] + '|Referer=http://www.mangacity.org/jwplayer/player.swf'

        #Modif pr aliez
        if 'aplayer1.me' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
            api_call = api_call + '|User-Agent=' + UA

        if 'sport7' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
            api_call = api_call + '|User-Agent=' + UA + '&referer=' + self.__sUrl

        #Special pour hd-stream.in et film-streaming.co
        if 'playlist.m3u8' in api_call:
            # base = re.sub(r'(playlist.m3u8*.+)', '', api_call)
            oRequest = cRequestHandler(api_call)
            sHtmlContent = oRequest.request()
            sPattern =  ',NAME="([^"]+)".+?(chunklist.+?.m3u8)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                #initialisation des tableaux
                url=[]
                qua=[]
                api_call = ''
                #Remplissage des tableaux
                for i in aResult[1]:
                    url.append(str(i[1]))
                    qua.append(str(i[0]))

                #Affichage du tableau
                api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
