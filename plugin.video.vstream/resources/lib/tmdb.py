# -*- coding: utf-8 -*-
#Code de depart par AnthonyBloomer
#Modif pour vStream

import json
import pprint
from urllib import quote_plus, urlopen, urlencode
import xbmc


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

    def get_config(self):
        return self._call('configuration', '')

    # Get the basic movie information for a specific movie id.
    def get_movie(self, movie_id, append_to_response="append_to_response=trailers,images,casts,translations"):
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
    def search(self, name, year='', page=1):
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
            xbmc.log('passse')
            tmdb_id = meta['results'][0]['id']
        #cherche toutes les infos
            
            meta = self.get_movie(tmdb_id)
            meta = self._format(meta)
        else:
            meta = {}
       
        
        #[arr.append(obj(**res)) for res in result['results']]
        return meta

    # Get the similar movies for a specific movie id.
    def similar(self, id, page=1):
        arr = []
        result = self._call('movie/' + str(id) + '/similar', 'page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

    # Get the primary information about a TV series by id.
    def get_tv_show(self, show_id, append_to_response="append_to_response=trailers,images,casts,translations"):
        return obj(**self._call('tv/' + str(show_id), append_to_response))

    # Get the latest TV show id.
    def get_latest_tv_show(self):
        return obj(**self._call('tv/latest', ''))

    # Search for TV shows by title.
    def search_tv(self, term, page=1):
        arr = []
        result = self._call('search/tv', 'query=' + quote_plus(term) + '&page=' + str(page))
        [arr.append(obj(**res)) for res in result['results']]
        return arr

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
            _meta['duration'] = meta['runtime'] *60
        _meta['plot'] = meta['overview']
        if 'certification' in meta:
            _meta['mpaa'] = meta['certification']
        if 'release_date' in meta:
            _meta['premiered'] = int(meta['release_date'][:4])
        if not 'year' in meta and 'premiered' in meta:
            _meta['year'] = meta['premiered']
        if 'backdrop_path' in meta:
            _meta['backdrop_url'] = self.fanart+meta['backdrop_path']
        if 'poster_path' in meta:
            _meta['cover_url'] = self.poster+meta['poster_path']
        
        if not 'playcount' in meta:
            _meta['playcount'] = self.__set_playcount(6)
            
        #ont prend juste le premier
        try:
            _meta['trailer'] = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % meta['trailers']['youtube'][0]['source']
        except:
            _meta['trailer'] = ''
            
    
        return _meta

    def _call(self, action, append_to_response):
        url = '%s%s?api_key=%s&%s&language=%s' % (self.URL, action, self.api_key, append_to_response, self.lang)
        response = urlopen(url)
        data = json.loads(response.read())
        if self.debug:
            pprint.pprint(data)
            print 'URL: ' + url
        return data