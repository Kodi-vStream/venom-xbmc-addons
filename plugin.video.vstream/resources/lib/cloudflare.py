#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
import re,os
import urllib2,urllib
import xbmc
import xbmcaddon

#Cookie path
#C:\Users\BRIX\AppData\Roaming\Kodi\userdata\addon_data\plugin.video.vstream\

#Light method
#Ne marche que si meme user-agent
    # req = urllib2.Request(sUrl,None,headers)
    # try:
        # response = urllib2.urlopen(req)
        # sHtmlContent = response.read()
        # response.close()
            
    # except urllib2.HTTPError, e:

        # if e.code == 503:
            # if CloudflareBypass().check(e.headers):
                # cookies = e.headers['Set-Cookie']
                # cookies = cookies.split(';')[0]
                # sHtmlContent = CloudflareBypass().GetHtml(sUrl,e.read(),cookies)
    
#Heavy method
# sHtmlContent = CloudflareBypass().GetHtml(sUrl)

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def parseInt(chain):
    
    chain = chain.replace(' ','')
    chain = re.sub(r'!!\[\]','1',chain) # !![] = 1
    chain = re.sub(r'\(!\+\[\]','(1',chain)  #si le bloc commence par !+[] >> +1
    chain = re.sub(r'(\([^()]+)\+\[\]\)','(\\1)*10)',chain)  # si le bloc fini par +[] >> *10
    
    #bidouilles a optimiser non geree encore par regex
    chain = re.sub(r'\(\+\[\]\)','0',chain)
    if chain.startswith('!+[]'):
        chain = chain.replace('!+[]','1')
    
    return eval(chain)
    
def CheckIfActive(data):
    if 'Checking your browser before accessing' in data:
    #if ( "URL=/cdn-cgi/" in head.get("Refresh", "") and head.get("Server", "") == "cloudflare-nginx" ):
        return True
    return False
    
