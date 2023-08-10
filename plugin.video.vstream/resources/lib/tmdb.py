# -*- coding: utf-8 -*-
# Code de depart par AnthonyBloomer
# Modif pour vStream
# https://github.com/Kodi-vStream/venom-xbmc-addons/
import re
import string
import xbmcvfs
import json
import unicodedata
import threading

from resources.lib.comaddon import addon, dialog, VSlog, VSPath, isMatrix, xbmc
from resources.lib.util import QuotePlus

try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine for tmdb')
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine for tmdb')

#Gestion du multithread
lock  = threading.Semaphore()


class cTMDb:
    # https://developers.themoviedb.org/3/genres/get-movie-list
    # https://developers.themoviedb.org/3/genres/get-tv-list
    TMDB_GENRES = {
        12: 'Aventure',
        14: 'Fantastique',
        16: 'Animation',
        18: 'Drame',
        27: 'Horreur',
        28: 'Action',
        35: 'Comédie',
        36: 'Histoire',
        37: 'Western',
        53: 'Thriller',
        80: 'Crime',
        99: 'Documentaire',
        878: 'Science-Fiction',
        9648: 'Mystère',
        10402: 'Musique',
        10749: 'Romance',
        10751: 'Familial',
        10752: 'Guerre',
        10759: 'Action & Aventure',
        10762: 'Kids',
        10763: 'News',
        10764: 'Realité',
        10765: 'Science-Fiction & Fantastique',
        10766: 'Feuilleton',
        10767: 'Talk',
        10768: 'Guerre & Politique',
        10769: 'Etranger',
        10770: 'Téléfilm'
    }

    URL = 'https://api.themoviedb.org/3/'
    URL_TRAILER = 'plugin://plugin.video.youtube/play/?video_id=%s' # ancien : 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
    CACHE = 'special://home/userdata/addon_data/plugin.video.vstream/video_cache.db'

    # important seul xbmcvfs peux lire le special
    if not isMatrix():
        REALCACHE = VSPath(CACHE).decode('utf-8')
    else:
        REALCACHE = VSPath(CACHE)

    def __init__(self, api_key='', debug=False):

        self.ADDON = addon()

        self.api_key = self.ADDON.getSetting('api_tmdb')
        self.debug = debug
        self.lang = self.ADDON.getSetting('tmdb_lang')
        if not self.lang:
            self.lang = 'fr'
        self.poster = 'https://image.tmdb.org/t/p/%s' % self.ADDON.getSetting('poster_tmdb')
        self.fanart = 'https://image.tmdb.org/t/p/%s' % self.ADDON.getSetting('backdrop_tmdb')

        try:
            if not xbmcvfs.exists(self.CACHE):
                self.db = sqlite.connect(self.REALCACHE, isolation_level=None)
                self.db.row_factory = sqlite.Row
                self.dbcur = self.db.cursor()
                self.dbcur.execute('pragma journal_mode=wal')
                self.__createdb()
                return
        except:
            VSlog('Error: Unable to write on %s' % self.REALCACHE)
            pass

        try:
            # Optimisation des acces SqlLite -> Autocommit
            # https://charlesleifer.com/blog/going-fast-with-sqlite-and-python/
            self.db = sqlite.connect(self.REALCACHE, isolation_level=None)
            self.db.row_factory = sqlite.Row
            self.dbcur = self.db.cursor()
            self.dbcur.execute('pragma journal_mode=wal')
        except:
            VSlog('Error: Unable to connect to %s' % self.REALCACHE)
            pass

    def __createdb(self, dropTable=''):
        try:
            # Permets de detruire une table pour la recreer de zero.
            if dropTable != '':
                self.dbcur.execute("DROP TABLE " + dropTable)
        except:
            VSlog('Error: Unable to drop table %s' % dropTable)
            pass

        sql_create = "CREATE TABLE IF NOT EXISTS movie ("\
                     "imdb_id TEXT, "\
                     "tmdb_id TEXT, "\
                     "title TEXT, "\
                     "year INTEGER, "\
                     "director TEXT, "\
                     "writer TEXT, "\
                     "tagline TEXT, "\
                     "cast TEXT, "\
                     "crew TEXT, "\
                     "rating FLOAT, "\
                     "votes TEXT, "\
                     "duration INTEGER, "\
                     "plot TEXT, "\
                     "mpaa TEXT, "\
                     "premiered TEXT, "\
                     "genre TEXT, "\
                     "studio TEXT, "\
                     "status TEXT, "\
                     "poster_path TEXT, "\
                     "trailer TEXT, "\
                     "backdrop_path TEXT, "\
                     "UNIQUE(tmdb_id)"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table movie creee')
        except:
            VSlog('Error: Cannot create table movie')

        sql_create = "CREATE TABLE IF NOT EXISTS saga ("\
                     "tmdb_id TEXT, "\
                     "title TEXT, "\
                     "plot TEXT, "\
                     "genre TEXT, "\
                     "poster_path TEXT, "\
                     "backdrop_path TEXT, "\
                     "UNIQUE(tmdb_id)"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table saga creee')
        except:
            VSlog('Error: Cannot create table saga')

        sql_create = "CREATE TABLE IF NOT EXISTS tvshow ("\
                     "imdb_id TEXT, "\
                     "tmdb_id TEXT, "\
                     "title TEXT, "\
                     "year INTEGER, "\
                     "director TEXT, "\
                     "writer TEXT, "\
                     "cast TEXT, "\
                     "crew TEXT, "\
                     "rating FLOAT, "\
                     "votes TEXT, "\
                     "duration INTEGER, "\
                     "plot TEXT, "\
                     "mpaa TEXT, "\
                     "premiered TEXT, "\
                     "genre TEXT, "\
                     "studio TEXT, "\
                     "status TEXT, "\
                     "poster_path TEXT, "\
                     "trailer TEXT, "\
                     "backdrop_path TEXT, "\
                     "nbseasons INTEGER, "\
                     "UNIQUE(tmdb_id)"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table tvshow creee')
        except:
            VSlog('Error: Cannot create table tvshow')

        sql_create = "CREATE TABLE IF NOT EXISTS season ("\
                     "tmdb_id TEXT, " \
                     "season INTEGER, "\
                     "year INTEGER, "\
                     "premiered TEXT, "\
                     "poster_path TEXT, "\
                     "plot TEXT, "\
                     "episode INTEGER, "\
                     "UNIQUE(tmdb_id, season)"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table season creee')
        except:
            VSlog('Error: Cannot create table season')

        sql_create = "CREATE TABLE IF NOT EXISTS episode ("\
                     "tmdb_id TEXT, "\
                     "originaltitle TEXT,"\
                     "season INTEGER, "\
                     "episode INTEGER, "\
                     "year INTEGER, "\
                     "title TEXT, "\
                     "director TEXT, "\
                     "writer TEXT, "\
                     "guest_stars TEXT, "\
                     "plot TEXT, "\
                     "rating FLOAT, "\
                     "votes TEXT, "\
                     "premiered TEXT, "\
                     "tagline TEXT, "\
                     "poster_path TEXT, "\
                     "UNIQUE(tmdb_id, season, episode)"\
                     ");"

        try:
            self.dbcur.execute(sql_create)
            VSlog('table episode creee')
        except:
            VSlog('Error: Cannot create table episode')

    def __del__(self):
        """ Cleanup db when object destroyed """
        try:
            self.dbcur.close()
            self.db.close()
        except:
            VSlog('Unable to close database')
            pass

    def getToken(self):
        result = self._call('authentication/token/new', '')
        total = len(result)

        if (total > 0):
            url = 'https://www.themoviedb.org/authenticate/'
            if not xbmc.getCondVisibility('system.platform.android'):
                # Si possible on ouvre la page automatiquement dans un navigateur internet.
                import webbrowser
                webbrowser.open(url + result['request_token'])
                sText = (self.ADDON.VSlang(30421)) % (url, result['request_token'])
                DIALOG = dialog()
                if not DIALOG.VSyesno(sText):
                    return False
            else:
                import pyqrcode
                from resources.lib.librecaptcha.gui import cInputWindowYesNo
                qr = pyqrcode.create(url + result['request_token'])
                qr.png(VSPath('special://home/userdata/addon_data/plugin.video.vstream/qrcode.png'), scale=5)
                oSolver = cInputWindowYesNo(captcha='special://home/userdata/addon_data/plugin.video.vstream/qrcode.png', msg="Scanner le QRCode pour acceder au lien d'autorisation", roundnum=1)
                retArg = oSolver.get()
                DIALOG = dialog()
                if retArg == "N":
                    return False

            result = self._call('authentication/session/new', 'request_token=' + result['request_token'])

            if 'success' in result and result['success']:
                self.ADDON.setSetting('tmdb_session', str(result['session_id']))
                DIALOG.VSinfo(self.ADDON.VSlang(30000))
                return
            else:
                DIALOG.VSerror('Erreur' + self.ADDON.VSlang(30000))
                return

            # xbmc.executebuiltin('Container.Refresh')
            return
        return

    # cherche dans les films ou serie l'id par le nom, return ID ou FALSE
    def get_idbyname(self, name, year='', mediaType='movie', page=1):

        # On enleve le contenu entre paranthese.
        try:
            name = name.split('(')[0]
        except:
            pass

        if year:
            term = QuotePlus(name) + '&year=' + year
        else:
            term = QuotePlus(name)

        meta = self._call('search/' + str(mediaType), 'query=' + term + '&page=' + str(page))

        # si pas de résultat avec l'année, on teste sans l'année
        if 'total_results' in meta:
            if year and meta['total_results'] == 0:
                return self.search_movie_name(name)

            # cherche 1 seul resultat
            if meta['total_results'] != 0:
                tmdb_id = meta['results'][0]['id']
                return tmdb_id

        return False

    # Search for movies by title.
    def search_movie_name(self, name, year='', page=1):

        name = re.sub(" +", " ", name)  # nettoyage du titre

        if year:
            term = QuotePlus(name) + '&year=' + year
        else:
            term = QuotePlus(name)

        meta = self._call('search/movie', 'query=' + term + '&page=' + str(page))

        if 'errors' not in meta and 'status_code' not in meta:

            # si pas de résultat avec l'année, on teste sans l'année
            if 'total_results' in meta and meta['total_results'] == 0 and year:
                return self.search_movie_name(name)

            # cherche 1 seul resultat
            if 'total_results' in meta and meta['total_results'] != 0:
                movie = ''

                # s'il n'y en a qu'un, c'est le bon
                if meta['total_results'] == 1:
                    movie = meta['results'][0]

                else:
                    # premiere boucle, recherche la correspondance parfaite sur le nom
                    for searchMovie in meta['results']:
                        if searchMovie['genre_ids'] and 99 not in searchMovie['genre_ids']:
                            if self._clean_title(searchMovie['title']) == self._clean_title(name):
                                movie = searchMovie
                                break
                    # sinon, hors documentaire et année proche
                    if not movie:
                        for searchMovie in meta['results']:
                            if searchMovie['genre_ids'] and 99 not in searchMovie['genre_ids']:

                                # controle supplémentaire sur l'année meme si déjà dans la requete
                                if year:
                                    if 'release_date' in searchMovie and searchMovie['release_date']:
                                        release_date = searchMovie['release_date']
                                        yy = release_date[:4]
                                        if int(year)-int(yy) > 1 :
                                            continue    # plus de deux ans d'écart, c'est pas bon
                                movie = searchMovie
                                break

                    # Rien d'interessant, on prend le premier
                    if not movie:
                        movie = meta['results'][0]

                # recherche de toutes les infos
                tmdb_id = movie['id']
                meta = self.search_movie_id(tmdb_id)
        else:
            meta = {}

        return meta

    # Search for collections by title.
    def search_collection_name(self, name):
        name = re.sub(" +", " ", name)  # nettoyage du titre
        term = QuotePlus(name)
        meta = self._call('search/collection', 'query=' + term)

        if 'errors' not in meta and 'status_code' not in meta:

            # cherche 1 seul resultat
            if 'total_results' in meta and meta['total_results'] != 0:

                collection = ''

                # s'il n'y en a qu'un, c'est le bon
                if meta['total_results'] == 1:
                    collection = meta['results'][0]

                else:
                    # premiere boucle, recherche la correspondance parfaite sur le nom
                    for searchCollec in meta['results']:
                        cleanTitleTMDB = self._clean_title(searchCollec['name'])
                        cleanTitleSearch = self._clean_title(name)
                        if cleanTitleTMDB == cleanTitleSearch:
                            collection = searchCollec
                            break
                    # sinon, le premier qui n'est pas du genre animation
                    if not collection:
                        for searchCollec in meta['results']:
                            if 'animation' not in searchCollec['name']:
                                collection = searchCollec
                                break

                    # Rien d'interessant, on prend le premier
                    if not collection:
                        collection = meta['results'][0]

                meta = collection
                tmdb_id = collection['id']
                meta['tmdb_id'] = tmdb_id

                # recherche de toutes les infos
                meta = self.search_collection_id(tmdb_id)
        else:
            meta = {}

        return meta

    # Search for TV shows by title.
    def search_tvshow_name(self, name, year='', page=1, genre=''):
        if year:
            term = QuotePlus(name) + '&first_air_date_year=' + year
        else:
            term = QuotePlus(name)

        meta = self._call('search/tv', 'query=' + term + '&page=' + str(page))

        if 'errors' not in meta and 'status_code' not in meta:

            # si pas de résultat avec l'année, on teste sans l'année
            if 'total_results' in meta and meta['total_results'] == 0 and year:
                return self.search_tvshow_name(name)

            # cherche 1 seul resultat
            if 'total_results' in meta and meta['total_results'] != 0:
                movie = ''

                # s'il n'y en a qu'un, c'est le bon
                if meta['total_results'] == 1:
                    movie = meta['results'][0]

                else:
                    # premiere boucle, recherche la correspondance parfaite sur le nom
                    for searchMovie in meta['results']:
                        if genre == '' or genre in searchMovie['genre_ids']:
                            movieName = searchMovie['name']
                            if self._clean_title(movieName) == self._clean_title(name):
                                movie = searchMovie
                                break
                    # sinon, hors documentaire et année proche
                    if not movie:
                        for searchMovie in meta['results']:
                            if genre and genre in searchMovie['genre_ids']:

                                # controle supplémentaire sur l'année meme si déjà dans la requete
                                if year:
                                    if 'first_air_date' in searchMovie and searchMovie['first_air_date']:
                                        release_date = searchMovie['first_air_date']
                                        yy = release_date[:4]
                                        if int(year)-int(yy) > 1:
                                            continue    # plus de deux ans d'écart, c'est pas bon
                                movie = searchMovie
                                break

                    # Rien d'interessant, on prend le premier
                    if not movie:
                        movie = meta['results'][0]

                # recherche de toutes les infos
                tmdb_id = movie['id']
                meta = self.search_tvshow_id(tmdb_id)
        else:
            meta = {}

        return meta

    # Search for person by name.
    def search_person_name(self, name):
        name = re.sub(" +", " ", name)  # nettoyage du titre
        term = QuotePlus(name)

        meta = self._call('search/person', 'query=' + term)

        # si pas d'erreur
        if 'errors' not in meta and 'status_code' not in meta:

            # on prend le premier resultat
            if 'total_results' in meta and meta['total_results'] != 0:
                meta = meta['results'][0]

                # recherche de toutes les infos
                person_id = meta['id']
                meta = self.search_person_id(person_id)
        else:
            meta = {}

        return meta

    # Get the basic movie information for a specific movie id.
    def search_movie_id(self, movie_id, append_to_response='append_to_response=trailers,credits,release_dates'):
        result = self._call('movie/' + str(movie_id), append_to_response)
        result['tmdb_id'] = movie_id
        return result  # obj(**self._call('movie/' + str(movie_id), append_to_response))

    # Get the primary information about a TV series by id.
    def search_tvshow_id(self, show_id, append_to_response='append_to_response=external_ids,videos,credits,release_dates'):
        result = self._call('tv/' + str(show_id), append_to_response)
        result['tmdb_id'] = show_id
        return result

    # Get the primary information about a TV series by id.
    def search_season_id(self, show_id, season):
        result = self._call('tv/' + str(show_id) + '/season/' + str(season))
        result['tmdb_id'] = show_id
        return result

    # Get the primary information about a episode.
    def search_episode_id(self, show_id, season, episode):
        if season:
            result = self._call('tv/' + str(show_id) + '/season/' + str(season) + '/episode/' + str(episode))
            result['tmdb_id'] = show_id
            return result
        else:
            return False

    # Get the basic informations for a specific collection id.
    def search_collection_id(self, collection_id):
        result = self._call('collection/' + str(collection_id))
        result['tmdb_id'] = collection_id
        return result

    # Get the basic person informations for a specific person id.
    def search_person_id(self, person_id):
        result = self._call('person/' + str(person_id))
        result['tmdb_id'] = person_id
        return result

    # Get the informations for a specific network.
    def search_network_id(self, network_id):
        result = self._call('network/%s/images' % str(network_id))
        if 'status_code' not in result and 'logos' in result:
            network = result['logos'][0]
            vote = -1

            # On prend le logo qui a la meilleure note
            for logo in result['logos']:
                logoVote = float(logo['vote_average'])
                if logoVote > vote:
                    network = logo
                    vote = logoVote
            network['tmdb_id'] = network_id
            network.pop('vote_average')
            return network
        return {}

    def _format(self, meta, name, media_type=""):
        _meta = {
            'imdb_id': meta.get('imdb_id', ""),
            'tmdb_id': meta.get('tmdb_id', "") if meta.get('tmdb_id') else meta.get('id'),
            'tvdb_id': "",
            "title": meta.get('title') if meta.get('title') else meta.get('name', ""),
            'media_type': meta.get('media_type', "") if media_type == "" else media_type,
            'rating': meta.get('s_vote_average', 0.0) if meta.get('s_vote_average') else meta.get('vote_average', 0.0),
            'votes': meta.get('s_vote_count', 0) if meta.get('s_vote_count') else meta.get('vote_count', 0),
            "duration": 0,
            'plot':  ''.join([meta.get(key, "") for key in ['s_overview', 'overview', 'biography'] if meta.get(key) != None]),
            'mpaa': meta.get('mpaa', ""),
            'premiered': meta.get('s_premiered', "") if meta.get('s_premiered') else meta.get('release_date', "") if meta.get('release_date') else meta.get('first_air_date', "") if meta.get('first_air_date') else meta.get('air_date', ""),
            'year': meta.get('s_year', 0) if meta.get('s_year') else meta.get('year', 0),
            'trailer': '',
            'tagline': meta.get('name') if media_type == "episode" else meta.get('tagline'),
            'genre': '',
            'studio': '',
            'status': meta.get('status', ""),
            'cast': '',
            'crew': '',
            'director': meta.get('s_director', "") if meta.get('s_director') else meta.get('director', ""),
            'writer': meta.get('s_writer', "") if meta.get('s_writer') else meta.get('writer', ""),
            'poster_path': ''.join([meta.get(key, "") for key in ['poster_path', 'still_path', 'file_path', 'profile_path'] if meta.get(key) != None]),
            'backdrop_path': ''.join([meta.get(key, "") for key in ['backdrop_path', 'still_path', 'file_path', 'profile_path'] if meta.get(key) != None]),
            'episode': meta.get('episode_number', 0),
            'season':  meta.get('season_number', 0) if meta.get('season_number') else meta.get('seasons', []),
            'nbseasons': meta.get('number_of_seasons', ""),
            'guest_stars': str(meta.get('guest_stars', [])),
            }


        if 'episode_run_time' in meta and len(meta['episode_run_time']):
            duration = meta.get('episode_run_time', 0)[0]
        else:
            duration = meta.get('runtime', 0)
        if duration:
            _meta['duration'] = duration * 60

        
        try:
            if _meta['year'] == 0:
                _meta['year'] = int(_meta['premiered'][:4])
        except:
            pass

        if 'production_companies' in meta:
            for studio in meta['production_companies']:
                if _meta['studio'] == '':
                    _meta['studio'] += studio['name']
                else:
                    _meta['studio'] += ' / ' + studio['name']

        if 'genre' in meta:
            listeGenre = meta['genre']
            if '{' in listeGenre:
                meta['genres'] = eval(listeGenre)
            else:
                _meta['genre'] = listeGenre
        elif 'genres' in meta:
            for genre in meta['genres']:
                if _meta['genre'] == '':
                    _meta['genre'] += genre['name']
                else:
                    _meta['genre'] += ' / ' + genre['name']

        elif 'genre_ids' in meta:
            genres = self.getGenresFromIDs(meta['genre_ids'])
            _meta['genre'] = ''
            for genre in genres:
                if _meta['genre'] == '':
                    _meta['genre'] += genre
                else:
                    _meta['genre'] += ' / ' + genre

            if not isMatrix():
                _meta['genre'] = unicode(_meta['genre'], 'utf-8')

        elif 'parts' in meta:   # Il s'agit d'une collection, on récupere le genre du premier film
            genres = self.getGenresFromIDs(meta['parts'][0]['genre_ids'])
            _meta['genre'] = ''
            for genre in genres:
                if _meta['genre'] == '':
                    _meta['genre'] += genre
                else:
                    _meta['genre'] += ' / ' + genre

            if not isMatrix():
                _meta['genre'] = unicode(_meta['genre'], 'utf-8')

        trailer_id = ''
        if 'trailer' in meta and meta['trailer']:   # Lecture du cache
            _meta['trailer'] = meta['trailer']
        elif 'trailers' in meta:    # Trailer d'un film retourné par TMDB
            try:    # Recherche de la BA en français
                trailers = meta['trailers']['youtube']
                for trailer in trailers:
                    if trailer['type'] == 'Trailer':
                        if 'VF' in trailer['name']:
                            trailer_id = trailer['source']
                            break
                # pas de trailer français, on prend le premier
                if not trailer_id:
                    trailer_id = meta['trailers']['youtube'][0]['source']
                _meta['trailer'] = self.URL_TRAILER % trailer_id
            except:
                pass
        elif 'videos' in meta and meta['videos']:  # Trailer d'une série retourné par TMDB
            try:  # Recherche de la BA en français
                trailers = meta['videos']
                if len(trailers['results']) > 0:
                    for trailer in trailers['results']:
                        if trailer['type'] == 'Trailer' and trailer['site'] == 'YouTube':
                            trailer_id = trailer['key']  # Au moins c'est un trailer, pas forcement français
                            if 'fr' in trailer['iso_639_1']:
                                trailer_id = trailer['key']
                                break
                    # pas de trailer, on prend la premiere vidéo disponible
                    if not trailer_id:
                        trailer_id = meta['videos'][0]['key']
                    _meta['trailer'] = self.URL_TRAILER % trailer_id
            except:
                pass

        if 'credits' in meta and meta['credits']:
            # Code from https://github.com/jurialmunkey/plugin.video.themoviedb.helper/blob/matrix/resources/lib/tmdb/mapping.py
            cast_list = []
            if meta.get('credits', {}).get('cast'):
                cast_list += meta['credits']['cast']
            cast = []
            cast_item = None
            for i in sorted(cast_list, key=lambda k: k.get('order', 0)):
                if cast_item:
                    if cast_item.get('name') != i.get('name'):
                        cast.append(cast_item)
                        cast_item = None
                    elif i.get('character'):
                        if 'role' in cast_item:
                            cast_item['role'] = u'{} / {}'.format(cast_item['role'], i['character'])
                        else:
                            cast_item = None
                if not cast_item:
                    cast_item = {
                        'id': i.get('id'),
                        'name': i.get('name'),
                        'character': i.get('character'),
                        'order': i.get('order')}
                    if i.get('profile_path'):
                        cast_item['thumbnail'] = self.poster + i['profile_path']
            if cast_item:
                cast.append(cast_item)
            _meta['cast'] = json.dumps(cast)

        # Pas dans le cache, à récupérer depuis TMDB
        if not _meta['director'] and not _meta['writer']:
            crews = []
            if "credits" in meta:
                crews = eval(str(meta['credits']['crew']))
                _meta['crew'] = json.dumps(crews)
            elif "crew" in meta: # cas des épisodes
                crews = eval(str(meta['crew']))

            if len(crews) > 0:
                for crew in crews:
                    if crew['job'] == 'Director':
                        _meta['director'] = crew['name']
                    elif crew['department'] == 'Writing':
                        if _meta['writer'] != '':
                            _meta['writer'] += ' / '
                        _meta['writer'] += '%s (%s)' % (crew['job'], crew['name'])
                    elif crew['department'] == 'Production' and 'Producer' in crew['job']:
                        if _meta['writer'] != '':
                            _meta['writer'] += ' / '
                        _meta['writer'] += '%s (%s)' % (crew['job'], crew['name'])

        if _meta["mpaa"] == "":
            try:
                cert = meta['release_dates']
                if len(cert['results']) >0:
                    for data in cert['results']:
                        if 'fr' in data['iso_3166_1']:
                            _meta['mpaa'] = data['release_dates'][0]['certification']
                            break
                    if not _meta['mpaa']:
                        _meta['mpaa'] = cert['results'][0]['release_dates'][0]['certification']
            except:
                pass

        if _meta['poster_path']:
            _meta['poster_path'] = self.poster + _meta['poster_path']

        if _meta['backdrop_path']:
            _meta['backdrop_path'] = self.fanart + _meta['backdrop_path']
        return _meta

    def _clean_title(self, title):
        # vire accent
        try:
            bMatrix = isMatrix()
            if not bMatrix:
                title = unicode(title, 'utf-8')
            title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('unicode_escape')
            if not bMatrix:
                title = title.encode('utf-8')  # on repasse en utf-8
        except Exception as e:
            pass

        # Vire tous les caracteres non alphabetiques
        title = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), '', title.lower())
        return title

    def _cache_search(self, media_type, name, tmdb_id='', year='', season='', episode=''):
        if media_type == 'movie':
            sql_select = 'SELECT * FROM movie'
            if tmdb_id:
                sql_select = sql_select + ' WHERE tmdb_id = \'%s\'' % tmdb_id
            else:
                sql_select = sql_select + ' WHERE title = \'%s\'' % name
                if year:
                    sql_select = sql_select + ' AND year = %s' % year

        elif media_type == 'collection':
            sql_select = 'SELECT * FROM saga'
            if tmdb_id:
                sql_select = sql_select + ' WHERE tmdb_id = \'%s\'' % tmdb_id
            else:
                sql_select = sql_select + ' WHERE title = \'%s\'' % name

        elif media_type == 'tvshow' or media_type == 'anime':
            sql_select = 'SELECT * FROM tvshow'
            if tmdb_id:
                sql_select = sql_select + ' WHERE tvshow.tmdb_id = \'%s\'' % tmdb_id
            else:
                sql_select = sql_select + ' WHERE tvshow.title = \'%s\'' % name
                if year:
                    sql_select = sql_select + ' AND tvshow.year = %s' % year

        elif media_type == 'season' and season:
            sql_select = 'SELECT *, season.poster_path, season.premiered, ' \
                             'season.year, season.plot FROM season LEFT JOIN tvshow ON season.tmdb_id = tvshow.tmdb_id'
            if tmdb_id:
                sql_select = sql_select + ' WHERE tvshow.tmdb_id = \'%s\'' % tmdb_id
            else:
                sql_select = sql_select + ' WHERE tvshow.title = \'%s\'' % name
                if year:
                    sql_select = sql_select + ' AND tvshow.year = %s' % year
            
            sql_select = sql_select + ' AND season.season = \'%s\'' % season

        elif media_type == 'episode':
            sql_select = 'SELECT *, episode.title, episode.poster_path, episode.premiered, '\
                'episode.guest_stars, episode.year, episode.plot, '\
                'episode.director, episode.writer, episode.rating, episode.votes '\
                'FROM episode LEFT JOIN tvshow ON episode.tmdb_id = tvshow.tmdb_id'
            if tmdb_id:
                sql_select += ' WHERE tvshow.tmdb_id = \'%s\'' % tmdb_id
            else:
                sql_select += ' WHERE tvshow.title = \'%s\'' % name
                if year:
                    sql_select = sql_select + ' AND tvshow.year = %s' % year
            sql_select += ' AND episode.season = \'%s\' AND episode.episode = \'%s\'' % (season, episode)
        else:
            return None

        matchedrow = None
        try:
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
        except Exception as e:
            VSlog('************* Error selecting from cache db: %s' % e, 4)
            if 'no such column' in str(e) or 'no column named' in str(e):
                # Pour les series il faut reconstruire les deux tables.
                if media_type == "tvshow":
                    self.__createdb('tvshow')
                    self.__createdb('season')
                else:
                    self.__createdb(media_type)
                VSlog('Table recreated')

            # Deuxieme tentative
            try:
                self.dbcur.execute(sql_select)
                matchedrow = self.dbcur.fetchone()
                VSlog('************* Error fixed')
            except Exception as e:
                VSlog('************* Error 2: %s' % e, 4)
                pass

        if matchedrow:
            # VSlog('Found meta information by name in cache table')
            return dict(matchedrow)
        else:
            # VSlog('No match in local DB')
            return None

    def _cache_save(self, meta, name, media_type, season, episode, year):
        # Pas de cache pour les personnes ou les distributeurs
        if media_type in ('person', 'network'):
            return

        # cache des films
        if media_type == 'movie':
            return self._cache_save_movie(meta, name, year)

        # cache des séries et animes
        if media_type == 'tvshow' or media_type == 'anime':
            return self._cache_save_tvshow(meta, name, season, year)

        # cache des saisons
        if media_type == "season":
            return self._cache_save_season(meta, season)

        # cache des épisodes
        if media_type == "episode":
            return self._cache_save_episode(meta, name, season, episode)

        # cache des collections
        if media_type == 'collection':
            return self._cache_save_collection(meta, name)

            
            
    # sauvegarde movie dans la BDD
    def _cache_save_movie(self, meta, name, year):
        # year n'est pas forcement l'année du film mais l'année utilisée pour la recherche
        if not year and 'year' in meta:
            year = meta['year']

        try:
            sql = 'INSERT or IGNORE INTO movie (imdb_id, tmdb_id, title, year, cast, crew, writer, director, tagline, rating, votes, duration, ' \
                  'plot, mpaa, premiered, genre, studio, status, poster_path, trailer, backdrop_path) ' \
                  'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self._sqlExecute(sql, (meta['imdb_id'], meta['tmdb_id'], name, year, meta['cast'], meta['crew'], meta['writer'], meta['director'], meta['tagline'], meta['rating'], meta['votes'], str(meta['duration']), meta['plot'], meta['mpaa'], meta['premiered'], meta['genre'], meta['studio'], meta['status'], meta['poster_path'], meta['trailer'], meta['backdrop_path']))
        except Exception as e:
            VSlog(str(e))
            if 'no such column' in str(e) or 'no column named' in str(e) or "no such table" in str(e):
                self.__createdb('movie')
                VSlog('Table recreated')

                # Deuxieme tentative
                self._sqlExecute(sql, (meta['imdb_id'], meta['tmdb_id'], name, year, meta['cast'], meta['crew'], meta['writer'], meta['director'], meta['tagline'], meta['rating'], meta['votes'], str(meta['duration']), meta['plot'], meta['mpaa'], meta['premiered'], meta['genre'], meta['studio'], meta['status'], meta['poster_path'], meta['trailer'], meta['backdrop_path']))
            else:
                VSlog('SQL ERROR INSERT into table movie')
            pass

    # Cache pour les séries (et animes)
    def _cache_save_tvshow(self, meta, name, season, year):
        # Ecrit les saisons dans le cache
        for s_meta in meta['season']:
            s_meta['tmdb_id'] = meta['tmdb_id']
            self._cache_save_season(s_meta, season)

        if not year and 'year' in meta:
            year = meta['year']

        # sauvegarde tvshow dans la BDD
        try:
            sql = 'INSERT or IGNORE INTO tvshow (imdb_id, tmdb_id, title, year, cast, crew, writer, director, rating, votes, duration, ' \
                  'plot, mpaa, premiered, genre, studio, status, poster_path, trailer, backdrop_path, nbseasons) ' \
                  'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self._sqlExecute(sql, (meta['imdb_id'], meta['tmdb_id'], name, year, meta['cast'], meta['crew'], meta['writer'], meta['director'], meta['rating'], meta['votes'], meta['duration'], meta['plot'], meta['mpaa'], meta['premiered'], meta['genre'], meta['studio'], meta['status'], meta['poster_path'], meta['trailer'], meta['backdrop_path'], meta['nbseasons']))
        except Exception as e:
            VSlog(str(e))
            if 'no such column' in str(e) or 'no column named' in str(e):
                self.__createdb('tvshow')
                VSlog('Table recreated')

                # Deuxieme tentative
                self._sqlExecute(sql, (meta['imdb_id'], meta['tmdb_id'], name, year, meta['cast'], meta['crew'], meta['writer'], meta['director'], meta['rating'], meta['votes'], meta['duration'], meta['plot'], meta['mpaa'], meta['premiered'], meta['genre'], meta['studio'], meta['status'], meta['poster_path'], meta['trailer'], meta['backdrop_path'], meta['nbseasons']))
            else:
                VSlog('SQL ERROR INSERT into table tvshow')
            pass

    # Cache pour les saisons
    def _cache_save_season(self, meta, season):
        if 'air_date' in meta and meta['air_date']:
            premiered = meta['air_date']
        elif 'premiered' in meta and meta['premiered']:
            premiered = meta['premiered']
        else:
            premiered = 0

        s_year = 0
        if 'year' in meta and meta['year']:
            s_year = meta['year']
        else:
            try:
                if premiered:
                    s_year = int(premiered[:4])
            except:
                pass

        if 'season_number' in meta:
            season = meta['season_number']
        elif 'season' in meta:
            season = meta['season']

        if 'overview' in meta:
            plot = meta.get('overview', "")
        else:
            plot = ""

        if meta['poster_path']:
            fanart = self.poster + meta['poster_path']
        else:
            fanart = ""

        try:
            sql = 'INSERT or IGNORE INTO season (tmdb_id, season, year, premiered, poster_path, plot, episode) VALUES '\
                  '(?, ?, ?, ?, ?, ?, ?)'
            self._sqlExecute(sql, (meta['tmdb_id'], season, s_year, premiered, fanart, plot, meta.get('episode_count', 0)))
        except Exception as e:
            VSlog(str(e))
            if 'no such column' in str(e) or 'no column named' in str(e):
                self.__createdb('season')
                VSlog('Table recreated')

                # Deuxieme tentative
                try:
                    self._sqlExecute(sql, (meta['tmdb_id'], season, s_year, premiered, fanart, plot, meta.get('episode_count', 0)))
                except Exception as e:
                    VSlog(str(e))
            else:
                VSlog('SQL ERROR INSERT into table season')
        

    # Cache pour les épisodes
    def _cache_save_episode(self, meta, name, season, episode):
        try:
            title = name + '_S' + season + 'E' + episode
            sql = 'INSERT or IGNORE INTO episode (tmdb_id, originaltitle, season, episode, year, title, premiered, poster_path, plot, rating, votes, director, writer, guest_stars, tagline) VALUES ' \
                  '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self._sqlExecute(sql, (meta['tmdb_id'], title, season, episode, meta['year'], title, meta['premiered'], meta['poster_path'], meta['plot'], meta['rating'], meta['votes'], meta['director'], meta['writer'], ''.join(meta.get('guest_stars', "")), meta["tagline"]))
        except Exception as e:
            VSlog(str(e))
            if 'no such column' in str(e) or 'no column named' in str(e):
                self.__createdb('episode')
                VSlog('Table recreated')

                # Deuxieme tentative
                self._sqlExecute(sql, (meta['tmdb_id'], title, season, episode, meta['year'], title, meta['premiered'], meta['poster_path'], meta['plot'], meta['rating'], meta['votes'], meta['director'], meta['writer'], ''.join(meta.get('guest_stars', "")), meta["tagline"]))
            else:
                VSlog('SQL ERROR INSERT into table episode')

    # Cache pour les sagas
    def _cache_save_collection(self, meta, name):
        try:
            sql = 'INSERT or IGNORE INTO saga (tmdb_id, title, plot, genre, poster_path, backdrop_path) VALUES ' \
                  '(?, ?, ?, ?, ?, ?)'
            self._sqlExecute(sql, (meta['tmdb_id'], name, meta['plot'], meta['genre'], meta['poster_path'], meta["backdrop_path"]))
        except Exception as e:
            VSlog(str(e))
            if 'no such column' in str(e) or 'no column named' in str(e) or "no such table" in str(e):
                self.__createdb('saga')
                VSlog('Table recreated')

                # Deuxieme tentative
                self._sqlExecute(sql, (meta['tmdb_id'], name, meta['plot'], meta['genre'], meta['poster_path'], meta["backdrop_path"]))
            else:
                VSlog('SQL ERROR INSERT into table saga')
            pass

    def get_meta(self, media_type, name, imdb_id='', tmdb_id='', year='', season='', episode='', update=False):
        """
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
            season (int)
            episode (int)

        Returns:
            DICT of meta data or None if cannot be found.
        """

        name = re.sub(" +", " ", name)  # nettoyage du titre
        name = name.replace('VF','').replace('VOSTFR','')
        cleanTitle = None
        
        # VSlog('Attempting to retrieve meta data for %s: %s %s %s %s' % (media_type, name, year, imdb_id, tmdb_id))

        # recherche dans la base de données
        if not update:
            # Obligatoire pour pointer vers les bonnes infos dans la base de données
            if not tmdb_id:
                if media_type in ("season", "tvshow", "anime", "episode"):
                    name = re.sub('(?i)( s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))(?:([^"]+)|)', '', name)

            cleanTitle = self._clean_title(name)
            if not cleanTitle:
                return {}
            meta = self._cache_search(media_type, cleanTitle, tmdb_id, year, season, episode)

            if meta:
                return meta

        # recherche online
        meta = {}
        if media_type == 'movie':
            if tmdb_id:
                meta = self.search_movie_id(tmdb_id)
            elif name:
                meta = self.search_movie_name(name, year)
        elif media_type == 'tvshow':
            if tmdb_id:
                meta = self.search_tvshow_id(tmdb_id)
            elif name:
                meta = self.search_tvshow_name(name, year)
        elif media_type == 'season' and season:
            if tmdb_id:
                meta = self.search_season_id(tmdb_id, season)
            else:  # on retrouve l'id en cherchant la série qui peut être en cache
                meta = self.get_meta('tvshow', name, year=year)
                if 'tmdb_id' in meta and meta['tmdb_id']:
                    return self.get_meta('season', name, tmdb_id=meta['tmdb_id'], year=year, season=season)
        elif media_type == 'episode':
            if tmdb_id:
                meta = self.search_episode_id(tmdb_id, season, episode)
            else:  # on retrouve l'id en cherchant la série qui peut être en cache
                meta = self.get_meta('tvshow', name, year=year)
                if 'tmdb_id' in meta and meta['tmdb_id']:
                    meta = self.search_episode_id(meta['tmdb_id'], season, episode)
        elif media_type == 'anime':
            if tmdb_id:
                meta = self.search_tvshow_id(tmdb_id)
            elif name:
                meta = self.search_tvshow_name(name, year, genre=16)
        elif media_type == 'collection':
            if tmdb_id:
                meta = self.search_collection_id(tmdb_id)
            elif name:
                meta = self.search_collection_name(name)
        elif media_type == 'person':
            if tmdb_id:
                meta = self.search_person_id(tmdb_id)
            elif name:
                meta = self.search_person_name(name)
        elif media_type == 'network':
            if tmdb_id:
                meta = self.search_network_id(tmdb_id)

        # Mise en forme des metas si trouvé
        if meta and 'tmdb_id' in meta:
            meta = self._format(meta, name, media_type)
            # sauvegarde dans un cache
            if not cleanTitle:
                cleanTitle = self._clean_title(name)

            self._cache_save(meta, cleanTitle, media_type, season, episode, year)
        elif meta != False:   # initialise un meta vide
            meta = self._format(meta, name)
        else:
            meta = {}
        return meta

    def getUrl(self, url, page=1, term=''):
        # return url api exemple 'movie/popular' page en cours
        try:
            if term:
                term = term + '&page=' + str(page)
            else:
                term = 'page=' + str(page)
            result = self._call(url, term)
        except:
            return False
        return result
    
    def getPostUrl(self, url, post):
        # Execute une requete POST vers l'API
        # Utile pour :
        #       - Noter film
        #       - Ajouter/Retirer le film des favoris
        #       - Ajouter/Retirer le film de la watchlist
        # Appelé depuis le menu contextuel TMDB
        #
        # Paramètres :
        #   url : le complément de l'url de l'api
        #           ex : 'movie/64408/rating' pour noter un film
        #           ou : '' pour ajouter aux favoris
        #   post : json qui sera envoyé Request Body
        #           ex :   {
        #                   "value": 8.5
        #                  }

        from urllib import request
        session_id = self.ADDON.getSetting('tmdb_session')

        urlapi = self.URL + url +'?api_key='+self.ADDON.getSetting('api_tmdb')+'&session_id='+ session_id
        
        req = request.Request(urlapi, method="POST")
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(post)
        data = data.encode()
        r = request.urlopen(req, data=data)
        response = r.read()
        r.close()
        data = json.loads(response)
        return data    

    def _call(self, action, append_to_response=''):
        from resources.lib.handler.requestHandler import cRequestHandler
        url = '%s%s?language=%s&api_key=%s' % (self.URL, action, self.lang, self.api_key)
        if append_to_response:
            url += '&%s' % append_to_response

        oRequestHandler = cRequestHandler(url)
        data = oRequestHandler.request(jsonDecode=True)

        return data

    # SqlExecute Thread Safe
    def _sqlExecute(self, request, param = None):
        try:
            lock.acquire()
            self.dbcur.execute(request, param)
        except Exception as e:
            raise
        finally:
            lock.release()


    # retourne la liste des genres en Texte, à partir des IDs
    def getGenresFromIDs(self, genresID):
        sGenres = []
        for gid in genresID:
            genre = self.TMDB_GENRES.get(gid)
            if genre:
                sGenres.append(genre)
        return sGenres

    # Retourne le genre en Texte, à partir d'un ID
    def getGenreFromID(self, genreID):
        if not str(genreID).isdigit():
            return genreID

        genre = self.TMDB_GENRES.get(genreID)
        if genre:
            return genre
        return genreID
