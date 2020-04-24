# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmcaddon, xbmcgui, xbmc

"""System d'importation

from resources.lib.comaddon import addon, dialog, VSlog, xbmcgui, xbmc

"""

"""
from resources.lib.comaddon import addon

addons = addon() en haut de page.

utiliser une fonction comaddon ou xbmcaddon
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcaddon.html

addons.VSlang(30305)
addons.getLocalizedString(30305)
addons.openSettings()

utiliser la fonction avec un autre addon

addons2 = addon('plugin.video.youtube')
addons2.openSettings()
"""

class addon(xbmcaddon.Addon):

    #def __init__(self, id='plugin.video.vstream'):
    #    xbmcaddon.__init__(id)
    #    pass

    def VSlang(self, lang):
        return xbmc.translatePath(self.getLocalizedString(lang))
        #xbmcaddon.Addon('plugin.video.vstream').getLocalizedString(lang))
        #Bug avec accent xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getLocalizedString(lang)).decode('utf-8')

    #deprecier utiliser addons.setSetting et addons.getSetting
    def VSsetting(self, name, value = False):
        #addons = addon()
        #use addons.setting('name') pour getsetting
        #use addons.setting('name', 'value) pour setsetting
        if value:
            return self.setSetting(name, value)
        else:
            return self.getSetting(name)


"""
from resources.lib.comaddon import dialog

ne peux pas utiliser les autres fonction que dialog
dialogs = dialog()
dialogs.VSinfo('test')
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#Dialog
"""

class dialog(xbmcgui.Dialog):

    #def __init__(self):
    #    xbmcgui.__init__('')
    #    pass

    def VSok(self, desc, title = 'vStream'):
        dialog = self.ok(title, desc)
        return dialog

    def VSyesno(self, desc, title = 'vStream'):
        dialog = self.yesno(title, desc)
        return dialog

    def VSselect(self, desc, title = 'vStream'):
        ret = self.select(title, desc)
        return ret

    def VSselectqual(self, list_qual, list_url):

        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]

        ret = self.select(addon().VSlang(30448), list_qual)
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

        return self.notification(str(title), str(desc), xbmcgui.NOTIFICATION_INFO, iseconds, sound)

    def VSerror(self, e):
        return self.notification('vStream', 'Erreur: ' + str(e), xbmcgui.NOTIFICATION_ERROR, 2000), VSlog('Erreur: ' + str(e))

"""
from resources.lib.comaddon import progress

progress_ = progress()
progress_.VScreate(SITE_NAME)
progress_.VSupdate(progress_, total)
if progress_.iscanceled():
    break
progress_.VSclose(progress_)

dialog = progress() non recommander
progress = progress() non recommander
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#DialogProgress
"""

COUNT = 0
DIALOG2 = None

class empty():

    def VSupdate(self, dialog, total, text = '', search = False):
        pass

    def iscanceled(self):
        pass

    def VSclose(self, dialog):
        pass

class progress(xbmcgui.DialogProgress):

    def VScreate(self, title = 'vStream', desc = ''):
        global DIALOG2

        currentWindow = xbmcgui.getCurrentWindowId()
        if currentWindow == 10000:
            return empty()

        if DIALOG2 == None:
            self.create(title, desc)
            VSlog('create dialog')
            DIALOG2 = self
            return self
        else:
            return DIALOG2

    def VSupdate(self, dialog, total, text = '', search = False):
        if not search and window(10101).getProperty('search') == 'true':
            return
        global COUNT
        COUNT += 1
        iPercent = int(float(COUNT * 100) / total)
        dialog.update(iPercent, 'Loading: ' + str(COUNT) + '/' + str(total), text)


    def VSclose(self, dialog = ''):
        if not dialog and DIALOG2:
            dialog = DIALOG2
        if not dialog:
            return

        if window(10101).getProperty('search') == 'true':
            return
        dialog.close()
        VSlog('close dialog')
        del dialog
        return False

"""
from resources.lib.comaddon import window

window(10101).getProperty('test')
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#Window
"""

class window(xbmcgui.Window):

    def __init__(self, id):
        pass

"""
from resources.lib.comaddon import listitem
listitem.setLabel('test')
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#ListItem
"""

class listitem(xbmcgui.ListItem):

    #ListItem([label, label2, iconImage, thumbnailImage, path])

    def __init__(self, label = '', label2 = '', iconImage = '', thumbnailImage = '', path = ''):
        pass

"""
from resources.lib.comaddon import VSlog
VSlog('testtttttttttttt')
ou
xbmc.log
"""

#xbmc des fonctions pas des class
def VSlog(e, level = xbmc.LOGDEBUG):
    #rapelle l'ID de l'addon pour être appelé hors addon
    if (addon('plugin.video.vstream').getSetting('debug') == 'true'):
        level = xbmc.LOGNOTICE
    return xbmc.log('\t[PLUGIN] vStream: ' + str(e), level)

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

def VSread(sHtmlContent):
    import xbmcvfs
    file = 'special://userdata/addon_data/plugin.video.vstream/html.txt'
    if xbmcvfs.exists(file):
        xbmcvfs.delete(file)

    f = xbmcvfs.File (file, 'w')
    result = f.write(sHtmlContent)
    f.close()

#use cGui.showKeyBoard
def VSkeyboard(sDefaultText = ''):
    return False
