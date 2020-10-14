# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import progress, addon, dialog 
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tmdb import cTMDb
from resources.lib.util import Quote, cUtil, Unquote

import random

SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'PasteBin'
SITE_DESC = 'Liste depuis pastebin'

URL_MAIN = 'https://pastebin.com/raw/'

KEY_PASTE_ID = 'PASTE_ID'
SETTING_PASTE_ID = 'pastebin_id_'
SETTING_PASTE_LABEL = 'pastebin_label_'
UNCLASSIFIED_GENRE = '_NON CLASSÉ_'
UNCLASSIFIED_RESOLUTION = 'Indéterminé'

URL_SEARCH_MOVIES = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=film&sSearch=', 'showSearchGlobal')
URL_SEARCH_SERIES = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=serie&sSearch=', 'showSearchGlobal')
URL_SEARCH_ANIMS = (URL_MAIN + '&pasteID=' + KEY_PASTE_ID + '&sMedia=anime&sSearch=', 'showSearchGlobal')
FUNCTION_SEARCH = 'showSearchGlobal'


def getNbItemParPage():
    nbItem = addon().getSetting('pastebin_nbItemParPage')
    if nbItem:
        return int(nbItem)
    return 25

ITEM_PAR_PAGE = getNbItemParPage()
PASTE_PAR_GROUPE = 50   # jusqu'à 50 groupes de paste, chaque groupe peut contenir jusqu'à 50 liens pastebin

# Exemple
# CAT; TMDB; TITLE; SAISON; YEAR; GENRES; URLS=https://uptobox.com/
# film;714;Demain ne meurt jamais;James BOND;1997;['Action', 'Aventure', 'Thriller'];['nwxxxx','nwYYzz']
# serie;48866;Les 100;Saison 2; 2014; ['Fantastique', 'Aventure']; {'S02E01':['lien1', 'lien2'], 'S02E02':['lien1']}

# Exemple minimum
# TITLE; URLS
# Demain ne meurt jamais;['https://uptobox.com/nwxxxx']

class PasteBinContent:
    CAT = -1     # (Optionnel) - Catégorie 'film', 'serie' 'anime' (Film par défaut)
    TMDB = -1    # (optionnel) - Id TMDB
    TITLE = -1   # Titre du film / épisodes
    SAISON = -1  # (optionnel) - Saison pour les séries (ex 'Saison 03' ou 'S03' ou '03') OU Saga pour les films (ex 'Mission impossible')
    GROUPES = -1 # (optionnel) - Groupes tel que NETFLIX, HBO, MARVEL, DISNEY, Films enfants, ...
    YEAR = -1    # (optionnel) - Année
    GENRES = -1  # (optionnel) - Liste des genres
    RES = -1     # (optionnel) - Résolution (720p, 1080p, 4K, ...)
    DIRECTOR = -1#  (optionnel) - Réalisateur au format id:nom
    CAST = -1   #  (optionnel) - Acteurs au format id:nom
    NETWORK = -1   #  (optionnel) - Diffuseur au format id:nom
    URLS = -1    # Liste des liens, avec épisodes pour les séries
    HEBERGEUR = '' # (optionnel) - URL de l'hebergeur, pour éviter de le mettre dans chaque URL, ex : 'https://uptobox.com/'  

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
    
    def getLines(self, sContent):
        lines = sContent.splitlines()

        # Vérifie si la ligne d'entete existe avec les champs obligatoires
        entete = lines[0].split(";")
        if 'TITLE' not in entete and 'URLS' not in entete:
            return []

        # Calcul des index de chaque champ
        idx = 0
        for champ in entete:
            champ = champ.strip()
            
            if 'URL' in champ: # supporte URL ou URLS
                hebergeur = champ.split('=')
                champ = 'URLS'
                if len(hebergeur)>1:
                    self.HEBERGEUR = hebergeur[1].replace(' ','').replace('"','').replace('\'','')
                    if not self.HEBERGEUR.endswith('/'):
                        self.HEBERGEUR += '/'
            if champ in dir(self):
                setattr(self, champ, idx)
            idx +=1

        lines = [k.split(";") for k in lines[1:]]
        
        
        # Reconstruire les liens
        if self.HEBERGEUR:
            for line in lines:
                sHost = line[self.URLS]
                if "{" in sHost:
                    sUrl = eval(sHost)
                    for link in sUrl.keys():
                        sUrl[link] = self.HEBERGEUR + sUrl[link] 
                elif "[" in sHost:
                    sHost = eval(sHost)
                    sUrl = [(self.HEBERGEUR + link) for link in sHost]
                else:
                    sUrl = self.HEBERGEUR + sHost
                line[self.URLS] = sUrl
        
        return lines


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
    

    # Menu pour ajouter un lien
    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'addPasteName', '[COLOR coral]Ajouter un dossier PasteBin[/COLOR]', 'listes.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()


def showMenu():
    addons = addon()
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')

    prefixID = SETTING_PASTE_ID + str(pasteID)
    pasteBin = addons.getSetting(prefixID)
    contenu = getPasteBin(pasteBin)

    for numID in range(1, PASTE_PAR_GROUPE):
        pasteBin = addons.getSetting(prefixID + '_' + str(numID))
        contenu = contenu.union(getPasteBin(pasteBin))

    sUrl = URL_MAIN #+ pasteBin
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
            oGui.addDir(SITE_IDENTIFIER, 'showNetwork', 'Séries (Par diffuseurs)', 'genres.png', oOutputParameterHandler)
    
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
    

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('pasteID', pasteID)
    oGui.addDir(SITE_IDENTIFIER, 'addPasteID', '[COLOR coral]Ajouter un lien PasteBin[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getPasteBin(pasteBin):

    containList = set()
    
    if not pasteBin:
        return containList
    
    # Etablir les menus en fonction du contenu
    sUrl = URL_MAIN + pasteBin
    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

    # Calculer les menus
    for movie in movies:
        if pbContent.CAT == -1 or 'film' in movie[pbContent.CAT]:
            containList.add('containFilms')
            if pbContent.GENRES>=0 and len(movie[pbContent.GENRES].strip())>0:
                containList.add('containFilmGenres')
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip())>0:
                containList.add('containFilmGroupes')
            if pbContent.YEAR>=0 and len(movie[pbContent.YEAR].strip())>0:
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

        elif 'anime' in movie[pbContent.CAT]:
            containList.add('containAnimes')
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].replace('[', '').replace(']', '').strip())>0:
                containList.add('containAnimeGroupes')
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

    for numID in range(1, PASTE_PAR_GROUPE):
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

        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        sContent = oRequestHandler.request()
        pbContent = PasteBinContent()
        movies = pbContent.getLines(sContent)
    
        for movie in movies:
            if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
                continue
    
            genre = movie[pbContent.GENRES].strip()
            if not genre or genre == '':
                genre = "['"+UNCLASSIFIED_GENRE+"']"
            elif "''" in genre:
                genre = genre.replace("''", "'"+UNCLASSIFIED_GENRE+"'")
            genre = eval(genre)
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
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
        movies += moviesBin

    listNetwork = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        networks = movie[pbContent.NETWORK].strip()
        if networks <> '':
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
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
        movies += moviesBin

    listReal = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        reals = movie[pbContent.DIRECTOR].strip()
        if reals <> '':
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
        if nbItem % ITEM_PAR_PAGE == 0:
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
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
        movies += moviesBin

    listActeur = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        acteurs = movie[pbContent.CAST].strip()
        if acteurs <> '':
            acteurs = eval(acteurs)
            if acteurs:
                for acteur in acteurs:
                    if ':' in acteur:
                        acteurId, acteurName = acteur.split(':')
                        if acteurName not in listActeur:
                            listActeur[acteurName] = acteurId

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
        if nbItem % ITEM_PAR_PAGE == 0:
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
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
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
    sGroupe = aParams['sGroupe'] + ':' if 'sGroupe' in aParams else None

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
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

    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
        movies += moviesBin

    sagas = {}
    for movie in movies:
        if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
            continue

        saga = movie[pbContent.SAISON].strip()
        if saga <> '':
            sTmdbId = name = saga
            idName = saga.split(':', 1)
            if len(idName)>1:
                sTmdbId = idName[0]
                name = idName[1]
            if sTmdbId.isdigit():
                sagas[name] = sTmdbId
            else:
                sagas[saga] = saga
            
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
        if nbItem % ITEM_PAR_PAGE == 0:
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
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
        movies += moviesBin

    years = set()
    for line in movies:
        if pbContent.CAT >=0 and sMedia not in line[pbContent.CAT]:
            continue

        year = line[pbContent.YEAR].strip()
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
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
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
                    resolutions.add(UNCLASSIFIED_RESOLUTION)
        else:
            resolutions.add(res)

        if not res or res == '[]' : resolutions.add(UNCLASSIFIED_RESOLUTION)

    resolutions.discard('')
    
    # Trie des rsolutions
    resOrder = ['8K','4K','1080P', '1080p', '720P', '720p', '576p', '540P', '540p', '480P', '480p', '360P', '360p']
    def trie_res(key):
        if key == UNCLASSIFIED_RESOLUTION:
            return 20
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
            .replace('1080p', 'HD [1080p]')\
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

    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

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

    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(sUrl, pasteID)
    for pasteBin in listeIDs:
        oRequestHandler = cRequestHandler(URL_MAIN + pasteBin)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
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

    if bRandom:
        numItem = 0
        randoms = [random.randint(0, len(movies)) for _ in range(ITEM_PAR_PAGE)]
    
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

        # l'ID TMDB
        sTmdbId = None
        if pbContent.TMDB >= 0:
            sTmdbId = movie[pbContent.TMDB].strip()
            if sTmdbId in movieIds:
                continue            # Filtre des doublons
            movieIds.add(sTmdbId)

        # Filtrage par titre
        sTitle = movie[pbContent.TITLE].strip()
        
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
        if pbContent.YEAR >= 0:
            movieYear = movie[pbContent.YEAR].strip()
            if sYear:
                if not movieYear or sYear != movieYear:
                    continue
                # sDisplayTitle = '%s (%s)' % (sTitle, movieYear)

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
                if sRes == UNCLASSIFIED_RESOLUTION:
                    if '' not in listRes:
                        continue
                elif sRes not in listRes:
                    continue
        
        nbItem += 1
        progress_.VSupdate(progress_, ITEM_PAR_PAGE)
        if progress_.iscanceled():
            break

        if sMedia : sUrl += '&sMedia=' + sMedia
        if pasteID: sUrl += '&pasteID=' + pasteID
        if movieYear : sUrl += '&sYear=' + movieYear
        if sTmdbId: sUrl += '&idTMDB=' + sTmdbId
        sUrl += '&sTitle=' + sTitle
        
        sTitle = sTitle.replace('[', '').replace(']', '')   # Exemple pour le film [REC], les crochets sont génants pour certaines fonctions

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        if listRes: oOutputParameterHandler.addParameter('listRes', listRes)

        if sMedia == 'serie':
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        elif sMedia == 'anime':
            oGui.addAnime(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'animes.png', '', '', oOutputParameterHandler)
        else:
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if not sSearch:
            if nbItem % ITEM_PAR_PAGE == 0:
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

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None

    saisons = []
    listeIDs = getPasteList(sUrl, pasteID)
    pbContent = PasteBinContent()
    for pasteBin in listeIDs:
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)

        # Recherche les saisons de la série
        for serie in moviesBin:
            
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
                if pbContent.CAT >= 0 and 'serie' not in serie[pbContent.CAT]:
                    continue
                if searchYear and pbContent.YEAR >= 0:
                    sYear = serie[pbContent.YEAR].strip()
                    if sYear and sYear != searchYear:
                        continue

                sTitle = serie[pbContent.TITLE].strip()
                if sTitle != searchTitle:
                    continue
            
            numSaison = serie[pbContent.SAISON].strip()
            if numSaison not in saisons:
                saisons.append(numSaison)
                
        
    # Une seule saison, directement les épisodes
    if len(saisons) == 1:
        siteUrl += '&sSaison=' + saisons[0]
        showEpisodesLinks(siteUrl)
        return

    # Proposer les différentes saisons
    for sSaison in sorted(saisons):
        sUrl = siteUrl + '&sSaison=' + sSaison

        if sSaison.isdigit():
            sSaison = 'S{:02d}'.format(int(sSaison))
        
        sDisplayTitle = searchTitle + ' - ' + sSaison
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
    
    params = siteUrl.split('&',1)[1]
    aParams = dict(param.split('=') for param in params.split('&'))
    sSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchTitle = aParams['sTitle']
 
    if not sSaison:
        oGui.setEndOfDirectory()
        return
 
    lines = getHosterList(siteUrl)[0]

    listeEpisodes = []
    for episode in lines:
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
                if res.isdigit(): res += 'p'
                res = res.replace('P', 'p').replace('1080p', 'HD').replace('720p', 'HD').replace('2160p', '4K')
                sDisplayName = sTitle
                if res: sDisplayName += ' [%s]' %res
                resIdx += 1
            else:
                sDisplayName = sTitle

            oHoster.setDisplayName(sDisplayName)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()

