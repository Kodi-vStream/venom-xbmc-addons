# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import time
import xbmcvfs
from resources.lib.comaddon import progress, addon, dialog, VSlog, VSPath, isMatrix, xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import Quote, cUtil, Unquote
import resources.sites.ianime as i
from resources.lib.tmdb import cTMDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2 

try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite


CACHE = 'special://home/userdata/addon_data/plugin.video.vstream/pastebin_cache.db'
# important seul xbmcvfs peux lire le special
if not isMatrix():
    REALCACHE = VSPath(CACHE).decode('utf-8')
else:
    REALCACHE = VSPath(CACHE)


SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'PasteBin'
SITE_DESC = 'Liste depuis pastebin'

URL_MAIN = 'https://pastebin.com/raw/'

KEY_PASTE_ID = 'PASTE_ID'
SETTING_PASTE_ID = 'pastebin_id_'
SETTING_PASTE_LABEL = 'pastebin_label_'
UNCLASSIFIED_GENRE = '_NON CLASSÉ_'
UNCLASSIFIED = 'Indéterminé'

URL_SEARCH_MOVIES = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=film&sSearch=', 'showSearchGlobal')
URL_SEARCH_SERIES = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=serie&sSearch=', 'showSearchGlobal')
URL_SEARCH_ANIMS = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=anime&sSearch=', 'showSearchGlobal')
URL_SEARCH_DIVERS = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=divers&sSearch=', 'showSearchGlobal')
FUNCTION_SEARCH = 'showSearchGlobal'


def getNbItemParPage():
    nbItem = addon().getSetting('pastebin_nbItemParPage')
    if not nbItem:
        nbItem = "25"
        addon().setSetting('pastebin_nbItemParPage', nbItem)
    return int(nbItem)

ITEM_PAR_PAGE = getNbItemParPage()
GROUPE_MAX = 50          # jusqu'à 50 dossiers, limitation du skin
PASTE_PAR_GROUPE = 100   # jusqu'à 100 liens pastebin par dossier


# Durée du cache, en Heures
def getCacheDuration():
    cacheDuration = addon().getSetting('pastebin_cacheDuration')
    if not cacheDuration:
        cacheDuration = "12"  # en heure
        addon().setSetting('pastebin_cacheDuration', cacheDuration)
    return int(cacheDuration)

CACHE_DURATION = getCacheDuration()



# Exemple
# CAT; TMDB; TITLE; SAISON; YEAR; GENRES; URLS=https://uptobox.com/
# film;714;Demain ne meurt jamais;James BOND;1997;['Action', 'Aventure', 'Thriller'];['nwxxxx','nwYYzz']
# serie;48866;Les 100;Saison 2; 2014; ['Fantastique', 'Aventure']; {'S02E01':['lien1', 'lien2'], 'S02E02':['lien1']}

# Exemple minimum
# CAT;TITLE; URLS
# film;Demain ne meurt jamais;['https://uptobox.com/nwxxxx']

