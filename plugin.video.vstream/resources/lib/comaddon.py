# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmcaddon, xbmcgui, xbmc, xbmcplugin, xbmcvfs 
import time
"""System d'importation

from resources.lib.comaddon import addon, dialog, VSlog, xbmcgui, xbmc

"""

"""
from resources.lib.comaddon import addon

addons = addon() en haut de page.

utiliser une fonction comaddon ou xbmcaddon
https://codedocs.xyz/xbmc/xbmc/class_x_b_m_c_addon_1_1xbmcaddon_1_1_addon.html

addons.VSlang(30305)
addons.getLocalizedString(30305)
addons.openSettings()

utiliser la fonction avec un autre addon

addons2 = addon('plugin.video.youtube')
addons2.openSettings()
"""


"""
Ne pas utiliser :
class addon(xbmcaddon.Addon):

L'utilisation de subclass peut provoquer des fuites de mémoire, signalé par ce message :

the python script "\plugin.video.vstream\default.py" has left several classes in memory that we couldn't clean up. The classes include: class XBMCAddon::xbmcaddon::Addon

# https://stackoverflow.com/questions/26588266/xbmc-addon-memory-leak

"""
ADDONVS = xbmcaddon.Addon('plugin.video.vstream')    # singleton

# class addon(xbmcaddon.Addon):
class addon():

     
    def __init__(self, addonId = None):
        self.addonId = addonId

    def openSettings(self):
        return xbmcaddon.Addon(self.addonId).openSettings() if self.addonId else ADDONVS.openSettings()
        
    def getSetting(self, key):
        return xbmcaddon.Addon(self.addonId).getSetting(key) if self.addonId else ADDONVS.getSetting(key)
     
    def setSetting(self, key, value):
        return xbmcaddon.Addon(self.addonId).setSetting(key, value) if self.addonId else ADDONVS.setSetting(key, value)
     
    def getAddonInfo(self, info):
        return xbmcaddon.Addon(self.addonId).getAddonInfo(info) if self.addonId else ADDONVS.getAddonInfo(info)
     
    def VSlang(self, lang):
        return VSPath(xbmcaddon.Addon(self.addonId).getLocalizedString(lang)) if self.addonId else VSPath(ADDONVS.getLocalizedString(lang))
        #Bug avec accent xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getLocalizedString(lang)).decode('utf-8')

"""
from resources.lib.comaddon import dialog

Utilisation :
dialogs = dialog()
dialogs.VSinfo('test')
https://codedocs.xyz/xbmc/xbmc/group__python___dialog.html
"""

DIALOG = xbmcgui.Dialog() # Singleton

class dialog():
# class dialog(xbmcgui.Dialog):

    def VSok(self, desc, title = 'vStream'):
        return DIALOG.ok(title, desc)

    def VSyesno(self, desc, title = 'vStream'):
        return DIALOG.yesno(title, desc)

    def VSselect(self, desc, title = 'vStream'):
        return DIALOG.select(title, desc)

    def numeric(self, dialogType, heading, defaultt):
        return DIALOG.numeric(dialogType, heading, defaultt)

    def VSbrowse(self, type, heading, shares):
        return DIALOG.browse(type, heading, shares)

    def VSselectqual(self, list_qual, list_url):

        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]

        ret = DIALOG.select(addon().VSlang(30448), list_qual)
        if ret > -1:
            return list_url[ret]
        return ''

    def VSinfo(self, desc, title = 'vStream', iseconds = 0, sound = False):
        if (iseconds == 0):
            iseconds = 1000
        else:
            iseconds = iseconds * 1000

        if (addon().getSetting('Block_Noti_sound') == 'true'):
            sound = True

        return DIALOG.notification(str(title), str(desc), xbmcgui.NOTIFICATION_INFO, iseconds, sound)

    def VSerror(self, e):
        return DIALOG.notification('vStream', 'Erreur: ' + str(e), xbmcgui.NOTIFICATION_ERROR, 2000), VSlog('Erreur: ' + str(e))

    def VStextView(self, desc, title = "vStream"):
        return DIALOG.textviewer(title, desc)
    
"""
from resources.lib.comaddon import progress

Utilisation : 
progress_ = progress()
progress_.VScreate(SITE_NAME)
progress_.VSupdate(progress_, total)
if progress_.iscanceled():
    break
progress_.VSclose(progress_)

dialog = progress() non recommandé
progress = progress() non recommandé
https://codedocs.xyz/xbmc/xbmc/group__python___dialog_progress.html
"""

