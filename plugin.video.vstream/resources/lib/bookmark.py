# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc

from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'


class cFav:

    DIALOG = dialog()
    ADDON = addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delBookmark(self):
        oInputParameterHandler = cInputParameterHandler()
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        sAll = oInputParameterHandler.exist('sAll')
        sCat = oInputParameterHandler.getValue('sCat')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('sCleanTitle')
        # sTitle = cUtil().CleanName(sTitle)
        with cDb() as db:
            db.del_bookmark(siteUrl, sTitle, sCat, sAll)
        return True

    # Suppression d'un bookmark depuis un Widget
    def delBookmarkMenu(self):
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        sTitle = xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        siteUrl = xbmc.getInfoLabel('ListItem.Property(siteUrl)')
        with cDb() as db:
            db.del_bookmark(siteUrl, sTitle)

        return True

    def getBookmarks(self):
        oGui = cGui()

        # Comptages des marque-pages
        with cDb() as db:
            row = db.get_bookmark()

        compt = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in row:
            compt[int(i[5])] = compt[int(i[5])] + 1

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        total = compt[1] + compt[7]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30120), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        total = compt[2] + compt[3] + compt[4] + compt[8]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s/%s (%s)') % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '6')
        total = compt[6]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30332), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '5')
        total = compt[5]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30410), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sAll', 'true')
        oGui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30209), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        # Comptages des marque-pages
        with cDb() as db:
            row = db.get_bookmark()

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')

            # Série, Animes, Saison et Episodes sont visibles dans les marques-page "Séries"
            catList = ('2', '3', '4', '8')
            if sCat in catList:
                sCat = 2
                cGui.CONTENT = 'tvshows'
            else:
                catList = ('1', '7')    # films, saga
                cGui.CONTENT = 'movies'
                if sCat in catList:
                    sCat = 1
                else:
                    catList = sCat
                    cGui.CONTENT = 'videos'
            gen = (x for x in row if x['cat'] in catList)
        else:
            oGui.setEndOfDirectory()
            return

        for data in gen:

            try:
                title = data['title'].encode('utf-8')
            except:
                title = data['title']

            thumbnail = data['icon']

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

                site = data['site']
                function = data['fav']
                cat = data['cat']
                fanart = data['fanart']

                if thumbnail == '':
                    thumbnail = 'False'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteurl)
                oOutputParameterHandler.addParameter('sMovieTitle', title)
                oOutputParameterHandler.addParameter('searchtext', title)
                oOutputParameterHandler.addParameter('sThumbnail', thumbnail)
                # Dans ajouter source c'est bien sThumb donc...
                oOutputParameterHandler.addParameter('sThumb', thumbnail)

                if (function == 'play'):
                    oHoster = cHosterGui().checkHoster(siteurl)
                    oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
                    oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
                    oOutputParameterHandler.addParameter('sMediaUrl', siteurl)

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(site)
                oGuiElement.setFunction(function)
                oGuiElement.setTitle(title)
                oGuiElement.setFileName(title)
                oGuiElement.setIcon("mark.png")
                if (cat  == '1'):           # Films
                    oGuiElement.setMeta(1)
                    oGuiElement.setCat(1)
                elif (cat == '2'):          # Séries
                    oGuiElement.setMeta(2)
                    oGuiElement.setCat(2)
                elif (cat == '3'):          # Anime
                    oGuiElement.setMeta(4)
                    oGuiElement.setCat(3)
                elif (cat == '4'):          # Saisons
                    oGuiElement.setMeta(5)
                    oGuiElement.setCat(4)
                elif (cat == '5'):          # Divers
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(5)
                elif (cat == '6'):          # TV (Officiel)
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(6)
                elif (cat == '7'):          # Saga
                    oGuiElement.setMeta(3)
                    oGuiElement.setCat(7)
                elif (cat == '8'):          # Episodes
                    oGuiElement.setMeta(6)
                    oGuiElement.setCat(8)
                else:
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(cat)
                oGuiElement.setThumbnail(thumbnail)
                oGuiElement.setFanart(fanart)
                oGuiElement.addItemProperties('isBookmark', True)

                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'delBookmark', self.ADDON.VSlang(30412))

                if (function == 'play'):
                    oGui.addHost(oGuiElement, oOutputParameterHandler)  # addHost n'existe plus
                else:
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

            except:
                oOutputParameterHandler = cOutputParameterHandler()
                oGui.addDir(SITE_IDENTIFIER, 'DoNothing', '[COLOR red]ERROR[/COLOR]', 'films.png', oOutputParameterHandler)

        # La suppression n'est pas accessible lors de l'utilisation en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', sCat)
            oGui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

        return

    def setBookmark(self):
        oInputParameterHandler = cInputParameterHandler()

        sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')
        iCat = 0
        if sCat:
            iCat = int(sCat)
        if iCat < 1 or iCat > 8:
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30038))
            return

        meta = {}

        sSiteUrl = oInputParameterHandler.getValue('siteUrl') if oInputParameterHandler.exist('siteUrl') else xbmc.getInfoLabel('ListItem.Property(siteUrl)')
        sTitle = oInputParameterHandler.getValue('sMovieTitle') if oInputParameterHandler.exist('sMovieTitle') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sSite = oInputParameterHandler.getValue('sId') if oInputParameterHandler.exist('sId') else xbmc.getInfoLabel('ListItem.Property(sId)')
        sFav = oInputParameterHandler.getValue('sFav') if oInputParameterHandler.exist('sFav') else xbmc.getInfoLabel('ListItem.Property(sFav)')

        if sTitle == '':
            self.DIALOG.VSinfo('Error', 'Probleme sur le titre')
            return

        meta['siteurl'] = sSiteUrl
        meta['title'] = sTitle
        meta['site'] = sSite
        meta['fav'] = sFav
        meta['cat'] = sCat

        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            # Comptages des marque-pages
            with cDb() as db:
                db.insert_bookmark(meta)
        except:
            pass
