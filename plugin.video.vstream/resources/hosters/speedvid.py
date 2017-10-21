#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.packer import cPacker
from resources.lib.util import VSlog
from resources.lib.config import cConfig

#from resources.lib.jsparser import JsParser

import re,xbmcgui

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
    
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')
        sHtmlContent = oRequest.request()

        oParser = cParser()
        
        aResult = re.search('(ﾟωﾟ.+?\(\'_\'\);)', sHtmlContent,re.DOTALL | re.UNICODE)
        if (aResult):
            VSlog('AA encryption')
            sHtmlContent = AADecoder(aResult.group(1)).decode()

            #recuperation de l'url
            Url = re.findall('href *= *"(.+?)"',sHtmlContent)[0]
            if not 'speedvid' in Url:
                Url = 'http://www.speedvid.net/' + Url  
            if not 'http' in Url:
                if Url.startswith('//'):
                    Url = 'http:' + Url
                else:
                    Url = 'http://' + Url

        
        oRequest = cRequestHandler(Url)
        oRequest.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        sHtmlContent = oRequest.request()  
        

        api_call = ''
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\))<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for packed in aResult[1]:

                sHtmlContent = cPacker().unpack(packed)
                sHtmlContent = sHtmlContent.replace('\\','')
                

                sPattern2 = "{file:.([^']+.mp4)"
                aResult2 = oParser.parse(sHtmlContent, sPattern2)
                if (aResult2[0] == True):
                    # tris des faux liens
                    if not 'speedvid' in aResult2[1][0]:
                        api_call = aResult2[1][0]
                    

        if (api_call):
            api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
            return True, api_call
            
        return False, False

        
#*********************************************************************************************************************************


#
# Modified version From https://github.com/Kodi-vStream/venom-xbmc-addons
#
#
# Unpacker for Dean Edward's p.a.c.k.e.r, a part of javascript beautifier
# by Einar Lielmanis <einar@jsbeautifier.org>
#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#
# usage:
#
# if detect(some_string):
#     unpacked = unpack(some_string)
#

"""Unpacker for Dean Edward's p.a.c.k.e.r"""

import urllib2
import string
import xbmc

