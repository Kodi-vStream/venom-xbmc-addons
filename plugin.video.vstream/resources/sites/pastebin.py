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


SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'PasteBin'
SITE_DESC = 'Liste depuis pastebin'

URL_MAIN = 'https://pastebin.com/raw/'

KEY_PASTE_ID = 'PASTE_ID'
SETTING_PASTE_ID = 'pastebin_id_'
SETTING_PASTE_LABEL = 'pastebin_label_'
UNCLASSIFIED_GENRE = '_NON CLASSÉ_'

URL_SEARCH_MOVIES = (URL_MAIN + KEY_PASTE_ID + '&sMedia=film&sSearch=', 'showSearchGlobal')
URL_SEARCH_SERIES = (URL_MAIN + KEY_PASTE_ID + '&sMedia=serie&sSearch=', 'showSearchGlobal')
URL_SEARCH_ANIMS = (URL_MAIN + KEY_PASTE_ID + '&sMedia=anime&sSearch=', 'showSearchGlobal')
FUNCTION_SEARCH = 'showSearchGlobal'


ITEM_PAR_PAGE = 20

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
    GROUPES = -1  # (optionnel) - Groupes tel que NETFLIX, HBO, MARVEL, DISNEY, Films enfants, ...
    YEAR = -1    # (optionnel) - Année
    GENRES = -1  # (optionnel) - Liste des genres
    URLS = -1    # Liste des liens, avec épisodes pour les séries
    HEBERGEUR = '' # (optionnel) - URL de l'hebergeur, pour éviter de le mettre dans chaque URL, ex : 'https://uptobox.com/'  
    listeGroupe = {} # (optionnel) - Liste de groupes nommés
    
    def getLines(self, sContent):
        lines = sContent.splitlines()

        # Vérifie si la ligne d'entete existe avec les champs obligatoires
        entete = lines[0].replace(' ','').split(";")
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
                
            if 'GROUPE' in champ:  # supporte GROUPE ou GROUPES
                groupes = champ.split('=')
                champ = 'GROUPES'
                if '{' in groupes[1]:  # GROUPES = {"R": ["Réalisateur"], "D": ["Diffuseur"]}
                    self.listeGroupe = eval(groupes[1])
                
            if champ in dir(self):
                setattr(self, champ, idx)
            idx +=1

        lines = [k.split(";") for k in lines[1:]]

        return lines
    
    
    def getGroupeName(self, groupeID):
        groupe = self.listeGroupe.get(groupeID)
        if groupe:
            return groupe
        return groupeID

def load():
    addons = addon()
    oGui = cGui()

    numID = 0
    pasteListe = {}
    
    # Recherche des listes déclarées
    while True:
        numID += 1
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
            break

        pasteID = addons.getSetting(SETTING_PASTE_ID + str(numID))
        if pasteID:
            pasteListe[pasteLabel] = pasteID
    
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
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'deletePaste', addons.VSlang(30412))
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
    

    # Menu pour ajouter un lien
    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'addPasteID', '[COLOR coral]Ajouter un lien PasteBin[/COLOR]', 'listes.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()


