#-*- coding: utf-8 -*-
from resources.lib.config import cConfig

import sys
import os

class cSiteHandler:

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

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        #items = os.listdir(sFolder)
        items = os.listdir(unicode(sFolder, 'utf-8'))
        for sItemName in items:
            #sFilePath = os.path.join(sFolder, sItemName)
            sFilePath = os.path.join(unicode(sFolder, 'utf-8'), sItemName)
            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')
            
            if (os.path.isdir(sFilePath) == False):
                #if (str(sFilePath.lower()).endswith('py')):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName, sLabel):
        try:
            exec "from resources.sites import "+sName
            exec "sSearch = "+sName+"."+sLabel
            exec "sSiteName = "+sName+".SITE_NAME"
            #sPluginSettingsName = sName
            sPluginSettingsName = 'plugin_' + sName
            return sSearch[0], sPluginSettingsName, sSearch[1], sSiteName
        except Exception, e:
            cConfig().log("cant import plugin: " + str(sName))            
            return False, False

    def getRootFolder(self):        
        sRootFolder = cConfig().getAddonPath()
        cConfig().log("Root Folder: " + sRootFolder)
        return sRootFolder
        
    def getRootArt(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/art/')
       
        sFolder = sFolder.replace('\\', '/')
        return sFolder

    def getAvailablePlugins(self, sLabel):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/sites')

        # xbox hack        
        sFolder = sFolder.replace('\\', '/')
        cConfig().log("Sites Folder: " + sFolder)
        
        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            cConfig().log("Load Plugin: " + str(sFileName))

            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName, sLabel)
            if (aPlugin[0] != False):
                sSiteUrl = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]
                sSiteName = aPlugin[3]

                # existieren zu diesem plugin die an/aus settings
                bPlugin = oConfig.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true'):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteUrl, sSiteName, sFileName, sSiteDesc))
                else:
                   # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                   aPlugins.append(self.__createAvailablePluginsItem(sSiteUrl,sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def __createAvailablePluginsItem(self, sSiteUrl, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sSiteUrl)
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry