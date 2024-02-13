# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import imp
import platform
import random
import threading
import time
import xbmc
import xbmcvfs

from resources.lib.comaddon import progress, addon, dialog, VSlog, VSPath, isMatrix, siteManager
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.util import cUtil, Unquote
from resources.lib.gui.gui import cGui


try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite


SITE_IDENTIFIER = 'pastebin'
SITE_NAME = '[COLOR violet]PasteBin[/COLOR]'

SITE_DESC = 'Liste depuis %s' % SITE_NAME

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SETTING_PASTE_ID = SITE_IDENTIFIER + '_id_'
SETTING_PASTE_LABEL = SITE_IDENTIFIER + '_label_'
UNCLASSIFIED_GENRE = '_NON CLASSÉ_'
UNCLASSIFIED = 'Indéterminé'

MOVIE_MOVIE = (URL_MAIN + '&sMedia=film', 'showMenuFilms')
#MOVIE_NEWS = (URL_MAIN + '&sMedia=film&sYear=2023', 'showMovies')
MOVIE_NEWS = ('movie/now_playing', 'showTMDB')
# MOVIE_GENRES = (URL_MAIN + '&sMedia=film', 'showGenres')
MOVIE_GENRES = ('genre/movie/list', 'showGenreMovieTMDB')

MOVIE_ANNEES = (URL_MAIN + '&sMedia=film', 'showYears')
MOVIE_LIST = (URL_MAIN + '&sMedia=film', 'alphaList')
MOVIE_VIEWS = ('movie/popular', 'showTMDB')
MOVIE_NOTES = ('movie/top_rated', 'showTMDB')

SERIE_SERIES = (URL_MAIN + '&sMedia=serie', 'showMenuTvShows')
SERIE_NEWS = ('trending/tv/day', 'showTMDB')
SERIE_VIEWS = ('tv/popular', 'showTMDB')
SERIE_GENRES = ('genre/tv/list', 'showGenreTV')
SERIE_ANNEES = (URL_MAIN + '&sMedia=serie', 'showYears')
SERIE_LIST = (URL_MAIN + '&sMedia=serie', 'alphaList')

ANIM_ANIMS = (URL_MAIN + '&sMedia=anime', 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + '&sMedia=anime&sYear=2023', 'showMovies')
ANIM_ANNEES = (URL_MAIN + '&sMedia=anime', 'showYears')
ANIM_VFS = (URL_MAIN + '&sMedia=anime&bNews=True', 'showMovies')
ANIM_GENRES = (URL_MAIN + '&sMedia=anime', 'showGroupes')
ANIM_LIST = (URL_MAIN + '&sMedia=anime', 'alphaList')


