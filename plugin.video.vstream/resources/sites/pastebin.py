# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import progress, addon, dialog 
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote, cUtil, Unquote


SITE_IDENTIFIER = 'pastebin'
SITE_NAME = 'pastebin'
SITE_DESC = 'Liste depuis pastebin'

URL_MAIN = 'https://pastebin.com/raw/'

KEY_PASTE_ID = 'PASTE_ID'
SETTING_PASTE_ID = 'pastebin_id_'
SETTING_PASTE_LABEL = 'pastebin_label_'

URL_SEARCH_MOVIES = (URL_MAIN + KEY_PASTE_ID + '?type=film&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + KEY_PASTE_ID + '?type=serie&s=', 'showMovies')


ITEM_PAR_PAGE = 20


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
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('pasteID', pasteID)
        oGui.addDir(SITE_IDENTIFIER, 'deletePaste', '[COLOR red]' + pasteLabel + '[/COLOR]', 'mark.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = URL_SEARCH_MOVIES[0].replace(KEY_PASTE_ID, pasteID)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = URL_MAIN + pasteID
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMedia', 'film')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Années)', 'annees.png', oOutputParameterHandler)

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

        if sMedia not in movie[0]:
            continue

        genre = movie[4]
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

        if sMedia not in movie[0]:
            continue

        year = movie[3].strip()
        years.add(year)

    for sYear in sorted(years, reverse=True):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sMedia', sMedia)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'years.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMedia = oInputParameterHandler.getValue('sMedia')
    sGenre = oInputParameterHandler.getValue('sGenre')
    sYear = oInputParameterHandler.getValue('sYear')
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

    nbItem = 0
    index = 0
    progress_ = progress().VScreate(SITE_NAME)
    for line in lines:

        # Pagination, on se repositionne
        index += 1
        if index <= numItem:
            continue
        numItem += 1

        # Infos d'une ligne
        movie = line.split(';')

        # Filtrage par média (film/série)
        if sMedia not in movie[0]:
            continue

        # Filtrage par genre
        genres = movie[4]
        if sGenre and genres:
            genres = eval(genres)
            if sGenre not in genres:
                continue

        # l'ID TMDB
        sTmdbId = movie[1].strip()

        # Filtrage par titre
        sTitle = movie[2].strip()
        if sSearchTitle:
            if cUtil().CheckOccurence(sSearchTitle, sTitle) == 0:
                continue

        # Filtrage par années
        year = movie[3].strip()
        if sYear:
            if not year or sYear != year:
                continue
        if year:
            sTitle = '%s (%s)' % (sTitle, year)

        nbItem += 1
        progress_.VSupdate(progress_, ITEM_PAR_PAGE)
        if progress_.iscanceled():
            break

        sHost = movie[5]

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sHost', sHost)
        if sTmdbId:
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', '', '', oOutputParameterHandler)

        # Gestion de la pagination
        if not sSearch:
            if nbItem % ITEM_PAR_PAGE == 0:
                numPage += 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMedia', sMedia)
                oOutputParameterHandler.addParameter('sGenre', sGenre)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('numPage', numPage)
                oOutputParameterHandler.addParameter('numItem', numItem)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(numPage) + ' >>>[/COLOR]', oOutputParameterHandler)
                break

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHoster = oInputParameterHandler.getValue('sHost')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sHoster = eval(sHoster)

    for sHosterUrl in sHoster:
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


# Ajout d'un lien pastebin
def addPasteID():
    oGui = cGui()
    addons = addon()

    # Recherche d'un setting de libre
    names = set()
    numID = 0
    newID = 1
    while True:
        numID += 1
        pasteLabel = addons.getSetting(SETTING_PASTE_LABEL + str(numID))
        if pasteLabel == '':
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
    if not dialog().VSyesno(addons.VSlang(30412)):
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
    

