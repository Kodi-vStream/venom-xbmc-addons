#-*- coding: utf-8 -*-
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.db import cDb

import sys
import os
import urllib
import xbmcgui
import xbmc

class cRechercheHandler:

    Count = 0

    def __init__(self):
        self.__sText = ""
        self.__sDisp = ""
        self.__sRead = "True"

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
            oGui = cGui()
            sSearchText = oGui.showKeyBoard()
            sText = urllib.quote(sSearchText)
        self.__sText = sText
        return self.__sText

    def getText(self):
        return self.__sText


    def setDisp(self, sDisp):
        if not sDisp:
            disp = ['search1','search2','search3','search4','search5','search10'] #modif
            dialog2 = xbmcgui.Dialog()
            dialog_select = [cConfig().getSetting('search1_label'), cConfig().getSetting('search2_label'), cConfig().getSetting('search3_label'), cConfig().getSetting('search4_label'), cConfig().getlanguage(30092),'Recherche Alluc_ee']#modif

            ret = dialog2.select(cConfig().getlanguage(30093),dialog_select)

            if ret > -1:
                sDisp = disp[ret]
                
        self.__sDisp = sDisp
        return self.__sDisp

    def setRead(self, sRead):
        self.__sRead = sRead

    def getDisp(self):
        return self.__sDisp

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

    def __importPlugin_old(self, sName, sLabel, sText):
        oConfig = cConfig()
        sPluginSettingsName = sLabel+'_' +sName
        bPlugin = oConfig.getSetting(sPluginSettingsName)
        #multicherche
        if sLabel == 'search5':
            bPlugin = 'true'

        OnPlugins = oConfig.getSetting('plugin_' + sName)

        if (bPlugin == 'true') and (OnPlugins == 'true'):
            try:
                oGui = cGui()

                exec "from resources.sites import " + sName
                exec "sDisplayname = " + sName + ".SITE_NAME"
                exec "sSearch = " + sName + ".URL_SEARCH"

                cConfig().log("Load Recherche: " + str(sName))

                cRechercheHandler.Count += 1
                Count = cRechercheHandler.Count
                if (Count == 1):
                    oGui.addText(sName, '[COLOR khaki]%s: %s[/COLOR]' % (cConfig().getlanguage(30076), sText), 'none.png')
                    
                oGui.addText(sName, '%s. [COLOR olive]%s[/COLOR]' % (Count, sDisplayname), 'sites/%s.png' % (sName))

                sUrl = sSearch[0]+sText
                searchUrl = "%s.%s('%s')" % (sName, sSearch[1], sUrl)
                exec searchUrl

                return True
            except Exception, e:
                cConfig().log("cant import plugin: " + str(sName))
                return False, False
        else:
            return False, False
            
    def __importPlugin(self, sName, sLabel):
        pluginData = {}
        oConfig = cConfig()
        sPluginSettingsName = sLabel+'_' +sName
        bPlugin = oConfig.getSetting(sPluginSettingsName)
        #multicherche
        if sLabel == 'search5':
            bPlugin = 'true'

        OnPlugins = oConfig.getSetting('plugin_' + sName)

        if (bPlugin == 'true') and (OnPlugins == 'true'):
            try:

                plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
                
                pluginData['identifier'] = plugin.SITE_IDENTIFIER
                pluginData['name'] = plugin.SITE_NAME
                pluginData['search'] = plugin.URL_SEARCH
                 
            except Exception, e:
                cConfig().log("cant import plugin: " + str(sName))
            
        return pluginData


    def getRootFolder(self):
        sRootFolder = cConfig().getAddonPath()
        cConfig().log("Root Folder: " + sRootFolder)
        return sRootFolder

    def getRootArt(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/art/').decode("utf-8")

        sFolder = sFolder.replace('\\', '/')
        return sFolder

    def getAvailablePlugins(self):
        oConfig = cConfig()
        sText = self.getText()
        if not sText:
            return False
        sLabel = self.getDisp()
        if not sLabel:
            return False

        #historique
        try:
            if (cConfig().getSetting("history-view") == 'true' and self.__sRead != "False"):
                meta = {}
                meta['title'] = sText
                meta['disp'] = sLabel
                cDb().insert_history(meta)
        except: pass

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'resources/sites').decode("utf-8")

        # xbox hack
        sFolder = sFolder.replace('\\', '/')
        cConfig().log("Sites Folder: " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)
  
        aPlugins = []
        for sFileName in aFileNames:
            aPlugin = self.__importPlugin(sFileName, sLabel)
            if aPlugin:
                aPlugins.append(aPlugin)
        
        #multiselect
        if sLabel == 'search5':
            multi = []
            for plugin in aPlugins:
                multi.append(plugin['identifier'])
            dialog = xbmcgui.Dialog()
            ret = dialog.multiselect(cConfig().getlanguage(30094), multi)
            NewFileNames = []
            if ret > -1:
                for i in ret:
                    NewFileNames.append(aPlugins[i])

            aPlugins = NewFileNames
        #fin multiselect
        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier, sPluginDesc):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