URL_SEARCH_MOVIES = (URL_MAIN + '&sMedia=film&sSearch=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '&sMedia=serie&sSearch=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + '&sMedia=anime&sSearch=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '&sMedia=divers&sSearch=', 'showMovies')

CACHE = 'special://home/userdata/addon_data/plugin.video.vstream/%s_cache.db' % SITE_IDENTIFIER

# Dépend de la version de python
PYVERSION = platform.python_version()
VSlog('Pastebin - Python version : ' + PYVERSION)
if '3.10' in PYVERSION:
    REALCACHE = VSPath(CACHE)
    PATH = 'special://home/addons/plugin.video.vstream/resources/lib/pasteCrypt310.pyc'
elif '3.11' in PYVERSION:
    REALCACHE = VSPath(CACHE)
    PATH = 'special://home/addons/plugin.video.vstream/resources/lib/pasteCrypt311.pyc'
elif '2.' in PYVERSION:
    REALCACHE = VSPath(CACHE).decode('utf-8')
    PATH = 'special://home/addons/plugin.video.vstream/resources/lib/pasteCrypt2.pyc'
else:  # autre Versions 3.0x
    REALCACHE = VSPath(CACHE)
    PATH = 'special://home/addons/plugin.video.vstream/resources/lib/pasteCrypt3.pyc'


# Pour le multithreading
lock = threading.Semaphore()


def getNbItemParPage():
    nbItem = addon().getSetting(SITE_IDENTIFIER + '_nbItemParPage')
    if not nbItem:
        nbItem = "25"
        addon().setSetting(SITE_IDENTIFIER + '_nbItemParPage', nbItem)
    return int(nbItem)


ITEM_PAR_PAGE = getNbItemParPage()
GROUPE_MAX = 50          # jusqu'à 50 dossiers, limitation du skin
PASTE_PAR_GROUPE = 100   # jusqu'à 100 liens pastebin par dossier


# Durée du cache, en Heures
def getCacheDuration():
    cacheDuration = addon().getSetting(SITE_IDENTIFIER + '_cacheDuration')
    if not cacheDuration:
        cacheDuration = "72"  # en heure
        addon().setSetting(SITE_IDENTIFIER + '_cacheDuration', cacheDuration)
    return int(cacheDuration)


CACHE_DURATION = getCacheDuration()


""" GESTION DU CACHE """


class PasteCache:

    def __init__(self):

        try:
            if not xbmcvfs.exists(CACHE):
                self.db = sqlite.connect(REALCACHE, isolation_level=None)
                self.db.row_factory = sqlite.Row
                self.dbcur = self.db.cursor()
                self.__createdb()
                return
        except:
            VSlog('Error: Unable to create DB %s' % REALCACHE)
            pass

        try:
            self.db = sqlite.connect(REALCACHE, isolation_level=None)
            self.db.row_factory = sqlite.Row
            self.dbcur = self.db.cursor()
        except:
            VSlog('Error: Unable to connect to %s' % REALCACHE)
            pass

    def __createdb(self):

        sql_create = "CREATE TABLE IF NOT EXISTS %s ("\
                     "paste_id TEXT, "\
                     "date FLOAT, "\
                     "content BLOB,"\
                     "UNIQUE(paste_id)"\
                     ");" % SITE_IDENTIFIER
        try:
            self.dbcur.execute(sql_create)
            VSlog('table %s creee' % SITE_IDENTIFIER)
        except:
            VSlog('Error: Unable to create table %s' % SITE_IDENTIFIER)

    def __del__(self):
        """ Cleanup db when object destroyed """
        try:
            self.dbcur.close()
            self.db.close()
        except:
            pass

    # Récupérer dans le cache
    def read(self, pasteID):

        try:
            sql_select = 'SELECT * FROM %s WHERE paste_id = \'%s\'' % (SITE_IDENTIFIER, pasteID)
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
        except Exception as e:
            VSlog('************* Error selecting from %s db: %s' % (SITE_IDENTIFIER, e), 4)
            return None, False, False

        if matchedrow:
            data = dict(matchedrow)

            # Supprimer les données trop anciennes
            renew = False
            cacheDuration = time.time() - CACHE_DURATION * 3600
            if data['date'] < cacheDuration:
                renew = True

            # Utiliser les données du cache
            if isMatrix():
                content = data['content'].decode("utf-8")
            else:
                content = str(data['content'])
            if content[-1] == '.':
                return content[:-1], True, renew
            return content, False, renew
        else:
            return None, False, False

    # Sauvegarde des données dans un cache
    def save(self, pasteID, pasteContent, isMovie):

        try:
            sql = 'INSERT or IGNORE INTO %s (paste_id, content, date) VALUES (?, ?, ?)' % SITE_IDENTIFIER
            buff = str(pasteContent)
            if isMovie:
                buff += '.'

            if isMatrix():
                buff = memoryview(bytes(buff, encoding='utf-8'))
            else:
                buff = buffer(buff)

            lock.acquire()
            self.dbcur.execute(sql, (pasteID, buff, time.time()))
        except Exception as e:
            VSlog('SQL ERROR INSERT into table \'%s\', ID=%s, e=%s' % (SITE_IDENTIFIER, pasteID, e))
            pass
        finally:
            lock.release()

    # Supprimer une entrée
    def remove(self, pasteID):
        try:
            sql_delete = 'DELETE FROM %s WHERE paste_id = \'%s\'' % (SITE_IDENTIFIER, pasteID)
            lock.acquire()
            self.dbcur.execute(sql_delete)
        except Exception as e:
            VSlog('************* Error deleting from cache db: %s, e=%s' % (pasteID, e), 4)
            return None
        finally:
            lock.release()

    # Supprimer tout le cache
    def clean(self):
        VSlog('PasteCache - deleteAll')
        try:
            sql_delete = 'UPDATE %s set date = 0' % SITE_IDENTIFIER
            # sql_delete = 'DELETE FROM %s' % SITE_IDENTIFIER
            lock.acquire()
            self.dbcur.execute(sql_delete)
        except Exception as e:
            VSlog('************* Error deleting from %s db: %s' % (SITE_IDENTIFIER, e), 4)
            return False
        finally:
            lock.release()
        return True

# Exemple
# CAT; TMDB; TITLE; SAISON; YEAR; GENRES; URLS=https://uptobox.com/
# film;714;Demain ne meurt jamais;James BOND;1997;['Action', 'Aventure', 'Thriller'];['nwxxxx','nwYYzz']
# serie;48866;Les 100;Saison 2; 2014; ['Fantastique', 'Aventure']; {'S02E01':['lien1', 'lien2'], 'S02E02':['lien1']}

# Exemple minimum
# CAT;TITLE; URLS
# film;Mes vacances au mont St-Michel;['https://uptobox.com/nwxxxx']


class PasteContent:
    PASTE = 0       # Id du paste
    CAT = -1        # (Optionnel) - Catégorie 'film', 'serie' 'anime' (Film par défaut)
    TMDB = -1       # (optionnel) - Id TMDB
    TITLE = -1      # Titre du film / épisodes
    SAISON = -1     # (optionnel) - Saison pour les séries (ex 'Saison 03' ou 'S03' ou '03') OU Saga pour les films (ex 'Mission impossible')
    GROUPES = -1    # (optionnel) - Groupes tel que NETFLIX, HBO, MARVEL, DISNEY, Films enfants, ...
    YEAR = -1       # (optionnel) - Année
    GENRES = -1     # (optionnel) - Liste des genres
    RES = -1        # (optionnel) - Résolution (720p, 1080p, 4K, ...)
    DIRECTOR = -1   # (optionnel) - Réalisateur au format id : nom
    CAST = -1       # (optionnel) - Acteurs au format id : nom
    NETWORK = -1    # (optionnel) - Diffuseur au format id : nom
#    HEBERGEUR = ''  # (optionnel) - URL de l'hebergeur, pour éviter de le mettre dans chaque URL, ex : 'https://uptobox.com/'
    movies = False  # Liste des liens, avec épisodes pour les séries
    URLS = -1       # Liste des liens, avec épisodes pour les séries
    chiffrer = None
    cache = None
    keyUpto = None
    keyAlld = None
    keyReald = None
    upToStream = None  # 2 = upToBox, 3 = upToStream, 4 = upToStream+UpToBox. Pas de trie par qualité si uptostream.

    # Pour comparer deux pastes, savoir si les champs sont dans le même ordre
    def isFormat(self, other):
        if not isinstance(other, PasteContent):
            return False

        return self.CAT == other.CAT \
            and self.TMDB == other.TMDB \
            and self.TITLE == other.TITLE \
            and self.SAISON == other.SAISON \
            and self.GROUPES == other.GROUPES \
            and self.YEAR == other.YEAR \
            and self.GENRES == other.GENRES \
            and self.RES == other.RES \
            and self.DIRECTOR == other.DIRECTOR \
            and self.CAST == other.CAST \
            and self.NETWORK == other.NETWORK \
            and self.URLS == other.URLS

    # Utilisation du paramètre "passer par Uptobox ou par uptostream ?"
    # 2 = uptobox
    # 3 = uptostream
    # 4 = uptobox + uptostream
    def getUptoStream(self):
        addons = addon()
        if not self.upToStream:
            if addons.getSetting("hoster_uptobox_premium"): # pas uptobox premium -> mode direct
                mode = 2
            else:   
                mode = int(addons.getSetting("hoster_uptobox_mode_default"))
            self.upToStream = 4-mode
        return self.upToStream

    def getLines(self, pasteBin, sMedia=''):

        sContent, self.movies, renew = self._getCache().read(pasteBin)

        # Lecture en cache
        if sContent:
            lines = eval(sContent)       # TODO trop long
            if lines[0].startswith('#'):    # paste index
                if renew: # renouveller le cache du paste index
                    threading.Timer(10, renewPaste, args=(pasteBin, )).start()
                return self.readIndex(lines, sMedia)
            entete = lines[0].split(";")

        # Lecture sur le site
        else:
            # test si paste accessible
            lines, self.movies = self._decompress(pasteBin)
            if not lines:
                return []

            if lines[0].startswith('#'):  # paste index
                allLines = self.readIndex(lines, sMedia)
                if allLines:
                    self._getCache().save(pasteBin, lines, self.movies)
                return allLines

            # Vérifie si la ligne d'entête existe avec les champs obligatoires
            entete = lines[0].split(";")
            if 'TITLE' not in entete and 'URL' not in entete:
                return []
            self._getCache().save(pasteBin, lines, self.movies)

        # Calcul des index de chaque champ
        self.PASTE = 0
        hebergeur = None
        for champ in entete:
            champ = champ.strip()

            if 'URL' in champ:  # supporte URL ou URLS
                hebergeur = champ.split('=')
                champ = 'URLS'
                if len(hebergeur) > 1:
                    hebergeur = hebergeur[1].replace(' ', '').replace('"', '').replace('\'', '')
                else:
                    hebergeur = None
            if champ in dir(self):
                setattr(self, champ, self.PASTE)
            self.PASTE += 1

        # On vérifie le type de média s'il est demandé
        sMediaPaste = 'film'     # par défaut si non défini
        if self.CAT >= 0:
            sMediaPaste = lines[1].split(";")[self.CAT]
        if sMedia and len(lines) > 1:
            if sMedia != sMediaPaste:
                return []

        isFilm = sMediaPaste in ('film', 'divers')
        links = []
        for k in lines[1:]:
            line = k.split(";")
            line.append(pasteBin)

            # remettre l'hebergeur en prefixe du lien
            if hebergeur:
                link = line[self.URLS]
                if isFilm:
                    if "'" in link:
                        link = link.replace("['", "['" + hebergeur)
                        line[self.URLS] = link.replace(", '", ", '" + hebergeur)
                    else:
                        line[self.URLS] = hebergeur + link
                else:    # series/ anime, plusieurs liens
                    link = link.replace(":'", ": '" + hebergeur) # format en ligne
                    line[self.URLS] = link.replace(": '", ": '" + hebergeur)  # format du cache

            links.append(line)

        # renouveler le contenu d'un paste
        if renew:
            lastMediaTitle = lines[1].split(";")[self.TITLE]
            # décaler le lancement du scan
            decal = random.randint(3, 6)
            t = threading.Timer(decal, renewPaste, args=(pasteBin, lastMediaTitle))
            t.start()

        return links

    # renouveler le contenu du cache, avec préchargement des metadonnées
    def renew(self, pasteId, lastMediaTitle):

        # Vider le cache du paste
        self._getCache().remove(pasteId)

        # Récupérer la dernière version du paste
        movies = self.getLines(pasteId)

        # Préchargement des métadonnées désactivé en attendant de trouver une méthode plus performante 
        if False:
            
            # pas de recherche de contenu pour un paste index
            if not lastMediaTitle:
                return
    
            # Récupérer les métadonnées des derniers contenus
            if self.TMDB == -1 or self.CAT == -1:
                return
    
            from resources.lib.tmdb import cTMDb
            TMDb = cTMDb()
            nbMeta = 100
            numItem = 0
            tmdbIDs = []    # id déjà traités
    
            # Recherche de nouveaux contenus
            progress_ = progress().VScreate(addon().VSlang(30141))
            total = min(nbMeta, len(movies))
    
            # préchargement des méta
            for movie in movies:
                numItem += 1
                if numItem == nbMeta:
                    break
    
                tmdbID = movie[self.TMDB]
                if not tmdbID or tmdbID in tmdbIDs:
                    numItem -= 1
                    continue
                tmdbIDs.append(tmdbID)
    
                sTitle = movie[self.TITLE]
    
                # si on retombe sur le contenu de l'ancien paste, on s'arrête de scanner
                if lastMediaTitle == sTitle:
                    break
    
                progress_.VSupdate(progress_, total, text=sTitle)
    
                sType = movie[self.CAT].replace('film', 'movie').replace('serie', 'tvshow')
                args = (sType, sTitle)
                kwargs = {'tmdb_id': tmdbID}
                meta = TMDb.get_meta(*args, **kwargs)
    
            progress_.VSclose(progress_)

    def resolveLink(self, pasteBin, link):

        uptobox = True
        if 'uptobox' in link:
            uptobox = True
        # elif not 'http' in link:
        #     uptobox = True  # si rien de précisé, on part sur du uptobox
        
        # ces liens sont chiffrés, il faut les déchiffrer
        if uptobox:
            # Recherche d'un compte premium valide
            from resources.lib.handler.premiumHandler import cPremiumHandler
            links = None
            if not self.keyUpto and not self.keyAlld and not self.keyReald:
                self.keyUpto = cPremiumHandler('uptobox').getToken()
                if self.keyUpto:
                    links = self._resolveLink(pasteBin, link)
                if not links:
                    self.keyUpto = None
                    self.keyAlld = cPremiumHandler('alldebrid').getToken()
                    if self.keyAlld:
                        links = self._resolveLink(pasteBin, link)
                if not links:
                    self.keyAlld = None
                    self.keyReald = cPremiumHandler('realdebrid').getToken()
                    if self.keyReald:
                        links = self._resolveLink(pasteBin, link)
                        if not links:
                            self.keyReald = None

            # Un compte avec un des trois débrideurs
            if not links:# and (self.keyUpto or self.keyAlld or self.keyReald):
                links = self._resolveLink(pasteBin, link)
            if links:
                return links
            else:
                dialog().VSinfo('Certains liens ne sont pas disponibles')
                return [(None, None, None)]

        return [(link, 'ori', 'ori')]

    def _resolveLink(self, pasteBin, link):

        # Un token avec un des trois débrideurs
        links = None
        status = 'nok'
        if self.keyUpto:
            upto = self.getUptoStream()
            links, status = self._getCrypt().resolveLink(pasteBin, link, self.keyUpto, upto)
        elif self.keyAlld:
            links, status = self._getCrypt().resolveLink(pasteBin, link, self.keyAlld, 0)
        elif self.keyReald:
            links, status = self._getCrypt().resolveLink(pasteBin, link, self.keyReald, 1)
        elif self.movies:
            links, status = self._getCrypt().resolveLink(pasteBin, link, self.keyReald, -1)
        else:
            links = [(link, "ori", "ori")]
            status = "ok"

        if status != 'ok':  # Certains liens en erreur
            VSlog('Erreur : ' + str(status))

        if links and len(links) > 0:
            return links

    def _decompress(self, pasteBin):

        lines = []
        hasMovies = False
        if len(pasteBin) == 9:
            try:
                lines = self._getCrypt().loadFile(pasteBin)
                if lines:
                    hasMovies = True
            except Exception as e:
                VSlog('Exception \'%s\', ID=%s, e=%s' % (SITE_IDENTIFIER, pasteBin, e))
                pass

        if not hasMovies:
            pastebinUrl = addon().getSetting('pastebin_url')
            if not pastebinUrl:
                pastebinUrl = URL_MAIN
            from resources.lib.handler.requestHandler import cRequestHandler
            oRequestHandler = cRequestHandler(pastebinUrl + pasteBin)
            oRequestHandler.setTimeout(4)
            sContent = oRequestHandler.request()
            if sContent.startswith('<'):
                return [], False

            if sContent.startswith('CAT;'):
                lines = sContent.splitlines()

            # paste index
            elif sContent.startswith('#'):
                lines = sContent.splitlines()

        return lines, hasMovies

    def _getCrypt(self):
        if not self.chiffrer:
            self.chiffrer = imp.load_compiled("Chiffrage", VSPath(PATH)).Crypt()
        return self.chiffrer

    def _getCache(self):
        if not self.cache:
            self.cache = PasteCache()
        return self.cache

    def readIndex(self, pastes, sMedia=''):
        lines = []
        for paste in pastes:
            if paste.startswith('#'):    # ligne en commentaire
                continue
            if len(paste.strip()) == 0:  # ligne vide
                continue
            lines += self.getLines(paste, sMedia)
        return lines


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Divers)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'search/person')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchActor', 'Recherche (Acteurs)', 'actor.png', oOutputParameterHandler)


