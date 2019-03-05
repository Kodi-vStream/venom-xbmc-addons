#-*- coding: utf-8 -*-
#from resources.lib.config import cConfig

from resources.lib.comaddon import addon, VSlog

import sys
import xbmcvfs

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
        #items = os.listdir(unicode(sFolder, 'utf-8'))
        folder, items = xbmcvfs.listdir(sFolder)
        items.sort()
        for sItemName in items:
            
            if not sItemName.endswith(".py"):
                continue
            

            #sFilePath = os.path.join(unicode(sFolder, 'utf-8'), sItemName)
            sFilePath = "/".join([sFolder, sItemName])
            #size
            # sSize = 0
            # try:
            #     file=open(sFilePath)
            #     Content = file.read()
            #     sSize = len(Content)
            #     file.close()
            # except: pass

            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            #cConfig().log("Load Plugin %s : Size %s" % (sItemName, sSize))
            VSlog("Load Plugin %s" % (sItemName))

            #if (os.path.isdir(sFilePath) == False):
            if (xbmcvfs.exists(sFilePath) == True):
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
            VSlog("Cant import plugin " + str(sName))
            return False, False

    # def getRootFolder(self):
    #     sRootFolder = cConfig().getAddonPath()
    #     cConfig().log("Root Folder " + sRootFolder)
    #     return sRootFolder

    # def getRootArt(self):
    #     oConfig = cConfig()

    #     sFolder =  self.getRootFolder()
    #     sFolder = os.path.join(sFolder, 'resources/art/').decode("utf-8")

    #     sFolder = sFolder.replace('\\', '/')
    #     return sFolder

    def getAvailablePlugins(self,force = False):
        #oConfig = cConfig()
        addons = addon()

        #sFolder =  self.getRootFolder()
        #sFolder = os.path.join(sFolder, 'resources/sites')
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        #cConfig().log("Sites Folder " + sFolder)
        VSlog("Sites Folder " + sFolder)

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
                bPlugin = addons.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true') or (force == True):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))
                else:
                   # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                   aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

        return aPlugins


    def getAllPlugins(self):
        #oConfig = cConfig()

        #sFolder =  self.getRootFolder()
        #sFolder = os.path.join(sFolder, 'resources/sites')
        #print sFolder
        

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]

                # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