def showMenu():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')
    
    # Etablir les menus en fonction du contenu
    sUrl = URL_MAIN + pasteID
    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

    # Calculer les menus
    containFilms = False
    containFilmGenres = False
    containFilmGroupes = False
    containFilmSaga = False
    containFilmYear = False
    containSeries = False
    containSerieGroupes = False
    containAnimes = False
    containAnimeGroupes = False

    for movie in movies:
        if 'film' in movie[pbContent.CAT]:
            containFilms = True
            if pbContent.GENRES>=0 and len(movie[pbContent.GENRES].strip())>0:
                containFilmGenres = True
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].strip())>0:
                containFilmGroupes = True
            if pbContent.YEAR>=0 and len(movie[pbContent.YEAR].strip())>0:
                containFilmYear = True
            if pbContent.SAISON>=0 and len(movie[pbContent.SAISON].strip())>0:
                containFilmSaga = True
        if 'serie' in movie[pbContent.CAT]:
            containSeries = True
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].strip())>0:
                containSerieGroupes = True

        if 'anime' in movie[pbContent.CAT]:
            containAnimes = True
            if pbContent.GROUPES>=0 and len(movie[pbContent.GROUPES].strip())>0:
                containAnimeGroupes = True

    if containFilms or not containSeries:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_MOVIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        if containFilmGenres:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
            oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    
        if containFilmGroupes:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Films (Dossiers)', 'genres.png', oOutputParameterHandler)
    
        if containFilmSaga:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
            oGui.addDir(SITE_IDENTIFIER, 'showSaga', 'Films (Saga)', 'genres.png', oOutputParameterHandler)
    
        if containFilmYear:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
            oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Années)', 'annees.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=film')
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Films (Liste)', 'listes.png', oOutputParameterHandler)


    if containSeries:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_SERIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie')
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

        if containSerieGroupes:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie')
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Séries (Dossiers)', 'genres.png', oOutputParameterHandler)
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=serie')
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Séries (Liste)', 'listes.png', oOutputParameterHandler)


    if containAnimes:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_ANIMS[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime')
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Animes (Genres)', 'genres.png', oOutputParameterHandler)

        if containAnimeGroupes:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime')
            oGui.addDir(SITE_IDENTIFIER, 'showGroupes', 'Animes (Dossiers)', 'genres.png', oOutputParameterHandler)
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '&sMedia=anime')
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Animes (Liste)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl += Quote(sSearchText)
        
        # Recherche globale si le pastebin n'est pas mentionné
        if KEY_PASTE_ID in sUrl:
            showSearchGlobal(sUrl)
        else:
            showMovies(sUrl)
        oGui.setEndOfDirectory()


def showSearchGlobal(sSearch=''):
    addons = addon()

    sUrl = sSearch

    # Parcourir la liste des PasteBin
    numID = 0
    while True:
        numID += 1
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
            break # Fin de la liste

        pasteID = addons.getSetting(SETTING_PASTE_ID + str(numID))
        if pasteID:
            searchUrl = sUrl.replace(KEY_PASTE_ID, pasteID)
            try:
                showMovies(searchUrl)
            except:
                pass


