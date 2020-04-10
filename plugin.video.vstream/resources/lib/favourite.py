#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, xbmc
import urllib

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'

class cFav:

    DIALOG = dialog()
    ADDON = addon()

    #effacement direct par menu
    def delBookmarksMenu(self):
        if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            cDb().del_bookmark()
        return True

    #avec confirmation pour les autres
    def delBookmarks(self):
        if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            cDb().del_bookmark()
        return True

    def getBookmarks(self):
        oGui = cGui()

        #Comptages des marque-pages
        row = cDb().get_bookmark()

        compt = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in row:
            compt[int(i[5])] = compt[int(i[5])] + 1

        # sTitle = '[COLOR khaki]Vous avez %s marque-page[/COLOR]' % (len(row))
        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://')
        # oGui.addText(SITE_IDENTIFIER, sTitle)

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
        oGui.addDir(SITE_IDENTIFIER, 'delBookmarks', self.ADDON.VSlang(30209), 'trash.png', oOutputParameterHandler)

        #A virer dans les versions future, pour le moment c'est juste pr supprimer les liens bugges
        if compt[0] > 0:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', '0')
            oGui.addDir(SITE_IDENTIFIER, 'getFav', '[COLOR red]Erreur /!\ lien à supprimer!!! (' + str(compt[0]) + ')[/COLOR]', 'mark.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()

        #aParams = oInputParameterHandler.getAllParameter()

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
                siteurl = urllib.unquote_plus(data[2])
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
                #Dans ajouter source c'est bien sThumb donc...
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

                #self.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)
                oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler, 'cFav', 'cFav', 'delBookmarksMenu', self.ADDON.VSlang(30412))

                if (function == 'play'):
                    oGui.addHost(oGuiElement, oOutputParameterHandler)
                else:
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

                    #oGui.addFav(site, function, title, 'mark.png', thumbnail, fanart, oOutputParameterHandler)

            except:
                oGui.addDir(SITE_IDENTIFIER, 'DoNothing', '[COLOR red]ERROR[/COLOR]', 'films.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', sCat)
        oGui.addDir(SITE_IDENTIFIER, 'delBookmarks', self.ADDON.VSlang(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

        return

    def setBookmark(self):
        oInputParameterHandler = cInputParameterHandler()

        if oInputParameterHandler.getValue('sId') == 'kepliz_com':
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30037))
            return

        if int(oInputParameterHandler.getValue('sCat')) < 1:
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30038))
            return

        meta = {}
        meta['siteurl'] = oInputParameterHandler.getValue('siteUrl')
        meta['site'] = oInputParameterHandler.getValue('sId')
        meta['fav'] = oInputParameterHandler.getValue('sFav')
        meta['cat'] = oInputParameterHandler.getValue('sCat')

        #ListItem.title contient des code de couleurs, sMovieTitle le titre en plus "propre"
        #Inutile a la prochaine version, car plus de couleurs a la base.
        if oInputParameterHandler.getValue('sMovieTitle'):
            meta['title'] = oInputParameterHandler.getValue('sMovieTitle')
        else:
            meta['title'] = xbmc.getInfoLabel('ListItem.title')

        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] =  xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            cDb().insert_bookmark(meta)
        except:
            pass
