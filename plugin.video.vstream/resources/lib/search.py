# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import traceback
import threading
import xbmc

from resources.lib.gui.gui import cGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window
from resources.lib.util import Quote

SITE_IDENTIFIER = 'cSearch'
SITE_NAME = 'Search'


class cSearch:

    MAX_NUMBER_CRITERIA = 5

    def __init__(self):
        self.addons = addon()
        self.autoPlayVideo = False
        self.findAndPlay = False

    def load(self):
        cGui().setEndOfDirectory()

    def searchGlobal(self, sSearchText='', sCat=''):
        try:
            if not sSearchText:
                oInputParameterHandler = cInputParameterHandler()
                sSearchText = oInputParameterHandler.getValue('searchtext')
                sCat = oInputParameterHandler.getValue('sCat')

            sSearchText = sSearchText.replace(':', ' ')

            listPlugins = self._initSearch(sSearchText, sCat)

            if len(listPlugins) == 0:
                return True

            listThread = self._launchSearch(listPlugins, self._pluginSearch, [Quote(sSearchText), True])
            self._finishSearch(listThread)

            oGui = cGui()
            oGui.addText('globalSearch', self.addons.VSlang(30081) % sSearchText, 'search.png')

            count = 0
            searchResults = cGui().getSearchResult()
            for plugin in listPlugins:
                pluginId = plugin['identifier']
                if pluginId in searchResults.keys() and (len(searchResults[pluginId]) > 0): # Au moins un résultat
                    count += 1

                    # nom du site
                    oGui.addText(pluginId, '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']),
                                 'sites/%s.png' % (pluginId))
                    for result in searchResults[pluginId]:
                        oGui.addFolder(result['guiElement'], result['params'])

            if not count: # aucune source ne retourne de résultats
                oGui.addText('globalSearch') # "Aucune information"

            self._progressClose()
            cGui.CONTENT = 'files'

            oGui.setEndOfDirectory()

        except Exception as error:
            VSlog('Error with searchGlobal: ' + str(error))
            traceback.print_exc()
            self._progressForceClose()

        return True

    def playVideo(self):
        return self.quickSearch(True)

    def _progressInit(self):
        if not self.autoPlayVideo:
            self.progress_ = progress().VScreate(large=True)

    def _progressUpdate(self):
        if not self.autoPlayVideo and not self._progressIsCancel():
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

    def quickSearch(self, autoPlayVideo=False):
        try:
            self.autoPlayVideo = autoPlayVideo

            searchInfo = self._getSearchInfo()
            listPlugins = self._initSearch(searchInfo['title'], searchInfo['cat'])

            if len(listPlugins) == 0:
                return True

            self.findAndPlay = False
            self.allVideoLink = {}
            self.eventFindOneLink = threading.Event()

            window(10101).setProperty('playVideo', 'true')
            listThread = self._launchSearch(listPlugins, self._quickSearchForPlugin, [searchInfo])

            if autoPlayVideo:
                while len(self.listRemainingPlugins) > 0 and self._continueToSearch():
                    self.eventFindOneLink.wait()
                    self.eventFindOneLink.clear()
                    self._tryToAutoPlaySpecificCriteria(cSearch.MAX_NUMBER_CRITERIA)

                if self._continueToSearch():
                    self._tryToAutoPlay()

            self._finishSearch(listThread)
            window(10101).setProperty('playVideo', 'false')
            window(10101).setProperty('search', 'false')

            self._progressClose()

            if not self.findAndPlay:
                self._displayAllResult(searchInfo)

        except Exception as error:
            VSlog('Error with quickSearch: ' + str(error))
            traceback.print_exc()
            self._progressForceClose()

        return True

    def _progressInit(self):
        if not self.autoPlayVideo:
            # kodi 17 vire la fenetre busy qui se pose au dessus de la barre de Progress
            try:
                xbmc.executebuiltin('Dialog.Close(busydialog)')
            except Exception:
                pass

            self.progress_ = progress().VScreate(large=True)


    def _progressUpdate(self):
        if not self.autoPlayVideo and not self._progressIsCancel():
            numberResult = sum(map(len, self.allVideoLink.values()))
            message = "\n"
            message += (self.addons.VSlang(31209) % numberResult)
            message += "\n"
            message += (self.addons.VSlang(31208) % (", ".join(self.listRemainingPlugins[0:5])))
            if len(self.listRemainingPlugins) > 5:
                message += " ..."
            self.progress_.VSupdate(self.progress_, self.progressTotal, message, True)


    def _progressIsCancel(self):
        if not self.autoPlayVideo:
            return self.progress_.iscanceled()
        else:
            return False


    def _progressClose(self):
        if not self.autoPlayVideo:
            self.progress_.VSclose(self.progress_)


    def _progressForceClose(self):
        progress().VSclose()


    def _monitorAbortRequest(self):
        return xbmc.Monitor().abortRequested()


    def _continueToSearch(self):
        return not (self.findAndPlay or self._monitorAbortRequest() or self._progressIsCancel())


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
            cGui.resetSearchResult()
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

            if not self._continueToSearch():
                break

            thread = threading.Thread(target=targetFunction, name=plugin['name'], args=tuple([plugin] + argsList))
            thread.start()
            listThread.append(thread)

        return listThread

    def _finishSearch(self, listThread):
        # On attend que les thread soient fini
        for thread in listThread:
            thread.join()
        window(10101).setProperty('search', 'false')

    def _tryToAutoPlay(self):
        if len(self.allVideoLink) > 0:
            numberMaxCriteria = max(self.allVideoLink.keys())
            for iNumberCriteria in range(numberMaxCriteria, 0, -1):
                self._tryToAutoPlaySpecificCriteria(iNumberCriteria)

    def _tryToAutoPlaySpecificCriteria(self, numberCriteria):
        if numberCriteria in self.allVideoLink:
            for searchResult in self.allVideoLink[numberCriteria]:
                # Si on ne doit pas arrêter de chercher et si on a pas encore tester ce résultat
                if self._continueToSearch() and searchResult['params'].getValue('playTest') == 'false':
                    # On marque le film comme déjà testé
                    searchResult['params'].addParameter('playTest', 'true')
                    # On essaye de le lancer
                    find = self._playHosterGui(searchResult['guiElement'].getFunction(), \
                        [searchResult['params'], True])
                    if find: # Si on a réussi
                        self.findAndPlay = True # On enregistre que tout est bon
                        return

    # Boucle récursive qui permet d'aller simuler le "clic" d'un utilisateur pour naviguer dans les menus
    # Le but étant d'arriver au lien de la vidéo directement
    def _deepSearchLoop(self, searchResult, searchInfo):
        if self._continueToSearch():
            numberOfCriteria = self._getScoreOfThisResult(searchResult, searchInfo)

            if numberOfCriteria > 0:
                videoParams = searchResult['params'] # OutputParameter
                siteId = searchResult['guiElement'].getSiteName()
                functionName = searchResult['guiElement'].getFunction()

                if siteId == 'cHosterGui':
                    if numberOfCriteria not in self.allVideoLink:
                        self.allVideoLink[numberOfCriteria] = []

                    # On note qu'on a pas encore testé ce résultat
                    searchResult['params'].addParameter('playTest', 'false')
                    self.allVideoLink[numberOfCriteria].append(searchResult)

                    # Si on doit autoPlay et qu'on a le maximum de critère
                    if self.autoPlayVideo and numberOfCriteria == cSearch.MAX_NUMBER_CRITERIA:
                        # On signale qu'il faut lancer la vidéo
                        self.eventFindOneLink.set()

                else:
                    videoParams.addParameter('searchSiteId', siteId) # On concerve le site d'origine
                    cGui.emptySearchResult(siteId)
                    self._executePluginForSearch(siteId, functionName, videoParams)

                    pluginResult = cGui.getSearchResult()
                    for newSearchResult in pluginResult[siteId]:
                        if self._continueToSearch():
                            # On garde toutes les données qu'on avait au par avant
                            newSearchResult['params'].mergeUnexistingInfos(videoParams)
                             # On concerve le site d'origine
                            newSearchResult['params'].addParameter('searchSiteId', siteId)

                            if newSearchResult['guiElement'].getSiteName() == siteId and \
                                newSearchResult['guiElement'].getFunction() == functionName:
                                VSlog("Will not loop on the same function: " + str(siteId) + "." + str(functionName))
                            else:
                                self._deepSearchLoop(newSearchResult, searchInfo)
                        else:
                            break


    def _quickSearchForPlugin(self, plugin, searchInfo):
        if self._continueToSearch():
            self._pluginSearch(plugin, Quote(searchInfo['title']))
            searchResults = cGui.getSearchResult()
            pluginId = plugin['identifier']
            pluginName = plugin['name']

        if pluginId in searchResults and len(searchResults[pluginId]) > 0:  # Au moins un résultat
            pluginResult = searchResults[pluginId][:]

            for searchResult in pluginResult:
                searchResult['params'].addParameter('searchSiteName', pluginName)
                self._deepSearchLoop(searchResult, searchInfo)
                if not self._continueToSearch():
                    break
        else:
            VSlog("No result for: " + str(pluginId))
        self.listRemainingPlugins.remove(pluginName)
        self._progressUpdate()

        if len(self.listRemainingPlugins) == 0 and self.autoPlayVideo:
            self.eventFindOneLink.set()

    def _removeNonLetterCaracter(self, word):
        return "".join(re.findall(r'[a-zA-Z0-9 ]*', word, flags=re.I)).strip()

    def _getSearchInfo(self):
        oInputParameterHandler = cInputParameterHandler()

        if oInputParameterHandler.exist('cat'):
            searchCat = int(oInputParameterHandler.getValue('cat'))
        else:
            searchCat = -1

        if oInputParameterHandler.exist('title'):
            searchTitle = self._removeNonLetterCaracter(oInputParameterHandler.getValue('title'))
        else:
            searchTitle = ""

        if oInputParameterHandler.exist('year'):
            searchYear = str(oInputParameterHandler.getValue('year'))
        else:
            searchYear = ""

        return {'title': searchTitle, 'cat': searchCat, 'year': searchYear}


    def _isYearCorrect(self, result, searchInfo):
        resultYear = result['params'].getValue('sYear')
        if resultYear:
            if resultYear != searchInfo['year']:
                return 1
            else:
                # VSlog("Exclude because 'year' not correct: " + str(resultYear))
                return -1
        return 1


    def _isMovieTitleCorrect(self, result, searchInfo):
        resultTitle = result['params'].getValue('sMovieTitle')
        if resultTitle:
            if self._checkAllSearchWordInTitle(searchInfo['title'], resultTitle):
                if searchInfo['title'].lower() == self._removeNonLetterCaracter(resultTitle).lower():
                    return 2
                else:
                    return 1
            else:
                # VSlog("Exclude because 'title' not correct: " + str(resultTitle))
                return -1
        return 0


    def _isLangCorrect(self, result, searchInfo):
        resultLang = str(result['params'].getValue('sLang')).lower()
        autoPlayLang = self.addons.getSetting('autoPlayLang') # 0 = fr, vostfr ET 1 = fr ET 2 = all

        if resultLang and resultLang != 'false':
            if autoPlayLang == '1':
                if 'vf' in resultLang or 'truefrench' in resultLang:
                    return 1
                elif 'en' in resultLang or resultLang in 'vostfr':
                    # VSlog("Exclude because 'vostfr' or 'en': " + str(resultLang))
                    return -1
            elif autoPlayLang == '0' and ('vf' in resultLang or 'truefrench' in resultLang or 'vostfr' in resultLang):
                return 1
            elif autoPlayLang == '2':
                return 1
        return 0


    def _isCategorieCorrect(self, result, searchInfo):
        searchCat = searchInfo['cat']
        resultMeta = int(result['params'].getValue('sMeta'))
        if searchCat >= 0 and resultMeta != 0:
            if searchCat == 1 and resultMeta != 1:
                # VSlog("Exclude because it is not a film (meta: " + str(resultMeta) + ")")
                return -1
            # Pour l'instant les séries ne fonctionnent pas
            elif searchCat in [2, 4] and resultMeta not in [2, 5]:
                # VSlog("Exclude because it is not a serie (meta: " + str(resultMeta) + ")")
                return -1
            else:
                return 1
        return 0


    def _getScoreOfThisResult(self, result, searchInfo):
        yearScore = self._isYearCorrect(result, searchInfo)
        titleScore = self._isMovieTitleCorrect(result, searchInfo)
        langScore = self._isLangCorrect(result, searchInfo)
        catScore = self._isCategorieCorrect(result, searchInfo)

        if yearScore < 0 or titleScore < 0 or langScore < 0 or catScore < 0:
            return 0

        return yearScore + titleScore + langScore + catScore


    def _checkAllSearchWordInTitle(self, searchTitle, resultTitle):
        searchTitle = searchTitle.lower()
        resultTitle = resultTitle.lower()

        for word in searchTitle.split():
            if word not in resultTitle:
                return False
        return True


    def _displayAllResult(self, searchInfo):
        searchGui = cGui()
        allSearchInfo = searchInfo['title'] + ' ' + searchInfo['year']
        searchGui.addText('globalSearch', self.addons.VSlang(30081) % allSearchInfo, 'search.png')

        if len(self.allVideoLink) == 0:
            searchGui.addText('globalSearch')  # "Aucune information"
        else:
            for numCriteria in range(max(self.allVideoLink.keys()), 0, -1):
                if numCriteria in self.allVideoLink.keys():
                    for result in self.allVideoLink[numCriteria]:
                        self._displayOneResult(searchGui, result)

        cGui.CONTENT = 'files'
        searchGui.setEndOfDirectory()


    def _displayOneResult(self, searchGui, result):
        resultParams = result['params']
        title = resultParams.getValue('sTitle')

        lang = resultParams.getValue('sLang')
        if lang:
            title += " (" + str(lang) + ")"

        year = resultParams.getValue('sYear')
        if year:
            title += " " + str(year)

        hoster = resultParams.getValue('sHosterIdentifier')
        if hoster:
            title += " - [COLOR skyblue]" + str(hoster) + "[/COLOR]"

        quality = resultParams.getValue('sQual')
        if quality:
            title += " [" + str(quality).upper() + "]"

        searchSiteName = resultParams.getValue('searchSiteName')
        if searchSiteName:
            title += " - [COLOR olive]" + str(searchSiteName) + "[/COLOR]"

        result['guiElement'].setTitle(title)
        searchGui.addFolder(result['guiElement'], result['params'], False)

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

    def _executePluginForSearch(self, sSiteName, sFunction, parameters):
        VSlog("Execute " + str(sSiteName) + "." + str(sFunction))

        try:
            plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
            function = getattr(plugins, sFunction)
            function(parameters)
            result = True
        except Exception as error:
            VSlog('could not load site: ' + sSiteName + ' error: ' + str(error))
            traceback.print_exc()
            result = False

        return result


    def _playHosterGui(self, sFunction, parameters = None):
        plugins = __import__('resources.lib.gui.hoster', fromlist=['cHosterGui']).cHosterGui()
        function = getattr(plugins, sFunction)
        if parameters:
            return function(*parameters)
        else:
            return function()
