#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
import os
import urllib
import xbmc

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'

class cFav:

    def __init__(self):
        self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        #self.__sFunctionName = ''
      

    def delFavourites(self):
        
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        meta = {}      
        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['siteurl'] = siteUrl
        try:
            cDb().del_favorite(meta)
        except:
            pass
        
        #sTitle = oInputParameterHandler.getValue('sTitle')
        #sId = oInputParameterHandler.getValue('sId')
        #sUrl = oInputParameterHandler.getValue('siteUrl')
        #sFav = oInputParameterHandler.getValue('sFav')
        return
    
   
     
    def getFavourites(self):
        oGui = cGui()

        row = cDb().get_countfavorite()
        sTitle = '[COLOR khaki]Vous avez %s marque page[/COLOR]' % (str(row))
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, sTitle, oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Films', 'mark.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Séries', 'mark.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('sCat', '3')
        # oGui.addDir(SITE_IDENTIFIER, 'getFav()', 'Pages', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '4')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Sources', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Divers', 'mark.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '6')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'TV', 'mark.png', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()

        #aParams = oInputParameterHandler.getAllParameter()

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
        else:
            sCat = '5'
        
        try:
            row = cDb().get_favorite()

            for data in row:

                title = data[1]
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
                    oGuiElement.setIcon("mark.png")
                    oGuiElement.setMeta(0)
                    oGuiElement.setThumbnail(thumbnail)
                    oGuiElement.setFanart(fanart)
                    
                    oGui.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)
                    
                    if (function == 'play'):
                        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)
                    else:
                        oGui.addFolder(oGuiElement, oOutputParameterHandler)
                        
                    #oGui.addFav(site, function, title, "mark.png", thumbnail, fanart, oOutputParameterHandler)
               
            
            oGui.setEndOfDirectory()
        except: pass
        return
        
    def setFavorite(self):
        oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        #print oInputParameterHandler.getAllParameter()
        
        meta = {}
        meta['siteurl'] = oInputParameterHandler.getValue('siteUrl')
        meta['site'] = oInputParameterHandler.getValue('sId')
        meta['fav'] = oInputParameterHandler.getValue('sFav')
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        
        meta['title'] = xbmc.getInfoLabel('ListItem.title')
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] =  xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            cDb().insert_favorite(meta)
        except:
            pass
