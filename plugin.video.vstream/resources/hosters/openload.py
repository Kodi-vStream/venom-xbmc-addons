#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.jjdecode import JJDecoder
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.aadecode import AADecoder
import re,urllib2

import xbmc

#Merci a cmos pour son code
#Convert from decimal to any base number
#http://code.activestate.com/recipes/65212-convert-from-decimal-to-any-base-number/
def base10toN(num, n):
    """Change a  to a base-n number.
    Up to base-36 is supported without special notation."""
    
    new_num_string = ''
    current = num

    while current != 0:
        remainder = current % n
        if 36 > remainder > 9:
            remainder_string = chr(remainder + 87)
        elif remainder >= 36:
            remainder_string = '(' + str(remainder) + ')'
        else:
            remainder_string = str(remainder)
        new_num_string = remainder_string + new_num_string
        current = current / n
    return new_num_string


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
        #self.__sUrl = self.__sUrl.replace('/embed/', '/f/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        #Debut des tests de decodage
        oParser = cParser()
        string = ''
       
        #"aaencode - Encode any JavaScript program to Japanese style emoticons (^_^)"
        sPattern = '<script type="text\/javascript">(ﾟωﾟ.+?)<\/script>'
        #sPattern = "<video(?:.|\s)*?<script\s[^>]*?>.+?<\/script>\s<script\s[^>]*?>((?:.|\s)*?)<\/"
        
        aResult = oParser.parse(sHtmlContent, sPattern)
        #xbmc.log(str(aResult))
        
        #ok on a maintenant 4 liens
        vid = 'XXXXXX'
        string2 = []
        for aEntry in aResult[1]:
            s = AADecoder(aEntry).decode()
            #xbmc.log(s)
            string2.append(s)
            
            if 'welikekodi_ya_rly' in s:
                c0 = re.search('welikekodi_ya_rly = ([^<>;"]+);', s)
                if c0:
                    c = c0.group(1)
                    c = c.replace('Math.round','int')
                    #xbmc.log('calcul : ' + c )
                    cc = str(eval(c))
                    vid = '[' + cc + ']'
                    #xbmc.log('resultat : ' + vid )
        
        for string3 in string2:
            if ('toString' in string3) and (vid in string3):
                
                #xbmc.log(string3)
                
                base = int(re.findall('toString\(a\+([0-9]+)\)',string3)[0])
                table = re.findall('(\([0-9][^)]+\))',string3)
                
                for str1 in table:
                    val = re.findall('([0-9]+),([0-9]+)',str1)
                    base2 = base + int(val[0][0])
                    str2 = base10toN(int(val[0][1]), base2)
                    string3 = string3.replace(str1, str2)
                
                #xbmc.log(string3)
                
                #nettoyage
                string3 = string3.replace('+', '')
                string3 = string3.replace('"', '')
                string3 = string3.replace('', '')

                #bidouille pour pas avoir a tout recoder
                q = re.findall('(http[^<>}]+)',string3)
                if not q:
                    q = re.findall('return (\/\/[^<>}]+)',string3)
                    url = 'http:' + q[0]
                else:
                    url = q[0]
                string = 'src="' + url + '?mime=true"'
 
        if not (string): 
            #Dean Edwards Packer
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sUnpacked = cPacker().unpack(aResult[1][0])
                string = JJDecoder(sUnpacked).decode()

        if (string):
            sContent = string.replace('\\','')
            
            api_call = ''

            sPattern = 'src=\s*?"(.*?)\?'
            aResult = oParser.parse(sContent, sPattern)
            
            #print aResult
            
            if (aResult[0] == True):
                api_call = aResult[1][0]
                
            if not api_call:
                sPattern = 'window\.vr *=["\'](.+?)["\']'
                aResult = oParser.parse(sContent, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]

        if (api_call):
            
            if 'openload.co/stream' in api_call:
                UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
                headers = {'User-Agent': UA }
                          
                req = urllib2.Request(api_call,None,headers)
                res = urllib2.urlopen(req)
                finalurl = res.geturl()
                #xbmc.log(finalurl)
                api_call = finalurl

            return True, api_call
            
        return False, False
        
