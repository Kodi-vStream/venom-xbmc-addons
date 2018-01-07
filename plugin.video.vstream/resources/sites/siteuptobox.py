#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.parser import cParser 
from resources.lib.util import cUtil,VSlog
from resources.lib.config import cConfig
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import MPencode
from resources.lib.config import GestionCookie

import xbmc,xbmcgui,urllib2,re

SITE_IDENTIFIER = 'siteuptobox' 
SITE_NAME = '[COLOR dodgerblue]' + 'VotreCompteUptobox' + '[/COLOR]'
SITE_DESC = 'Fichiers sur compte Uptobox'
URL_MAIN = 'https://uptobox.com/'
BURL = URL_MAIN + '?op=my_files' 
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = { 'User-Agent' : UA }

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
            oOutputParameterHandler.addParameter('file', 'fileonly')
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
            oOutputParameterHandler.addParameter('file', 'fileonly')
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
    
    sFileonly = ''
    if (oInputParameterHandler.exist('file')):
        sFileonly = oInputParameterHandler.getValue('file')

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
            oOutputParameterHandler.addParameter('file', 'fileonly')
            oGui.addNext(SITE_IDENTIFIER, 'showFile', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
            
        if sFileonly != 'fileonly':    
            sFolder = __checkForFolder(sHtmlContent)
            if (sFolder != False):
                for aEntry in sFolder:
                    sUrl = URL_MAIN+aEntry[0]
                    sTitle = aEntry[1]
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('title', sTitle)
                    oGui.addDir(SITE_IDENTIFIER, 'showFile', sTitle, 'genres.png', oOutputParameterHandler)
            
        oGui.setEndOfDirectory()
        
    else:
        showFolder(sHtmlContent)



def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^']+)'>(?:Next|Suivant).+?<\/a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]
 
    return False
    
def __checkForFolder(sHtmlContent):
    sHtmlContent = sHtmlContent.replace('class="blue_link">&nbsp;. .&nbsp; ()</a></td>','')
    sPattern = '<td class="tri">.+?<a href="([^"]+)" class="blue_link">(.+?)<\/a><\/td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1]
        
    return False
    
def showFolder(sHtmlContent=''):
    oGui = cGui()
    oPremiumHandler = cPremiumHandler('uptobox')
    if not sHtmlContent:
        sHtmlContent = oPremiumHandler.GetHtml(BURL)
    else:
        sHtmlContent = sHtmlContent.replace('class="blue_link">&nbsp;. .&nbsp; ()</a></td>','')
        
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

    sId = sMediaUrl.rsplit('/', 1)[1]

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
  
    aResult = re.search("request.open\('POST', '([^']+)'\);",sHtmlContent,re.DOTALL)
    if (aResult):
        UPurl = aResult.group(1)
        fields = {'urls':'["'+sMediaUrl+'"]'}
        mpartdata = MPencode(fields)

        req = urllib2.Request(UPurl,mpartdata[1],headers)
        req.add_header('Content-Type', mpartdata[0].replace(',',';'))
        req.add_header('Cookie', cookies)
        req.add_header('Content-Length', len(mpartdata[1]))

        xbmcgui.Dialog().notification('Info upload', 'Envoi de la requete patienter ..', xbmcgui.NOTIFICATION_INFO,2000,False)
        try:
            rep = urllib2.urlopen(req)
        except urllib2.URLError, e:
            #VSlog(e.code)
            #VSlog(e.reason)
            return ''

        sHtmlContent = rep.read()
        #VSlog(sHtmlContent)
        rep.close()
        xbmc.executebuiltin("Dialog.Close(all,true)")
        if 'success' in sHtmlContent:
           xbmcgui.Dialog().notification('Info upload', 'Upload réussie', xbmcgui.NOTIFICATION_INFO,2000,False)
        else:
           xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO,2000,False)
    else:
        xbmcgui.Dialog().notification('Info upload','Erreur pattern',xbmcgui.NOTIFICATION_ERROR,2000,False)

