# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import imp
import random
import time
import xbmc
import xbmcvfs

from resources.lib.comaddon import progress, addon, dialog, VSlog, VSPath, isMatrix
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.util import Quote, cUtil, Unquote
from resources.lib.tmdb import cTMDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.premiumHandler import cPremiumHandler

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite


SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'PasteBin'

SITE_DESC = 'Liste depuis %s' % SITE_NAME

URL_MAIN = 'https://pastebin.com/raw/'

KEY_PASTE_ID = 'PASTE_ID'
SETTING_PASTE_ID = SITE_IDENTIFIER + '_id_'
SETTING_PASTE_LABEL = SITE_IDENTIFIER + '_label_'
UNCLASSIFIED_GENRE = '_NON CLASSÉ_'
UNCLASSIFIED = 'Indéterminé'

URL_SEARCH_MOVIES = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=film&sSearch=', 'showSearchGlobal')
URL_SEARCH_SERIES = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=serie&sSearch=', 'showSearchGlobal')
URL_SEARCH_ANIMS = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=anime&sSearch=', 'showSearchGlobal')
URL_SEARCH_DIVERS = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=divers&sSearch=', 'showSearchGlobal')
FUNCTION_SEARCH = 'showSearchGlobal'


CACHE = 'special://home/userdata/addon_data/plugin.video.vstream/%s_cache.db'  % SITE_IDENTIFIER

if not isMatrix():
    REALCACHE = VSPath(CACHE).decode('utf-8')
    PATH = 'special://home/addons/plugin.video.vstream/resources/lib/pasteCrypt2.pyc'
else:
    REALCACHE = VSPath(CACHE)
    PATH = 'special://home/addons/plugin.video.vstream/resources/lib/pasteCrypt3.pyc'


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
        cacheDuration = "12"  # en heure
        addon().setSetting(SITE_IDENTIFIER + '_cacheDuration', cacheDuration)
    return min(int(cacheDuration), 168)

CACHE_DURATION = getCacheDuration()


""" GESTION DU CACHE """


class PasteCache:

    def __init__(self):

        try:
            if not xbmcvfs.exists(CACHE):
                self.db = sqlite.connect(REALCACHE)
                self.db.row_factory = sqlite.Row
                self.dbcur = self.db.cursor()
                self.__createdb()
                return
        except:
            VSlog('Error: Unable to create DB %s' % REALCACHE)
            pass

        try:
            self.db = sqlite.connect(REALCACHE)
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
        except:
            VSlog('Error: Unable to create table %s' % SITE_IDENTIFIER)

        self.dbcur.execute(sql_create)
        VSlog('table %s creee' % SITE_IDENTIFIER)

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
            return None, False

        if matchedrow:
            data = dict(matchedrow)

            # Supprimer les données trop anciennes
            cacheDuration = time.time() - CACHE_DURATION * 3600
            if data['date'] < cacheDuration:
                self.clean(cacheDuration)
                return None, False

            # Utiliser les données du cache
            if isMatrix():
                content = data['content'].decode("utf-8")
            else:
                content = str(data['content'])
            if content[-1] == '.':
                return content[:-1], True
            return content, False
        else:
            return None, False

    # Sauvegarde des données dans un cache
    def save(self, pasteID, pasteContent, isMovie):

        try:
            sql = 'INSERT INTO %s (paste_id, content, date) VALUES (?, ?, ?)' % SITE_IDENTIFIER
            buff = str(pasteContent)
            if isMovie:
                buff += '.'

            if isMatrix():
                buff = memoryview(bytes(buff, encoding='utf-8'))
            else:
                buff = buffer(buff)

            self.dbcur.execute(sql, (pasteID, buff, time.time()))
            self.db.commit()
        except Exception as e:
            VSlog('SQL ERROR INSERT into table \'%s\', ID=%s, e=%s' % (SITE_IDENTIFIER, pasteID, e))
            pass

    # Suprimer une entrée
    def remove(self, ID):

        try:
            sql_delete = 'DELETE FROM %s WHERE paste_id = \'%s\'' % (SITE_IDENTIFIER, ID)
            self.dbcur.execute(sql_delete)
            self.db.commit()
        except Exception as e:
            VSlog('************* Error deleting from cache db: %s, e=%s' % (ID, e), 4)
            return None

    # Suprimer les données trop anciennes
    def clean(self, cacheDuration):

        try:
            sql_delete = 'DELETE FROM %s WHERE date < \'%s\'' % (SITE_IDENTIFIER, cacheDuration)
            self.dbcur.execute(sql_delete)
            self.db.commit()
        except Exception as e:
            VSlog('************* Error deleting from %s db: %s' % (SITE_IDENTIFIER, e), 4)
            return None

    # Suprimer tout le cache
    def delete(self):
        VSlog('PasteCache - delete')
        
        # sql_select = "SELECT paste_id FROM %s" % SITE_IDENTIFIER
        # try:
            # self.dbcur.execute(sql_select)
            # matchedrow = self.dbcur.fetchall()
            # if not matchedrow:
                # return False  # Rien à supprimer
        # except Exception as e:
            # VSlog('SQL ERROR : %s' % sql_select)
            # return False
        
        try:
            sql_delete = 'DELETE FROM %s' % SITE_IDENTIFIER
            self.dbcur.execute(sql_delete)
            self.db.commit()
        except Exception as e:
            VSlog('************* Error deleting from %s db: %s' % (SITE_IDENTIFIER, e), 4)
            return False
        return True

