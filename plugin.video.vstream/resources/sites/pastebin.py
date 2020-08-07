# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import progress, addon, dialog 
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote, cUtil, Unquote


SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'PasteBin'
SITE_DESC = 'Liste depuis pastebin'

URL_MAIN = 'https://pastebin.com/raw/'

KEY_PASTE_ID = 'PASTE_ID'
SETTING_PASTE_ID = 'pastebin_id_'
SETTING_PASTE_LABEL = 'pastebin_label_'

URL_SEARCH_MOVIES = (URL_MAIN + KEY_PASTE_ID + '?type=film&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + KEY_PASTE_ID + '?type=serie&s=', 'showMovies')


ITEM_PAR_PAGE = 20

class idxInFile:
    CAT = 0     # Catégorie 'film', 'serie', 'anime'
    TMDB = 1    # Id TMDB (optionnel)
    TITLE = 2   # Titre du film / épisodes
    SAGA = 3    # Saga (ex 'Mission impossible') (optionnel)
    SAISON = 3  # Saison (ex 'Saison 3') (optionnel)
    YEAR = 4    # Année (Optionnel)
    GENRES = 5  # Liste des genres (optionnel)
    URLS = 6    # Liste des liens, avec épisodes pour les séries

# Exemples
# film;714;Demain ne meurt jamais;James BOND;1997;['Action', 'Aventure', 'Thriller'];['https://uptobox.com/nwxxxx','https://uptobox.com/nwYYzz']
# serie;48866;Les 100;Saison 2; 2014; ['Fantastique', 'Aventure']; {'S02E01':['lien1', 'lien2'], 'S02E02':['lien1']}


def load():
    addons = addon()
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'addPasteID', 'Ajouter un lien PasteBin privé', 'listes.png', oOutputParameterHandler)

    numID = 0
    pasteListe = {}
    
#     # WIP - Ajout des listes publiques
#     publicIDs = set()
#     while True:
#         numID += 1
#         pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
#         if pasteLabel == '':
#             break
# 
#         pasteID = addons.getSetting(SETTING_PASTE_ID + str(numID))
#         if pasteID:
#             pasteListe[pasteLabel] = pasteID
#             publicIDs.add(pasteID)
    
    
    # Recherche des listes privées
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
    
    oGui.setEndOfDirectory()


