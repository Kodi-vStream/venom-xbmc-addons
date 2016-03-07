#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.jjdecode import JJDecoder
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
#from resources.lib.aadecode import AADecoder
import re,urllib2

def base10toN(num, n):

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
        sPattern = "<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)<\/script"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            string = AADecoder(aResult[1][0]).decode()
            #print string
            if 'toString' in string:
                base = int(re.findall('toString\(a\+([0-9]+)\)',string)[0])
                table = re.findall('(\([0-9][^)]+\))',string)
                
                for i in table:
                    val = re.findall('([0-9]+),([0-9]+)',i)
                    base2 = base + int(val[0][0])
                    char = base10toN(int(val[0][1]), base2)
                    string = string.replace(i, char)
                
                #nettoyage
                string = string.replace('+', '')
                string = string.replace('"', '')
                string = string.replace('', '')

                #bidouille pour pas avoir a tout recoder
                url = re.findall('(http[^<>}]+)',string)[0]
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
            return True, api_call
            
        return False, False
        
# author : Djeman
# Updated by Shani-08


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
        rerr=enc_int.split('))+')
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
                        c+=')'*startbrackets-endbrackets
                    
                    #fh = open('c:\\test.txt', "w")
                    #fh.write(c)
                    #fh.close()
                    
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

        # get data
        pattern = (r"\(ﾟДﾟ\)\[ﾟoﾟ\]\+ (.+?)\(ﾟДﾟ\)\[ﾟoﾟ\]\)")
        result = re.search(pattern, self.encoded_str, re.DOTALL)
        if result is None:
            print "AADecoder: data not found"
            return False

        data = result.group(1)

        # hex decode string
        begin_char = "(ﾟДﾟ)[ﾟεﾟ]+"
        alt_char = "(oﾟｰﾟo)+ "

        out = ''

        while data != '':
            # Check new char
            if data.find(begin_char) != 0:
                print "AADecoder: data not found"
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
                print "no match :  "
                print  data + "\nout = " + out + "\n"
                return False
            
            out += chr(int(str_char, radix))

        if out == "":
            print "no match : " + data
            return False

        return out