# Exemple
# CAT; TMDB; TITLE; SAISON; YEAR; GENRES; URLS=https://uptobox.com/
# film;714;Demain ne meurt jamais;James BOND;1997;['Action', 'Aventure', 'Thriller'];['nwxxxx','nwYYzz']
# serie;48866;Les 100;Saison 2; 2014; ['Fantastique', 'Aventure']; {'S02E01':['lien1', 'lien2'], 'S02E02':['lien1']}

# Exemple minimum
# CAT;TITLE; URLS
# film;Demain ne meurt jamais;['https://uptobox.com/nwxxxx']


class PasteContent:
    CAT = -1        # (Optionnel) - Catégorie 'film', 'serie' 'anime' (Film par défaut)
    TMDB = -1       # (optionnel) - Id TMDB
    TITLE = -1      # Titre du film / épisodes
    SAISON = -1     # (optionnel) - Saison pour les séries (ex 'Saison 03' ou 'S03' ou '03') OU Saga pour les films (ex 'Mission impossible')
    GROUPES = -1    # (optionnel) - Groupes tel que NETFLIX, HBO, MARVEL, DISNEY, Films enfants, ...
    YEAR = -1       # (optionnel) - Année
    GENRES = -1     # (optionnel) - Liste des genres
    RES = -1        # (optionnel) - Résolution (720p, 1080p, 4K, ...)
    DIRECTOR = -1   #  (optionnel) - Réalisateur au format id:nom
    CAST = -1       #  (optionnel) - Acteurs au format id:nom
    NETWORK = -1    #  (optionnel) - Diffuseur au format id:nom
    HEBERGEUR = ''  # (optionnel) - URL de l'hebergeur, pour éviter de le mettre dans chaque URL, ex : 'https://uptobox.com/'
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
        if not self.upToStream:
            if not cPremiumHandler('uptobox').isPremiumModeAvailable():
                self.upToStream = 2 # forcer une valeur pour ne pas retester
            else:
                mode = int(addon().getSetting("hoster_uptobox_mode_default"))
                self.upToStream = 4-mode
        return self.upToStream

    def getLines(self, pasteBin):

        sContent, self.movies = self._getCache().read(pasteBin)

        # Lecture en cache
        if sContent:
            lines = eval(sContent)
            entete = lines[0].split(";")

        # Lecture sur le site
        else:
            # test si paste accessible
            lines, self.movies = self._decompress(pasteBin)
            if not lines:
                return []

            # Vérifie si la ligne d'entete existe avec les champs obligatoires
            entete = lines[0].split(";")
            if 'TITLE' not in entete and 'URL' not in entete:
                return []
            self._getCache().save(pasteBin, lines, self.movies)

        # Calcul des index de chaque champ
        idx = 0
        for champ in entete:
            champ = champ.strip()

            if 'URL' in champ:  # supporte URL ou URLS
                hebergeur = champ.split('=')
                champ = 'URLS'
                if len(hebergeur) > 1:
                    self.HEBERGEUR = hebergeur[1].replace(' ', '').replace('"', '').replace('\'', '')
            if champ in dir(self):
                setattr(self, champ, idx)
            idx += 1

        lines = [k.split(";") for k in lines[1:]]

        return lines

    def resolveLink(self, pasteBin, link):
        if not self.movies:
            return [(self.HEBERGEUR+link, 'ori', 'ori')]

        if 'uptobox' in self.HEBERGEUR:
            # Recherche d'un compte premium valide
            links = None
            if not self.keyUpto and not self.keyAlld and not self.keyReald:
                self.keyUpto = cPremiumHandler('uptobox').getToken()
                if self.keyUpto:
                    links = self._resolveLink(pasteBin, link)
                if not links:
                    self.keyUpto = None
                    self.keyReald = cPremiumHandler('realdebrid').getToken()
                    if self.keyReald:
                        links = self._resolveLink(pasteBin, link)
                if not links:
                    self.keyReald = None
                    self.keyAlld = cPremiumHandler('alldebrid').getToken()
                    if self.keyAlld:
                        links = self._resolveLink(pasteBin, link)
                        if not links:
                            self.keyAlld = None

            # Un compte avec un des trois débrideurs
            if not links and (self.keyUpto or self.keyAlld or self.keyReald):
                links = self._resolveLink(pasteBin, link)
            if links:
                return links
            else:
                dialog().VSinfo('Certains liens nécessitent un Compte Premium')

        return [(self.HEBERGEUR+link, 'ori', 'ori')]

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

        if status == 'ok' and links and len(links)>0:
            return links
        
        err = 'Erreur : ' + str(status)
        VSlog(err)

    def _decompress(self, pasteBin):

        lines = []
        hasMovies = False
        try:
            lines = self._getCrypt().loadFile(pasteBin)
            if lines:
                hasMovies = True
        except Exception as e:
            pass

        if not hasMovies:
            oRequestHandler = cRequestHandler(URL_MAIN + pasteBin)
            oRequestHandler.setTimeout(4)
            sContent = oRequestHandler.request()
            if sContent.startswith('<'):
                return [], False

            if sContent.startswith('CAT;'):
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