def showMenu():
    oInputParameterHandler = cInputParameterHandler()
    pasteID = oInputParameterHandler.getValue('pasteID')
    
    # Etablir les menus en fonction du contenu
    sUrl = URL_MAIN + pasteID
    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    lines = sContent.splitlines()

    containFilms = False
    containFilmGenres = False
    containFilmSaga = False
    containFilmYear = False
    containSeries = False
    
    for line in lines:
        movie = line.split(';')

        if 'film' in movie[idxInFile.CAT]:
            containFilms = True
            if len(movie[idxInFile.GENRES].strip())>0:
                containFilmGenres = True
            if len(movie[idxInFile.YEAR].strip())>0:
                containFilmYear = True
            if len(movie[idxInFile.SAGA].strip())>0:
                containFilmSaga = True
        if 'serie' in movie[idxInFile.CAT]:
            containSeries = True

    
    oGui = cGui()

    if containFilms:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_MOVIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Films (Liste)', 'listes.png', oOutputParameterHandler)

    if containFilmGenres:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    if containFilmSaga:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSaga', 'Films (Saga)', 'genres.png', oOutputParameterHandler)

    if containFilmYear:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Années)', 'annees.png', oOutputParameterHandler)

    if containSeries:
        oOutputParameterHandler = cOutputParameterHandler()
        searchUrl = URL_SEARCH_SERIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', searchUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'serie')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'serie')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'serie')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaList', 'Séries (Liste)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl += Quote(sSearchText)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    lines = sContent.splitlines()

    genres = set()
    for line in lines:
        movie = line.split(';')

        if sMedia not in movie[idxInFile.CAT]:
            continue

        genre = movie[idxInFile.GENRES]
        genre = eval(genre)
        if genre:
            genres = genres.union(genre)

    for sGenre in sorted(genres):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sGenre', sGenre)
        oOutputParameterHandler.addParameter('sMedia', sMedia)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSaga():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    lines = sContent.splitlines()

    sagas = set()
    for line in lines:
        movie = line.split(';')

        if sMedia not in movie[idxInFile.CAT]:
            continue

        saga = movie[idxInFile.SAGA].strip()
        if saga <> '':
            sagas.add(saga)
            
    for sSaga in sorted(sagas):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sSaga', sSaga)
        oOutputParameterHandler.addParameter('sMedia', sMedia)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sSaga, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    lines = sContent.splitlines()

    years = set()
    for line in lines:
        movie = line.split(';')

        if sMedia not in movie[idxInFile.CAT]:
            continue

        year = movie[idxInFile.YEAR].strip()
        years.add(year)

    for sYear in sorted(years, reverse=True):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sMedia', sMedia)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'years.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def AlphaList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')

    for i in range(0, 36):
        if (i < 10):
            sLetter = chr(48 + i)
        else:
            sLetter = chr(65 + i -10)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMedia', sMedia)
        oOutputParameterHandler.addParameter('sAlpha', sLetter)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] Lettre [COLOR red]' + sLetter + '[/COLOR][/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')
    sGenre = oInputParameterHandler.getValue('sGenre')
    sSaga = oInputParameterHandler.getValue('sSaga')
    sYear = oInputParameterHandler.getValue('sYear')
    sAlpha = oInputParameterHandler.getValue('sAlpha')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    sSearchTitle = ''
    if sSearch:
        oParser = cParser()
        sUrl = sSearch
        sTypeSearch = oParser.parse(sUrl, '\?type=(.+?)&s=(.+)')
        if sTypeSearch[0]:
            sMedia = sTypeSearch[1][0][0]
            sSearchTitle = sTypeSearch[1][0][1]
            sSearchTitle = Unquote(sSearchTitle)
        else:
            sMedia = 'film'

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()

    lines = sContent.splitlines()

    serieTitles = set()
    nbItem = 0
    index = 0
    progress_ = progress().VScreate(SITE_NAME)

    # création d'un tableau
    movies = [k.split(";") for k in lines]
    
    # Recherche par ordre alphabetique => le tableau doit être trié
    if sAlpha:
        movies = sorted(movies, key=lambda line: line[idxInFile.TITLE])
        
        
    for movie in movies:

        # Pagination, on se repositionne
        index += 1
        if index <= numItem:
            continue
        numItem += 1

        # Filtrage par média (film/série)
        if sMedia not in movie[idxInFile.CAT]:
            continue

        # Filtrage par saga
        if sSaga and sSaga != movie[idxInFile.SAGA].strip():
            continue

        # Filtrage par genre
        genres = movie[idxInFile.GENRES]
        if sGenre and genres:
            genres = eval(genres)
            if sGenre not in genres:
                continue

        # l'ID TMDB
        sTmdbId = movie[idxInFile.TMDB].strip()

        # Filtrage par titre
        sTitle = movie[idxInFile.TITLE].strip()
        
        # Titre recherché
        if sSearchTitle:
            if cUtil().CheckOccurence(sSearchTitle, sTitle) == 0:
                continue

        # recherche alphabétique
        if sAlpha:
            if sTitle[0] != sAlpha:
                continue

        # Une série ne doit apparaitre qu'une seule fois, les saisons sont gérées plus tard
        if sMedia == 'serie':
            if sTitle in serieTitles:
                continue
            serieTitles.add(sTitle)

        # Filtrage par années
        year = movie[idxInFile.YEAR].strip()
        if sYear:
            if not year or sYear != year:
                continue
            
            
        sDisplayTitle = sTitle
        if year:
            sDisplayTitle = '%s (%s)' % (sTitle, year)

        nbItem += 1
        progress_.VSupdate(progress_, ITEM_PAR_PAGE)
        if progress_.iscanceled():
            break

        sHost = movie[idxInFile.URLS]

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTitle', sTitle)
        oOutputParameterHandler.addParameter('sHost', sHost)
        if sTmdbId:
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

        if sMedia == 'serie':
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        elif sMedia == 'anime':
            oGui.addAnime(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
        else:
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if not sSearch:
            if nbItem % ITEM_PAR_PAGE == 0:
                numPage += 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMedia', sMedia)
                oOutputParameterHandler.addParameter('sGenre', sGenre)
                oOutputParameterHandler.addParameter('sSaga', sSaga)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sAlpha', sAlpha)
                oOutputParameterHandler.addParameter('numPage', numPage)
                oOutputParameterHandler.addParameter('numItem', numItem)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(numPage) + ' >>>[/COLOR]', oOutputParameterHandler)
                break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showSerieSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sContent = oRequestHandler.request()
    lines = sContent.splitlines()

    saisons = {}

    # Recherche les saisons de la série    
    for line in lines:
        movie = line.split(';')
        title = movie[idxInFile.TITLE].strip()
        if title != sTitle:
            continue
        saisons[movie[idxInFile.SAISON].strip()] = movie[idxInFile.URLS]

    # Une seule saison, directement les épisodes
    if len(saisons) == 1:
        showSerieLinks()
        return

    # Proposer les différentes saisons
    numSaisons = saisons.keys()
    for sSaison in sorted(numSaisons):
        links = saisons[sSaison]
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', sTitle)
        oOutputParameterHandler.addParameter('sHost', links)
        oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sSaison, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHoster = oInputParameterHandler.getValue('sHost')
    sTitle = oInputParameterHandler.getValue('sTitle')
    
    sHoster = eval(sHoster)

    # Trie des épisodes 
    episodes = sHoster.keys()

    for episode in sorted(episodes):
        links = sHoster[episode]
        
        sDisplayTitle = sTitle + ' ' + episode

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sHost', links)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHoster = oInputParameterHandler.getValue('sHost')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sHoster = eval(sHoster)

    for sHosterUrl in sHoster:
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
            names.add(pasteLabel)   # Labels déjà utilisés
    
    settingID = SETTING_PASTE_ID + str(newID)
    settingLabel = SETTING_PASTE_LABEL + str(newID)
    
    
    # Demande du label et controle si déjà existant
    sLabel = oGui.showKeyBoard('', "Saisir un titre")
    if sLabel == False:
        return
    if sLabel in names:
        dialog().VSok(addons.VSlang(30082))
        return


    # Demande de l'id PasteBin
    sID = oGui.showKeyBoard('', "Saisir l'ID")
    if sID == False:
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
    

