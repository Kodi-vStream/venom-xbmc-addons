#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.jjdecode import JJDecoder
from resources.hosters.hoster import iHoster
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil

from resources.lib.aadecode import AADecoder
from resources.lib.jjdecode import JJDecoder
from resources.lib.packer import cPacker

import re,urllib2, base64, math

import xbmc

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

def parseInt(sin):
    return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

def CheckCpacker(str):
    oParser = cParser()
    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = oParser.parse(str, sPattern)
    if (aResult[0]):
        xbmc.log('Cpacker encryption')
        str2 = aResult[1][0]
        if not str2.endswith(';'):
            str2 = str2 + ';'
            
        return cPacker().unpack(str2)

    return str
    
def CheckJJDecoder(str):
    oParser = cParser()
    sPattern = '([a-z]=.+?\(\)\)\(\);)'
    aResult = oParser.parse(str, sPattern)
    if (aResult[0]):
        xbmc.log('JJ encryption')
        return JJDecoder(aResult[1][0]).decode()
        
    return str
    
def CheckAADecoder(str):
    oParser = cParser()
    sPattern = '(ﾟωﾟ.+?)<\/script>'
    aResult = oParser.parse(str, sPattern)
    if (aResult[0]):
        xbmc.log('AA encryption')
        return AADecoder(aResult[1][0]).decode()
        
    return str
    
def GetOpenloadUrl(url):
    if 'openload.co/stream' in url:
    
        headers = {'User-Agent': UA }
                  
        req = urllib2.Request(url,None,headers)
        res = urllib2.urlopen(req)
        finalurl = res.geturl()
        
        #autres infos
        #xbmc.log(res.info())
        #xbmc.log(res.info()['Content-Length'])
        
        if 'KDA_8nZ2av4/x.mp4' in finalurl:
            xbmc.log('pigeon url : ' + url)
            finalurl = ''
            
        #xbmc.log(finalurl)
        return finalurl
    return url
        
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Openload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'#[COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'openload'

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
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('openload.io','openload.co')
        #self.__sUrl = self.__sUrl.replace('/embed/', '/f/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
   
        oParser = cParser()        
        
        #recuperation de la page
        xbmc.log('url teste : ' + self.__sUrl)
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent = oRequest.request()
        
        #Recuperation url cachee
        TabUrl = []
        sPattern = '<span id="([^"]+)">([^<>]+)<\/span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            TabUrl = aResult[1]
        else:
            return False, False
        
        #on essais de situer le code
        sPattern = '<script src="\/assets\/js\/video-js\/video\.js\.ol\.js">(.+)*'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sHtmlContent = aResult[1][0]
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        code = ''
        
        #liste tout les decoders
        sHtmlContent = CheckCpacker(sHtmlContent)
        #xbmc.log(sHtmlContent)
        sHtmlContent = CheckJJDecoder(sHtmlContent)
        #xbmc.log(sHtmlContent)
        
        code = sHtmlContent
        #xbmc.log(code)
        
        if not (code):
            return False,False
            
        #Search the coded url
        hideenurl = ''
        sPattern = '\$\("#([^"]+)"\)'
        aResult = oParser.parse(code, sPattern)
        if (aResult[0]):
            for i in TabUrl:
                if aResult[1][0] == i[0]:
                    hideenurl = i[1]
                    #xbmc.log(str(i))

        if not(hideenurl):
            xbmc.log('Url codee non trouvee')
            return False, False
        
        #Calcul du decalage
        sPattern = '\(tmp\.slice\(-1\)\.charCodeAt\(0\) \+ ([0-9]+)\)'
        aResult = oParser.parse(code, sPattern)
        
        val = 3
        if (aResult[0]):
            val = int(aResult[1][0])
            
        xbmc.log('Decalage : ' + str(val))
        
        string = cUtil().unescape(hideenurl)
        
        url = ''
        
        for c in string:
            v = ord(c)
            if v >= 33 and v <= 126:
                v = ((v + 14) % 94) + 33
            url = url + chr(v)
        
        url = url[:-1] + chr(ord(url[-1]) + val)
        
        api_call = "https://openload.co/stream/" + url + "?mime=true"        
        xbmc.log('1 er url : ' + api_call)
        api_call = GetOpenloadUrl(api_call)
        
        #Si ca marche pas on teste d'autres trucs au hazard
        if not (api_call):
            url0 = url[:-1] + chr(ord(url[-1]) - val)
            for i in range(0,5):
                if i != val:
                    url2 = url0[:-1] + chr(ord(url0[-1]) + i)
                    url2 = "https://openload.co/stream/" + url2 + "?mime=true" 
                    #xbmc.log(url2)
                    url3 = GetOpenloadUrl(url2)
                    if (url3):
                        api_call = url3
        
        if (api_call):          
            return True, api_call
            
        return False, False
 