def load():
    addons = addon()
    oGui = cGui()

    numID = 0
    pasteListe = {}

    # Recherche des listes déclarées
    for numID in range(1, 50):
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel:
            pasteListe[pasteLabel] = numID

    # Trie des dossiers par label
    pasteListe = sorted(pasteListe.items(), key=lambda paste: paste[0])

    if len(pasteListe) > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_MOVIES[0]
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

        searchUrl = URL_SEARCH_SERIES[0]
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

        searchUrl = URL_SEARCH_ANIMS[0]
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)

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
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'renamePasteName', addons.VSlang(30223))
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'refreshPaste', "Forcer la mise à jour")
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'deletePasteName', addons.VSlang(30412))
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # Menu pour ajouter un dossier (hors widget)
    if not xbmc.getCondVisibility('Window.IsActive(home)'):
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'addPasteName', '[COLOR coral]Ajouter un dossier %s[/COLOR]' % SITE_NAME, 'listes.png', oOutputParameterHandler)

    # Menu pour raffraichir tout le cache
    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'refreshAllPaste', '[COLOR coral]Mettre à jour tous les contenus[/COLOR]', 'download.png', oOutputParameterHandler)

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
            oOutputParameterHandler.addParameter('pasteID', pasteID) # remettre les paramètres lorsqu'on recycle oOutputParameterHandler
            oGui.addDir(SITE_IDENTIFIER, 'addPasteID', '[COLOR coral]Ajouter un code %s[/COLOR]' % SITE_NAME, 'notes.png', oOutputParameterHandler)
            
            oOutputParameterHandler.addParameter('pasteID', pasteID) # remettre les paramètres lorsqu'on recycle oOutputParameterHandler
            oGui.addDir(SITE_IDENTIFIER, 'adminPasteID', '[COLOR coral]Retirer un code %s[/COLOR]' % SITE_NAME, 'trash.png', oOutputParameterHandler)

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
        searchUrl = URL_SEARCH_MOVIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

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
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Films (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

        if 'containFilmReal' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showRealisateur', 'Films (Par réalisateurs)', 'actor.png', oOutputParameterHandler)

        if 'containFilmCast' in contenu:
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showCast', 'Films (Par acteurs)', 'actor.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&bRandom=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Aléatoires)', 'listes.png', oOutputParameterHandler)

    if 'containSeries' in contenu:
        searchUrl = URL_SEARCH_SERIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

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
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Séries (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&bRandom=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Aléatoires)', 'listes.png', oOutputParameterHandler)

    if 'containAnimes' in contenu:
        searchUrl = URL_SEARCH_ANIMS[0].replace(KEY_PASTE_ID, pasteID)
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
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Animes (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    if 'containDivers' in contenu:
        searchUrl = URL_SEARCH_DIVERS[0].replace(KEY_PASTE_ID, pasteID)
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
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Divers (Ordre alphabétique)', 'az.png', oOutputParameterHandler)


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


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl += Quote(sSearchText)

        # Recherche globale si le pastebin n'est pas indiqué
        if KEY_PASTE_ID in sUrl:
            showSearchGlobal(sUrl)
        else:
            showMovies(sUrl)
        oGui.setEndOfDirectory()


def showSearchGlobal(sSearch=''):
    addons = addon()

    sUrl = sSearch

    for numID in range(1, GROUPE_MAX):
        prefixID = SETTING_PASTE_LABEL + str(numID)
        pastebin = addons.getSetting(prefixID)
        if pastebin:
            searchUrl = sUrl.replace(KEY_PASTE_ID, str(numID))
            try:
                showMovies(searchUrl)
            except:
                pass


def showGenres():
    tmdb = cTMDb()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    listeIDs = getPasteList(sUrl, pasteID)

    genres = {}
    pbContent = PasteContent()
    for pasteBin in listeIDs:

        movies = pbContent.getLines(pasteBin)

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
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteContent()
    listNetwork = {}
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)
        for movie in movies:
            if pbContent.CAT >= 0 and sMedia not in movie[pbContent.CAT]:
                continue
    
            networks = movie[pbContent.NETWORK].strip()
            if networks != '':
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
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)
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
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)
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
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)

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
                                if grID not in sousGroupe:
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

    pbContent = PasteContent()
    groupes = set()
    
    if sGroupe:
        listeIDs = getPasteList(sUrl, pasteID)
        for pasteBin in listeIDs:
            movies = pbContent.getLines(pasteBin)
            for movie in movies:
                groupe = movie[pbContent.GROUPES].strip().replace("''", '')
                if groupe:
                    groupe = eval(groupe)
                    if groupe:
                        for gr in groupe:
                            if gr.startswith(sGroupe):
                                groupes.add(gr)

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
    listeIDs = getPasteList(sUrl, pasteID)

    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)
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
        if not sSagaName.lower().endswith('saga'):
            sSagaName = sSagaName + " Saga"
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
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)
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
def trie_res(key):
    resOrder = ['8K', '4K', '2160P', '1080P', '720P', '576P', '540P', '480P', '360P']
    if key == UNCLASSIFIED:
        return 20
    key = key.replace('p', 'P')
    if key not in resOrder:
        resOrder.append(key)
    return resOrder.index(key)

