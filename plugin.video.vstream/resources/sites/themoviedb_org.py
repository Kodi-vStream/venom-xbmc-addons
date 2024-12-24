# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import addon, dialog, VSupdate, isMatrix, siteManager
from resources.lib.util import cUtil
from resources.lib.tmdb import cTMDb

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = 'TheMovieDB'
SITE_DESC = 'Base de données video.'

# doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

API_VERS = '3'
API_URL = URL_MAIN + API_VERS

# FANART_URL = 'https://image.tmdb.org/t/p/original/'
# https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6

view = '500'
tmdb_session = ''
tmdb_account = ''

DIFFUSEURS = {
            141: 'ICI Radio-Canada Télé', 302:'TVA',
            1131: 'Télé-Québec', 1312: 'ICI TOU.TV',
            1290: 'Club Illico', 1344: 'Crave',
            3529: 'ICI TOU.TV - EXTRA', 4161: 'Noovo',
            5071: 'Vrai', 4330: 'Paramount+',
            213: 'Netflix', 1024: 'Prime Video',
            285: 'Canal+', 1899: 'OCS Max',
            2058: '13e rue', 129: 'A&E',
            2: 'ABC', 1628: 'Arte', 88: 'FX',
            5522: 'Arte.TV', 80: 'Adult Swim',
            2552: 'Apple TV+', 4: 'BBC One',
            16: 'CBS', 64: 'Discovery',
            2739: 'Disney+', 19: 'FOX',
            49: 'HBO', 453: 'Hulu',
            712: 'M6', 6: 'NBC', 21: 'Warner Bros',
            43: 'National Geographic', 13: 'Nickelodeon',
            67: 'Showtime', 318: 'Starz',
            77: 'Syfy', 290: 'TF1', 174: 'AMC',
            71: 'The CW', 3353: 'Peacock'
            }


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilm', "Films", 'films.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSerie', "Séries", 'tv.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', 'person/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuActeur', "Acteurs", 'actor.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showMenuFilm():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', "%s - %s" % (addons.VSlang(30076), addons.VSlang(30120)), 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSaga', "%s - %s" % (addons.VSlang(30076), addons.VSlang(30139)), 'search-sagas.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30101), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', addons.VSlang(30428), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30104), 'notes.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', 'http://')
    # oGui.addDir(SITE_IDENTIFIER, 'showFolderList', 'Listes TMDB', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSerie():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', addons.VSlang(30121), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30101), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreTV', addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30431), 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMenuActeur():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'search/person')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchActor', addons.VSlang(30076), 'search-actor.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'person/popular?language=en-EN')
    oGui.addDir(SITE_IDENTIFIER, 'searchActors', addons.VSlang(30102), 'actor.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMyTmdb():
    oGui = cGui()
    grab = cTMDb()
    addons = addon()

    tmdb_session = addons.getSetting('tmdb_session')
    if tmdb_session == '':
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'https://')
        oGui.addDir(SITE_IDENTIFIER, 'getToken', addons.VSlang(30305), 'tmdb.png', oOutputParameterHandler)
    else:
        # pas de deco possible avec l'api donc on test l'username sinon ont supprime tous
        result = grab.getUrl('account', '1', 'session_id=' + tmdb_session)

        if 'username' in result and result['username']:

            # pas de menu sans ID user c'est con
            addons.setSetting('tmdb_account', str(result['id']))

            sUsername = result['username']
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'https://')
            oGui.addText(SITE_IDENTIFIER, (addons.VSlang(30306)) % sUsername)

            # /account/{account_id}/favorite/movies
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/favorite/movies' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30434), 'films.png', oOutputParameterHandler)

            # /account/{account_id}/rated/movies
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/rated/movies' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30435), 'notes.png', oOutputParameterHandler)

            # /account/{account_id}/watchlist/movies
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/watchlist/movies' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30436), 'popular.png', oOutputParameterHandler)

            # /account/{account_id}/favorite/tv
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/favorite/tv' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30437), 'series.png', oOutputParameterHandler)

            # /account/{account_id}/rated/tv
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/rated/tv' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30438), 'notes.png', oOutputParameterHandler)

            # /account/{account_id}/watchlist/tv
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/watchlist/tv' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30440), 'popular.png', oOutputParameterHandler)

            # /account/{account_id}/rated/tv/episodes
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/rated/tv/episodes' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30439), 'notes.png', oOutputParameterHandler)

            # /account/{account_id}/lists
            oOutputParameterHandler.addParameter('session_id', tmdb_session)
            oOutputParameterHandler.addParameter('siteUrl', 'account/%s/lists' % int(result['id']))
            oGui.addDir(SITE_IDENTIFIER, 'showUserLists', addons.VSlang(30441), 'listes.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('siteUrl', 'http://')
            oGui.addDir(SITE_IDENTIFIER, 'ouTMyTmdb', addons.VSlang(30309), 'listes.png', oOutputParameterHandler)

        else:
            ouTMyTmdb()

    oGui.setEndOfDirectory()


def ouTMyTmdb():
    addons = addon()
    addons.setSetting('tmdb_session', '')
    addons.setSetting('tmdb_account', '')

    dialog().VSinfo(addons.VSlang(30320))
    VSupdate()
    showMyTmdb()
    return


def getContext():
    addons = addon()
    dialogs = dialog()

    tmdb_account = addons.getSetting('tmdb_account')
    if tmdb_account == "":
        dialogs.VSerror(addons.VSlang(30442))
        return False, False, False

    disp = []
    lang = []
    fow = []
    yn = []

    disp.append('vote')
    fow.append('vote')
    yn.append(True)
    lang.append(addons.VSlang(30443))

    disp.append('account/%s/watchlist' % tmdb_account)
    fow.append('watchlist')
    yn.append(True)
    lang.append(addons.VSlang(30444))

    disp.append('account/%s/favorite' % tmdb_account)
    fow.append('favorite')
    yn.append(True)
    lang.append(addons.VSlang(30445))

    disp.append('addtolist')
    fow.append('addtolist')
    yn.append(True)
    lang.append(addons.VSlang(31211))    

    disp.append('addtonewlist')
    fow.append('addtonewlist')
    yn.append(True)
    lang.append(addons.VSlang(31210))  

    disp.append('account/%s/watchlist' % tmdb_account)
    fow.append('watchlist')
    yn.append(False)
    lang.append(addons.VSlang(30446))

    disp.append('account/%s/favorite' % tmdb_account)
    fow.append('favorite')
    yn.append(False)
    lang.append(addons.VSlang(30447))

    ret = dialogs.VSselect(lang, 'TMDB')
    if ret > -1:
        return disp[ret], fow[ret], yn[ret]

    return False


def getCat():

    disp = ['1', '2']
    dialogs = dialog()
    dialog_select = 'Films', 'Series'

    ret = dialogs.select('TMDB', dialog_select)
    if ret > -1:
        sType = disp[ret]

    return sType


def getAction():
    oGui = cGui()
    grab = cTMDb()
    dialogs = dialog()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()

    sAction = ''
    if not sAction:
        sAction, sFow, sYn = getContext()
    if not sAction:
        return

    sCat = oInputParameterHandler.getValue('sCat')
    if not sCat:
        sCat = getCat()
    if not sCat:
        return

    # dans le doute si meta active
    sTMDB = oInputParameterHandler.getValue('sTmdbId')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')

    sCat = sCat.replace('1', 'movie').replace('2', 'tv')

    if not sTMDB:
        sTMDB = grab.get_idbyname(oInputParameterHandler.getValue('sFileName'), '', sCat)
    if not sTMDB:
        return

    if sAction == 'vote':
        # vote /movie/{movie_id}/rating
        # /tv/{tv_id}/rating
        # /tv/{tv_id}/season/{season_number}/episode/{episode_number}/rating
        numboard = oGui.showNumBoard('Min 0.5 - Max 10')
        if numboard != None:
            if sSeason is not False and sEpisode is not False:
                sAction = '%s/%s/season/%s/episode/%s/rating' % (sCat, sTMDB, sSeason, sEpisode)
            else:
                sAction = '%s/%s/rating' % (sCat, sTMDB)
            sPost = {"value": numboard}
        else:
            return

    elif sAction == 'addtolist':
        if sCat == 'tv':
            dialogs.VSinfo("Vous ne pouvez pas ajouter une série à une liste de films tmdb")
            return
        result = grab.getUrl('account/%s/lists' % addons.getSetting('tmdb_account'), term='session_id=%s' % addons.getSetting('tmdb_session'))
        total = len(result)
        if total == 0:
            return
        labels = []
        for i in result['results']:
            labels.append(i['name'])
        idliste = dialogs.VSselect(labels, addons.VSlang(31212))
        if idliste == -1 :
            return
        
        idliste = result['results'][idliste]['id']
        sAction = 'list/%s/add_item' % (idliste)
        sPost = {"media_id": sTMDB}

    elif sAction == 'addtonewlist':
        if sCat == 'tv':
            dialogs.VSinfo("Vous ne pouvez pas ajouter une série à une liste de films tmdb")
            return        
        # nom de la nouvelle liste
        listname = oGui.showKeyBoard()
        if listname == '':
            return
        # creation de la liste
        sAction = 'list'
        sPost = {
                "name": listname,
                "description": " ",
                "language": "fr"
                }
        rep = grab.getPostUrl(sAction, sPost)
        # recuperer son id
        if 'success' in rep:
            idliste = rep['list_id']
        else:
            return
        # ajout du film à la nouvelle liste
        sAction = 'list/%s/add_item' % (idliste)
        sPost = {"media_id": sTMDB}

    else:
        sPost = {"media_type": sCat, "media_id": sTMDB, sFow: sYn}

    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        dialogs.VSinfo(data['status_message'])

    return

"""
# comme le cat change pour le type ont refait
def getWatchlist():
    grab = cTMDb()
    addons = addon()

    tmdb_session = addons.getSetting('tmdb_session')
    tmdb_account = addons.getSetting('tmdb_account')

    if not tmdb_session:
        return

    if not tmdb_account:
        return

    oInputParameterHandler = cInputParameterHandler()
    sCat = oInputParameterHandler.getValue('sCat')
    if not sCat:
        return

    sCat = sCat.replace('1', 'movie').replace('2', 'tv')

    # dans le doute si meta active
    sTMDB = oInputParameterHandler.getValue('sTmdbId')
    sTitle = oInputParameterHandler.getValue('sFileName')

# import re
#     if sCat == "tv":
#         sSeason = re.search('aison (\d+)',sTitle).group(1)
#         sEpisode = re.search('pisode (\d+)',sTitle).group(1)

    if not sTMDB:
        sTMDB = grab.get_idbyname(sTitle, '', sCat)
    if not sTMDB:
        return

    sPost = {"media_type": sCat, "media_id": sTMDB, 'watchlist': True}
    sAction = 'account/%s/watchlist' % tmdb_account

    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        dialog().VSinfo(data['status_message'])

    return

"""
def getToken():
    grab = cTMDb()
    return grab.getToken()


def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText.replace(' ', '+'))
        # oGui.setEndOfDirectory()
        return


