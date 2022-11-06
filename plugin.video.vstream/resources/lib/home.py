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
from resources.lib.comaddon import addon, window

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'


class cHome:

    addons = addon()

    def load(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showVOD', self.addons.VSlang(30131), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDirect', self.addons.VSlang(30132), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.addons.VSlang(30350), 'replay.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMyVideos', self.addons.VSlang(30130), 'star.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'ShowTools', self.addons.VSlang(30033), 'tools.png', oOutputParameterHandler)

        view = False
        if (self.addons.getSetting('active-view') == 'true'):
            view = self.addons.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)

    def showVOD(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMenuSearch', self.addons.VSlang(30076), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.addons.VSlang(30120), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.addons.VSlang(30121), 'series.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.addons.VSlang(30112), 'buzz.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.addons.VSlang(30122), 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDramas', self.addons.VSlang(30124), 'dramas.png', oOutputParameterHandler)

        # ininteressant
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir(SITE_IDENTIFIER, 'showNets', self.addons.VSlang(30114), 'buzz.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMyVideos(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cViewing', 'showMenu', self.addons.VSlang(30125), 'replay.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getBookmarks', self.addons.VSlang(30207), 'mark.png', oOutputParameterHandler)

        oGui.addDir('cDownload', 'getDownloadList', self.addons.VSlang(30229), 'download.png', oOutputParameterHandler)

        # les enregistrements de chaines TV ne sont plus opérationnelles
        # folder = self.addons.getSetting('path_enregistrement')
        # if not folder:
        #     folder = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement"/>'
        # oOutputParameterHandler.addParameter('siteUrl', folder)
        # oGui.addDir('cLibrary', 'openLibrary', self.addons.VSlang(30225), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showUsers', self.addons.VSlang(30455), 'user.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'activeSources', self.addons.VSlang(30362), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def showMenuSearch(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'load', self.addons.VSlang(30088), 'searchtmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'series.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '9')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30123), 'dramas.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30080), 'buzz.png', oOutputParameterHandler)

        if (self.addons.getSetting('history-view') == 'true'):
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.addons.VSlang(30308), 'annees.png', oOutputParameterHandler)

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

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_HD')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30160)), 'hd.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30102)), 'views.png', oOutputParameterHandler)

        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_COMMENTS')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30103)), 'comments.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30111)), 'az.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_NOTES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30104)), 'notes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ENFANTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30109)), 'enfants.png', oOutputParameterHandler)

        # oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VF')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30107)), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VOSTFR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30108)), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_MOVIE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30120)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30102)), 'views.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30111)), 'az.png', oOutputParameterHandler)

        # oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VFS')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30107)), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30108)), 'vostfr.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30121)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30102)), 'views.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30111)), 'az.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_VOSTFRS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30108)), 'vf.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANIMS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30122)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDramas(self):
        oGui = cGui()

        # Affiche les Nouveautés Dramas
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '9')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30123), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_VIEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30102)), 'views.png', oOutputParameterHandler)

        # Affiche les Genres Dramas
        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30106)), 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_LIST')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30111)), 'az.png', oOutputParameterHandler)

        # Affiche les Sources Dramas
        oOutputParameterHandler.addParameter('siteUrl', 'DRAMA_DRAMAS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30124)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = cGui()

        # Affiche les Nouveautés Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30080), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_DOCS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30112)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSports(self):
        oGui = cGui()

        # Affiche les live Sportifs
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_LIVE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30119)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_TV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30200)), 'tv.png', oOutputParameterHandler)

        # Affiche les Genres Sportifs
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Sportives
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_SPORTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30113)), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDirect(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'showSports', self.addons.VSlang(30113), 'sport.png', oOutputParameterHandler)
        oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', self.addons.VSlang(30115), 'tv.png', oOutputParameterHandler)
        oGui.addDir('freebox', 'showMenuMusic', self.addons.VSlang(30203), 'music.png', oOutputParameterHandler)
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
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30134), 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_REPLAY')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30113)), 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_REPLAYTV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30117)), 'host.png', oOutputParameterHandler)

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

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteuptobox', 'load', 'Uptobox', 'sites/siteuptobox.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteonefichier', 'load', self.addons.VSlang(30327), 'sites/siteonefichier.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def ShowTools(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', self.addons.VSlang(30227), 'notes.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', self.addons.VSlang(30224), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', self.addons.VSlang(30303), 'library.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), 'host.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'globalSources', self.addons.VSlang(30449), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def opensetting(self):
        addon().openSettings()


    def showHistory(self):
        oGui = cGui()

        from resources.lib.db import cDb
        with cDb() as db:
            row = db.get_history()

        if row:
            oGui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416))
        else:
            oGui.addText(SITE_IDENTIFIER)
        oOutputParameterHandler = cOutputParameterHandler()
        for match in row:
            sTitle = match['title']
            sCat = match['disp']

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
