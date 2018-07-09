#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, VSlog, xbmc

import urllib

import xbmcvfs


SITE_IDENTIFIER = 'cDb'
SITE_NAME = 'DB'


try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine') 
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine') 


class cDb:

    #os.path.join(self.__oCache,'vstream.db').decode("utf-8")
    DB = "special://userdata/addon_data/plugin.video.vstream/vstream.db"
    #important seul xbmcvfs peux lire le special
    REALDB = xbmc.translatePath(DB).decode("utf-8")
    DIALOG = dialog()

    def __init__(self):

        try:
            #if not os.path.exists(self.cache):
            if not xbmcvfs.exists(self.DB):
                self.db = sqlite.connect(self.REALDB)
                self.db.row_factory = sqlite.Row
                self.dbcur = self.db.cursor()
                self._create_tables()
        except:
            VSlog('erreur: Impossible d ecrire sur %s' % self.REALDB )
            pass

        try:
            self.db = sqlite.connect(self.REALDB)
            self.db.row_factory = sqlite.Row
            self.dbcur = self.db.cursor()
        except:
            VSlog('erreur: Impossible de ce connecter sur %s' % self.REALDB )
            pass

        
      

    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass

    def _create_tables(self):

        sql_create2 = "DROP TABLE history"
        
        ''' Create table '''
        sql_create = "CREATE TABLE IF NOT EXISTS history ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""disp TEXT, ""icone TEXT, ""isfolder TEXT, ""level TEXT, ""lastwatched TIMESTAMP "", ""UNIQUE(title)"");"
        self.dbcur.execute(sql_create)
        
        sql_create = "CREATE TABLE IF NOT EXISTS resume ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""hoster TEXT, ""point TEXT, ""UNIQUE(title, hoster)"");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS watched ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""site TEXT, ""UNIQUE(title, site)"");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS favorite ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""siteurl TEXT, ""site TEXT, ""fav TEXT, ""cat TEXT, ""icon TEXT, ""fanart TEXT, ""UNIQUE(title, site)"");"
        self.dbcur.execute(sql_create)         

        #sql_create = "DROP TABLE download"
        #self.dbcur.execute(sql_create)
        
        sql_create = "CREATE TABLE IF NOT EXISTS download ("" addon_id integer PRIMARY KEY AUTOINCREMENT, ""title TEXT, ""url TEXT, ""path TEXT, ""cat TEXT, ""icon TEXT, ""size TEXT,""totalsize TEXT, ""status TEXT, ""UNIQUE(title, path)"");"
        self.dbcur.execute(sql_create) 

        VSlog('Table initialized') 
    
    #Ne pas utiliser cette fonction pour les chemins
    def str_conv(self, data):
        if isinstance(data, str):
            # Must be encoded in UTF-8
            data = data.decode('utf8')
            
        import unicodedata
        data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        data = data.decode('string-escape') #ATTENTION : provoque des bugs pour les chemins a cause du caractere '/'
        
        return data
    
    def insert_history(self, meta):

        #title = urllib.unquote(meta['title']).decode('ascii', 'ignore')
        title = self.str_conv(urllib.unquote(meta['title']))
        disp = meta['disp']
        icon = 'icon.png'
        
        try:        
            ex = "INSERT INTO history (title, disp, icone) VALUES (?, ?, ?)"
            self.dbcur.execute(ex, (title,disp,icon))
            self.db.commit() 
            VSlog('SQL INSERT history Successfully')
        except Exception, e:
            if 'UNIQUE constraint failed' in e.message:
                ex = "UPDATE history set title = '%s', disp = '%s', icone= '%s' WHERE title = '%s'" % (title, disp, icon, title)
                self.dbcur.execute(ex)
                self.db.commit() 
                VSlog('SQL UPDATE history Successfully')
            VSlog('SQL ERROR INSERT') 
            pass
        self.db.close()

    def insert_resume(self, meta):
        title = self.str_conv(meta['title'])
        site = urllib.quote_plus(meta['site'])
        #hoster = meta['hoster']
        point = meta['point']
        ex = "DELETE FROM resume WHERE hoster = '%s'" % (site)
        self.dbcur.execute(ex)
        ex = "INSERT INTO resume (title, hoster, point) VALUES (?, ?, ?)"
        self.dbcur.execute(ex, (title,site,point))

        try:
            self.db.commit() 
            VSlog('SQL INSERT resume Successfully') 
        except Exception, e:
            #print ('************* Error attempting to insert into %s cache table: %s ' % (table, e))
            VSlog('SQL ERROR INSERT') 
            pass
        self.db.close()  

    def insert_watched(self, meta):

        title = self.str_conv(meta['title'])
        site = urllib.quote_plus(meta['site'])
        ex = "INSERT INTO watched (title, site) VALUES (?, ?)"
        self.dbcur.execute(ex, (title,site))
        try:
            self.db.commit() 
            VSlog('SQL INSERT watched Successfully') 
        except Exception, e:
            #print ('************* Error attempting to insert into %s cache table: %s ' % (table, e))
            VSlog('SQL ERROR INSERT') 
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
            VSlog('SQL ERROR EXECUTE') 
            return None
        self.dbcur.close()

    def get_resume(self, meta):
        title = self.str_conv(meta['title'])
        site = urllib.quote_plus(meta['site'])

        sql_select = "SELECT * FROM resume WHERE hoster = '%s'" % (site)

        try:    
            self.dbcur.execute(sql_select)
            #matchedrow = self.dbcur.fetchone()
            matchedrow = self.dbcur.fetchall()
            return matchedrow        
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return None
        self.dbcur.close()

    def get_watched(self, meta):        
        count = 0
        site = urllib.quote_plus(meta['site'])
        sql_select = "SELECT * FROM watched WHERE site = '%s'" % (site)

        try:    
            self.dbcur.execute(sql_select)
            #matchedrow = self.dbcur.fetchone()
            matchedrow = self.dbcur.fetchall()

            if matchedrow:
                count = 1
            else:
                count = 0    
            return count        
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return None
        self.dbcur.close()          

    def del_history(self):
    
        oInputParameterHandler = cInputParameterHandler()    
        if (oInputParameterHandler.exist('searchtext')):
            sql_delete = "DELETE FROM history WHERE title = '%s'" % (oInputParameterHandler.getValue('searchtext'))
        else:       
            sql_delete = "DELETE FROM history;"

        try:    
            self.dbcur.execute(sql_delete)
            self.db.commit()
            self.DIALOG.VSinfo('Historique supprime')
            xbmc.executebuiltin("Container.Refresh")
            return False, False       
        except Exception, e:
            VSlog('SQL ERROR DELETE') 
            return False, False
        self.dbcur.close()  
    
    
    def del_watched(self, meta):
        site = urllib.quote_plus(meta['site'])
        sql_select = "DELETE FROM watched WHERE site = '%s'" % (site)

        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close() 
        
    def del_resume(self, meta):
        site = urllib.quote_plus(meta['site'])

        sql_select = "DELETE FROM resume WHERE hoster = '%s'" % (site)

        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close()

        
        
    #***********************************
    #   Favoris fonctions
    #***********************************
    
    def insert_favorite(self, meta):

        title = self.str_conv(meta['title'])
        siteurl = urllib.quote_plus(meta['siteurl'])

        try: 
            sIcon = meta['icon'].decode('UTF-8') 
        except:
            sIcon = meta['icon']

        
        try:
            ex = "INSERT INTO favorite (title, siteurl, site, fav, cat, icon, fanart) VALUES (?, ?, ?, ?, ?, ?, ?)"
            self.dbcur.execute(ex, (title,siteurl, meta['site'],meta['fav'],meta['cat'],sIcon,meta['fanart']))
            
            self.db.commit() 
            
            self.DIALOG.VSinfo('Enregistré avec succés', meta['title'])
            VSlog('SQL INSERT favorite Successfully') 
        except Exception, e:
            if 'UNIQUE constraint failed' in e.message:
                self.DIALOG.VSinfo('Marque-page deja present', meta['title'])
            VSlog('SQL ERROR INSERT') 
            pass
        self.db.close()
        
    def get_favorite(self):
    
        sql_select = "SELECT * FROM favorite"

        try:    
            self.dbcur.execute(sql_select)
            #matchedrow = self.dbcur.fetchone()
            matchedrow = self.dbcur.fetchall()
            return matchedrow        
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return None
        self.dbcur.close()

    def del_favorite(self):
        
        oInputParameterHandler = cInputParameterHandler()
        
        if (oInputParameterHandler.exist('sCat')):
            sql_delete = "DELETE FROM favorite WHERE cat = '%s'" % (oInputParameterHandler.getValue('sCat'))
        
        if(oInputParameterHandler.exist('sMovieTitle')):
            
            siteUrl = oInputParameterHandler.getValue('siteUrl')
            sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
            siteUrl = urllib.quote_plus(siteUrl)
            title = self.str_conv(sMovieTitle)
            title = title.replace("'", r"''")       
            sql_delete = "DELETE FROM favorite WHERE siteurl = '%s' AND title = '%s'" % (siteUrl,title)
        
        if(oInputParameterHandler.exist('sAll')):      
            sql_delete = "DELETE FROM favorite;"

        try:    
            self.dbcur.execute(sql_delete)
            self.db.commit()
            self.DIALOG.VSinfo('Favoris supprimé')
            xbmc.executebuiltin("Container.Refresh")
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close() 

