# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

# from resources.lib.statistic import cStatistic
from resources.lib.gui.hoster import cHosterGui
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb
from resources.lib.comaddon import progress, VSlog, addon, window, xbmc
from resources.lib.util import Quote
# http://kodi.wiki/view/InfoLabels
# http://kodi.wiki/view/List_of_boolean_conditions


####################
#
#  Permet de debuguer avec Eclipse
#
# Tuto ici :
# https://github.com/Kodi-vStream/venom-xbmc-addons/issues/2739
#
####################

DEBUG = False  # Mettre True pour activer le debug

if DEBUG:

####################
#
# Version WINDOWS
#
####################

    # append pydev remote debugger
    import sys
    sys.path.append('C:\Program Files (x86)\Kodi\system\Python\Lib\pysrc')

    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
        pydevd.settrace('localhost', stdoutToServer = True, stderrToServer = True)
    except ImportError:
        sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")

####################
#
# Version LINUX
#
####################

    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
#     try:
#         import pydevd
#         pydevd.settrace('localhost', stdoutToServer = True, stderrToServer = True)
#     except ImportError:
#         sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class main:

    def __init__(self):
        self.parseUrl()
        # Ne pas desactiver la ligne d'en dessous, car sinon ca genere
        # des probleme de Db sous Android.
        cDb()._create_tables()

    def parseUrl(self):

        # import sys
        # xbmc.log('arg :' + str(sys.argv), xbmc.LOGNOTICE)
        # xbmc.log('Debug 1 >>' + str(xbmc.getInfoLabel('Container().CurrentPage')), xbmc.LOGNOTICE)
        # xbmc.log('Debug 2 >>' + str(xbmc.getInfoLabel('Container.FolderPath')), xbmc.LOGNOTICE)

        oInputParameterHandler = cInputParameterHandler()

        if oInputParameterHandler.exist('function'):
            sFunction = oInputParameterHandler.getValue('function')
        else:
            VSlog('call load methode')
            sFunction = "load"

        if sFunction == 'setSetting':
            if oInputParameterHandler.exist('id'):
                plugin_id = oInputParameterHandler.getValue('id')
            else:
                return

            if oInputParameterHandler.exist('value'):
                value = oInputParameterHandler.getValue('value')
            else:
                return

            setSetting(plugin_id, value)
            return

        if sFunction == 'DoNothing':
            return

        if not oInputParameterHandler.exist('site'):

            # mise a jour
            try:
                # from resources.lib.about import cAbout
                # cAbout().getUpdate()
                plugins = __import__('resources.lib.about', fromlist = ['about']).cAbout()
                function = getattr(plugins, 'getUpdate')
                function()
            except:
                pass

            # charge home
            plugins = __import__('resources.lib.home', fromlist = ['home']).cHome()
            function = getattr(plugins, 'load')
            function()
            return

        if oInputParameterHandler.exist('site'):
            sSiteName = oInputParameterHandler.getValue('site')
            #if oInputParameterHandler.exist('title'):
                #sTitle = oInputParameterHandler.getValue('title')
            #else:
                #sTitle = 'none'

            VSlog('load site ' + sSiteName + ' and call function ' + sFunction)
            # cStatistic().callStartPlugin(sSiteName, sTitle)

            if isHosterGui(sSiteName, sFunction):
                return

            if isGui(sSiteName, sFunction):
                return

            if isFav(sSiteName, sFunction):
                return

            if isLibrary(sSiteName, sFunction):
                return

            if isDl(sSiteName, sFunction):
                return

            if isHome(sSiteName, sFunction):
                return

            if isTrakt(sSiteName, sFunction):
                return

            if sSiteName == 'globalSearch':
                searchGlobal()
                return

            if sSiteName == 'globalRun':
                __import__('resources.lib.runscript', fromlist = ['runscript'])
                # function = getattr(plugins, sFunction)
                # function()
                return

            if sSiteName == 'globalSources':
                oGui = cGui()
                oPluginHandler = cPluginHandler()
                aPlugins = oPluginHandler.getAvailablePlugins(True)

                if len(aPlugins) == 0:
                    addons = addon()
                    addons.openSettings()
                    xbmc.executebuiltin('Container.Refresh')
                else:
                    for aPlugin in aPlugins:
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                        icon = 'sites/%s.png' % (aPlugin[1])
                        # icon = 'https://imgplaceholder.com/512x512/transparent/fff?text=%s&font-family=Roboto_Bold' % aPlugin[1]
                        oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)

                oGui.setEndOfDirectory()
                return

            if sSiteName == 'globalParametre':
                addons = addon()
                addons.openSettings()
                return
            # if isAboutGui(sSiteName, sFunction) == True:
                # return

            # charge sites
            try:
            # exec "from resources.sites import " + sSiteName + " as plugin"
            # exec "plugin." + sFunction + "()"
                plugins = __import__('resources.sites.%s' % sSiteName, fromlist = [sSiteName])
                function = getattr(plugins, sFunction)
                function()
            except Exception as e:
                progress().VSclose() # Referme le dialogue en cas d'exception, sinon blocage de Kodi
                VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
                import traceback
                traceback.print_exc()
                return


