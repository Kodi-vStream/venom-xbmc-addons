#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster

import re,urllib2,urllib
import xbmcgui
from resources.lib.packer import cPacker
import xbmc

#Remarque : meme code que vodlocker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
#UA = 'Nokia7250/1.0 (3.14) Profile/MIDP-1.0 Configuration/CLDC-1.0'

def ASCIIDecode(string):
    
    i = 0
    l = len(string)
    ret = ''
    while i < l:
        c =string[i]
        if string[i:(i+2)] == '\\x':
            c = chr(int(string[(i+2):(i+4)],16))
            i+=3
        if string[i:(i+2)] == '\\u':
            cc = int(string[(i+2):(i+6)],16)
            if cc > 256:
                #ok c'est de l'unicode, pas du ascii
                return ''
            c = chr(cc)
            i+=5
        ret = ret + c
        i = i + 1

    return ret

def GetHtml(url,headers):
    request = urllib2.Request(url,None,headers)
    reponse = urllib2.urlopen(request)
    sCode = reponse.read()
    reponse.close()
    
    return sCode

def UnlockUrl(url2=None):
    headers9 = {
    'User-Agent': UA,
    'Referer':'https://www.flashx.tv/dl?playthis'
    }
    
    url1 = 'https://www.flashx.tv/js/code.js'
    if url2:
        url1 = url2
        
    if not url1.startswith('http'):
        url1 = 'https:' + url1
        
    cConfig().log('unlock url :' + url1)
    
    oRequest = cRequestHandler(url1)
    oRequest.addParameters('User-Agent', UA)
    #oRequest.addParameters('Accept', '*/*')
    #oRequest.addParameters('Accept-Encoding', 'gzip, deflate, br')
    #oRequest.addParameters('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addParameters('Referer','https://www.flashx.tv/dl?playthis')
    code = oRequest.request()
    
    url = ''
    if not code:
        url = oRequest.getRealUrl()
    else:
        #cConfig().log(code)
        aResult = re.search("!= null\){\s*\$.get\('([^']+)',{(.+?)}", code, re.DOTALL)
        if aResult:
            dat = aResult.group(2)
            dat = dat.replace("'",'')
            dat = dat.replace(" ",'')

            dat2 = dict(x.split(':') for x in dat.split(','))

            dat3 = aResult.group(1) + '?'
            for i,j in dat2.items():
                dat3 = dat3 + str(i)+ '=' + str(j) + '&'
            
            url = dat3[:-1]
            
    #url = 'https://www.flashx.tv/flashx.php?fxfx=6'
    
    if url:
        cConfig().log(url)
        GetHtml(url,headers9)
        return True
        
    return False

