# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import time
import json
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

"""System d'importation
from resources.lib.comaddon import addon, dialog, VSlog
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
ADDONVS = xbmcaddon.Addon('plugin.video.vstream')  # singleton


# class addon(xbmcaddon.Addon):
class addon:
    def __init__(self, addonId=None):
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


"""
from resources.lib.comaddon import dialog

Utilisation :
dialogs = dialog()
dialogs.VSinfo('test')
https://codedocs.xyz/xbmc/xbmc/group__python___dialog.html
"""


class dialog:
    def __init__(self):
        self.DIALOG = xbmcgui.Dialog()

    def VSok(self, desc, title='vStream'):
        return self.DIALOG.ok(title, desc)

    def VSyesno(self, desc, title='vStream'):
        return self.DIALOG.yesno(title, desc)

    def VSselect(self, desc, title='vStream'):
        return self.DIALOG.select(title, desc)

    def numeric(self, dialogType, heading, defaultt):
        return self.DIALOG.numeric(dialogType, heading, defaultt)

    def VSbrowse(self, type, heading, shares):
        return self.DIALOG.browse(type, heading, shares)

    def VSselectqual(self, list_qual, list_url):

        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]

        ret = self.DIALOG.select(addon().VSlang(30448), list_qual)
        if ret > -1:
            return list_url[ret]
        return ''

    def VSinfo(self, desc, title='vStream', iseconds=0, sound=False):
        if (iseconds == 0):
            iseconds = 1000
        else:
            iseconds = iseconds * 1000

        if (addon().getSetting('Block_Noti_sound') == 'true'):
            sound = True

        return self.DIALOG.notification(str(title), str(desc), xbmcgui.NOTIFICATION_INFO, iseconds, sound)

    def VSerror(self, e):
        return self.DIALOG.notification('vStream', 'Erreur: ' + str(e), xbmcgui.NOTIFICATION_ERROR, 2000), VSlog('Erreur: ' + str(e))

    def VStextView(self, desc, title='vStream'):
        return self.DIALOG.textviewer(title, desc)


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


class empty:

    def VSupdate(self, dialog, total, text='', search=False):
        pass

    def iscanceled(self):
        pass

    def VSclose(self, dialog):
        pass

    def getProgress(self):
        return 100  # simuler la fin de la progression

# Basé sur UrlResolver
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
                pd.create(self.heading, line1 + '\n' + line2 + '\n' + line3)
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
                self.pd.update(percent, line1 + '\n' + line2 + '\n' + line3)


class progress:
    def __init__(self):
        self.PROGRESS = None
        self.COUNT = 0

    def VScreate(self, title='', desc='', large=False):
        # l'option "large" permet de forcer un sablier large, seul le sablier large peut être annulé.

        # Ne pas afficher le sablier si nous ne sommes pas dans un menu vStream
        currentWindow = xbmcgui.getCurrentWindowId()
        if currentWindow != 10025 and currentWindow != 10028:  # 10025 = videonav, 10000 = home
            return empty()

        # Ne pas afficher le sablier si une dialog est ouverte, inclut le menu contextuel
        # sauf pour le spinner de chargement (10138)
        dlgId = xbmcgui.getCurrentWindowDialogId()
        if dlgId != 9999 and dlgId != 10138:  # 9999 = None
            return empty()

        if self.PROGRESS == None:
            if not title:
                title = addon().VSlang(30140)
            
            if large:
                self.PROGRESS = xbmcgui.DialogProgress()
            elif ADDONVS.getSetting('spinner_small') == 'true':
                self.PROGRESS = xbmcgui.DialogProgressBG()
            else:
                self.PROGRESS = xbmcgui.DialogProgress()
            self.PROGRESS.create(title, desc)

        return self

    def VSupdate(self, dialog, total, text='', search=False):
        if not self.PROGRESS:    # Déjà refermé
            return

        if not search and window(10101).getProperty('search') == 'true':
            return

        if not text:
            text= addon().VSlang(30140)

        self.COUNT += 1
        iPercent = int(float(self.COUNT * 100) / total)
        text += ' : ' + str(self.COUNT) + '/' + str(total) + '\n'
        if isinstance(self.PROGRESS, xbmcgui.DialogProgress):
            self.PROGRESS.update(iPercent, text )
        else:
            self.PROGRESS.update(iPercent, message = text )

    def iscanceled(self):
        if isinstance(self.PROGRESS, xbmcgui.DialogProgress):
            return self.PROGRESS.iscanceled()
        return False

    def VSclose(self, dialog=''):
        if not self.PROGRESS:
            return  # Déjà fermée

        if window(10101).getProperty('search') == 'true':
            return

        if self.PROGRESS:  # test si pas fermé entre-temps
            self.PROGRESS.close()

    def getProgress(self):
        return self.COUNT


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
    def __init__(self, label='', label2=''):
        pass

    # Permet l'ajout d'un menu après la création d'un item
    def addMenu(self, sFile, sFunction, sTitle, oOutputParameterHandler=False):
        sPluginPath = 'plugin://plugin.video.vstream/'  # cPluginHandler().getPluginPath()
        nbContextMenu = self.getProperty('nbcontextmenu')
        nbContextMenu = int(nbContextMenu) if nbContextMenu else 0

        sUrl = '%s?site=%s&function=%s' % (sPluginPath, sFile, sFunction)
        if oOutputParameterHandler:
            sUrl += '&%s' % oOutputParameterHandler.getParameterAsUri()

        property = 'contextmenulabel(%d)' % nbContextMenu
        self.setProperty(property, sTitle)

        property = 'contextmenuaction(%d)' % nbContextMenu
        self.setProperty(property, 'RunPlugin(%s)' % sUrl)

        self.setProperty('nbcontextmenu', str(nbContextMenu + 1))


"""
from resources.lib.comaddon import VSlog
VSlog('testtttttttttttt')
"""


# xbmc des fonctions pas des class
def VSlog(e, level=xbmc.LOGDEBUG):
    try:
        # rapelle l'ID de l'addon pour être appelé hors addon
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


# Transforme les "special" en chemin normal.
def VSPath(pathSpecial):
    if isMatrix():
        path = xbmcvfs.translatePath(pathSpecial)
    else:
        path = xbmc.translatePath(pathSpecial)
    return path


# Récupere le nom du profil courant
def VSProfil():
    # On chercher le profil courant.
    request = {
        "jsonrpc": "2.0",
        "method": "Profiles.GetCurrentProfile",
        "params": {
            "properties": ["thumbnail", "lockmode"]
        },
        "id": 1
    }

    req = json.dumps(request)
    response = xbmc.executeJSONRPC(req)
    # On recupere le nom.
    name = json.loads(response)['result']['label']
    return name


# Gestion des sources : activer/désactiver, libellé, url, ... 
class siteManager:

    SITES = 'sites'
    ACTIVE = 'active'
    CLOUDFLARE = 'cloudflare'
    LABEL = 'label'
    URL_MAIN = 'url'

    def __init__(self):
        
        # Propriétés par défaut
        self.defaultPath = VSPath('special://home/addons/plugin.video.vstream/resources/sites.json')
        self.defaultData = None

        # Propriétés selon le profil        
        name = VSProfil()
        if name == 'Master user':   # Le cas par defaut
            path = VSPath('special://home/userdata/addon_data/plugin.video.vstream/sites.json')
        else:
            path = VSPath('special://home/userdata/profiles/' + name + '/addon_data/plugin.video.vstream/sites.json')
        
        # Résolution du chemin
        try:
            self.propertiesPath = VSPath(path).decode('utf-8')
        except AttributeError:
            self.propertiesPath = VSPath(path)

        # Chargement des properties
        try:
            self.data = json.load(open(self.propertiesPath))
        except IOError:
            # le fichier n'existe pas, on le crée à partir des settings par défaut
            xbmcvfs.copy(self.defaultPath, path)
            self.data = json.load(open(self.propertiesPath))
            

    # site désactivé par la team
    def isEnable(self, sourceName):
        return self.getDefaultProperty(sourceName, self.ACTIVE) == 'True'

    # site identifié par la team comme étant protégé par Cloudflare, false par défaut si non renseigné
    def isCloudFlare(self, sourceName):
        return self.getDefaultProperty(sourceName, self.CLOUDFLARE) == 'True'

    
    # sites désactivé par l'utilisateur
    def isActive(self, sourceName):
        return self.getProperty(sourceName, self.ACTIVE) == 'True'
    
    def setActive(self, sourceName, state):
        self.setProperty(sourceName, self.ACTIVE, state)

    def getUrlMain(self, sourceName):
        return str(self.getDefaultProperty(sourceName, self.URL_MAIN))
    
    def disableAll(self):
        for sourceName in self.data[self.SITES]:
            self.setActive(sourceName, False)
        return

    def enableAll(self):
        for sourceName in self.data[self.SITES]:
            self.setActive(sourceName, True)
        return


    def getDefaultProperty(self, sourceName, propName):
        defaultProps = self._getDefaultProp(sourceName)
        if propName not in defaultProps:
            return False
        return defaultProps.get(propName)


    def getProperty(self, sourceName, propName):
        sourceData = self._getDataSource(sourceName)
        if sourceData:
            if propName in sourceData:
                return sourceData.get(propName)

            # Propriété inconnue, on récupérere la valeur par défaut ...
            defaultProps = self._getDefaultProp(sourceName)
            if propName not in defaultProps:
                return False

            # ... et on l'enregistre
            value = defaultProps.get(propName)
            self.setProperty(sourceName, propName, value)
            self.save()
            return value


    def setProperty(self, sourceName, propName, value):
        sourceData = self._getDataSource(sourceName)
        if sourceData:
            sourceData[propName] = str(value)

    def setDefaultProps(self, props):
        self.defaultData = props
        self._saveDefault()

    # Lire les settings d'une source
    def _getDataSource(self, sourceName):

        # userSettings
        sourceData = self.data[self.SITES].get(sourceName)
        
        # pas de user Settings, on recherche dans les default Settings
        if not sourceData:
            sourceData = self._getDefaultProp(sourceName)

            # Sauvegarder dans les user Settings
            if sourceData:
                self.data[self.SITES][sourceName] = sourceData

        return sourceData 
        
    # Récupérer les propriétés par défaut d'une source
    def _getDefaultProp(self, sourceName):

        # Chargement des properties par défaut
        if not self.defaultData:
            self.defaultData = json.load(open(self.defaultPath))

        # Retrouver la prop par défaut
        sourceData = self.defaultData[self.SITES].get(sourceName) if self.defaultData and self.SITES in self.defaultData else None
        
        # pas de valeurs par défaut, on en crée à la volée
        if not sourceData:
            return {}

        return sourceData
    
    # Sauvegarder les propriétés modifiées
    def save(self):
        with open(self.propertiesPath, 'w') as f:
            f.write(json.dumps(self.data, indent=4))

    # Sauvegarder les propriétés par défaut
    def _saveDefault(self):
        with open(self.defaultPath, 'w') as f:
            f.write(json.dumps(self.defaultData, indent=4))

    

class addonManager:
    # Demande l'installation d'un addon
    def installAddon(self, addon_id):
        xbmc.executebuiltin('InstallAddon(%s)' % addon_id, True)

    # Vérifie la présence d'un addon
    def isAddonExists(self, addon_id):
        return not xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id) == 0

    # Active/desactive un addon
    def enableAddon(self, addon_id, enable='True'):

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
