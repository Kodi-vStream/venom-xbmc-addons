#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://www.video.tt/embed/xxx
#http://thevideo.me/embed-xxx-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import VScreateDialogSelect
from resources.lib.packer import cPacker
from resources.lib.util import VSlog


import re,xbmc,urllib,urllib2

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"

#Meme code que vidup

 
def LoadLinks(htmlcode):
    VSlog('Scan des liens')

    sPattern ='[\("\'](https*:)*(\/[^,"\'\)\s]+)[\)\'"]'
    aResult = re.findall(sPattern, htmlcode, re.DOTALL)

    #xbmc.log(str(aResult))
    for http,urlspam in aResult:
        sUrl = urlspam
            
        if http:
            sUrl = http + sUrl
            
        sUrl = sUrl.replace('/\/','//')
        sUrl = sUrl.replace('\/','/')
        
        #filtrage mauvaise url
        if (sUrl.count('/') < 2) or ('<' in sUrl) or ('>' in sUrl) or (len(sUrl) < 15):
            continue
        if '[' in sUrl or ']' in sUrl:
            continue
        if '.jpg' in sUrl or '.png' in sUrl:
            continue
        
        VSlog('test : ' + sUrl)
        
        if '\\x' in sUrl or '\\u' in sUrl:
            sUrl = ASCIIDecode(sUrl)
            if not sUrl:
                continue
        
        if sUrl.startswith('//'):
            sUrl = 'http:' + sUrl
            
        if sUrl.startswith('/'):
            host = 'https://thevideo.website'
            sUrl = host + sUrl
        
        #Url ou il ne faut pas aller
        if 'dok3v' in sUrl:
            continue
            
        #pour test
        if ('.js' not in sUrl) and ('.cgi' not in sUrl):
            continue
        #if 'flashx' in sUrl:
            #continue

        headers8 = {
        'User-Agent': UA
        #'Referer':'https://www.flashx.tv/dl?playthis'
        }
        
        try:
            request = urllib2.Request(sUrl,None,headers8)
            reponse = urllib2.urlopen(request)
            sCode = reponse.read()
            reponse.close()
            VSlog('Worked ' + sUrl)
        except urllib2.HTTPError, e:
            if not e.geturl() == sUrl:
                try:
                    headers9 = {
                    'User-Agent': UA,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding':'gzip, deflate, br'
                    }
                    request = urllib2.Request(e.geturl().replace('https', 'http'), None, headers9)
                    reponse = urllib2.urlopen(request)
                    sCode = reponse.read()
                    reponse.close()
                    VSlog('Worked ' + sUrl)
                except urllib2.HTTPError, e:
                    VSlog(str(e.code))
                    #xbmc.log(e.read())
                    VSlog('Redirection Blocked ' + sUrl + ' Red ' + e.geturl())
                    pass
            else:
                VSlog('Blocked ' + sUrl)
                VSlog(str(e.code))
                VSlog('>>' + e.geturl())
                #cConfig().log(e.read())
    
    VSlog('fin des unlock')


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'TheVideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'thevideo_me'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def __getIdFromUrl(self,sUrl):
        """ URL trouvées:
            https://thevideo.me/1a2b3c4e5d6f
            https://thevideo.me/embed-1a2b3c4e5d6f.html
            http(s)://thevideo.me/embed-1a2b3c4e5d6f-816x459.html
        """
        sPattern = '\/(?:embed-)?(\w+)(?:-\d+x\d+)?(?:\.html)?$' 
        aResult = cParser().parse( sUrl, sPattern )
        if (aResult[0] == True):
            return aResult[1][0]
        return ''
 
    def setUrl(self, sUrl):
        sId = self.__getIdFromUrl( sUrl )
        self.__sUrl = 'https://thevideo.me/embed-' + sId + '.html'

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = False
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        #decodage de la page html
        sHtmlContent3 = sHtmlContent
        code = ''
        maxboucle = 3
        while (maxboucle > 0):
            VSlog('loop : ' + str(maxboucle))
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            #sHtmlContent3 = CheckJJDecoder(sHtmlContent3)           
            #sHtmlContent3 = CheckAADecoder(sHtmlContent3)
            
            maxboucle = maxboucle - 1   
         
        sHtmlContent = sHtmlContent3
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        #LoadLinks(sHtmlContent)
        
        oParser = cParser()
        
        sPattern = "var thief='([^']+)';"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not (aResult[0]):
            VSlog('thief var')
            return False , False
            
        key = aResult[1][0].replace('+','')
            
        sPattern = "'rc=[^<>]+?\/(.+?)'\.concat"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not (aResult[0]):
            VSlog('url var')
            return False , False
            
        ee = aResult[1][0]
            
        url2 = 'https://thevideo.me/' + ee + '/' + key
        
        VSlog('unlock url 1 :' + url2)

        oRequest = cRequestHandler(url2)
        sHtmlContent2 = oRequest.request()
        
        if (True):
            code = cPacker().unpack(sHtmlContent2)
            
            #fh = open('c:\\test.txt', "w")
            #fh.write(code)
            #fh.close()    
            
            sPattern = '"vt=([^"]+)'
            r2 = re.search(sPattern,code)
            if not (r2):
                VSlog('vt error')
                return False,False
        
        if (True):   
            #Unlock url
            url1 = re.search(r'async src="([^"]+)">', sHtmlContent,re.DOTALL).group(1)
            VSlog(url1)
            oRequest = cRequestHandler(url1)
            sHtmlContenttmp1 = oRequest.request()
            
            sId = self.__getIdFromUrl( self.__sUrl )
            url2 = 'https://thevideo.website/api/slider/' + sId
            VSlog(url2)
            oRequest = cRequestHandler(url2)
            sHtmlContenttmp2 = oRequest.request()
            #url3 = re.search(r'"src":"([^"]+)"', sHtmlContenttmp2,re.DOTALL).group(1)
            #VSlog(url3)
            #oRequest = cRequestHandler(url3)
            #sHtmlContenttmp3 = oRequest.request()
            
            xbmc.sleep(1000)
            
        sPattern = '{"file":"([^"]+)","label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si  1 url
            if len(url) == 1:
                api_call = url[0]
            #Affichage du tableau
            elif len(url) > 1:
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]

        #xbmc.sleep(5000)
                    
        #api_call ='https://n4081.thevideo.me:8777/ivcgn7pgt23xu37wrbrovparhhdg6yozy42ehjynz3p3lxyt2da7ibbxyhzjgbcxf5vtsutqndvnbfcpxvelknwgfy3pbkml7ff3s2baxyzssn7o6rw66s2gcnlmzejg75pcbw2io7vdcqkg3o2ggpduysgsbybagh434jamjp3pc5gdvqc7tpfd7hxn4hdx5p2klae7mrjecghepspd6jezziuqi4xrfsbg5hldgqfirxevcaaurglqznpxivy5wndsnvedx4xokoonky77bi4mjzzq/v.mp4?direct=false&ua=1&vt=pw42hcaoyjkxkx3qfwd4gdyoc775sk55pq7sqsr7rsv4rp3qk4huxuitpwqolirqnsmcyomiwarevrb4mt4lgbouyzxvtx3z4i3it6m3gr4lke7tske5sljujqarhotsraukqq4nqwkzoqdqw5qo7zjmobw5vzwd6r5oudfvp3deh2xo3boy75pkrzybt2mftelbbbqcifmoezvqw3cqeanck5lmzhshcph2qtseoakvw26bscztw44didbp63qrmc56j3wu7kmg6bhpiidfstx57m'
        if (api_call):
            api_call = api_call + '?direct=false&ua=1&vt=' + r2.group(1)
            return True, api_call
            
        return False, False

        
#-----------------------------------------------------------------------------------------
def CheckCpacker(str):

    sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\s*)<'
    aResult = re.search(sPattern, str,re.DOTALL | re.UNICODE)
    if (aResult):
        #VSlog('Cpacker encryption')
        str2 = aResult.group(1)
        
        if not str2.endswith(';'):
            str2 = str2 + ';'

        #if not str2.startswith('eval'):
        #    str2 = 'eval(function' + str2[4:]
        
        #Me demandez pas pourquoi mais si je l'affiche pas en log, ca freeze ?????
        #VSlog(str2)
        
        try:
            tmp = cPacker().unpack(str2)
            #tmp = tmp.replace("\\'","'")
        except:
            tmp =''
            
        #VSlog(tmp)

        return str[:(aResult.start() + 1)] + tmp + str[(aResult.end()-1):]
        
    return str