def LoadLinks(htmlcode):
        xbmc.log('Scan des liens')
    
        host = 'https://www.flashx.tv'
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
            
            #xbmc.log('test : ' + sUrl)
            
            if '\\x' in sUrl or '\\u' in sUrl:
                sUrl = ASCIIDecode(sUrl)
                if not sUrl:
                    continue
            
            if sUrl.startswith('//'):
                sUrl = 'http:' + sUrl
                
            if sUrl.startswith('/'):
                sUrl = host + sUrl
            
            #Url ou il ne faut pas aller
            if 'dok3v' in sUrl:
                continue
                
            #pour test
            if '.js' not in sUrl:
                continue
            #if 'flashx' in sUrl:
                #continue

            headers8 = {
            'User-Agent': UA,
            'Referer':'https://www.flashx.tv/dl?playthis'
            }
            
            try:
                request = urllib2.Request(sUrl,None,headers8)
                reponse = urllib2.urlopen(request)
                sCode = reponse.read()
                reponse.close()
                xbmc.log('Worked ' + sUrl)
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
                        xbmc.log('Worked ' + sUrl)
                    except urllib2.HTTPError, e:
                        xbmc.log(str(e.code))
                        #xbmc.log(e.read())
                        xbmc.log('Redirection Blocked ' + sUrl + ' Red ' + e.geturl())
                        pass
                else:
                    xbmc.log('Blocked ' + sUrl)
                    xbmc.log(str(e.code))
                    xbmc.log('>>' + e.geturl())
                    xbmc.log(e.read())
        
        xbmc.log('fin des unlock')

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'FlashX'
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
        return 'flashx'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def GetRedirectHtml(self,web_url,sId,NoEmbed = False):
        
        headers = {
        #'Host' : 'www.flashx.tv',
        'User-Agent': UA,
        #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer':'http://embed.flashx.tv/embed.php?c=' + sId,
        'Accept-Encoding':'identity'
        }
        
        MaxRedirection = 3
        while MaxRedirection > 0:
            
            #generation headers
            #headers2 = headers
            #headers2['Host'] = self.GetHost(web_url)
            
            cConfig().log(str(MaxRedirection) + ' Test sur : ' + web_url)
            request = urllib2.Request(web_url,None,headers)
      
            redirection_target = web_url
        
            try:
                #ok ca a enfin marche
                reponse = urllib2.urlopen(request)
                sHtmlContent = reponse.read()
                reponse.close()

                if not (reponse.geturl() == web_url) and not (reponse.geturl() == ''):
                    redirection_target = reponse.geturl()
                else:
                    break
            except urllib2.URLError, e:
                if (e.code == 301) or  (e.code == 302):
                    redirection_target = e.headers['Location']
                else:
                    #cConfig().log(str(e.code))
                    #cConfig().log(str(e.read()))
                    return False
                
            web_url = redirection_target
            
            if 'embed' in redirection_target and NoEmbed:
                #rattage, on a pris la mauvaise url
                cConfig().log('2')
                return False
            
            MaxRedirection = MaxRedirection - 1
            
        return sHtmlContent

    def __getIdFromUrl(self, sUrl):
        sPattern = "https*:\/\/((?:www.|play.)?flashx.tv)\/(?:playvid-)?(?:embed-)?(?:embed.+?=)?(-*[0-9a-zA-Z]+)?(?:.html)?"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def GetHost(self,sUrl):
        oParser = cParser()
        sPattern = 'https*:\/\/(.+?)\/'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = 'http://' + self.GetHost(sUrl) + '/embed.php?c=' + self.__getIdFromUrl(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def CheckGoodUrl(self,url):
        
        xbmc.log('test de ' + url)
        headers = {'User-Agent': UA
                   #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   #'Accept-Encoding':'gzip, deflate, br',
                   #'Host':'openload.co',
                   #'Referer':referer
        }

        req = urllib2.Request(url)#,None,headers)
        res = urllib2.urlopen(req)
        #pour afficher contenu
        #xbmc.log(res.read())
        #pour afficher header
        xbmc.log(str(res.info()))
        #Pour afficher redirection
        xbmc.log('red ' + res.geturl())
        
        if 'embed' is res.geturl():
            return false
            
        html = res.read()
        
        res.close()

        return res
        
    def __getMediaLinkForGuest(self):
        
        oParser = cParser()
        
        #on recupere le host atuel
        HOST = self.GetHost(self.__sUrl)
 
        #on recupere l'ID
        sId = self.__getIdFromUrl(self.__sUrl)
        if sId == '':
            cConfig().log("Id prb")
            return False,False
        
        #on ne garde que les chiffres
        #sId = re.sub(r'-.+', '', sId)
        
        #on cherche la vraie url
        sHtmlContent = self.GetRedirectHtml(self.__sUrl, sId)
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        #sPattern = '(<[^<>]+(?:"visibility:hidden"|"opacity: 0;")><a )*href="(http:\/\/www\.flashx[^"]+)'
        sPattern = 'href=["\'](https*:\/\/www\.flashx[^"\']+)'
        AllUrl = re.findall(sPattern,sHtmlContent,re.DOTALL)
        cConfig().log(str(AllUrl))

        #Disabled for the moment
        if (False):
            if AllUrl:
                # Need to find which one is the good link
                # Use the len don't work
                for i in AllUrl:
                    if i[0] == '':
                        web_url = i[1]
            else:
                return False,False
        else:
            web_url = AllUrl[0]
            
        web_url = AllUrl[0]
        
        #Requests to unlock video
        #unlock fake video
        LoadLinks(sHtmlContent)
        #unlock bubble
        url2 = re.search('["\']([^"\']+?js\/code\.js\?cache.+?)["\']', sHtmlContent, re.DOTALL)
        if url2:
            url2 = url2.group(1)
        if not UnlockUrl(url2):
            cConfig().log('No special unlock url')
            return False,False
               
        #get the page
        sHtmlContent = self.GetRedirectHtml(web_url, sId, True)
        
        if sHtmlContent == False:
            cConfig().log('Passage en mode barbare')
            #ok ca a rate on passe toutes les url de AllUrl
            for i in AllUrl:
                if not i == web_url:
                    sHtmlContent = self.GetRedirectHtml(i, sId, True)
                    if sHtmlContent:
                        break

        if not sHtmlContent:
            return False,False

        #fh = open('c:\\test2.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        cConfig().log('Page obtenue')

        if 'reload the page!' in sHtmlContent:
            cConfig().log("page bloquée")
            
            #On recupere la bonne url
            sGoodUrl = web_url

            #on recupere la page de refresh
            sPattern = 'reload the page! <a href="([^"]+)">!! <b>'
            aResult = re.findall(sPattern,sHtmlContent)
            if not aResult:
                return False,False
            sRefresh = aResult[0]
            
            #on recupere le script de debloquage
            sPattern = 'type="text\/javascript" src="([^"]+checkembed[^"]+)"><\/script>'
            aResult = re.findall(sPattern,sHtmlContent)
            if not aResult:
                return False,False
            
            #on debloque la page (en test ca a l'air inutile)
            sHtmlContent = self.GetRedirectHtml(aResult[0],sId)
            
            #lien speciaux ?
            if sRefresh.startswith('./'):
                sRefresh = 'http://' + self.GetHost(sGoodUrl) + sRefresh[1:]
            
            #on rafraichit la page
            sHtmlContent = self.GetRedirectHtml(sRefresh,sId)
            
            #et on re-recupere la page
            sHtmlContent = self.GetRedirectHtml(sGoodUrl,sId)
            
        if (False):
         
            #A t on le lien code directement?
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern,sHtmlContent)
                    
            if (aResult):
                cConfig().log( "lien code")
                
                AllPacked = re.findall('(eval\(function\(p,a,c,k.*?)\s+<\/script>', sHtmlContent, re.DOTALL)
                if AllPacked:
                    for i in AllPacked:
                        sUnpacked = cPacker().unpack(i)
                        sHtmlContent = sUnpacked
                        #xbmc.log(sHtmlContent)
                        if "file" in sHtmlContent:
                            break
                else:
                    return False,False
  
        #decodage classique
        sPattern = '{file:"([^",]+)",label:"([^"<>,]+)"}'
        sPattern = '{src: *\'([^"\',]+)\'.+?label: *\'([^"<>,\']+)\''
        aResult = oParser.parse(sHtmlContent, sPattern)

        api_call = ''
        
        #xbmc.log(str(aResult))
        
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Affichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality', qua)
                if (ret > -1):
                    api_call = url[ret]

        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