class PasteBinContent:
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
    c = False       # Liste des liens, avec épisodes pour les séries
    HEBERGEUR = ''  # (optionnel) - URL de l'hebergeur, pour éviter de le mettre dans chaque URL, ex : 'https://uptobox.com/'  
    URLS = -1       # Liste des liens, avec épisodes pour les séries

    # Pour comparer deux pastes, savoir si les champs sont dans le même ordre 
    def isFormat(self, other): 
        if not isinstance(other, PasteBinContent):
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
    
    def getLines(self, pasteBin):
        
        #Lecture en cache
        sContent, self.c = self._cache_read(pasteBin)
        
        if sContent:
            lines = sContent.splitlines()
            entete = lines[0].split(";")

        # Lecture sur le site
        else:
            sUrl = URL_MAIN + pasteBin
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setTimeout(4)
            sContent = oRequestHandler.request()
            if sContent.startswith('<'):
                return []

            # test si paste accessible
            sContent, self.c = self.decompress(sContent)

            # Vérifie si la ligne d'entete existe avec les champs obligatoires
            lines = sContent.splitlines()
            entete = lines[0].split(";")
            if 'TITLE' not in entete and 'URL' not in entete:
                return []
            self._cache_save(pasteBin, sContent)

        # Calcul des index de chaque champ
        idx = 0
        for champ in entete:
            champ = champ.strip()
            
            if 'URL' in champ: # supporte URL ou URLS
                hebergeur = champ.split('=')
                champ = 'URLS'
                if len(hebergeur)>1:
                    self.HEBERGEUR = hebergeur[1].replace(' ','').replace('"','').replace('\'','')
            if champ in dir(self):
                setattr(self, champ, idx)
            idx +=1

        lines = [k.split(";") for k in lines[1:]]
        
        return lines

            
    def decompress(self, sContent):
        
        if sContent.startswith('CAT;'):
            return sContent, False
        
        sContent = sContent.decode('utf8')
        d = i.s.index(sContent[0])
        s =''
        for tx in sContent[1:].splitlines():
            tab = sorted(list(set([x for x in tx])))
            cr = [(tab[(tab.index(t) - d) % len(tab)]) for t in tx]
            s += ''.join(cr) + '\r\n'
            
        s = s.encode('utf8')
        return s, True
    
    
    """
    GESTION DU CACHE
    """

    def __init__(self):
    
        try:
            if not xbmcvfs.exists(CACHE):
                self.db = sqlite.connect(REALCACHE)
                self.db.row_factory = sqlite.Row
                self.dbcur = self.db.cursor()
                self.__createdb()
                return
        except:
            VSlog('Error: Unable to write on %s' % REALCACHE)
            pass
    
        try:
            self.db = sqlite.connect(REALCACHE)
            self.db.row_factory = sqlite.Row
            self.dbcur = self.db.cursor()
        except:
            VSlog('Error: Unable to connect to %s' % REALCACHE)
            pass
    
    def __createdb(self):
    
        sql_create = "CREATE TABLE IF NOT EXISTS pastebin ("\
                     "paste_id TEXT, "\
                     "date FLOAT, "\
                     "content BLOB,"\
                     "UNIQUE(paste_id)"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
        except:
            VSlog('Error: Cannot create table movie')
    
        self.dbcur.execute(sql_create)
        VSlog('table pastebin creee')
    
    def __del__(self):
        """ Cleanup db when object destroyed """
        try:
            self.dbcur.close()
            self.db.close()
        except:
            pass
    
    # Récupérer dans le cache
    def _cache_read(self, pasteID):
    
        try:
            sql_select = 'SELECT * FROM pastebin WHERE paste_id = \'%s\'' % pasteID
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
        except Exception as e:
            VSlog('************* Error selecting from cache db: %s' % e, 4)
            return None, False
    
        if matchedrow:
            data = dict(matchedrow)

            # Supprimer les données trop anciennes
            cacheDuration = time.time() - CACHE_DURATION * 3600
            if data['date'] < cacheDuration:
                self._cache_del(cacheDuration)
                return None, False
            
            # Utiliser les données du cache
            content = str(data['content'])
            if content[-1] == '.':
                return content[:-1], True
            return content, False
        else:
            return None, False
    
    # Sauvegarde des données dans un cache
    def _cache_save(self, pasteID, pasteContent):
    
        try:
            sql = 'INSERT INTO pastebin (paste_id, content, date) VALUES (?, ?, ?)'
            self.dbcur.execute(sql, (pasteID, buffer(pasteContent+'.' if self.c else pasteContent), time.time()))
            #buffer(zlib.compress(html))
            self.db.commit()
        except Exception as e:
            VSlog('SQL ERROR INSERT into table pastebin')
            pass
    
    
    # Suprimer les données trop anciennes
    def _cache_del(self, cacheDuration):
        
        try:
            sql_delete = 'DELETE FROM pastebin WHERE date < \'%s\'' % cacheDuration
            self.dbcur.execute(sql_delete)
            self.db.commit()
        except Exception as e:
            VSlog('************* Error deleting from cache db: %s' % e, 4)
            return None
    

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
    
    # Trie des listes par label
    pasteListe = sorted(pasteListe.items(), key=lambda paste: paste[0])

    if len(pasteListe)>0:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_MOVIES[0]
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_SERIES[0]
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)
    
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_ANIMS[0]
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)
    

    for pasteBin in pasteListe:
        pasteLabel = pasteBin[0]
        pasteID = pasteBin[1]
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showMenu')
        oGuiElement.setTitle(pasteLabel)
        oGuiElement.setIcon("mark.png")
        oGuiElement.setMeta(0)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('pasteID', pasteID)
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'deletePasteName', addons.VSlang(30412))
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
    

    # Menu pour ajouter un dossier (hors widget)
    if not xbmc.getCondVisibility('Window.IsActive(home)'):
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'addPasteName', '[COLOR coral]Ajouter un dossier PasteBin[/COLOR]', 'listes.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()