#non utiliser ?

    # def writeFavourites(self):

    #     oInputParameterHandler = cInputParameterHandler()
    #     sTitle = oInputParameterHandler.getValue('sTitle')
    #     sId = oInputParameterHandler.getValue('sId')
    #     sUrl = oInputParameterHandler.getValue('siteUrl')
    #     sFav = oInputParameterHandler.getValue('sFav')

    #     if (oInputParameterHandler.exist('sCat')):
    #         sCat = oInputParameterHandler.getValue('sCat')
    #     else:
    #         sCat = '5'

    #     sUrl = urllib.quote_plus(sUrl)
    #     fav_db = self.__sFile
    #     watched = {}
    #     if not os.path.exists(fav_db):
    #         file(fav_db, "w").write("%r" % watched) 
            
    #     if os.path.exists(fav_db):
    #         watched = eval(open(fav_db).read() )
    #         watched[sUrl] = watched.get(sUrl) or []
            
    #         #add to watched
    #         if not watched[sUrl]:
    #             #list = [sFav, sUrl];
    #             watched[sUrl].append(sFav)
    #             watched[sUrl].append(sId)
    #             watched[sUrl].append(sTitle)
    #             watched[sUrl].append(sCat)
    #         else:
    #             watched[sUrl][0] = sFav
    #             watched[sUrl][1] = sId
    #             watched[sUrl][2] = sTitle
    #             watched[sUrl][3] = sCat

    #     file(fav_db, "w").write("%r" % watched)
    #     cConfig().showInfo('Marque-Page', sTitle)
        #fav_db.close()
    
    #***********************************
    #   Download fonctions
    #***********************************
    
    def insert_download(self, meta):

        title = self.str_conv(meta['title'])
        url = urllib.quote_plus(meta['url'])        
        sIcon = urllib.quote_plus(meta['icon'])
        sPath = meta['path']

        ex = "INSERT INTO download (title, url, path, cat, icon, size, totalsize, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        self.dbcur.execute(ex, (title,url, sPath,meta['cat'],sIcon, '', '', 0))

        try:
            self.db.commit() 
            VSlog('SQL INSERT download Successfully') 
            self.DIALOG.VSinfo('Enregistré avec succés', meta['title'])
        except Exception, e:
            #print ('************* Error attempting to insert into %s cache table: %s ' % (table, e))
            VSlog('SQL ERROR INSERT') 
            pass
        self.db.close()
        
    def get_Download(self, meta = ''):
    
        if meta == '':
            sql_select = "SELECT * FROM download"
        else:
            url = urllib.quote_plus(meta['url'])
            sql_select = "SELECT * FROM download WHERE url = '%s' AND status = '0'" % (url)
            
        try:    
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            return matchedrow        
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return None
        self.dbcur.close()
        
    def clean_download(self):

        sql_select = "DELETE FROM download WHERE status = '2'"
        
        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close()
 
    def reset_download(self, meta):

        url = urllib.quote_plus(meta['url'])
        sql_select = "UPDATE download SET status = '0' WHERE status = '2' AND url = '%s'" % (url)
        
        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close()     
        
    def del_download(self, meta):

        if len(meta['url']) > 1:
            url = urllib.quote_plus(meta['url'])
            sql_select = "DELETE FROM download WHERE url = '%s'" % (url)
        elif len(meta['path']) > 1:
            path = meta['path']
            sql_select = "DELETE FROM download WHERE path = '%s'" % (path)
        else:
            return
        
        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close()
        
    def Cancel_download(self):
        sql_select = "UPDATE download SET status = '0' WHERE status = '1'"
        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close()   
        
    def update_download(self, meta):
    
        path = meta['path']
        size = meta['size']
        totalsize = meta['totalsize']
        status = meta['status']

        sql_select = "UPDATE download set size = '%s', totalsize = '%s', status= '%s' WHERE path = '%s'" % (size, totalsize, status, path)

        try:    
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception, e:
            VSlog('SQL ERROR EXECUTE') 
            return False, False
        self.dbcur.close()    
