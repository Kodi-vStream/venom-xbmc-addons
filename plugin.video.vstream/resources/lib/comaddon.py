#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmcaddon, xbmcgui, xbmc

"""
from resources.lib.comaddon import addon
ou
from resources.lib.comaddon import *

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

    def VSsetting(self, name, value=False):
        #adons = addon()
        #use addons.setting('name') pour getsetting
        #use addons.setting('name', 'value) pour setsetting
        if value:
            return self.setSetting(name, value)
        else:
            return self.getSetting(name)


"""
from resources.lib.comaddon import dialog
ou
from resources.lib.comaddon import *

ne peux pas utiliser les autres fonction que dialog 
dialogs = dialog()
dialogs.VSinfo('test')
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#Dialog
"""

class dialog(xbmcgui.Dialog):

    #def __init__(self):
    #    xbmcgui.__init__('')
    #    pass
    def VSok(self, desc, title='vStream'):
        dialog = self.ok(title, desc)
        return dialog

    def VSyesno(self, desc, title='vStream'):
        dialog = self.yesno(title, desc)
        return dialog

    def VSselect(desc, title='vStream'):
        dialog = self.select(sTitle, desc)
        return dialog

    def VSinfo(self, desc, title='vStream', iseconds=0, sound = False):
        if (iseconds == 0):
            iseconds = 1000
        else:
            iseconds = iseconds * 1000
        
        if (addon().getSetting('Block_Noti_sound') == 'true'):
            sound = True

        return self.notification(str(title), str(desc),xbmcgui.NOTIFICATION_INFO,iseconds,sound)

    def VSerror(self, e):
        return self.notification('Vstream','Erreur: '+str(e),xbmcgui.NOTIFICATION_ERROR,2000), log('Erreur: ' + str(e))
        
"""
from resources.lib.comaddon import progress
ou
from resources.lib.comaddon import *
dialog = progress()
dialog.VScreate(SITE_NAME)
dialog.VSupdate(dialog, total)
dialog.close()
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#DialogProgress
"""

COUNT = 0
DIALOG2 = None

class progress(xbmcgui.DialogProgress):

    
    def VScreate(self, title='vStream', desc=''):
        global DIALOG2
        if DIALOG2 == None:
            dialog = self.create(title, desc)
            DIALOG2 = dialog
            return dialog
        else:
            return DIALOG2

    def VSupdate(self, dialog, total, text=''):
        global COUNT
        COUNT += 1
        iPercent = int(float(COUNT * 100) / total)
        self.update(iPercent, 'Loading: '+str(COUNT)+'/'+str(total), text)

        
"""
from resources.lib.comaddon import window
ou
from resources.lib.comaddon import *
window(10101).getProperty('test')
http://mirrors.kodi.tv/docs/python-docs/16.x-jarvis/xbmcgui.html#Window
"""

class window(xbmcgui.Window):
    
    def __init__(self, id):
        pass

"""
from resources.lib.comaddon import *
VSlog('testtttttttttttt')
"""
#xbmc des fonctions pas des class
def VSlog(e, level=xbmc.LOGDEBUG):
    if (addon().getSetting('Block_Noti_sound') == 'true'):
        level = xbmc.LOGNOTICE
    return xbmc.log('\t[PLUGIN] Vstream: '+str(e), xbmc.LOGDEBUG)

def VSupdate():
    return xbmc.executebuiltin("Container.Refresh")

def VSshow_busy():
    xbmc.executebuiltin('ActivateWindow(busydialog)')

def VShide_busy():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
        xbmc.sleep(100)