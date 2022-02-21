# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import traceback
import xbmc

# from resources.lib.statistic import cStatistic
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window
from resources.lib.util import Quote
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
    sys.path.append(r'H:\Program Files\Kodi\system\Python\Lib\pysrc')

    try:
        from pysrc import pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        try:
            import pydevd  # with the addon script.module.pydevd, only use `import pydevd`
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")

class Main(object):

    def __init__(self):
        self.plugin_handler = cPluginHandler()
        self.parse_url()

    def parse_url(self):
        # Exclue les appels par des plugins qu'on ne sait pas gérer, par exemple:
        # plugin://plugin.video.vstream/extrafanart
        plugin_path = self.plugin_handler.getPluginPath()
        if plugin_path == 'plugin://plugin.video.vstream/extrafanart/':
            return

        input_parameter_handler = cInputParameterHandler()

        # Get SiteName
        if input_parameter_handler.exist('site'):
            self.site_name = input_parameter_handler.getValue('site')
        else:
            self.site_name = 'cHome'
            self.function_name = 'load'

        # Get function_name
        if input_parameter_handler.exist('function'):
            self.function_name = input_parameter_handler.getValue('function')
        else:
            VSlog('call load methode')
            self.function_name = "load"

        if self.function_name == 'setSetting':
            set_setting(input_parameter_handler)
            return

        elif self.function_name == 'setSettings':
            set_settings(input_parameter_handler)
            return

        elif self.function_name == 'DoNothing':
            return

        self.parse_url_for_site()

    def parse_url_for_site(self):
        VSlog('load site ' + self.site_name + ' and call function ' + self.function_name)

        list_action = {
            'cHosterGui': 'resources.lib.gui.hoster',
            'cGui': 'resources.lib.gui.gui',
            'cFav': 'resources.lib.bookmark',
            'cViewing': 'resources.lib.viewing',
            'cLibrary': 'resources.lib.library',
            'cDownload': 'resources.lib.download',
            'cHome': 'resources.lib.home',
            'cTrakt': 'resources.lib.trakt'
        }

        for action in list_action:
            if self.try_to_call_method(action, list_action[action]):
                return

        if self.site_name == 'globalSearch':
            search_global()

        elif self.site_name == 'globalRun':
            __import__('resources.lib.runscript', fromlist=['runscript'])
            # function = getattr(plugins, function_name)
            # function()

        elif self.site_name == 'globalSources':
            gui = cGui()
            list_plugins = self.plugin_handler.getAvailablePlugins(force=True)

            if len(list_plugins) == 0:
                addons = addon()
                addons.openSettings()
                gui.updateDirectory()
            else:
                for plugin in list_plugins:
                    output_parameter_handler = cOutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', 'http://venom')
                    icon = 'sites/%s.png' % (plugin[1])
                    gui.addDir(plugin[1], 'load', plugin[0], icon, output_parameter_handler)

            gui.setEndOfDirectory()

        elif self.site_name == 'globalParametre':
            addons = addon()
            addons.openSettings()

        else:
            # charge sites
            try:
                plugins = __import__('resources.sites.%s' % self.site_name, fromlist=[self.site_name])
                function = getattr(plugins, self.function_name)
                function()
            except Exception as error:
                progress().VSclose()  # Referme le dialogue en cas d'exception, sinon blocage de Kodi
                VSlog('could not load site: ' + self.site_name + ' error: ' + str(error))
                traceback.print_exc()


    def try_to_call_method(self, action_site_name, path):
        if self.site_name == action_site_name:
            imported_plugin = __import__(path, fromlist=[self.site_name])
            plugin_object = getattr(imported_plugin, self.site_name)()
            function = getattr(plugin_object, self.function_name)
            function()
            return True
        return False


def set_setting(input_parameter_handler):
    if not (input_parameter_handler.exist('id') or input_parameter_handler.exist('value')):
        return

    plugin_id = input_parameter_handler.getValue('id')
    value = input_parameter_handler.getValue('value')

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
def set_settings(input_parameter_handler):
    addons = addon()

    for i in range(1, 100):
        plugin_id = input_parameter_handler.getValue('id' + str(i))
        if plugin_id:
            value = input_parameter_handler.getValue('value' + str(i))
            value = value.replace('\n', '')
            old_setting = addons.getSetting(plugin_id)
            # modifier si différent
            if old_setting != value:
                addons.setSetting(plugin_id, value)

    return True

def search_global():
    gui = cGui()
    addons = addon()

    input_parameter_handler = cInputParameterHandler()
    search_text = input_parameter_handler.getValue('searchtext')
    categorie = input_parameter_handler.getValue('sCat')

    recherche_handler = cRechercheHandler()
    recherche_handler.setText(search_text)
    recherche_handler.setCat(categorie)
    list_plugins = recherche_handler.getAvailablePlugins()
    if not list_plugins:
        return True

    total = len(list_plugins)
    progress_ = progress().VScreate(large=True)

    # kodi 17 vire la fenetre busy qui se pose au dessus de la barre de Progress
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
    except Exception:
        pass

    gui.addText('globalSearch', addons.VSlang(30081) % search_text, 'search.png')
    search_text = Quote(search_text)

    count = 0
    for plugin in list_plugins:

        progress_.VSupdate(progress_, total, plugin['name'], True)
        if progress_.iscanceled():
            break

        gui.searchResults[:] = []  # vider le tableau de résultats pour les récupérer par source
        _plugin_search(plugin, search_text)

        if len(gui.searchResults) > 0:  # Au moins un résultat
            count += 1

            # nom du site
            gui.addText(plugin['identifier'], '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']),
                'sites/%s.png' % (plugin['identifier']))
            for result in gui.searchResults:
                gui.addFolder(result['guiElement'], result['params'])

    if not count:   # aucune source ne retourne de résultats
        gui.addText('globalSearch')  # "Aucune information"

    progress_.VSclose(progress_)

    cGui.CONTENT = 'files'

    gui.setEndOfDirectory()
    return True


def _plugin_search(plugin, search_text):

    # Appeler la source en mode Recherche globale
    window(10101).setProperty('search', 'true')

    try:
        plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        url = plugin['search'][0] + str(search_text)
        function(url)

        VSlog('Load Search: ' + str(plugin['identifier']))
    except Exception:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')


Main()
