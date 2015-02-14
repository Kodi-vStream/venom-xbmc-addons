#-*- coding: utf-8 -*-
#Venom.
from config import cConfig

import xbmc, xbmcgui, xbmcaddon
import sys, os

SITE_IDENTIFIER = 'clear'
SITE_NAME = 'Clear'

class cClear:

    def __init__(self):
        self.main(sys.argv[1])
        #self.__sFunctionName = ''
      

    def main(self, env):
        

        if (env == 'addon'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                
                cached_fav = cConfig().getFileFav()
                cached_DB = cConfig().getFileDB()
                self.ClearDir2(xbmc.translatePath(cached_fav),True)
                self.ClearDir2(xbmc.translatePath(cached_DB),True)
                xbmc.executebuiltin("XBMC.Notification(Clear Addon Cache,Successful,5000,"")")
            return

        if (env == 'xbmc'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                self.ClearDir(xbmc.translatePath('special://temp/'),True)
                xbmc.executebuiltin("XBMC.Notification(Clear XBMC Cache,Successful,5000,"")")
            return

        else :
                return
        return

    def ClearDir(self, dir, clearNested = False):
        for the_file in os.listdir(dir):
            file_path = os.path.join(dir, the_file)
            if clearNested and os.path.isdir(file_path):
                self.ClearDir(file_path, clearNested)
                try: os.rmdir(file_path)
                except Exception, e: print str(e)
            else:
                try:os.unlink(file_path)
                except Exception, e: print str(e)
                    
    def ClearDir2(self, dir, clearNested = False):

            try:os.unlink(dir)
            except Exception, e: print str(e)

cClear()