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
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.config import cConfig
from resources.lib.db import cDb

import xbmc, xbmcgui, sys

class main:
    def __init__(self):
        #print 'Debug 0'
        self.parseUrl()
        cDb()._create_tables()

    def parseUrl(self):

        #print sys.argv

        #print 'Debug 1'
        oInputParameterHandler = cInputParameterHandler()
        #print 'Debug 2'
        if (oInputParameterHandler.exist('function')):
            #print 'Debug 3'
            sFunction = oInputParameterHandler.getValue('function')
        else:
            #print 'Debug 4'
            cConfig().log('call load methode')
            sFunction = "load"

        #print 'Debug 5'
        if (sFunction=='DoNothing'):
            return

        if (not oInputParameterHandler.exist('site')):            
            plugins = __import__('resources.lib.home', fromlist=['home']).cHome()
            function = getattr(plugins, 'load')
            function()
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

            if (isLibrary(sSiteName, sFunction) == True):
                return

            if (isDl(sSiteName, sFunction) == True):
                return

            if (isHome(sSiteName, sFunction) == True):
                return

            if (isTrakt(sSiteName, sFunction) == True):
                return
                
            if sSiteName == 'globalSearch':
                searchGlobal()
                return
                
            if sSiteName == 'globalSources':
            
                oGui = cGui()
                oPluginHandler = cPluginHandler()
                aPlugins = oPluginHandler.getAvailablePlugins()
                if (len(aPlugins) == 0):
                    oGui.openSettings()
                    oGui.updateDirectory()
                else:
                    for aPlugin in aPlugins:
                    
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                        icon = 'sites/%s.png' % (aPlugin[1])
                        oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)

                oGui.setEndOfDirectory()
                return

            if sSiteName == 'globalParametre':
                oGui = cGui()
                oGui.openSettings()
                oGui.updateDirectory()
                return
            #if (isAboutGui(sSiteName, sFunction) == True):
                #return

            #charge Home
            try:
                from resources.lib.about import cAbout
                cAbout().getUpdate()
                #exec "from resources.lib.about import cAbout as plugin"
                #exec "plugin.getUpdate()"
            except:
                pass
            try:
            #exec "from resources.sites import " + sSiteName + " as plugin"
            #exec "plugin."+ sFunction +"()"
                plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
                function = getattr(plugins, sFunction)
                function()
            except:
                cConfig().log('could not load site: ' + sSiteName )
                return
            


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
        from resources.lib.favourite import cFav
        oFav = cFav()
        exec "oFav."+ sFunction +"()"
        return True
    return False

def isLibrary(sSiteName, sFunction):
    if (sSiteName == 'cLibrary'):
        from resources.lib.library import cLibrary
        oLibrary = cLibrary()
        exec "oLibrary."+ sFunction +"()"
        return True
    return False

def isDl(sSiteName, sFunction):
    if (sSiteName == 'cDownload'):
        from resources.lib.download import cDownload
        oDownload = cDownload()
        exec "oDownload."+ sFunction +"()"
        return True
    return False

def isHome(sSiteName, sFunction):
    if (sSiteName == 'cHome'):
        oHome = cHome()
        exec "oHome."+ sFunction +"()"
        return True
    return False

def isTrakt(sSiteName, sFunction):
    if (sSiteName == 'cTrakt'):
        from resources.lib.trakt import cTrakt
        oTrakt = cTrakt()
        exec "oTrakt."+ sFunction +"()"
        return True
    return False

def searchGlobal():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSearchText = oInputParameterHandler.getValue('searchtext')
    sReadDB = oInputParameterHandler.getValue('readdb')
    sDisp = oInputParameterHandler.getValue('disp')

    oHandler = cRechercheHandler()
    sSearchText = oHandler.setText(sSearchText)
    oHandler.setDisp(sDisp)
    oHandler.setRead(sReadDB)
    aPlugins = oHandler.getAvailablePlugins()
    if not aPlugins: return True
    total = len(aPlugins)
    
    #xbmc.log(str(aPlugins), xbmc.LOGNOTICE)
    
    dialog = cConfig().createDialog("vStream")
    xbmcgui.Window(10101).setProperty('search', 'true')
    
    oGui.addText2('globalSearch', '[COLOR khaki]%s: %s[/COLOR]' % (cConfig().getlanguage(30076), sSearchText), 'none.png')
    
    for count, plugin in enumerate(aPlugins):
    
        xbmc.log(str(plugin['name']), xbmc.LOGNOTICE)
        text = '%s/%s - %s' % ((count+1), total, plugin['name'])
        cConfig().updateDialogSearch(dialog, total, text)
        if dialog.iscanceled():
            break
        
        #nom du site
        oGui.addText2(plugin['identifier'], '%s. [COLOR olive]%s[/COLOR]' % ((count+1), plugin['name']), 'sites/%s.png' % (plugin['identifier']))
        #recherche import
        _pluginSearch(plugin, sSearchText)
        
    
    
    xbmcgui.Window(10101).setProperty('search', 'false')
    cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

    return True
    
def _pluginSearch(plugin, sSearchText):
    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0]+str(sSearchText)
        function(sUrl)      
        cConfig().log("Load Recherche: " + str(plugin['identifier']))
    except:
        cConfig().log(plugin['identifier']+': search failed')
        
main()

#import vstream
#vstream.run()