def showMenu():
    addons = addon()
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')
    sMedia = oInputParameterHandler.getValue('sMedia')

    pbContent = PasteBinContent()
    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    contenu = getPasteBin(pbContent, pasteBin)

    for numID in range(1, PASTE_PAR_GROUPE):
        pasteBin = addons.getSetting(prefixID + '_' + str(numID))
        contenu = contenu.union(getPasteBin(pbContent, pasteBin))
        
    if not sMedia:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('pasteID', pasteID)
        
        cnt = contenu.intersection(['containFilms', 'containSeries', 'containAnimes', 'containDivers'])
        if len(cnt) == 1:
            showDetailMenu(pasteID, contenu)
        else:
            if 'containFilms' in contenu:
                oOutputParameterHandler.addParameter('sMedia', 'film')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Films', 'films.png', oOutputParameterHandler)
        
            if 'containSeries' in contenu:
                oOutputParameterHandler.addParameter('sMedia', 'serie')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Séries', 'tv.png', oOutputParameterHandler)
            
            if 'containAnimes' in contenu:
                oOutputParameterHandler.addParameter('sMedia', 'anime')
                oGui.addDir(SITE_IDENTIFIER, 'showMenu', 'Animes', 'animes.png', oOutputParameterHandler)
        
        # Menu pour ajouter un lien (hors widget)
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            oGui.addDir(SITE_IDENTIFIER, 'addPasteID', '[COLOR coral]Ajouter un code PasteBin[/COLOR]', 'notes.png', oOutputParameterHandler)
            oGui.addDir(SITE_IDENTIFIER, 'adminPasteID', '[COLOR coral]Retirer un code PasteBin[/COLOR]', 'trash.png', oOutputParameterHandler)

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
    
    sUrl = URL_MAIN + '&numPage=1'#+ pasteBin
    if 'containFilms' in contenu:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_MOVIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if 'containFilmGenres' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    
        if 'containFilmGroupes' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Films (Listes)', 'genres.png', oOutputParameterHandler)
    
        if 'containFilmSaga' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showSaga', 'Films (Saga)', 'genres.png', oOutputParameterHandler)
    
        if 'containFilmYear' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Par années)', 'annees.png', oOutputParameterHandler)

        if 'containFilmRes' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showResolution', 'Films (Par résolutions)', 'hd.png', oOutputParameterHandler)

        if 'containFilmNetwork' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Films (Par diffuseurs)', 'host.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Films (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

        if 'containFilmReal' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showRealisateur', 'Films (Par réalisateurs)', 'actor.png', oOutputParameterHandler)

        if 'containFilmCast' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showCast', 'Films (Par acteurs)', 'actor.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&bRandom=True&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Aléatoires)', 'news.png', oOutputParameterHandler)


    if 'containSeries' in contenu:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_SERIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

        if 'containSerieGroupes' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Séries (Listes)', 'genres.png', oOutputParameterHandler)
    
        if 'containSerieNetwork' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'host.png', oOutputParameterHandler)
    
        if 'containSerieYear' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Séries (Ordre alphabétique)', 'az.png', oOutputParameterHandler)


    if 'containAnimes' in contenu:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_ANIMS[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Animes (Genres)', 'genres.png', oOutputParameterHandler)

        if 'containAnimeGroupes' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Animes (Listes)', 'genres.png', oOutputParameterHandler)
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Animes (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)
    
    if 'containDivers' in contenu:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_DIVERS[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Divers)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Divers (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if 'containDiversGenres' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Divers (Catégories)', 'genres.png', oOutputParameterHandler)

        if 'containDiversGroupes' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Divers (Listes)', 'genres.png', oOutputParameterHandler)
    
        if 'containDiversYear' in contenu:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Divers (Par années)', 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=divers&pasteID=' + pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Divers (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)
    


# Etablir les menus en fonction du contenu
def getPasteBin(pbContent, pasteBin):

    containList = set()
    
    if not pasteBin:
        return containList
    
    movies = pbContent.getLines(pasteBin)

    # Calculer les menus
    for movie in movies:
        if pbContent.CAT == -1 or 'film' in movie[pbContent.CAT]:
            containList.add('containFilms')
            if pbContent.GENRES>=0 and len(movie[pbContent.GENRES].strip())>2:
                containList.add('containFilmGenres')
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip())>0:
                containList.add('containFilmGroupes')
            if pbContent.YEAR>=0 and len(movie[pbContent.YEAR].strip())>1:
                containList.add('containFilmYear')
            if pbContent.RES>=0 and len(movie[pbContent.RES].replace('[', '').replace(']', '').replace(',', '').strip())>0:
                containList.add('containFilmRes')
            if pbContent.DIRECTOR>=0 and len(movie[pbContent.DIRECTOR].replace('[', '').replace(']', '').replace(',', '').strip())>0:
                containList.add('containFilmReal')
            if pbContent.CAST>=0 and len(movie[pbContent.CAST].replace('[', '').replace(']', '').replace(',', '').strip())>0:
                containList.add('containFilmCast')
            if pbContent.SAISON>=0 and len(movie[pbContent.SAISON].strip())>0:
                containList.add('containFilmSaga')
            if pbContent.NETWORK>=0 and len(movie[pbContent.NETWORK].replace('[', '').replace(']', '').strip())>0:
                containList.add('containFilmNetwork')

        elif 'serie' in movie[pbContent.CAT]:
            containList.add('containSeries')
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip())>0:
                containList.add('containSerieGroupes')
            if pbContent.NETWORK>=0 and len(movie[pbContent.NETWORK].replace('[', '').replace(']', '').strip())>0:
                containList.add('containSerieNetwork')
            if pbContent.YEAR>=0 and len(movie[pbContent.YEAR].strip())>1:
                containList.add('containSerieYear')

        elif 'anime' in movie[pbContent.CAT]:
            containList.add('containAnimes')
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip())>0:
                containList.add('containAnimeGroupes')

        elif 'divers' in movie[pbContent.CAT]:
            containList.add('containDivers')
            if pbContent.GENRES>=0 and len(movie[pbContent.GENRES].strip())>2:
                containList.add('containDiversGenres')
            if pbContent.YEAR>=0 and len(movie[pbContent.YEAR].strip())>1:
                containList.add('containDiversYear')
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip())>0:
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

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    listeIDs = getPasteList(sUrl, pasteID)
    
    genres = {}
    for pasteBin in listeIDs:

        pbContent = PasteBinContent()
        movies = pbContent.getLines(pasteBin)
    
        for movie in movies:
            if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
                continue
    
            genre = movie[pbContent.GENRES].strip()
            if not genre or genre == '':
                genre = "['"+UNCLASSIFIED_GENRE+"']"
            elif "''" in genre:
                genre = genre.replace("''", "'"+UNCLASSIFIED_GENRE+"'")
            genre = eval(genre)
            if isinstance(genre, int):
                genre = [genre]
            if genre:
                for g in genre:
                    sDisplayGenre = g
                    if str(g).isdigit():
                        sDisplayGenre = tmdb.getGenreFromID(g)
                    if not sDisplayGenre in genres:
                        genres[sDisplayGenre] = g
    
    genreKeys = genres.keys()
    for sDisplayGenre in sorted(genreKeys):
        genre = genres.get(sDisplayGenre)
        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = siteUrl + '&sGenre=' + str(genre)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showNetwork():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    listNetwork = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
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

    for networkName, networkId in sorted(listNetwork.items()):
        progress_.VSupdate(progress_, maxProgress)
        if progress_.iscanceled():
            break

        sUrl = siteUrl + '&sNetwork=' + networkId + ":" + networkName.replace('+', '|')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', networkId)    # Utilisé par TMDB
        oGui.addNetwork(SITE_IDENTIFIER, 'showMovies', networkName, 'host.png', oOutputParameterHandler)
    progress_.VSclose(progress_)
    
    oGui.setEndOfDirectory()