def showResolution():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteContent()
    resolutions = set()
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        movies = pbContent.getLines(pasteBin)
        for line in movies:
            if pbContent.CAT >= 0 and sMedia not in line[pbContent.CAT]:
                continue
    
            res = line[pbContent.RES].strip()
            if '[' in res:
                if res != '[]':
                    res = eval(res)
                    resolutions = resolutions.union(res)
                    if '' in res or len(res) == 0:
                        resolutions.add(UNCLASSIFIED)
            else:
                resolutions.add(res)
    
            if not res or res == '[]':
                resolutions.add(UNCLASSIFIED)

    resolutions.discard('')

    resolutions = sorted(resolutions, key=trie_res)

    oOutputParameterHandler = cOutputParameterHandler()
    for sRes in resolutions:
        if sRes == '':
            continue

        sDisplayRes = sRes
        if sDisplayRes.isdigit():
            sDisplayRes += 'p'
        sDisplayRes = sDisplayRes\
            .replace('P', 'p')\
            .replace('1080p', 'fullHD [1080p]')\
            .replace('720p', 'HD [720p]')\
            .replace('540p', 'SD [540p]')\
            .replace('480p', 'SD [480p]')\
            .replace('360p', 'SD [360p]')\
            .replace('4K', '2160p')\
            .replace('8K', '4320p')\
            .replace('2160p', '4K [2160p]')\
            .replace('4320p', '8K [4320p]')

        sUrl = siteUrl + '&sRes=' + sRes
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayRes, 'hd.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def AlphaList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for i in range(0, 36):
        if (i < 10):
            sLetter = chr(48 + i)
        else:
            sLetter = chr(65 + i - 10)

        sUrl = siteUrl + '&sAlpha=' + sLetter

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
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
    bRandom = bNews = False

    if sSearch:
        siteUrl = sSearch

    sSearchTitle = ''

    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
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
        sGroupe = aParams['sGroupe'].replace(' | ', ' & ')
    if 'sYear' in aParams:
        sYear = aParams['sYear']
    if 'sRes' in aParams:
        sRes = aParams['sRes']
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
    if not numPage and 'numPage' in aParams:
        numPage = aParams['numPage']

    pbContent = PasteContent()
    movies = []
    pasteLen = []
    pasteMaxLen = []
    maxlen = 0
    listeIDs = getPasteList(sUrl, pasteID)

    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin
        pasteLen.append(len(moviesBin))
        maxlen += len(moviesBin)
        pasteMaxLen.append(maxlen)

    # si plusieurs pastes, on les parcourt en parallèle
    if (bNews or sYear or sGenre or sRes) and len(listeIDs) > 1:
        moviesNews = []
        i = j = k = 0
        lenMovie = len(movies)
        while k < lenMovie:
            if i < pasteMaxLen[j]:
                moviesNews.append(movies[i])
                k += 1
            i += pasteLen[j]
            j += 1
            if j >= len(pasteMaxLen):
                i = (i % lenMovie) + 1
                j=0

        movies = moviesNews

    # Recherche par ordre alphabetique => le tableau doit être trié
    if sAlpha:
        movies = sorted(movies, key=lambda line: line[pbContent.TITLE])

    # Recherche par saga => trie par années
    if sSaga and pbContent.YEAR >= 0:
        movies = sorted(movies, key=lambda line: line[pbContent.YEAR])

    # Dans un dossier => trie par années inversées (du plus récent)
    if sGroupe or sDirector or sCast:
        movies = sorted(movies, key=lambda line: line[pbContent.YEAR], reverse=True)

    # Gestion de la pagination
    if not numItem:
        numItem = 0
    else:
        numItem = int(numItem)
    numPage = int(numPage)
    if numPage > 1 and numItem == 0:  # choix d'une page
        numItem = (numPage-1) * ITEM_PAR_PAGE
        if numItem > len(movies):   # accès direct à la dernière page
            numPage = len(movies) / ITEM_PAR_PAGE
            numItem = (numPage-1) * ITEM_PAR_PAGE

    if bRandom:
        numItem = 0
        # Génération d'indices aléatoires, ajout de deux indices car les doublons aléatoires sont rassemblés
        randoms = [random.randint(0, len(movies)) for _ in range(ITEM_PAR_PAGE+2)]

    movieIds = set()

    nbItem = 0
    index = 0
    progress_ = progress().VScreate(SITE_NAME)
    oOutputParameterHandler = cOutputParameterHandler()

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
            listNetwork = eval(listNetwork)
            if sNetwork not in listNetwork:
                continue

        # Filtrage par groupe
        if sGroupe and pbContent.GROUPES >= 0:
            groupes = movie[pbContent.GROUPES].strip()
            if not groupes:
                continue
            groupes = eval(groupes)
            if sGroupe not in groupes:
                continue

        # Filtrage par titre
        sTitle = movie[pbContent.TITLE].strip()

        # l'ID TMDB
        sTmdbId = None
        if pbContent.TMDB >= 0:
            sTmdbId = movie[pbContent.TMDB].strip()
            if sTmdbId:
                if sTmdbId in movieIds:
                    continue            # Filtre des doublons
                movieIds.add(sTmdbId)
        if not sTmdbId:
            if sTitle in movieIds:
                continue            # Filtre des doublons
            movieIds.add(sTitle)

        # Titre recherché
        if sSearchTitle:
            if cUtil().CheckOccurence(sSearchTitle, sTitle) == 0:
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
                res = movie[pbContent.RES].strip()
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
                elif sRes not in listRes:
                    continue

        nbItem += 1
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

        # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
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
        if not sSearch:

            if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(movies):
                numPage += 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('numPage', numPage)
                oOutputParameterHandler.addParameter('numItem', numItem)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(numPage), oOutputParameterHandler)
                break

    progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()


def showSerieSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    searchTitle = oInputParameterHandler.getValue('sMovieTitle')
    searchYear = oInputParameterHandler.getValue('sYear')

    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')

    sUrl, params = sUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'serie'

    saisons = {}
    listeIDs = getPasteList(sUrl, pasteID)
    pbContent = PasteContent()
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)

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
            if numSaison not in saisons:
                saisons[numSaison] = set()
            
            # on ne gere pas les résolutions pour uptostream
            if pbContent.getUptoStream() == 3:
                continue
            
            # Résolutions dispo pour la saison
            listRes = saisons[numSaison]
            if pbContent.RES >= 0:
                res = serie[pbContent.RES].strip()
                if '[' in res:
                    for r in eval(res):
                        listRes.add(r)
                else:
                    listRes.add(res)


#     # Une seule saison, directement les épisodes
#     if len(saisons) == 1:
#         key, res = saisons.items()
#         siteUrl += '&sSaison=' + key
#         showEpisodesLinks(siteUrl)
#         return

    # Proposer les différentes saisons
    oOutputParameterHandler = cOutputParameterHandler()
    saisons = sorted(saisons.items(), key=lambda saison: saison[0])
    for sSaison, res in saisons:

        sDisplaySaison = sSaison
        if sSaison.isdigit():
            sDisplaySaison = 'S{:02d}'.format(int(sSaison))

        if len(res) == 0:
            sUrl = siteUrl + '&sSaison=' + sSaison
            sDisplayTitle = searchTitle + ' - ' + sDisplaySaison
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas le sTitre afin de pouvoir mettre la saison en marque-page
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodesLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        else:
            for resolution in res:
                sUrl = siteUrl + '&sSaison=' + sSaison
                sDisplayTitle = ('%s %s') % (searchTitle, sDisplaySaison)
                if resolution:
                    sUrl += '&sRes=' + resolution
                    sDisplayTitle += ' [%s]' % resolution
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas le sTitre afin de pouvoir mettre la saison en marque-page
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodesLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodesLinks(siteUrl=''):
    oGui = cGui()

    if not siteUrl:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')

    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')
    params = sUrl.split('&', 1)[1]
    aParams = dict(param.split('=') for param in params.split('&'))
    sSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchTitle = aParams['sTitle'].replace(' | ', ' & ')

    if not sSaison:
        oGui.setEndOfDirectory()
        return

    lines = getHosterList(siteUrl)

    listeEpisodes = []
    for episode in lines:
        for numEpisode in episode.keys():
            if numEpisode not in listeEpisodes:
                listeEpisodes.append(numEpisode)

    sDisplaySaison = sSaison
    if sSaison.isdigit():
        sDisplaySaison = 'S{:02d}'.format(int(sSaison))

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
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')
    params = sUrl.split('&', 1)[1]
    aParams = dict(param.split('=') for param in params.split('&'))

    listRes = getHosterList(siteUrl)

    for res in sorted(listRes.keys(), key=trie_res):
        displayRes = res.replace('P', 'p').replace('1080p', 'fullHD').replace('720p', 'HD').replace('2160p', '4K')
        for sHosterUrl, lang in listRes[res]:
    
            if not sHosterUrl.startswith('http'):
                sHosterUrl += 'http://' + sHosterUrl
    
            if '/dl/' in sHosterUrl or '.download.' in sHosterUrl or '.uptostream.' in sHosterUrl:
                oHoster = cHosterGui().getHoster('lien_direct')
            else:
                oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if oHoster:
                sDisplayName = sTitle
                if displayRes:
                    sDisplayName += ' [%s]' % displayRes
                if lang:
                    sDisplayName += ' (%s)' % lang
    
                oHoster.setDisplayName(sDisplayName)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


