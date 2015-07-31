from resources.lib.config import cConfig


# sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources', 'lib'))
# sys.path.append (sLibrary)
# sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources', 'lib', 'gui'))
# sys.path.append (sLibrary)
# sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources', 'lib', 'handler'))
# sys.path.append (sLibrary)
# sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources','sites'))
# sys.path.append (sLibrary)
# sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources','hosters'))
# sys.path.append (sLibrary)

from resources.lib.statistic import cStatistic
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.favourite import cFav
from resources.lib.about import cAbout
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.config import cConfig
from resources.lib.db import cDb

class main:
    def __init__(self):
        self.parseUrl()
        cDb()._create_tables()

    def parseUrl(self):
	    oInputParameterHandler = cInputParameterHandler()

	    if (oInputParameterHandler.exist('function')):
	        sFunction = oInputParameterHandler.getValue('function')
	    else:
	        cConfig().log('call load methode')
	        sFunction = "load"

            
	    if (sFunction=='DoNothing'):
	        return

	    if (oInputParameterHandler.exist('site')):
	        sSiteName = oInputParameterHandler.getValue('site')
	        cConfig().log('load site ' + sSiteName + ' and call function ' + sFunction)
	        cStatistic().callStartPlugin(sSiteName)

	        if (isHosterGui(sSiteName, sFunction) == True):
	            return
	        
	        if (isGui(sSiteName, sFunction) == True):
	            return
	            
	        if (isFav(sSiteName, sFunction) == True):
	            return

	        if (isHome(sSiteName, sFunction) == True):
	            return

	        #if (isAboutGui(sSiteName, sFunction) == True):            
	            #return

	        #try:
	        exec "from resources.sites import " + sSiteName + " as plugin"
	        exec "plugin."+ sFunction +"()"
	        #except:
	        #    cConfig().log('could not load site: ' + sSiteName )
	    else:

	        if (cConfig().getSetting("home-view") == 'true'):
	            oHome = cHome()
	            cAbout()
	            exec "oHome."+ sFunction +"()"
	            return

	        oGui = cGui()
	        oPluginHandler = cPluginHandler()
	        aPlugins = oPluginHandler.getAvailablePlugins()
	        if (len(aPlugins) == 0):
	            oGui.openSettings()
		    oGui.updateDirectory()
	        else:
	            for aPlugin in aPlugins:
                    
	                # oGuiElement = cGuiElement()
	                # oGuiElement.setTitle(aPlugin[0])
	                # oGuiElement.setSiteName(aPlugin[1])
	                # oGuiElement.setDescription(aPlugin[2])
	                # oGuiElement.setFunction(sFunction)
	                # oGuiElement.setIcon("icon.png")
	                # oGui.addFolder(oGuiElement)
                    
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', 'test')
                        oGui.addDir(aPlugin[1], sFunction, aPlugin[0], 'icon.png', oOutputParameterHandler)

	        oGui.setEndOfDirectory()
	

def isHosterGui(sSiteName, sFunction):
    if (sSiteName == 'cHosterGui'):
        oHosterGui = cHosterGui()
        exec "oHosterGui."+ sFunction +"()"
        return True
    return False
    
def isGui(sSiteName, sFunction):
    if (sSiteName == 'cGui'):
        oGui = cGui()
        exec "oGui."+ sFunction +"()"
        return True
    return False
    
def isFav(sSiteName, sFunction):
    if (sSiteName == 'cFav'):
        oFav = cFav()
        exec "oFav."+ sFunction +"()"
        return True
    return False

def isHome(sSiteName, sFunction):
    if (sSiteName == 'cHome'):
        oHome = cHome()
        exec "oHome."+ sFunction +"()"
        return True
    return False

main()

#import vstream
#vstream.run()
