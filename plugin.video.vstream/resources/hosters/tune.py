#-*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import cUtil,VScreateDialogSelect
import json

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Tune'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'tune'
        
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
        sPattern = 'vid=([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        oParser = cParser()

        id = self.__getIdFromUrl(self.__sUrl)
        
        sUrl = 'https://embed.tune.pk/play/' + id  + '?autoplay=no&ssl=yes&inline=true'

        oRequest = cRequestHandler(sUrl)
        sHtmlContent1 = oRequest.request()

        sPattern = "var requestURL *= *'([^']+)';.+?\"X-secret-Header\":\"(.+?)\"}"
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if (aResult[0] == True):
            vUrl = aResult[1][0][0]
            Secret = aResult[1][0][1]
            oRequest = cRequestHandler(vUrl)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('X-secret-Header', Secret)
            sHtmlContent = oRequest.request()

            sHtmlContent = cUtil().removeHtmlTags(sHtmlContent)
            sHtmlContent = cUtil().unescape(sHtmlContent)

            content = json.loads(sHtmlContent)
            content = content["data"]["details"]["player"]
            if content:
                url = []
                qua = []
                for x in content['sources']:
                    url.append(x['file'])
                    qua.append(repr(x['label']))

                if len(url) == 1:
                    api_call = url[0]

                elif len(url) > 1:
                    ret = VScreateDialogSelect(qua)
                    if (ret > -1):
                        api_call = url[ret]
            else:
                sPattern = '<meta itemprop="contentURL" content="([^"]+)"'
                aResult = oParser.parse(sHtmlContent1, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]
                    
            if (api_call):
                return True, api_call + '|User-Agent=' + UA 

            return False, False
