#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
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

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'

def parseInt(sin):
    return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

def CheckCpacker(str):
    oParser = cParser()
    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = oParser.parse(str, sPattern)
    if (aResult[0]):
        str2 = aResult[1][0]
        if not str2.endswith(';'):
            str2 = str2 + ';'
        try:
            str = cPacker().unpack(str2)
            #xbmc.log('Cpacker encryption')
        except:
            pass

    return str
    
def CheckJJDecoder(str):
    oParser = cParser()
    sPattern = '([a-z]=.+?\(\)\)\(\);)'
    aResult = oParser.parse(str, sPattern)
    if (aResult[0]):
        #xbmc.log('JJ encryption')
        return JJDecoder(aResult[1][0]).decode()
        
    return str
    
def CheckAADecoder(str):
    sPattern = '[>;]\s*(ﾟωﾟ.+?\(\'_\'\);)'
    aResult = re.search(sPattern, str,re.DOTALL | re.UNICODE)
    if (aResult):
        #xbmc.log('AA encryption')
        tmp = AADecoder(aResult.group(1)).decode()
        #xbmc.log('>> ' + tmp)
        return str[:aResult.start()] + tmp + str[aResult.end():]
        
    return str

def GetOpenloadUrl(url,referer):
    if 'openload.co/stream' in url:
    
        headers = {'User-Agent': UA,
                   #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   #'Accept-Encoding':'gzip, deflate, br',
                   #'Host':'openload.co',
                   'Referer':referer
        }

        req = urllib2.Request(url,None,headers)
        res = urllib2.urlopen(req)
        #xbmc.log(res.read())
        finalurl = res.geturl()

        
        xbmc.log('Url decodee : ' + finalurl)
        
        #autres infos
        #xbmc.log(str(res.info()))
        #xbmc.log(res.info()['Content-Length'])
        
        if 'KDA_8nZ2av4/x.mp4' in finalurl:
            xbmc.log('pigeon url : ' + url)
            finalurl = ''
        if 'Content-Length' in res.info():
            if res.info()['Content-Length'] == '33410733':
                xbmc.log('pigeon url : ' + url)
                finalurl = ''
        if url == finalurl:
            xbmc.log('Bloquage')
            finalurl = ''        

        return finalurl
    return url
    
#Code updated with code from https://gitlab.com/iptvplayer-for-e2 
def decodek(k):
    y = ord(k[0]);
    e = y - 0x32
    d = max(2, e)
    e = min(d, len(k) - 0x14 - 2)
    t = k[e:e + 0x14]
    h = 0
    g = []
    while h < len(t):
        f = t[h:h+2]
        g.append(int(f, 0x10))
        h += 2
    v = k[0:e] + k[e+0x14:]
    p = []
    h = 0
    while h < len(v):
        B = v[h:h + 3]
        f = int(B, 0x10)
        if (h / 3) % 3 == 0:
            f = int(B, 8)
        A = g[(h / 3) % 0xa]
        f = f ^ 0x2F
        f = f ^ A;
        p.append(chr(f))
        h += 3
        
    return "".join(p)
    
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
        #xbmc.log('url teste : ' + self.__sUrl)
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent1 = oRequest.request()
        
        #Recuperation url cachee
        TabUrl = []
        sPattern = '<span id="([^"]+)">([^<>]+)<\/span>'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if (aResult[0]):
            TabUrl = aResult[1]
            #xbmc.log(str(TabUrl))
        else:
            return False, False
            
        #xbmc.log("Nbre d'url : " + str(len(TabUrl)))
        
        #on essais de situer le code
        sPattern = '<script src="\/assets\/js\/video-js\/video\.js\.ol\.js"(.+)*'
        
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if (aResult[0]):
            sHtmlContent3 = aResult[1][0]
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        #xbmc.log(sHtmlContent3)
        
        code = ''
        
        #liste tout les decoders
        maxboucle = 3
        
        while (('window.r' not in sHtmlContent3) and (maxboucle > 0)):
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            #xbmc.log(sHtmlContent3)
            sHtmlContent3 = CheckJJDecoder(sHtmlContent3)
            #xbmc.log(sHtmlContent3)            
            sHtmlContent3 = CheckAADecoder(sHtmlContent3)
            #xbmc.log(sHtmlContent3)
            
            maxboucle = maxboucle - 1
            
        code = sHtmlContent3   
        #xbmc.log('>>' + code)
        
        if not (code):
            return False,False
            
        aResult = oParser.parse(code, "window.r='([^']+)';")
        if (aResult[0]):
            ID = aResult[1][0]
            
        #xbmc.log('Id : ' +  ID)
            
        #Search the coded url
        for i in TabUrl:
            if len(i[1]) > 30:
                hideenurl = i[1]
                #xbmc.log('hidden url : ' + str(i))

        if not(hideenurl):
            #xbmc.log('Url codee non trouvee')
            return False, False
            
        #Code updated with code from https://gitlab.com/iptvplayer-for-e2    
        sCode = decodek(hideenurl)

        api_call = "https://openload.co/stream/" + sCode + "?mime=true"  
        #Now on teste les urls
        # api_call = "https://openload.co/stream/" + urlcode + "?mime=true"        
        #xbmc.log('1 er url : ' + api_call)
        #api_call = GetOpenloadUrl(api_call,self.__sUrl)
        
        # if (False):
            # # Si ca marche pas on teste d'autres trucs au hazard
            # if not (api_call):
                # url0 = url[:-1] + chr(ord(url[-1]) - val)
                # for i in range(1,3):
                    # if i != val:
                        # url2 = url0[:-1] + chr(ord(url0[-1]) + i)
                        # url2 = "https://openload.co/stream/" + url2 + "?mime=true" 
                        # # xbmc.log(url2)
                        # url3 = GetOpenloadUrl(url2,self.__sUrl)
                        # xbmc.sleep(2000)
                        # if (url3):
                            # api_call = url3
        
        # xbmc.log('Url validee : ' + api_call)
        
        if (api_call):          
            return True, api_call
            
        return False, False
