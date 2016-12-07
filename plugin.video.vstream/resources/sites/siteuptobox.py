#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#johngf - V0.4b
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.parser import cParser 
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import xbmc,xbmcgui,urllib,urllib2,re
from resources.lib.handler.premiumHandler import cPremiumHandler
import random, mimetypes, string
SITE_IDENTIFIER = 'siteuptobox' 
SITE_NAME = '[COLOR dodgerblue]' + 'VotreCompteUptobox' + '[/COLOR]'
SITE_DESC = 'fichier sur compte uptobox'
URL_MAIN = 'https://uptobox.com/'
BURL = 'https://uptobox.com/?op=my_files' 
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = { 'User-Agent' : UA }

def load(): 
    oGui = cGui()
    oPremiumHandler = cPremiumHandler('uptobox')
    
    if (cConfig().getSetting('hoster_uptobox_username') == '') and (cConfig().getSetting('hoster_uptobox_password') == ''):
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]'+ 'Nécessite Un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
    else:
        if (oPremiumHandler.Readcookie('uptobox') != ''):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'MesFichiers', 'genres.png', oOutputParameterHandler)
    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
            oGui.addDir(SITE_IDENTIFIER, 'showFolder', 'MesDossiers', 'genres.png', oOutputParameterHandler)
        else:
            Connection = oPremiumHandler.Authentificate()
            if (Connection == False):
                xbmcgui.Dialog().notification('Info connexion', 'Connexion refusé', xbmcgui.NOTIFICATION_ERROR,2000,False)
                return
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'MesFichiers', 'genres.png', oOutputParameterHandler)
    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
            oGui.addDir(SITE_IDENTIFIER, 'showFolder', 'MesDossiers', 'genres.png', oOutputParameterHandler)    
     

    oGui.setEndOfDirectory()
    
def showFile():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oPremiumHandler = cPremiumHandler('uptobox')

    if 'uptobox.com' in sUrl:
        sHtmlContent = oPremiumHandler.GetHtml(sUrl)
    else:    
        sHtmlContent = oPremiumHandler.GetHtml(BURL)

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
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl,'')
                
        cConfig().finishDialog(dialog)
        
    oGui.setEndOfDirectory()

def showFolder():
    oGui = cGui()
    oPremiumHandler = cPremiumHandler('uptobox')

    sHtmlContent = oPremiumHandler.GetHtml(BURL)
    
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
            oGui.addDir(SITE_IDENTIFIER, 'showFile', sDisplayTitle, 'genres.png', oOutputParameterHandler)
                
        cConfig().finishDialog(dialog)
        
    oGui.setEndOfDirectory()
       
def AddmyAccount():
    if (cConfig().getSetting('hoster_uptobox_username') == '') and (cConfig().getSetting('hoster_uptobox_password') == ''):
        return 
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
    # on récupère l'id
    sId = sMediaUrl.replace('https://uptobox.com/','')
    sId = sMediaUrl.replace('http://uptobox.com/','')
    #go page            
    Upurl = 'https://uptobox.com/?op=my_files&add_my_acc=' + sId

    oPremiumHandler = cPremiumHandler('uptobox')
    if (oPremiumHandler.Readcookie('uptobox') != ''):
        #xbmc.log('cookie trouvé')
        cookies = oPremiumHandler.Readcookie('uptobox')
        sHtmlContent = oPremiumHandler.GetHtmlwithcookies(Upurl,None,cookies)
        if (len(sHtmlContent) > 25):
            #xbmc.log('mais il a expiré')
            oPremiumHandler.Authentificate()
            cookies = oPremiumHandler.Readcookie('uptobox')
            sHtmlContent = oPremiumHandler.GetHtmlwithcookies(Upurl,None,cookies)
            #xbmc.log('nouveau cookie')
    else:
        #xbmc.log('aucun cookie')
        sHtmlContent = oPremiumHandler.GetHtml(Upurl)
        
    xbmc.executebuiltin("Dialog.Close(all,true)") 
    if ('dded to your account' in sHtmlContent):
         xbmcgui.Dialog().notification('Info upload','Fichier ajouté à votre compte',xbmcgui.NOTIFICATION_INFO,2000,False)      
    elif ('nvalid file' in sHtmlContent):
         xbmcgui.Dialog().notification('Info upload','Fichier introuvable',xbmcgui.NOTIFICATION_INFO,2000,False)
    else:
         xbmcgui.Dialog().notification('Info upload','Erreur',xbmcgui.NOTIFICATION_ERROR,2000,False)    

def UptomyAccount():
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
    #xbmc.log(str(sMediaUrl))
    oPremiumHandler = cPremiumHandler('uptobox')
    #go page d'accueil           
    sHtmlContent = oPremiumHandler.GetHtml(URL_MAIN)
    cookies = oPremiumHandler.Readcookie('uptobox')
  
    aResult = re.search('<div id="div_url".+?action="([^"]+)".+?name="sess_id" value="([^"]+)".+?name="srv_tmp_url" value="([^"]+)"',sHtmlContent,re.DOTALL)
    if (aResult):
        aCt = aResult.group(1)
        sId = aResult.group(2)
        sTmp = aResult.group(3)
 
        UPurl = ('%s%s&js_on=1&utype=reg&upload_type=url' % (aCt,sId))
 
        fields = {'sess_id':sId,'upload_type':'url','srv_tmp_url':sTmp,'url_mass':sMediaUrl,'tos':'1','submit_btn':'Uploader'}
        mpartdata = MPencode(fields)
        req = urllib2.Request(UPurl,mpartdata[1],headers)
        req.add_header('Content-Type', mpartdata[0])
        req.add_header('Cookie', cookies)
        req.add_header('Content-Length', len(mpartdata[1]))
        #req.add_data(mpartdata[1])
        #xbmc.log(str(mpartdata[1]))
        try:
           rep = urllib2.urlopen(req)
        except:
            return ''

        sHtmlContent = rep.read()
        rep.close()
    
        if '>OK<' in sHtmlContent:
           xbmcgui.Dialog().notification('Info upload', 'Upload réussie', xbmcgui.NOTIFICATION_INFO,2000,False)
        else:
           xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO,2000,False)
    else:
        xbmcgui.Dialog().notification('Info upload','Erreur pattern',xbmcgui.NOTIFICATION_ERROR,2000,False)
        

def MPencode(fields):
	random_boundary = __randy_boundary()
	content_type = "multipart/form-data, boundary=%s" % random_boundary

	form_data = []
	
	if fields:
		for (key, value) in fields.iteritems():
			if not hasattr(value, 'read'):
				itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (random_boundary, key, value)
				form_data.append(itemstr)
			elif hasattr(value, 'read'):
				with value:
					file_mimetype = mimetypes.guess_type(value.name)[0] if mimetypes.guess_type(value.name)[0] else 'application/octet-stream'
					itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n%s\r\n' % (random_boundary, key, value.name, file_mimetype, value.read())
				form_data.append(itemstr)
			else:
				raise Exception(value, 'Field is neither a file handle or any other decodable type.')
	else:
		pass

	form_data.append('--%s--\r\n' % random_boundary)

	return content_type, ''.join(form_data)

def __randy_boundary(length=10,reshuffle=False):
	character_string = string.letters+string.digits
	boundary_string = []
	for i in range(0,length):
		rand_index = random.randint(0,len(character_string) - 1)
		boundary_string.append(character_string[rand_index])
	if reshuffle:
		random.shuffle(boundary_string)
	else:
		pass
	return ''.join(boundary_string)        
        
 