def showRealisateur():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
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

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    listReal = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        reals = movie[pbContent.DIRECTOR].strip()
        if reals != '':
            reals = eval(reals)
            if reals:
                for real in reals:
                    if ':' in real:
                        realId, realName  = real.split(':')
                        if realName not in listReal:
                            listReal[realName] = realId

    nbItem = 0
    index = 0
    maxProgress = min(len(listReal), ITEM_PAR_PAGE)
    progress_ = progress().VScreate(SITE_NAME)

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
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', realId)    # Utilisé par TMDB
        oGui.addPerson(SITE_IDENTIFIER, 'showMovies', realName, 'actor.png', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(listReal) :
            numPage += 1
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oOutputParameterHandler.addParameter('numItem', numItem)
            oGui.addNext(SITE_IDENTIFIER, 'showRealisateur', '[COLOR teal]Page ' + str(numPage) + ' >>>[/COLOR]', oOutputParameterHandler)
            break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showCast():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    if not numPage and 'numPage' in aParams : numPage = aParams['numPage']

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    listActeur = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
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
    if numPage>1 and numItem == 0:  # choix d'une page
        numItem = (numPage-1) * ITEM_PAR_PAGE
        if numItem > len(listActeur):   # accès direct à la dernière page
            numPage = len(listActeur) / ITEM_PAR_PAGE
            numItem = (numPage-1) * ITEM_PAR_PAGE

    nbItem = 0
    index = 0
    maxProgress = min(len(listActeur), ITEM_PAR_PAGE)
    progress_ = progress().VScreate(SITE_NAME)

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
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', acteurId)    # Utilisé par TMDB
        oGui.addPerson(SITE_IDENTIFIER, 'showMovies', acteurName, 'actor.png', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(listActeur) :
            numPage += 1
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oOutputParameterHandler.addParameter('numItem', numItem)
            oGui.addNext(SITE_IDENTIFIER, 'showCast', '[COLOR teal]Page ' + str(numPage) + ' >>>[/COLOR]', oOutputParameterHandler)
            break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showGroupes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    sousGroupe = set()
    groupesPerso = set()
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue
        groupe = movie[pbContent.GROUPES].strip().replace("''",'')
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

    groupes = groupesPerso.union(sousGroupe)
    for sGroupe in sorted(groupes):
        sUrl = siteUrl + '&sGroupe=' + sGroupe
        oOutputParameterHandler = cOutputParameterHandler()
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

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    sGroupe = aParams['sGroupe'].replace('+', ' ') + ':' if 'sGroupe' in aParams else None

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    groupes = set()
    if sGroupe:
        for movie in movies:
            groupe = movie[pbContent.GROUPES].strip().replace("''",'')
            if groupe:
                groupe = eval(groupe)
                if groupe:
                    for gr in groupe:
                        if gr.startswith(sGroupe):
                            groupes.add(gr)

    for sGroupe in sorted(groupes):
        sUrl = siteUrl + '&sGroupe=' + sGroupe.replace('+', '|')
        oOutputParameterHandler = cOutputParameterHandler()
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

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    if not numPage and 'numPage' in aParams : numPage = aParams['numPage']

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    sagas = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        saga = movie[pbContent.SAISON].strip()
        if saga != '':
            sTmdbId = name = saga
            idName = saga.split(':', 1)
            if len(idName)>1:
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
    if numPage>1 and numItem == 0:  # choix d'une page
        numItem = (numPage-1) * ITEM_PAR_PAGE
        if numItem > len(sagas):   # accès direct à la dernière page
            numPage = len(sagas) / ITEM_PAR_PAGE
            numItem = (numPage-1) * ITEM_PAR_PAGE

    nbItem = 0
    index = 0
    progress_ = progress().VScreate(SITE_NAME)
    names = sagas.keys()
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

        oOutputParameterHandler = cOutputParameterHandler()
        if sTmdbId.isdigit():
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)    # Utilisé par TMDB
            sUrl = siteUrl + '&sSaga=' + sTmdbId + ':' + sSagaName
        else:
            sUrl = siteUrl + '&sSaga=' + sSagaName
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        
        sDisplaySaga = sSagaName
        sSagaName = sSagaName.replace('[', '').replace(']', '')   # Exemple pour le film [REC], les crochets sont génant pour certaines fonctions
        if not sSagaName.lower().endswith('saga'):
            sSagaName = sSagaName + " Saga"
        oOutputParameterHandler.addParameter('sMovieTitle', sSagaName)
        
        oGui.addMoviePack(SITE_IDENTIFIER, 'showMovies', sDisplaySaga, 'genres.png', '', '', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(names) :
            numPage += 1
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oOutputParameterHandler.addParameter('numItem', numItem)
            oGui.addNext(SITE_IDENTIFIER, 'showSaga', '[COLOR teal]Page ' + str(numPage) + ' >>>[/COLOR]', oOutputParameterHandler)
            break


    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    years = set()
    for line in movies:
        if pbContent.CAT >=0 and sMedia not in line[pbContent.CAT]:
            continue

        year = line[pbContent.YEAR].strip()
        if not year:
            year = UNCLASSIFIED
        years.add(year)

    for sYear in sorted(years, reverse=True):
        sUrl = siteUrl + '&sYear=' + sYear
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'years.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showResolution():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    resolutions = set()
    for line in movies:
        if pbContent.CAT >=0 and sMedia not in line[pbContent.CAT]:
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

        if not res or res == '[]' : resolutions.add(UNCLASSIFIED)

    resolutions.discard('')
    
    # Trie des rsolutions
    resOrder = ['8K','4K','1080P', '720P', '576P', '540P', '480P', '360P']
    def trie_res(key):
        if key == UNCLASSIFIED:
            return 20
        key = key.replace('p', 'P')
        if key not in resOrder:
            resOrder.append(key)
        return resOrder.index(key)
    
    resolutions = sorted(resolutions, key=trie_res)

    for sRes in resolutions:
        if sRes == '': continue

        sDisplayRes = sRes
        if sDisplayRes.isdigit(): sDisplayRes += 'p'
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
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayRes, 'hd.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def AlphaList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    for i in range(0, 36):
        if (i < 10):
            sLetter = chr(48 + i)
        else:
            sLetter = chr(65 + i -10)

        sUrl = siteUrl + '&sAlpha=' + sLetter

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] Lettre [COLOR red]' + sLetter + '[/COLOR][/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    sMedia = 'film' # Par défaut
    pasteID = sGenre = sSaga = sGroupe = sYear = sRes = sAlpha = sNetwork = sDirector = sCast = None
    bRandom = False
    
    if sSearch:
        siteUrl = sSearch

    sSearchTitle = ''
    
    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')
    
    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))

    if 'pasteID' in aParams: pasteID = aParams['pasteID']
    if 'sMedia' in aParams: sMedia = aParams['sMedia']
    if 'sSearch' in aParams: sSearchTitle = Unquote(aParams['sSearch']).replace(' | ', ' & ')
    if 'sGenre' in aParams: sGenre = aParams['sGenre'].replace(' | ', ' & ')
    if 'sSaga' in aParams:
        sSaga = aParams['sSaga'].replace(' | ', ' & ')
    if 'sGroupe' in aParams: sGroupe = aParams['sGroupe'].replace(' | ', ' & ')
    if 'sYear' in aParams: sYear = aParams['sYear']
    if 'sRes' in aParams: sRes = aParams['sRes']
    if 'sAlpha' in aParams: sAlpha = aParams['sAlpha']
    if 'sNetwork' in aParams: sNetwork = aParams['sNetwork']
    if 'sDirector' in aParams: sDirector = aParams['sDirector']
    if 'sCast' in aParams: sCast = aParams['sCast']
    if 'bRandom' in aParams: bRandom = aParams['bRandom']
    if not numPage and 'numPage' in aParams : numPage = aParams['numPage']

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

    # Recherche par ordre alphabetique => le tableau doit être trié
    if sAlpha:
        movies = sorted(movies, key=lambda line: line[pbContent.TITLE])
        
    # Recherche par saga => trie par années
    if sSaga and pbContent.YEAR>=0:
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
    if numPage>1 and numItem == 0:  # choix d'une page
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
        if sGenre and pbContent.GENRES >=0 :
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
        if sDirector and pbContent.DIRECTOR >= 0 :
            listDirector = movie[pbContent.DIRECTOR].strip()
            if not listDirector:
                continue
            listDirector = eval(listDirector)
            if sDirector not in listDirector:
                continue

        # Filtrage par acteur
        if sCast and pbContent.CAST >=0 :
            listCast = movie[pbContent.CAST].strip()
            if not listCast:
                continue
            listCast = eval(listCast)
            if sCast not in listCast:
                continue

        # Filtrage par diffuseur
        if sNetwork and pbContent.NETWORK >= 0 :
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
            if pbContent.RES>=0:
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
        if sMedia : sUrl += '&sMedia=' + sMedia
        if pasteID: sUrl += '&pasteID=' + pasteID
        if movieYear : sUrl += '&sYear=' + movieYear
        if sTmdbId: sUrl += '&idTMDB=' + sTmdbId
        if sRes: sUrl += '&sRes=' + sRes
        sUrl += '&sTitle=' + sTitle
        
        # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
        sTitle = sTitle.replace('+', ' ').replace(' & ', ' | ')
        sTitle = sTitle.replace('[', '').replace(']', '')   # Exemple pour le film [REC], les crochets sont génants pour certaines fonctions

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        if sTmdbId: oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)    # Utilisé par TMDB
        if movieYear : oOutputParameterHandler.addParameter('sYear', movieYear) # Utilisé par TMDB
        if listRes: oOutputParameterHandler.addParameter('listRes', listRes)

        if sMedia == 'serie':
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        elif sMedia == 'anime':
            oGui.addAnime(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'animes.png', '', '', oOutputParameterHandler)
        elif sMedia == 'divers':
            oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'doc.png', oOutputParameterHandler)
        else:
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if not sSearch:
 
            if nbItem % ITEM_PAR_PAGE == 0 and numPage*ITEM_PAR_PAGE < len(movies) :
                numPage += 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('numPage', numPage)
                oOutputParameterHandler.addParameter('numItem', numItem)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(numPage) + ' >>>[/COLOR]', oOutputParameterHandler)
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

    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'serie'

    saisons = {}
    listeIDs = getPasteList(sUrl, pasteID)
    pbContent = PasteBinContent()
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)

        # Recherche les saisons de la série
        for serie in moviesBin:
            
            if pbContent.CAT >=0 and sMedia not in serie[pbContent.CAT]:
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
    saisons = sorted(saisons.items(), key=lambda saison: saison[0])
    for sSaison, res in saisons:

        sDisplaySaison = sSaison
        if sSaison.isdigit():
            sDisplaySaison = 'S{:02d}'.format(int(sSaison))
        
        if len(res) == 0:
            sUrl = siteUrl + '&sSaison=' + sSaison
            sDisplayTitle = searchTitle + ' - ' + sDisplaySaison
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas le sTitre afin de pouvoir mettre la saison en marque-page
            oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodesLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        else:
            for resolution in res:
                sUrl = siteUrl + '&sSaison=' + sSaison + '&sRes=' + resolution
                sDisplayTitle = ('%s %s [%s]') % (searchTitle, sDisplaySaison, resolution)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas le sTitre afin de pouvoir mettre la saison en marque-page
                oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodesLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodesLinks(siteUrl = ''):
    oGui = cGui()
    
    if not siteUrl:    
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
    
    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')
    params = sUrl.split('&',1)[1]
    aParams = dict(param.split('=') for param in params.split('&'))
    sSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    sRes = aParams['sRes'] if 'sRes' in aParams else None
    searchTitle = aParams['sTitle'].replace(' | ', ' & ')
 
    if not sSaison:
        oGui.setEndOfDirectory()
        return
 
    lines, listRes = getHosterList(siteUrl)
    if len(listRes) != len (lines):
        listRes = None

    listeEpisodes = []
    resIdx = 0
    for episode in lines:
        if listRes:
            res = listRes[resIdx]
            resIdx += 1
            if sRes != res:
                continue
        for numEpisode in episode.keys():
            if not numEpisode in listeEpisodes:
                listeEpisodes.append(numEpisode)
 
    sDisplaySaison = sSaison
    if sSaison.isdigit():
        sDisplaySaison = 'S{:02d}'.format(int(sSaison))

    for episode in sorted(listeEpisodes):
        sUrl = siteUrl + '&sEpisode=' + str(episode)

        if str(episode).isdigit():
            episode = '{}E{:02d}'.format(sDisplaySaison, int(episode))
        else:
            episode = '{}{}'.format(sDisplaySaison, episode)
        sDisplayTitle = searchTitle + ' - ' + episode
 
        oOutputParameterHandler = cOutputParameterHandler()
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
    params = sUrl.split('&',1)[1]
    aParams = dict(param.split('=') for param in params.split('&'))
    sRes = aParams['sRes'] if 'sRes' in aParams else None

    listHoster, listRes = getHosterList(siteUrl)    

    if len(listRes) != len (listHoster):
        listRes = None

    resIdx = 0
    for sHosterUrl in listHoster:

        if not sHosterUrl.startswith('http'):
            sHosterUrl += 'http://'+ sHosterUrl

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            
            if listRes:
                res = listRes[resIdx]
                resIdx += 1
                # Filtre la résolution
                if sRes and sRes != res:
                    continue
                
                if res.isdigit(): res += 'p'
                res = res.replace('P', 'p').replace('1080p', 'fullHD').replace('720p', 'HD').replace('2160p', '4K')
                sDisplayName = sTitle
                if res: sDisplayName += ' [%s]' %res
            else:
                sDisplayName = sTitle

            oHoster.setDisplayName(sDisplayName)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()

