from sys import excepthook
from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler

from resources.lib.db import cDb
from resources.lib.tmdb import cTMDb
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
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
                    oOutputParameterHandler.addParameter('siteUrl', 'movie/'+data['tmdb_id']+'/recommendations')
                    oGui.addDir(SITE_TMDB, 'showMovies', 'Parce que vous avez regardé: '+data['title'], 'search.png', oOutputParameterHandler)
        except:
            pass
        oGui.setEndOfDirectory()

    def showShowsRecommandations(self):
        oGui = cGui()

        with cDb() as DB:
            row = DB.get_catWatched('4', 5)

            if not row:
                oGui.setEndOfDirectory()
                return
            
            for data in row:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'tv/'+data['tmdb_id']+'/recommendations')
                oGui.addDir(SITE_TMDB, 'showSeries', 'Parce que vous avez regardé: '+data['title'], 'search.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()