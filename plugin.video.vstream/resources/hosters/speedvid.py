from resources.lib.handler.requestHandler import cRequestHandler,MPencode
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
# from resources.lib.util import VSlog
#from resources.lib.config import cConfig

#from resources.lib.jsparser import JsParser

import re,xbmcgui,urllib2,urllib

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Speedvid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'speedvid'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://speedvid.net/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
        headers = { 'User-Agent' : UA }
        
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')
        sHtmlContent = oRequest.request()

        oParser = cParser()
        
        #Recherche de la vraie page
        Url = ''
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\))<'
        aResult = re.findall(sPattern,sHtmlContent)
        if (aResult):
            for packed in aResult:
 
                # cConfig().log('>>' + packed)
                
                #Recherche du bon bloc
                if not 'mp4' in packed and not 'FRAMEBORDER' in packed:

                    fields = {'urlin':packed,'private':'on','referer':'http://www.ask.com/web?q=triplepack'}
                    mpartdata = MPencode(fields)

                    req = urllib2.Request('http://jsunpack.jeek.org/?',mpartdata[1],headers)
                    req.add_header('Content-Type', mpartdata[0].replace(',',';'))
                    req.add_header('Content-Length', len(mpartdata[1]))
                    req.add_header('Connection','keep-alive')
                    try:
                        rep = urllib2.urlopen(req)
                    except:
                        return ''

                    sHtml = rep.read()
                    rep.close()
                    break

            code = re.search('location.href="(.+?)"',sHtml,re.DOTALL)
            if code:
                Url = 'http://www.speedvid.net/' + code.group(1)

            
            oRequest = cRequestHandler(Url)
            oRequest.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')
            oRequest.addHeaderEntry('Referer',self.__sUrl)
            sHtmlContent = oRequest.request()

            url=[]
            qua=[]
            api_call = ''
        
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\))<'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                for packed in aResult[1]:
                    sHtmlContent = cPacker().unpack(packed)
                    sHtmlContent = sHtmlContent.replace('\\','')
                    if "jwplayer('vplayer').setup" in sHtmlContent:
                        sPattern2 = "{file:.([^']+.mp4)"
                        aResult2 = oParser.parse(sHtmlContent, sPattern2)
                        if (aResult2[0] == True):
                            api_call = aResult2[1][0]
                            break
                            
                    # # url.append(aResult2[1][0])
                    # # if 'HD' in aResult2[1][0]:
                        # # qua.append('HD')
                    # # else:
                        # # qua.append('SD')
                    
        # Si une seule url
        # # if len(url) == 1:
            # # api_call = url[0]
        # si plus de une
        # # elif len(url) > 1:
        # Afichage du tableau
            # # dialog2 = xbmcgui.Dialog()
            # # ret = dialog2.select('Select Quality', qua)
            # # if (ret > -1):
                # # api_call = url[ret]

        if (api_call):
            api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
            return True, api_call
            
        return False, False
