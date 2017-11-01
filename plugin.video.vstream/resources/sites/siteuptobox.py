#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#johngf - V0.4.1
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.parser import cParser 
from resources.lib.util import cUtil
from resources.lib.config import cConfig
from resources.lib.handler.premiumHandler import cPremiumHandler

from resources.lib.config import GestionCookie

import xbmc,xbmcgui,urllib,urllib2,re,random,mimetypes,string

SITE_IDENTIFIER = 'siteuptobox' 
SITE_NAME = '[COLOR dodgerblue]' + 'VotreCompteUptobox' + '[/COLOR]'
SITE_DESC = 'Fichiers sur compte Uptobox'
URL_MAIN = 'https://uptobox.com/'
BURL = URL_MAIN + '?op=my_files' 
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = { 'User-Agent' : UA }

URL_UPTOBOX_SEARCH = (URL_MAIN + '?op=my_files&per_page=1000&fld_id=0&key=', 'showMovies')


def load(): 
    oGui = cGui()
    oPremiumHandler = cPremiumHandler('uptobox')
    
    if (cConfig().getSetting('hoster_uptobox_username') == '') and (cConfig().getSetting('hoster_uptobox_password') == ''):
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite Un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
    else:
        if (GestionCookie().Readcookie('uptobox') != ''):
        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers', 'genres.png', oOutputParameterHandler)
    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
            oGui.addDir(SITE_IDENTIFIER, 'showFolder', 'Mes Dossiers', 'genres.png', oOutputParameterHandler)
        else:
            Connection = oPremiumHandler.Authentificate()
            if (Connection == False):
                xbmcgui.Dialog().notification('Info connexion', 'Connexion refusée', xbmcgui.NOTIFICATION_ERROR,2000,False)
                return
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers', 'genres.png', oOutputParameterHandler)
    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
            oGui.addDir(SITE_IDENTIFIER, 'showFolder', 'Mes Dossiers', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_UPTOBOX_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

    
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
    sPattern = '<td><a href="([^"]+)" class=".+?">([^<]+)<\/a>.+?<td>(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1] 
            sHosterUrl = aEntry[0]
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl,'')
                
        cConfig().finishDialog(dialog)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showFile', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^']+)'>(?:Next|Suivant).+?<\/a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]
 
    return False

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
               sUrl = URL_MAIN + sUrl
               
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

    sId = sMediaUrl.replace(URL_MAIN,'')
    if 'https://uptostream.com/iframe/' in sMediaUrl : sId = sMediaUrl.replace('https://uptostream.com/iframe/','') 
    else : sId = sMediaUrl.replace('http://uptobox.com/','') 
          
    Upurl = URL_MAIN + '?op=my_files&add_my_acc=' + sId

    oPremiumHandler = cPremiumHandler('uptobox')
    if (GestionCookie().Readcookie('uptobox') != ''):

        cookies = GestionCookie().Readcookie('uptobox')
        sHtmlContent = oPremiumHandler.GetHtmlwithcookies(Upurl,None,cookies)
        if (len(sHtmlContent) > 25):

            oPremiumHandler.Authentificate()
            cookies = GestionCookie().Readcookie('uptobox')
            sHtmlContent = oPremiumHandler.GetHtmlwithcookies(Upurl,None,cookies)

    else:
        sHtmlContent = oPremiumHandler.GetHtml(Upurl)
        
    xbmc.executebuiltin("Dialog.Close(all,true)") 
    if ('dded to your account' in sHtmlContent):
         xbmcgui.Dialog().notification('Info upload','Fichier ajouté à votre compte',xbmcgui.NOTIFICATION_INFO,2000,False)      
    elif ('nvalid file' in sHtmlContent):
         xbmcgui.Dialog().notification('Info upload','Fichier introuvable',xbmcgui.NOTIFICATION_INFO,2000,False)
    else:
         xbmcgui.Dialog().notification('Info upload','Erreur',xbmcgui.NOTIFICATION_ERROR,2000,False)    

def UptomyAccount():
    if (cConfig().getSetting('hoster_uptobox_username') == '') and (cConfig().getSetting('hoster_uptobox_password') == ''):
        return 
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

    oPremiumHandler = cPremiumHandler('uptobox')
         
    sHtmlContent = oPremiumHandler.GetHtml(URL_MAIN)
    cookies = GestionCookie().Readcookie('uptobox')
  
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
        xbmcgui.Dialog().notification('Info upload', 'Envoi de la requete patienter ..', xbmcgui.NOTIFICATION_INFO,2000,False)
        try:
           rep = urllib2.urlopen(req)
        except:
            return ''

        sHtmlContent = rep.read()
        rep.close()
        xbmc.executebuiltin("Dialog.Close(all,true)")
        if '>OK<' in sHtmlContent:
           xbmcgui.Dialog().notification('Info upload', 'Upload réussie', xbmcgui.NOTIFICATION_INFO,2000,False)
        else:
           xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO,2000,False)
    else:
        xbmcgui.Dialog().notification('Info upload','Erreur pattern',xbmcgui.NOTIFICATION_ERROR,2000,False)

def showMovies(sSearch = ''):
    oGui = cGui()
      
    oInputParameterHandler = cInputParameterHandler()
    sUrl = sSearch
    
    oPremiumHandler = cPremiumHandler('uptobox')

    if 'uptobox.com' in sUrl:
        sHtmlContent = oPremiumHandler.GetHtml(sUrl)
    else:    
        sHtmlContent = oPremiumHandler.GetHtml(BURL)

    oParser = cParser()
    sPattern = '<td><a href="([^"]+)" class=".+?">([^<]+)<\/a>.+?<td>(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1] 
            sHosterUrl = aEntry[0]
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl,'')
                
        cConfig().finishDialog(dialog)
        
            
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^']+)'>(?:Next|Suivant).+?<\/a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]
 
    return False
        
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
