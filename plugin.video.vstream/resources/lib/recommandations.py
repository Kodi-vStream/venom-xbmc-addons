from resources.lib.comaddon import dialog, addon
from resources.lib.gui.gui import cGui
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler

from resources.lib.db import cDb
from resources.sites.themoviedb_org import SITE_IDENTIFIER as SITE_TMDB

SITE_IDENTIFIER = 'cRecommandations'
SITE_NAME = 'Recommandations'

class cRecommandations:
    DIALOG = dialog()
    ADDON = addon()

    def showMoviesRecommandations(self):
        oGui = cGui()
        try:
            with cDb() as DB:
                row = DB.get_catWatched('1', 5)

                if not row:
                    oGui.setEndOfDirectory()
                    return
                
                for data in row:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sTmdbId', data['tmdb_id'])
                    oOutputParameterHandler.addParameter('siteUrl', 'movie/'+data['tmdb_id']+'/recommendations')
                    oGui.addMovie(SITE_TMDB, 'showMovies', self.ADDON.VSlang(31213)+ ' ' +data['title'], 'films.png', '', '', oOutputParameterHandler)
        except:
            pass
        # On force la vue fichier. 
        # La vue films ou séries ne rendrait pas bien en n'affichant pas le texte "Parce que vous avez regardé..." et pourrai semer de la confusion
        cGui.CONTENT = 'files'
        oGui.setEndOfDirectory()

    def showShowsRecommandations(self):
        oGui = cGui()
        try:
            with cDb() as DB:
                row = DB.get_catWatched('4', 5)

                if not row:
                    oGui.setEndOfDirectory()
                    return
                
                for data in row:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sTmdbId', data['tmdb_id'])
                    oOutputParameterHandler.addParameter('siteUrl', 'tv/'+data['tmdb_id']+'/recommendations')
                    oGui.addMovie(SITE_TMDB, 'showSeries', self.ADDON.VSlang(31213)+ ' ' +data['title'], 'series.png', '', '', oOutputParameterHandler)
        except:
            pass
        # On force la vue fichier. 
        # La vue films ou séries ne rendrait pas bien en n'affichant pas le texte "Parce que vous avez regardé..." et pourrai semer de la confusion
        cGui.CONTENT = 'files'
        oGui.setEndOfDirectory()