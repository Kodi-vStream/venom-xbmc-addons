#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler

import urllib
import xbmc

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'

class cFav:

    def __init__(self):
        self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        #self.__sFunctionName = ''

    #effacement direct par menu
    def delFavouritesMenu(self):
        cDb().del_favorite()
        return True

    #avec confirmation pour les autres
    def delFavourites(self):
        if cConfig().createDialogYesNo("Voulez vous vraiment supprimer toute cette liste"):
            cDb().del_favorite()
        return True

    def getFavourites(self):
        oGui = cGui()

        #Comptages des favoris
        row = cDb().get_favorite()

        compt = [0,0,0,0,0,0,0,0]
        for i in row:
            compt[int(i[5])] = compt[int(i[5])] + 1

        # sTitle = '[COLOR khaki]Vous avez %s marque page[/COLOR]' % (len(row))
        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://')
        # oGui.addText(SITE_IDENTIFIER, sTitle)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Films (' + str(compt[1]) + ')', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Séries (' + str(compt[2]) + ')', 'mark.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sCat', '3')
        # oGui.addDir(SITE_IDENTIFIER, 'getFav()', 'Pages', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '6')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'TV (' + str(compt[6]) + ')', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '4')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Sources (' + str(compt[4]) + ')', 'mark.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sCat', '7')
        # oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Recherche Visuelle (' + str(compt[7]) + ')', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Divers (' + str(compt[5]) + ')', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sAll', 'true')
        oGui.addDir(SITE_IDENTIFIER, 'delFavourites', cConfig().getlanguage(30209), 'trash.png', oOutputParameterHandler)

        #A virer dans les versions future, pour le moment c'est juste pr supprimer les liens bugges
        if compt[0] > 0:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', '0')
            oGui.addDir(SITE_IDENTIFIER, 'getFav', '[COLOR red]Erreur /!\ lien a supprimer !!! (' + str(compt[0]) + ')[/COLOR]', 'mark.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()

        #aParams = oInputParameterHandler.getAllParameter()

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
        else:
            sCat = '5'

        row = cDb().get_favorite()

        for data in row:

            try:
                title = data[1].encode('utf-8')
            except:
                title = data[1]


            try:

                siteurl = urllib.unquote_plus(data[2])
                site = data[3]
                function = data[4]
                cat = data[5]
                thumbnail = data[6]
                fanart = data[7]

                if thumbnail == '':
                    thumbnail = 'False'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteurl)
                oOutputParameterHandler.addParameter('sMovieTitle', title)
                oOutputParameterHandler.addParameter('searchtext', title)
                oOutputParameterHandler.addParameter('sThumbnail', thumbnail)

                if (function == 'play'):
                    oHoster = cHosterGui().checkHoster(siteurl)
                    oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
                    oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
                    oOutputParameterHandler.addParameter('sMediaUrl', siteurl)

                if (cat == sCat):
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
                    oGui.CreateSimpleMenu(oGuiElement,oOutputParameterHandler,'cFav','cFav','delFavouritesMenu',cConfig().getlanguage(30412))

                    if (function == 'play'):
                        oGui.addHost(oGuiElement, oOutputParameterHandler)
                    else:
                        oGui.addFolder(oGuiElement, oOutputParameterHandler)

                    #oGui.addFav(site, function, title, "mark.png", thumbnail, fanart, oOutputParameterHandler)

            except:
                oGui.addDir(SITE_IDENTIFIER, 'DoNothing', '[COLOR red]ERROR[/COLOR]', 'films.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', sCat)
        oGui.addDir(SITE_IDENTIFIER, 'delFavourites', cConfig().getlanguage(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

        return

    def setFavorite(self):
        oInputParameterHandler = cInputParameterHandler()
        #cConfig().log(str(oInputParameterHandler.getAllParameter()))

        if oInputParameterHandler.getValue('sId') == 'kepliz_com':
            cConfig().showInfo('Error','Non possible pour ce site')
            return

        if int(oInputParameterHandler.getValue('sCat')) < 1:
            cConfig().showInfo('Error','Mise en Favoris non possible pour ce lien')
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
            cDb().insert_favorite(meta)
        except:
            pass
