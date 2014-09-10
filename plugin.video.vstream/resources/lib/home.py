#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
import os
import urllib

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'
color_films = cConfig().getSetting('color_films')
color_series = cConfig().getSetting('color_series')
color_anims = cConfig().getSetting('color_anims')
color_tvs = cConfig().getSetting('color_tvs')

class cHome:
      

    def load(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('freebox', 'load', '[COLOR '+color_tvs+']Télévision[/COLOR]', 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNews', '[COLOR '+color_films+']Films Nouveautés[/COLOR]', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieViews', '[COLOR '+color_films+']Films Les Plus Vus[/COLOR]', 'views.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieComments', '[COLOR '+color_films+']Films Les Plus Commentés[/COLOR]', 'comments.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNotes', '[COLOR '+color_films+']Films Les Mieux Notés[/COLOR]', 'notes.png', oOutputParameterHandler)
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieGenres', '[COLOR '+color_films+']Films Par Genres[/COLOR]', 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieSeries', '[COLOR '+color_series+']Séries Nouveautés[/COLOR]', 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieVfs', '[COLOR '+color_series+']Séries VF[/COLOR]', 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieVostfrs', '[COLOR '+color_series+']Séries VOSTFR[/COLOR]', 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animAnims', '[COLOR '+color_anims+']Animes Nouveautés[/COLOR]', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animVfs', '[COLOR '+color_anims+']Animes VF[/COLOR]', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animVostfrs', '[COLOR '+color_anims+']Animes VOSTFR[/COLOR]', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animMovies', '[COLOR '+color_anims+']Animes Films[/COLOR]', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'docDocs', 'Documentaires', 'doc.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'sportSports', 'Sport', 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNets', 'Vidéo du Net', 'buzz.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getFavourites', '[COLOR teal]Marque-page[/COLOR]', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSources', 'Toutes les Sources', 'host.png', oOutputParameterHandler)


        
        oGui.setEndOfDirectory()
    
    def showTV(self):
        oGui = cGui()
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('freebox', 'load', '[COLOR '+color_tvs+']Télévision Box[/COLOR]', 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('chaine_tv', 'load', '[COLOR '+color_tvs+']Tv du net[/COLOR]', 'tv.png', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()

    def showSources(self):
        oGui = cGui()
        
        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins()
        for aPlugin in aPlugins:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(aPlugin[1], 'load', aPlugin[0], 'tv.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def movieNews(self):
        self.__callpluging('showMovies','MOVIE_NEWS', '[COLOR '+color_films+']Films Nouveautés[/COLOR]', 'news.png')

    def movieViews(self):
        self.__callpluging('showMovies','MOVIE_VIEWS', '[COLOR '+color_films+']Films Les Plus Vus[/COLOR]', 'views.png')

    def movieComments(self):
        self.__callpluging('showMovies','MOVIE_COMMENTS', '[COLOR '+color_films+']Films Les Plus Commentés[/COLOR]', 'comments.png')

    def movieNotes(self):
        self.__callpluging('showMovies','MOVIE_NOTES', '[COLOR '+color_films+']Films Les Mieux Notés[/COLOR]', 'notes.png')

    def movieGenres(self):
        self.__callpluging('showGenre','MOVIE_GENRES', '[COLOR '+color_films+']Films Par Genres[/COLOR]', 'genres.png')

    def serieSeries(self):
        self.__callpluging('showMovies','SERIE_SERIES', '[COLOR '+color_series+']Séries Nouveautés[/COLOR]', 'series.png')

    def serieVfs(self):
        self.__callpluging('showMovies','SERIE_VFS', '[COLOR '+color_series+']Séries VF[/COLOR]', 'series.png')

    def serieVostfrs(self):
        self.__callpluging('showMovies','SERIE_VOSTFRS', '[COLOR '+color_series+']Séries VOSTFR[/COLOR]', 'series.png')

    def animAnims(self):
        self.__callpluging('showMovies','ANIM_ANIMS', '[COLOR '+color_anims+']Animes Nouveautés[/COLOR]', 'animes.png')

    def animVfs(self):
        self.__callpluging('showMovies','ANIM_VFS', '[COLOR '+color_anims+']Animes VF[/COLOR]', 'animes.png')

    def animVostfrs(self):
        self.__callpluging('showMovies','ANIM_VOSTFRS', '[COLOR '+color_anims+']Animes VOSTFR[/COLOR]', 'animes.png')

    def animMovies(self):
        self.__callpluging('showMovies','ANIM_MOVIES', '[COLOR '+color_anims+']Animes OAVS/Films[/COLOR]', 'animes.png')

    def docDocs(self):
        self.__callpluging('showMovies','DOC_DOCS', 'Documentaires', 'doc.png')

    def sportSports(self):
        self.__callpluging('showReplay','SPORT_SPORTS', 'Sport', 'sport.png')

    def movieNets(self):
        self.__callpluging('showReplay','MOVIE_NETS', 'Vidéo du Net', 'buzz.png')

    def showSearch(self):
        oGui = cGui()
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'searchMovie', 'Recherche Films/Series/mangas', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'searchDoc', 'Recherche Documentaires', 'search.png', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()

    def searchMovie(self):
        oGui = cGui()
        liste = []
        liste.append( ["frenchstream_org", "showMovies", "http://frenchstream.org/?s="] )
        liste.append( ["full_streaming_org", "showMovies", "http://full-streaming.org/xfsearch/"] )
        liste.append( ["adkami_com", "showMovies", "http://www.adkami.com/video?recherche="] )
        liste.append( ["dpstreaming_org", "showMovies", "http://dpstreaming.org/?s="] )
        liste.append( ["fifostream_me", "showMovies", "http://www.fifostream.me/?s="] )
        liste.append( ["filmstreamingz_fr", "showMovies", "http://filmstreamingz.fr/?s="] )
        liste.append( ["filmstreamingz_fr", "showMovies", "http://seriestreaming.org/?s="] )
        liste.append( ["full_stream_net", "showMovies", "http://full-stream.net/xfsearch/"] )
        liste.append( ["fullmoviz_org", "showMovies", "http://www.fullmoviz.org/?s="] )
        liste.append( ["streamzer_net", "resultSearch", "http://www.streamzer.net/index.php?file=Search&op=mod_search&main="] )
        liste.append( ["vos_animes_com", "showMovies", "http://www.vos-animes.com/xfsearch/"] )
        self.__callsearch(liste)
        oGui.setEndOfDirectory()

    def searchDoc(self):
        oGui = cGui()
        liste = []
        liste.append( ["docspot_fr", "showMovies", "http://www.docspot.fr/?s="] )
        liste.append( ["notre_ecole_net", "showMovies", "http://www.notre-ecole.net/?s="] )
        liste.append( ["reportagestv_com", "showMovies", "http://www.reportagestv.com/?s="] )
        liste.append( ["streamzer_net", "resultSearch", "http://www.streamzer.net/index.php?file=Search&op=mod_search&main="] )
        self.__callsearch(liste)
        oGui.setEndOfDirectory()

        

    def __callpluging(self, sFunction, sVar, sTitle, sIcon):
        oGui = cGui()
        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins()
        for aPlugin in aPlugins:
            try:
                exec "import "+aPlugin[1]
                exec "sSiteUrl = "+aPlugin[1]+"."+sVar
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
                oGui.addDir(aPlugin[1], sFunction, sTitle+' - [COLOR azure]'+aPlugin[0]+'[/COLOR]', sIcon, oOutputParameterHandler)
            except:        
                pass

        oGui.setEndOfDirectory()

    def __callsearch(self, liste):
        oGui = cGui()
        sSearchText = oGui.showKeyBoard()
        for sSiteName, sFunction,sUrl in liste: 
            if (sSearchText != False):
                sUrl = sUrl+sSearchText 
                try:
                    exec "import "+sSiteName+" as search"
                    searchUrl = "search.%s('%s')" % (sFunction, sUrl)
                    exec searchUrl
                except:       
                    pass
            else: return
        oGui.setEndOfDirectory()

