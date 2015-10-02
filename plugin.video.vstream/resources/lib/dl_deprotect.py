#-*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from time import time
from base64 import urlsafe_b64encode
import urllib2,xbmc,urllib,re
from urllib2 import URLError



#Cette fonction n'est pas encore utilisée, servira le jour ou dl-protect re-activera le captcha
# def get_response(img):
    # try:
        # img = xbmcgui.ControlImage(450, 0, 400, 130, img)
        # wdlg = xbmcgui.WindowDialog()
        # wdlg.addControl(img)
        # wdlg.show()
        # #xbmc.sleep(3000)
        # kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        # kb.doModal()
        # if (kb.isConfirmed()):
            # solution = kb.getText()
            # if solution == '':
                # raise Exception('You must enter text in the image to access video')
            # else:
                # return solution
        # else:
            # raise Exception('Captcha Error')
    # finally:
        # wdlg.close()


def DecryptDlProtect(url):
    if not (url): return ''
    
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Referer' : url ,
    'Host' : 'www.dl-protect.com',
    #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-gb, en;q=0.9',
    'Pragma' : '',
    'Accept-Charset' : '',
    }
    
    request = urllib2.Request(url,None,headers)
    try: 
        reponse = urllib2.urlopen(request)
    except URLError, e:
        print e.read()
        print e.reason
        
    sHtmlContent = reponse.read()
    
    #Recuperatioen et traitement cookies ???
    cookies=reponse.info()['Set-Cookie']
    c2 = re.findall('__cfduid=(.+?); .+? cu=(.+?);.+?PHPSESSID=(.+?);',cookies)
    cookies = '__cfduid=' + str(c2[0][0]) + ';cu=' + str(c2[0][1]) + ';PHPSESSID=' + str(c2[0][2])
    
    reponse.close()
        
    key = re.findall('input name="key" value="(.+?)"',sHtmlContent)
    
    #Ce parametre ne sert pas encore pour le moment
    mstime = int(round(time() * 1000))
    b64time = "_" + urlsafe_b64encode(str(mstime)).replace("=", "%3D")

    if 'Please click on continue to see' in sHtmlContent:
        #tempo necessaire
        cGui().showInfo("Patientez", 'Decodage en cours' , 2)
        xbmc.sleep(1000)
        
        query_args = ( ('submitform' , '' ) , ( 'key' , key[0] ) , ('i' , b64time ), ( 'submitform' , 'Continuer')  )
        data = urllib.urlencode(query_args)
        
        #rajout des cookies
        headers.update({'Cookie': cookies})

        request = urllib2.Request(url,data,headers)

        try: 
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
            
        sHtmlContent = reponse.read()
        
        reponse.close()
    
    return sHtmlContent
        
 