# Retrouve tous les liens disponibles pour un film, ou un épisode, gère les groupes multipaste
def getHosterList(siteUrl):
    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')

    siteUrl, params = sUrl.split('&', 1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    sRes = aParams['sRes'] if 'sRes' in aParams else None
    searchYear = aParams['sYear'] if 'sYear' in aParams else None
    searchSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchEpisode = aParams['sEpisode'] if 'sEpisode' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    searchTitle = aParams['sTitle'].replace(' | ', ' & ')

    pbContent = PasteContent()
    listEpisodes = []
    listRes = {}
    listeIDs = getPasteList(siteUrl, pasteID)

    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)

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

            # Filtrage par saison
            if searchSaison and pbContent.SAISON >= 0:
                sSaisons = movie[pbContent.SAISON].strip()
                if sSaisons and searchSaison != sSaisons:
                    continue

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
                res = movie[pbContent.RES].strip()
                if '[' in res:
                    listResMovie.extend(eval(res))
                else:
                    listResMovie.append(res)

                for link in listLinks:
                    if idxResMovie < len(listResMovie):
                        resMovie = listResMovie[idxResMovie]
                    else:
                        resMovie = ''
                    idxResMovie += 1
                    
                    # On vérifie la résolution attendue si pas uptostream
                    if sRes and resMovie != sRes:
                        if pbContent.getUptoStream() == 2:
                            continue

                    listLinks = pbContent.resolveLink(pasteBin, link)
                    for url, res, lang in listLinks:
                        if 'unknown' in lang:
                            lang = ''
                        else:
                            lang = str(lang) if lang != 'ori' else ''
                        if res != 'ori': 
                            res = str(res)
                        else:
                            res = resMovie
                            if 'Multi' in res and not lang:
                                res = res.replace('Multi', '').strip()
                                lang = 'multi'
                        
                        linkToAdd = False
                        if sRes:    # Recherche d'une résolution en particulier
                            if res and res != 'ori':
                                if res in sRes:
                                    linkToAdd = True
                            elif sRes == resMovie:
                                linkToAdd = True
                        else:
                            linkToAdd = True

                        if linkToAdd:
                            if res.isdigit():
                                res += 'P'
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
            names.add(pasteLabel)   # Labels déjà utilisés

    settingLabel = SETTING_PASTE_LABEL + str(newID)

    # Demande du label et controle si déjà existant
    sLabel = oGui.showKeyBoard('', "[COLOR coral]Saisir un nom pour le dossier[/COLOR]")
    if sLabel == False:
        return
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
            names.add(pasteLabel)   # Labels déjà utilisés

    # Demande du label et controle si déjà existant
    sLabel = oGui.showKeyBoard('', "[COLOR coral]Saisir un nom pour le dossier[/COLOR]")
    if sLabel == False:
        return
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


