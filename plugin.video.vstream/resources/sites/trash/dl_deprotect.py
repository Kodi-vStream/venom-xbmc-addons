#-*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from time import time
from socket import timeout
import base64
import urllib2,urllib,re

import xbmc,xbmcgui

import xbmc

import xbmcaddon,os
PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))

#-----------------------------------------------------------
#Partie veant de PYLOAD https://github.com/pyload
#Non utlise encore

# Information decoding
# For test purposes
def info_decode(i):
    # Remove end string
    assert i.endswith("_%3D")
    i = i[0:-4]
    # Invert string
    i = i[::-1]
    # Base 64 decode
    i = base64.b64decode(i)
    # Split information
    infos = i.split('|')
    assert(len(infos) == 4)
    res = infos[0]
    user_agent = infos[1]
    plugins = [x.split(';') for x in infos[2].split('&')]
    java = {"ENABLE": True, "DISABLE":False}[infos[3]]
    # Return information
    return {'res':res,
            'user_agent':user_agent,
            'plugins':plugins,
            'java':java}

# Information encoding
def info_encode(info):
    # Pack information
    res = info['res']
    user_agent = info['user_agent']
    plugins = '&'.join(';'.join(x) for x in info['plugins'])
    java = {True:"ENABLE", False:"DISABLE"}[info['java']]
    i = '|'.join([res, user_agent, plugins, java])
    # Base 64 encode
    i = base64.b64encode(i)
    # Invert string
    i = i[::-1]
    # Add end string and return
    i = i + "_%3D"
    return i

# Sample configuration
def conf():
    useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'
    conf = {'res': '1280x611x24',
            'java': True,
            'user_agent': useragent,
            'plugins': [['Adobe Acrobat', 'nppdf32.dll', 'Adobe PDF Plug-In For Firefox and Netscape 11.0.13', '11.0.13.17'],
                        ['Adobe Acrobat', 'nppdf32.dll', 'Adobe PDF Plug-In For Firefox and Netscape 11.0.13', '11.0.13.17'],
                        ['Java(TM) Platform SE 8 U51', 'npjp2.dll', 'Next Generation Java Plug-in 11.51.2 for Mozilla browsers', '11.51.2.16'],
                        ['Shockwave Flash', 'NPSWF32_19_0_0_226.dll', 'Shockwave Flash 19.0 r0', '19.0.0.226']]}
    return conf


 #-----------------------------------------------------------------   
    
