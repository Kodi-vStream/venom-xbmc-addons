# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import sys
import xbmcvfs

from resources.lib.comaddon import addon, VSlog

class cSiteHandler:

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
            sFilePath = "/".join([sFolder, sItemName])
            sFilePath = sFilePath.replace('\\', '/')

            if (xbmcvfs.exists(sFilePath) == True):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName, sLabel):
        try:
            exec ("from resources.sites import " + sName, globals())
            exec ("sSearch = " + sName + "." + sLabel, globals())
            exec ("sSiteName = " + sName + ".SITE_NAME", globals())
            sPluginSettingsName = 'plugin_' + sName
            return sSearch[0], sPluginSettingsName, sSearch[1], sSiteName
        except Exception:
            VSlog("Cannot import plugin: " + str(sName))
            return False, False

    def getAvailablePlugins(self, sLabel):
        addons = addon()
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder: " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            VSlog("Load Plugin: " + str(sFileName))

            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName, sLabel)
            if (aPlugin[0] != False):
                sSiteUrl = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteDesc = aPlugin[2]
                sSiteName = aPlugin[3]

                # existieren zu diesem plugin die an/aus settings
                bPlugin = addons.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true'):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteUrl, sSiteName, sFileName, sSiteDesc))
                else:
                    # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                    aPlugins.append(self.__createAvailablePluginsItem(sSiteUrl, sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def __createAvailablePluginsItem(self, sSiteUrl, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sSiteUrl)
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
