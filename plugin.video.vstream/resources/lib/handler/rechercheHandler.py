#-*- coding: utf-8 -*-
#from resources.lib.config import cConfig
from resources.lib.comaddon import addon, VSlog
from resources.lib.db import cDb

import sys
import xbmcvfs

class cRechercheHandler:

    Count = 0

    def __init__(self):
        self.__sText = ""
        self.__sDisp = ""
        self.__sCat = ""

    def getPluginHandle(self):
        try:
            return int( sys.argv[ 1 ] )
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
        #items = os.listdir(sFolder)
        #items = os.listdir(unicode(sFolder, 'utf-8'))
        folder, items = xbmcvfs.listdir(sFolder)
        items.sort()

        for sItemName in items:
            #sFilePath = os.path.join(sFolder, sItemName)
            #sFilePath = os.path.join(unicode(sFolder, 'utf-8'), sItemName)
            sFilePath = "/".join([sFolder, sItemName])
            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            if (xbmcvfs.exists(sFilePath) == True):
                #if (str(sFilePath.lower()).endswith('py')):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList


    def importPlugin(self, sName, sCat):
        pluginData = {}

        #multicherche
        # if sLabel == 'search5':
        #     bPlugin = 'true'

        if sCat == '1':
            sSearch = 'URL_SEARCH_MOVIES'
        elif sCat == '2':
            sSearch = 'URL_SEARCH_SERIES'
        elif sCat == '3':
            sSearch = 'URL_SEARCH_MISC'
        else :
            sSearch = 'URL_SEARCH'

        try:

            plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])

            pluginData['identifier'] = plugin.SITE_IDENTIFIER
            pluginData['name'] = plugin.SITE_NAME
            pluginData['search'] = getattr(plugin, sSearch)
            return pluginData

        except Exception, e:
            #VSlog("cant import plugin: " + str(sName))
            return False


    # def getRootFolder(self):
    #     sRootFolder = cConfig().getAddonPath()
    #     cConfig().log("Root Folder: " + sRootFolder)
    #     return sRootFolder

    # def getRootArt(self):
    #     oConfig = cConfig()

    #     sFolder =  self.getRootFolder()
    #     sFolder = os.path.join(sFolder, 'resources/art/').decode("utf-8")

    #     sFolder = sFolder.replace('\\', '/')
    #     return sFolder

    def getAvailablePlugins(self):

        addons = addon()
        sText = self.getText()
        if not sText:
            return False
        sCat =  self.getCat()
        if not sCat:
            return False

        #historique
        try:
            if (addons.getSetting("history-view") == 'true'):
                meta = {}
                meta['title'] = sText
                meta['disp'] = sCat
                cDb().insert_history(meta)
        except: pass

        #sFolder =  self.getRootFolder()
        #sFolder = os.path.join(sFolder, 'resources/sites')
        
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder: " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            sPluginSettingsName = 'plugin_' + sFileName
            bPlugin = addons.getSetting(sPluginSettingsName)
            if (bPlugin == 'true'):
                aPlugin = self.importPlugin(sFileName, sCat)
                if aPlugin:
                    aPlugins.append(aPlugin)
        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