class cPacker():
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,')

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = self._filterargs(source)
        
        
        #correction
        if (len(symtab) > count) and (count > 0):
            del symtab[count:]
        if (len(symtab) < count) and (count > 0):
            symtab.append('BUGGED')                    
            
        #xbmc.log(str(count), xbmc.LOGNOTICE)
        #xbmc.log(str(symtab), xbmc.LOGNOTICE)
        #xbmc.log(str(len(symtab)), xbmc.LOGNOTICE) 

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')
        
        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word  = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return self._replacestrings(source)

    def _cleanstr(self, str):
        str = str.strip()
        if str.find("function") == 0:
            pattern = (r"=\"([^\"]+).*}\s*\((\d+)\)")
            args = re.search(pattern, str, re.DOTALL)
            if args:
                a = args.groups()
                def openload_re(match):
                    c = match.group(0)
                    b = ord(c) + int(a[1])
                    return chr(b if (90 if c <= "Z" else 122) >= b else b - 26)

                str = re.sub(r"[a-zA-Z]", openload_re, a[0]);
                str = urllib2.unquote(str)

        elif str.find("decodeURIComponent") == 0:
            str = re.sub(r"(^decodeURIComponent\s*\(\s*('|\"))|(('|\")\s*\)$)", "", str);
            str = urllib2.unquote(str)
        elif str.find("\"") == 0:
            str = re.sub(r"(^\")|(\"$)|(\".*?\")", "", str);
        elif str.find("'") == 0:
            str = re.sub(r"(^')|('$)|('.*?')", "", str);

        return str

    def _filterargs(self, source):
        """Juice from a source file the four args needed by decoder."""
        
        source = source.replace(',[],',',0,')

        juicer = (r"}\s*\(\s*(.*?)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\((.*?)\).split\((.*?)\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return self._cleanstr(a[0]), self._cleanstr(a[3]).split(self._cleanstr(a[4])), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        juicer = (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('(.*?)'\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return a[0], a[3].split(a[4]), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')



    def _replacestrings(self, source):
        """Strip string lookup table (list) and replace values in source."""
        match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

        if match:
            varname, strings = match.groups()
            startpoint = len(match.group(0))
            lookup = strings.split('","')
            variable = '%s[%%d]' % varname
            for index, value in enumerate(lookup):
                source = source.replace(variable % index, '"%s"' % value)
            return source[startpoint:]
        return source
        
def UnpackingError(Exception):
    #Badly packed source or general error.#
    #xbmc.log(str(Exception))
    print Exception
    pass


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base
        
        #Error not possible, use 36 by defaut
        if base == 0 :
            base = 36
        
        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret

        
class AADecoder(object):
    def __init__(self, aa_encoded_data):
        self.encoded_str = aa_encoded_data.replace('/*´∇｀*/','')

        self.b = ["(c^_^o)", "(ﾟΘﾟ)", "((o^_^o) - (ﾟΘﾟ))", "(o^_^o)",
                  "(ﾟｰﾟ)", "((ﾟｰﾟ) + (ﾟΘﾟ))", "((o^_^o) +(o^_^o))", "((ﾟｰﾟ) + (o^_^o))",
                  "((ﾟｰﾟ) + (ﾟｰﾟ))", "((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "(ﾟДﾟ) .ﾟωﾟﾉ", "(ﾟДﾟ) .ﾟΘﾟﾉ",
                  "(ﾟДﾟ) ['c']", "(ﾟДﾟ) .ﾟｰﾟﾉ", "(ﾟДﾟ) .ﾟДﾟﾉ", "(ﾟДﾟ) [ﾟΘﾟ]"]

    def is_aaencoded(self):
        idx = self.encoded_str.find("ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); ")
        if idx == -1:
            return False

        if self.encoded_str.find("(ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');", idx) == -1:
            return False

        return True

    def base_repr(self, number, base=2, padding=0):
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if base > len(digits):
            base = len(digits)

        num = abs(number)
        res = []
        while num:
            res.append(digits[num % base])
            num //= base
        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))

    def decode_char(self, enc_char, radix):
        end_char = "+ "
        str_char = ""
        while enc_char != '':
            found = False
            #for i in range(len(self.b)):
            #    if enc_char.find(self.b[i]) == 0:
            #        str_char += self.base_repr(i, radix)
            #        enc_char = enc_char[len(self.b[i]):]
            #        found = True
            #        break

            if not found:
                for i in range(len(self.b)):             
                    enc_char=enc_char.replace(self.b[i], str(i))
                
                startpos=0
                findClose=True
                balance=1
                result=[]
                if enc_char.startswith('('):
                    l=0
                    
                    for t in enc_char[1:]:
                        l+=1
                        if findClose and t==')':
                            balance-=1;
                            if balance==0:
                                result+=[enc_char[startpos:l+1]]
                                findClose=False
                                continue
                        elif not findClose and t=='(':
                            startpos=l
                            findClose=True
                            balance=1
                            continue
                        elif t=='(':
                            balance+=1
                 

                if result is None or len(result)==0:
                    return ""
                else:
                    
                    for r in result:
                        value = self.decode_digit(r, radix)
                        if value == "":
                            return ""
                        else:
                            str_char += value
                            
                    return str_char

            enc_char = enc_char[len(end_char):]

        return str_char


    def decode_digit(self, enc_int, radix):

        #enc_int=enc_int.replace('(ﾟΘﾟ)','1').replace('(ﾟｰﾟ)','4').replace('(c^_^o)','0').replace('(o^_^o)','3')  

        rr = '(\(.+?\)\))\+'
        rerr=enc_int.split(')))+')
        v = ''
        
        #new mode
        if (True):

            for c in rerr:
                
                if len(c)>0:
                    if c.strip().endswith('+'):
                        c=c.strip()[:-1]

                    startbrackets=len(c)-len(c.replace('(',''))
                    endbrackets=len(c)-len(c.replace(')',''))
                    
                    if startbrackets>endbrackets:
                        startbrackets = int (startbrackets)
                        endbrackets = int (endbrackets )
                        c+=')'*startbrackets-endbrackets

                    
                    c = c.replace('!+[]','1')
                    c = c.replace('-~','1+')
                    c = c.replace('[]','0')
                    
                    v+=str(eval(c))
                    
            return v
         
        # mode 0=+, 1=-
        mode = 0
        value = 0

        while enc_int != '':
            found = False
            for i in range(len(self.b)):
                if enc_int.find(self.b[i]) == 0:
                    if mode == 0:
                        value += i
                    else:
                        value -= i
                    enc_int = enc_int[len(self.b[i]):]
                    found = True
                    break

            if not found:
                return ""

            enc_int = re.sub('^\s+|\s+$', '', enc_int)
            if enc_int.find("+") == 0:
                mode = 0
            else:
                mode = 1

            enc_int = enc_int[1:]
            enc_int = re.sub('^\s+|\s+$', '', enc_int)

        return self.base_repr(value, radix)

    def decode(self):

        self.encoded_str = re.sub('^\s+|\s+$', '', self.encoded_str)
        
        self.encoded_str = self.encoded_str.replace('((ﾟДﾟ))','(ﾟДﾟ)')
        self.encoded_str = self.encoded_str.replace('((ﾟДﾟ)[ﾟoﾟ])','(ﾟДﾟ)[ﾟoﾟ]')

        
        # get data
        pattern = (r"\(ﾟДﾟ\)\[ﾟoﾟ\]\+ (.+?)\(ﾟДﾟ\)\[ﾟoﾟ\]\)")
        result = re.search(pattern, self.encoded_str, re.DOTALL)
        if result is None:
            VSlog("AADecoderee: data not found")
            return False

        data = result.group(1)

        # hex decode string
        begin_char = "(ﾟДﾟ)[ﾟεﾟ]+"
        alt_char = "(oﾟｰﾟo)+ "

        out = ''

        while data != '':
            
            # Check new char
            if data.find(begin_char) != 0:
                VSlog("AADecoderwwww: data not found")
                return False

            data = data[len(begin_char):]

            # Find encoded char
            enc_char = ""
            if data.find(begin_char) == -1:
                enc_char = data
                data = ""
            else:
                enc_char = data[:data.find(begin_char)]
                data = data[len(enc_char):]

            
            radix = 8
            # Detect radix 16 for utf8 char
            if enc_char.find(alt_char) == 0:
                enc_char = enc_char[len(alt_char):]
                radix = 16

            str_char = self.decode_char(enc_char, radix)
            
            if str_char == "":
                VSlog("no match :  ")
                print  data + "\nout = " + out + "\n"
                return False
            
            out += chr(int(str_char, radix))

        if out == "":
            VSlog("no match : " + data )
            return False

        return out