# Retrouve tous les liens disponibles pour un film, ou un épisode, gère les groupes multipaste
def getHosterList(siteUrl):
    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    searchYear = aParams['sYear'] if 'sYear' in aParams else None
    searchSaison = aParams['sSaison'] if 'sSaison' in aParams else None
    searchEpisode = aParams['sEpisode'] if 'sEpisode' in aParams else None
    idTMDB = aParams['idTMDB'] if 'idTMDB' in aParams else None
    searchTitle = aParams['sTitle']
    
    pbContent = PasteBinContent()
    movies = []
    listeIDs = getPasteList(siteUrl, pasteID)
    for pasteBin in listeIDs:
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        moviesBin = pbContent.getLines(sContent)
        movies += moviesBin

    listHoster = []
    listRes = []

    for movie in movies:

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
            if pbContent.CAT >=0 and sMedia not in movie[pbContent.CAT]:
                continue
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
        if "[" in links:
            links = eval(links)
            listHoster.extend(links)
        elif isinstance(links, list):
            listHoster.extend(links)
        else:
            if searchEpisode:
                for numEpisode, link in links.items():
                    if str(numEpisode) == searchEpisode:
                        listHoster.append(link)
                        break
            else:
                listHoster.append(links)

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

    # Supprime les doublons en gardant l'ordre
