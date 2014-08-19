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
            self.__oname = self.__oSettings.getAddonInfo("name")
            self.__ocache = xbmc.translatePath(self.__oSettings.getAddonInfo("profile"))
            self.__sRootArt = os.path.join(os.getcwd(), 'resources/art/')
            self.__sIcon = self.__sRootArt+'icon.png'
            self.__sFileFav = self.__ocache+'favourite.db'


    def isDharma(self):
        return self.__bIsDharma

    def getPluginId(self):
	return 'plugin.video.vstream'
    
    def getSettingCache(self):
        return self.__ocache
    
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
        