#    sUrl =
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '&numPage=1&sMedia=film')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'tv.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animes', 'animes.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMisc', 'Divers', 'buzz.png', oOutputParameterHandler)


    # Menu pour gérer les dossiers
    sDecoColor = addon().getSetting('deco_color')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFolder', '[COLOR %s]Gérer les codes[/COLOR]' % sDecoColor, 'notes.png', oOutputParameterHandler)

    # Menu pour gérer les paramètres
    oGui.addDir(SITE_IDENTIFIER, 'adminContenu', '[COLOR %s]Gérer les contenus[/COLOR]' % sDecoColor, 'library.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenu():
    addons = addon()
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')
    sMedia = oInputParameterHandler.getValue('sMedia')

    pbContent = PasteContent()
    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    contenu = getPasteBin(pbContent, pasteBin)

    for numID in range(1, PASTE_PAR_GROUPE):
        pasteBin = addons.getSetting(prefixID + '_' + str(numID))
        contenu = contenu.union(getPasteBin(pbContent, pasteBin))

    if not sMedia:
        oOutputParameterHandler = cOutputParameterHandler()

        cnt = contenu.intersection(['containFilms', 'containSeries', 'containAnimes', 'containDivers'])
        if len(cnt) == 1:
            showDetailMenu(pasteID, contenu)
        else:
            if 'containFilms' in contenu:
                oOutputParameterHandler.addParameter('pasteID', pasteID)
                oOutputParameterHandler.addParameter('sMedia', 'film')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Films', 'films.png', oOutputParameterHandler)

            if 'containSeries' in contenu:
                oOutputParameterHandler.addParameter('pasteID', pasteID)
                oOutputParameterHandler.addParameter('sMedia', 'serie')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Séries', 'tv.png', oOutputParameterHandler)

            if 'containAnimes' in contenu:
                oOutputParameterHandler.addParameter('pasteID', pasteID)
                oOutputParameterHandler.addParameter('sMedia', 'anime')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Animes', 'animes.png', oOutputParameterHandler)

            if 'containDivers' in contenu:
                oOutputParameterHandler.addParameter('pasteID', pasteID)
                oOutputParameterHandler.addParameter('sMedia', 'divers')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Divers', 'buzz.png', oOutputParameterHandler)

        # Menu pour ajouter un lien (hors widget)
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            sDecoColor = addons.getSetting('deco_color')
            oOutputParameterHandler.addParameter('pasteID', pasteID) # remettre les paramètres lorsqu'on recycle oOutputParameterHandler
            oGui.addDir(SITE_IDENTIFIER, 'addPasteID', '[COLOR %s]Ajouter un code %s[/COLOR]' % (sDecoColor, SITE_NAME), 'notes.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('pasteID', pasteID) # remettre les paramètres lorsqu'on recycle oOutputParameterHandler
            oGui.addDir(SITE_IDENTIFIER, 'adminPasteID', '[COLOR %s]Retirer un code %s[/COLOR]' % (sDecoColor, SITE_NAME), 'trash.png', oOutputParameterHandler)

    elif 'film' in sMedia:
        contenu.discard('containSeries')
        contenu.discard('containAnimes')
        contenu.discard('containDivers')
        showDetailMenu(pasteID, contenu)
    elif 'serie' in sMedia:
        contenu.discard('containFilms')
        contenu.discard('containAnimes')
        contenu.discard('containDivers')
        showDetailMenu(pasteID, contenu)
    elif 'anime' in sMedia:
        contenu.discard('containFilms')
        contenu.discard('containSeries')
        contenu.discard('containDivers')
        showDetailMenu(pasteID, contenu)
    elif 'divers' in sMedia:
        contenu.discard('containFilms')
        contenu.discard('containSeries')
        contenu.discard('containAnimes')
        showDetailMenu(pasteID, contenu)

    oGui.setEndOfDirectory()


def showDetailMenu(pasteID, contenu):
    oGui = cGui()

    sUrl = URL_MAIN + '&numPage=1'  # + pasteBin
    oOutputParameterHandler = cOutputParameterHandler()
    if 'containFilms' in contenu:
        searchUrl = URL_MAIN + '&pasteID=' + pasteID + '&sMedia=film&sSearch='
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&sYear=2023&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Nouveautés)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&bNews=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if 'containFilmGenres' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'genres.png', oOutputParameterHandler)

        if 'containFilmGroupes' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Films (Listes)', 'listes.png', oOutputParameterHandler)

        if 'containFilmSaga' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showSaga', 'Films (Saga)', 'genres.png', oOutputParameterHandler)

        if 'containFilmYear' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Par années)', 'annees.png', oOutputParameterHandler)

        if 'containFilmRes' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showResolution', 'Films (Par résolutions)', 'hd.png', oOutputParameterHandler)

        if 'containFilmNetwork' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Films (Par diffuseurs)', 'host.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Films (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

        if 'containFilmReal' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showRealisateur', 'Films (Par réalisateurs)', 'actor.png', oOutputParameterHandler)

        if 'containFilmCast' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showCast', 'Films (Par acteurs)', 'actor.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&bRandom=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Aléatoires)', 'films.png', oOutputParameterHandler)

    if 'containSeries' in contenu:
        searchUrl = URL_MAIN + '&pasteID=' + pasteID + '&sMedia=serie&sSearch='
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&sYear=2023&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Nouveautés)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&bNews=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if 'containSerieGenres' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

        if 'containSerieGroupes' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Séries (Listes)', 'listes.png', oOutputParameterHandler)

        if 'containSerieNetwork' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

        if 'containSerieYear' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Séries (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&bRandom=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Aléatoires)', 'series.png', oOutputParameterHandler)

    if 'containAnimes' in contenu:
        searchUrl = URL_MAIN + '&pasteID=' + pasteID + '&sMedia=anime&sSearch='
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&bNews=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if 'containAnimeGenres' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Animes (Genres)', 'genres.png', oOutputParameterHandler)

        if 'containAnimeGroupes' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Animes (Listes)', 'listes.png', oOutputParameterHandler)

        if 'containAnimeNetwork' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Animes (Par diffuseurs)', 'host.png', oOutputParameterHandler)

        if 'containAnimeYear' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Animes (Par années)', 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Animes (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    if 'containDivers' in contenu:
        searchUrl = URL_MAIN + '&pasteID=' + pasteID + '&sMedia=divers&sSearch='
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Divers)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Divers (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if 'containDiversGenres' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Divers (Catégories)', 'genres.png', oOutputParameterHandler)

        if 'containDiversGroupes' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Divers (Listes)', 'listes.png', oOutputParameterHandler)

        if 'containDiversYear' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Divers (Par années)', 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Divers (Ordre alphabétique)', 'az.png', oOutputParameterHandler)


