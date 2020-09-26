# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# type
# https://www.youtube.com/embed/etc....
# https://www.youtube.com/watch?v=etc...
# http://www.youtube-nocookie.com/v/etc...
# https://youtu.be/etc...

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.lib.util import Unquote, Quote

URL_MAIN = 'https://www.youtube.com/get_video_info?video_id='


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Youtube'
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
        return 'youtube'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl
        self.__sUrl = self.__sUrl.rsplit('/', 1)[1]
        self.__sUrl = self.__sUrl.replace('watch?v=', '')
        self.__sUrl = self.__sUrl.replace('?rel=0', '')
        self.__sUrl = self.__sUrl.replace('&cc_load_policy=1', '')
        self.__sUrl = self.__sUrl.replace('?', '').replace('&', '')
        self.__sUrl = self.__sUrl.replace('feature=oembed', '')
        self.__sUrl = self.__sUrl.replace('autoplay=1', '')
        self.__sUrl = self.__sUrl.replace('autohide=1', '')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, sUrl):
        return

    def getMediaLink(self):
        first_test = self.__getMediaLinkForGuest()

        if first_test != False:
            return first_test
        else:
            return self.__getMediaLinkForGuest2()

    def __getMediaLinkForGuest(self):
        api_call = ''

        oParser = cParser()
        oRequestHandler = cRequestHandler(URL_MAIN + self.__sUrl)
        sHtml = Unquote(oRequestHandler.request())
        sHtmlContent = sHtml[7 + sHtml.find('formats'):sHtml.rfind('adaptiveFormats')]
        sPattern = '"url":"([^"]+)".+?"qualityLabel":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            url = []
            qua = [] 
            for aEntry in aResult[1]:
                #Py3 a besoin de la deuxieme version, je laisse le 1er replace au cas où pour Py2
                url.append(aEntry[0].replace("\u0026","&").replace("\\u0026","&"))
                qua.append(aEntry[1])

            if url:
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call
        else:
            return False

    def __getMediaLinkForGuest2(self):
        api_call = ''

        oParser = cParser()
        pdata = 'url=' + Quote('https://www.youtube.com/embed/' + self.__sUrl) + '&submit=1'

        oRequest = cRequestHandler('https://ytoffline.net/fr/validate/')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
        oRequest.addHeaderEntry('Referer', 'https://ytoffline.net/fr/download/?url=https://www.youtube.com/embed/' + self.__sUrl)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()
        sHtmlContent1 = oParser.abParse(sHtmlContent, '<div id="mp4" class="display-block tabcontent">', '<div id="audio" class="tabcontent">')
        sPattern = '<td>([^<]+)<small>.+?data-href="([^"]+)"'
        aResult = oParser.parse(sHtmlContent1, sPattern)

        if (aResult[0] == True):
            # initialisation des tableaux
            url = []
            qua = []
            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
