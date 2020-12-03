# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import sys
import xbmcvfs

from resources.lib.comaddon import addon, VSlog

class cPluginHandler:

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

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        folder, items = xbmcvfs.listdir(sFolder)
        items.sort()
        for sItemName in items:

            if not sItemName.endswith(".py"):
                continue

            sFilePath = "/".join([sFolder, sItemName])

            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            VSlog("Load Plugin %s" % sItemName)

            if (xbmcvfs.exists(sFilePath) == True):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName):
        try:
            exec("from resources.sites import " + sName, globals())
            exec("sSiteName = " + sName + ".SITE_NAME", globals())
            exec("sSiteDesc = " + sName + ".SITE_DESC", globals())
            sPluginSettingsName = 'plugin_' + sName
            return sSiteName, sPluginSettingsName, sSiteDesc
        except Exception as e:
            VSlog("Cannot import plugin " + str(sName))
            VSlog("Detail de l\'erreur " + str(e))
            return False, False

    def getAvailablePlugins(self, force=False):
        addons = addon()

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
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
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
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
