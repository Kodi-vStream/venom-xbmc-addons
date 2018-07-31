#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.config import GestionCookie
from resources.lib.comaddon import progress, dialog, addon
import xbmc,xbmcgui

sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'siteonefichier'
SITE_NAME = "[COLOR %s]%s[/COLOR] [COLOR %s](%s)[/COLOR]" % ("dodgerblue", "VotreCompte1fichier", sColor, "beta")

SITE_DESC = 'Fichiers sur compte 1Fichier'
URL_MAIN = 'https://1fichier.com/'
URL_FILE = URL_MAIN + 'console/files.pl'
URL_REMOTE = URL_MAIN + 'console/remote.pl'

def load():
    addons = addon()

    if (addons.getSetting('hoster_onefichier_username') == '') and (addons.getSetting('hoster_onefichier_password') == ''):
        oGui = cGui()
        oGui.addText(SITE_IDENTIFIER, "[COLOR %s]%s[/COLOR]" % ("red", "Nécessite Un Compte 1Fichier Premium ou Gratuit"))
        oGui.setEndOfDirectory()
    else:
        if (GestionCookie().Readcookie('onefichier') != ''):
            showFile(URL_FILE)

        else:
            oPremiumHandler = cPremiumHandler('onefichier')
            Connection = oPremiumHandler.Authentificate()
            if (Connection == False):
                oGui = cGui()
                oGui.addText(SITE_IDENTIFIER, "[COLOR %s]%s[/COLOR]" % ("red", "Connexion refusée"))
                oGui.setEndOfDirectory()

            else:
                showFile(URL_FILE)


def showFile(sFileTree = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
    if (oInputParameterHandler.exist('siteUrl')):
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    if sFileTree:
        sUrl = sFileTree
        
    oPremiumHandler = cPremiumHandler('onefichier')

    sHtmlContent = oPremiumHandler.GetHtml(sUrl)

    oParser = cParser()
    sPattern = '((?:|directory")) *rel="([^"]+)"><div class="dF"><a href="#" onclick="return false">(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', "%s%s%s%s" % (URL_FILE, "?dir_id=", aEntry[1], '&oby=0&search='))
                oOutputParameterHandler.addParameter('sTitle', aEntry[2])
                oGui.addDir(SITE_IDENTIFIER, 'showFile', aEntry[2], 'genres.png', oOutputParameterHandler)

            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', "%s%s" % (URL_MAIN, "console/link.pl"))
                oOutputParameterHandler.addParameter('sCode', aEntry[1])
                oOutputParameterHandler.addParameter('sTitle', aEntry[2])
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', aEntry[2], 'genres.png', oOutputParameterHandler)


        progress_.VSclose(progress_)


    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sCode = oInputParameterHandler.getValue('sCode')
    
    oPremiumHandler = cPremiumHandler('onefichier')

    sHtmlContent = oPremiumHandler.GetHtml(sUrl,'selected%5B%5D=' + sCode)

    sPattern = '<a href="([^"]+)">(.+?)<\/a><\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHosterUrl = aResult[1][0][0]
        sTitle = aResult[1][0][1]
        
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


def UptomyAccount():
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

    oPremiumHandler = cPremiumHandler('onefichier')
    #requete
    sHtmlContent = oPremiumHandler.GetHtml(URL_REMOTE,"%s%s%s" % ("links=", sMediaUrl, "&did=0"))
    #sleep au cas ou
    xbmc.sleep(2000)
    #on verifie que le liens est dans la liste d'attente
    aResult = oPremiumHandler.GetHtml('%s%s' % (URL_REMOTE,'?c=todo'))
    if (aResult):
        sCheck = aResult.find(sMediaUrl)
        if sCheck != -1:
            #penible ce dialog auth
            xbmc.executebuiltin("Dialog.Close(all,true)")
            xbmcgui.Dialog().notification('Info upload', 'OK', xbmcgui.NOTIFICATION_INFO, 2000, False)
        else:
            #penible ce dialog auth
            xbmc.executebuiltin("Dialog.Close(all,true)")
            xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO, 2000, False)

