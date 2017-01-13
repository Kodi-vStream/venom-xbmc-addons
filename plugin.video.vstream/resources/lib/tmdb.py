# -*- coding: utf-8 -*-
#Code de depart par AnthonyBloomer
#Modif pour vStream

from resources.lib.config import cConfig

import json, os
import pprint
from urllib import quote_plus, urlopen, urlencode
import xbmc

try:
    from sqlite3 import dbapi2 as sqlite
    cConfig().log('SQLITE 3 as DB engine') 
except:
    from pysqlite2 import dbapi2 as sqlite
    cConfig().log('SQLITE 2 as DB engine') 


class obj:
    def __init__(self, **entries):
        self.__dict__.update(entries)


# http://docs.themoviedb.apiary.io
class cTMDb:
    URL = "http://api.themoviedb.org/3/"

    def __init__(self, api_key, debug=False, lang='en'):
        self.api_key = api_key
        self.debug = debug
        self.lang = lang
        self.poster = 'https://image.tmdb.org/t/p/w396'
        self.fanart = 'https://image.tmdb.org/t/p/w1280'
        self.cache = os.path.join(cConfig().getSettingCache(),'video_cache.db')
        
        try:
            if not os.path.exists(self.cache):
                f = open(self.cache,'w')
                f.close()
                self.db = sqlite.connect(self.cache)
                self.dbcur = self.db.cursor()
                self.__createdb()
        except:
            pass
            
        try:
            self.db = sqlite.connect(self.cache)
            self.dbcur = self.db.cursor()
        except:
            pass

    def __createdb(self):

        sql_create = "CREATE TABLE IF NOT EXISTS movie ("\
                           "imdb_id TEXT, "\
                           "tmdb_id TEXT, "\
                           "title TEXT, "\
                           "year INTEGER,"\
                           "director TEXT, "\
                           "writer TEXT, "\
                           "tagline TEXT, "\
                           "cast TEXT,"\
                           "rating FLOAT, "\
                           "votes TEXT, "\
                           "duration TEXT, "\
                           "plot TEXT,"\
                           "mpaa TEXT, "\
                           "premiered TEXT, "\
                           "genre TEXT, "\
                           "studio TEXT,"\
                           "thumb_url TEXT, "\
                           "cover_url TEXT, "\
                           "trailer TEXT, "\
                           "backdrop_url TEXT,"\
                           "imgs_prepacked TEXT,"\
                           "playcount INTEGER,"\
                           "UNIQUE(imdb_id, tmdb_id, title, year)"\
                           ");"
        try:
            self.dbcur.execute(sql_create)
        except:
            xbmc.log("non")
       
        sql_create = "CREATE TABLE IF NOT EXISTS tvshow ("\
                           "imdb_id VARCHAR(10), "\
                           "tvdb_id VARCHAR(10), "\
                           "title TEXT, "\
                           "year INTEGER,"\
                           "cast TEXT,"\
                           "rating FLOAT, "\
                           "duration TEXT, "\
                           "plot TEXT,"\
                           "mpaa TEXT, "\
                           "premiered TEXT, "\
                           "genre TEXT, "\
                           "studio TEXT,"\
                           "status TEXT,"\
                           "banner_url TEXT, "\
                           "cover_url TEXT,"\
                           "trailer TEXT, "\
                           "backdrop_url TEXT,"\
                           "imgs_prepacked TEXT,"\
                           "playcount INTEGER,"\
                           "UNIQUE(imdb_id, tvdb_id, title)"\
                           ");"
                           
        self.dbcur.execute(sql_create)
       
        sql_create = "CREATE TABLE IF NOT EXISTS season ("\
                           "imdb_id VARCHAR(10), "\
                           "tvdb_id VARCHAR(10), " \
                           "season INTEGER, "\
                           "cover_url TEXT,"\
                           "playcount INTEGER,"\
                           "UNIQUE(imdb_id, tvdb_id, season)"\
                           ");"
                           
        self.dbcur.execute(sql_create)
        
        sql_create = "CREATE TABLE IF NOT EXISTS episode ("\
                           "imdb_id VARCHAR(10), "\
                           "tvdb_id VARCHAR(10), "\
                           "episode_id VARCHAR(10), "\
                           "season INTEGER, "\
                           "episode INTEGER, "\
                           "title TEXT, "\
                           "director TEXT, "\
                           "writer TEXT, "\
                           "plot TEXT, "\
                           "rating FLOAT, "\
                           "premiered TEXT, "\
                           "poster TEXT, "\
                           "playcount INTEGER, "\
                           "UNIQUE(imdb_id, tvdb_id, episode_id, title)"\
                           ");"
                           
        self.dbcur.execute(sql_create)
        xbmc.log("table creer")
        
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass

    # Get the basic movie information for a specific movie id.
    def search_movie_id(self, movie_id, append_to_response="append_to_response=trailers,images,casts,translations"):
        result = self._call('movie/'+ str(movie_id), append_to_response)
        return result #obj(**self._call('movie/' + str(movie_id), append_to_response))

    # Get the user reviews for a movie
    def get_movie_reviews(self, id, page=1):
        arr = []
        result = self._call('movie/%s/reviews' % id, 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    def get_movie_lists(self, id, page=1):
        arr = []
        result = self._call('movie/%s/lists' % id, 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    def get_movie_videos(self, id, page=1):
        arr = []
        result = self._call('movie/%s/videos' % id, 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    def get_movie_recommendations(self, movie_id, page=1):
        arr = []
        result = self._call('movie/%s/recommendations' % movie_id, 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    def discover_movies(self, params):
        arr = []
        result = self._call('discover/movie/', urlencode(params))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    def discover_tv_shows(self, params):
        arr = []
        result = self._call('discover/tv/', urlencode(params))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the latest movie id.
    def get_latest_movie(self):
        return obj(**self._call('movie/latest', ''))

    # Get the list of movies playing that have been, or are being released this week. This list refreshes every day.
    def now_playing(self, page=1):
        arr = []
        result = self._call('movie/now_playing', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the list of top rated movies. By default, this list will only include movies that have 50 or more votes.
    # This list refreshes every day.
    def top_rated(self, page=1):
        arr = []
        result = self._call('movie/top_rated', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the list of upcoming movies by release date. This list refreshes every day.
    def upcoming(self, page=1):
        arr = []
        result = self._call('movie/upcoming', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the list of popular movies on The Movie Database. This list refreshes every day.
    def popular(self, page=1):
        arr = []
        result = self._call('movie/popular', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Search for movies by title.
    def search_movie_name(self, name, year='', page=1):
    
        meta = {}
        
        if year:
            term = name + '&year=' + year
        else:
            term = name
            
        meta = self._call('search/movie', 'query=' + quote_plus(term) + '&page=' + str(page))
        #teste sans l'année
        if meta and meta['total_results'] == 0 and year:
                meta = self._search(name,'') 
        #cherche 1 seul resultat
        if meta and meta['total_results'] != 0 and meta['results']:
            tmdb_id = meta['results'][0]['id']            
            #cherche toutes les infos
            meta = self.search_movie_id(tmdb_id)
        else:
            meta = {}

        return meta
        
            # Search for TV shows by title.
    def search_tvshow_name(self, term, page=1):
        arr = []
        result = self._call('search/tv', 'query=' + quote_plus(term) + '&page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the similar movies for a specific movie id.
    def similar(self, id, page=1):
        arr = []
        result = self._call('movie/' + str(id) + '/similar', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the primary information about a TV series by id.
    def search_tvshow_id(self, show_id, append_to_response="append_to_response=trailers,images,casts,translations"):
        return obj(**self._call('tv/' + str(show_id), append_to_response))

    # Get the latest TV show id.
    def get_latest_tv_show(self):
        return obj(**self._call('tv/latest', ''))

    # Get the similar TV shows for a specific tv id.
    def similar_shows(self, id, page=1):
        arr = []
        result = self._call('tv/' + str(id) + '/similar', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the list of popular TV shows. This list refreshes every day.
    def popular_shows(self, page=1):
        arr = []
        result = self._call('tv/popular', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the list of top rated TV shows.
    # By default, this list will only include TV shows that have 2 or more votes.
    # This list refreshes every day.

    def top_rated_shows(self, page=1):
        arr = []
        result = self._call('tv/top_rated', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the general person information for a specific id.
    def get_person(self, id):
        return obj(**self._call('person/' + str(id), ''))

    # Search for people by name.
    def search_person(self, term, page=1):
        arr = []
        result = self._call('search/person', 'query=' + quote_plus(term) + '&page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr
      
    def __set_playcount(self, overlay):
        if int(overlay) == 7:
            return 1
        else:
            return 0
            
    def _format(self, meta):
        _meta = {}

        _meta['title'] = meta['title']
        _meta['tmdb_id'] = meta['id']
        if 'imdb_id' in meta:
            _meta['imdb_id'] = meta['imdb_id']
        if 'runtime' in meta:
            if meta['runtime'] > 0:
                _meta['duration'] = int(meta['runtime']) *60
            else: 
                 _meta['duration'] = 0
        _meta['plot'] = meta['overview']
        if 'certification' in meta:
            _meta['mpaa'] = meta['certification']
        if 'release_date' in meta:
            _meta['year'] = int(meta['release_date'][:4])
        # if not 'year' in meta and 'premiered' in _meta:
            # _meta['year'] = _meta['premiered']
        
        if 'genres' in meta:
            _meta['genre'] = ""
            for genre in meta['genres']:
                if _meta['genre'] == "":
                     _meta['genre'] += genre['name']
                else:
                    _meta['genre'] += '/'+genre['name']
            
        if 'backdrop_path' in meta:
            _meta['backdrop_url'] = self.fanart+str(meta['backdrop_path'])
        if 'poster_path' in meta:
            _meta['cover_url'] = self.poster+str(meta['poster_path'])
        
        if not 'playcount' in meta:
            _meta['playcount'] = self.__set_playcount(6)
            
        #ont prend juste le premier
        try:
            _meta['trailer'] = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % meta['trailers']['youtube'][0]['source']
        except:
            _meta['trailer'] = ''
            
    
        return _meta
        
    def _cache_search(self, media_type, name, tmdb_id='', year=''):
        if media_type == 'movie':
                sql_select = "SELECT * FROM movie"
                if tmdb_id:
                    sql_select = sql_select + " WHERE tmdb_id = '%s'" % tmdb_id
                else:
                    sql_select = sql_select + " WHERE title = '%s'" % name

                if year:
                    sql_select = sql_select + " AND year = %s" % year
         
        try:
            self.dbcur.execute(sql_select)            
            matchedrow = self.dbcur.fetchone()
        except Exception, e:
            xbmc.log('************* Error selecting from cache db: %s' % e, 4)
            return None
            
        if matchedrow:
            xbmc.log('Found meta information by name in cache table: %s' % dict(matchedrow), 0)
            return dict(matchedrow)
        else:
            xbmc.log('No match in local DB', 0)
            return None
        
    def _cache_save(self, meta, media_type, overlay):
    
        #self.dbcur.execute('INSERT INTO movie VALUES (NULL, x)'), meta)
        xbmc.log(str(meta))       
        
        columns = ', '.join(meta.keys())
        placeholders = ':'+', :'.join(meta.keys())
        sql = 'INSERT INTO movie (%s) VALUES (%s)' % (columns, placeholders)
        self.dbcur.execute(sql, meta)
        try:
            self.db.commit() 
            cConfig().log('SQL INSERT watched Successfully') 
        except Exception, e:
            #print ('************* Error attempting to insert into %s cache table: %s ' % (table, e))
            cConfig().log('SQL ERROR INSERT') 
            pass
        self.db.close()
    
    
        
    def get_meta(self, media_type, name, imdb_id='', tmdb_id='', year='', overlay=6, update=False):
        '''
        Main method to get meta data for movie or tvshow. Will lookup by name/year 
        if no IMDB ID supplied.       
        
        Args:
            media_type (str): 'movie' or 'tvshow'
            name (str): full name of movie/tvshow you are searching
        Kwargs:
            imdb_id (str): IMDB ID        
            tmdb_id (str): TMDB ID
            year (str): 4 digit year of video, recommended to include the year whenever possible
                        to maximize correct search results.
            overlay (int): To set the default watched status (6=unwatched, 7=watched) on new videos
                        
        Returns:
            DICT of meta data or None if cannot be found.
        '''
       
        xbmc.log('vstream Meta', 0)
        xbmc.log('Attempting to retrieve meta data for %s: %s %s %s %s' % (media_type, name, year, imdb_id, tmdb_id), 0)
        #recherche dans la base de donner
        if not update:
            meta = self._cache_search(media_type, name, tmdb_id, year)
        else:
            meta = {}
            
        #recherche online

        if not meta:
            
            if media_type=='movie':
                if tmdb_id:
                    meta = self.search_movie_id(tmdb_id)                
                else:
                    meta = self.search_movie_name(name, year)
            elif media_type=='tvshow':
                if tmdb_id:
                    meta = self.search_tvshow_id(tmdb_id)
                else:
                    meta = self.search_tvshow_name(name, year)
            #meta = self.__format_meta(media_type, meta, name)
            xbmc.log(str(meta))   
            
            #transforme les metas
            meta = self._format(meta)         
            #ecrit dans le cache
            self._cache_save(meta, media_type, overlay)
            

            
        
        return meta

    def _call(self, action, append_to_response):
        url = '%s%s?api_key=%s&%s&language=%s' % (self.URL, action, self.api_key, append_to_response, self.lang)
        response = urlopen(url)
        data = json.loads(response.read())
        if self.debug:
            pprint.pprint(data)
            print 'URL: ' + url
        return data