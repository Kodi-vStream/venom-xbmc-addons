#-*- coding: utf-8 -*-
#johngf - V0.2
from resources.lib.gui.hoster import cHosterGui 
from resources.lib.handler.hosterHandler import cHosterHandler 
from resources.lib.gui.gui import cGui 
from resources.lib.gui.guiElement import cGuiElement 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.lib.parser import cParser 
from resources.lib.util import cUtil

import xbmc,urllib,urllib2

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = { 'User-Agent' : UA }

SITE_IDENTIFIER = 'siteuptobox' 
SITE_NAME = '[COLOR red]' + 'ComptePremiumUptobox.com' + '[/COLOR]'
SITE_DESC = 'fichier sur compte uptobox' 

def load(): 
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'getPremiumUser', 'MesFichiers', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
    oGui.addDir(SITE_IDENTIFIER, 'getPremiumUser', 'MesDossiers', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
    
def getPremiumUser():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    post_data = {}
    url = 'https://login.uptobox.com/logarithme'
    post_data['op'] = 'login'
    post_data['login'] = 'ton id' #ton identifiant ici entre les ''
    post_data['password'] = 'ton pass' #ton pass ici entre les ''
    request = urllib2.Request(url, urllib.urlencode(post_data), headers)
    response = urllib2.urlopen(request)
    head = response.headers
    response.close()
    
    cookies = ''
    if 'Set-Cookie' in head:
        oParser = cParser()
        sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
        aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
        if (aResult[0] == True):
            for cook in aResult[1]:
                cookies = cookies + cook[0] + '=' + cook[1]+ ';'
                
    url2 = 'https://uptobox.com/?op=my_files'            
    req = urllib2.Request(url2, None, headers)  
    req.add_header('Cookie', cookies)

    try:
       response = urllib2.urlopen(req)
    except urllib2.URLError, e:
            print e.code
            print e.reason
            return ''

        
    sHtmlContent = response.read()
    response.close()
    if 'Dossier' in sUrl:
        showfolder(sHtmlContent,cookies)
    else:
        showlink(sHtmlContent)
    
def showlink(sHtmlContent):
    oGui = cGui()

    oParser = cParser()
    sPattern = '<td><a href="([^"]+)" class=".+?">([^<]+)<\/a><\/td><td>(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1] + ' ' + '[' + aEntry[2] + ']'
            sHosterUrl = aEntry[0]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = cUtil().DecoTitle(sTitle)
        
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl,'')
                
        cConfig().finishDialog(dialog)
        
    oGui.setEndOfDirectory()

def showfolder(sHtmlContent,cookies):
    oGui = cGui()

    oParser = cParser()
    sPattern = '<td class="tri">.+?<a href="([^"]+)" class="blue_link">(.+?)<\/a><\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl = aEntry[0]
            if not sUrl.startswith('https'):
               sUrl = 'https://uptobox.com/' + sUrl
               
            sDisplayTitle = cUtil().DecoTitle(sTitle)  
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('cookie', cookies)
            oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'genres.png', oOutputParameterHandler)
                
        cConfig().finishDialog(dialog)
        
    oGui.setEndOfDirectory()
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCookie = oInputParameterHandler.getValue('cookie')
    
    req = urllib2.Request(sUrl, None, headers)               
    req.add_header('Cookie', sCookie)
    try:
       response = urllib2.urlopen(req)
    except urllib2.URLError, e:
            print e.code
            print e.reason
            return ''
    
    sHtmlContent = response.read()
    response.close()
    
    oParser = cParser()
    sPattern = '<td><a href="([^"]+)" class=".+?">([^<]+)<\/a><\/td><td>(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1] + ' ' + '[' + aEntry[2] + ']'
            sHosterUrl = aEntry[0]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = cUtil().DecoTitle(sTitle)
        
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl,'')
                
        cConfig().finishDialog(dialog)
        
    oGui.setEndOfDirectory()
