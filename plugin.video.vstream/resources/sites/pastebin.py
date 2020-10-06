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


ITEM_PAR_PAGE = 20
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

    # Pour comparer deux pastes, savoir si mêmes champs
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
            and self.URLS == other.URLS \
            and self.HEBERGEUR == other.HEBERGEUR \
    
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
                
            if champ in dir(self):
                setattr(self, champ, idx)
            idx +=1

        lines = [k.split(";") for k in lines[1:]]
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
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film&pasteID=' + pasteID)
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

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    listeIDs = getPasteList(siteUrl, pasteID)
    
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
        siteUrl = URL_MAIN + '&sMedia=' + sMedia +'&sGenre=' + str(genre)
        if pasteID:
            siteUrl += '&pasteID=' + pasteID
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showNetwork():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

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
                        networkId = network.split(':')[0]
                        networkName = network.split(':')[1]
                        if networkName in listNetwork:
                            continue
                        listNetwork[networkName] = networkId

    maxProgress = len(listNetwork)
    progress_ = progress().VScreate(SITE_NAME)

    for networkName, networkId in sorted(listNetwork.items()):
        progress_.VSupdate(progress_, maxProgress)
        if progress_.iscanceled():
            break

        sUrl = siteUrl + '&sMedia=' + sMedia +'&sNetwork=' + networkId + ":" + networkName.replace('+', '|')
        if pasteID: sUrl += '&pasteID=' + pasteID
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

    siteUrl, params = siteUrl.split('&',1)
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
    listeIDs = getPasteList(siteUrl, pasteID)
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
                        realId = real.split(':')[0]
                        realName = real.split(':')[1]
                        if realName in listReal:
                            continue
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

        sUrl = siteUrl + '&sMedia=' + sMedia +'&sDirector=' + realId + ":" + realName
        if pasteID: sUrl += '&pasteID=' + pasteID
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', realId)    # Utilisé par TMDB
        oGui.addPerson(SITE_IDENTIFIER, 'showMovies', realName, 'actor.png', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0:
            numPage += 1
            
            sUrl = siteUrl + '&sMedia=' + sMedia
            if pasteID: sUrl += '&pasteID=' + pasteID
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
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

    siteUrl, params = siteUrl.split('&',1)
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
    listeIDs = getPasteList(siteUrl, pasteID)
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
                        acteurId = acteur.split(':')[0]
                        acteurName = acteur.split(':')[1]
                        if acteurName in listActeur:
                            continue
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

        sUrl = siteUrl + '&sMedia=' + sMedia +'&sCast=' + acteurId + ":" + acteurName
        if pasteID: sUrl += '&pasteID=' + pasteID
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', acteurId)    # Utilisé par TMDB
        oGui.addPerson(SITE_IDENTIFIER, 'showMovies', acteurName, 'actor.png', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0:
            numPage += 1
            
            sUrl = siteUrl + '&sMedia=' + sMedia
            if pasteID: sUrl += '&pasteID=' + pasteID
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
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

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

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
                        if grID in sousGroupe:
                            continue
                        sousGroupe.add(grID)
                    else:
                        groupesPerso.add(gr)

    groupes = groupesPerso.union(sousGroupe)
    for sGroupe in sorted(groupes):
        sUrl = siteUrl + '&sMedia=' + sMedia +'&sGroupe=' + sGroupe
        if pasteID: sUrl += '&pasteID=' + pasteID
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

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None
    if 'sGroupe' in aParams:
        sGroupe = aParams['sGroupe'] + ':'

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

    groupes = set()
    for movie in movies:
        groupe = movie[pbContent.GROUPES].strip().replace("''",'')
        if groupe:
            groupe = eval(groupe)
            if groupe:
                for gr in groupe:
                    if gr.startswith(sGroupe):
                        groupes.add(gr)

    for sGroupe in sorted(groupes):
        sUrl = siteUrl + '&sMedia=' + sMedia +'&sGroupe=' + sGroupe.replace('+', '|')
        if pasteID: sUrl += '&pasteID=' + pasteID
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

    siteUrl, params = siteUrl.split('&',1)
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
    listeIDs = getPasteList(siteUrl, pasteID)
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

        sUrl = siteUrl + '&sMedia=' + sMedia
        if pasteID: sUrl += '&pasteID=' + pasteID

        oOutputParameterHandler = cOutputParameterHandler()
        if sTmdbId.isdigit():
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)    # Utilisé par TMDB
            sUrl += '&sSaga=' + sTmdbId + ':' + sSagaName
        else:
            sUrl += '&sSaga=' + sSagaName
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
            
            sUrl = siteUrl + '&sMedia=' + sMedia
            if pasteID: sUrl += '&pasteID=' + pasteID
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
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

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

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

    years = set()
    for line in movies:
        if pbContent.CAT >=0 and sMedia not in line[pbContent.CAT]:
            continue

        year = line[pbContent.YEAR].strip()
        years.add(year)

    for sYear in sorted(years, reverse=True):
        sUrl = siteUrl + '&sMedia=' + sMedia +'&sYear=' + sYear
        if pasteID: sUrl += '&pasteID=' + pasteID
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'years.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showResolution():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

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

    for sRes in sorted(resolutions):
        if sRes == '': continue

        sDisplayRes = sRes
        if sDisplayRes.isdigit(): sDisplayRes += 'p'
        sDisplayRes = sDisplayRes.replace('P', 'p').replace('1080p', 'HD [1080p]').replace('720p', 'SD [720p]').replace('4K', '2160p').replace('2160p', '4K [2160p]')

        sUrl = siteUrl + '&sMedia=' + sMedia +'&sRes=' + sRes 
        if pasteID: sUrl += '&pasteID=' + pasteID
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayRes, 'hd.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def AlphaList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    sMedia = aParams['sMedia'] if 'sMedia' in aParams else 'film'
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    for i in range(0, 36):
        if (i < 10):
            sLetter = chr(48 + i)
        else:
            sLetter = chr(65 + i -10)

        siteUrl = sUrl + '&sMedia=' + sMedia +'&sAlpha=' + sLetter
        if pasteID: sUrl += '&pasteID=' + pasteID

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
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
    siteUrl = siteUrl.replace('+', ' ').replace('|', '+').replace(' & ', ' | ')
    
    siteUrl, params = siteUrl.split('&',1)
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
    listeIDs = getPasteList(siteUrl, pasteID)
    for pasteBin in listeIDs:
        sUrl = URL_MAIN + pasteBin
        oRequestHandler = cRequestHandler(sUrl)
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
    
    serieTitles = set()
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
        if sDirector and pbContent.DIRECTOR >=0 :
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
        if sNetwork and pbContent.NETWORK >=0 :
            listNetwork = movie[pbContent.NETWORK].strip()
            if not listNetwork:
                continue
            listNetwork = eval(listNetwork)
            if sNetwork not in listNetwork:
                continue

        # Filtrage par groupe
        if sGroupe and pbContent.GROUPES >=0:
            groupes = movie[pbContent.GROUPES].strip()
            if not groupes:
                continue
            groupes = eval(groupes)
            if sGroupe not in groupes:
                continue

        # l'ID TMDB
        sTmdbId = None
        if pbContent.TMDB >=0:
            sTmdbId = movie[pbContent.TMDB].strip()
        

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

        # Une série ne doit apparaitre qu'une seule fois, les saisons sont gérées plus tard
        if sMedia in ('serie', 'anime'):
            if sTitle in serieTitles:
                continue
            serieTitles.add(sTitle)

        sDisplayTitle = sTitle

        # Filtrage par années
        if pbContent.YEAR>=0:
            year = movie[pbContent.YEAR].strip()
            if sYear:
                if not year or sYear != year:
                    continue
                sDisplayTitle = '%s (%s)' % (sTitle, year)

        # Filtrage par résolutions vidéos
        listRes = None
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

        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = siteUrl
        if sMedia : sUrl += '&sMedia=' + sMedia
        if pasteID: sUrl += '&pasteID=' + pasteID
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        
        sTitle = sTitle.replace('[', '').replace(']', '')   # Exemple pour le film [REC], les crochets sont génant pour certaines fonctions
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        if sTmdbId:
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

        if sMedia == 'serie':
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        elif sMedia == 'anime':
            oGui.addAnime(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'animes.png', '', '', oOutputParameterHandler)
        else:
            sHost = movie[pbContent.URLS]
            if len(sHost.replace('[', '').replace(']', '').replace('"', '').replace('\'', '').strip()) > 0:
                
                # Reconstruire les liens
                if pbContent.HEBERGEUR:
                    if "[" in sHost:
                        sHost = eval(sHost)
                        sUrl = [(pbContent.HEBERGEUR + link) for link in sHost]
                    else:
                        sUrl = pbContent.HEBERGEUR + sHost
                else:
                    sUrl = sHost

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                if listRes:
                    oOutputParameterHandler.addParameter('listRes', listRes)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if not sSearch:
            if nbItem % ITEM_PAR_PAGE == 0:
                numPage += 1
                
                sUrl = siteUrl
                if sMedia : sUrl += '&sMedia=' + sMedia
                if pasteID : sUrl += '&pasteID=' + pasteID
                if sGenre : sUrl += '&sGenre=' + sGenre
                if sSaga : sUrl += '&sSaga=' + sSaga
                if sGroupe : sUrl += '&sGroupe=' + sGroupe
                if sYear : sUrl += '&sYear=' + sYear
                if sRes : sUrl += '&sRes=' + sRes
                if sDirector : sUrl += '&sDirector=' + sDirector
                if sCast : sUrl += '&sCast=' + sCast
                if sNetwork : sUrl += '&sNetwork=' + sNetwork
                if sAlpha : sUrl += '&sAlpha=' + sAlpha
                if bRandom : sUrl += '&bRandom=True'
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
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
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

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

    saisons = []

    # Recherche les saisons de la série
    for line in movies:
        title = line[pbContent.TITLE].strip()
        if title != sTitle:
            continue
        saisons.append(line[pbContent.SAISON].strip())

    # Une seule saison, directement les épisodes
    if len(saisons) == 1:
        saison = saisons[0]
        showSerieLinks(saison)
        return

    # Proposer les différentes saisons
    for sSaison in sorted(saisons):
        sUrl = siteUrl + '&sSaison=' + sSaison
        if pasteID: sUrl += '&pasteID=' + pasteID

        if sSaison.isdigit():
            sSaison = 'S{:02d}'.format(int(sSaison))
        
        sDisplayTitle = sTitle + ' - ' + sSaison

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas le sTitre afin de pouvoir mettre la saison en marque-page
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieLinks(sSaison=None):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    siteUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    pasteID = aParams['pasteID'] if 'pasteID' in aParams else None

    if not sSaison:
        if 'sSaison' in aParams:
            sSaison = aParams['sSaison']
    
        sTitle = sTitle[:sTitle.rindex(' - ')]
    
    if not sSaison:
        oGui.setEndOfDirectory()
        return

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

    # Recherche la saison
    links = None
    for line in movies:
        if line[pbContent.TITLE].strip() != sTitle:
            continue
        if line[pbContent.SAISON].strip() == sSaison:
            links = line[pbContent.URLS]
            break

    if str(sSaison).isdigit():
        sSaison = 'S{:02d}'.format(int(sSaison))
 
    if not links:
        oGui.setEndOfDirectory()
        return

    sHoster = eval(links)
        
    # Trie des épisodes 
    episodes = sHoster.keys()

    for episode in sorted(episodes):
        links = sHoster[episode]
        
        if str(episode).isdigit():
            episode = '{}E{:02d}'.format(sSaison, int(episode))
        elif episode[0] == 'E': 
            episode = '{}{}'.format(sSaison, episode)
        sDisplayTitle = sTitle + ' - ' + episode

        # Reconstruire les liens
        if pbContent.HEBERGEUR:
            if isinstance(links, list):
                sUrl = [(pbContent.HEBERGEUR + link) for link in links]  
            else:
                sUrl = pbContent.HEBERGEUR + links
        else:
            sUrl = links
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)

        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sHoster = oInputParameterHandler.getValue('siteUrl')
    listRes = oInputParameterHandler.getValue('listRes')

    if "[" in sHoster:
        listHoster = eval(sHoster)
    else:
        listHoster = []   
        listHoster.append(sHoster)

    # La liste des résolutions doit avoir la même taille que la liste des host,
    # sinon on affiche pas la résolution de chaque flux
    if listRes:
        listRes = eval(listRes)
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
                res = res.replace('P', 'p').replace('1080p', 'HD').replace('720p', 'SD').replace('2160p', '4K')
                sDisplayName = sTitle
                if res: sDisplayName += ' [%s]' %res
                resIdx += 1
            else:
                sDisplayName = sTitle

            oHoster.setDisplayName(sDisplayName)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


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
        IDs.add(pasteBin)        # IDs déjà renseigné
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
    sID = oGui.showKeyBoard('', "Saisir l'ID du PasteBin")
    if sID == False:
        return
    if sID in IDs:
        dialog().VSok(addons.VSlang(30082))
        return
 
    # Vérifier que les pastes ont le même format d'entete
    pbContentOld = None
    if len(IDs)>0:
        pbContentOld = PasteBinContent()
        sUrl = URL_MAIN + IDs.pop()
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        pbContentOld.getLines(sContent)

    if pbContentOld:
        pbContentNew = PasteBinContent()
        sUrl = URL_MAIN + sID
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(4)
        sContent = oRequestHandler.request()
        pbContentNew.getLines(sContent)
        if not pbContentNew.isFormat(pbContentOld):
            dialog().VSok(addons.VSlang(30022))
            return
    
    addons.setSetting(settingID, sID)
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