#     links = [links.extend(elem) for elem in listHoster if not elem in links]

    return listHoster, listRes
    

# Ajout d'un lien pastebin
def addPasteName():
    oGui = cGui()
    addons = addon()

    # Recherche d'un setting de libre
    names = set()
    newID = 0
    for numID in range(1, PASTE_PAR_GROUPE):
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
            if newID == 0:
                newID = numID
        else:
            names.add(pasteLabel)   # Labels déjà utilisés
    
    settingLabel = SETTING_PASTE_LABEL + str(newID)
    
    
    # Demande du label et controle si déjà existant
    sLabel = oGui.showKeyBoard('', "Saisir un nom")
    if sLabel == False:
        return
    if sLabel in names:
        dialog().VSok(addons.VSlang(30082))
        return

    # Enregistrer Label/id dans les settings
    addons.setSetting(settingLabel, sLabel)
    dialog().VSinfo(addons.VSlang(30042))
    
    oGui.updateDirectory()


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
    pasteID = oGui.showKeyBoard('', "Saisir l'ID du PasteBin")
    if pasteID == False:
        return
    if pasteID in IDs:              # ID déjà dans le groupe
        dialog().VSok(addons.VSlang(30082))
        return
 
    # Vérifier l'entete du Paste
    pbContentNew = PasteBinContent()
    sUrl = URL_MAIN + pasteID
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setTimeout(4)
    sContent = oRequestHandler.request()
    movies = pbContentNew.getLines(sContent)
    if len(movies) ==0 :
        dialog().VSok(addons.VSlang(30022))
        return
    
    # Vérifier que les autres pastes du groupe ont le même format d'entete
    if len(IDs)>0:
        pbContentOld = PasteBinContent()
        sUrl = URL_MAIN + IDs.pop()
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        pbContentOld.getLines(sContent)

        if not pbContentNew.isFormat(pbContentOld):
            dialog().VSok(addons.VSlang(30022))
            return
    
    addons.setSetting(settingID, pasteID)
    dialog().VSinfo(addons.VSlang(30042))
    
    oGui.updateDirectory()


# Retirer un groupe PasteBin
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

# msgctxt "#30072"
# msgid "File deleted"
# msgstr "Fichier supprimé"
