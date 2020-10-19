# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
# from resources.lib.handler.pluginHandler import cPluginHandler
# from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.siteHandler import cSiteHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb
from resources.lib.comaddon import addon, window

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'

# temp d'execution
# import time, random

# l = range(100000)

# tps1 = time.clock()
# random.shuffle(l)
# l.sort()
# tps2 = time.clock()
# print(tps2 - tps1)


class cHome:

    addons = addon()

    def load(self):

        oGui = cGui()

        if (self.addons.getSetting('home_update') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showUpdate', '%s (%s)' % (self.addons.VSlang(30418), self.addons.getSetting('service_futur')), 'update.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'load', self.addons.VSlang(30088), 'searchtmdb.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('freebox', 'load', self.addons.VSlang(30115), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.addons.VSlang(30117), 'replay.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.addons.VSlang(30120), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.addons.VSlang(30121), 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.addons.VSlang(30122), 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.addons.VSlang(30112), 'doc.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_SPORTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30113), 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showNets', self.addons.VSlang(30114), 'buzz.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showUsers', self.addons.VSlang(30455), 'user.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'ShowTools', self.addons.VSlang(30033), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getBookmarks', self.addons.VSlang(30207), 'mark.png', oOutputParameterHandler)

        if (self.addons.getSetting('history-view') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.addons.VSlang(30308), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'globalSources', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        view = False
        if (self.addons.getSetting('active-view') == 'true'):
            view = self.addons.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)

    def showUpdate(self):
        try:
            from resources.lib.about import cAbout
            cAbout().checkdownload()
        except:
            pass
        return

    def showSearchText(self):
        oGui = cGui()
        sSearchText = oGui.showKeyBoard(heading=self.addons.VSlang(30076))
        if sSearchText:
            self.showSearch(sSearchText)
            oGui.setEndOfDirectory()
        else:
            return False

    def showSearch(self, searchtext=cInputParameterHandler().getValue('searchtext')):

        if not searchtext:
            return self.showSearchText()

        # n'existe plus mais pas sure.
        # xbmcgui.Window(10101).clearProperty('search_text')
        window(10101).clearProperty('search_text')

        oGui = cGui()

        # print(xbmc.getInfoLabel('ListItem.Property(Category)'))

        oGui.addText('globalSearch', self.addons.VSlang(30077) % searchtext, 'none.png')

        # utilisation de guielement pour ajouter la bonne catégorie

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(self.addons.VSlang(30078))
        oGuiElement.setFileName(self.addons.VSlang(30078))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        # oGuiElement.setThumbnail(sThumbnail)
        # oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(1)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(self.addons.VSlang(30079))
        oGuiElement.setFileName(self.addons.VSlang(30079))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        # oGuiElement.setThumbnail(sThumbnail)
        # oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(2)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(self.addons.VSlang(30080))
        oGuiElement.setFileName(self.addons.VSlang(30080))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        # oGuiElement.setThumbnail(sThumbnail)
        # oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(3)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oOutputParameterHandler.addParameter('searchtext', searchtext)
        # oOutputParameterHandler.addParameter('disp', 'search10')
        # oOutputParameterHandler.addParameter('readdb', 'True')
        # oGui.addDir('globalSearch', 'showSearchText', 'self.addons.VSlang(30417), 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_REPLAYTV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_HD')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30160)), 'hd.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30102)), 'views.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_COMMENTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30103)), 'comments.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_NOTES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30104)), 'notes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30111)), 'listes.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VF')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30107)), 'vf.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VOSTFR')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30108)), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_MOVIE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30111)), 'listes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VFS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30107)), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30108)), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_DRAMAS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), 'Dramas'), 'dramas.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VFS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30107)), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30108)), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ENFANTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30109)), 'enfants.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANIMS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = cGui()

        # Affiche les Nouveautés Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_DOCS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'doc.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showNets(self):
        oGui = cGui()

        # Affiche les Nouveautés Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30114), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30114), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NETS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showUsers(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteuptobox', 'load', self.addons.VSlang(30325), 'sites/siteuptobox.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteonefichier', 'load', self.addons.VSlang(30327), 'sites/siteonefichier.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def ShowTools(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', self.addons.VSlang(30300), 'library.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', self.addons.VSlang(30202), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showHistory(self):
        oGui = cGui()

        row = cDb().get_history()
        if row:
            oGui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416))
        else:
            oGui.addText(SITE_IDENTIFIER)
        for match in row:
            oOutputParameterHandler = cOutputParameterHandler()

            # code to get type with disp
            sType = self.addons.getSetting('search' + match[2][-1:] + '_type')
            if sType:
                oOutputParameterHandler.addParameter('type', sType)
                window(10101).setProperty('search_type', sType)

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oOutputParameterHandler.addParameter('searchtext', match[1])
            # oOutputParameterHandler.addParameter('disp', match[2])
            # oOutputParameterHandler.addParameter('readdb', 'False')

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')
            oGuiElement.setTitle('- ' + match[1])
            oGuiElement.setFileName(match[1])
            oGuiElement.setCat(match[2])
            oGuiElement.setIcon('search.png')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, 'cHome', 'delSearch', self.addons.VSlang(30412))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if row:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', self.addons.VSlang(30413), 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def delSearch(self):
        cDb().del_history()
        return True

    def callpluging(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')

        oPluginHandler = cSiteHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sSiteUrl)
        for aPlugin in aPlugins:
            try:
                # exec('import ' + aPlugin[1])
                # exec('sSiteUrl = ' + aPlugin[1] + '.' + sVar)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                icon = 'sites/%s.png' % (aPlugin[2])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, oOutputParameterHandler)
            except:
                pass

        oGui.setEndOfDirectory()

    def showHostDirect(self):  # fonction de recherche
        oGui = cGui()
        sUrl = oGui.showKeyBoard(heading=self.addons.VSlang(30045))
        if (sUrl != False):

            oHoster = cHosterGui().checkHoster(sUrl)
            if (oHoster != False):
                oHoster.setDisplayName(self.addons.VSlang(30046))
                oHoster.setFileName(self.addons.VSlang(30046))
                cHosterGui().showHoster(oGui, oHoster, sUrl, '')

        oGui.setEndOfDirectory()

    # def searchMovie(self):
    #     oGui = cGui()
    #     oInputParameterHandler = cInputParameterHandler()
    #     sSearchText = oInputParameterHandler.getValue('searchtext')
    #     sReadDB = oInputParameterHandler.getValue('readdb')
    #     sDisp = oInputParameterHandler.getValue('disp')

    #     oHandler = cRechercheHandler()
    #     oHandler.setText(sSearchText)
    #     oHandler.setDisp(sDisp)
    #     oHandler.setRead(sReadDB)
    #     aPlugins = oHandler.getAvailablePlugins()

    #     oGui.setEndOfDirectory()

    # def showSources(self):
    #     oGui = cGui()

    #     oPluginHandler = cPluginHandler()
    #     aPlugins = oPluginHandler.getAvailablePlugins()
    #     for aPlugin in aPlugins:
    #         oOutputParameterHandler = cOutputParameterHandler()
    #         oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    #         icon = 'sites/%s.png' % (aPlugin[1])
    #         oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)

    #     oGui.setEndOfDirectory()

