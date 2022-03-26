# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import traceback
import threading
import xbmc

from resources.lib.gui.gui import cGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window
from resources.lib.util import Quote

class cSearch:

    def __init__(self):
        self.addons = addon()

    def searchGlobal(self):
        try:
            oInputParameterHandler = cInputParameterHandler()
            sSearchText = oInputParameterHandler.getValue('searchtext')
            sCat = oInputParameterHandler.getValue('sCat')

            listPlugins = self._initSearch(sSearchText, sCat)

            if len(listPlugins) == 0:
                return True

            listThread = self._launchSearch(listPlugins, self._pluginSearch, [Quote(sSearchText), True])
            self._finishSearch(listThread)

            oGui = cGui()
            oGui.addText('globalSearch', self.addons.VSlang(30081) % sSearchText, 'search.png')

            total = count = 0
            searchResults = oGui.getSearchResult()
            values = searchResults.values()
            for result in values:
                total += len(result)
            self._progressClose()

            if total:
                xbmc.sleep(500)    # Nécessaire pour enchainer deux progressBar
                # Progress de chargement des metadata
                progressMeta = progress().VScreate(self.addons.VSlang(30076) + ' - ' + sSearchText, large = total > 50)
                for plugin in listPlugins:
                    pluginId = plugin['identifier']
                    if pluginId in searchResults.keys() and (len(searchResults[pluginId]) > 0): # Au moins un résultat
                        # nom du site
                        count += 1
                        oGui.addText(pluginId, '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']),
                            'sites/%s.png' % (pluginId))

                        # résultats du site
                        for result in searchResults[pluginId]:
                            progressMeta.VSupdate(progressMeta, total)
                            if progressMeta.iscanceled():
                                break
                            oGui.addFolder(result['guiElement'], result['params'])
                        if progressMeta.iscanceled():
                            break

                progressMeta.VSclose(progressMeta)
            
            else: # aucune source ne retourne de résultat
                oGui.addText('globalSearch') # "Aucune information"

            cGui.CONTENT = 'files'

            oGui.setEndOfDirectory()

        except Exception as error:
            VSlog('Error with searchGlobal: ' + str(error))
            traceback.print_exc()
            self._progressForceClose()

        return True


    def _progressInit(self):
        self.progress_ = progress().VScreate(large=True)


    def _progressUpdate(self):
        searchResults = cGui().getSearchResult()
        numberResult = 0
        values = searchResults.values()
        for result in values:
            numberResult += len(result)
        message = "\n"
        message += (self.addons.VSlang(31209) % numberResult)
        message += "\n"
        message += (self.addons.VSlang(31208) % (", ".join(self.listRemainingPlugins[0:7])))
        if len(self.listRemainingPlugins) > 7:
            message += ", ..."
        self.progress_.VSupdate(self.progress_, self.progressTotal, message, True)


    def _progressClose(self):
        self.progress_.VSclose(self.progress_)


    def _progressForceClose(self):
        progress().VSclose()


    def _getAvailablePlugins(self, searchText, categorie):
        oHandler = cRechercheHandler()
        oHandler.setText(searchText)
        oHandler.setCat(categorie)
        return oHandler.getAvailablePlugins()


    def _initSearch(self, searchText, searchCat):
        try:
            listPlugins = self._getAvailablePlugins(searchText, searchCat)
            if not listPlugins:
                return []

            self.progressTotal = len(listPlugins)
            self._progressInit()

            self.listRemainingPlugins = [plugin['name'] for plugin in listPlugins]
            cGui().resetSearchResult()
            return listPlugins
        except Exception as error:
            VSlog('Error when search is initiate: ' + str(error))
            traceback.print_exc()
            self._progressForceClose()
            return []

    def _launchSearch(self, listPlugins, targetFunction, argsList):
        listThread = []
        window(10101).setProperty('search', 'true')
        for plugin in listPlugins:
            thread = threading.Thread(target = targetFunction, args = tuple([plugin] + argsList))
            thread.start()
            listThread.append(thread)

        return listThread

    def _finishSearch(self, listThread):
        # On attend que les thread soient finis
        for thread in listThread:
            thread.join()
        
        window(10101).setProperty('search', 'false')


    def _pluginSearch(self, plugin, sSearchText, updateProcess = False):
        try:
            plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
            function = getattr(plugins, plugin['search'][1])
            sUrl = plugin['search'][0] + str(sSearchText)

            function(sUrl)
            if updateProcess:
                self.listRemainingPlugins.remove(plugin['name'])
                self._progressUpdate()

            VSlog('Load Search: ' + str(plugin['identifier']))
        except Exception as e:
            VSlog(plugin['identifier'] + ': search failed (' + str(e) + ')')


