# -*- coding: utf-8 -*-
#Code de depart par AnthonyBloomer
#Modif pour vStream

from resources.lib.config import cConfig

import json, os, copy
import pprint
from urllib import quote_plus, urlopen, urlencode
import xbmc

try:
    from sqlite3 import dbapi2 as sqlite
    cConfig().log('SQLITE 3 as DB engine') 
except:
    from pysqlite2 import dbapi2 as sqlite
    cConfig().log('SQLITE 2 as DB engine') 

    
# https://developers.themoviedb.org/3
class cTMDb:
    URL = "http://api.themoviedb.org/3/"

    def __init__(self, api_key, debug=False, lang='fr'):
        self.api_key = api_key
        self.debug = debug
        self.lang = lang
        self.poster = 'https://image.tmdb.org/t/p/%s' % cConfig().getSetting('poster_tmdb')
        self.fanart = 'https://image.tmdb.org/t/p/%s'  % cConfig().getSetting('backdrop_tmdb')
        self.cache = os.path.join(cConfig().getSettingCache(),'video_cache.db')
        
        try:
            if not os.path.exists(self.cache):
                f = open(self.cache,'w')
                f.close()
                self.db = sqlite.connect(self.cache)
                self.db.row_factory = sqlite.Row 
                self.dbcur = self.db.cursor()
                self.__createdb()
        except:
            pass
            
        try:
            self.db = sqlite.connect(self.cache)
            self.db.row_factory = sqlite.Row 
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
                           "imdb_id TEXT, "\
                           "tmdb_id TEXT, "\
                           "title TEXT, "\
                           "year INTEGER,"\
                           "director TEXT, "\
                           "writer TEXT, "\
                           "cast TEXT,"\
                           "rating FLOAT, "\
                           "votes TEXT, "\
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
                           "UNIQUE(imdb_id, tmdb_id, title)"\
                           ");"
                           
        self.dbcur.execute(sql_create)
       
        sql_create = "CREATE TABLE IF NOT EXISTS season ("\
                           "imdb_id TEXT, "\
                           "tmdb_id TEXT, " \
                           "season INTEGER, "\
                           "year INTEGER,"\
                           "premiered TEXT, "\
                           "cover_url TEXT,"\
                           "playcount INTEGER,"\
                           "UNIQUE(imdb_id, tmdb_id, season)"\
                           ");"
                           
        self.dbcur.execute(sql_create)
        
        sql_create = "CREATE TABLE IF NOT EXISTS episode ("\
                           "imdb_id TEXT, "\
                           "tmdb_id TEXT, "\
                           "episode_id TEXT, "\
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
                           "UNIQUE(imdb_id, tmdb_id, episode_id, title)"\
                           ");"
                           
        self.dbcur.execute(sql_create)
        xbmc.log("table creer")
        
    def __del__(self):
        ''' Cleanup db when object destroyed '''
        try:
            self.dbcur.close()
            self.dbcon.close()
        except: pass

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
        if 'errors' not in meta:
            if meta and meta['total_results'] == 0 and year:
                    meta = self.search_movie_name(name,'')
                    
            #cherche 1 seul resultat
            if meta and meta['total_results'] != 0 and meta['results']:
                tmdb_id = meta['results'][0]['id'] 
                #cherche toutes les infos
                meta = self.search_movie_id(tmdb_id)
            else:
                meta = {}
        else:
            meta = {}
            
        return meta
     
            # Search for TV shows by title.
    def search_tvshow_name(self, name, year='', page=1):
    
        meta = {}
        
        if year:
            term = name + '&year=' + year
        else:
            term = name
        meta = self._call('search/tv', 'query=' + quote_plus(term) + '&page=' + str(page))
        if 'errors' not in meta:
            if meta and meta['total_results'] == 0 and year:
                    meta = self.search_tvshow_name(name,'')  
            #cherche 1 seul resultat
            if meta and meta['total_results'] != 0 and meta['results']:
                tmdb_id = meta['results'][0]['id'] 
                #cherche toutes les infos
                meta = self.search_tvshow_id(tmdb_id)
            else:
                meta = {}
        else:
            meta = {}
            
        return meta
      
    # Get the basic movie information for a specific movie id.
    def search_movie_id(self, movie_id, append_to_response="append_to_response=trailers,credits"):
        result = self._call('movie/'+ str(movie_id), append_to_response)
        return result #obj(**self._call('movie/' + str(movie_id), append_to_response))
        
    # Get the primary information about a TV series by id.
    def search_tvshow_id(self, show_id, append_to_response="append_to_response=external_ids,credits,translations"):
        result = self._call('tv/' + str(show_id), append_to_response)
        return result
        
        
    # Get the similar movies for a specific movie id.
    def similar(self, id, page=1):
        arr = []
        result = self._call('movie/' + str(id) + '/similar', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr



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
     
    def _cache_format(self, meta):
    
        if 'cast' in meta:
            meta['cast'] = eval(str(meta['cast']))
            
        if 's_cover_url' in meta:
            meta['cover_url'] = meta['s_cover_url']
            
        if 's_premiered' in meta:
            meta['premiered'] = meta['s_premiered']
            
        if 's_year' in meta:
            meta['year'] = meta['s_year']
            
            
        return meta
        
    def _format(self, meta, name):
        _meta = {}

        if not 'title' in meta:
            _meta['title'] = name
        else:            
            _meta['title'] = meta['title']
        if 'id' in meta:
            _meta['tmdb_id'] = meta['id']
        if 'imdb_id' in meta:
            _meta['imdb_id'] = meta['imdb_id']
        else:
            _meta['imdb_id'] = ""
            
        if 'external_ids' in meta:
            _meta['imdb_id'] = meta['external_ids']['imdb_id']
         
            
        if 'runtime' in meta:
            if meta['runtime'] > 0:
                _meta['duration'] = int(meta['runtime']) *60
            else: 
                 _meta['duration'] = 0
                 
         
        if 'overview' in meta:
            _meta['plot'] = meta['overview']
        
        if 'certification' in meta:
            _meta['mpaa'] = meta['certification']
        if 'release_date' in meta:
            _meta['premiered'] = meta['release_date']
        if 'first_air_date' in meta:
            _meta['premiered'] = meta['first_air_date']
        if 'premiered' in _meta:
            _meta['year'] = int(_meta['premiered'][:4])
        # if not 'year' in meta and 'premiered' in _meta:
            # _meta['year'] = _meta['premiered']
        
        if 'production_companies' in meta:
            _meta['studio'] = ""
            for studio in meta['production_companies']:
                if _meta['studio'] == "":
                     _meta['studio'] += studio['name']
                else:
                    _meta['studio'] += ' / '+studio['name']
                    
        if 'genres' in meta:
            _meta['genre'] = ""
            for genre in meta['genres']:
                if _meta['genre'] == "":
                     _meta['genre'] += genre['name']
                else:
                    _meta['genre'] += ' / '+genre['name']
            
        if 'backdrop_path' in meta:
            _meta['backdrop_url'] = self.fanart+str(meta['backdrop_path'])
        if 'poster_path' in meta:
            _meta['cover_url'] = self.poster+str(meta['poster_path'])
        
        if not 'playcount' in meta:
            _meta['playcount'] = self.__set_playcount(6)
            
        if 'tagline' in meta:
            _meta['tagline'] = meta['tagline']
            
        if 'vote_average' in meta:
            _meta['rating'] = meta['vote_average']
            
        if 'vote_count' in meta:
            _meta['votes'] = meta['vote_count']
            
        if 'seasons' in meta:
                _meta['seasons'] = meta['seasons']
            
        # if 'cast' in meta:
            # xbmc.log("passeeeeeeeeeeeeeeeeeee")
            # _meta['cast'] = json.loads(_meta['cast'])
            
        if 'credits' in meta:
            #meta['cast'] = str(meta['casts']['cast'])
            licast = []
            for cast in meta['credits']['cast']:
                licast.append((cast['name'], cast['character']))
            _meta['cast'] = licast

            _meta['writer'] = ""
            for crew in meta['credits']['crew']:
                if crew['job'] == 'Director':
                    _meta['director'] = crew['name']
                else:  
                    if _meta['writer'] == "":
                        _meta['writer'] += '%s (%s)' % (crew['job'], crew['name'])
                    else:
                       _meta['writer'] += ' / %s (%s)' % (crew['job'], crew['name'])
                                 
            
        #ont prend juste le premier
        try:
            _meta['trailer'] = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % meta['trailers']['youtube'][0]['source']
        except:
            _meta['trailer'] = ''
            
    
        return _meta
     
    def _clean_title(self, title):
        title= title.replace(' ', '')
        title = title.lower()
        return title
        
        
    def _cache_search(self, media_type, name, tmdb_id='', year=''):
        if media_type == "movie":
            sql_select = "SELECT * FROM movie"
            if tmdb_id:
                sql_select = sql_select + " WHERE tmdb_id = '%s'" % tmdb_id
            else:
                sql_select = sql_select + " WHERE title = '%s'" % name

            if year:
                sql_select = sql_select + " AND year = %s" % year
                
        elif media_type == "tvshow":
            sql_select = "SELECT * FROM tvshow"
            if xbmc.getInfoLabel('ListItem.season'):
                sql_select = "SELECT *, season.cover_url as s_cover_url, season.premiered as s_premiered, season.year as s_year FROM tvshow LEFT JOIN season ON tvshow.imdb_id = season.imdb_id"
            if tmdb_id:
                sql_select = sql_select + " WHERE tvshow.tmdb_id = '%s'" % tmdb_id
            else:
                sql_select = sql_select + " WHERE tvshow.title = '%s'" % name

            if year:
                sql_select = sql_select + " AND tvshow.year = %s" % year
                
            if xbmc.getInfoLabel('ListItem.season'):
                sql_select = sql_select + "and season.season = '%s'" % xbmc.getInfoLabel('ListItem.season')
            
        #xbmc.log(str(sql_select))
        try:
            self.dbcur.execute(sql_select)            
            matchedrow = self.dbcur.fetchone()
        except Exception, e:
            xbmc.log('************* Error selecting from cache db: %s' % e, 4)
            return None
            
        if matchedrow:
            xbmc.log('Found meta information by name in cache table') 
            return self._cache_format(dict(matchedrow))
        else:
            xbmc.log('No match in local DB', 0)
            return None
            
    def _cache_save(self, meta, name, media_type, overlay):

        metadb = copy.copy(meta)    
        metadb['title'] = name
        #list en str
        if 'cast' in metadb:
            metadb['cast'] = str(metadb['cast'])

        #ecrit dans la base les saisons trop lourd?
        if 'seasons' in metadb:
            for season in meta['seasons']:
                if 'poster_path' in season:
                    season['poster_path'] = self.poster+str(season['poster_path'])
            
                sql = "INSERT INTO season (imdb_id, tmdb_id, season, year, premiered, cover_url, playcount) VALUES (?, ?, ?, ?, ?, ?, ?)"
                self.dbcur.execute(sql, (metadb['imdb_id'], season['id'], season['season_number'], season['air_date'], season['air_date'], season['poster_path'], 6))
                try:
                    self.db.commit() 
                    cConfig().log('SQL INSERT Successfully') 
                except Exception, e:
                    cConfig().log('SQL ERROR INSERT') 
                    pass
            del metadb['seasons']
            del meta['seasons']
        
        columns = ', '.join(metadb.keys())
        placeholders = ':'+', :'.join(metadb.keys())
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (media_type, columns, placeholders)
        self.dbcur.execute(sql, metadb)
        try:
            self.db.commit() 
            cConfig().log('SQL INSERT Successfully') 
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
            meta = self._cache_search(media_type, self._clean_title(name), tmdb_id, year)
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
            #transforme les metas
            if meta:
                meta = self._format(meta, name)  
                
                #ecrit dans le cache
                self._cache_save(meta, self._clean_title(name), media_type, overlay)
            else:
                #utiliser par l'addon donc plante si y a vraiment pas de reponse.
                meta['title'] = name         
                meta['imdb_id'] = ''
                meta['tmdb_id'] = ''
                meta['tvdb_id'] = ''        
                meta['backdrop_url'] = ''
                meta['cover_url'] = ''
                meta['playcount'] = ''
                meta['trailer'] = ''
                
        return meta


    def _call(self, action, append_to_response):
        url = '%s%s?api_key=%s&%s&language=%s' % (self.URL, action, self.api_key, append_to_response, self.lang)
        response = urlopen(url)
        xbmc.log(url)
        data = json.loads(response.read())
        if self.debug:
            pprint.pprint(data)
            print 'URL: ' + url
        return data