# Etablir les menus en fonction du contenu
def getPasteBin(pbContent, pasteBin):

    containList = set()

    if not pasteBin:
        return containList

    movies = pbContent.getLines(pasteBin)

    # pas de liste par résolution si utilisation seule des sources uptostream
    noResList = pbContent.getUptoStream() == 3

    # Calculer les menus
    for movie in movies:
        if pbContent.CAT == -1 or 'film' in movie[pbContent.CAT]:
            containList.add('containFilms')
            if pbContent.GENRES >= 0 and len(movie[pbContent.GENRES].strip()) > 2:
                containList.add('containFilmGenres')
            if pbContent.GROUPES >= 0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containFilmGroupes')
            if pbContent.YEAR >= 0 and len(movie[pbContent.YEAR].strip()) > 1:
                containList.add('containFilmYear')
            if not noResList and pbContent.RES >= 0 and len(movie[pbContent.RES].replace('[', '').replace(']', '').replace(',', '').strip()) > 0:
                containList.add('containFilmRes')
            if pbContent.DIRECTOR >= 0 and len(movie[pbContent.DIRECTOR].replace('[', '').replace(']', '').replace(',', '').strip()) > 0:
                containList.add('containFilmReal')
            if pbContent.CAST >= 0 and len(movie[pbContent.CAST].replace('[', '').replace(']', '').replace(',', '').strip()) > 0:
                containList.add('containFilmCast')
            if pbContent.SAISON >= 0 and len(movie[pbContent.SAISON].strip()) > 0:
                containList.add('containFilmSaga')
            if pbContent.NETWORK >= 0 and len(movie[pbContent.NETWORK].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containFilmNetwork')

        elif 'serie' in movie[pbContent.CAT]:
            containList.add('containSeries')
            if pbContent.GENRES >= 0 and len(movie[pbContent.GENRES].strip()) > 2:
                containList.add('containSerieGenres')
            if pbContent.GROUPES >= 0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containSerieGroupes')
            if pbContent.NETWORK >=0 and len(movie[pbContent.NETWORK].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containSerieNetwork')
            if pbContent.YEAR >= 0 and len(movie[pbContent.YEAR].strip()) > 1:
                containList.add('containSerieYear')

        elif 'anime' in movie[pbContent.CAT]:
            containList.add('containAnimes')
            if pbContent.GENRES >= 0 and len(movie[pbContent.GENRES].strip()) > 2:
                containList.add('containAnimeGenres')
            if pbContent.GROUPES >= 0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containAnimeGroupes')
            if pbContent.NETWORK >=0 and len(movie[pbContent.NETWORK].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containAnimeNetwork')
            if pbContent.YEAR >= 0 and len(movie[pbContent.YEAR].strip()) > 1:
                containList.add('containAnimeYear')

        elif 'divers' in movie[pbContent.CAT]:
            containList.add('containDivers')
            if pbContent.GENRES >= 0 and len(movie[pbContent.GENRES].strip()) > 2:
                containList.add('containDiversGenres')
            if pbContent.YEAR >= 0 and len(movie[pbContent.YEAR].strip()) > 1:
                containList.add('containDiversYear')
            if pbContent.GROUPES >= 0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip()) > 0:
                containList.add('containDiversGroupes')
    return containList


def showMenuFilms():
    oGui = cGui()
    addons = addon()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sRes = 'sRes=' in sUrl
    if sRes:
        oGui.addText(SITE_IDENTIFIER, sLabel='[COLOR red]## Résolution %s ##[/COLOR]' % (sUrl.split('sRes=')[1]), sIcon='hd.png')

    oOutputParameterHandler = cOutputParameterHandler()

    # oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sSearch=')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&bNews=True')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    if not sRes:
        oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
        oGui.addDir(SITE_IDENTIFIER, 'showTMDB', addons.VSlang(30426), 'news.png', oOutputParameterHandler)
        # oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&sYear=2023')
        # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Nouveautés)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'movie/popular')
        oGui.addDir(SITE_IDENTIFIER, 'showTMDB', addons.VSlang(30425), 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Films (Listes)', 'listes.png', oOutputParameterHandler)

    if not sRes:
        oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
        oGui.addDir(SITE_IDENTIFIER, 'showGenreMovieTMDB', addons.VSlang(30428), 'genres.png', oOutputParameterHandler)
    else:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', addons.VSlang(30428), 'genres.png', oOutputParameterHandler)

    if not sRes:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSaga', 'Films (Saga)', 'genres.png', oOutputParameterHandler)

    if not sRes:
        oOutputParameterHandler.addParameter('siteUrl', 'movie/top_rated')
        oGui.addDir(SITE_IDENTIFIER, 'showTMDB', addons.VSlang(30427), 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    if not sRes:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showResolution', 'Films (Par résolutions)', 'hd.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
    # oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Films (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Films (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    if not sRes:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showRealisateur', 'Films (Par réalisateurs)', 'actor.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showCast', 'Films (Par acteurs)', 'actor.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&bRandom=True')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Aléatoires)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()
    addons = addon()
    sUrl = URL_MAIN + '&sMedia=serie&numPage=1'

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&bNews=True')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sYear=2023')
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Nouveautés)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'trending/tv/day')#tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showTMDB', addons.VSlang(30430), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showTMDB', addons.VSlang(30429), 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Séries (Listes)', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreTV', addons.VSlang(30432), 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', sUrl)
    # oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', 'tv/top_rated')
    # oGui.addDir(SITE_IDENTIFIER, 'showTMDB', addons.VSlang(30431), 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Séries (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&bRandom=True')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Aléatoires)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()
    sUrl = URL_MAIN + '&sMedia=anime&numPage=1'

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&bNews=True')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sYear=2023')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes (Nouveautés)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Animes (Listes)', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Animes (Par diffuseurs)', 'host.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Animes (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Animes (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl + '&bRandom=True')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes (Aléatoires)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMisc():
    oGui = cGui()
    sUrl = URL_MAIN + '&sMedia=divers&numPage=1'

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Divers)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Divers (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', sUrl)
    # oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Divers (Catégories)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Divers (Listes)', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'alphaList', 'Divers (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuFolder():
    from resources.lib.gui.guiElement import cGuiElement
    oGui = cGui()
    addons = addon()

    # Recherche des listes déclarées
    pasteListe = {}
    numID = 0
    for numID in range(1, 50):
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel:
            pasteListe[pasteLabel] = numID

    # Trie des dossiers par label
    pasteListe = sorted(pasteListe.items(), key=lambda paste: paste[0])

    oOutputParameterHandler = cOutputParameterHandler()
    for pasteBin in pasteListe:
        pasteLabel = pasteBin[0]
        pasteID = pasteBin[1]

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showMenu')
        oGuiElement.setTitle(pasteLabel)
        oGuiElement.setIcon("mark.png")
        oGuiElement.setMeta(0)

        oOutputParameterHandler.addParameter('pasteID', pasteID)
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'renamePasteName', addons.VSlang(30223))
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'deletePasteName', addons.VSlang(30412))
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # Menus non visibles en widget
    if not xbmc.getCondVisibility('Window.IsActive(home)'):
        sDecoColor = addons.getSetting('deco_color')

        # Menu pour ajouter un dossier
        oGui.addDir(SITE_IDENTIFIER, 'addPasteName', '[COLOR %s]Ajouter un dossier[/COLOR]' % sDecoColor, 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# films par genre selon TMDB
def showGenreMovieTMDB():
    from resources.lib.tmdb import cTMDb
    grab = cTMDb()
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        bMatrix = isMatrix()
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            if not bMatrix:
                sTitle = sTitle.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showTMDB', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# films par genre dans le paste, permet des filtres par résolution par exemple
def showGenreMovie():
    from resources.lib.tmdb import cTMDb
    grab = cTMDb()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl('genre/movie/list')
    if len(result) > 0:
        bMatrix = isMatrix()
        oOutputParameterHandler = cOutputParameterHandler()
        for genre in result['genres']:
            sId, sTitle = str(genre['id']), genre['name']
            if not bMatrix:
                sTitle = sTitle.encode("utf-8")
            oOutputParameterHandler.addParameter('siteUrl', siteUrl + '&sGenre=' + sId)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenreTV():
    from resources.lib.tmdb import cTMDb
    grab = cTMDb()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    if len(result) > 0:
        bMatrix = isMatrix()
        siteUrl = URL_MAIN + '&numPage=1&sMedia=serie'
        oOutputParameterHandler = cOutputParameterHandler()
        for genre in result['genres']:
            sId, sTitle = str(genre['id']), genre['name']
            if not bMatrix:
                sTitle = sTitle.encode("utf-8")
            oOutputParameterHandler.addParameter('siteUrl', siteUrl + '&sGenre=' + sId)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTMDB():
    from resources.lib.tmdb import cTMDb
    grab = cTMDb()
    oGui = cGui()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numPage:
        numPage = 1
    numPage = int(numPage)

    term = ''

    result = grab.getUrl(siteUrl, numPage, term)
    total = len(result)
    results = None
    if total > 0:
        if 'cast' in result:
            sMedia = 'film'
            sType = 'person'
            results = result['cast']
        elif 'results' in result:
            sMedia = 'film' if 'movie' in siteUrl else 'serie'
            sType = 'movie' if 'movie' in siteUrl else 'tvshow'
            results = result['results']
        total = len(results)

    if total > 0 and results:
        bMatrix = isMatrix()
        tmdbIds = {}
        for data in results:
            tmdbIds[data['id']] = data['title'] if 'title' in data else data['name']

        pbContent = PasteContent()
        movies = []
        for numID in range(1, GROUPE_MAX):
            prefixID = SETTING_PASTE_LABEL + str(numID)
            pastebin = addons.getSetting(prefixID)
            if pastebin:
                listeIDs = getPasteList(numID)
                for pasteBin in listeIDs:
                    moviesBin = pbContent.getLines(pasteBin, sMedia)
                    nbMovies = len(moviesBin)
                    if nbMovies > 0:
                        movies += moviesBin

        # filmographie triée par date
        if sType == 'person':
            if pbContent.YEAR >= 0:
                movies = sorted(movies, key=lambda line: line[pbContent.YEAR], reverse=True)

        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for movie in movies:
            # l'ID TMDB
            sTmdbId = None
            if pbContent.TMDB == -1:
                continue
            sTmdbId = movie[pbContent.TMDB].strip()
            if not sTmdbId:
                continue

            sTitle = tmdbIds.pop(int(sTmdbId), None)
            if not sTitle:
                continue

            if not bMatrix:
                sTitle = sTitle.encode("utf-8")

            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN
            if sMedia:
                sUrl += '&sMedia=' + sMedia
            if sTmdbId:
                sUrl += '&idTMDB=' + sTmdbId
            sUrl += '&sTitle=' + sTitle
            sDisplayTitle = sTitle

            # Pour supporter les caractères '&' et '+' dans les noms alors qu'ils sont réservés
            sTitle = sTitle.replace('+', ' ').replace(' & ', ' | ')
            sTitle = sTitle.replace('[', '').replace(']', '')   # Exemple pour le film [REC], les crochets sont génants pour certaines fonctions

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if sTmdbId:
                oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)  # Utilisé par TMDB

            if sMedia == 'serie':
                oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
            elif sMedia == 'anime':
                oGui.addAnime(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'animes.png', '', '', oOutputParameterHandler)
            elif sMedia == 'divers':
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'doc.png', '', '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

            if len(tmdbIds) == 0:
                break

        progress_.VSclose(progress_)

        if sType != 'person':
            numPage += 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oGui.addNext(SITE_IDENTIFIER, 'showTMDB', 'Page ' + str(numPage), oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    from resources.lib.util import Quote
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl += Quote(sSearchText)

        showMovies(sUrl)
        oGui.setEndOfDirectory()


def showSearchActor():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if not sSearchText:
        return

    showActors(sSearchText.replace(' ', '+'))


def showActors(sSearch=''):
    from resources.lib.tmdb import cTMDb
    grab = cTMDb()
    oGui = cGui()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        # format obligatoire évite de modif le format de l'url dans la lib >> _call
        # a cause d'un ? pas ou il faut pour ça >> invalid api key
        result = grab.getUrl(sUrl, iPage, 'query=' + sSearch)

    else:
        result = grab.getUrl(sUrl, iPage)

    total = len(result)

    if total > 0:
        total = len(result['results'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        # récup le nombre de page pour NextPage
        nbrpage = result['total_pages']

        for i in result['results']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sName, sThumb = i['name'], i['profile_path']

            if sThumb:
                POSTER_URL = grab.poster
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''

            if not isMatrix():
                sName = sName.encode('utf-8')

            sTitle = str(sName)
            actorId = str(i['id'])
            oOutputParameterHandler.addParameter('siteUrl', 'person/' + actorId + '/movie_credits')
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', actorId)    # Utilisé par TMDB
            oGui.addPerson(SITE_IDENTIFIER, 'showTMDB', sTitle, 'actor.png', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if int(iPage) < int(nbrpage):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)

            # ajoute param sSearch pour garder le bon format d'url avec grab url
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)

            oGui.addNext(SITE_IDENTIFIER, 'showActors', 'Page ' + str(iNextPage), oOutputParameterHandler)

    view = addons.getSetting('visuel-view')

    oGui.setEndOfDirectory(view)


def showGenres():
    from resources.lib.tmdb import cTMDb
    tmdb = cTMDb()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    listeIDs = getPasteList(pasteID)

    genres = {}
    pbContent = PasteContent()
    for pasteBin in listeIDs:

        movies = pbContent.getLines(pasteBin, sMedia)

        for movie in movies:
            try:
                if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                    continue

                genre = movie[pbContent.GENRES].strip()
                if not genre or genre == '':
                    genre = "['" + UNCLASSIFIED_GENRE + "']"
                elif "''" in genre:
                    genre = genre.replace("''", "'" + UNCLASSIFIED_GENRE + "'")
                genre = eval(genre)
                if isinstance(genre, int):
                    genre = [genre]
                if genre:
                    for g in genre:
                        sDisplayGenre = g
                        if str(g).isdigit():
                            sDisplayGenre = tmdb.getGenreFromID(g)
                        if sDisplayGenre not in genres:
                            genres[sDisplayGenre] = g
            except Exception as e:
                VSlog('Error in paste : ' + pasteBin)
                VSlog('Error in media : ' + ';'.join(movie))
                VSlog('Error : ' + str(e))

    genreKeys = genres.keys()
    oOutputParameterHandler = cOutputParameterHandler()
    for sDisplayGenre in sorted(genreKeys):
        genre = genres.get(sDisplayGenre)
        sUrl = siteUrl + '&sGenre=' + str(genre)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showNetwork():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'serie'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteContent()
    listNetwork = {}
    listeIDs = getPasteList(pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin, sMedia)
        for movie in movies:
            if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                continue

            networks = movie[pbContent.NETWORK].strip()
            if networks != '' and networks != '[]':
                networks = eval(networks)
                if networks:
                    for network in networks:
                        if ':' in network:
                            networkId, networkName = network.split(':')
                            if networkName not in listNetwork:
                                listNetwork[networkName] = networkId

    maxProgress = len(listNetwork)
    progress_ = progress().VScreate(SITE_NAME)

    oOutputParameterHandler = cOutputParameterHandler()
    for networkName, networkId in sorted(listNetwork.items()):
        progress_.VSupdate(progress_, maxProgress)
        if progress_.iscanceled():
            break

        sUrl = siteUrl + '&sNetwork=' + networkId + ":" + networkName.replace('+', '|')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', networkId)    # Utilisé par TMDB
        oGui.addNetwork(SITE_IDENTIFIER, 'showMovies', networkName, 'host.png', oOutputParameterHandler)
    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showRealisateur():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')

    # Gestion de la pagination
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    pbContent = PasteContent()
    listReal = {}
    listeIDs = getPasteList(pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin, sMedia)
        for movie in movies:
            if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                continue

            reals = movie[pbContent.DIRECTOR].strip()
            if reals != '':
                reals = eval(reals)
                if reals:
                    for real in reals:
                        if ':' in real:
                            realId, realName = real.split(':')
                            if realName not in listReal:
                                listReal[realName] = realId

    nbItem = 0
    index = 0
    maxProgress = min(len(listReal), ITEM_PAR_PAGE)
    progress_ = progress().VScreate(SITE_NAME)

    oOutputParameterHandler = cOutputParameterHandler()
    for realName, realId in sorted(listReal.items()):
        # Pagination, on se repositionne
        index += 1
        if index <= numItem:
            continue
        numItem += 1

        progress_.VSupdate(progress_, maxProgress)
        if progress_.iscanceled():
            break

        sUrl = siteUrl + '&sDirector=' + realId + ":" + realName
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', realId)    # Utilisé par TMDB
        oGui.addPerson(SITE_IDENTIFIER, 'showMovies', realName, 'actor.png', '', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(listReal):
            numPage += 1

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oOutputParameterHandler.addParameter('numItem', numItem)
            oGui.addNext(SITE_IDENTIFIER, 'showRealisateur', 'Page ' + str(numPage), oOutputParameterHandler)
            break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showCast():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    if not numPage and 'numPage' in aParams:
        numPage = aParams['numPage']

    pbContent = PasteContent()
    listActeur = {}
    listeIDs = getPasteList(pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin, sMedia)
        for movie in movies:
            if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                continue

            acteurs = movie[pbContent.CAST].strip()
            if acteurs != '':
                acteurs = eval(acteurs)
                if acteurs:
                    for acteur in acteurs:
                        if ':' in acteur:
                            acteurId, acteurName = acteur.split(':')
                            if acteurName not in listActeur:
                                listActeur[acteurName] = acteurId

    # Gestion de la pagination
    if not numItem:
        numItem = 0
    else:
        numItem = int(numItem)
    numPage = int(numPage)
    if numPage > 1 and numItem == 0:  # choix d'une page
        numItem = (numPage-1) * ITEM_PAR_PAGE
        if numItem > len(listActeur):   # accès direct à la dernière page
            numPage = len(listActeur) / ITEM_PAR_PAGE
            numItem = (numPage-1) * ITEM_PAR_PAGE

    nbItem = 0
    index = 0
    maxProgress = min(len(listActeur), ITEM_PAR_PAGE)
    progress_ = progress().VScreate(SITE_NAME)

    oOutputParameterHandler = cOutputParameterHandler()
    for acteurName, acteurId in sorted(listActeur.items()):
        # Pagination, on se repositionne
        index += 1
        if index <= numItem:
            continue
        numItem += 1

        progress_.VSupdate(progress_, maxProgress)
        if progress_.iscanceled():
            break

        sUrl = siteUrl + '&sCast=' + acteurId + ":" + acteurName
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', acteurId)    # Utilisé par TMDB
        oGui.addPerson(SITE_IDENTIFIER, 'showMovies', acteurName, 'actor.png', '', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(listActeur):
            numPage += 1

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oOutputParameterHandler.addParameter('numItem', numItem)
            oGui.addNext(SITE_IDENTIFIER, 'showCast', 'Page ' + str(numPage), oOutputParameterHandler)
            break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showGroupes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteContent()
    sousGroupe = set()
    groupesPerso = set()
    listeIDs = getPasteList(pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin, sMedia)

        for movie in movies:
            try:
                if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                    continue
                groupe = movie[pbContent.GROUPES].strip().replace("''", '')
                if groupe:
                    groupe = eval(groupe)
                    if groupe:
                        for gr in groupe:
                            if ':' in gr:
                                grID = gr.split(':')[0]
                                sousGroupe.add(grID)
                            else:
                                groupesPerso.add(gr)
            except Exception as e:
                VSlog('Error in paste : ' + pasteBin)
                VSlog('Error in media : ' + ';'.join(movie))
                VSlog('Error : ' + str(e))

    groupes = groupesPerso.union(sousGroupe)
    oOutputParameterHandler = cOutputParameterHandler()
    for sGroupe in sorted(groupes):
        sUrl = siteUrl + '&sGroupe=' + sGroupe
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        if sGroupe in sousGroupe:
            oGui.addDir(SITE_IDENTIFIER, 'showGroupeDetails', sGroupe, 'genres.png', oOutputParameterHandler)
        else:
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sGroupe, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGroupeDetails():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    sGroupe = aParams['sGroupe'].replace('+', ' ') + ':' if 'sGroupe' in aParams else None
    sMedia = aParams['sMedia']

    pbContent = PasteContent()
    groupes = set()

    if sGroupe:
        listeIDs = getPasteList(pasteID)
        for pasteBin in listeIDs:
            movies = pbContent.getLines(pasteBin, sMedia)
            for movie in movies:
                try:
                    groupe = movie[pbContent.GROUPES].strip().replace("''", '')
                    if groupe:
                        groupe = eval(groupe)
                        if groupe:
                            for gr in groupe:
                                if gr.startswith(sGroupe):
                                    groupes.add(gr)
                except Exception as e:
                    pass

    oOutputParameterHandler = cOutputParameterHandler()
    for sGroupe in sorted(groupes):
        sUrl = siteUrl + '&sGroupe=' + sGroupe.replace('+', '|')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        sDisplayGroupe = sGroupe.split(':')[1]
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayGroupe, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSaga():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    if not numPage and 'numPage' in aParams:
        numPage = aParams['numPage']

    pbContent = PasteContent()
    sagas = {}
    listeIDs = getPasteList(pasteID)

    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin, sMedia)
        for movie in movies:
            if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                continue

            saga = movie[pbContent.SAISON].strip()
            if saga != '':
                sTmdbId = name = saga
                idName = saga.split(':', 1)
                if len(idName) > 1:
                    sTmdbId = idName[0]
                    name = idName[1]
                if sTmdbId.isdigit():
                    sagas[name] = sTmdbId
                else:
                    sagas[saga] = saga

    # Gestion de la pagination
    if not numItem:
        numItem = 0
    else:
        numItem = int(numItem)
    numPage = int(numPage)
    if numPage > 1 and numItem == 0:  # choix d'une page
        numItem = (numPage-1) * ITEM_PAR_PAGE
        if numItem > len(sagas):   # accès direct à la dernière page
            numPage = len(sagas) / ITEM_PAR_PAGE
            numItem = (numPage-1) * ITEM_PAR_PAGE

    nbItem = 0
    index = 0
    progress_ = progress().VScreate(SITE_NAME)
    names = sagas.keys()
    oOutputParameterHandler = cOutputParameterHandler()
    for sSagaName in sorted(names):

        # Pagination, on se repositionne
        index += 1
        if index <= numItem:
            continue
        numItem += 1

        progress_.VSupdate(progress_, ITEM_PAR_PAGE)
        if progress_.iscanceled():
            break

        sTmdbId = sagas[sSagaName]

        if sTmdbId.isdigit():
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)  # Utilisé par TMDB
            sUrl = siteUrl + '&sSaga=' + sTmdbId + ':' + sSagaName
        else:
            oOutputParameterHandler.addParameter('sTmdbId', '')
            sUrl = siteUrl + '&sSaga=' + sSagaName
        oOutputParameterHandler.addParameter('siteUrl', sUrl)

        sDisplaySaga = sSagaName
        sSagaName = sSagaName.replace('[', '').replace(']', '')  # Exemple pour le film [REC], les crochets sont génant pour certaines fonctions
        oOutputParameterHandler.addParameter('sMovieTitle', sSagaName)

        oGui.addMoviePack(SITE_IDENTIFIER, 'showMovies', sDisplaySaga, 'genres.png', '', '', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(names):
            numPage += 1

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oOutputParameterHandler.addParameter('numItem', numItem)
            oGui.addNext(SITE_IDENTIFIER, 'showSaga', 'Page ' + str(numPage), oOutputParameterHandler)
            break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteContent()
    years = set()
    listeIDs = getPasteList(pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin, sMedia)
        for line in movies:
            if pbContent.CAT >= 0 and sMedia not in line[pbContent.CAT]:
                continue

            year = line[pbContent.YEAR].strip()
            if not year:
                year = UNCLASSIFIED
            years.add(year)

    oOutputParameterHandler = cOutputParameterHandler()
    for sYear in sorted(years, reverse=True):
        sUrl = siteUrl + '&sYear=' + sYear
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Trie des résolutions
resOrder = ['8K', '2160P', '4K', '1080P', 'fullHD', '720P', 'HD', 'SD', '576P', '540P', '480P', '360P', '']


def trie_res(key):
    if key == UNCLASSIFIED:
        return 100  # En dernier
    key = key.replace('p', 'P')

    if key in resOrder:
        return resOrder.index(key)

    for res in resOrder:
        if key.find(res) >= 0:
            idx = resOrder.index(res)+1
            resOrder.insert(idx, key)
            return idx
        if res.find(key) >= 0:
            idx = resOrder.index(res)+1
            resOrder.insert(idx, key)
            return idx

    resOrder.append(key)
    return len(resOrder)-1


def showResolution():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    oOutputParameterHandler = cOutputParameterHandler()
    resolutions = [('DOLBY VISION', 'DOLBY VISION'), ('4K', '4K [2160p]'), ('1080P', 'fullHD [1080p]'), ('720P', 'HD [720p]'), ('SD', 'SD'), ('3D', '3D')]
    for sRes, sDisplayRes in resolutions:
        sUrl = siteUrl + '&sRes=' + sRes
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', sDisplayRes, 'hd.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def alphaList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    oOutputParameterHandler = cOutputParameterHandler()
    for i in range(48, 84):
        sLetter = chr(i+7 if i > 57 else i)
        oOutputParameterHandler.addParameter('siteUrl', siteUrl + '&sAlpha=' + sLetter)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] Lettre [COLOR red]' + sLetter + '[/COLOR][/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    sMedia = 'film'  # Par défaut
    pasteID = sGenre = sSaga = sGroupe = sYear = sRes = sAlpha = sNetwork = sDirector = sCast = None
    bSilent = bRandom = bNews = False

    if sSearch:
        siteUrl = sSearch

    sSearchTitle = ''

    # Pour supporter les caractères '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')

    sUrl, params = sUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))

    if 'pasteID' in aParams:
        pasteID = aParams['pasteID']
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    if 'sSearch' in aParams:
        sSearchTitle = Unquote(aParams['sSearch']).replace(' | ', ' & ')
    if 'sGenre' in aParams:
        sGenre = aParams['sGenre'].replace(' | ', ' & ')
    if 'sSaga' in aParams:
        sSaga = aParams['sSaga'].replace(' | ', ' & ')
    if 'sGroupe' in aParams:
        sGroupe = "'" + aParams['sGroupe'].replace(' | ', ' & ') + "'"
    if 'sYear' in aParams:
        sYear = aParams['sYear']
    if 'sRes' in aParams:
        sRes = aParams['sRes'].upper()
    if 'sAlpha' in aParams:
        sAlpha = aParams['sAlpha']
    if 'sNetwork' in aParams:
        sNetwork = aParams['sNetwork']
    if 'sDirector' in aParams:
        sDirector = aParams['sDirector']
    if 'sCast' in aParams:
        sCast = aParams['sCast']
    if 'bRandom' in aParams:
        bRandom = aParams['bRandom']
    if 'bNews' in aParams:
        bNews = aParams['bNews']
    if 'bSilent' in aParams:
        bSilent = aParams['bSilent']
    if not numPage and 'numPage' in aParams:
        numPage = aParams['numPage']

    if sSearchTitle:
        oUtil = cUtil()
        sSearchTitle = oUtil.CleanName(sSearchTitle)

    if bRandom:
        numItem = 0
    else:
        numItem = int(numItem) if numItem else 0

    pbContent = PasteContent()
    movies = []
    pasteLen = []
    pasteMaxLen = []
    maxlen = 0

    listeIDs = getPasteList(pasteID)

    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin, sMedia)
        nbMovies = len(moviesBin)
        if nbMovies > 0:
            movies += moviesBin
            pasteLen.append(nbMovies)
            maxlen += nbMovies
            pasteMaxLen.append(maxlen)

    # si plusieurs pastes, on les parcourt en parallèle
    if (bNews or sRes or sNetwork) and len(listeIDs) > 1:
        listName = set()
        moviesNews = []
        i = j = k = 0
        lenMovies = len(movies)
        if bNews and not sRes:   # Si pas de tris, pas besoin de récupérer plus qu'on ne peut en afficher
            nbMoviesNewsMax = min(lenMovies, numItem + ITEM_PAR_PAGE + 1)
            nbMoviesNews = 0

        while k < lenMovies:
            if i < pasteMaxLen[j]:
                # Filtrage par média (film/série)
                if pbContent.CAT >=0 and sMedia in movies[i][pbContent.CAT]:
                    if bNews and not sRes:
                        movieName = movies[i][pbContent.TITLE]
                        if movieName not in listName:  # trie des séries en doublons (à cause des saisons)
                            listName.add(movieName)
                            moviesNews.append(movies[i])
                            nbMoviesNews += 1
                            if nbMoviesNews == nbMoviesNewsMax:
                                break
                    else:
                        moviesNews.append(movies[i])
                k += 1
            i += pasteLen[j]
            j += 1
            if j >= len(pasteMaxLen):
                i = (i % lenMovies) + 1
                j = 0

        movies = moviesNews

    # Classement par ID TMDB, pseudo-classement par sortie
    if sYear or sGenre:
        try:
            movies = sorted(movies, key=lambda line: int(line[pbContent.TMDB]) if line[pbContent.TMDB] else 0, reverse=True)
        except Exception as e:
            raise
            
    # Recherche par ordre alphabétique => le tableau doit être trié
    if sAlpha:
        movies = sorted(movies, key=lambda line: line[pbContent.TITLE])

    # Recherche par saga => trie par années
    if sSaga and pbContent.YEAR >= 0:
        movies = sorted(movies, key=lambda line: line[pbContent.YEAR])

    # Dans un dossier => trie par années inversées (du plus récent)
    if sGroupe or sDirector or sCast:
        movies = sorted(movies, key=lambda line: line[pbContent.YEAR], reverse=True)

    # Gestion de la pagination
    numPage = int(numPage)
    if numPage > 1 and numItem == 0:  # choix d'une page
        numItem = (numPage-1) * ITEM_PAR_PAGE
        if numItem > len(movies):   # accès direct à la dernière page
            numPage = len(movies) / ITEM_PAR_PAGE
            numItem = (numPage-1) * ITEM_PAR_PAGE

    if bRandom:
        # Génération d'indices aléatoires, ajout d'une marge car les doublons aléatoires sont rassemblés
        randoms = [random.randint(0, len(movies)) for _ in range(ITEM_PAR_PAGE*2)]

    movieIds = set()

    nbItem = 0
    index = 0

    if not bSilent:
        progress_ = progress().VScreate(SITE_NAME)
    oOutputParameterHandler = cOutputParameterHandler()

    if sRes:
        oGui.addText(SITE_IDENTIFIER, sLabel='[COLOR red]## Résolution %s ##[/COLOR]' % sRes, sIcon='hd.png')

    for movie in movies:

        if bRandom and index not in randoms:
            index += 1
            continue

        # Pagination, on se repositionne
        index += 1
        if index <= numItem:
            continue
        numItem += 1

        # Filtrage par média (film/série), "film" par défaut si pas précisé
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        # Filtrage par liste
        if sGroupe and pbContent.GROUPES >= 0:
            groupes = movie[pbContent.GROUPES].strip()
            if not groupes or groupes == '[]':
                continue
            # groupes = eval(groupes)
            groupes = groupes.replace('"', "'")
            if sGroupe not in groupes:
                continue

        # Filtrage par saga
        if sSaga and sSaga != movie[pbContent.SAISON].strip():
            continue

        # Filtrage par genre
        if sGenre and pbContent.GENRES >= 0:
            genres = movie[pbContent.GENRES].strip()
            if not genres or genres == '' or "''" in genres:
                if sGenre != UNCLASSIFIED_GENRE:
                    continue
            elif genres:
                genres = eval(genres)
                genres = [str(g) for g in genres]
                if sGenre not in genres:
                    continue

        # Filtrage par réalisateur
        if sDirector and pbContent.DIRECTOR >= 0:
            listDirector = movie[pbContent.DIRECTOR].strip()
            if not listDirector:
                continue
            listDirector = eval(listDirector)
            if sDirector not in listDirector:
                continue

        # Filtrage par acteur
        if sCast and pbContent.CAST >= 0:
            listCast = movie[pbContent.CAST].strip()
            if not listCast:
                continue
            listCast = eval(listCast)
            if sCast not in listCast:
                continue

        # Filtrage par diffuseur
        if sNetwork and pbContent.NETWORK >= 0:
            listNetwork = movie[pbContent.NETWORK].strip()
            if not listNetwork:
                continue
            # listNetwork = eval(listNetwork)
            if sNetwork not in listNetwork:
                continue

        # Filtrage par titre
        sTitle = movie[pbContent.TITLE].strip()

        # l'ID TMDB
        sTmdbId = None
        if pbContent.TMDB >= 0:
            sTmdbId = movie[pbContent.TMDB].strip()
            if sTmdbId:
                if sTmdbId in movieIds:
                    continue  # Filtre des doublons
                movieIds.add(sTmdbId)
        if not sTmdbId:
            if sTitle in movieIds:
                continue  # Filtre des doublons
            movieIds.add(sTitle)

        # Titre recherché
        if sSearchTitle:
            if not oUtil.CheckOccurence(sSearchTitle, sTitle):
                continue

        # Recherche alphabétique
        if sAlpha:
            if sTitle[0].upper() != sAlpha:
                continue

        sDisplayTitle = sTitle

        # Filtrage par années
        movieYear = ''
        if pbContent.YEAR >= 0:
            movieYear = movie[pbContent.YEAR].strip()
            # sDisplayTitle = '%s (%s)' % (sTitle, movieYear)
        if sYear:
            if sYear == UNCLASSIFIED:
                if movieYear != '':
                    continue
            elif not movieYear or sYear != movieYear:
                continue

        # Filtrage par résolutions vidéos
        listRes = None

        if 'film' in sMedia:
            if pbContent.RES >= 0:
                res = movie[pbContent.RES].strip().upper()
                listRes = []
                if '[' in res:
                    listRes.extend(eval(res))
                else:
                    listRes.append(res)
                if len(listRes) == 0:
                    listRes.append('')

            if sRes:
                if sRes == UNCLASSIFIED:
                    if '' not in listRes:
                        continue

                bValid = False
                for res in listRes:
                    if sRes in res:
                        bValid = True
                        break

                if not bValid:
                    continue

        nbItem += 1
        if not bSilent:
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

        sUrl = URL_MAIN
        if sMedia:
            sUrl += '&sMedia=' + sMedia
        if pasteID:
            sUrl += '&pasteID=' + pasteID
        if movieYear:
            sUrl += '&sYear=' + movieYear
        if sTmdbId:
            sUrl += '&idTMDB=' + sTmdbId
        if sRes:
            sUrl += '&sRes=' + sRes
        sUrl += '&sTitle=' + sTitle

        # Pour supporter les caractères '&' et '+' dans les noms alors qu'ils sont réservés
        sTitle = sTitle.replace('+', ' ').replace(' & ', ' | ')
        sTitle = sTitle.replace('[', '').replace(']', '')   # Exemple pour le film [REC], les crochets sont génants pour certaines fonctions

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        if sTmdbId:
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)  # Utilisé par TMDB
        if movieYear:
            oOutputParameterHandler.addParameter('sYear', movieYear)  # Utilisé par TMDB
        if listRes:
            oOutputParameterHandler.addParameter('listRes', listRes)

        if sMedia == 'serie':
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        elif sMedia == 'anime':
            oGui.addAnime(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'animes.png', '', '', oOutputParameterHandler)
        elif sMedia == 'divers':
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'doc.png', '', '', oOutputParameterHandler)
        else:
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(movies):
            if not sSearchTitle:
                numPage += 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('numPage', numPage)
                oOutputParameterHandler.addParameter('numItem', numItem)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(numPage), oOutputParameterHandler)
            break

    if not bSilent:
        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()


def showSerieSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    searchTitle = oInputParameterHandler.getValue('sMovieTitle')
    searchYear = oInputParameterHandler.getValue('sYear')

    # Pour supporter les caractères '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')

    sUrl, params = sUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'serie'

    saisons = {}
    listeIDs = getPasteList(pasteID)
    pbContent = PasteContent()
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin, sMedia)

        # Recherche les saisons de la série
        for serie in moviesBin:

            if pbContent.CAT >= 0 and sMedia not in serie[pbContent.CAT]:
                continue

            # Recherche par id
            found = False
            if idTMDB and pbContent.TMDB >= 0:
                sMovieID = serie[pbContent.TMDB].strip()
                if sMovieID:
                    if sMovieID != idTMDB:
                        continue
                    found = True

            # Sinon, recherche par titre/année
            if not found:
                if searchYear and pbContent.YEAR >= 0:
                    sYear = serie[pbContent.YEAR].strip()
                    if sYear and sYear != searchYear:
                        continue

                sTitle = serie[pbContent.TITLE].strip()
                if sTitle != searchTitle:
                    continue

            numSaison = serie[pbContent.SAISON].strip()
            
            if numSaison.isdigit():
                numSaison = '%02d' % int(numSaison)
            if numSaison not in saisons:
                saisons[numSaison] = set()

            # on ne gère pas les résolutions pour uptostream
            if pbContent.getUptoStream() == 3:
                continue

            # Résolutions disponible pour la saison
            listRes = saisons[numSaison]
            if pbContent.RES >= 0:
                res = serie[pbContent.RES].strip()
                if '[' in res:
                    for r in eval(res):
                        listRes.add(r)
                else:
                    listRes.add(res)


    # Proposer les différentes saisons
    oOutputParameterHandler = cOutputParameterHandler()
    saisons = sorted(saisons.items(), key=lambda saison: saison[0])
    for sSaison, res in saisons:

        sDisplaySaison = sSaison
        if sSaison.isdigit():
            sDisplaySaison = 'S{:02d}'.format(int(sSaison))
            sDisplayTitle = searchTitle + ' - ' + sDisplaySaison
        else:
            sDisplaySaison = sDisplaySaison.replace('Episodes ', '').replace('(', '').replace(')', '')
            sDisplayTitle = '[' + sDisplaySaison + ']' + ' - ' + searchTitle
        sUrl = siteUrl + '&sSaison=' + sSaison
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas sTitre afin de pouvoir mettre la saison en marque-page
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodesLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodesLinks(siteUrl=''):
    oGui = cGui()

    if not siteUrl:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')

    # Pour supporter les caractères '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')
    params = sUrl.split('&', 1)[1]
    aParams = dict(param.split('=') for param in params.split('&'))
    sSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchTitle = aParams['sTitle'].replace(' | ', ' & ')

    if not sSaison:
        oGui.setEndOfDirectory()
        return

    lines = getHosterList(siteUrl)

    listeEpisodes = set()
    for episode in lines:
        for numEpisode in episode.keys():
            numEpisode = str(numEpisode).replace('E', '')
            numEpisode = int(numEpisode)
            if numEpisode not in listeEpisodes:
                listeEpisodes.add(numEpisode)

    sDisplaySaison = sSaison
    if sSaison.isdigit():
        sDisplaySaison = 'S{:02d}'.format(int(sSaison))
    elif 'P' in sDisplaySaison:
        sDisplaySaison = ''

    oOutputParameterHandler = cOutputParameterHandler()
    for episode in sorted(listeEpisodes):
        sUrl = siteUrl + '&sEpisode=' + str(episode)

        if str(episode).isdigit():
            episode = '{}E{:02d}'.format(sDisplaySaison, int(episode))
        else:
            episode = '{}{}'.format(sDisplaySaison, episode)
        sDisplayTitle = searchTitle + ' - ' + episode

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    from resources.lib.gui.hoster import cHosterGui
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle').replace(' | ', ' & ')
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    listRes = getHosterList(siteUrl)

    oOutputParameterHandler = cOutputParameterHandler()

    # Pre-trie pour insérer les résolutions inconnues, puis refaire un deuxième trie
    sorted(listRes.keys(), key=trie_res)
    for res in sorted(listRes.keys(), key=trie_res):
        for sHosterUrl, lang in listRes[res]:
            sUrl = sHosterUrl
    
            sDisplayName = sTitle
            if res:
                oOutputParameterHandler.addParameter('sRes', res)
                displayRes = res.replace('P', 'p').replace('1080p', 'fullHD').replace('720p', 'HD').replace('2160p', '4K').replace('WEB', 'HD')
                sDisplayName += ' [%s]' % displayRes
            if lang:
                sDisplayName += ' (%s)' % lang
    
            link, paste, movies = sUrl.split('|')
            if movies == 'FALSE':
                oHoster = oHosterGui.checkHoster(link)
                if oHoster:
                    oHoster.setDisplayName(sDisplayName)
                    oHoster.setFileName(sTitle)
                    oHosterGui.showHoster(oGui, oHoster, link, '')
            else:
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addLink(SITE_IDENTIFIER, 'showHoster', sDisplayName, 'host.png', '', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showHoster():
    from resources.lib.gui.hoster import cHosterGui
    oHosterGui = cHosterGui()
    oGui = cGui()
    pbContent = PasteContent()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    link, paste, pbContent.movies = oInputParameterHandler.getValue('siteUrl').split('|')
    hosterLienDirect = oHosterGui.getHoster('lien_direct')

    resolvedLinks = pbContent.resolveLink(paste, link)
    for sHosterUrl, res, lang in resolvedLinks:
        if sHosterUrl:
            if not sHosterUrl.startswith('http'):
                sHosterUrl = 'http://' + sHosterUrl
    
            if '/dl/' in sHosterUrl or '.download.' in sHosterUrl or '.uptostream.' in sHosterUrl:
                oHoster = hosterLienDirect
            else:
                oHoster = oHosterGui.checkHoster(sHosterUrl)
    
            if oHoster:
                sDisplayName = sTitle
                oHoster.setDisplayName(sDisplayName)
                oHoster.setFileName(sTitle)
                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


# Retrouve tous les liens disponibles pour un film ou un épisode, gère les groupes multipaste
def getHosterList(siteUrl):
    # Pour supporter les caractères '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')

    siteUrl, params = sUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    sRes = aParams['sRes'].upper() if 'sRes' in aParams else None
    searchYear = aParams['sYear'] if 'sYear' in aParams else None
    searchSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchEpisode = aParams['sEpisode'] if 'sEpisode' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    searchTitle = aParams['sTitle'].replace(' | ', ' & ')

    if sRes == UNCLASSIFIED:
        sRes = ''

    pbContent = PasteContent()
    listEpisodes = []
    listRes = {}
    listeIDs = getPasteList(pasteID)
    urls = [] # pour détecter les liens en double

    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin, sMedia)

        for movie in moviesBin:

            # Filtrer par catégorie
            if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                continue

            # Recherche par id
            found = False
            if idTMDB and pbContent.TMDB >= 0:
                sMovieID = movie[pbContent.TMDB].strip()
                if sMovieID:
                    if sMovieID != idTMDB:
                        continue
                    found = True

            # sinon, recherche par titre/année
            if not found:
                # Filtrage par années
                if searchYear and pbContent.YEAR >= 0:
                    sYear = movie[pbContent.YEAR].strip()
                    if sYear and sYear != searchYear:
                        continue

                # Filtrage par titre
                sTitle = movie[pbContent.TITLE].strip()
                if sTitle != searchTitle:
                    continue

            # Filtrage par saison
            if searchSaison and pbContent.SAISON >= 0:
                sSaisons = movie[pbContent.SAISON].strip()
                if sSaisons:
                    if sSaisons.isdigit():
                        sSaisons = '%02d' % int(sSaisons)
                    if searchSaison != sSaisons:
                        continue

            links = movie[pbContent.URLS]

            # numérotation des épisodes 08 -> 8 (problème de décodage en octal)
            if "{" in links:
                links = links.replace('{0', '{').replace('{:', '{0:').replace(',0', ',')

            listLinks = []

            if "[" in links or "{" in links:
                links = eval(links)

            # Films
            if isinstance(links, list):
                for link in links:
                    listLinks.append(link)

            # Séries
            elif isinstance(links, dict):
                if searchEpisode:
                    for numEpisode, link in links.items():
                        numEpisode = str(numEpisode).replace('E', '')   # E001 -> 001
                        if numEpisode.isdigit():
                            numEpisode = int(numEpisode)    # enlever les 0 devant
                        
                        if str(numEpisode) == searchEpisode:
                            listLinks.append(link)
                            break
                else:
                    listEpisodes.append(links)

            # lien direct
            else:
                listLinks.append(links)

            if len(listLinks) > 0:
                listResMovie = []
                idxResMovie = 0
                if pbContent.RES == -1:
                    res = ''
                else:
                    res = movie[pbContent.RES].strip().upper()
                if '[' in res:
                    listResMovie.extend(eval(res))
                else:
                    listResMovie.append(res)

                for link in listLinks:
                    if idxResMovie < len(listResMovie):
                        resMovie = listResMovie[idxResMovie].upper()
                        if resMovie and resMovie in '540P576P480P360P':
                            resMovie = 'SD'
                    else:
                        resMovie = ''
                    idxResMovie += 1

                    # On vérifie la résolution attendue si pas uptostream
                    if sRes and sRes not in resMovie:
                        if pbContent.getUptoStream() == 2:
                            continue

                    resolvedLinks = [(link + '|' + movie[pbContent.PASTE] + '|' + ('TRUE' if pbContent.movies else 'FALSE'), "ori", "ori")]
