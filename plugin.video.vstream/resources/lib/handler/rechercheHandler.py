# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import addon, VSlog, VSPath
from resources.lib.db import cDb

import sys
import xbmcvfs
import json


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
            sSearch = 'URL_SEARCH_DRAMAS'
        elif sCat == '5':
            sSearch = 'URL_SEARCH_MISC'
        else:
            sSearch = 'URL_SEARCH'

        try:
            plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
            pluginData['identifier'] = plugin.SITE_IDENTIFIER
            pluginData['name'] = plugin.SITE_NAME
            pluginData['search'] = getattr(plugin, sSearch)
            return pluginData
        except:
            return False

    def getAvailablePlugins(self):
        path = VSPath('special://home/addons/plugin.video.vstream/resources/sites.json')
        addons = addon()
        sText = self.getText()
        if not sText:
            return False
        sCat = self.getCat()
        if not sCat:
            return False

        # historique
        try:
            if (addons.getSetting("history-view") == 'true'):
                meta = {'title': sText, 'disp': sCat}
                with cDb() as db:
                    db.insert_history(meta)
        except:
            pass

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"

        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder: " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)
        with open(path) as f:
            data = json.load(f)

        aPlugins = []
        for sFileName in aFileNames:
            pluginData = data["site"].get('plugin_' + sFileName)
            if pluginData is None:
                data['site'].update({'plugin_' + sFileName: {"label": sFileName, "active": "true"}})
                if self.__siteAdded == False:
                    self.__siteAdded = True

            bPlugin = data['site']['plugin_' + sFileName]['active']
            if (bPlugin == 'true'):
                aPlugin = self.importPlugin(sFileName, sCat)
                if aPlugin:
                    aPlugins.append(aPlugin)

        if self.__siteAdded == True:
            with open(path, 'w') as f:
                f.write(json.dumps(data, indent=4))

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = [sPluginName, sPluginIdentifier, sPluginDesc]
        return aPluginEntry