# Retrouve tous les liens disponibles pour un film, ou un épisode, gère les groupes multipaste
def getHosterList(siteUrl):
    # Pour supporter les caracteres '&' et '+' dans les noms alors qu'ils sont réservés
    sUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')

    siteUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    searchYear = aParams['sYear'] if 'sYear' in aParams else None
    searchSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchEpisode = aParams['sEpisode'] if 'sEpisode' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    searchTitle = aParams['sTitle'].replace(' | ', ' & ')

    pbContent=p = PasteBinContent()
    listHoster = []
    listRes = []
    movies = []
    listeIDs = getPasteList(siteUrl, pasteID)
    for pasteBin in listeIDs:
        moviesBin = pbContent.getLines(pasteBin)
        movies += moviesBin

        for movie in moviesBin:
    
            # Filtrer par catégorie
            if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
                continue
    
            # Filtrage par saison
            if searchSaison and pbContent.SAISON >= 0:
                sSaisons = movie[pbContent.SAISON].strip()
                if sSaisons and searchSaison != sSaisons:
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
    
            links = movie[pbContent.URLS]

            # numérotation des épisodes 08 -> 8 (problème de décodage en octal)
            if "{" in links:
                links = links.replace('{0', '{').replace('{:', '{0:').replace(',0', ',')

            listLinks = []

            if "[" in links or "{" in links:
                links = eval(links)
            if isinstance(links, list):
                for l in links:
                    listLinks.append(''.join([chr(ord(x)^31) for x in l]) if p.c else l)
            elif isinstance(links, dict):
                if searchEpisode:
                    for numEpisode, link in links.items():
                        if str(numEpisode) == searchEpisode:
                            listLinks.append(''.join([chr(ord(x)^31) for x in link]) if p.c else link)
                            break
                else:
                    listHoster.append(links)
            else:
                listLinks.append(links)
    
            if pbContent.HEBERGEUR:
                listLinks = [(pbContent.HEBERGEUR + link) for link in listLinks]
                
            listHoster.extend(listLinks)
                    
            # Retrouve les résolutions pour les films
            if pbContent.RES >= 0 and 'film' in sMedia:
                res = movie[pbContent.RES].strip()
                if '[' in res:
                    listRes.extend(eval(res))
                else:
                    listRes.append(res)
                if len(listRes) < len(links):  # On complete les résolutions manquantes
                    for _ in range(len(links) - len(listRes)):
                        listRes.append('')
    
            # Retrouve les résolutions pour les séries
            if pbContent.RES >= 0 and 'serie' in sMedia:
                res = movie[pbContent.RES].strip()
                if '[' in res:
                    listRes.extend(eval(res))
                else:
                    listRes.append(res)

    # Supprime les doublons en gardant l'ordre
