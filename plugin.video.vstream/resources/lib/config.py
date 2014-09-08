import os
import sys
import xbmc
import xbmcplugin

class cConfig:

    def __check(self):
        try:
            import xbmcaddon           
            self.__bIsDharma = True            
        except ImportError:
            self.__bIsDharma = False

    def __init__(self):
        self.__check()

        if (self.__bIsDharma):
            import xbmcaddon
            self.__oSettings = xbmcaddon.Addon(self.getPluginId())
            self.__aLanguage = self.__oSettings.getLocalizedString
            self.__setSetting = self.__oSettings.setSetting
            self.__getSetting = self.__oSettings.getSetting
            self.__oVersion = self.__oSettings.getAddonInfo("version")
            self.__oId = self.__oSettings.getAddonInfo("id")
            self.__oPath = self.__oSettings.getAddonInfo("path")
            self.__oName = self.__oSettings.getAddonInfo("name")
            self.__oCache = xbmc.translatePath(self.__oSettings.getAddonInfo("profile"))
            self.__sRootArt = os.path.join(self.__oPath,'resources/art/')
            self.__sIcon = os.path.join(self.__oPath,'resources/art/icon.png')
            self.__sFileFav = os.path.join(self.__oCache,'favourite.db')


    def isDharma(self):
        return self.__bIsDharma

    def getPluginId(self):
        return 'plugin.video.vstream'
    
    def getSettingCache(self):
        return self.__oCache

    def getAddonPath(self):
        return self.__oPath

    def getAddonVersion(self):
        return self.__oVersion
    
    def getFileFav(self):
        return self.__sFileFav

    def showSettingsWindow(self):
        if (self.__bIsDharma):
            self.__oSettings.openSettings()
        else:
            try:		
		xbmcplugin.openSettings( sys.argv[ 0 ] )
            except:
		pass

    def getSetting(self, sName):
        if (self.__bIsDharma):
            return self.__oSettings.getSetting(sName)
        else:
            try:                
                return xbmcplugin.getSetting(sName)
            except:
		return ''

    def getLocalizedString(self, sCode):
        if (self.__bIsDharma):
            return self.__aLanguage(sCode)
        else:
            try:		
		return xbmc.getLocalizedString(sCode)
            except:
		return ''
        
    def showKeyBoard(self, sDefaultText=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False
        
    def showInfo(self, sTitle, sDescription, iSeconds=0):
        if (self.__bIsDharma == False):
            return

        if (iSeconds == 0):
                iSeconds = 1000
        else:
                iSeconds = iSeconds * 1000
        
        xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds, self.__sIcon))
        
    def update(self):
        xbmc.executebuiltin("Container.Refresh")


    def error(self, e):
        xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % ('Vstream Erreur', (str(e)), '10000', self.__sIcon))
        xbmc.log('\t[PLUGIN] Vstream Erreur: '+str(e))

    def log(self, e):
        xbmc.log('\t[PLUGIN] Vstream: '+str(e))
        