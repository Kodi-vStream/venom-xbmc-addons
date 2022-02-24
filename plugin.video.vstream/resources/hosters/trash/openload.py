#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import re

try: # Python 2
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.aadecode import AADecoder
from resources.lib.jjdecode import JJDecoder
from resources.lib.packer import cPacker
from resources.lib.util import QuoteSafe
from resources.lib.comaddon import dialog, VSlog, xbmc
#Pour le futur
from resources.lib.jsparser import JsParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'openload', 'OpenLoad')

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace('openload.io', 'openload.co')
        self._url = QuoteSafe(sUrl)
        if self._url[-4:-3] == '.':
            self._url = self._url.replace(self._url.split('/')[-1], '')

    def __getHost(self):
        parts = self._url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self):
        oParser = cParser()

        #recuperation de la page
        #xbmc.log('url teste : ' + self._url)
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('referer', self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent1 = oRequest.request()

        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent1)
        #fh.close()

        #Recuperation url cachee
        TabUrl = []
        #sPattern = '<span style="".+?id="([^"]+)">([^<]+)<\/span>'
        sPattern = '<p id="([^"]+)" *style=\"\">([^<]+)<\/p>'
        aResult = re.findall(sPattern, sHtmlContent1)
        if not aResult:
            sPattern = '<p style="" *id="([^"]+)" *>([^<]+)<\/p>'
            aResult = re.findall(sPattern, sHtmlContent1)
        if (aResult):
            TabUrl = aResult
        else:
            VSlog('OPL er 1')
            return False, False

        #xbmc.log("Nbre d'url : " + str(len(TabUrl)))

        #on essait de situer le code
        sPattern = '<script src="\/assets\/js\/video-js\/video\.js.+?.js"(.+)*'

        aResult = re.findall(sPattern, sHtmlContent1, re.DOTALL)
        if (aResult):
            sHtmlContent3 = aResult[0]
        else:
            VSlog('OPL er 2')
            return False, False

        #Deobfuscation, a optimiser pour accelerer le traitement
        code = ''
        maxboucle = 4
        while (maxboucle > 0):
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            sHtmlContent3 = CheckJJDecoder(sHtmlContent3)
            sHtmlContent3 = CheckAADecoder(sHtmlContent3)

            maxboucle = maxboucle - 1

        code = sHtmlContent3

        #fh = open('c:\\html.txt', 'w')
        #fh.write(code)
        #fh.close()

        id_final = ''
        sPattern = 'var srclink.*?\/stream\/.*?(#[^\'"]+).*?mime=true'
        aResult = re.findall(sPattern, code)
        if (aResult):
            id_final = aResult[0]
        else:
            VSlog('OPL er 9')
            return False, False

        if not (code):
            VSlog('OPL er 3')
            return False, False

        #Search the coded url
        Coded_url = ''
        for i in TabUrl:
            if len(i[1]) > 30:
                Coded_url = i[1]
                Item_url = '#' + i[0]
                VSlog( Item_url + ' : ' + Coded_url )

        if not(Coded_url):
            VSlog('Url codée non trouvée')
            return False, False

        #Nettoyage du code pr traitement
        code = CleanCode(code, Coded_url)

        #fh = open('c:\\JS.txt', 'w'w)
        #fh.write(code)
        #fh.close()

        VSlog('Code JS extrait')

        dialog().VSinfo('Décodage: Peut durer plus d\'une minute.', self.__sDisplayName, 15)

        #interpreteur JS
        JP = JsParser()
        Liste_var = []
        JP.AddHackVar(Item_url, Coded_url)

        JP.ProcessJS(code, Liste_var)

        url = None
        #for name in [ '#streamurl', '#streamuri', '#streamurj']:
        #    if JP.IsVar( JP.HackVars, name ):
        #        url = JP.GetVarHack( name )
        #        VSlog( 'Decoded url ' + name + ' : ' + url )
        #        break
        url = JP.GetVarHack(id_final)

        if not(url):
            VSlog('Rate, debug: ' + str(Liste_var))
            return False, False

        dialog().VSinfo('Ok, lien décodé.', self.__sDisplayName, 15)

        api_call = self.__getHost() + '/stream/' + url + '?mime=true'

        if '::' in api_call:
            dialog().VSinfo('Possible problème d\'ip V6', self.__sDisplayName, 5)
            xbmc.sleep(5*1000)

        VSlog(api_call)

        if api_call:
            return True, api_call

        return False, False

#****************************************************************
#Fonction utilisee pour nettoyer le code et recuperer le code JS
#****************************************************************

def ASCIIDecode(string):

    i = 0
    l = len(string)
    ret = ''
    while i < l:
        c = string[i]
        if string[i:(i + 2)] == '\\x':
            c = chr(int(string[(i + 2):(i + 4)], 16))
            i += 3
        if string[i:(i + 2)] == '\\u':
            cc = int(string[(i + 2):(i + 6)], 16)
            if cc > 256:
                #ok c'est de l'unicode, pas du ascii
                return ''
            c = chr(cc)
            i += 5
        ret = ret + c
        i = i + 1

    return ret

