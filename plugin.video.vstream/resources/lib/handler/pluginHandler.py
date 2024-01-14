# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import sys
import xbmcvfs
import json

from resources.lib.comaddon import addon, VSlog, VSPath


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
        items = xbmcvfs.listdir(sFolder)[1]
        items.remove("__init__.py")
        items.sort()
        
        for sItemName in items:
            if not sItemName.endswith(".py"):
                continue

            sFilePath = "/".join([sFolder, sItemName])

            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            if (xbmcvfs.exists(sFilePath) == True):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName, sLabel=""):
        try:
            exec("from resources.sites import " + sName, globals())
            exec("sSiteName = " + sName + ".SITE_NAME", globals())
            sPluginSettingsName = 'plugin_' + sName
            if sLabel:
                exec("sSearch = " + sName + "." + sLabel, globals())
                return sSearch[0], sPluginSettingsName, sSearch[1], sSiteName
            else:
                exec("sSiteDesc = " + sName + ".SITE_DESC", globals())
                return sSiteName, sPluginSettingsName, sSiteDesc
        except Exception as e:
            VSlog("Cannot import plugin " + str(sName))
            VSlog("Detail de l\'erreur " + str(e))
            return False, False

    def getAvailablePlugins(self, sLabel="", force=False):
        path = VSPath('special://home/addons/plugin.video.vstream/resources/sites.json')
        with open(path) as f:
            data = json.load(f)
        addons = addon()

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            # existieren zu diesem plugin die an/aus settings
            bPlugin = data['site']["plugin_" + sFileName]['active']
            if (bPlugin != ''):
                # settings gefunden
                if (bPlugin == 'true') or (force == True):
                    # wir versuchen das plugin zu importieren
                    if sLabel:
                        aPlugin = self.__importPlugin(sFileName, sLabel)
                    else:
                        aPlugin = self.__importPlugin(sFileName)

                    if (aPlugin[0] != False):
                        sPluginSettingsName = aPlugin[1]
                        sSiteDesc = aPlugin[2]
                        if sLabel:
                            sSiteUrl = aPlugin[0]
                            sSiteName = aPlugin[3]
                            item = self.__createAvailablePluginsItem(sSiteUrl, sSiteName, sFileName, sSiteDesc)
                        else:
                            sSiteName = aPlugin[0]
                            item = self.__createAvailablePluginsItem("", sSiteName, sFileName, sSiteDesc)

                        aPlugins.append(item)

        return aPlugins

    def getAllPlugins(self):
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')

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
                aPlugins.append(self.__createAvailablePluginsItem("", sSiteName, sFileName, sSiteDesc))

        return aPlugins

    def __createAvailablePluginsItem(self, sSiteUrl, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        if sSiteUrl:
            aPluginEntry.append(sSiteUrl)
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