def showInfo(sTitle, sDescription, iSeconds=0):
    if (iSeconds == 0):
        iSeconds = 1000
    else:
        iSeconds = iSeconds * 1000
    xbmc.executebuiltin("Notification(%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds))

class NoRedirection(urllib2.HTTPErrorProcessor):    
    def http_response(self, request, response):
        return response

class CloudflareBypass(object):

    def __init__(self):
        self.state = False
        self.HttpReponse = None
                       
    def DeleteCookie(self,Domain):
        xbmc.log('Effacement cookies')
        file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        os.remove(os.path.join(PathCache,file))
        
    def SaveCookie(self,Domain,data):
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

        #save it
        file = open(Name,'w')
        file.write(data)

        file.close()
        
    def Readcookie(self,Domain):
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        
        try:
            file = open(Name,'r')
            data = file.read()
            file.close()
        except:
            return ''
        
        return data
    
    #Return param for head
    def GetHeadercookie(self,url):
        #urllib.quote_plus()
        Domain = re.sub(r'https*:\/\/([^/]+)(\/*.*)','\\1',url)
        cook = self.Readcookie(Domain.replace('.','_'))
        if cook == '':
            return ''
            
        return '|' + urllib.urlencode({'User-Agent':UA,'Cookie': cook })
    
    def SetHeader(self):
        head=[]
        head.append(('User-Agent', UA))
        head.append(('Host' , self.host))
        head.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
        head.append(('Referer', self.url))
        head.append(('Content-Type', 'text/html; charset=utf-8'))
        return head
          
    def GetResponse(self,htmlcontent):
        #line1 = re.findall('var t,r,a,f, (.+?)={"(.+?)":\+*(.+?)};',htmlcontent)
        line1 = re.findall('var s,t,o,p,b,r,e,a,k,i,n,g,f, (.+?)={"(.+?)":\+*(.+?)};',htmlcontent)

        varname = line1[0][0] + '.' + line1[0][1]
        calcul = int(parseInt(line1[0][2]))
        
        AllLines = re.findall(';' + varname + '([*\-+])=([^;]+)',htmlcontent)
        
        for aEntry in AllLines:
            calcul = eval( str(calcul) + str(aEntry[0]) + str(parseInt(aEntry[1])))

        rep = calcul + len(self.host)
        
        return str(rep)
    
    def GetReponseInfo(self):
        return self.HttpReponse.geturl(), self.HttpReponse.headers
        
    def GetHtml(self,url,htmlcontent = '',cookies = '',postdata = ''):
        
        self.hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',url)
        self.host = re.sub(r'https*:\/\/','',self.hostComplet)
        self.url = url
                       
        cookieMem = self.Readcookie(self.host.replace('.','_'))
        if not (cookieMem == ''):
            
            cookies = cookieMem
            xbmc.log('cookies present')
            
            #Test PRIORITAIRE
            opener = urllib2.build_opener(NoRedirection)
            opener.addheaders = self.SetHeader()
                      
            #Add saved cookies
            opener.addheaders.append (('Cookie', cookies))
            
            self.HttpReponse = opener.open(url,postdata)
            htmlcontent = self.HttpReponse.read()
            head = self.HttpReponse.headers
            
            if not CheckIfActive(htmlcontent):
                # ok no more protection
                self.HttpReponse.close()
                return htmlcontent
            
            self.HttpReponse.close()
            
            #Arf, problem, cookies not working, delete them
            xbmc.log('Cookies Out of date')
            self.DeleteCookie(self.host.replace('.','_'))
            
            #Get the first new cookie, we already have the new html code
            cookies = ''
            if 'Set-Cookie' in head:
                cookies = head['Set-Cookie']
                cookies = cookies.split(';')[0]
        
        
        #if we need a first load
        if (htmlcontent == '') or (cookies == ''):

            opener = urllib2.build_opener(NoRedirection)
            opener.addheaders = self.SetHeader()
           
            self.HttpReponse = opener.open(url,postdata)
            
            #code
            htmlcontent = self.HttpReponse.read()
            
            #fh = open('c:\\test.txt', "r")
            #htmlcontent = fh.read()
            #fh.close()
            
            #if no protection
            head = self.HttpReponse.headers
            if not CheckIfActive(htmlcontent):
                return htmlcontent
            
            xbmc.log("Page protegée, tout a charger")
            #cookie
            head = self.HttpReponse.headers
            if 'Set-Cookie' in head:
                cookies = head['Set-Cookie']
                cookies = cookies.split(';')[0]
            
            self.HttpReponse.close()
        
        #2 eme etape recuperation cookies
        hash = re.findall('<input type="hidden" name="jschl_vc" value="(.+?)"\/>',htmlcontent)[0]
        passe = re.findall('<input type="hidden" name="pass" value="(.+?)"\/>',htmlcontent)[0]

        #calcul de la reponse
        rep = self.GetResponse(htmlcontent)

        #Temporisation
        showInfo("Information", 'Decodage protection CloudFlare' , 5)
        xbmc.sleep(4000)
        
        NewUrl = self.hostComplet + '/cdn-cgi/l/chk_jschl?jschl_vc='+ urllib.quote_plus(hash) +'&pass=' + urllib.quote_plus(passe) + '&jschl_answer=' + rep
        
        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = self.SetHeader()
        
        #Add first cookie
        if not cookies == '':
            opener.addheaders.append(('Cookie', cookies))

        self.HttpReponse = opener.open(NewUrl,postdata)

        if 'Set-Cookie' in self.HttpReponse.headers:
            cookies2 = str(self.HttpReponse.headers.get('Set-Cookie'))
            c1 = re.findall('__cfduid=(.+?);',cookies2)
            c2 = re.findall('cf_clearance=(.+?);',cookies2)
            
            #If we have only cf_clearance, it's still ok, it s the more important
            if c2 and not c1:
                c1 = re.findall('__cfduid=([0-9a-z]+)',cookies)
            
            if not c1 or not c2:
                xbmc.log("Probleme protection Cloudflare : Decodage rate")
                showInfo("Erreur", 'Probleme protection CloudFlare' , 5)
                self.HttpReponse.close()
                return ''
                
            cookies = '__cfduid=' + c1[0] + '; cf_clearance=' + c2[0]

        else:
            xbmc.log("Probleme protection Cloudflare : Cookies manquants")
            showInfo("Erreur", 'Probleme protection CloudFlare' , 5)
            self.HttpReponse.close()
            return ''
        
        self.HttpReponse.close()
        
        #Memorisation
        self.SaveCookie(self.host.replace('.','_'),cookies)


        #3 eme etape : on refait la requete mais avec les nouveaux cookies       
        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = self.SetHeader()
        
        #Add the two cookies
        opener.addheaders.append (('Cookie', cookies))
        
        self.HttpReponse = opener.open(url,postdata)
        htmlcontent = self.HttpReponse.read()
        head = self.HttpReponse.headers
        if CheckIfActive(htmlcontent):
            #Arf new cookie not working
            xbmc.log("New cookie not working")
            #self.DeleteCookie(self.host.replace('.','_'))
            self.HttpReponse.close()
            return ''
            
        self.HttpReponse.close()

        return htmlcontent