def SubHexa(g):
    return g.group(1) + Hexa(g.group(2))

def Hexa(string):
    return str(int(string, 0))

def parseInt(sin):
    if re.match(r'\d+', str(sin), re.M) and not callable(sin):
        return int(''.join([c for c in re.split(r'[,.]', str(sin))[0] if c.isdigit()]))
    return None

def CheckCpacker(strToPack):

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, strToPack)
    if (aResult):
        str2 = aResult[0]
        if not str2.endswith(';'):
            str2 = str2 + ';'
        try:
            strToPack = cPacker().unpack(str2)
            print('Cpacker encryption')
        except:
            pass

    return strToPack

def CheckJJDecoder(strDecoder):

    sPattern = '([a-z]=.+?\(\)\)\(\);)'
    aResult = re.findall(sPattern, strDecoder)
    if (aResult):
        print('JJ encryption')
        return JJDecoder(aResult[0]).decode()

    return strDecoder

def CheckAADecoder(strToDecode):
    aResult = re.search('([>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)', strToDecode, re.DOTALL | re.UNICODE)
    if (aResult):
        print('AA encryption')
        tmp = aResult.group(1) + AADecoder(aResult.group(2)).decode()
        return strToDecode[:aResult.start()] + tmp + strToDecode[aResult.end():]

    return strToDecode

def CleanCode(code, Coded_url):
    #extract complete code
    r = re.search(r'type="text\/javascript">(.+?)<\/script>', code, re.DOTALL)
    if r:
        code = r.group(1)

    #1 er decodage
    code = ASCIIDecode(code)

    #fh = open('c:\\html2.txt', "w")
    #fh.write(code)
    #fh.close()

    #extract first part
    P3 = "^(.+?)}\);\s*\$\(\"#videooverlay"
    r = re.search(P3, code, re.DOTALL)
    if r:
        code = r.group(1)
    else:
        VSlog('er1')
        return False

    #hack a virer dans le futur
    code = code.replace('!![]', 'true')
    P8 = '\$\(document\).+?\(function\(\){'
    code= re.sub(P8, '\n', code)
    P4 = 'if\(!_[0-9a-z_\[\(\'\)\]]+,document[^;]+\)\){'
    code = re.sub(P4, 'if (false) {', code)
    P4 = 'if\(+\'toString\'[^;]+document[^;]+\){'
    code = re.sub(P4, 'if (false) {', code)

    #hexa convertion
    code = re.sub('([^_])(0x[0-9a-f]+)', SubHexa, code)

    #Saut de ligne
    #code = code.replace(';', ';\n')
    code = code.replace('case', '\ncase')
    code = code.replace('}', '\n}\n')
    code = code.replace('{', '{\n')

    #tab
    code = code.replace('\t', '')

    #hack
    code = code.replace('!![]', 'true')

    return code

#************************************************************
#Fonctions non utilisées, juste la pour memoire
#************************************************************

def GetOpenloadUrl(url,referer):
    if 'openload.co/stream' in url:

        headers = {'User-Agent': UA,
                   #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   #'Accept-Encoding': 'gzip, deflate, br',
                   #'Host': 'openload.co',
                   'Referer': referer
        }

        req = urllib2.Request(url, None, headers)
        res = urllib2.urlopen(req)
        #xbmc.log(res.read())
        finalurl = res.geturl()


        VSlog('Url decodee : ' + finalurl)

        #autres infos
        #xbmc.log(str(res.info()))
        #xbmc.log(res.info()['Content-Length'])

        if 'KDA_8nZ2av4/x.mp4' in finalurl:
            VSlog('pigeon url : ' + url)
            finalurl = ''
        if 'Content-Length' in res.info():
            if res.info()['Content-Length'] == '33410733':
                VSlog('pigeon url : ' + url)
                finalurl = ''
        if url == finalurl:
            VSlog('Bloquage')
            finalurl = ''

        return finalurl
    return url

#Code updated with code from https://gitlab.com/iptvplayer-for-e2
def decodek(k):
    y = ord(k[0])
    e = y - 0x37
    d = max(2, e)
    e = min(d, len(k) - 0x24 - 2)
    t = k[e:e + 0x24]
    h = 0
    g = []
    while h < len(t):
        f = t[h:h+3]
        g.append(int(f, 0x8))
        h += 3
    v = k[0:e] + k[e+0x24:]
    p = []
    i = 0
    h = 0
    while h < len(v):
        B = v[h:h + 2]
        C = v[h:h + 3]
        f = int(B, 0x10)
        h += 0x2

        if (i % 3) == 0:
            f = int(C, 8)
            h += 1
        elif i % 2 == 0 and i != 0 and ord(v[i-1]) < 0x3c:
            f = int(C, 0xa)
            h += 1

        A = g[i % 0xc]
        f = f ^ 0xd5
        f = f ^ A
        p.append(chr(f))
        i += 1

    return "".join(p)
