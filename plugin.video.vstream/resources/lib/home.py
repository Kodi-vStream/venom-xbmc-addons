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

class cHome:
      

    def load(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showTV', 'Télévision', 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'docDocs', 'Documentaires', 'doc.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNews', 'Films Nouveautés', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieViews', 'Films Les Plus Vus', 'views.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieComments', 'Films Les Plus Commentés', 'comments.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNotes', 'Films Les Mieux Notés', 'notes.png', oOutputParameterHandler)
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieGenres', 'Films Par Genres', 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieSeries', 'Séries Nouveautés', 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieVfs', 'Séries VF', 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'serieVostfrs', 'Séries VOSTFR', 'series.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animAnims', 'Animes Nouveautés', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animVfs', 'Animes VF', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animVostfrs', 'Animes VOSTFR', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'animMovies', 'Animes Films', 'animes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'sportSports', 'Sport', 'sport.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'movieNets', 'Vidéo du Net', 'buzz.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getFavourites', 'Marque-page', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSources', 'Toutes les Sources', 'host.png', oOutputParameterHandler)


        
        oGui.setEndOfDirectory()
    
    def showTV(self):
        oGui = cGui()
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('freebox', 'load', 'FreeBox', 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('chaine_tv', 'load', 'Tv du net', 'tv.png', oOutputParameterHandler)
        
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
        self.__callpluging('showMovies','MOVIE_NEWS', 'Nouveautés', 'news.png')

    def movieViews(self):
        self.__callpluging('showMovies','MOVIE_VIEWS', 'Les Plus Vus', 'views.png')

    def movieComments(self):
        self.__callpluging('showMovies','MOVIE_COMMENTS', 'Les Plus Commentés', 'comments.png')

    def movieNotes(self):
        self.__callpluging('showMovies','MOVIE_NOTES', 'Les Mieux Notés', 'notes.png')

    def movieGenres(self):
        self.__callpluging('showGenre','MOVIE_GENRES', 'Par Genres', 'genres.png')

    def serieSeries(self):
        self.__callpluging('showMovies','SERIE_SERIES', 'Nouveautés', 'series.png')

    def serieVfs(self):
        self.__callpluging('showMovies','SERIE_VFS', 'VF', 'series.png')

    def serieVostfrs(self):
        self.__callpluging('showMovies','SERIE_VOSTFRS', 'VOSTFR', 'series.png')

    def animAnims(self):
        self.__callpluging('showMovies','ANIM_ANIMS', 'Nouveautés', 'animes.png')

    def animVfs(self):
        self.__callpluging('showMovies','ANIM_VFS', 'VF', 'animes.png')

    def animVostfrs(self):
        self.__callpluging('showMovies','ANIM_VOSTFRS', 'VOSTFR', 'animes.png')

    def animMovies(self):
        self.__callpluging('showMovies','ANIM_MOVIES', 'OAVS/Films', 'animes.png')

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

