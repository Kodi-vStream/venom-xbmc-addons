# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc

# from resources.lib.statistic import cStatistic
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window
from resources.lib.search import cSearch
# http://kodi.wiki/view/InfoLabels
# http://kodi.wiki/view/List_of_boolean_conditions


####################
#
#  Permet de debuguer avec Eclipse
#
# Tuto ici :
# https://github.com/Kodi-vStream/venom-xbmc-addons/wiki
#
####################

# Mettre True pour activer le debug
DEBUG = False

if DEBUG:

    import sys  # pydevd module need to be copied in Kodi\system\python\Lib\pysrc
    sys.path.append('H:\Program Files\Kodi\system\Python\Lib\pysrc')

    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        try:
            import pydevd  # with the addon script.module.pydevd, only use `import pydevd`
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class main:

    def __init__(self):
        self.parseUrl()

    def parseUrl(self):
        # Exclue les appels par des plugins qu'on ne sait pas gérer, par exemple :  plugin://plugin.video.vstream/extrafanart
        oPluginHandler = cPluginHandler()
        pluginPath = oPluginHandler.getPluginPath()
        if pluginPath == 'plugin://plugin.video.vstream/extrafanart/':
            return

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

        if sFunction == 'setSettings':
            setSettings(oInputParameterHandler)
            return

        if sFunction == 'DoNothing':
            return

        if not oInputParameterHandler.exist('site'):
            # charge home
            plugins = __import__('resources.lib.home', fromlist=['home']).cHome()
            function = getattr(plugins, 'load')
            function()
            return

        if oInputParameterHandler.exist('site'):
            sSiteName = oInputParameterHandler.getValue('site')
            VSlog('load site ' + sSiteName + ' and call function ' + sFunction)

            if isHosterGui(sSiteName, sFunction):
                return

            if isGui(sSiteName, sFunction):
                return

            if isFav(sSiteName, sFunction):
                return

            if isViewing(sSiteName, sFunction):
                return

            if isLibrary(sSiteName, sFunction):
                return

            if isDl(sSiteName, sFunction):
                return

            if isHome(sSiteName, sFunction):
                return

            if isTrakt(sSiteName, sFunction):
                return

            if isSearch(sSiteName, sFunction):
                return

            if sSiteName == 'globalRun':
                __import__('resources.lib.runscript', fromlist=['runscript'])
                # function = getattr(plugins, sFunction)
                # function()
                return

            if sSiteName == 'globalSources':
                oGui = cGui()
                aPlugins = oPluginHandler.getAvailablePlugins(force=True)

                if len(aPlugins) == 0:
                    addons = addon()
                    addons.openSettings()
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
                addons = addon()
                addons.openSettings()
                return
            # if isAboutGui(sSiteName, sFunction) == True:
                # return

            # charge sites
            try:
                plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
                function = getattr(plugins, sFunction)
                function()
            except Exception as e:
                progress().VSclose()  # Referme le dialogue en cas d'exception, sinon blocage de Kodi
                VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
                import traceback
                traceback.print_exc()
                return


def setSetting(plugin_id, value):
    addons = addon()
    setting = addons.getSetting(plugin_id)

    # modifier si différent
    if setting != value:
        addons.setSetting(plugin_id, value)
        return True

    return False


# Permet la modification des settings depuis un raccourci dans le skin (jusqu'à 100 paramètres).
# Supporte les retours à la ligne seulement derrière le paramètre, exemple :
# RunAddon(plugin.video.vstream,function=setSettings&id1=plugin_cinemay_com&value1=true
# &id2=plugin_cinemegatoil_org&value2=false
# &id3=hoster_uploaded_premium&value3=true
# &id4=hoster_uploaded_username&value4=MyName
# &id5=hoster_uploaded_password&value5=MyPass)
def setSettings(oInputParameterHandler):
    addons = addon()

    for i in range(1, 100):
        plugin_id = oInputParameterHandler.getValue('id' + str(i))
        if plugin_id:
            value = oInputParameterHandler.getValue('value' + str(i))
            value = value.replace('\n', '')
            oldSetting = addons.getSetting(plugin_id)
            # modifier si différent
            if oldSetting != value:
                addons.setSetting(plugin_id, value)

    return True


def isHosterGui(sSiteName, sFunction):
    if sSiteName == 'cHosterGui':
        plugins = __import__('resources.lib.gui.hoster', fromlist=['cHosterGui']).cHosterGui()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isGui(sSiteName, sFunction):
    if sSiteName == 'cGui':
        oGui = cGui()
        exec("oGui." + sFunction + "()")
        return True
    return False


def isFav(sSiteName, sFunction):
    if sSiteName == 'cFav':
        plugins = __import__('resources.lib.bookmark', fromlist=['cFav']).cFav()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isViewing(sSiteName, sFunction):
    if sSiteName == 'cViewing':
        plugins = __import__('resources.lib.viewing', fromlist=['cViewing']).cViewing()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isLibrary(sSiteName, sFunction):
    if sSiteName == 'cLibrary':
        plugins = __import__('resources.lib.library', fromlist=['cLibrary']).cLibrary()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isDl(sSiteName, sFunction):
    if sSiteName == 'cDownload':
        plugins = __import__('resources.lib.download', fromlist=['cDownload']).cDownload()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isHome(sSiteName, sFunction):
    if sSiteName == 'cHome':
        oHome = cHome()
        exec("oHome." + sFunction + "()")
        return True
    return False


def isTrakt(sSiteName, sFunction):
    if sSiteName == 'cTrakt':
        plugins = __import__('resources.lib.trakt', fromlist=['cTrakt']).cTrakt()
        function = getattr(plugins, sFunction)
        function()
        return True
    return False


def isSearch(sSiteName, sFunction):
    if sSiteName == 'globalSearch':
        oSearch = cSearch()
        exec("oSearch.searchGlobal()")
        return True
    return False


def _pluginSearch(plugin, sSearchText):

    # Appeler la source en mode Recherche globale
    window(10101).setProperty('search', 'true')

    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0] + str(sSearchText)

        function(sUrl)

        VSlog('Load Search: ' + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')


main()
