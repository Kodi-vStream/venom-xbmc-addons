#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
#from resources.lib.handler.pluginHandler import cPluginHandler
#from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.siteHandler import cSiteHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb

from resources.lib.comaddon import addon, window


SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'

#temp d'execution
# import time, random

# l = range(100000) 

# tps1 = time.clock() 
# random.shuffle(l) 
# l.sort() 
# tps2 = time.clock() 
# print(tps2 - tps1)

class cHome:

    ADDON = addon()


    def load(self):

        oGui = cGui()

        if (self.ADDON.getSetting('home_update') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showUpdate', '%s (%s)' % (self.ADDON.VSlang(30418), self.ADDON.getSetting('service_futur')), 'update.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.ADDON.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'load', self.ADDON.VSlang(30088), 'searchtmdb.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir('freebox', 'load', self.ADDON.VSlang(30115), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('freebox', 'load', self.ADDON.VSlang(30115), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.ADDON.VSlang(30117), 'replay.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.ADDON.VSlang(30120), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.ADDON.VSlang(30121), 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.ADDON.VSlang(30122), 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.ADDON.VSlang(30112), 'doc.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_SPORTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30113), 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showNets', self.ADDON.VSlang(30114), 'buzz.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cTrakt', 'getLoad', self.ADDON.VSlang(30214), 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', self.ADDON.VSlang(30202), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', self.ADDON.VSlang(30300), 'library.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getFavourites', self.ADDON.VSlang(30207), 'mark.png', oOutputParameterHandler)

        if (self.ADDON.getSetting("history-view") == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.ADDON.VSlang(30308), 'annees.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'globalSources', self.ADDON.VSlang(30138), 'host.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir('globalParametre', 'showSources', '[COLOR teal]'+self.ADDON.VSlang(30023)+'[/COLOR]', 'param.png', oOutputParameterHandler)


        view = False
        if (self.ADDON.getSetting("active-view") == 'true'):
            view = self.ADDON.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)


    def showUpdate(self):
        try:
            from resources.lib.about import cAbout
            cAbout().checkdownload()
        except:
            pass
        return

    def showDocs(self):
        oGui = cGui()

        # Affiche les Nouveautés Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30112), self.ADDON.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30112), self.ADDON.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_DOCS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showNets(self):
        oGui = cGui()

        # Affiche les Nouveautés Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30114), self.ADDON.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30114), self.ADDON.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NETS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30101)), 'films_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_HD')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30160)), 'films_hd.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30102)), 'films_views.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_COMMENTS')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30103)), 'films_comments.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_NOTES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30104)), 'films_notes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30105)), 'films_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30120), self.ADDON.VSlang(30106)), 'films_annees.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VF')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '[COLOR '+color_films+']'+self.ADDON.VSlang(30134)+'[/COLOR]', 'films_vf.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VOSTFR')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '[COLOR '+color_films+']'+self.ADDON.VSlang(30135)+'[/COLOR]', 'films_vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_MOVIE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30138), 'films_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30101)), 'series_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_HD')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30160)), 'films_hd.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30105)), 'series_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30106)), 'series_annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VFS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30107)), 'series_vf.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30108)), 'series_vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30138), 'series_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30122), self.ADDON.VSlang(30101)), 'animes_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VFS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30122), self.ADDON.VSlang(30107)), 'animes_vf.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30122), self.ADDON.VSlang(30108)), 'animes_vostfr.png', oOutputParameterHandler)

        #non utiliser ANIM_MOVIES

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30122), self.ADDON.VSlang(30105)), 'animes_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30122), self.ADDON.VSlang(30106)), 'animes_annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ENFANTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30122), self.ADDON.VSlang(30109)), 'animes_enfants.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANIMS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30138), 'animes_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30117), self.ADDON.VSlang(30101)), 'replay_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.ADDON.VSlang(30117), self.ADDON.VSlang(30105)), 'replay_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_REPLAYTV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.ADDON.VSlang(30138), 'replay_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

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

    def showSearchText(self):
        oGui = cGui()
        sSearchText = oGui.showKeyBoard()
        if sSearchText:
            self.showSearch(sSearchText)
            oGui.setEndOfDirectory()
        else :
            return False

    def showSearch(self, searchtext=cInputParameterHandler().getValue('searchtext')):

        if not searchtext:
            return self.showSearchText()

        #n'existe plus mais pas sure.
        #xbmcgui.Window(10101).clearProperty('search_text')
        window(10101).clearProperty('search_text')

        oGui = cGui()

        #print xbmc.getInfoLabel('ListItem.Property(Category)')

        oGui.addText('globalSearch', self.ADDON.VSlang(30077) % (searchtext), 'none.png')

        #utilisation de guielement pour ajouter la bonne catégories

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(self.ADDON.VSlang(30078))
        oGuiElement.setFileName(self.ADDON.VSlang(30078))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(1)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(self.ADDON.VSlang(30079))
        oGuiElement.setFileName(self.ADDON.VSlang(30079))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(2)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(self.ADDON.VSlang(30080))
        oGuiElement.setFileName(self.ADDON.VSlang(30080))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(3)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oOutputParameterHandler.addParameter('searchtext', searchtext)
        # oOutputParameterHandler.addParameter('disp', 'search10')
        # oOutputParameterHandler.addParameter('readdb', 'True')
        # oGui.addDir('globalSearch', 'showSearchText', '[COLOR orange]Recherche: Alluc_ee[/COLOR]', 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def showHistory(self):

        oGui = cGui()

        row = cDb().get_history()
        if row:
            oGui.addText(SITE_IDENTIFIER, self.ADDON.VSlang(30416))
        else :
            oGui.addText(SITE_IDENTIFIER)
        for match in row:
            oOutputParameterHandler = cOutputParameterHandler()

            #code to get type with disp
            type = self.ADDON.getSetting('search' + match[2][-1:] + '_type')
            if type:
                oOutputParameterHandler.addParameter('type', type)
                #xbmcgui.Window(10101).setProperty('search_type', type)
                window(10101).setProperty('search_type', type)

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oOutputParameterHandler.addParameter('searchtext', match[1])
            #oOutputParameterHandler.addParameter('disp', match[2])
            #oOutputParameterHandler.addParameter('readdb', 'False')


            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')
            oGuiElement.setTitle("- "+match[1])
            oGuiElement.setFileName(match[1])
            oGuiElement.setCat(match[2])
            oGuiElement.setIcon("search.png")
            oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,SITE_IDENTIFIER,'cHome','delSearch', self.ADDON.VSlang(30412))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if row:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', self.ADDON.VSlang(30413), 'search.png', oOutputParameterHandler)


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
                #exec "import "+aPlugin[1]
                #exec "sSiteUrl = "+aPlugin[1]+"."+sVar
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                icon = 'sites/%s.png' % (aPlugin[2])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, oOutputParameterHandler)
            except:
                pass

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
