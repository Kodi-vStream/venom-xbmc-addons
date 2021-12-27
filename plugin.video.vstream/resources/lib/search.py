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

SITE_IDENTIFIER = 'cSearch'
SITE_NAME = 'Search'


class cSearch:

    addons = addon()
    MAX_NUMBER_CRITERIA = 5

    def __init__(self):
        self.autoPlayVideo = False
        self.playSemaphore = threading.Semaphore()

    def load(self):
        oGui = cGui()
        oGui.setEndOfDirectory()

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

            total = count = 0
            searchResults = oGui.getSearchResult()
            values = searchResults.values()
            for result in values:
                total += len(result)
            self._progressClose()

            if total:
                xbmc.sleep(500)    # Nécessaire pour enchainer deux progressBar
                # Progress de chargement des metadata
                progressMeta = progress().VScreate(self.addons.VSlang(30076) + ' - ' + sSearchText, large=total > 50)
                for plugin in listPlugins:
                    pluginId = plugin['identifier']
                    if pluginId in searchResults.keys() and (len(searchResults[pluginId]) > 0):  # Au moins un résultat
                        # nom du site
                        count += 1
                        oGui.addText(pluginId, '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']),
                                     'sites/%s.png' % pluginId)

                        # résultats du site
                        for result in searchResults[pluginId]:
                            progressMeta.VSupdate(progressMeta, total)
                            if progressMeta.iscanceled():
                                break
                            oGui.addFolder(result['guiElement'], result['params'])
                        if progressMeta.iscanceled():
                            break

                progressMeta.VSclose(progressMeta)

            else:  # aucune source ne retourne de résultat
                oGui.addText('globalSearch')  # "Aucune information"

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
            # VSlog("----------- QuickSearch ! -----------")
            self.oSearchGui = cGui()

            searchInfo = self._getSearchInfo()
            oHandler = cRechercheHandler()
            oHandler.setText(searchInfo['title'])
            oHandler.setCat(searchInfo['cat'])
            listPlugins = oHandler.getAvailablePlugins()

            self.progressTotal = len(listPlugins)
            self._progressInit()

            self.findAndPlay = False
            # self.tryPlay = False
            # self.linkToTryToPlay = []
            self.allVideoLink = {}
            listThread = []

            self.eventFindOneLink = threading.Event()
            self.oSearchGui.searchResults = {}
            window(10101).setProperty('search', 'true')
            window(10101).setProperty('playVideo', 'true')
            for plugin in listPlugins:
                if not self._continueDeepSearch():
                    break

                thread = threading.Thread(target = self._quickSearchForPlugin, args = (plugin, searchInfo))
                thread.start()
                listThread.append(thread)

            if autoPlayVideo:
                self.eventFindOneLink.wait()
                searchResult = self.allVideoLink[cSearch.MAX_NUMBER_CRITERIA][0]

                window(10101).setProperty('autoPlay', 'true')
                find = self._playHosterGui(searchResult['guiElement'].getFunction(), searchResult['params'])
                if find:
                    self.findAndPlay = True
                window(10101).setProperty('autoPlay', 'false')

            for thread in listThread:
                thread.join()

            window(10101).setProperty('playVideo', 'false')
            window(10101).setProperty('search', 'false')

            self._progressClose()
            if not self.findAndPlay:
                self._displayResult()
        except Exception as e:
            VSlog('Error with quickSearch: ' + str(e))
            import traceback
            traceback.print_exc()
            self._progressForceClose()

        return True

    def _launchSearch(self, listPlugins, targetFunction, argsList):
        listThread = []
        window(10101).setProperty('search', 'true')
        for plugin in listPlugins:
            thread = threading.Thread(target=targetFunction, name=plugin['name'], args=tuple([plugin] + argsList))
            thread.start()
            listThread.append(thread)

        return listThread

    def _finishSearch(self, listThread):
        # On attend que les thread soient finis
        for thread in listThread:
            thread.join()
        window(10101).setProperty('search', 'false')

    def _continueDeepSearch(self):
        return not (self.findAndPlay or self._monitorAbortRequest() or self._progressIsCancel())

    def _deepSearchLoop(self, searchResult, searchInfo):
        if self._continueDeepSearch():
            numberOfCriteria = self._getResultNumberOfCriteria(searchResult, searchInfo)

            if numberOfCriteria > 0:
                guiElement = searchResult['guiElement']
                videoParams = searchResult['params'] # OutputParameter
                siteId = guiElement.getSiteName()

                # VSlog("================== " + str(siteId) + "." + str(guiElement.getFunction()) + " ==================")
                # VSlog("numberOfCriteria: " + str(numberOfCriteria))

                if siteId == 'cHosterGui':
                    if numberOfCriteria not in self.allVideoLink:
                        self.allVideoLink[numberOfCriteria] = []
                    self.allVideoLink[numberOfCriteria].append(searchResult)

                    if self.autoPlayVideo and numberOfCriteria == cSearch.MAX_NUMBER_CRITERIA:
                        self.eventFindOneLink.set()
                        # VSlog("Try play and try to get semaphore")
                        # self.playSemaphore.acquire()
                        # if not self.tryPlay and not self.findAndPlay:
                        #     self.tryPlay = True
                        #     self.playSemaphore.release()
                        #     VSlog("Try to play")

                        #     window(10101).setProperty('autoPlay', 'true')
                        #     find = self._playHosterGui(guiElement.getFunction(), videoParams)
                        #     if find:
                        #         self.findAndPlay = True
                        #     VSlog("playMovieCorrectly: " + str(self.findAndPlay))
                        #     window(10101).setProperty('autoPlay', 'false')
                        #     self.tryPlay = False

                        # else:
                        #     self.playSemaphore.release()
                        #     VSlog("Release try play semaphore")
                        #     self.linkToTryToPlay.append(searchResult)


                else:
                    videoParams.addParameter('searchSiteId', siteId)
                    cGui.emptySearchResult(siteId)
                    self._executePluginForSearch(siteId, guiElement.getFunction(), videoParams)

                    pluginResult = cGui.getSearchResult()
                    for searchResult in pluginResult[siteId]:
                        if self._continueDeepSearch():
                            searchResult['params'].mergeUnexistingInfos(videoParams)
                            searchResult['params'].addParameter('searchSiteId', siteId)

                            if searchResult['guiElement'].getSiteName() == siteId and \
                                searchResult['guiElement'].getFunction() == guiElement.getFunction():
                                VSlog("Loop with the same result: " + str(siteId) + "." + str(guiElement.getFunction()))
                            else:
                                self._deepSearchLoop(searchResult, searchInfo)


    def _quickSearchForPlugin(self, plugin, searchInfo):
        self._pluginSearch(plugin, Quote(searchInfo['title']))
        searchResults = cGui.getSearchResult()
        pluginId = plugin['identifier']
        pluginName = plugin['name']

        if pluginId in searchResults and len(searchResults[pluginId]) > 0:  # Au moins un résultat
            pluginResult = searchResults[pluginId][:]

            for searchResult in pluginResult:
                searchResult['params'].addParameter('searchSiteName', pluginName)
                self._deepSearchLoop(searchResult, searchInfo)
                if self._continueDeepSearch():
                    break
        else:
            VSlog("No result for: " + str(pluginId))
        self._progressUpdate(pluginName)

    def _getSearchInfo(self):
        oInputParameterHandler = cInputParameterHandler()

        if oInputParameterHandler.exist('cat'):
            searchCat = int(oInputParameterHandler.getValue('cat'))
        else:
            searchCat = -1

        if oInputParameterHandler.exist('title'):
            searchTitle = oInputParameterHandler.getValue('title')
        else:
            searchTitle = ""

        if oInputParameterHandler.exist('year'):
            searchYear = str(oInputParameterHandler.getValue('year'))
        else:
            searchYear = ""

        return {'title': searchTitle, 'cat': searchCat, 'year': searchYear}

    def _displayResult(self):
        if len(self.allVideoLink) == 0:
            self.oSearchGui.addText('globalSearch')  # "Aucune information"
        else:
            # for numCriteria in self.allVideoLink.keys():
            for numCriteria in range(cSearch.MAX_NUMBER_CRITERIA, 0, -1):
                if numCriteria in self.allVideoLink.keys():
                    for result in self.allVideoLink[numCriteria]:
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
                            title += " - [COLOR violet]" + str(hoster) + "[/COLOR]"
                        quality = resultParams.getValue('sQual')
                        if quality:
                            title += " [" + str(quality).upper() + "]"
                        searchSiteName = resultParams.getValue('searchSiteName')
                        if searchSiteName:
                            title += " - [COLOR olive]" + str(searchSiteName) + "[/COLOR]"

                        result['guiElement'].setTitle(title)
                        self.oSearchGui.addFolder(result['guiElement'], result['params'], False)


        cGui.CONTENT = 'files'
        self.oSearchGui.setEndOfDirectory()

    def _getResultNumberOfCriteria(self, result, searchInfo):
        numberOfCriteria = 0
        searchTitle = searchInfo['title']
        searchCat = searchInfo['cat']
        searchYear = searchInfo['year']

        sYear = result['params'].getValue('sYear')
        if sYear and sYear != searchYear:
            VSlog("Exclude because 'year' not correct: " + str(sYear))
            return 0
        else:
            numberOfCriteria += 1

        sMovieTitle = result['params'].getValue('sMovieTitle')
        if sMovieTitle:
            if not self._checkAllSearchWordInTitle(searchTitle, sMovieTitle):
                VSlog("Exclude because 'title' not correct: " + str(sMovieTitle))
                return 0
            else:
                numberOfCriteria += 1
                if self._checkIsExactSameTitle(searchTitle, sMovieTitle):
                    numberOfCriteria += 1

        sLang = str(result['params'].getValue('sLang')).lower()
        VSlog('sLang: ' + str(sLang))
        if sLang and (sLang == 'vf' or sLang == 'truefrench'):
            numberOfCriteria += 1
        elif sLang and ('vostfr' in sLang or 'en' in sLang):
            VSlog("Exclude because 'vostfr' or 'en': " + str(sLang))
            return 0

        if searchCat >= 0:
            sMeta = int(result['params'].getValue('sMeta'))
            if sMeta != 0:
                if searchCat == 1 and sMeta != 1:
                    VSlog("Exclude because is is not a film (meta: " + str(sMeta) + ")")
                    return 0
                elif searchCat in [2, 4] and sMeta not in [2, 5]:
                    VSlog("Exclude because is is not a serie (meta: " + str(sMeta) + ")")
                    return 0
                else:
                    numberOfCriteria += 1

            #    Categorie       Meta          sCat     CONTENT
            #    Film            1             1        movies
            #    Serie           2             2        tvshows
            #    Anime           4             3        tvshows
            #    Saison          5             4        episodes
            #    Divers          0             5        videos
            #    IPTV (Officiel) 0             6        files
            #    Saga            3             7        movies
            #    Episodes        6             8        episodes
            #    Person          7             /        artists
            #    Network         8             /        files
        return numberOfCriteria


    def _checkAllSearchWordInTitle(self, searchTitle, resultTitle):
        searchTitle = searchTitle.lower()
        resultTitle = resultTitle.lower()

        for word in searchTitle.split():
            if word not in resultTitle:
                return False
        return True

    def _checkIsExactSameTitle(self, searchTitle, resultTitle):
        return searchTitle.strip().lower() == resultTitle.strip().lower()

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
        except Exception as e:
            VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
            import traceback
            traceback.print_exc()
            result = False

        return result

    def _playHosterGui(self, sFunction, parameters = None):
        plugins = __import__('resources.lib.gui.hoster', fromlist=['cHosterGui']).cHosterGui()
        function = getattr(plugins, sFunction)
        if parameters:
            return function(parameters)
        else:
            return function()