def showGenres():
    tmdb = cTMDb()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    else:
        sMedia = 'film'

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

    genres = {}
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
                genres[sDisplayGenre] = g

    genreKeys = genres.keys()
    for sDisplayGenre in sorted(genreKeys):
        genre = genres.get(sDisplayGenre)
        oOutputParameterHandler = cOutputParameterHandler()
        siteUrl = sUrl + '&sMedia=' + sMedia +'&sGenre=' + str(genre) 
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGroupes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    else:
        sMedia = 'film'

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

    groupesSys = set()
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
                        if grID in groupesSys:
                            continue
                        groupesSys.add(grID)
                        grLabel = pbContent.getGroupeName(grID)
                        siteUrl = sUrl + '&sMedia=' + sMedia +'&sGroupe=' + grID #+ ':' + sGroupe 
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                        oGui.addDir(SITE_IDENTIFIER, 'showGroupeDetails', grLabel, 'genres.png', oOutputParameterHandler)
                    else:
                        groupesPerso.add(gr)

    for sGroupe in sorted(groupesPerso):
        siteUrl = sUrl + '&sMedia=' + sMedia +'&sGroupe=' + sGroupe 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sGroupe, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGroupeDetails():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = siteUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    if 'sGroupe' in aParams:
        sGroupe = aParams['sGroupe'] + ':'
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    else:
        sMedia = 'film'

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

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
        siteUrl = sUrl + '&sMedia=' + sMedia +'&sGroupe=' + sGroupe 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        sDisplayGroupe = sGroupe.split(':')[1]
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayGroupe, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSaga():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')

    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    else:
        sMedia = 'film'

    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

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

        siteUrl = sUrl + '&sMedia=' + sMedia + '&sSaga=' + sSagaName 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sSagaName)
        if sTmdbId.isdigit():
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        else:
            oOutputParameterHandler.addParameter('sMovieTitle', sSagaName)
        oGui.addMoviePack(SITE_IDENTIFIER, 'showMovies', sSagaName, 'genres.png', '', '', oOutputParameterHandler)

        nbItem += 1
        if nbItem % ITEM_PAR_PAGE == 0:
            numPage += 1
            
            siteUrl = sUrl
            if sMedia : siteUrl += '&sMedia=' + sMedia
            
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
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    else:
        sMedia = 'film'

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

    years = set()
    for line in movies:
        if pbContent.CAT >=0 and sMedia not in line[pbContent.CAT]:
            continue

        year = line[pbContent.YEAR].strip()
        years.add(year)

    for sYear in sorted(years, reverse=True):
        siteUrl = sUrl + '&sMedia=' + sMedia +'&sYear=' + sYear 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'years.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def AlphaList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))
    if 'sMedia' in aParams:
        sMedia = aParams['sMedia']
    else:
        sMedia = 'film'

    for i in range(0, 36):
        if (i < 10):
            sLetter = chr(48 + i)
        else:
            sLetter = chr(65 + i -10)

        siteUrl = sUrl + '&sMedia=' + sMedia +'&sAlpha=' + sLetter

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] Lettre [COLOR red]' + sLetter + '[/COLOR][/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    sMedia = 'film' # Par défaut
    sGenre = sSaga = sGroupe = sYear = sAlpha = None

    if sSearch:
        sUrl = sSearch

    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    sSearchTitle = ''
    
    # Pour supporter le caractere '&' dans les noms alors qu'il est réservé
    sUrl = sUrl.replace(' & ', ' | ')
    
    sUrl, params = sUrl.split('&',1)
    aParams = dict(param.split('=') for param in params.split('&'))

    if 'sMedia' in aParams: sMedia = aParams['sMedia']
    if 'sSearch' in aParams: sSearchTitle = Unquote(aParams['sSearch']).replace(' | ', ' & ')
    if 'sGenre' in aParams: sGenre = aParams['sGenre'].replace(' | ', ' & ')
    if 'sSaga' in aParams:
        if sTmdbId:
            sSaga = sTmdbId + ':'
        sSaga += aParams['sSaga'].replace(' | ', ' & ')
    if 'sGroupe' in aParams: sGroupe = aParams['sGroupe'].replace(' | ', ' & ')
    if 'sYear' in aParams: sYear = aParams['sYear']
    if 'sAlpha' in aParams: sAlpha = aParams['sAlpha']

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setTimeout(4)
    sContent = oRequestHandler.request()
    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

    serieTitles = set()
    nbItem = 0
    index = 0
    progress_ = progress().VScreate(SITE_NAME)

    # Recherche par ordre alphabetique => le tableau doit être trié
    if sAlpha:
        movies = sorted(movies, key=lambda line: line[pbContent.TITLE])
        
    # Recherche par saga => trie par années
    if sSaga and pbContent.YEAR>=0:
        movies = sorted(movies, key=lambda line: line[pbContent.YEAR])
        
        
    for movie in movies:

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

        # Filtrage par groupe
        if sGroupe and pbContent.GROUPES >=0:
            groupes = movie[pbContent.GROUPES].strip()
            if groupes:
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
        if sMedia == 'serie':
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

        nbItem += 1
        progress_.VSupdate(progress_, ITEM_PAR_PAGE)
        if progress_.iscanceled():
            break


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        
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
                        siteUrl = [(pbContent.HEBERGEUR + link) for link in sHost]  
                    else:
                        siteUrl = pbContent.HEBERGEUR + sHost
                else:
                    siteUrl = sHost

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if not sSearch:
            if nbItem % ITEM_PAR_PAGE == 0:
                numPage += 1
                
                siteUrl = sUrl
                if sMedia : siteUrl += '&sMedia=' + sMedia
                if sGenre : siteUrl += '&sGenre=' + sGenre
                if sSaga : siteUrl += '&sSaga=' + sSaga
                if sGroupe : siteUrl += '&sGroupe=' + sGroupe
                if sYear : siteUrl += '&sYear=' + sYear
                if sAlpha : siteUrl += '&sAlpha=' + sAlpha
                
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
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

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
        siteUrl = sUrl + '&sSaison=' + sSaison

        if sSaison.isdigit():
            sSaison = 'S{:02d}'.format(int(sSaison))
        
        sDisplayTitle = sTitle + ' ' + sSaison

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle) # on ne passe pas le sTitre afin de pouvoir mettre la saison en marque-page
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieLinks(sSaison=None):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    if not sSaison:
        sTitle = sTitle[:-4]
        sUrl, params = sUrl.split('&',1)
        aParams = dict(param.split('=') for param in params.split('&'))
        if 'sSaison' in aParams:
            sSaison = aParams['sSaison']
            
    if not sSaison:
        oGui.setEndOfDirectory()
        return

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    pbContent = PasteBinContent()
    movies = pbContent.getLines(sContent)

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
        sDisplayTitle = sTitle + ' ' + episode

        # Reconstruire les liens
        if pbContent.HEBERGEUR:
            if isinstance(links, list):
                siteUrl = [(pbContent.HEBERGEUR + link) for link in links]  
            else:
                siteUrl = pbContent.HEBERGEUR + links
        else:
            siteUrl = links
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)

        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sHoster = oInputParameterHandler.getValue('siteUrl')

    if "[" in sHoster:
        listHoster = eval(sHoster)
    else:
        listHoster = []   
        listHoster.append(sHoster)

    for sHosterUrl in listHoster:
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