def get_response(img,cookie):    
    
    #on telecharge l'image
    filename  = os.path.join(PathCache,'Captcha.png')

    headers2 = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
        #'Referer' : url ,
        'Host' : 'www.dl-protect.com',
        'Accept' : 'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'en-gb, en;q=0.9',
        'Accept-Encoding' : 'gzip, deflate',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Cookie' : cookie
        }
        
    try:
        req = urllib2.Request(img,None,headers2)
        image_on_web = urllib2.urlopen(req)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            downloaded_image = file(filename, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return ''
    except:
        return ''

    #on affiche le dialogue
    solution = ''
    try:
        img = xbmcgui.ControlImage(450, 0, 400, 130, filename)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        #xbmc.sleep(3000)
        kb = xbmc.Keyboard('', 'Tapez les Lettres/chiffres de l\'image', False)
        kb.doModal()
        if (kb.isConfirmed()):
            solution = kb.getText()
            if solution == '':
                cGui().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
        else:
            cGui().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
    finally:
        wdlg.removeControl(img)
        wdlg.close()
        
    return solution

def DecryptDlProtect(url):

    if not (url): return ''

    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Referer' : url ,
    'Host' : 'www.dl-protect.com',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-gb, en;q=0.9',
    #'Pragma' : '',
    #'Accept-Charset' : '',
    'Content-Type' : 'application/x-www-form-urlencoded',
    }
    
    request = urllib2.Request(url,None,headers)
    try: 
        reponse = urllib2.urlopen(request,timeout = 5)
    except urllib2.URLError, e:
        cGui().showInfo("Erreur", 'Site Dl-Protect HS' , 5)
        print e.read()
        print e.reason
        return ''
    except urllib2.HTTPError, e:
        cGui().showInfo("Erreur", 'Site Dl-Protect HS' , 5)
        print e.read()
        print e.reason
        return ''
    except timeout:
        print 'timeout'
        cGui().showInfo("Erreur", 'Site Dl-Protect HS' , 5)
        return ''
    
    #Si redirection
    UrlRedirect = reponse.geturl()
    if not(UrlRedirect == url):
        reponse.close()
        return UrlRedirect
        
    sHtmlContent = reponse.read()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
        
    #site out ?
    if 'A technical problem occurred' in sHtmlContent:
        print 'Dl-protect HS'
        cGui().showInfo("Erreur", 'Site Dl-Protect HS' , 5)
        return ''
        
    #lien HS ?
    if 'the link you are looking for is not found' in sHtmlContent:
        print 'lien Dl-protect HS'
        cGui().showInfo("Erreur", 'Lien non disponible' , 5)
        return ''
    
    #Recuperatioen et traitement cookies ???
    cookies=reponse.info()['Set-Cookie']
    #print cookies
    c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',cookies)

    if not c2:
        print 'Probleme de cookies'
        return ''
    cookies = ''
    for cook in c2:
        cookies = cookies + cook[0] + '=' + cook[1]+ ';'
        
    #print cookies

    reponse.close()
    
    #Quel captcha est utilise ?
    #Google re captcha ?
    r = re.search('data-sitekey="([^"]+)', sHtmlContent)
    if r:
        import cookielib
        import recaptcha
        cookieJar = cookielib.LWPCookieJar()
        recaptcha.performCaptcha(url,cookieJar)
        return ''
    #captcha classique
    elif '<td align=center> Please enter the characters from the picture to see the links </td>' in sHtmlContent:
        return ClassicCaptcha(sHtmlContent,cookies,url,headers)
    
    #Pas de cpatcha, juste le boutton.
    if 'Please click on continue to see' in sHtmlContent:
        
        key = re.findall('input name="key" value="(.+?)"',sHtmlContent)
    
        #Ce parametre ne sert pas encore pour le moment
        mstime = int(round(time() * 1000))
        b64time = "_" + base64.urlsafe_b64encode(str(mstime)).replace("=", "%3D")
              
        #tempo necessaire
        cGui().showInfo("Patientez", 'Decodage en cours' , 2)
        xbmc.sleep(1000)
        
        query_args = ( ('submitform' , '' ) , ( 'key' , key[0] ) , ('i' , b64time ), ( 'submitform' , 'Continue')  )
        data = urllib.urlencode(query_args)
        
        #rajout des cookies
        headers.update({'Cookie': cookies})

        request = urllib2.Request(url,data,headers)

        try: 
            reponse = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
            
        sHtmlContent = reponse.read()
        
        reponse.close()
    
        return sHtmlContent
        
    return ''
 
def ClassicCaptcha(sHtmlContent,cookies,url,headers):

        s = re.findall('<img id="captcha" alt="Security code" src="([^<>"]+?)"',sHtmlContent)
        
        if 'http://www.dl-protect.com' in s[0]:
            image = s[0]
        else:
            image = 'http://www.dl-protect.com' + s[0]
        
        #print image
        
        captcha = get_response(image,cookies)
        
        key = re.findall('name="key" value="(.+?)"',sHtmlContent)
        
        #Ce parametre ne sert pas encore
        mstime = int(round(time() * 1000))
        b64time = "_" + base64.urlsafe_b64encode(str(mstime)).replace("=", "%3D")
        
        #test = info_encode(conf())
        #b64time = test.replace("%3D","=")
        
        query_args = ( ('key' , key[0] ) , ( 'i' , b64time) , ('secure' , captcha ), ('submitform','') , ( 'submitform' , 'Decrypt link')  )
        
        data = urllib.urlencode(query_args)
    
        #rajout des cookies
        headers.update({'Cookie': cookies})

        request = urllib2.Request(url,data,headers)

        try: 
            reponse = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
            
        sHtmlContent = reponse.read()
        reponse.close()
        
        if '<td align=center> Please enter the characters from the picture to see the links </td>' in sHtmlContent:
            cGui().showInfo("Erreur", 'Mauvais Captcha' , 5)
            return 'rate'
        
        return sHtmlContent

        