# Forcer la mise à jour d'un dossier PasteBin
def refreshPaste():

    addons = addon()
    cache = PasteCache()

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')

    # Supprimer le cache de chaque paste du dossier
    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    if pasteBin:
        cache.remove(pasteBin)
    for numID in range(1, PASTE_PAR_GROUPE):
        pasteID = prefixID + '_' + str(numID)
        pasteBin = addons.getSetting(pasteID)
        if pasteBin != '':
            cache.remove(pasteBin)

    dialog().VSinfo(addons.VSlang(30014))


# Forcer la mise à jour de tous les dossiers PasteBin
def refreshAllPaste():
    oGui = cGui()
    oGui.addText(SITE_IDENTIFIER, '[COLOR teal]Mise à jour des contenus  ..... [/COLOR]', 'download.png')
    oGui.setEndOfDirectory()
    
    xbmc.sleep(1000) # laisser le temps de voir que l'action a bien été prise en compte
    
    # le skin peut rappeler la fonction une deuxième fois, ne pas prendre en compte en vérifiant si on est revenu sur la home
    if not xbmc.getCondVisibility('Window.IsActive(home)'):
        PasteCache().delete()
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


# Retourne la liste des PasteBin depuis l'URL ou un groupe
def getPasteList(siteUrl, pasteID):
    addons = addon()

    IDs = []

    siteId = siteUrl.split(URL_MAIN)    # Supporte le format https://pastebin.com/raw/izu23hfkjhd
    if siteId[1]:
        IDs.append(siteId[1])

    if pasteID:
        prefixID = SETTING_PASTE_ID + str(pasteID)
        pasteBin = addons.getSetting(prefixID)
        if pasteBin and pasteBin not in IDs:
            IDs.append(pasteBin)
        for numID in range(1, PASTE_PAR_GROUPE):
            pasteID = prefixID + '_' + str(numID)
            pasteBin = addons.getSetting(pasteID)
            if pasteBin and pasteBin not in IDs:
                IDs.append(pasteBin)
    return IDs


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
    if pasteID == False:
        return
    if pasteID in IDs:          # ID déjà dans le groupe
        dialog().VSok(addons.VSlang(30082))
        return

    # Vérifier l'entete du Paste
    pbContentNew = PasteContent()

    try:
        movies = pbContentNew.getLines(pasteID)
        if len(movies) == 0:
            dialog().VSok(addons.VSlang(30022))
            return
    except Exception:
        dialog().VSinfo(addons.VSlang(30011))
        raise

    # Vérifier que les autres pastes du groupe ont le même format d'entete
    if len(IDs) > 0:
        pbContentOld = PasteContent()
        pbContentOld.getLines(IDs.pop())

        if not pbContentNew.isFormat(pbContentOld):
            dialog().VSok(addons.VSlang(30022))
            return

    addons.setSetting(settingID, pasteID)
    dialog().VSinfo(addons.VSlang(30042))

    oGui.updateDirectory()


# Liste de pastes avec possibilité de les supprimer
def adminPasteID():
    oGui = cGui()
    addons = addon()

    oGui.addText(SITE_IDENTIFIER, '[COLOR coral]Valider le code à retirer[/COLOR]', 'trash.png')

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')    # Numéro du dossier
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
        color = 'white' # Forcer une couleur évite aussi le nettoyage du "titre"
        try:
            movies = pbContentNew.getLines(pasteBin)
            if len(movies) == 0:
                color = 'red'
        except Exception:
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
    pasteID = oInputParameterHandler.getValue('pasteID')      # Numéro du dossier
    pasteDel = oInputParameterHandler.getValue('pasteBin')    # Paste

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
