# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import addon, VSlog, siteManager
from resources.lib.db import cDb

import sys
import xbmcvfs


class cRechercheHandler:
    Count = 0

    def __init__(self):
        self.__sText = ""
        self.__sDisp = ""
        self.__sCat = ""
        self.__siteAdded = False

    def getPluginHandle(self):
        try:
            return int(sys.argv[1])
        except:
            return 0

    def getPluginPath(self):
        try:
            return sys.argv[0]
        except:
            return ''

    def setText(self, sText):
        if not sText:
            return False
        self.__sText = sText
        return self.__sText

    def getText(self):
        return self.__sText

    def setCat(self, sCat):
        if not sCat:
            return False
        self.__sCat = sCat
        return self.__sCat

    def getCat(self):
        return self.__sCat

    def setDisp(self, sDisp):
        if not sDisp:
            return False
        self.__sDisp = sDisp
        return self.__sDisp

    def getDisp(self):
        return self.__sDisp

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        items = xbmcvfs.listdir(sFolder)[1]
        items.remove("__init__.py")
        items.sort()

        for sItemName in items:
            sFilePath = "/".join([sFolder, sItemName])
            sFilePath = sFilePath.replace('\\', '/')

            if (xbmcvfs.exists(sFilePath) == True):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def importPlugin(self, sName, sCat):
        pluginData = {}

        if sCat == '1':
            sSearch = 'URL_SEARCH_MOVIES'
        elif sCat == '2':
            sSearch = 'URL_SEARCH_SERIES'
        elif sCat == '3':
            sSearch = 'URL_SEARCH_ANIMS'
        elif sCat == '4':
            sSearch = 'URL_SEARCH_SERIES'
        elif sCat == '5':
            sSearch = 'URL_SEARCH_MISC'
        elif sCat == '6':
            sSearch = 'URL_SEARCH_REPLAY'
        elif sCat == '7':
            sSearch = 'URL_SEARCH_MOVIES'
        elif sCat == '8':
            sSearch = 'URL_SEARCH_SERIES'
        elif sCat == '9':
            sSearch = 'URL_SEARCH_DRAMAS'
        else:
            sSearch = 'URL_SEARCH'

        try:
            plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
            pluginData['identifier'] = plugin.SITE_IDENTIFIER
            pluginData['name'] = plugin.SITE_NAME
            pluginData['search'] = getattr(plugin, sSearch)
            return pluginData
        except Exception as e:
            if ("has no attribute '%s'" % sSearch) not in str(e):
                VSlog(str(e))
            return False

    def getAvailablePlugins(self):
        sText = self.getText()
        if not sText:
            return False
        sCat = self.getCat()
        if not sCat:
            return False

        # historique
        addons = addon()
        try:
            if (addons.getSetting("history-view") == 'true'):
                meta = {'title': sText, 'disp': sCat}
                with cDb() as db:
                    db.insert_history(meta)
        except Exception as e:
            VSlog(str(e))
            pass

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder: " + sFolder)

        sitesManager = siteManager()

        use_flaresolverr = addon().getSetting("use_flaresolverr") == 'true'   # Utiliser FlareSolverrr

        aPlugins = []
        aFileNames = self.__getFileNamesFromFolder(sFolder)
        for sFileName in aFileNames:
            if sitesManager.isEnable(sFileName):
                if sitesManager.isActive(sFileName):
                    if use_flaresolverr or not sitesManager.isCloudFlare(sFileName):
                        aPlugin = self.importPlugin(sFileName, sCat)
                        if aPlugin:
                            aPlugins.append(aPlugin)

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = [sPluginName, sPluginIdentifier, sPluginDesc]
        return aPluginEntry