#                    resolvedLinks = pbContent.resolveLink(movie[pbContent.PASTE], link)
                    
                    for url, res, lang in resolvedLinks:
                        if not url:
                            continue
                        
                        if url in urls: # retrait des liens en double
                            continue
                        urls.append(url)
                        
                        if 'unknown' in lang:
                            lang = ''
                        else:
                            lang = str(lang) if lang != 'ori' else ''
                        if res and res != 'ori': 
                            res = str(res)
                            if res in '540P576P480P360P':
                                res = 'SD'
                            elif res.isdigit():
                                res += 'P'
                        else:
                            res = resMovie
                            if 'Multi' in res and not lang:
                                res = res.replace('Multi', '').strip()
                                lang = 'multi'

                        linkToAdd = False
                        if sRes:    # Recherche d'une résolution en particulier
                            if res and res != 'ori':
                                if sRes in res:
                                    linkToAdd = True
                            elif sRes in resMovie:
                                linkToAdd = True
                        else:
                            linkToAdd = True

                        if linkToAdd:
                            hoster = listRes.get(res)
                            if not hoster:
                                listRes[res] = ([[url, lang]])
                            else:
                                # filtre des résultats avec uptostream, retrait des doublons qualités/langues
                                exist = False
                                if pbContent.getUptoStream() in [3, 4]:
                                    for u, l in hoster:
                                        if l[:2].lower() == lang[:2].lower():
                                            exist = True
                                            break
                                if not exist:
                                    hoster.append([url, lang])

    if listEpisodes:
        return listEpisodes
    return listRes


