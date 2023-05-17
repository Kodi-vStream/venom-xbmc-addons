# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc

from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cWatched'
SITE_NAME = 'Watched'


class cWatched:

    DIALOG = dialog()
    ADDON = addon()

    def showMenu(self):
        oGui = cGui()
        addons = addon()

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'getWatched', addons.VSlang(30126), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')       # films
        oGui.addDir(SITE_IDENTIFIER, 'getWatched', addons.VSlang(30120), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '4')       # saisons
        oGui.addDir(SITE_IDENTIFIER, 'getWatched', '%s/%s' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122)), 'series.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')       # Divers
        oGui.addDir(SITE_IDENTIFIER, 'getWatched', self.ADDON.VSlang(30410), 'buzz.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getWatched(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        catFilter = oInputParameterHandler.getValue('sCat')

        with cDb() as DB:
            row = DB.get_allwatched()
            if not row:
                oGui.setEndOfDirectory()
                return

            for data in row:

                try:
                    title = data['title'].encode('utf-8')
                except:
                    title = data['title']
                if not title:
                    continue

                try:
                    cat = data['cat']
                    if catFilter and cat != catFilter:
                        continue

                    try:
                        siteurl = data['siteurl'].encode('utf-8')
                    except:
                        siteurl = data['siteurl']

                    if siteurl:
                        if isMatrix():
                            siteurl = UnquotePlus(siteurl.decode('utf-8'))
                            title = str(title, 'utf-8')
                        else:
                            siteurl = UnquotePlus(siteurl)

                    sTitleWatched = data['title_id']
                    site = data['site']
                    function = data['fav']
                    sSeason = data['season']
                    sTmdbId = data['tmdb_id'] if data['tmdb_id'] != '0' else ''

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', siteurl)
                    oOutputParameterHandler.addParameter('sMovieTitle', title)
                    oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
                    oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                    oOutputParameterHandler.addParameter('sSeason', sSeason)
                    oOutputParameterHandler.addParameter('sCat', cat)

                    if cat == '1':
                        oGui.addMovie(site, function, title, 'films.png', '', title, oOutputParameterHandler)
                    elif cat == '4':
                        oGui.addSeason(site, function, title, 'series.png', '', title, oOutputParameterHandler)
                    elif cat == '5':
                        oGui.addMisc(site, function, title, 'buzz.png', '', title, oOutputParameterHandler)
                    else:
                        continue # on ne presente pas l'historique des épisodes, il faut passer par l'historique des saisons

                except Exception as e:
                    pass

        oGui.setEndOfDirectory()

        return
