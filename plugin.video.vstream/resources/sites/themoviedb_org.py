# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, addon, dialog, VSupdate, isMatrix, siteManager
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.tmdb import cTMDb

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = '[COLOR orange]TheMovieDB[/COLOR]'
SITE_DESC = 'Base de données video.'

# doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

API_KEY = '92ab39516970ab9d86396866456ec9b6'
API_VERS = '3'
API_URL = URL_MAIN + API_VERS

# FANART_URL = 'https://image.tmdb.org/t/p/original/'
# https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6

view = '500'
tmdb_session = ''
tmdb_account = ''


def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', '%s (TMDB)' % addons.VSlang(30330), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30425), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30426), 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30427), 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', addons.VSlang(30428), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30429), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30430), 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'tv/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30431), 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreTV', addons.VSlang(30432), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'person/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showActors', addons.VSlang(30433), 'actor.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('topimdb', 'load', 'Top Imdb', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showFolderList', 'Listes TMDB', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', addons.VSlang(30423), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', addons.VSlang(30424), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'search/person')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchActor', addons.VSlang(30450), 'search.png', oOutputParameterHandler)

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
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30436), 'views.png', oOutputParameterHandler)

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
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30440), 'views.png', oOutputParameterHandler)

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
    grab = cTMDb()
    dialogs = dialog()

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
        numboard = dialogs.numeric(0, 'Min 0.5 - Max 10')
        if numboard != None:
            sAction = '%s/%s/rating' % (sCat, sTMDB)
            sPost = {"value": numboard}
        else:
            return

    else:
        sPost = {"media_type": sCat, "media_id": sTMDB, sFow: sYn}

    data = grab.getPostUrl(sAction, sPost)

    if len(data) > 0:
        dialogs.VSinfo(data['status_message'])

    return


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


def getToken():
    grab = cTMDb()
    return grab.getToken()


def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        showMovies(sSearchText.replace(' ', '+'))
        # oGui.setEndOfDirectory()
        return


def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        showSeries(sSearchText.replace(' ', '+'))
        # oGui.setEndOfDirectory()
        return


def showSearchActor():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        showActors(sSearchText.replace(' ', '+'))
        # oGui.setEndOfDirectory()
        return


def showGenreMovie():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenreTV():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")
            # sUrl = API_URL + '/genre/' + str(sId) + '/tv'
            sUrl = 'discover/tv'
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('genre', sId)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

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
    total = len(result)
    if total > 0:
        oOutputParameterHandler = cOutputParameterHandler()
        for i in result['results']:
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


def showMovies(sSearch=''):
    oGui = cGui()
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
        total = len(result)
        if total > 0:
            total = len(result['results'])
            progress_ = progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

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

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError as e:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    # changement mode
    view = addons.getSetting('visuel-view')

    oGui.setEndOfDirectory(view)


def showSeries(sSearch=''):
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if oInputParameterHandler.exist('genre'):
            term = 'with_genres=' + oInputParameterHandler.getValue('genre')

        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        result = grab.getUrl(sUrl, iPage, term)

    oGui = cGui()

    try:
        total = len(result)

        if total > 0:
            total = len(result['results'])
            progress_ = progress().VScreate(SITE_NAME)

            for i in result['results']:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

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

                cGui.CONTENT = "tvshows"
                oGuiElement = cGuiElement()
                oGuiElement.setTmdbId(sId)
                oGuiElement.setSiteName(SITE_IDENTIFIER)  # à activer pour saisons
                oGuiElement.setFunction('showSeriesSaison')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setFileName(sTitle)
                oGuiElement.setIcon('series.png')
                oGuiElement.setMeta(2)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setPoster(sThumb)
                oGuiElement.setFanart(sFanart)
                oGuiElement.setCat(2)
                oGuiElement.setDescription(sDesc)
                oGuiElement.setYear(sYear)
                oGuiElement.setGenre(sGenre)

                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            progress_.VSclose(progress_)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)
                if oInputParameterHandler.exist('genre'):
                    oOutputParameterHandler.addParameter('genre', oInputParameterHandler.getValue('genre'))
                oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun résultat n\'a été trouvé.[/COLOR]')

    # changement mode
    view = addons.getSetting('visuel-view')

    oGui.setEndOfDirectory(view)


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
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        total = len(result['seasons'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['seasons']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')

    oGui.setEndOfDirectory(view)


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
        total = len(result['episodes'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['episodes']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')
    oGui.setEndOfDirectory(view)


def showActors(sSearch=''):
    oGui = cGui()
    grab = cTMDb()
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
        # à cause d'un ? pas ou il faut pour ça >> invalid api key
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

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if not isMatrix():
                sName = sName.encode('utf-8')

            oOutputParameterHandler.addParameter('siteUrl', 'person/' + str(i['id']) + '/movie_credits')
            sTitle = str(sName)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showFilmActor')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sName)
            oGuiElement.setIcon('actors.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumb)
            oGuiElement.setPoster(sThumb)
            oGuiElement.setCat(7)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

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


def showFilmActor():
    oGui = cGui()
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    result = grab.getUrl(sUrl, iPage)

    total = len(result)
    if total > 0:
        total = len(result['cast'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['cast']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Mise en forme des infos (au format meta imdb)
            i = grab._format(i, '', "person")

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

        progress_.VSclose(progress_)

    # changement mode
    view = addons.getSetting('visuel-view')

    oGui.setEndOfDirectory(view)


def showLists():
    oGui = cGui()
    grab = cTMDb()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    result = grab.getUrl('list/' + sUrl, iPage, '')
    total = len(result)
    if total > 0:
        total = len(result['items'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['items']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

        progress_.VSclose(progress_)

    view = addons.getSetting('visuel-view')

    oGui.setEndOfDirectory(view)


def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span><a class='page-numbers' href='([^<]+)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return aResult[1][0]

    return False
