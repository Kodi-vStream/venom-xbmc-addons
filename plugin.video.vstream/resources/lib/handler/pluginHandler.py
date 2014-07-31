from resources.lib.config import cConfig
import logger
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
        items = os.listdir(sFolder)
        for sItemName in items:
            sFilePath = os.path.join(sFolder, sItemName)
            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')
            
            if (os.path.isdir(sFilePath) == False):
                if (str(sFilePath.lower()).endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName):
        try:
            exec "import " + sName
            exec "sSiteName = " + sName + ".SITE_NAME"
            sPluginSettingsName = 'plugin_' + sName
            return sSiteName, sPluginSettingsName
        except Exception, e:
            logger.error("can't import plugin: " + str(sName))            
            return False, False

    def getRootFolder(self):        
        sRootFolder = os.getcwd()
        logger.info('root folder: ' + sRootFolder)
        return sRootFolder

    def getAvailablePlugins(self):
        oConfig = cConfig()

        sFolder =  self.getRootFolder()
        sFolder = os.path.join(sFolder, 'sites')

        # xbox hack        
        sFolder = sFolder.replace('\\', '/')
        logger.info('sites folder: ' + sFolder)
        
        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:
            logger.info('load plugin: '+ str(sFileName))

            # wir versuchen das plugin zu importieren
            aPlugin = self.__importPlugin(sFileName)
            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]

                # existieren zu diesem plugin die an/aus settings
                bPlugin = oConfig.getSetting(sPluginSettingsName)
                if (bPlugin != ''):
                    # settings gefunden
                    if (bPlugin == 'true'):
                        aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName))
                else:
                   # settings nicht gefunden, also schalten wir es trotzdem sichtbar
                   aPlugins.append(self.__createAvailablePluginsItem(sSiteName, sFileName))

        return aPlugins

    def __createAvailablePluginsItem(self, sPluginName, sPluginIdentifier):
        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        return aPluginEntry