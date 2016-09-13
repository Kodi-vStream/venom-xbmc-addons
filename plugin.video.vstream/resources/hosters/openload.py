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

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        
        api_call = ''
        
        oParser = cParser()        
        
        #recuperation de la page
        xbmc.log('url teste : ' + self.__sUrl)
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent = oRequest.request()
        
        #Recuperation url cachee
        hideenurl = ''
        sPattern = '<span id="hiddenurl">(.+?)<\/span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            hideenurl = aResult[1][0]
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
        sHtmlContent = CheckJJDecoder(sHtmlContent)
        
        code = sHtmlContent
        #xbmc.log(code)
        
        if not (code):
            return False,False
            
        sPattern = '\(tmp\.slice\(-1\)\.charCodeAt\(0\) \+ ([0-9]+)\)'
        aResult = oParser.parse(code, sPattern)
        
        #xbmc.log(str(aResult))
        
        val = 3
        if (aResult[0]):
            val = int(aResult[1][0])
        
        string = cUtil().unescape(hideenurl)
        
        url = ''
        
        for c in string:
            v = ord(c)
            if v >= 33 and v <= 126:
                v = ((v + 14) % 94) + 33
            url = url + chr(v)
        
        url = url[:-1] + chr(ord(url[-1]) + val)
        
        api_call = "https://openload.co/stream/" + url + "?mime=true"
        
        xbmc.log(api_call)
        
        if (api_call):
            
            if 'openload.co/stream' in api_call:
                
                headers = {'User-Agent': UA }
                          
                req = urllib2.Request(api_call,None,headers)
                res = urllib2.urlopen(req)
                finalurl = res.geturl()
                #xbmc.log(finalurl)
                api_call = finalurl

            return True, api_call
            
        return False, False
 
