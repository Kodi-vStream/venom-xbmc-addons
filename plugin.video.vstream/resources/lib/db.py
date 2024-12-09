# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import dialog, addon, VSlog, VSPath, isMatrix, VSProfil
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.util import QuotePlus, Unquote

SITE_IDENTIFIER = 'cDb'
SITE_NAME = 'DB'

try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite


class cDb(object):
    def __enter__(self):
        name = VSProfil()

        # Le cas par defaut.
        if name == 'Master user':
            DB = 'special://home/userdata/addon_data/plugin.video.vstream/vstream.db'
        else:
            DB = 'special://home/userdata/profiles/' + name + '/addon_data/plugin.video.vstream/vstream.db'

        try:
            REALDB = VSPath(DB).decode('utf-8')
        except AttributeError:
            REALDB = VSPath(DB)

        try:
            self.db = sqlite.connect(REALDB)
            self.db.row_factory = sqlite.Row
            self.dbcur = self.db.cursor()

            self.dbcur.execute("""
                SELECT name, sql FROM sqlite_master
                WHERE type='table'
                ORDER BY name;""")
            if self.dbcur.fetchone() is None:
                self._create_tables()
            return self

        except:
            VSlog('Error: Unable to access to %s' % REALDB)
            pass

    def __exit__(self, exc_type, exc_value, traceback):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.db.close()
        except:
            pass

    def _create_tables(self, dropTable=''):

        if dropTable != '':
            self.dbcur.execute("DROP TABLE IF EXISTS " + dropTable)
            self.db.commit()

        ''' Create table '''
        sql_create = "CREATE TABLE IF NOT EXISTS history ("\
                     "addon_id integer PRIMARY KEY AUTOINCREMENT, "\
                     "title TEXT, "\
                     "disp TEXT, "\
                     "icone TEXT, "\
                     "UNIQUE(title)"\
                     ");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS resume ("\
                     "addon_id integer PRIMARY KEY AUTOINCREMENT, "\
                     "title TEXT, "\
                     "hoster TEXT, "\
                     "point TEXT, "\
                     "total TEXT, "\
                     "UNIQUE(title, hoster)"\
                     ");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS watched ("\
                     "addon_id integer PRIMARY KEY AUTOINCREMENT, "\
                     "tmdb_id TEXT, "\
                     "title_id TEXT, "\
                     "title TEXT, "\
                     "siteurl TEXT, "\
                     "site TEXT, "\
                     "fav TEXT, "\
                     "cat TEXT, "\
                     "season integer, "\
                     "UNIQUE(title_id)"\
                     ");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS favorite ("\
                     "addon_id integer PRIMARY KEY AUTOINCREMENT, "\
                     "title TEXT, "\
                     "siteurl TEXT, "\
                     "site TEXT, "\
                     "fav TEXT, "\
                     "cat TEXT, "\
                     "icon TEXT, "\
                     "fanart TEXT, "\
                     "UNIQUE(title, site)"\
                     ");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS viewing ("\
                     "addon_id integer PRIMARY KEY AUTOINCREMENT, "\
                     "tmdb_id TEXT, "\
                     "title_id TEXT, "\
                     "title TEXT, "\
                     "siteurl TEXT, "\
                     "site TEXT, "\
                     "fav TEXT, "\
                     "cat TEXT, "\
                     "season integer, "\
                     "UNIQUE (title_id)"\
                     ");"
        self.dbcur.execute(sql_create)

        sql_create = "CREATE TABLE IF NOT EXISTS download ("\
                     "addon_id integer PRIMARY KEY AUTOINCREMENT, "\
                     "title TEXT, "\
                     "url TEXT, "\
                     "path TEXT, "\
                     "cat TEXT, "\
                     "icon TEXT, "\
                     "size TEXT,"\
                     "totalsize TEXT, "\
                     "status TEXT, "\
                     "UNIQUE(title, path)"\
                     ");"
        self.dbcur.execute(sql_create)

        VSlog('Table initialized')

    # Ne pas utiliser cette fonction pour les chemins
    def str_conv(self, data):
        if not isMatrix():
            if isinstance(data, str):
                # Must be encoded in UTF-8
                try:
                    data = data.decode('utf8')
                except AttributeError:
                    pass
            import unicodedata
            data = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')

            try:
                data = data.decode('string-escape')  # ATTENTION: bugs pour les chemins a cause du caractere '/'
            except:
                pass

        else:
            data = data.encode().decode()

        return data.strip()

    # ***********************************
    #   History fonctions
    # ***********************************

    def insert_history(self, meta):

        # title = Unquote(meta['title']).decode('ascii', 'ignore')
        title = self.str_conv(Unquote(meta['title']))
        disp = meta['disp']
        icon = 'icon.png'

        # on ne garde l'historique que pour les films, séries, animes, doc, drama
        if disp not in ('1', '2', '3', '5', '9'):
            return
        
        try:
            ex = 'INSERT INTO history (title, disp, icone) VALUES (?, ?, ?)'
            self.dbcur.execute(ex, (title, disp, icon))
            self.db.commit()
            VSlog('SQL INSERT history Successfully')
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                ex = "UPDATE history set title = '%s', disp = '%s', icone= '%s' WHERE title = '%s'" % (title, disp, icon, title)
                self.dbcur.execute(ex)
                self.db.commit()
                VSlog('SQL UPDATE history Successfully')
            else:
                VSlog('SQL ERROR INSERT, title = %s, %s' % (title, e))
            pass

    def get_history(self, cat = None):
        if cat:
            sql_select = 'SELECT * FROM history where disp = %s ORDER BY addon_id DESC' % cat
        else:
            sql_select = 'SELECT * FROM history ORDER BY addon_id DESC'

        try:
            self.dbcur.execute(sql_select)
            # matchedrow = self.dbcur.fetchone()
            matchedrow = self.dbcur.fetchall()
            return matchedrow
        except Exception as e:
            VSlog('SQL ERROR EXECUTE, %s' % e)
            return None

    def del_history(self):
        from resources.lib.gui.gui import cGui
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        if oInputParameterHandler.exist('searchtext'):
            sql_delete = "DELETE FROM history WHERE title = '%s'" % (oInputParameterHandler.getValue('searchtext'))
        else:
            sql_delete = 'DELETE FROM history;'

        try:
            self.dbcur.execute(sql_delete)
            self.db.commit()
            dialog().VSinfo(addon().VSlang(30041))
            oGui.updateDirectory()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR DELETE : %s' % sql_delete)
            return False, False

    # ***********************************
    #   Watched fonctions
    # ***********************************

    def insert_watched(self, meta):
        title = meta['title']
        if not title:
            return

        titleWatched = meta['titleWatched'].replace(' ', '')
        cat = meta['cat'] if 'cat' in meta else '1'
        siteurl = QuotePlus(meta['siteurl'])
        tmdbId = meta['tmdbId'] if 'tmdbId' in meta else ''
        site = meta['site']
        fav = meta['fav']
        season = meta['season'] if 'season' in meta else ''

        # on enleve avant de remettre pour retrier
        ex = "DELETE FROM watched WHERE title_id = '%s' and cat = '%s'" % (titleWatched, cat)
        try:
            self.dbcur.execute(ex)
        except Exception as e:
            VSlog('SQL ERROR - ' + ex)
            pass

        ex = 'INSERT or IGNORE INTO watched (tmdb_id, title_id, title, siteurl, site, cat, fav, season) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        try:
            self.dbcur.execute(ex, (tmdbId, titleWatched, title, siteurl, site, cat, fav, season))
            self.db.commit()
            VSlog('SQL INSERT watched Successfully')
        except Exception as e:
            if 'no such column' in str(e) or 'no column named' in str(e) or 'no such table' in str(e):
                if 'named cat' in str(e):  # ajout nouvelle colonne 'cat'
                    self.dbcur.execute("ALTER TABLE watched add column cat TEXT")
                    self.db.commit()
                    VSlog('Table recreated : watched')

                if 'named tmdb_id' in str(e):  # ajout nouvelle colonne 'tmdb_id'
                    self.dbcur.execute("ALTER TABLE watched add column tmdb_id TEXT")
                    self.db.commit()
                    VSlog('Table recreated : watched')

                if 'named season' in str(e):  # ajout nouvelle colonne 'season'
                    self.dbcur.execute("ALTER TABLE watched add column season integer")
                    self.db.commit()
                    VSlog('Table recreated : watched')

                # Deuxieme tentative
                self.dbcur.execute(ex, (tmdbId, titleWatched, title, siteurl, site, cat, fav, season))
                self.db.commit()
            else:
                VSlog('SQL ERROR INSERT watched : title = %s' % e)

        # Lecture d'une episode, on retient aussi la saison
        if cat == "8":
            meta['cat'] = 4
            meta['fav'] = meta['seasonFunc']
            meta['siteurl'] = meta['seasonUrl']
            tvshowtitle = title[:title.rindex('E')].strip()
            meta['title'] = tvshowtitle
            titleWatched = titleWatched[:titleWatched.rindex('E')].strip()
            meta['titleWatched'] = titleWatched
            self.insert_watched(meta)

    def get_watched(self, meta):
        title = meta['titleWatched']
        if not title:
            return False
        title = title.replace(' ', '')
        cat = meta['cat'] if 'cat' in meta else '1'

        sql_select = "SELECT * FROM watched WHERE title_id = '%s'" % title

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()

            # Gestion des homonymes films / séries
            # Si la cat est enregistrée, on vérifie si c'est la même
            for data in matchedrow:
                matchedcat = data['cat']
                if matchedcat:
                    return int(matchedcat) == int(cat)

            return True if matchedrow else False
        except Exception as e:
            if 'no such column' in str(e) or 'no column named' in str(e) or 'no such table' in str(e):
                self.convertWatched()    # MAJ du modele de table
                # Deuxieme tentative
                try:
                    self.dbcur.execute(sql_select)
                    matchedrow = self.dbcur.fetchall()
                    return True if matchedrow else False
                except Exception as e:
                    VSlog('SQL ERROR %s' % sql_select)
            return False

    def get_catWatched(self, cat):
        
        sql_select = "SELECT tmdb_id, * FROM watched"

        if cat:
            sql_select += " where cat = '%s'" % cat

        sql_select += " order by addon_id DESC"

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            return matchedrow

        except Exception as e:
            if 'no such column' in str(e) or 'no column named' in str(e) or 'no such table' in str(e):
                self.convertWatched()    # MAJ du modele de table
                try:    # 2eme tentative
                    self.dbcur.execute(sql_select)
                    matchedrow = self.dbcur.fetchall()
                    return matchedrow
                except Exception as e:
                    pass
            VSlog('SQL ERROR : %s' % sql_select)
        return None
        

    def del_watched(self, meta):
        title = meta['titleWatched']
        if not title:
            return

        tmdbId = meta['tmdbId'] if 'tmdbId' in meta else ''
        if tmdbId:
            sql_select = "DELETE FROM watched WHERE tmdb_id = '%s'" % tmdbId
        else:
            sql_select = "DELETE FROM watched WHERE title_id = '%s'" % title
        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
        return False, False


    # conversion de l'ancienne table watched
    def convertWatched(self):
        try:
            self.dbcur.execute("ALTER TABLE watched RENAME COLUMN title TO title_id")
        except Exception as e:
            pass
        try:
            self.dbcur.execute("ALTER TABLE watched add title TEXT")
        except Exception as e:
            pass
        try:
            self.dbcur.execute("ALTER TABLE watched add tmdb_id TEXT")
        except Exception as e:
            pass
        try:
            self.dbcur.execute("ALTER TABLE watched add siteurl TEXT")
        except Exception as e:
            pass
        try:
            self.dbcur.execute("ALTER TABLE watched add site TEXT")
        except Exception as e:
            pass
        try:
            self.dbcur.execute("ALTER TABLE watched add fav TEXT")
        except Exception as e:
            pass
        try:
            self.dbcur.execute("ALTER TABLE watched add season integer")
        except Exception as e:
            pass
        
        return
    

    # ***********************************
    #   Resume fonctions
    # ***********************************

    def insert_resume(self, meta):
        title = self.str_conv(meta['titleWatched']).replace(' ', '')
        site = QuotePlus(meta['site'])
        point = meta['point']
        total = meta['total']
        ex = "DELETE FROM resume WHERE title = '%s'" % title
        try:
            self.dbcur.execute(ex)
        except Exception as e:
            VSlog('SQL ERROR - ' + ex)
            pass

        try:
            ex = 'INSERT INTO resume (title, hoster, point, total) VALUES (?, ?, ?, ?)'
            self.dbcur.execute(ex, (title, site, point, total))
            self.db.commit()
        except Exception as e:
            if 'no such column' in str(e) or 'no column named' in str(e) or 'no such table' in str(e):
                self._create_tables('resume')
                VSlog('Table recreated : resume')

                # Deuxieme tentative
                self.dbcur.execute(ex, (title, site, point, total))
                self.db.commit()
            else:
                VSlog('SQL ERROR INSERT : %s' % e)

    def get_resume(self, meta):
        title = self.str_conv(meta['titleWatched'])
        # site = QuotePlus(meta['site'])

        sql_select = "SELECT point, total FROM resume WHERE title = '%s'" % title

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
            # matchedrow = self.dbcur.fetchall()
            if not matchedrow:
                return False, False
            return float(matchedrow[0]), float(matchedrow[1])

        except Exception as e:
            if 'no such column' in str(e) or 'no column named' in str(e):
                self._create_tables('resume')
                VSlog('Table recreated : resume')
            else:
                VSlog('SQL ERROR : %s' % e)
        return False, False

    def del_resume(self, meta):
        title = QuotePlus(meta['titleWatched'])

        sql_select = "DELETE FROM resume WHERE title = '%s'" % title

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return False, False

    #  ***********************************
    #  Bookmark fonctions
    #  ***********************************

    def insert_bookmark(self, meta):

        title = self.str_conv(meta['title'])
        siteurl = QuotePlus(meta['siteurl'])

        try:
            sIcon = meta['icon'].decode('UTF-8')
        except:
            sIcon = meta['icon']

        try:
            ex = 'INSERT INTO favorite (title, siteurl, site, fav, cat, icon, fanart) VALUES (?, ?, ?, ?, ?, ?, ?)'
            self.dbcur.execute(ex, (title, siteurl, meta['site'], meta['fav'], meta['cat'], sIcon, meta['fanart']))

            self.db.commit()

            dialog().VSinfo(addon().VSlang(30042), meta['title'], 4)
            VSlog('SQL INSERT favorite Successfully - ' + meta['title'])
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                dialog().VSinfo(addon().VSlang(30043), meta['title'])
            VSlog('SQL ERROR INSERT : %s' % e)
            pass

    def get_bookmark(self):

        sql_select = 'SELECT * FROM favorite order by addon_id desc'

        try:
            self.dbcur.execute(sql_select)
            # matchedrow = self.dbcur.fetchone()
            matchedrow = self.dbcur.fetchall()
            return matchedrow
        except Exception as e:
            VSlog('SQL ERROR EXECUTE')
            return None

    def del_bookmark(self, sSiteUrl='', sMovieTitle='', sCat='', sAll=False):

        sql_delete = None

        # Tous supprimer
        if sAll:
            sql_delete = 'DELETE FROM favorite;'

        # Supprimer un bookmark selon son titre
        elif sMovieTitle:
            siteUrl = QuotePlus(sSiteUrl)
            title = self.str_conv(sMovieTitle)
            title = title.replace("'", r"''")
            sql_delete = "DELETE FROM favorite WHERE siteurl = '%s' AND title = '%s'" % (siteUrl, title)

        # Supprimer un bookmark selon son url
        elif sSiteUrl:
            siteUrl = QuotePlus(sSiteUrl)
            sql_delete = "DELETE FROM favorite WHERE siteurl = '%s'" % siteUrl

        # Supprimer toute une catégorie
        elif sCat:
            catList = ('1', '7')    # films, saga
            if sCat not in catList:
                catList = ('2', '3', '4', '8')
                if sCat not in catList:
                    catList = ('0', sCat)
            sql_delete = "DELETE FROM favorite WHERE cat in %s" % str(catList)

        if sql_delete:
            from resources.lib.gui.gui import cGui
            try:
                self.dbcur.execute(sql_delete)
                self.db.commit()
                update = self.db.total_changes

                if not update and sSiteUrl and sMovieTitle:
                    # si pas trouvé, on essaie sans le titre, seulement l'URL
                    return self.del_bookmark(sSiteUrl)

                dialog().VSinfo(addon().VSlang(30044))
                cGui().updateDirectory()
                return True
            except Exception as e:
                VSlog('SQL ERROR %s' % sql_delete)
        return False

    # ***********************************
    #   InProgress fonctions
    # ***********************************

    def insert_viewing(self, meta):

        if 'title' not in meta:
            return
        if 'siteurl' not in meta:
            return

        title = self.str_conv(meta['title'])
        titleWatched = self.str_conv(meta['titleWatched']).replace(' ', '')
        siteurl = QuotePlus(meta['siteurl'])
        cat = meta['cat']
        saison = meta['season'] if 'season' in meta else ''
        sTmdbId = meta['tmdbId'] if 'tmdbId' in meta else ''

        # on enleve avant de remettre pour retrier
        ex = "DELETE FROM viewing WHERE title_id = '%s' and cat = '%s'" % (titleWatched, cat)
        try:
            self.dbcur.execute(ex)
        except Exception as e:
            VSlog('SQL ERROR - ' + ex)
            pass

        try:
            ex = 'INSERT INTO viewing (tmdb_id, title_id, title, siteurl, site, fav, cat, season) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            self.dbcur.execute(ex, (sTmdbId, titleWatched, title, siteurl, meta['site'], meta['fav'], cat, saison))
            self.db.commit()
            VSlog('SQL INSERT viewing Successfully')
        except Exception as e:
            if 'no such column' in str(e) or 'no column named' in str(e) or 'no such table' in str(e):
                self._create_tables('viewing')
                VSlog('Table recreated : viewing')

                # Deuxieme tentative
                self.dbcur.execute(ex, (sTmdbId, titleWatched, title, siteurl, meta['site'], meta['fav'], cat, saison))
                self.db.commit()
            else:
                VSlog('SQL ERROR INSERT : %s' % e)
            pass

    def get_viewing(self):
        sql_select = "SELECT * FROM viewing group by title order by addon_id DESC"

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            return matchedrow

        except Exception as e:
            VSlog('SQL ERROR : %s' % sql_select)
            return None

    def del_viewing(self, meta):
        sTitleWatched = meta['titleWatched'] if 'titleWatched' in meta else None

        if not sTitleWatched:       # delete a category or all
            sql_delete = "DELETE FROM viewing"
            if 'cat' in meta:
                sql_delete += " where cat = '%s'" % meta['cat']
        else:
            sql_delete= "DELETE FROM viewing WHERE title_id = '%s'" % sTitleWatched
            if 'cat' in meta:
                sql_delete += " and cat = '%s'" % meta['cat']

        update = 0
        try:
            self.dbcur.execute(sql_delete)
            self.db.commit()
            update = self.db.total_changes

            # si pas trouvé, on essaie sans la cat, juste le titre
            if not update and sTitleWatched and 'cat' in meta:
                del meta['cat']
                return self.del_viewing(meta)

            return True
        except Exception as e:
            VSlog('SQL ERROR %s, error = %s' % (sql_delete, e))

        return update

    #  ***********************************
    #  Download fonctions
    #  ***********************************

    def insert_download(self, meta):

        title = self.str_conv(meta['title'])
        url = QuotePlus(meta['url'])
        sIcon = QuotePlus(meta['icon'])
        sPath = meta['path']
        ex = 'INSERT INTO download (title, url, path, cat, icon, size, totalsize, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

        try:
            self.dbcur.execute(ex, (title, url, sPath, meta['cat'], sIcon, '', '', 0))
            self.db.commit()
            VSlog('SQL INSERT download Successfully')
        except Exception as e:
            VSlog('SQL ERROR INSERT into download')
            pass

    def get_download(self, meta=''):

        if meta == '':
            sql_select = 'SELECT * FROM download'
        else:
            url = QuotePlus(meta['url'])
            sql_select = "SELECT * FROM download WHERE url = '%s' AND status = '0'" % url

        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchall()
            return matchedrow
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return None

    def clean_download(self):

        sql_select = "DELETE FROM download WHERE status = '2'"

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return False, False

    def reset_download(self, meta):

        url = QuotePlus(meta['url'])
        sql_select = "UPDATE download SET status = '0' WHERE status = '2' AND url = '%s'" % url

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return False, False

    def del_download(self, meta):

        if len(meta['url']) > 1:
            url = QuotePlus(meta['url'])
            sql_select = "DELETE FROM download WHERE url = '%s'" % url
        elif len(meta['path']) > 1:
            path = meta['path']
            sql_select = "DELETE FROM download WHERE path = '%s'" % path
        else:
            return

        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return False, False

    def cancel_download(self):
        sql_select = "UPDATE download SET status = '0' WHERE status = '1'"
        try:
            self.dbcur.execute(sql_select)
            self.db.commit()
            return False, False
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return False, False

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
        except Exception as e:
            VSlog('SQL ERROR %s' % sql_select)
            return False, False