# Ajout d'un dossier pastebin
def addPasteName():
    oGui = cGui()
    addons = addon()

    # Recherche d'un setting de libre
    names = set()
    newID = 0
    for numID in range(1, GROUPE_MAX):
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
            if newID == 0:
                newID = numID
        else:
            names.add(pasteLabel)  # Labels déjà utilisés

    settingLabel = SETTING_PASTE_LABEL + str(newID)

    # Demande du label et contrôle si déjà existant
    sLabel = oGui.showKeyBoard('', "[COLOR coral]Saisir un nom pour le dossier[/COLOR]")
    if sLabel is False:
        return

    sLabel = sLabel.strip()
    if sLabel in names:
        dialog().VSok(addons.VSlang(30082))
        return

    # Enregistrer Label/id dans les settings
    addons.setSetting(settingLabel, sLabel)
    dialog().VSinfo(addons.VSlang(30042))

    oGui.updateDirectory()


# Retirer un dossier PasteBin
def deletePasteName():

    addons = addon()
    if not dialog().VSyesno(addons.VSlang(30456)):
        return

    cache = PasteCache()
    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')

    labelSetting = SETTING_PASTE_LABEL + pasteID
    addons.setSetting(labelSetting, '')

    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteID = addons.getSetting(prefixID)
    if pasteID:
        addons.setSetting(prefixID, '')
        cache.remove(pasteID)

    for numID in range(1, PASTE_PAR_GROUPE):
        settingID = prefixID + '_' + str(numID)
        pasteID = addons.getSetting(settingID)
        if pasteID:
            addons.setSetting(settingID, '')
            cache.remove(pasteID)

    cGui().updateDirectory()


