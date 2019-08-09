#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.aadecode import AADecoder
from resources.lib.jjdecode import JJDecoder
import re
from resources.lib.comaddon import VSlog
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MyStream'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'mystream'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

        # sPattern =  '(?:https*:\/\/|\/\/)(?:www.|embed.|)mystream.(?:la|com|to)\/(?:video\/|external\/|embed-|)([0-9a-zA-Z]+)'
        # oParser = cParser()
        # aResult = oParser.parse(sUrl, sPattern)
        # self.__sUrl = 'https://mysembed.net/' + str(aResult[1][0])

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        url = self.__sUrl
        
        #url = self.__sUrl.replace('embed.mystream.to','mstream.cloud')
        #url = 'https://mstream.cloud/gfa35ebu1nt1'

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        sHtmlContent = oRequest.request()


        oParser = cParser()
        
        api_call = False
        a = ''
        b = ''
        c = ''
        urlcoded = ''
        
        sPattern =  '(?:[>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = AADecoder(i).decode()
                #VSlog(decoded)
                
                r = re.search("atob\(\'([^']+)\'\)", decoded, re.DOTALL | re.UNICODE)
                if r:
                    urlcoded = r.group(1)

                    break
                    
        
        reducesHtmlContent = oParser.abParse(sHtmlContent, '<z9></z9><script>','{if(document')

        sPattern =  '(\w+)'
        aResult = oParser.parse(reducesHtmlContent, sPattern)
        if aResult[0]:
            mlist = sorted(aResult[1], key=len)
            mlist = mlist[-2:]
            a = mlist[0]
            b = mlist[1]
            #VSlog('a= ' + str(a))
            #VSlog('b= ' + str(b))
            
        sPattern =  "=\['getAttribute','*([^']+)'*\]"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            encodedC = aResult[1][0].replace('window.','')
            #VSlog('encodec= ' + str(encodedC))
            c = Cdecode(sHtmlContent,encodedC)
            if c:
                #VSlog('c= ' + str(c))
                api_call = decode(urlcoded,a,b,c)

 
        if (api_call):
            return True, api_call + '|User-Agent=' + UA
            
        return False, False
        
def Cdecode(sHtmlContent,encodedC):
    oParser = cParser()
    sPattern =  '<([0-9a-zA-Z]+)><script>([^<]+)<\/script>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    z = []
    y = []
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            z.append(JJDecoder(aEntry[1]).decode())
        #VSlog(z)
        for x in z:
            r1 = re.search("atob\(\'([^']+)\'\)", x, re.DOTALL | re.UNICODE)
            if r1:
                y.append(base64.b64decode(r1.group(1)))
                
        for w in y:

            r2 = re.search(encodedC + "='([^']+)'", w)
            if r2:
                return r2.group(1)

def decode(urlcoded,a,b,c):
    TableauTest = {}
    key = ''

    l = a
    n = "0123456789"
    h = b
    j = 0

    while j < len(l) :
        k = 0
        while k < len(n):
            TableauTest[l[j] + n[k]] = h[int(j + k)]

            k+=1

        j+=1

    hash = c
    i = 0
    while i < len(hash):
        key = key + TableauTest[hash[i] + hash[i + 1]]
        i+= 2


    chain = base64.b64decode(urlcoded)

    secretKey = {}
    y = 0
    temp = ''
    url = ""

    x = 0
    while x < 256:
        secretKey[x] = x
        x += 1

    x = 0
    while x < 256:
        y = (y + secretKey[x] + ord(key[x % len(key)])) % 256
        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp
        x += 1

    x = 0
    y = 0
    i = 0
    while i < len(chain):
        x += 1 % 256
        y = (y + secretKey[x]) % 256
        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp

        url = url + (chr(ord(chain[i]) ^ secretKey[(secretKey[x] + secretKey[y]) % 256]))

        i += 1
        
    return url
