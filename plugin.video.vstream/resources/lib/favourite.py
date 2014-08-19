#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
import os
import urllib

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'

class cFav:

    def __init__(self):
        self.__sFile = cConfig().getFileFav()
        self.__sTitle = ''
        #self.__sFunctionName = ''
      

    def delFavourites(self):
    
        oInputParameterHandler = cInputParameterHandler()
        #sTitle = oInputParameterHandler.getValue('sTitle')
        sId = oInputParameterHandler.getValue('sId')
        sUrl = oInputParameterHandler.getValue('siteUrl')
        #sFav = oInputParameterHandler.getValue('sFav')
        
        sUrl = urllib.quote_plus(sUrl)
        #print vars(oInputParameterHandler)
        
        fav_db = self.__sFile
        
        if os.path.exists(fav_db):
            watched = eval(open(fav_db).read() )
            watched[sUrl] = watched.get(sUrl) or []
            del watched[sUrl]
        file(fav_db, "w").write("%r" % watched)
        cConfig().showInfo('Supprimer', sId)
        cConfig().update()
        return
    
   
        
    def getFavourites(self):
        oGui = cGui()
        fav_db = self.__sFile

        if os.path.exists(fav_db): 
            watched = eval( open(fav_db).read() )

            items = []
            item = []
            for result in watched:

                sUrl = result
                sFunction =  watched[result][0]
                sId = watched[result][1]
                sTitle = sId+' - '+urllib.unquote_plus(sUrl)
                items.append([sId, sFunction, sUrl])
                item.append(result)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sFav', 'setdel')
                
                oGui.addFav(sId, sFunction, sTitle, 'mark.png', sUrl, oOutputParameterHandler)
               
            
            oGui.setEndOfDirectory()
        else: return
        return items


    def writeFavourites(self):

        oInputParameterHandler = cInputParameterHandler()
        sTitle = oInputParameterHandler.getValue('sTitle')
        sId = oInputParameterHandler.getValue('sId')
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sFav = oInputParameterHandler.getValue('sFav')

        sUrl = urllib.quote_plus(sUrl)
        fav_db = self.__sFile
        watched = {}
        if not os.path.exists(fav_db):
            file(fav_db, "w").write("%r" % watched) 
            
        if os.path.exists(fav_db):
            watched = eval(open(fav_db).read() )
            watched[sUrl] = watched.get(sUrl) or []
            
            #add to watched
            if not watched[sUrl]:
                #list = [sFav, sUrl];
                watched[sUrl].append(sFav)
                watched[sUrl].append(sId)
            else:
                watched[sUrl][0] = sFav
                watched[sUrl][1] = sId

        file(fav_db, "w").write("%r" % watched)
        cConfig().showInfo('Marque-Page', sId)
        #fav_db.close()