#     links = [links.extend(elem) for elem in listHoster if not elem in links]

    return listHoster, listRes
    

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
    
    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')

    labelSetting = SETTING_PASTE_LABEL + pasteID
    addons.setSetting(labelSetting, '')

    prefixID = SETTING_PASTE_ID + str(pasteID)
    addons.setSetting(prefixID, '')

    for numID in range(1, PASTE_PAR_GROUPE):
        pasteID = prefixID + '_' + str(numID)
        if addons.getSetting(pasteID):
            addons.setSetting(pasteID, '')

    cGui().updateDirectory()



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
        IDs.add(pasteBin)           # IDs déjà renseigné
    if pasteBin == '':
        settingID = prefixID
    for numID in range(1, PASTE_PAR_GROUPE):
        pasteID = prefixID + '_' + str(numID)
        pasteBin = addons.getSetting(pasteID)
        if pasteBin != '':
            IDs.add(pasteBin)        # IDs déjà renseigné
        elif not settingID:
            settingID = pasteID
     
    # Demande de l'id PasteBin
    pasteID = oGui.showKeyBoard('', "[COLOR coral]Saisir l'ID du PasteBin[/COLOR]")
    if pasteID == False:
        return
    if pasteID in IDs:              # ID déjà dans le groupe
        dialog().VSok(addons.VSlang(30082))
        return
 
    # Vérifier l'entete du Paste
    pbContentNew = PasteBinContent()

    try:
        movies = pbContentNew.getLines(pasteID)
        if len(movies) == 0 :
            dialog().VSok(addons.VSlang(30022))
            return
    except Exception:
        dialog().VSinfo(addons.VSlang(30011))
        raise
    
    # Vérifier que les autres pastes du groupe ont le même format d'entete
    if len(IDs)>0:
        pbContentOld = PasteBinContent()
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

    pbContentNew = PasteBinContent()
    for numID in range(0, PASTE_PAR_GROUPE):
        if numID == 0 :
            pasteBin = addons.getSetting(prefixID)
        else:
            pasteBin = addons.getSetting(prefixID + '_' + str(numID))
        if not pasteBin:
            continue
     
        # Vérifier la qualité du Paste
        color = 'white' # Forcer une couleur évite aussi le nettoyage du "titre" 
        try:
            movies = pbContentNew.getLines(pasteBin)
            if len(movies) == 0 :
                color = 'red'
        except Exception:
            dialog().VSinfo(addons.VSlang(30011))
            raise

        pasteLabel = '[COLOR %s]%s[/COLOR]' % (color, pasteBin)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('pasteID', pasteID)
        oOutputParameterHandler.addParameter('pasteBin', pasteBin)
        oGui.addDir(SITE_IDENTIFIER, 'deletePasteID', pasteLabel, 'trash.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Suppression d'un paste dans un dossier
def deletePasteID():
    
    addons = addon()
    if not dialog().VSyesno(addons.VSlang(30456)):
        return

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')      # Numéro du dossier
    pasteDel = oInputParameterHandler.getValue('pasteBin')    # Paste

    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    if pasteDel == pasteBin:
        addons.setSetting(prefixID, '')
    else:
        for numID in range(1, PASTE_PAR_GROUPE):
            pasteID = prefixID + '_' + str(numID)
            pasteBin = addons.getSetting(pasteID)
            if pasteDel == pasteBin:
                addons.setSetting(pasteID, '')
                break
    
    dialog().VSinfo(addons.VSlang(30072))
    
    cGui().updateDirectory()


