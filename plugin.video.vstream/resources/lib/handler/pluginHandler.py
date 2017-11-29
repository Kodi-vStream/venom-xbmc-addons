#-*- coding: utf-8 -*-
from resources.lib.config import cConfig

import sys
import os

class cPluginHandler:

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
        items.sort()
        for sItemName in items:
            
            if not sItemName.endswith(".py"):
                continue
            
            #sFilePath = os.path.join(sFolder, sItemName)
            sFilePath = os.path.join(unicode(sFolder, 'utf-8'), sItemName)
            #size
            sSize = 0
            try:
                file=open(sFilePath)
                Content = file.read()
                sSize = len(Content)
                file.close()
            except: pass

            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            cConfig().log("Load Plugin %s : Size %s" % (sItemName, sSize))

            if (os.path.isdir(sFilePath) == False):
                #if (str(sFilePath.lower()).endswith('py')):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName):
        try:
            exec "from resources.sites import " + sName
            exec "sSiteName = " + sName + ".SITE_NAME"
            exec "sSiteDesc = " + sName + ".SITE_DESC"
            sPluginSettingsName = 'plugin_' + sName
            return sSiteName, sPluginSettingsName, sSiteDesc
        except Exception, e:
            cConfig().log("Cant import plugin " + str(sName))
            return False, False

    def getRootFolder(self):
        sRootFolder = cConfig().getAddonPath()
        cConfig().log("Root Folder " + sRootFolder)
        return sRootFolder

    def getRootArt(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/art/').decode("utf-8")

        sFolder = sFolder.replace('\\', '/')
        return sFolder

    def getAvailablePlugins(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/sites')

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        cConfig().log("Sites Folder " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]

                # existieren zu diesem plugin die an/aus settings
                bPlugin = oConfig.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true'):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))
                else:
                   # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                   aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

        return aPlugins


    def getSearchPlugins(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/sites')

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        cConfig().log("Sites Folder " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            cConfig().log("Load Plugin " + str(sFileName))

            aPlugin = self.__importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]

                # tester si active ou pas
                bPlugin = oConfig.getSetting(sPluginSettingsName)
                #test si une recherche et possible
                try:
                    exec "from resources.sites import " + sFileName
                    exec "sSearch = " + sFileName + ".URL_SEARCH"
                    sPlugin = True
                except:
                    sPlugin = False
                
                if  sPlugin == True:
                    aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
