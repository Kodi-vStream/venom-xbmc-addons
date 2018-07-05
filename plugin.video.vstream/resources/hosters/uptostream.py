#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog #,VSlog

import urllib,re


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Uptostream'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

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
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
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
            aResult = aResult[1][0].replace('.','%2E')
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
        if re.search('<div class=[\'"]theater-background[\'"]></div>\s*<h1>[^<>]+(?:MULTI|VOSTFR)[^<>]*</h1>',sHtmlContent,re.IGNORECASE):
        
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
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        SubTitle = ''
        SubTitle = self.checkSubtitle(sHtmlContent)
        #VSlog(SubTitle)
        
        oParser = cParser()
        sPattern =  'src":[\'"]([^<>\'"]+)[\'"],"type":[\'"][^\'"><]+?[\'"],"label":[\'"]([0-9]+p)[\'"].+?"lang":[\'"]([^\'"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #VSlog(str(aResult))
        
        if (aResult[0] == True):
            url=[]
            qua=[]
            lang=[]
 
            for aEntry in aResult[1]:
                url.append(aEntry[0])
                tmp_qua = aEntry[1]
                
                if (len(aEntry)>2):
                    if 'unknow' not in aEntry[2]:
                        tmp_qua = tmp_qua + ' (' + aEntry[2] + ')'
                qua.append(tmp_qua)

            api_call = dialog().VSselectqual(qua, url)         

            if (api_call):

                api_call = urllib.unquote(api_call)
            
                if not api_call.startswith('http'):
                    api_call = 'http:' + api_call

                if SubTitle:
                    return True, api_call, SubTitle
                else:
                    return True, api_call
        
        return False, False
