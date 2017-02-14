#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.siteHandler import cSiteHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb
import os
import urllib
import xbmc, xbmcgui

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'

class cHome:


    def load(self):
        oGui = cGui()

        if (cConfig().getSetting('home_cherches') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showSearch', cConfig().getlanguage(30076), 'search.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_cherchev') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('themoviedb_org', 'load', cConfig().getlanguage(30088), 'searchtmdb.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_tvs') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('freebox', 'load', cConfig().getlanguage(30115), 'tv.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_replaytvs') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showReplay', cConfig().getlanguage(30117), 'replay.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_films') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', cConfig().getlanguage(30120), 'films.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_series') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', cConfig().getlanguage(30121), 'series.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_anims') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showAnimes', cConfig().getlanguage(30122), 'animes.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_docs') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showDocs', cConfig().getlanguage(30112), 'doc.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_sports') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportSports', cConfig().getlanguage(30113), 'sport.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_videos') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showNets', cConfig().getlanguage(30114), 'buzz.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cTrakt', 'getLoad', 'Trakt (bêta)', 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', cConfig().getlanguage(30202), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', cConfig().getlanguage(30300), 'library.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'showSources', cConfig().getlanguage(30116), 'host.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getFavourites', '[COLOR teal]'+cConfig().getlanguage(30210)+'[/COLOR]', 'mark.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalParametre', 'showSources', '[COLOR teal]'+cConfig().getlanguage(30023)+'[/COLOR]', 'param.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_update') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showUpdate', '[COLOR green]Mise a jour disponible[/COLOR]', 'update.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
        if (cConfig().getSetting("active-view") == 'true'):
            xbmc.executebuiltin('Container.SetViewMode(%s)' % cConfig().getSetting('accueil-view'))

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
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'docNews', '%s (%s)' % (cConfig().getlanguage(30112), cConfig().getlanguage(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'docGenres', '%s (%s)' % (cConfig().getlanguage(30112), cConfig().getlanguage(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'docDocs', cConfig().getlanguage(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showNets(self):
        oGui = cGui()

        # Affiche les Nouveautés Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'netsNews', '%s (%s)' % (cConfig().getlanguage(30114), cConfig().getlanguage(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'netsGenres', '%s (%s)' % (cConfig().getlanguage(30114), cConfig().getlanguage(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNets', cConfig().getlanguage(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showTV(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('freebox', 'load', 'Télévision Box', 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('chaine_tv', 'load', 'Tv du net', 'tv.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNews', '%s (%s)' % (cConfig().getlanguage(30120), cConfig().getlanguage(30101)), 'films_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieHD', '%s (%s)' % (cConfig().getlanguage(30120), cConfig().getlanguage(30160)), 'films_hd.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieViews', '%s (%s)' % (cConfig().getlanguage(30120), cConfig().getlanguage(30102)), 'films_views.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieComments', '%s (%s)' % (cConfig().getlanguage(30120), cConfig().getlanguage(30103)), 'films_comments.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNotes', '%s (%s)' % (cConfig().getlanguage(30120), cConfig().getlanguage(30104)), 'films_notes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieGenres', '%s (%s)' % (cConfig().getlanguage(30120), cConfig().getlanguage(30105)), 'films_genres.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir(SITE_IDENTIFIER, 'movieVF', '[COLOR '+color_films+']'+cConfig().getlanguage(30134)+'[/COLOR]', 'films_vf.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir(SITE_IDENTIFIER, 'movieVOSTFR', '[COLOR '+color_films+']'+cConfig().getlanguage(30135)+'[/COLOR]', 'films_vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieMovie', cConfig().getlanguage(30138), 'films_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieNews', '%s (%s)' % (cConfig().getlanguage(30121), cConfig().getlanguage(30101)), 'series_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieHD', '%s (%s)' % (cConfig().getlanguage(30121), cConfig().getlanguage(30160)), 'films_hd.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieGenres', '%s (%s)' % (cConfig().getlanguage(30121), cConfig().getlanguage(30105)), 'series_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieVfs', '%s (%s)' % (cConfig().getlanguage(30121), cConfig().getlanguage(30107)), 'series_vf.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieVostfrs', '%s (%s)' % (cConfig().getlanguage(30121), cConfig().getlanguage(30108)), 'series_vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieSeries', cConfig().getlanguage(30138), 'series_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animNews', '%s (%s)' % (cConfig().getlanguage(30122), cConfig().getlanguage(30101)), 'animes_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animVfs', '%s (%s)' % (cConfig().getlanguage(30122), cConfig().getlanguage(30107)), 'animes_vf.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animVostfrs', '%s (%s)' % (cConfig().getlanguage(30122), cConfig().getlanguage(30108)), 'animes_vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animGenres', '%s (%s)' % (cConfig().getlanguage(30122), cConfig().getlanguage(30105)), 'animes_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animAnims', cConfig().getlanguage(30138), 'animes_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'replayNews', '%s (%s)' % (cConfig().getlanguage(30117), cConfig().getlanguage(30101)), 'replay_news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'replayGenres', '%s (%s)' % (cConfig().getlanguage(30117), cConfig().getlanguage(30105)), 'replay_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'replayReplay', cConfig().getlanguage(30138), 'replay_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSources(self):
        oGui = cGui()

        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins()
        for aPlugin in aPlugins:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            icon = 'sites/%s.png' % (aPlugin[1])
            oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def movieMovie(self):
        self.__callpluging('MOVIE_MOVIE', 'films_host.png')

    def movieNews(self):
        self.__callpluging('MOVIE_NEWS', 'films_news.png')

    def movieViews(self):
        self.__callpluging('MOVIE_VIEWS', 'films_views.png')

    def movieHD(self):
        self.__callpluging('MOVIE_HD', 'films_hd.png')

    def movieComments(self):
        self.__callpluging('MOVIE_COMMENTS', 'films_comments.png')

    def movieNotes(self):
        self.__callpluging('MOVIE_NOTES', 'films_notes.png')

    def movieGenres(self):
        self.__callpluging('MOVIE_GENRES', 'films_genres.png')

    def movieVF(self):
        self.__callpluging('MOVIE_VF', 'films_vf.png')

    def movieVOSTFR(self):
        self.__callpluging('MOVIE_VOSTFR', 'films_vostfr.png')

    def serieSeries(self):
        self.__callpluging('SERIE_SERIES', 'series_host.png')

    def serieNews(self):
        self.__callpluging('SERIE_NEWS', 'series_news.png')

    def serieVfs(self):
        self.__callpluging('SERIE_VFS', 'series_vf.png')

    def serieVostfrs(self):
        self.__callpluging('SERIE_VOSTFRS', 'series_vostfr.png')

    def serieHD(self):
        self.__callpluging('SERIE_HD', 'films_hd.png')

    def serieGenres(self):
        self.__callpluging('SERIE_GENRES', 'series_genres.png')

    def animAnims(self):
        self.__callpluging('ANIM_ANIMS', 'animes_host.png')

    def animNews(self):
        self.__callpluging('ANIM_NEWS', 'animes_news.png')

    def animVfs(self):
        self.__callpluging('ANIM_VFS', 'animes_vf.png')

    def animGenres(self):
        self.__callpluging('ANIM_GENRES', 'animes_genres.png')

    def animVostfrs(self):
        self.__callpluging('ANIM_VOSTFRS', 'animes_vostfr.png')

    def animMovies(self):
        self.__callpluging('ANIM_MOVIES', 'animes.png')

    def docDocs(self):
        self.__callpluging('DOC_DOCS', 'doc.png')

    def docNews(self):
        self.__callpluging('DOC_NEWS', 'news.png')

    def docGenres(self):
        self.__callpluging('DOC_GENRES', 'genres.png')

    def sportSports(self):
        self.__callpluging('SPORT_SPORTS', 'sport.png')

    def movieNets(self):
        self.__callpluging('MOVIE_NETS', 'buzz.png')

    def netsNews(self):
        self.__callpluging('NETS_NEWS', 'news.png')

    def  netsGenres(self):
        self.__callpluging('NETS_GENRES', 'genres.png')

    def replayReplay(self):
        self.__callpluging('REPLAYTV_REPLAYTV', 'replay_host.png')

    def replayNews(self):
        self.__callpluging('REPLAYTV_NEWS', 'replay_news.png')

    def replayGenres(self):
        self.__callpluging('REPLAYTV_GENRES', 'replay_genres.png')

    def showSearch(self):

        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search1')
        oOutputParameterHandler.addParameter('type', cConfig().getSetting('search1_type'))
        oOutputParameterHandler.addParameter('readdb', 'True')
        sLabel1 = cConfig().getlanguage(30077)+": "+cConfig().getSetting('search1_label')
        oGui.addDir('globalSearch', 'searchMovie', sLabel1, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search2')
        oOutputParameterHandler.addParameter('type', cConfig().getSetting('search2_type'))
        oOutputParameterHandler.addParameter('readdb', 'True')
        sLabel2 = cConfig().getlanguage(30089)+": "+cConfig().getSetting('search2_label')
        oGui.addDir('globalSearch', 'searchMovie', sLabel2, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search3')
        oOutputParameterHandler.addParameter('type', cConfig().getSetting('search3_type'))
        oOutputParameterHandler.addParameter('readdb', 'True')
        sLabel3 = cConfig().getlanguage(30090)+": "+cConfig().getSetting('search3_label')
        oGui.addDir('globalSearch', 'searchMovie', sLabel3, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search4')
        oOutputParameterHandler.addParameter('type', cConfig().getSetting('search4_type'))
        oOutputParameterHandler.addParameter('readdb', 'True')
        sLabel4 = cConfig().getlanguage(30091)+": "+cConfig().getSetting('search4_label')
        oGui.addDir('globalSearch', 'searchMovie', sLabel4, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search5')
        oOutputParameterHandler.addParameter('type', '')
        oOutputParameterHandler.addParameter('readdb', 'True')
        sLabel5 = ('%s: %s') % (cConfig().getlanguage(30076), cConfig().getlanguage(30092))
        oGui.addDir('globalSearch', 'searchMovie', sLabel5, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search10')
        oOutputParameterHandler.addParameter('readdb', 'True')
        oGui.addDir('globalSearch', 'searchMovie', '[COLOR orange]Recherche: Alluc_ee[/COLOR]', 'search.png', oOutputParameterHandler)

        #history
        if (cConfig().getSetting("history-view") == 'true'):

            row = cDb().get_history()
            if row:
                oGui.addText(SITE_IDENTIFIER, "[COLOR azure]Votre Historique[/COLOR]")
            for match in row:
                oOutputParameterHandler = cOutputParameterHandler()

                #code to get type with disp
                type = cConfig().getSetting('search' + match[2][-1:] + '_type')
                if type:
                    oOutputParameterHandler.addParameter('type', type)
                    xbmcgui.Window(10101).setProperty('search_type', type)

                oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                oOutputParameterHandler.addParameter('searchtext', match[1])
                oOutputParameterHandler.addParameter('disp', match[2])
                oOutputParameterHandler.addParameter('readdb', 'False')
                oGui.addDir('globalSearch', 'searchMovie', "- "+match[1], 'search.png', oOutputParameterHandler)

            if row:

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                oGui.addDir(SITE_IDENTIFIER, 'delSearch', '[COLOR red]Supprimer l\'historique[/COLOR]', 'search.png', oOutputParameterHandler)


        oGui.setEndOfDirectory()

    def searchMovie2(self):
        oInputParameterHandler = cInputParameterHandler()
        sDisp = oInputParameterHandler.getValue('disp')
        oHandler = cRechercheHandler()
        liste = oHandler.getAvailablePlugins(sDisp)
        self.__callsearch(liste, sDisp)

    def delSearch(self):
        cDb().del_history()
        return True


    def __callpluging(self, sVar, sIcon):
        oGui = cGui()
        oPluginHandler = cSiteHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sVar)
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

    def searchMovie(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sSearchText = oInputParameterHandler.getValue('searchtext')
        sReadDB = oInputParameterHandler.getValue('readdb')
        sDisp = oInputParameterHandler.getValue('disp')

        oHandler = cRechercheHandler()
        oHandler.setText(sSearchText)
        oHandler.setDisp(sDisp)
        oHandler.setRead(sReadDB)
        aPlugins = oHandler.getAvailablePlugins()

        oGui.setEndOfDirectory()