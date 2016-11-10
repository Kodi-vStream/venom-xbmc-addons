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

class JsParser(object):
    def __init__(self):
        self.Var = []
        
    
    def GetBeetweenParenth(self,str):
        #Search the first (
        s = str.find('(')
        if s == -1:
            return ''
            
        n = 1
        e = s + 1
        while (n > 0) and (e < len(str)):
            c = str[e]
            if c == '(':
                n = n + 1
            if c == ')':
                n = n - 1
            e = e + 1
            
        s = s + 1
        e = e - 1
        return str[s:e]

    def SafeEval(self,str):
        f = re.search('[^0-9+-.\(\)]',str)
        if f:
            xbmc.log('Wrong parameter to Eval : ' + str)
            return 0
        return eval(str)
        
    def evalJS(self,JScode,tmp):
        #https://nemisj.com/python-api-javascript/
        
        JScode = JScode.replace(' ','')
        
        #Simple replacement
        JScode = JScode.replace('String.fromCharCode', 'chr')
        JScode = JScode.replace('.charCodeAt(0)', '')
        JScode = JScode.replace('tmp.length', str(len(tmp)))
        
        #xbmc.log('avant ' + JScode)
            
        #Eval Number
        modif = True
        while (modif):
            modif = False
            #Remplacement en virant parenthses
            r = re.search('[^a-z](\([0-9+-]+\))',JScode)
            if r:
                JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
                modif = True
            #remplacement en laissant parenthses
            r = re.search('[\(\),]([0-9+-]+[+-][0-9]+)[\(\),]',JScode)
            if r:
                JScode = JScode.replace(r.group(1),str(self.SafeEval(r.group(1))))
                modif = True
            #slice
            r = re.search('tmp\.slice\((-*[0-9]+)(?:,(-*[0-9]+))*\)',JScode)
            if r:
                if r.group(2):
                    JScode = JScode.replace(r.group(0), str(ord(tmp[int(r.group(1)):int(r.group(2))][0])) )
                else:
                    JScode = JScode.replace(r.group(0),str(ord(tmp[int(r.group(1)):][0])) )
                modif = True
         

        #Eval string
        modif = True
        while (modif):
            modif = False
            #Substring
            r = re.search('tmp\.substring\((-*[0-9]+)(?:,(-*[0-9]+))*\)',JScode)
            if r:
                if r.group(2):
                    JScode = JScode.replace(r.group(0),tmp[ int(r.group(1)) : int(r.group(2)) ] )
                else:
                    JScode = JScode.replace(r.group(0),tmp[ int(r.group(1)) :] )
                modif = True
            #chr
            r = re.search('chr\(([0-9]+)\)',JScode)
            if r:
                JScode = JScode.replace(r.group(0),chr(int(r.group(1))) )
                modif = True
            #join
            r = re.search('tmp\.join\((.+)\)',JScode)
            if r:
                JScode = JScode.replace(r.group(0),r.group(1).join(tmp) )
                modif = True            
        
        #On colle le tout
        JScode = JScode.replace ('+','')
        
        #xbmc.log('apres ' + JScode)
        
        return JScode
            
    def UpdateVar(self,var,value):
        for j in self.Var:
            if j[0] == var:
                self.Var[self.Var.index(j)] = (var,value)
                return
        self.Var.append((var,value))
            
    def ReplaceVar(self,JScode):
        modif = True
        while (modif):
            modif = False
            for j in self.Var:
                if j[0] in JScode:
                    JScode = JScode.replace(j[0],'(' + j[1]+ ')')
                    modif = True
                    
        return JScode

    def ProcessJS(self,JScode,tmp):
        #Need to use in future ast.literal_eval(), need python 3
        
        #Get variable and function fixed
        function = re.compile('function ([\w_]+\(\)) *{\s*return ([^;]+)').findall(JScode)
        if function:
            for i,j in function:
                self.UpdateVar(i,j)
 
        #xbmc.log(str(self.Var))
  
        #Extract principal chain
        f = re.search('var str = (.+?);',JScode)
        if not f:
            return ''
        JScode = f.group(1)
        
        #Update code with replace fixed fonctions
        JScode = self.ReplaceVar(JScode)
        
        #eval code
        JScode = self.evalJS(JScode,tmp)
        
        return JScode
        
        
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
        
        #on essais de situer le code
        sPattern = '<script src="\/assets\/js\/video-js\/video\.js\.ol\.js">(.+)*'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if (aResult[0]):
            sHtmlContent2 = aResult[1][0]
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        code = ''
        
        #liste tout les decoders
        maxboucle = 1
        sHtmlContent3 = sHtmlContent2
        
        while (('#streamurl' not in sHtmlContent3) and (maxboucle > 0)):
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            #xbmc.log(sHtmlContent3)
            sHtmlContent3 = CheckJJDecoder(sHtmlContent3)
            #xbmc.log(sHtmlContent3)            
            sHtmlContent3 = CheckAADecoder(sHtmlContent3)
            #xbmc.log(sHtmlContent3)
            
            maxboucle = maxboucle - 1
            
        code = sHtmlContent3   
        #xbmc.log(code)
        
        if not (code):
            return False,False
        
        #Remarques persos pour plus tard.
        #------------------------
        #La bonne url est tjours la plus courte
        #Mauvaise finie par x
        
        #Search the coded url
        hideenurl = ''
        Hiddenvar = 'y'
        
        sPattern = 'var j=([a-z])\.charCodeAt'
        aResult = oParser.parse(code, sPattern)
        if (aResult[0]):
            Hiddenvar = re.search('var j=([a-z])\.charCodeAt', code).group(1)
            
        sPattern = 'var ' + Hiddenvar + ' = \$\("#([^"]+)"\)'
        aResult = oParser.parse(code, sPattern)
        if (aResult[0]):
            for i in TabUrl:
                if aResult[1][0] == i[0]:
                    hideenurl = i[1]
                    xbmc.log('hidden url : ' + str(i))

        if not(hideenurl):
            xbmc.log('Url codee non trouvee')
            return False, False
        
        string = cUtil().unescape(hideenurl)
        
        url = ''

        for c in string:
            v = ord(c)              
            
            if v >= 33 and v <= 126:
                v = ((v + 14) % 94) + 33
            url = url + chr(v)

        #Partie gerant le decalage
        #xbmc.log('avant :' + url)
        url = JsParser().ProcessJS(code,url)
        #xbmc.log('apres :' + url)
        
        if not (url):
            return False,False
        
        #Now on teste les urls
        api_call = "https://openload.co/stream/" + url + "?mime=true"        
        xbmc.log('1 er url : ' + api_call)
        api_call = GetOpenloadUrl(api_call,self.__sUrl)
        
        if (False):
            #Si ca marche pas on teste d'autres trucs au hazard
            if not (api_call):
                url0 = url[:-1] + chr(ord(url[-1]) - val)
                for i in range(1,3):
                    if i != val:
                        url2 = url0[:-1] + chr(ord(url0[-1]) + i)
                        url2 = "https://openload.co/stream/" + url2 + "?mime=true" 
                        #xbmc.log(url2)
                        url3 = GetOpenloadUrl(url2,self.__sUrl)
                        xbmc.sleep(2000)
                        if (url3):
                            api_call = url3
        
        xbmc.log('Url validee : ' + api_call)
        
        if (api_call):          
            return True, api_call
            
        return False, False
 
