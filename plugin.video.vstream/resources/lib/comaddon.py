#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmcaddon

""" utiliser 
from resources.lib.comaddon import addon

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
        pass

    def lang(self, lang):
        return self.getLocalizedString(lang)