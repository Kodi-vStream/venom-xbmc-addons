from resources.lib.config import cConfig


sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources', 'lib'))
sys.path.append (sLibrary)
sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources', 'lib', 'gui'))
sys.path.append (sLibrary)
sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'resources', 'lib', 'handler'))
sys.path.append (sLibrary)
sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'sites'))
sys.path.append (sLibrary)
sLibrary            = xbmc.translatePath(os.path.join(cConfig().getAddonPath(), 'hosters'))
sys.path.append (sLibrary)

from resources.lib.statistic import cStatistic
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.favourite import cFav
from resources.lib.about import cAbout
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler

class main:
    def __init__(self):
        self.parseUrl()


    def parseUrl(self):
	    oInputParameterHandler = cInputParameterHandler()

	    if (oInputParameterHandler.exist('function')):
	        sFunction = oInputParameterHandler.getValue('function')
	    else:
	        cConfig().log('call load methode')
	        sFunction = "load"

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
	        exec "import " + sSiteName + " as plugin"
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
	                oGuiElement = cGuiElement()
	                oGuiElement.setTitle(aPlugin[0])
	                oGuiElement.setSiteName(aPlugin[1])
	                oGuiElement.setDescription(aPlugin[2])
	                oGuiElement.setFunction(sFunction)
	                oGuiElement.setIcon("icon.png")
	                oGui.addFolder(oGuiElement)

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