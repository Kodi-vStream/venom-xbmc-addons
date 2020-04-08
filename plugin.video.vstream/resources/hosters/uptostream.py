#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
#from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

from resources.lib.jsparser import JsParser

import json
import urllib, re, base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'UpToStream'
        self.__sFileName = self.__sDisplayName

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
        return self.__sUrl.split('/')[-1]

    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl

    def __getKey(self):
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'flashvars.filekey="(.+?)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.', '%2E')
            return aResult

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://uptostream.com/', '')
        self.__sUrl = self.__sUrl.replace('https://uptostream.com/', '')
        self.__sUrl = self.__sUrl.replace('iframe/', '')
        self.__sUrl = 'https://uptostream.com/' + str(self.__sUrl)

    def checkSubtitle(self,sHtmlContent):
        oParser = cParser()

        #On ne charge les sous titres uniquement si vostfr se trouve dans le titre.
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
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False
        
        self.__sUrl = 'https://uptostream.com/api/streaming/source/get?token=null&file_code=' + self.__getIdFromUrl()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', 'w')
        #fh.write(sHtmlContent)
        #fh.close()
        

        SubTitle = ''
        #Disabled for the moment
        #SubTitle = self.checkSubtitle(sHtmlContent)
        #VSlog(SubTitle)
        
        page = json.loads(sHtmlContent)
        JScode = page['data']['sources']
        JScode = JScode.encode('utf-8')
        
        #fh = open('c:\\test.txt', 'w')
        #fh.write(JScode1)
        #fh.close()
        
        VSlog(JScode)

        JP = JsParser()
        Liste_var = []
        dialog().VSinfo('Décodage: Peut durer plus d\'une minute.', "Attention", 15)
       
        sHtmlContent = JP.ProcessJS(JScode,Liste_var)
        res = JP.GetVar(Liste_var,'sources')[0]['src']
       
        VSlog(res)
        
        api_call = res
            
        if (api_call):

            #api_call = urllib.unquote(api_call)

            if not api_call.startswith('http'):
                api_call = 'http:' + api_call

            if SubTitle:
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