# Ajout d'un lien pastebin
def addPasteID():
    oGui = cGui()
    addons = addon()

    # Recherche d'un setting de libre
    names = set()
    IDs = set()
    numID = 0
    newID = 0
    while True:
        numID += 1
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
            if newID == 0:
                newID = numID
            break

        pasteID = addons.getSetting(SETTING_PASTE_ID + str(numID))
        if pasteID == '':
            newID = numID
        else:
            IDs.add(pasteID)        # IDs déjà renseignés
            names.add(pasteLabel)   # Labels déjà utilisés
    
    settingID = SETTING_PASTE_ID + str(newID)
    settingLabel = SETTING_PASTE_LABEL + str(newID)
    
    
    # Demande de l'id PasteBin
    sID = oGui.showKeyBoard('', "Saisir l'ID du PasteBin")
    if sID == False:
        return
    if sID in IDs:
        dialog().VSok(addons.VSlang(30082))
        return

    # Demande du label et controle si déjà existant
    sLabel = oGui.showKeyBoard('', "Saisir un nom")
    if sLabel == False:
        return
    if sLabel in names:
        dialog().VSok(addons.VSlang(30082))
        return

    # Enregistrer Label/id dans les settings    
    addons.setSetting(settingLabel, sLabel)
    addons.setSetting(settingID, sID)


# Retirer un lien PasteBin
def deletePaste():

    addons = addon()
    if not dialog().VSyesno(addons.VSlang(30456)):
        return
    
    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')

# Ne pas effacer le label, car un label renseigné sans id veut dire que le setting peut être recyclé
#     labelSetting = SETTING_PASTE_LABEL + pasteID
#     addons.setSetting(labelSetting, '')

    # Recherche d'un setting de libre
    numID = 0
    while True:
        numID += 1
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
            break   # plus de setting disponible

        idSetting = SETTING_PASTE_ID + str(numID)
        settingID = addons.getSetting(idSetting)
        if settingID == pasteID:
            addons.setSetting(idSetting, '')
            break
    