COUNT = 0
PROGRESS = None # Singleton

class empty():

    def VSupdate(self, dialog, total, text = '', search = False):
        pass

    def iscanceled(self):
        pass

    def VSclose(self, dialog):
        pass

#Baser sur UrlResolver
class CountdownDialog(object):
    __INTERVALS = 5

    def __init__(self, heading, line1='', line2='', line3='', active=True, countdown=60, interval=5):
        self.heading = heading
        self.countdown = countdown
        self.interval = interval
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        if active:
            if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
                pd = CustomProgressDialog.ProgressDialog()
            else:
                pd = xbmcgui.DialogProgress()
            if not self.line3:
                line3 = 'Expires in: %s seconds' % countdown
            if not isMatrix():
                pd.create(self.heading, line1, line2, line3)
            else:
                pd.create(self.heading,
                          line1 + '\n'
                          + line2 + '\n'
                          + line3)
            pd.update(100)
            self.pd = pd
        else:
            self.pd = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd

    def start(self, func, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        result = func(*args, **kwargs)
        if result:
            return result

        if self.pd is not None:
            start = time.time()
            expires = time_left = self.countdown
            interval = self.interval
            while time_left > 0:
                for _ in range(CountdownDialog.__INTERVALS):
                    xbmc.sleep(int(interval * 1000 / CountdownDialog.__INTERVALS))
                    if self.is_canceled():
                        return
                    time_left = expires - int(time.time() - start)
                    if time_left < 0:
                        time_left = 0
                    progress = int(time_left * 100 / expires)
                    line3 = 'Expires in: %s seconds' % time_left if not self.line3 else ''
                    self.update(progress, line3=line3)

                result = func(*args, **kwargs)
                if result:
                    return result

    def is_canceled(self):
        if self.pd is None:
            return False
        else:
            return self.pd.iscanceled()

    def update(self, percent, line1='', line2='', line3=''):
        if not line1:
            line1 = self.line1
        if not line2:
            line2 = self.line2
        if not line3:
            line3 = self.line3
        if self.pd is not None:
            if not isMatrix():
                self.pd.update(percent, line1, line2, line3)
            else:
                self.pd.update(percent,
                               line1 + '\n'
                               + line2 + '\n'
                               + line3)

class progress():

    def VScreate(self, title = 'vStream', desc = '', large=False):
        # l'option "large" permet de forcer un sablier large, seul le sablier large peut être annulé.

        # Ne pas afficher le sablier si nous ne sommes pas dans un menu vStream
        currentWindow = xbmcgui.getCurrentWindowId()
        if currentWindow != 10025 and currentWindow != 10028 : # 10025 = videonav, 10000 = home
            return empty()

        # Ne pas afficher le sablier si une dialog est ouverte, inclut le menu contextuel
        # sauf pour le spinner de chargement (10138)
        dlgId = xbmcgui.getCurrentWindowDialogId()
        if dlgId != 9999 and dlgId != 10138: # 9999 = None
            return empty()

#         # Ne pas afficher le sablier si le mode d'affichage est une liste
#         # Ne fonctionne pas car l'info correspond à la fenêtre precedente
#         viewMode = xbmc.getInfoLabel('Container.ViewMode')
#         VSlog('viewMode = '+ viewMode)
#         if 'list' in viewMode or 'List' in viewMode:
#             return empty()

        global PROGRESS
        if PROGRESS == None:
            if large:
                PROGRESS = xbmcgui.DialogProgress()
            elif ADDONVS.getSetting('spinner_small') == 'true':
                PROGRESS = xbmcgui.DialogProgressBG()
            else:
                PROGRESS = xbmcgui.DialogProgress()
            PROGRESS.create(title, desc)

        return self

    def VSupdate(self, dialog, total, text = '', search = False):

        global PROGRESS
        if not PROGRESS:    # Déjà refermé
            return
        
        if not search and window(10101).getProperty('search') == 'true':
            return
        
        global COUNT
        COUNT += 1
        iPercent = int(float(COUNT * 100) / total)
        PROGRESS.update(iPercent, 'Chargement ' + str(COUNT) + '/' + str(total) + " " + text)

    def iscanceled(self):
        global PROGRESS
        if isinstance(PROGRESS, xbmcgui.DialogProgress):
            return PROGRESS.iscanceled()
        return False

    def VSclose(self, dialog = ''):
        global PROGRESS
        if not PROGRESS:
            return      # Déjà fermée

        if window(10101).getProperty('search') == 'true':
            return
        
        if PROGRESS:            # test si pas fermé entre-temps
            dialog = PROGRESS   # Sémaphore pour synchroniser la fermeture
            PROGRESS = None
            dialog.close()

    def getProgress(self):
        return COUNT
    
"""
from resources.lib.comaddon import window

window(10101).getProperty('test')
https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__window.html
"""

class window(xbmcgui.Window):

    def __init__(self, winID):
        pass

"""
from resources.lib.comaddon import listitem
listitem.setLabel('test')
https://kodi.wiki/view/InfoLabels
https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
"""

class listitem(xbmcgui.ListItem):

    #ListItem([label, label2, iconImage, thumbnailImage, path])

    def __init__(self, label = '', label2 = '', iconImage = '', thumbnailImage = '', path = ''):
        pass

    # Permet l'ajout d'un menu après la création d'un item
    def addMenu(self, sFile, sFunction, sTitle, oOutputParameterHandler = False):
        sPluginPath = 'plugin://plugin.video.vstream/' # cPluginHandler().getPluginPath()
        nbContextMenu = self.getProperty('nbcontextmenu')
        nbContextMenu = int(nbContextMenu) if nbContextMenu else 0
        
        sUrl = '%s?site=%s&function=%s' % (sPluginPath, sFile, sFunction)
        if oOutputParameterHandler:
            sUrl += '&%s' % oOutputParameterHandler.getParameterAsUri()
        
        property = 'contextmenulabel(%d)' % nbContextMenu
        self.setProperty(property, sTitle);

        property = 'contextmenuaction(%d)' % nbContextMenu
        self.setProperty(property, 'RunPlugin(%s)' % sUrl);
        
        self.setProperty('nbcontextmenu', str(nbContextMenu+1))

"""
from resources.lib.comaddon import VSlog
VSlog('testtttttttttttt')
"""

#xbmc des fonctions pas des class
def VSlog(e, level = xbmc.LOGDEBUG):
    try:
        #rapelle l'ID de l'addon pour être appelé hors addon
        if (ADDONVS.getSetting('debug') == 'true'):
            if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                level = xbmc.LOGINFO
            else:
                level = xbmc.LOGNOTICE
        xbmc.log('\t[PLUGIN] vStream: ' + str(e), level)
        
    except:
        pass

def VSupdate():
    return xbmc.executebuiltin('Container.Refresh')

def VSshow_busy():
    xbmc.executebuiltin('ActivateWindow(busydialog)')

def VShide_busy():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
        xbmc.sleep(100)

def isKrypton():
    try:
        version = xbmc.getInfoLabel('system.buildversion')
        if version[0:2] >= '17':
            return True
        else:
            return False
    except:
        return False

def isMatrix():
    try:
        version = xbmc.getInfoLabel('system.buildversion')
        if version[0:2] >= '19':
            return True
        else:
            return False
    except:
        return False

def isNexus():
    try:
        version = xbmc.getInfoLabel('system.buildversion')
        if version[0:2] >= '20':
            return True
        else:
            return False
    except:
        return False

#Transforme les "special" en chemin normal.
def VSPath(pathSpecial):
    if isMatrix():
        path = xbmcvfs.translatePath(pathSpecial)
    else:
        path = xbmc.translatePath(pathSpecial)
    return path


class addonManager:

    # Demande l'installation d'un addon
    def installAddon(self, addon_id):
        xbmc.executebuiltin('InstallAddon(%s)' % addon_id, True)

    # Vérifie la présence d'un addon
    def isAddonExists(self, addon_id):
        return xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id) == 0

    # Active/desactive un addon
    def enableAddon(self, addon_id, enable = 'True'):
        import json
        # if enable=='True' and xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id) == 0:
            # VSlog('%s déjà activé'  %addon_id)
            # return True
    
        request = {
            "jsonrpc": "2.0",
            "method": "Addons.SetAddonEnabled",
            "params": {
                "addonid": "%s" % addon_id,
                "enabled": enable == 'True'
            },
            "id": 1
        }
    
        req = json.dumps(request)
        response = xbmc.executeJSONRPC(req)
        response = json.loads(response)
        try:
            VSlog("Activation de " + addon_id)
            VSlog("response = " + str(response))
            return response['result'] == 'OK'
        except KeyError:
            VSlog('enable_addon received an unexpected response - ' + addon_id, xbmc.LOGERROR)
            return False
    
