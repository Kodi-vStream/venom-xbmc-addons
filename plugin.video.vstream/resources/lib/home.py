# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.search import cSearch
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import addon
from resources.sites.themoviedb_org import SITE_IDENTIFIER as SITE_TMDB
from resources.lib.trakt import SITE_IDENTIFIER as SITE_TRAKT


SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'


class cHome:

    addons = addon()

    def load(self):
        oGui = cGui()
        oGui.addDir(SITE_IDENTIFIER, 'showVOD', self.addons.VSlang(30131), 'vod.png')
        oGui.addDir(SITE_IDENTIFIER, 'showDirect', self.addons.VSlang(30132), 'direct.png')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.addons.VSlang(30350), 'replay.png')
        oGui.addDir(SITE_IDENTIFIER, 'showMyVideos', self.addons.VSlang(30130), 'profile.png')
        oGui.addDir(SITE_IDENTIFIER, 'showTools', self.addons.VSlang(30033), 'tools.png')

        view = False
        if self.addons.getSetting('active-view') == 'true':
            view = self.addons.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)

    def showVOD(self):
        oGui = cGui()
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.addons.VSlang(30120), 'films.png')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.addons.VSlang(30121), 'series.png')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.addons.VSlang(30122), 'animes.png')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.addons.VSlang(30112), 'doc.png')
        oGui.addDir(SITE_IDENTIFIER, 'showDramas', self.addons.VSlang(30124), 'dramas.png')
        oGui.addDir(SITE_TMDB, 'showMenuActeur', self.addons.VSlang(30466), 'actor.png')
        oGui.addDir(SITE_IDENTIFIER, 'showMenuSearch', self.addons.VSlang(30135), 'search_direct.png')

        # ininteressant
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir(SITE_IDENTIFIER, 'showNets', self.addons.VSlang(30114), 'buzz.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMyVideos(self):
        oGui = cGui()
        oGui.addDir('cFav', 'getBookmarks', self.addons.VSlang(30207), 'mark.png')
        oGui.addDir('cViewing', 'showMenu', self.addons.VSlang(30125), 'vod.png')
        oGui.addDir('cWatched', 'showMenu', self.addons.VSlang(30321), 'annees.png')
        oGui.addDir(SITE_IDENTIFIER, 'showUsers', self.addons.VSlang(30455), 'profile.png')
        oGui.addDir('cDownload', 'getDownloadList', self.addons.VSlang(30229), 'download.png')

        # les enregistrements de chaines TV ne sont plus opérationnelles
        # folder = self.addons.getSetting('path_enregistrement')
        # if not folder:
        #     folder = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement"/>'
        # oOutputParameterHandler.addParameter('siteUrl', folder)
        # oGui.addDir('cLibrary', 'openLibrary', self.addons.VSlang(30225), 'download.png', oOutputParameterHandler)

        oGui.addDir('globalSources', 'activeSources', self.addons.VSlang(30362), 'host.png')
        oGui.setEndOfDirectory()

    def showMenuSearch(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()

        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir('themoviedb_org', 'load', self.addons.VSlang(30088), 'searchtmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30120), 'search-films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30121), 'search-series.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30122), 'search-animes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '9')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30124), 'search-dramas.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30112), 'search-divers.png', oOutputParameterHandler)

        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.addons.VSlang(30308), 'history.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMovieSearch(self):
        oGui = cGui()
        addons = self.addons
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
        oGui.addDir(SITE_TMDB, 'showSearchMovie', addons.VSlang(30120), 'search-films.png', oOutputParameterHandler)
    
        oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
        oGui.addDir(SITE_TMDB, 'showSearchSaga', addons.VSlang(30139), 'search-sagas.png', oOutputParameterHandler)
    
        # Chercher une liste Trakt
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_TRAKT, 'showSearchList', addons.VSlang(30123), 'search-list.png', oOutputParameterHandler)

        # recherche acteurs
        oOutputParameterHandler.addParameter('siteUrl', 'search/person')
        oGui.addDir(SITE_TMDB, 'showSearchActor', addons.VSlang(30466), 'search-actor.png', oOutputParameterHandler)

        if addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('sCat', '1')
            oGui.addDir(SITE_IDENTIFIER, 'showHistory', addons.VSlang(30308), 'history.png', oOutputParameterHandler)
    
        oGui.setEndOfDirectory()


    def showSeriesSearch(self):
        oGui = cGui()
        addons = self.addons
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
        oGui.addDir(SITE_TMDB, 'showSearchSerie', addons.VSlang(30121), 'search-series.png', oOutputParameterHandler)
    
            # Chercher une liste
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_TRAKT, 'showSearchList', addons.VSlang(30123), 'search-list.png', oOutputParameterHandler)
        
        if addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('sCat', '2')
            oGui.addDir(SITE_IDENTIFIER, 'showHistory', addons.VSlang(30308), 'history.png', oOutputParameterHandler)
    
        oGui.setEndOfDirectory()


    def showAnimesSearch(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        # recherche directe
        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search-animes.png', oOutputParameterHandler)
    
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('sCat', '3')
            oGui.addDir(SITE_IDENTIFIER, 'showHistory', self.addons.VSlang(30308), 'history.png', oOutputParameterHandler)
    
    
        oGui.setEndOfDirectory()

    def showDramasSearch(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        # recherche directe
        oOutputParameterHandler.addParameter('sCat', '9')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search-dramas.png', oOutputParameterHandler)
    
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('sCat', '9')
            oGui.addDir(SITE_IDENTIFIER, 'showHistory', self.addons.VSlang(30308), 'history.png', oOutputParameterHandler)
    
        oGui.setEndOfDirectory()

    def showDocsSearch(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        # recherche directe
        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search-divers.png', oOutputParameterHandler)
    
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('sCat', '5')
            oGui.addDir(SITE_IDENTIFIER, 'showHistory', self.addons.VSlang(30308), 'history.png', oOutputParameterHandler)
    
        oGui.setEndOfDirectory()


    def showSearchText(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sSearchText = oGui.showKeyBoard(heading=self.addons.VSlang(30076))
        if not sSearchText:
            return False

        oSearch = cSearch()
        sCat = oInputParameterHandler.getValue('sCat')
        oSearch.searchGlobal(sSearchText, sCat)
        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = cGui()
        addons = self.addons

        oOutputParameterHandler = cOutputParameterHandler()

        # oOutputParameterHandler.addParameter('sCat', '1')
        # oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30120), 'search.png', oOutputParameterHandler)

#        oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
        oGui.addDir(SITE_IDENTIFIER, 'showMovieSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        # Nouveautés
        oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        oGui.addDir(SITE_TMDB, 'showMoviesNews', addons.VSlang(30101), 'news.png', oOutputParameterHandler)

        # Populaires
        oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        oGui.addDir(SITE_TMDB, 'showMovies', addons.VSlang(30102), 'popular.png', oOutputParameterHandler)
        
        # Box office
        oOutputParameterHandler.addParameter('siteUrl', 'movies/boxoffice')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_TRAKT, 'getTrakt', addons.VSlang(30314), 'boxoffice.png', oOutputParameterHandler)
        
        # Genres
        oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
        oGui.addDir(SITE_TMDB, 'showGenreMovie', addons.VSlang(30105), 'genres.png', oOutputParameterHandler)
        
        # Années
        oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        oGui.addDir(SITE_TMDB, 'showMoviesYears', self.addons.VSlang(30106), 'annees.png', oOutputParameterHandler)

        # # Top films TMDB
        # oOutputParameterHandler.addParameter('siteUrl', 'discover/movie')
        # oGui.addDir(SITE_TMDB, 'showMoviesTop', addons.VSlang(30104), 'notes.png', oOutputParameterHandler)

        # Top films TRAKT
        oOutputParameterHandler.addParameter('siteUrl', 'movies/popular')
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_TRAKT, 'getTrakt', self.addons.VSlang(30104), 'notes.png', oOutputParameterHandler)


        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ENFANTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30109), 'enfants.png', oOutputParameterHandler)

        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VF')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30107)), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VOSTFR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30108), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_MOVIE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()
        addons=self.addons

        oOutputParameterHandler = cOutputParameterHandler()

        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_TMDB, 'showSearchSerie', addons.VSlang(30121), 'search-series.png', oOutputParameterHandler)
    
        # Nouveautés
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showSeriesNews', addons.VSlang(30101), 'news.png', oOutputParameterHandler)

        # Populaires TMDB
        # oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        # oGui.addDir(SITE_TMDB, 'showSeriesViews', addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

        # Populaires trakt
        oOutputParameterHandler.addParameter('siteUrl', 'shows/trending')
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_TRAKT, 'getTrakt', addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    
        # Par diffuseurs
        oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
        oGui.addDir(SITE_TMDB, 'showSeriesNetworks', addons.VSlang(30467), 'diffuseur.png', oOutputParameterHandler)
    
        # Par genres
        oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
        oGui.addDir(SITE_TMDB, 'showGenreTV', addons.VSlang(30105), 'genres.png', oOutputParameterHandler)
    
        # Les mieux notés TMDB
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showSeriesTop', addons.VSlang(30104), 'notes.png', oOutputParameterHandler)

        # Les mieux notés TRAKT
        # oOutputParameterHandler.addParameter('siteUrl', 'shows/popular')
        # oOutputParameterHandler.addParameter('sCat', '2')
        # oGui.addDir(SITE_TRAKT, 'getTrakt', addons.VSlang(30104), 'notes.png', oOutputParameterHandler)

        # Par années
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showSeriesYears', self.addons.VSlang(30106), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30111), 'az.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30108), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()

        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_IDENTIFIER, 'showAnimesSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('sCat', '3')
            oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search-animes.png', oOutputParameterHandler)

        # Nouveautés
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showAnimesNews', self.addons.VSlang(30101), 'news.png', oOutputParameterHandler)

        # Populaires
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showAnimes', self.addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

        # TOP
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oGui.addDir(SITE_TMDB, 'showAnimesTop', self.addons.VSlang(30104), 'notes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30111), 'az.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30108), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANIMS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDramas(self):
        oGui = cGui()

        # Affiche les Nouveautés Dramas
        oOutputParameterHandler = cOutputParameterHandler()
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_IDENTIFIER, 'showDramasSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('sCat', '9')
            oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search-dramas.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30101), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

        # Affiche les Genres Dramas
        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30106), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30111), 'az.png', oOutputParameterHandler)

        # Affiche les Sources Dramas
        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_DRAMAS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = cGui()

        # Affiche les Nouveautés Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        if self.addons.getSetting('history-view') == 'true':
            oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
            oGui.addDir(SITE_IDENTIFIER, 'showDocsSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('sCat', '5')
            oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search-divers.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30101), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_DOCS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSports(self):
        oGui = cGui()

        # Affiche les live Sportifs
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_LIVE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30119), 'replay.png', oOutputParameterHandler)

        # Affiche les Genres Sportifs
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30105), 'genre_sport.png', oOutputParameterHandler)

        # Chaines
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_TV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30200), 'tv.png', oOutputParameterHandler)

        # Affiche les Sources Sportives
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_SPORTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDirect(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'showSports', self.addons.VSlang(30113), 'sport.png', oOutputParameterHandler)
#        oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', self.addons.VSlang(30115), 'tv.png', oOutputParameterHandler)
        oGui.addDir('radio', 'load', self.addons.VSlang(30203), 'radio.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

    def showMenuTV(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()

        # SI plusieurs sources proposent la TNT
        # oOutputParameterHandler.addParameter('siteUrl', 'CHAINE_TV')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30332), 'host.png', oOutputParameterHandler)
        # SINON accès direct à la seule source
        oOutputParameterHandler.addParameter('siteUrl', 'TV')
        oGui.addDir('freebox', 'showWeb', self.addons.VSlang(30332), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'CHAINE_CINE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30200), self.addons.VSlang(30133)), 'films.png', oOutputParameterHandler)
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30113)), 'host.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'TV_TV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30200)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '6')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30101), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

        # oOutputParameterHandler.addParameter('siteUrl', 'SPORT_REPLAY')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30113), 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_REPLAYTV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showNets(self):
        oGui = cGui()

        # Affiche les Nouveautés Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30114), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Vidéos
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30114), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Vidéos
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NETS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30114)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showUsers(self):
        oGui = cGui()
        oGui.addDir('siteonefichier', 'load', self.addons.VSlang(30327), 'sites/siteonefichier.png')
        oGui.addDir('alldebrid', 'load', 'AllDebrid', 'sites/alldebrid.png')
        oGui.addDir('sitedarkibox', 'load', 'DarkiBox', 'sites/sitedarkibox.png')
        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png')
        oGui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), 'trakt.png')
        # oGui.addDir('siteuptobox', 'load', 'Uptobox', 'sites/siteuptobox.png')
        oGui.setEndOfDirectory()

    def showTools(self):
        oGui = cGui()
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', self.addons.VSlang(30227), 'parametres.png')
        oGui.addDir('cDownload', 'getDownload', self.addons.VSlang(30224), 'download.png')
        oGui.addDir('cLibrary', 'getLibrary', self.addons.VSlang(30303), 'library.png')
        oGui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), 'web.png')
        oGui.addDir(SITE_IDENTIFIER, 'showDonation', self.addons.VSlang(30143), 'paypal.png')
        oGui.addDir('globalSources', 'globalSources', self.addons.VSlang(30449), 'host.png')
        oGui.setEndOfDirectory()

    def showHistory(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sCat = oInputParameterHandler.getValue('sCat')

        from resources.lib.db import cDb
        with cDb() as db:
            row = db.get_history(sCat)

        if row:
            oGui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416), '')
        else:
            oGui.addText(SITE_IDENTIFIER)
        oOutputParameterHandler = cOutputParameterHandler()
        for match in row:
            sTitle = match['title']
            sCat = match['disp']

            # on ne propose l'historique que pour les films, séries, animes, doc, drama
            if int(sCat) not in (1, 2, 3, 5, 9):
                continue 

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oOutputParameterHandler.addParameter('searchtext', sTitle)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')

            try:
                oGuiElement.setTitle('- ' + sTitle)
            except:
                oGuiElement.setTitle('- ' + str(sTitle, 'utf-8'))

            oGuiElement.setFileName(sTitle)
            oGuiElement.setCat(sCat)
            oGuiElement.setIcon('search.png')
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, 'cHome', 'delSearch', self.addons.VSlang(30412))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if row:
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', self.addons.VSlang(30413), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def showDonation(self):
        from resources.lib.librecaptcha.gui import cInputWindowYesNo
        inputText = 'Merci pour votre soutien, il permet de maintenir ce projet.\r\nScanner ce code ou rendez vous sur :\r\nhttps://www.paypal.com/paypalme/kodivstream'
        oSolver = cInputWindowYesNo(captcha='special://home/addons/plugin.video.vstream/paypal.jpg', msg=inputText, roundnum=1, okDialog=True)
        oSolver.get()


    def showHostDirect(self):  # fonction de recherche
        oGui = cGui()
        sUrl = oGui.showKeyBoard(heading=self.addons.VSlang(30045))
        if sUrl:

            oHoster = cHosterGui().checkHoster(sUrl)
            if oHoster:
                oHoster.setDisplayName(self.addons.VSlang(30046))
                oHoster.setFileName(self.addons.VSlang(30046))
                cHosterGui().showHoster(oGui, oHoster, sUrl, '')

        oGui.setEndOfDirectory()

    def opensetting(self):
        self.addons.openSettings()

    def delSearch(self):
        from resources.lib.db import cDb
        with cDb() as db:
            db.del_history()
        return True

    def callpluging(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')

        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sSiteUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        for aPlugin in aPlugins:
            try:
                icon = 'sites/%s.png' % (aPlugin[2])
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, oOutputParameterHandler)
            except:
                pass

        oGui.setEndOfDirectory()
