#-*- coding: utf-8 -*-
#
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
import re,os
import urllib2,urllib
import xbmc

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

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

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
    
    
class NoRedirection(urllib2.HTTPErrorProcessor):    
    def http_response(self, request, response):
        return response

class CloudflareBypass(object):

    def __init__(self):
        self.state = False
                       
    def DeleteCookie(self,Domain):
        PathCache = cConfig().getSettingCache()
        file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        os.remove(os.path.join(PathCache,file))
        
    def SaveCookie(self,Domain,data):
        PathCache = cConfig().getSettingCache()
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

        #save it
        file = open(Name,'w')
        file.write(data)

        file.close()
        
    def Readcookie(self,Domain):
        PathCache = cConfig().getSettingCache()
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


  
    def check(self,head):
        #if 'Checking your browser before accessing' in htmlcontent:
        if ( "URL=/cdn-cgi/" in head.get("Refresh", "") and head.get("Server", "") == "cloudflare-nginx" ):
            self.state = True
            return True
        return False
    
    def SetHeader(self):
        head=[]
        head.append(('User-Agent', UA))
        head.append(('Host' , self.host))
        head.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
        head.append(('Referer', self.url))
        head.append(('Content-Type', 'text/html; charset=utf-8'))
        return head
          
    def GetResponse(self,htmlcontent):
        line1 = re.findall('var t,r,a,f, (.+?)={"(.+?)":\+*(.+?)};',htmlcontent)

        varname = line1[0][0] + '.' + line1[0][1]
        calcul = int(parseInt(line1[0][2]))
        
        AllLines = re.findall(';' + varname + '([*\-+])=([^;]+)',htmlcontent)
        
        for aEntry in AllLines:
            calcul = eval( str(calcul) + str(aEntry[0]) + str(parseInt(aEntry[1])))

        rep = calcul + len(self.host)
        
        return str(rep)
        
        
    def GetHtml(self,url,htmlcontent = '',cookies = ''):
        
        self.hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',url)
        self.host = re.sub(r'https*:\/\/','',self.hostComplet)
        self.url = url
                       
        cookieMem = self.Readcookie(self.host.replace('.','_'))
        if not (cookieMem == ''):
            cookies = cookieMem
            print 'cookies present'
            
            #Test PRIORITAIRE
            opener = urllib2.build_opener(NoRedirection)
            opener.addheaders = self.SetHeader()
                      
            #Add saved cookies
            opener.addheaders.append (('Cookie', cookies))
            
            response = opener.open(url)
            htmlcontent = response.read()
            head = response.headers
            if not self.check(head):
                # ok no more protection
                response.close()
                return htmlcontent
            
            response.close()
            
            #Arf, problem, cookies not working, delete them
            print "Cookies Out of date"
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
           
            response = opener.open(url)
            
            #code
            htmlcontent = response.read()
            #fh = open('c:\\test.txt', "r")
            #htmlcontent = fh.read()
            #fh.close()
            
            #if no protection
            head = response.headers
            if not self.check(head):
                return htmlcontent
            
            print "Page protegée, tout a charger"
            #cookie
            head = response.headers
            if 'Set-Cookie' in head:
                cookies = head['Set-Cookie']
                cookies = cookies.split(';')[0]
            
            response.close()
        
        #2 eme etape recuperation cookies
        hash = re.findall('<input type="hidden" name="jschl_vc" value="(.+?)"\/>',htmlcontent)[0]
        passe = re.findall('<input type="hidden" name="pass" value="(.+?)"\/>',htmlcontent)[0]

        #calcul de la reponse
        rep = self.GetResponse(htmlcontent)

        #Temporisation
        cGui().showInfo("Information", 'Decodage protection CloudFlare' , 5)
        xbmc.sleep(4000)
        
        NewUrl = self.hostComplet + '/cdn-cgi/l/chk_jschl?jschl_vc='+ urllib.quote_plus(hash) +'&pass=' + urllib.quote_plus(passe) + '&jschl_answer=' + rep
        
        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = self.SetHeader()
        
        #Add first cookie
        if not cookies == '':
            opener.addheaders.append(('Cookie', cookies))
        
        response = opener.open(NewUrl)

        if 'Set-Cookie' in response.headers:
            cookies2 = str(response.headers.get('Set-Cookie'))
            c1 = re.findall('__cfduid=(.+?);',cookies2)
            c2 = re.findall('cf_clearance=(.+?);',cookies2)
            
            #If we have only cf_clearance, it's still ok, it s the more important
            if c2 and not c1:
                c1 = re.findall('__cfduid=([0-9a-z]+)',cookies)
            
            if not c1 or not c2:
                print "Probleme protection Cloudflare : Decodage rate"
                cGui().showInfo("Erreur", 'Probleme protection CloudFlare' , 5)
                response.close()
                return ''
                
            cookies = '__cfduid=' + c1[0] + '; cf_clearance=' + c2[0]

        else:
            print "Probleme protection Cloudflare : Cookies manquants"
            cGui().showInfo("Erreur", 'Probleme protection CloudFlare' , 5)
            response.close()
            return ''
        
        response.close()
        
        #Memorisation
        self.SaveCookie(self.host.replace('.','_'),cookies)


        #3 eme etape : on refait la requete mais avec les nouveaux cookies       
        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = self.SetHeader()
        
        #Add the two cookies
        opener.addheaders.append (('Cookie', cookies))
        
        response = opener.open(url)
        htmlcontent = response.read()
        head = response.headers
        if self.check(head):
            #Arf new cookie not working
            print "New cookie not working"
            #self.DeleteCookie(self.host.replace('.','_'))
            response.close()
            return ''
            
        response.close()

        return htmlcontent
