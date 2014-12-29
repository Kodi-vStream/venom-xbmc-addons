#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
import os, sys
import urllib
import xbmc
from addon.common.addon import Addon

addon = Addon('plugin.video.vstream')


SITE_IDENTIFIER = 'cDb'
SITE_NAME = 'DB'


try:
    from sqlite3 import dbapi2 as sqlite
    cConfig().log('SQLITE 3 as DB engine') 
except:
    from pysqlite2 import dbapi2 as sqlite
    cConfig().log('SQLITE 2 as DB engine') 


class cDb:

    def __init__(self):

        DB = os.path.join(cConfig().getSettingCache(), 'vstream.db')

        try:
            self.db = sqlite.connect(DB)
            self.dbcur = self.db.cursor()

            self._create_tables()
        except:
            return False
        
      

    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass

    def _create_tables(self):

        sql_create2 = "DROP TABLE history"
        
        ''' Create table '''
        sql_create = "CREATE TABLE IF NOT EXISTS history ("\
                            "addon_id integer PRIMARY KEY AUTOINCREMENT,"\
                            "title TEXT,"\
                            "disp TEXT,"\
                            "icone TEXT,"\
                            "isfolder TEXT,"\
                            "level TEXT,"\
                            "lastwatched TIMESTAMP"\
                            ");"

        self.dbcur.execute(sql_create)     

        
        cConfig().log('Table watch_history initialized') 
    
    def str_conv(self, data):
        if isinstance(data, str):
            # Must be encoded in UTF-8
            data = data.decode('utf8')
        
        import unicodedata
        data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        
        data = data.decode('string-escape')
        
        return data
    
    def insert_history(self, meta):

        #title = urllib.unquote(meta['title']).decode('ascii', 'ignore')
        title = self.str_conv(urllib.unquote(meta['title']))
        disp = meta['disp']
        icon = 'icon.png'
        ex = "INSERT INTO history (title, disp, icone) VALUES (?, ?, ?)"
        self.dbcur.execute(ex, (title,disp,icon))

        try:
            self.db.commit() 
            cConfig().log('SQL INSERT Successfully') 
        except Exception, e:
            #print ('************* Error attempting to insert into %s cache table: %s ' % (table, e))
            cConfig().log('SQL ERROR INSERT') 
            pass
        self.db.close() 


    def get_history(self):
    
        sql_select = "SELECT * FROM history"

        try:    
            self.dbcur.execute(sql_select)
            #matchedrow = self.dbcur.fetchone()
            matchedrow = self.dbcur.fetchall()
            return matchedrow        
        except Exception, e:
            cConfig().log('SQL ERROR EXECUTE') 
            return None
        self.dbcur.close()   

    def del_history(self):

        sql_delete = "DELETE FROM history;"

        try:    
            self.dbcur.execute(sql_delete)
            self.db.commit()
            cConfig().showInfo('vStream', 'Historique supprimer')
            cConfig().update()
            return False, False       
        except Exception, e:
            cConfig().log('SQL ERROR DELETE') 
            return False, False
        self.dbcur.close()  

    
   
     
    def getFavourites(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Films', 'search.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Séries', 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Pages', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '4')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Lires', 'views.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'getFav', 'Divers', 'views.png', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()

    def getFav(self):
        oGui = cGui()
        fav_db = self.__sFile

        oInputParameterHandler = cInputParameterHandler()
        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
        else:
            sCat = '5'

        if os.path.exists(fav_db): 
            watched = eval( open(fav_db).read() )

            items = []
            item = []
            for result in watched:

                sUrl = result
                sFunction =  watched[result][0]
                sId = watched[result][1]
                try:
                    sTitle = watched[result][2]
                except:
                    sTitle = sId+' - '+urllib.unquote_plus(sUrl)

                try:
                    sCategorie = watched[result][3]
                except:
                    sCategorie = '5'

                items.append([sId, sFunction, sUrl])
                item.append(result)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', 'False')
                
                if (sFunction == 'play'):
                    oHoster = cHosterGui().checkHoster(sUrl)
                    oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
                    oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
                    oOutputParameterHandler.addParameter('sMediaUrl', sUrl)

                if (sCategorie == sCat):
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

        if (oInputParameterHandler.exist('sCat')):
            sCat = oInputParameterHandler.getValue('sCat')
        else:
            sCat = '5'

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
                watched[sUrl].append(sTitle)
                watched[sUrl].append(sCat)
            else:
                watched[sUrl][0] = sFav
                watched[sUrl][1] = sId
                watched[sUrl][2] = sTitle
                watched[sUrl][3] = sCat

        file(fav_db, "w").write("%r" % watched)
        cConfig().showInfo('Marque-Page', sTitle)
        #fav_db.close()