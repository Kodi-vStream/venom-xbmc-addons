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

addons.lang(30305)
addons.getLocalizedString(30305)
addons.openSettings()

utiliser la fonction avec un autre addon

addons2 = addon('plugin.video.youtube')
addons2.openSettings()
"""

class addon(xbmcaddon.Addon):

    def __init__(self, id='plugin.video.vstream'):
        xbmcaddon.__init__(id)
        print 'initttttttttt xbmcaddon'
        pass

    def lang(self, lang):
        return self.getLocalizedString(lang)

    def setting(self, name, value=False):
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
dialogs.info('test')
"""

class dialog(xbmcgui.Dialog):

    def __init__(self):
        xbmcgui.__init__('')
        print 'initttttttttt xbmcgui'
        pass

    def info(self, desc, title = 'vStream', iseconds=0,sound = False):
        if (iseconds == 0):
            iseconds = 1000
        else:
            iseconds = iseconds * 1000
        
        if addon().setting('Block_Noti_sound') == 'true':
            sound = True

        return self.notification(str(title), str(desc),xbmcgui.NOTIFICATION_INFO,iseconds,sound)

    def error(self, e):
        self.notification('Vstream','Erreur: '+str(e),xbmcgui.NOTIFICATION_ERROR,2000)
        log('Erreur: ' + str(e))


"""
from resources.lib.comaddon import *
log('testtttttttttttt')
"""
#xbmc des fonctions pas des class
def log(e):
    return xbmc.log('\t[PLUGIN] Vstream: '+str(e), xbmc.LOGDEBUG)