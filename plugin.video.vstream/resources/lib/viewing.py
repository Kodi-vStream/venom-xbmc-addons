# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.comaddon import dialog, addon, xbmc, isMatrix
from resources.lib.db import cDb
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.gui.gui import cGui
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cViewing'
SITE_NAME = 'Viewing'


class cViewing:

    DIALOG = dialog()
    ADDON = addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delViewing(self):
        oInputParameterHandler = cInputParameterHandler()
        sTitleWatched = oInputParameterHandler.getValue('sTitleWatched')
        sCat = oInputParameterHandler.getValue('sCat')

        if not sTitleWatched:  # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False

        meta = {}
        meta['titleWatched'] = sTitleWatched
        meta['cat'] = sCat

        if cDb().del_viewing(meta):
            self.DIALOG.VSinfo(addon().VSlang(30072))
            cGui().updateDirectory()
        return True

    # Suppression d'un bookmark depuis un Widget
    def delViewingMenu(self):
        sTitle = xbmc.getInfoLabel('ListItem.OriginalTitle')
        if not sTitle:    # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False
        sCat = xbmc.getInfoLabel('ListItem.Property(sCat)')
        meta = {}
        meta['titleWatched'] = sTitle
        meta['cat'] = sCat
        if cDb().del_viewing(meta):
            self.DIALOG.VSinfo(addon().VSlang(30072))
            cGui().updateDirectory()

        return True

    def getViewing(self):
        oGui = cGui()
        DB = cDb()
        # oInputParameterHandler = cInputParameterHandler()

        row = DB.get_viewing()
        if not row:
            oGui.setEndOfDirectory()
            return

        for data in row:

            try:
                title = data['title'].encode('utf-8')
            except:
                title = data['title']

            try:
                try:
                    siteurl = data['siteurl'].encode('utf-8')
                except:
                    siteurl = data['siteurl']

                if isMatrix():
                    siteurl = UnquotePlus(siteurl.decode('utf-8'))
                    title = str(title, 'utf-8')
                else:
                    siteurl = UnquotePlus(siteurl)

                sTitleWatched = data['title_id']
                site = data['site']
                function = data['fav']
                cat = data['cat']
                sSeason = data['season']
                sTmdbId = data['tmdb_id']  # if 'tmdb_id' in data else None

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteurl)
                oOutputParameterHandler.addParameter('sMovieTitle', title)
                oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
                oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                oOutputParameterHandler.addParameter('sSeason', sSeason)
                oOutputParameterHandler.addParameter('sCat', cat)
                oOutputParameterHandler.addParameter('isViewing', True)

                # pourcentage de lecture
                meta = {}
                meta['title'] = sTitleWatched
                resumetime, totaltime = DB.get_resume(meta)
                oOutputParameterHandler.addParameter('ResumeTime', resumetime)
                oOutputParameterHandler.addParameter('TotalTime', totaltime)

                if cat == '1':
                    oListItem = oGui.addMovie(site, function, title, 'films.png', '', title, oOutputParameterHandler)
                elif cat == '5':
                    oListItem = oGui.addMisc(site, function, title, 'films.png', '', title, oOutputParameterHandler)
                elif cat == '4':
                    oListItem = oGui.addSeason(site, function, title, 'series.png', '', title, oOutputParameterHandler)
                else:
                    oListItem = oGui.addTV(site, function, title, 'series.png', '', title, oOutputParameterHandler)

                oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                oOutputParameterHandler.addParameter('sCat', cat)
                oListItem.addMenu(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30412), oOutputParameterHandler)

            except Exception as e:
                pass

        # Vider toute la catégorie n'est pas accessible lors de l'utilisation en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            oOutputParameterHandler = cOutputParameterHandler()
            oGui.addDir(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

        return
