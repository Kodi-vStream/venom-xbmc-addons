from about.about import cAboutGui
from resources.lib.statistic import cStatistic
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
import logger

def run():        
    parseUrl()

def parseUrl():
    oInputParameterHandler = cInputParameterHandler()

    if (oInputParameterHandler.exist('function')):
        sFunction = oInputParameterHandler.getValue('function')
    else:
        logger.info('call load methode')
        sFunction = "load"

    if (oInputParameterHandler.exist('site')):
        sSiteName = oInputParameterHandler.getValue('site')
        logger.info('load site ' + sSiteName + ' and call function ' + sFunction)

        if (sFunction == 'load'):
            cStatistic().callStartPlugin(sSiteName)

        if (isHosterGui(sSiteName, sFunction) == True):
            return

        if (isAboutGui(sSiteName, sFunction) == True):            
            return

        #try:
        exec "import " + sSiteName + " as plugin"
        exec "plugin."+ sFunction +"()"
        #except:
        #    logger.fatal('could not load site: ' + sSiteName )
    else:
        oGui = cGui()
        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins()
        if (len(aPlugins) == 0):
            oGui.openSettings()
	    oGui.updateDirectory()
        else:
            for aPlugin in aPlugins:
                oGuiElement = cGuiElement()
                oGuiElement.setTitle(aPlugin[0])
                oGuiElement.setSiteName(aPlugin[1])
                oGuiElement.setFunction(sFunction)
                oGui.addFolder(oGuiElement)

        oGui.setEndOfDirectory()

def isHosterGui(sSiteName, sFunction):
    if (sSiteName == 'cHosterGui'):
        oHosterGui = cHosterGui()
        exec "oHosterGui."+ sFunction +"()"
        return True
    return False

def isAboutGui(sSiteName, sFunction):
    if (sSiteName == 'cAboutGui'):
        oAboutGui = cAboutGui()
        exec "oAboutGui."+ sFunction +"()"
        return True
    return False
