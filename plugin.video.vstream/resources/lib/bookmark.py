# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, xbmc
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
#         sTitle = cUtil().CleanName(sTitle)
        
        cDb().del_bookmark(siteUrl, sTitle, sCat, sAll)
        return True

    # Suppression d'un bookmark depuis un Widget
    def delBookmarkMenu(self):
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        sTitle = xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        siteUrl = xbmc.getInfoLabel('ListItem.Property(siteUrl)')

        cDb().del_bookmark(siteUrl, sTitle)

        return True

    def getBookmarks(self):
        oGui = cGui()

        # Comptages des marque-pages
        row = cDb().get_bookmark()

        compt = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in row:
            compt[int(i[5])] = compt[int(i[5])] + 1

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30120), str(compt[1])), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s/%s (%s)') % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122), str(compt[2])), 'mark.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sCat', '3')
        # oGui.addDir(SITE_IDENTIFIER, 'getFav()', 'Pages', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '6')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30332), str(compt[6])), 'mark.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sCat', '7')
        # oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30088), str(compt[7])), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        total = compt[3] + compt[4] + compt[5]
        oGui.addDir(SITE_IDENTIFIER, 'getFav', ('%s (%s)') % (self.ADDON.VSlang(30410), str(total)), 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sAll', 'true')
        oGui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30209), 'trash.png', oOutputParameterHandler)

        # A virer dans les versions future, pour le moment c'est juste pr supprimer les liens bugges
        if compt[0] > 0:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', '0')
            oGui.addDir(SITE_IDENTIFIER, 'getFav', '[COLOR red]Erreur /!\ lien à supprimer!!! (' + str(compt[0]) + ')[/COLOR]', 'mark.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        row = cDb().get_bookmark()

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
            gen = (x for x in row if x[5] in sCat)
        else:
            sCat = '5'
            gen = (x for x in row if x[5] not in ('1', '2', '6'))

        for data in gen:

            try:
                title = data[1].encode('utf-8')
            except:
                title = data[1]

            try:
                thumbnail = data[6].encode('utf-8')
            except:
                thumbnail = data[6]

            try:
                try:
                    siteurl = data[2].encode('utf-8')
                except:
                    siteurl = data[2]
                siteurl = UnquotePlus(siteurl)
                site = data[3]
                function = data[4]
                cat = data[5]
                fanart = data[7]

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
                if (cat  == '1'):
                    cGui.CONTENT = 'movies'
                    oGuiElement.setMeta(cat)
                    oGuiElement.setCat(1)
                elif (cat == '2'):
                    cGui.CONTENT = 'tvshows'
                    oGuiElement.setMeta(cat)
                    oGuiElement.setCat(2)
                else:
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(cat)
                oGuiElement.setThumbnail(thumbnail)
                oGuiElement.setFanart(fanart)
                oGuiElement.addItemProperties('isBookmark', True)

                oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler, 'cFav', 'cFav', 'delBookmark', self.ADDON.VSlang(30412))

                if (function == 'play'):
                    oGui.addHost(oGuiElement, oOutputParameterHandler)
                else:
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

            except:
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
        if int(sCat) not in (1, 2, 5):
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30038))
            return

        meta = {}
        
        sSiteUrl = oInputParameterHandler.getValue('siteUrl') if oInputParameterHandler.exist('siteUrl') else xbmc.getInfoLabel('ListItem.Property(siteUrl)')
        sTitle = oInputParameterHandler.getValue('sMovieTitle') if oInputParameterHandler.exist('sMovieTitle') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sSite = oInputParameterHandler.getValue('sId') if oInputParameterHandler.exist('sId') else xbmc.getInfoLabel('ListItem.Property(sId)')
        sFav = oInputParameterHandler.getValue('sFav') if oInputParameterHandler.exist('sFav') else xbmc.getInfoLabel('ListItem.Property(sFav)')

        meta['siteurl'] = sSiteUrl
        meta['title'] = sTitle
        meta['site'] = sSite
        meta['fav'] = sFav
        meta['cat'] = sCat

        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            cDb().insert_bookmark(meta)
        except:
            pass