def setSetting(plugin_id, value):
    addons = addon()
    setting = addons.getSetting(plugin_id)

    # Si le parametre existe, on autorise la modification
    if setting != '' and setting != value:
        addons.setSetting(plugin_id, value)
        return True

    return False


def isHosterGui(sSiteName, sFunction):
    if sSiteName == 'cHosterGui':
        oHosterGui = cHosterGui()
        exec ("oHosterGui." + sFunction + "()")
        return True
    return False


def isGui(sSiteName, sFunction):
    if sSiteName == 'cGui':
        oGui = cGui()
        exec ("oGui." + sFunction + "()")
        return True
    return False


def isFav(sSiteName, sFunction):
    if sSiteName == 'cFav':
        from resources.lib.bookmark import cFav
        oFav = cFav()
        exec ("oFav." + sFunction + "()")
        return True
    return False


def isLibrary(sSiteName, sFunction):
    if sSiteName == 'cLibrary':
        from resources.lib.library import cLibrary
        oLibrary = cLibrary()
        exec ("oLibrary." + sFunction + "()")
        return True
    return False


def isDl(sSiteName, sFunction):
    if sSiteName == 'cDownload':
        from resources.lib.download import cDownload
        oDownload = cDownload()
        exec ("oDownload." + sFunction + "()")
        return True
    return False


def isHome(sSiteName, sFunction):
    if sSiteName == 'cHome':
        oHome = cHome()
        exec ("oHome." + sFunction + "()")
        return True
    return False


def isTrakt(sSiteName, sFunction):
    if sSiteName == 'cTrakt':
        from resources.lib.trakt import cTrakt
        oTrakt = cTrakt()
        exec ("oTrakt." + sFunction + "()")
        return True
    return False


def searchGlobal():
    oGui = cGui()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    sSearchText = oInputParameterHandler.getValue('searchtext')
    sCat = oInputParameterHandler.getValue('sCat')

    oHandler = cRechercheHandler()
    oHandler.setText(sSearchText)
    oHandler.setCat(sCat)
    aPlugins = oHandler.getAvailablePlugins()
    if not aPlugins:
        return True

    total = len(aPlugins)
    progress_ = progress().VScreate()

    # kodi 17 vire la fenetre busy qui se pose au dessus de la barre de Progress
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
    except:
        pass

    oGui.addText('globalSearch', addons.VSlang(30081) % sSearchText, 'none.png')
    sSearchText = Quote(sSearchText)

    count = 0
    for plugin in aPlugins:
 
        progress_.VSupdate(progress_, total, plugin['name'], True)
        if progress_.iscanceled():
            progress_.close()
            break
 
        oGui.searchResults[:] = []  # vider le tableau de résultats pour les récupérer par source
        _pluginSearch(plugin, sSearchText)

        if len(oGui.searchResults) > 0: # Au moins un résultat
            count += 1

            # nom du site
            oGui.addText(plugin['identifier'], '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']), 'sites/%s.png' % (plugin['identifier']))
            for result in oGui.searchResults:
                oGui.addFolder(result['guiElement'], result['params'])
 
    if not count:   # aucune source ne retourne de résultats
        oGui.addText('globalSearch') # "Aucune information"

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
    return True


def _pluginSearch(plugin, sSearchText):

    # Appeler la source en mode Recherche globale
    window(10101).setProperty('search', 'true')
    
    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist = [plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0] + str(sSearchText)
        
        function(sUrl)
        
        VSlog('Load Search: ' + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')


main()