# Renommer un dossier PasteBin
def renamePasteName():

    addons = addon()
    oGui = cGui()

    # Recherche d'un setting de libre
    names = set()
    for numID in range(1, GROUPE_MAX):
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel:
            names.add(pasteLabel)  # Labels déjà utilisés

    # Demande du label et contrôle si déjà existant
    sLabel = oGui.showKeyBoard('', "[COLOR coral]Saisir un nom pour le dossier[/COLOR]")
    if sLabel is False:
        return

    sLabel = sLabel.strip()
    if sLabel in names:
        dialog().VSok(addons.VSlang(30082))
        return

    # Mettre à jour Label
    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')
    labelSetting = SETTING_PASTE_LABEL + pasteID
    addons.setSetting(labelSetting, sLabel)
    dialog().VSinfo(addons.VSlang(30042))

    oGui.updateDirectory()


# Forcer la mise à jour de tous les dossiers PasteBin
def refreshAllPaste():
    oGui = cGui()
    oGui.addText(SITE_IDENTIFIER, '[COLOR teal]Mise à jour des contenus  ..... [/COLOR]', 'download.png')
    oGui.setEndOfDirectory()

    xbmc.sleep(1000)  # laisser le temps de voir que l'action a bien été prise en compte

    # le skin peut rappeler la fonction une deuxième fois, ne pas prendre en compte en vérifiant si on est revenu sur la home
    if not xbmc.getCondVisibility('Window.IsActive(home)'):
        PasteCache().clean()
        dialog().VSinfo(addon().VSlang(30014))
        xbmc.sleep(1000)
        xbmc.executebuiltin('Action(Back)')


# Retirer tous les dossiers PasteBin
def deleteAllPasteName():

    addons = addon()
    cache = PasteCache()

    for numID in range(1, GROUPE_MAX):
        labelSetting = SETTING_PASTE_LABEL + str(numID)
        pasteLabel = addons.getSetting(labelSetting)
        if not pasteLabel:
            continue

        addons.setSetting(labelSetting, '')

        prefixID = SETTING_PASTE_ID + str(numID)
        pasteID = addons.getSetting(prefixID)
        if pasteID:
            addons.setSetting(prefixID, '')
            cache.remove(pasteID)

        for numID in range(1, PASTE_PAR_GROUPE):
            settingID = prefixID + '_' + str(numID)
            pasteID = addons.getSetting(settingID)
            if pasteID:
                addons.setSetting(settingID, '')
                cache.remove(pasteID)


# renouvelle le contenu d'un paste
def renewPaste(pasteID, lastMediaTitle=''):
    content = PasteContent()
    content.renew(pasteID, lastMediaTitle)


# Retourne la liste des PasteBin depuis l'URL ou un groupe
def getPasteList(pasteID = None):
    addons = addon()

    # Tous les pastes si non précisés
    if not pasteID:
        listeIDs = []
        for numID in range(1, GROUPE_MAX):
            prefixID = SETTING_PASTE_LABEL + str(numID)
            pastebin = addons.getSetting(prefixID)
            if pastebin:
                listeIDs += getPasteList(numID)
        return dict.fromkeys(listeIDs).keys()   # suppression des doublons et conserve l'ordre


    IDs = []
    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    if pasteBin and pasteBin not in IDs:
        IDs.append(pasteBin)
    for numID in range(1, PASTE_PAR_GROUPE):
        pasteID = prefixID + '_' + str(numID)
        pasteBin = addons.getSetting(pasteID)
        if pasteBin and pasteBin not in IDs:
            IDs.append(pasteBin)
    return set(IDs)


# Ajout d'un lien pastebin
def addPasteID():
    oGui = cGui()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')

    # Recherche d'un setting de libre
    # Et lister les pastes déjà déclarés pour éviter les doublons
    IDs = set()
    settingID = None
    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    if pasteBin:
        IDs.add(pasteBin)      # IDs déjà renseigné
    if pasteBin == '':
        settingID = prefixID
    for numID in range(1, PASTE_PAR_GROUPE):
        pasteID = prefixID + '_' + str(numID)
        pasteBin = addons.getSetting(pasteID)
        if pasteBin != '':
            IDs.add(pasteBin)  # IDs déjà renseigné
        elif not settingID:
            settingID = pasteID

    # Demande de l'id PasteBin
    pasteID = oGui.showKeyBoard('', "[COLOR coral]Saisir le code du %s[/COLOR]" % SITE_NAME)
    if pasteID is False:
        return

    pasteID = pasteID.strip()
    if pasteID in IDs:  # ID déjà dans le groupe
        dialog().VSok(addons.VSlang(30082))
        return

    # Vérifier l'entête du Paste
    pbContentNew = PasteContent()

    try:
        movies = pbContentNew.getLines(pasteID)
        if len(movies) == 0:
            dialog().VSok(addons.VSlang(30022))
            return
    except Exception as e:
        dialog().VSinfo(addons.VSlang(30011))
        raise

    # Vérifier que les autres pastes du groupe ont le même format d'entête
    if len(IDs) > 0:
        pbContentOld = PasteContent()
        pbContentOld.getLines(IDs.pop())

        if not pbContentNew.isFormat(pbContentOld):
            dialog().VSok(addons.VSlang(30022))
            return

    # ok, on ajoute le paste
    addons.setSetting(settingID, pasteID)
    dialog().VSinfo(addons.VSlang(30042))

    oGui.updateDirectory()


# Liste de pastes avec possibilité de les supprimer
def adminPasteID():
    oGui = cGui()
    addons = addon()

    oGui.addText(SITE_IDENTIFIER, '[COLOR coral]Valider le code à retirer[/COLOR]', 'trash.png')

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')  # Numéro du dossier
    prefixID = SETTING_PASTE_ID + str(pasteID)

    pbContentNew = PasteContent()
    oOutputParameterHandler = cOutputParameterHandler()
    for numID in range(0, PASTE_PAR_GROUPE):
        if numID == 0:
            pasteBin = addons.getSetting(prefixID)
        else:
            pasteBin = addons.getSetting(prefixID + '_' + str(numID))
        if not pasteBin:
            continue

        # Vérifier la qualité du Paste
        color = 'white'  # Forcer une couleur évite aussi le nettoyage du "titre"
        try:
            movies = pbContentNew.getLines(pasteBin)
            if len(movies) == 0:
                color = 'red'
        except Exception as e:
            dialog().VSinfo(addons.VSlang(30011))
            raise

        pasteLabel = '[COLOR %s]%s[/COLOR]' % (color, pasteBin)

        oOutputParameterHandler.addParameter('pasteID', pasteID)
        oOutputParameterHandler.addParameter('pasteBin', pasteBin)
        oGui.addDir(SITE_IDENTIFIER, 'deletePasteID', pasteLabel, 'trash.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Suppression d'un paste dans un dossier
def deletePasteID():

    addons = addon()
    if not dialog().VSyesno(addons.VSlang(30456)):
        return

    cache = PasteCache()
    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')    # Numéro du dossier
    pasteDel = oInputParameterHandler.getValue('pasteBin')  # Paste

    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    if pasteDel == pasteBin:
        addons.setSetting(prefixID, '')
        cache.remove(pasteBin)
    else:
        for numID in range(1, PASTE_PAR_GROUPE):
            pasteID = prefixID + '_' + str(numID)
            pasteBin = addons.getSetting(pasteID)
            if pasteDel == pasteBin:
                addons.setSetting(pasteID, '')
                cache.remove(pasteBin)
                break

    dialog().VSinfo(addons.VSlang(30072))

    cGui().updateDirectory()


# Menu d'administration des contenus
def adminContenu():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    sDecoColor = addon().getSetting('deco_color')

    # Menu pour afficher le nombre de média
    oGui.addDir(SITE_IDENTIFIER, 'getNbMedia', "[COLOR %s]Nombre total d'éléments[/COLOR]" % sDecoColor, 'views.png', oOutputParameterHandler)

    # Menu pour rafraichir le cache
    oGui.addDir(SITE_IDENTIFIER, 'refreshAllPaste', '[COLOR %s]Forcer la mise à jour des contenus[/COLOR]' % sDecoColor, 'download.png', oOutputParameterHandler)

    # Menu pour définir la période du cache
    oGui.addDir(SITE_IDENTIFIER, 'adminCacheDuration', '[COLOR %s]Période de rafraichissement des contenus[/COLOR]' % sDecoColor, 'update.png', oOutputParameterHandler)

    # Menu pour rafraichir le cache
    oGui.addDir(SITE_IDENTIFIER, 'adminNbElement', "[COLOR %s]Nombre d'éléments affichés[/COLOR]" % sDecoColor, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Définir la période de rafraichissement des pastes
def adminCacheDuration():
    oGui = cGui()
    nDuration = oGui.showNumBoard("Nombre d'heures", str(CACHE_DURATION))
    if nDuration:
        addon().setSetting(SITE_IDENTIFIER + '_cacheDuration', nDuration)


# Définir le nombre d'éléments par liste
def adminNbElement():
    oGui = cGui()
    nElement = oGui.showNumBoard("Nombre d'éléments par page", str(ITEM_PAR_PAGE))
    if nElement:
        addon().setSetting(SITE_IDENTIFIER + '_nbItemParPage', nElement)


# Retourne la décompte de média par type
def getNbMedia():
    idFilms = set()
    idSeries = set()
    idAnimes = set()
    idDivers = set()
    
    pbContent = PasteContent()
    listeIDs = getPasteList()
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        for movie in moviesBin:
            videoId = movie[pbContent.TMDB] if movie[pbContent.TMDB] else movie[pbContent.TITLE]
            if 'film' in movie[pbContent.CAT]:
                idFilms.add(videoId)
            elif 'serie' in movie[pbContent.CAT]:
                idSeries.add(videoId)
            elif 'anime' in movie[pbContent.CAT]:
                idAnimes.add(videoId)
            else:
                idDivers.add(videoId)
                
    oGui = cGui()
    oGui.addText(SITE_IDENTIFIER, 'Films[COLOR coral] (%d) [/COLOR]' % len(idFilms), 'films.png')
    oGui.addText(SITE_IDENTIFIER, 'Séries[COLOR coral] (%d) [/COLOR]' % len(idSeries), 'tv.png')
    oGui.addText(SITE_IDENTIFIER, 'Animés[COLOR coral] (%d) [/COLOR]' % len(idAnimes), 'animes.png')
    oGui.addText(SITE_IDENTIFIER, 'Divers[COLOR coral] (%d) [/COLOR]' % len(idDivers), 'buzz.png')
    oGui.setEndOfDirectory()