def showSearchSaga():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        searchSagas(sSearchText.replace(' ', '+'))
        return


def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showSeries(sSearchText.replace(' ', '+'))
        return


def showSearchActor():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        searchActors(sSearchText.replace(' ', '+'))
        return


def showGenreMovie():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    term = 'with_original_language=en|fr&'
#    term += '&with_status=3|4'
    term += '&with_genres=%d'

    # if oInputParameterHandler.exist('genre'):
    #     term += '&with_genres=' + oInputParameterHandler.getValue('genre')
    

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")
#            sUrl = 'genre/' + str(sId) + '/movies'
            sUrl = 'discover/movie'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('term', term % sId)
            oGui.addGenre(SITE_IDENTIFIER, 'showMovies', str(sTitle), oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenreTV():
    oGui = cGui()
    grab = cTMDb()

    # grab.TMDB_GENRES
    # "Talk", "News", "Réalité" # 10767, 10763, 10764
    ignoredGenres = (10763, 10764, 10767)

    term = 'with_original_language=en|fr&'
    term += '&without_genres=10763|10764|10767'
    term += '&with_status=3|4'
    term += '&with_genres=%d'

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']
            if sId in ignoredGenres:
                continue

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")
            # sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            sUrl = 'discover/tv'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('term', term % sId)
            oGui.addGenre(SITE_IDENTIFIER, 'showSeries', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showUserLists():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('session_id'):
        term += 'session_id=' + oInputParameterHandler.getValue('session_id')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    result = grab.getUrl(sUrl, iPage, term)
    results = result['results']
    # Compter le nombre de pages
    nbpages = result['total_pages']
    page = 2
    while page <= nbpages:
        result = grab.getUrl(sUrl, page, term)
        results += result['results']
        page += 1
    total = len(results)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in results:
            sId, sTitle = i['id'], i['name']

            # sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            oOutputParameterHandler.addParameter('siteUrl', sId)
            oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showFolderList():
    oGui = cGui()

    liste = []
    liste.append(['Top 50 des plus grands films', '10'])
    liste.append(['Gagnants des Oscars', '31670'])
    liste.append(['Les films fascinants ', '43'])
    liste.append(['science-fiction', '3945'])
    liste.append(['Les adaptations', '9883'])
    liste.append(['Disney Classic', '338'])
    liste.append(['Pixar', '3700'])
    liste.append(['Marvel', '1'])
    liste.append(['DC Comics Universe', '3'])
    liste.append(['Top Manga', '31665'])
    liste.append(['Top Manga 2', '31695'])
    liste.append(['Best séries', '36788'])
    liste.append(['Films de Noel', '40944'])
    # liste.append(['nom de la liste', 'ID de la liste'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Dernieres séries selon la date de sortie
def showMoviesNews():
    term = 'sort_by=primary_release_date.desc&'
#    term += 'primary_release_date.lte=2024-10-11&'
#    term += 'with_runtime.gte=65&'
    term += 'without_genres=99&'
    term += 'vote_count.gte=10'
    showMovies(term=term)

# TOP séries, selon la note / votes 
def showMoviesTop():
    term = 'sort_by=vote_average.desc&vote_count.gte=4000&'
    showMovies(term=term)


def showMovies(sSearch='', term=''):
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if oInputParameterHandler.exist('term'):
            term = oInputParameterHandler.getValue('term')
        else:
            term += 'with_original_language=en|fr'
    
            # exclure les films à venir
            # term += '&with_status=3|4'
    
            if oInputParameterHandler.exist('session_id'):
                term += '&session_id=' + oInputParameterHandler.getValue('session_id')
    
        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
        total = len(result)
        if total > 0:
            for i in result['results']:
                # Mise en forme des infos (au format meta imdb)
                i = grab._format(i, '', "movie")

                sId, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sTmdbId', sId)
                oOutputParameterHandler.addParameter('type', 'film')

                if isMatrix():
                    oOutputParameterHandler.addParameter('searchtext', sTitle)
                else:
                    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

                cGui.CONTENT = "movies"
                oGuiElement = cGuiElement()
                oGuiElement.setTmdbId(sId)
                oGuiElement.setSiteName('globalSearch')
                oGuiElement.setFunction('showSearch')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setFileName(sTitle)
                oGuiElement.setIcon('films.png')
                oGuiElement.setMeta(1)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setPoster(sThumb)
                oGuiElement.setFanart(sFanart)
                oGuiElement.setCat(1)
                oGuiElement.setDescription(sDesc)
                oGuiElement.setYear(sYear)
                oGuiElement.setGenre(sGenre)

                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oOutputParameterHandler.addParameter('term', term)
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError as e:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    oGui.setEndOfDirectory()


def searchSagas(sSearch=''):
    oGui = cGui()
    grab = cTMDb()

    if not sSearch:
        oInputParameterHandler = cInputParameterHandler()
        sSearch = oInputParameterHandler.getValue('searchtext')


    result = grab.getUrl('search/collection', 1, 'query=' + sSearch)
    try:
        total = len(result)
        if total > 0:
            for i in result['results']:
                # Mise en forme des infos (au format meta imdb)
                i = grab._format(i, '', "movie")

                sId, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']
                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'collection/%s' % sId)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sTmdbId', sId)

                oGui.addMoviePack(SITE_IDENTIFIER, 'showSagaMovies', sTitle, '', '', oOutputParameterHandler)

    except TypeError as e:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    oGui.setEndOfDirectory()


def showSagaMovies():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    result = grab.getUrl(sUrl)

    try:
        total = len(result)
        if total > 0:
            movies = result['parts']
            for i in sorted(movies, key=lambda movie: movie['release_date']):
                
                if not i['release_date']:
                    continue    # pas sortie
                
                i = grab._format(i, '', "movie")
                sId, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sTmdbId', sId)

                if isMatrix():
                    oOutputParameterHandler.addParameter('searchtext', sTitle)
                else:
                    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

                # oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', '', '', oOutputParameterHandler)
                oGui.addMovie('globalSearch', 'showSearch', sTitle, 'films.png', '', '', oOutputParameterHandler)

    except TypeError as e:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    oGui.setEndOfDirectory()

# Films par années
def showMoviesYears():
    showYears(True)

# Séries par années
def showSeriesYears():
    showYears(False)

def showYears(movie = False):
    oGui = cGui()
    import datetime
    
    term = 'with_original_language=en|fr&'
    term += '&without_genres=10767|10763|10764'
    if movie:
        url = 'discover/movie'
        func = 'showMovies'
        term += '&primary_release_year=%d'
    else:
        url = 'discover/tv'
        func = 'showSeries'
        term += '&with_status=3|4'
        term += '&first_air_date_year=%d'
        
            
    oOutputParameterHandler = cOutputParameterHandler()  # Pas de lien après 2022
    for year in reversed(range(1960, int(datetime.datetime.now().year) + 1)):
#         = str(i)
        oOutputParameterHandler.addParameter('siteUrl', url)
        oOutputParameterHandler.addParameter('term', term % year)
        oGui.addDir(SITE_IDENTIFIER, func, str(year), 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

'''
(BET)
(Boomerang)
(BrutX)
'''

# par diffuseurs
def showSeriesNetworks():
    oGui = cGui()
    
    term = 'with_original_language=en|fr&'
    term += '&without_genres=10767|10763|10764'
    term += '&with_status=3|4'
    term += '&with_networks=%d'
    
    for netID, name in sorted(DIFFUSEURS.items(), key=lambda diff: diff[1]):
        oOutputParameterHandler = cOutputParameterHandler()  # Pas de lien après 2022
        oOutputParameterHandler.addParameter('siteUrl', 'discover/tv')
        oOutputParameterHandler.addParameter('term', term % netID)
        oOutputParameterHandler.addParameter('sTmdbId', netID)    # Utilisé par TMDB
#        oOutputParameterHandler.addParameter('network', netID)    # Utilisé par TMDB
        
        oGui.addNetwork(SITE_IDENTIFIER, 'showSeries', name, 'host.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

# Dernieres séries selon la date de sortie
def showSeriesNews():
    # Exclure les séries d'Asie/Inde
    term = 'with_original_language=en|fr&sort_by=first_air_date.desc&'
    showSeries(term=term)

# Séries populaires
def showSeriesViews():
    term = 'with_original_language=en|fr&'
    showSeries(term=term)

# TOP séries, selon la note / votes 
def showSeriesTop():
    term = 'with_original_language=en|fr&sort_by=vote_average.desc&vote_count.gte=1900&'
    showSeries(term=term)

# japanimes populaires
def showAnimes():
    term = 'with_keywords=210024&' # &with_genres=16
    if addon().getSetting('contenu_adulte') == 'false':
        term += 'without_companies=125825&vote_count.gte=150&'
    showSeries(term=term)

# Derniers japanimes
def showAnimesNews():
    term = 'sort_by=first_air_date.desc&with_keywords=210024&'
    adult = addon().getSetting('contenu_adulte')
    if adult == 'false':
        term += 'without_companies=125825&vote_count.gte=150&'
    showSeries(term=term)

# TOP japanimes, selon la note / votes 
def showAnimesTop():
    term = 'with_keywords=210024&sort_by=vote_average.desc&vote_count.gte=800&'
    if addon().getSetting('contenu_adulte') == 'false':
        term += 'without_companies=125825&'
    showSeries(term=term)


# drama 'with_origin_country=KR'
# def showDramas():


# séries classées par défaut : POPULAIRE
def showSeries(sSearch='', term=''):
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''
    else:
        if oInputParameterHandler.exist('term'):
            term = oInputParameterHandler.getValue('term')
        else:
            
            # genre à exclure
            # grab.TMDB_GENRES
            # "Talk", "News", "Réalité" # 10767, 10763, 10764
            term += '&without_genres=10767|10763|10764'
            
            # exclure les séries à venir, [0 .. 5]
            #['Returning Series', 'Planned', 'In Production', 'Ended', 'Canceled', 'Pilot']
            term += '&with_status=3|4'
            
            if oInputParameterHandler.exist('session_id'):
                term += '&session_id=' + oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    oGui = cGui()

    try:
        total = len(result)

        if total > 0:
            for i in result['results']:
                # Mise en forme des infos (au format meta imdb)
                i = grab._format(i, '', "tvshow")
                sId, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                if not isMatrix():
                    sTitle = sTitle.encode("utf-8")

                sSiteUrl = 'tv/' + str(sId)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sId', sId)
                oOutputParameterHandler.addParameter('sFanart', sFanart)
                oOutputParameterHandler.addParameter('sTmdbId', sId)

                if isMatrix():
                    oOutputParameterHandler.addParameter('searchtext', sTitle)
                else:
                    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

                # série OU japanime
                anime = 'with_keywords=210024' in term

                cGui.CONTENT = "tvshows"
                oGuiElement = cGuiElement()
                oGuiElement.setTmdbId(sId)
                oGuiElement.setSiteName('globalSearch')
                oGuiElement.setFunction('searchMovie')
                # oGuiElement.setSiteName(SITE_IDENTIFIER)  # à remplacer pour saisons
                # oGuiElement.setFunction('showSeriesSaison')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setFileName(sTitle)
                oGuiElement.setIcon('series.png')
                oGuiElement.setMeta(4 if anime else 2)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setPoster(sThumb)
                oGuiElement.setFanart(sFanart)
                oGuiElement.setCat(3 if anime else 2)
                oGuiElement.setDescription(sDesc)
                oGuiElement.setYear(sYear)
                oGuiElement.setGenre(sGenre)

                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oOutputParameterHandler.addParameter('term', term)
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)
                oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    oGui.setEndOfDirectory()


def showSeriesSaison():
    oGui = cGui()
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sId = oInputParameterHandler.getValue('sId')

    if sId is False:
        sId = sUrl.split('/')[-1]

    if sFanart is False:
        sFanart = ''

    # recherche la serie complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    # oOutputParameterHandler.addParameter('type', 'serie')
    # oOutputParameterHandler.addParameter('searchtext', sMovieTitle)
    if not isMatrix():
        oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))
    else:
        oOutputParameterHandler.addParameter('searchtext', sMovieTitle)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(addons.VSlang(30414))
    oGuiElement.setCat(2)
    oGuiElement.setTmdbId(sTmdbId)
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['seasons']:
            sNbreEp, SSeasonNum = i['episode_count'], i['season_number']

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '', "season")
            sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            sTitle = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            sUrl = 'tv/' + str(sId) + '/season/' + str(SSeasonNum)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sSeason', SSeasonNum)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeriesEpisode')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(7)
            oGuiElement.setDescription(sDesc)
            oGuiElement.setYear(sYear)
            oGuiElement.setGenre(sGenre)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesEpisode():
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')

    sSeason = oInputParameterHandler.getValue('sSeason')
    # sId = oInputParameterHandler.getValue('sId')
    if sSeason is False:
        sSeason = sUrl.split('/')[-1]

    if sFanart is False:
        sFanart = ''

    oGui = cGui()

    # recherche saison complète
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    # oOutputParameterHandler.addParameter('type', 'serie')
    search = '%s S%02d' % (sMovieTitle, int(sSeason))
    # oOutputParameterHandler.addParameter('searchtext', search)

    if not isMatrix():
        oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(search))
    else:
        oOutputParameterHandler.addParameter('searchtext', search)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(addons.VSlang(30415))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    result = grab.getUrl(sUrl)

    total = len(result)
    if total > 0 and 'episodes' in result:
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['episodes']:
            # sId, sTitle, sOtitle, sThumb, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            sEpNumber = i['episode_number']

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '')
            sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")

            sTitle = 'S%s E%s %s' % (sSeason, str(sEpNumber), sTitle)

            sExtraTitle = ' S' + "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpNumber)

            oOutputParameterHandler.addParameter('siteUrl', sMovieTitle + '|' + sExtraTitle)  # Pour compatibilite Favoris
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sEpisode', sEpNumber)
            oOutputParameterHandler.addParameter('type', 'serie')

            if not isMatrix():
                oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))
            else:
                oOutputParameterHandler.addParameter('searchtext', sMovieTitle)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(2)
            oGuiElement.setDescription(sDesc)
            oGuiElement.setYear(sYear)
            oGuiElement.setGenre(sGenre)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def searchActors(sSearch=''):
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if not sUrl:
        sUrl = 'search/person'
        
    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('searchtext'):    # pour les raccourcis d'habillage
        sSearch = oInputParameterHandler.getValue('searchtext')

    if sSearch:
        # format obligatoire évite de modif le format de l'url dans la lib >> _call
        # à cause d'un ? pas ou il faut pour ça >> invalid api key
        result = grab.getUrl(sUrl, iPage, 'query=' + sSearch)

    else:
        result = grab.getUrl(sUrl, iPage)

    total = len(result)

    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()

        # récup le nombre de page pour NextPage
        nbrpage = result['total_pages']

        for actor in result['results']:
            sName, sThumb = actor['name'], actor['profile_path']

            # filtrer les acteurs peu connus 
            if len(actor['known_for']) < 3 or actor['popularity'] < 5.0:
                continue 
            # enlever les acteurs asie/inde
            film_lang = actor['known_for'][0]['original_language']
            if 'en' not in film_lang and 'fr' not in film_lang:
                continue

            if sThumb:
                POSTER_URL = grab.poster
                sThumb = POSTER_URL + sThumb
            else:
                sThumb = ''


            if not isMatrix():
                sName = sName.encode('utf-8')

            actorId = str(actor['id'])
            sTitle = str(sName)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', actorId)    # Utilisé par TMDB
            oOutputParameterHandler.addParameter('siteUrl', 'person/' + actorId + '/movie_credits')
            oGui.addPerson(SITE_IDENTIFIER, 'showFilmActor', sTitle, 'actor.png', sThumb, oOutputParameterHandler)
            
        if int(iPage) < int(nbrpage):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)

            # ajoute param sSearch pour garder le bon format d'url avec grab url
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)

            oGui.addNext(SITE_IDENTIFIER, 'searchActors', 'Page ' + str(iNextPage), oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showFilmActor():
    oGui = cGui()
    grab = cTMDb()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    result = grab.getUrl(sUrl, iPage)

    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['cast']:
            
            # exclure les documentaires, talk, animation
            genres = i['genre_ids']
            if len(genres) == 0 or 16 in genres or 99 in genres or 10767 in genres:
                continue
            
            # exclure les interventions, ou voix
            character = i['character']
            if '(voice' in character or '(archive' in character:
                continue
            
            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '', "person")

            if i['votes'] < 100:
                continue


            sId, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")

            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            oOutputParameterHandler.addParameter('type', 'film')

            if not isMatrix():
                oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))
            else:
                oOutputParameterHandler.addParameter('searchtext', sTitle)

            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('films.png')
            oGuiElement.setMeta(1)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(1)
            oGuiElement.setDescription(sDesc)
            oGuiElement.setYear(sYear)
            oGuiElement.setGenre(sGenre)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLists():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    result = grab.getUrl('list/' + sUrl, iPage, '')
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['items']:
            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '')

            sId, sTitle, sType, sThumb, sFanart, sVote, sDesc, sYear = i['tmdb_id'], i['title'], i['media_type'], i['poster_path'], i['backdrop_path'], i['rating'], i['plot'], i['year']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")

            sDisplayTitle = "%s (%s)" % (sTitle, sVote)

            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sId)

            if isMatrix():
                oOutputParameterHandler.addParameter('searchtext', sTitle)
            else:
                oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sDisplayTitle)
            oGuiElement.setFileName(sTitle)
            if sType == 'movie':
                oGuiElement.setIcon('films.png')
                oGuiElement.setMeta(1)
                oGuiElement.setCat(1)
            elif sType == 'tv':
                oGuiElement.setIcon('series.png')
                oGuiElement.setMeta(2)
                oGuiElement.setCat(2)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setFanart(sFanart)
            oGuiElement.setDescription(sDesc)
            oGuiElement.setYear(sYear)
            if 'genre' in i:
                oGuiElement.setGenre(i['genre'])

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    return False
