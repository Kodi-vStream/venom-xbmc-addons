from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler

from resources.lib.db import cDb
from resources.lib.tmdb import cTMDb



SITE_IDENTIFIER = 'cRecommandations'
SITE_NAME = 'Recommandations'


class cRecommandations:
    DIALOG = dialog()
    ADDON = addon()

    def showMoviesRecommandations(self):
        oGui = cGui()
        addons = addon()
        tmdb = cTMDb()


        with cDb() as DB:
            row = DB.get_catWatched('1')

            if not row:
                oGui.setEndOfDirectory()
                return
            
            for data in row:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('tmdbIdRecommandations', data['tmdb_id'])
                oGui.addDir(SITE_IDENTIFIER, 'showRecommandationsForMovie', 'Parce que vous avez regardé: '+data['title'], 'search.png', oOutputParameterHandler)
            
            
                # print("HEHO UN FILM")
                # print(data['title'] + ' - ' + data['tmdb_id'])
                # tmdb.get_recommandations_by_id_movie(data['tmdb_id'])

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sCat', '1')       # films
        # oGui.addDir('cWatched', 'getWatched', addons.VSlang(30120), 'films.png', oOutputParameterHandler)


        oGui.setEndOfDirectory()


    def showRecommandationsForMovie(self):
        oInputParameterHandler = cInputParameterHandler()
        tmdbId = oInputParameterHandler.getValue('tmdbIdRecommandations')

        print("Je recherche des reco pour:"+tmdbId)


    def showSeriesRecommandations(self):
        oGui = cGui()
        addons = self.addons
        oOutputParameterHandler = cOutputParameterHandler()

        print("ICI JE VEUX AFFICHER MON HISTORIQUE SERIES")

        oGui.addDir(SITE_IDENTIFIER, 'nothing series', "Nothing", 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

