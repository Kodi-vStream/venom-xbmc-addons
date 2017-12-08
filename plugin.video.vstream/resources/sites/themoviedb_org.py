#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import util
import urllib, unicodedata, re
import xbmcgui, xbmc
from resources.lib.tmdb import cTMDb

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = '[COLOR orange]TheMovieDB[/COLOR]'
SITE_DESC = 'Base de données video.'

#doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = 'https://www.themoviedb.org/'

API_KEY = '92ab39516970ab9d86396866456ec9b6'
API_VERS = '3'
API_URL = URL_MAIN+API_VERS

POSTER_URL = 'https://image.tmdb.org/t/p/w396'
#FANART_URL = 'https://image.tmdb.org/t/p/w780/'
FANART_URL = 'https://image.tmdb.org/t/p/w1280'
#FANART_URL = 'https://image.tmdb.org/t/p/original/'


#https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6

grab = cTMDb(api_key=cConfig().getSetting('api_tmdb'))
view = '500'
view = cConfig().getSetting('visuel-view')

xbmcgui.Window(10101).clearProperty('search_disp')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche de Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche de Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Populaires)', 'films_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films en salle', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Les mieux notés)', 'films_notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'genre/movie/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries (Populaires)', 'series_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries a la tv', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries (Les mieux notés)', 'series_notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'genre/tv/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreTV', 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'person/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showActors', 'Acteurs Populaires', 'actor.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir('topimdb', 'load', 'Top Imdb', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showFolderList', 'Listes TMDB', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return

def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showSeries(sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenreMovie():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)

    total = len(result)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")
            sUrl = 'genre/' + str(sId) + '/movies'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreTV():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    result = grab.getUrl(sUrl)

    total = len(result)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")
            #sUrl = API_URL+'/genre/'+str(sId)+'/tv'
            sUrl = 'discover/tv'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('genre', str(sId))
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', str(sTitle), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showFolderList():
    oGui = cGui()
    liste = []
    liste.append( ['Top Manga', '31665'] )
    liste.append( ['Top Manga 2', '31695'] )
    liste.append( ['Disney Classic', '338'] )
    liste.append( ['Pixar', '3700'] )
    liste.append( ['Top 50 des plus grands films', '10'] )
    liste.append( ['Marvel', '1'] )
    liste.append( ['DC Comics Universe', '3'] )
    liste.append( ['Les films fascinants ', '43'] )
    liste.append( ['Gagnants des Oscars', '31670'] )
    liste.append( ['Les adaptations', '9883'] )
    liste.append( ['science-fiction', '3945'] )
    liste.append( ['Best séries', '36788'] )
    liste.append( ['Films de Noel', '40944'] )
    #liste.append( ['nom de la liste', 'ID de la liste'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showLists', sTitle, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    if (oInputParameterHandler.exist('sSearch')):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage)

    oGui = cGui()

    total = len(result)

    if (total > 0):

        dialog = util.createDialog(SITE_NAME)
        for i in result['results']:

            total = len(result['results'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sId, sTitle, sOtitle, sThumbnail, sFanart, sDesc = i['id'], i['title'], i['original_title'], i['poster_path'], i['backdrop_path'], i['overview']
            if sThumbnail:
                sThumbnail = POSTER_URL + sThumbnail
            else: sThumbnail = ''

            sTitle = sTitle.encode("utf-8")
            if sFanart:
                sFanart = FANART_URL + sFanart
            else : sFanart = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            oOutputParameterHandler.addParameter('type', 'film')
            #oOutputParameterHandler.addParameter('searchtext', showTitle(sTitle,  str('none')))
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            #oGui.addMovieDB('globalSearch', 'showHosters', sTitle, 'films.png', sThumbnail, sFanart, oOutputParameterHandler)
            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('films.png')
            oGuiElement.setMeta(1)
            oGuiElement.setMetaAddon('true')
            #oGuiElement.setThumbnail(sThumbnail)
            #oGuiElement.setPoster(sThumbnail)
            #oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(1)
            oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', oOutputParameterHandler)


    #test pr chnagement mode
    #xbmc.executebuiltin('Container.SetViewMode(500)')

    oGui.setEndOfDirectory(view)

def showSeries(sSearch=''):
    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    if (oInputParameterHandler.exist('sSearch')):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if (oInputParameterHandler.exist('genre')):
            term = 'with_genres=' +  oInputParameterHandler.getValue('genre')
        else :
            term = ''

        result = grab.getUrl(sUrl, iPage, term)

    oGui = cGui()

    total = len(result)

    dialog = util.createDialog(SITE_NAME)

    if (total > 0):
        for i in result['results']:

            total = len(result['results'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sId, sTitle, sOtitle, sThumbnail, sFanart, sDesc = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path'], i['overview']
            if sThumbnail:
                sThumbnail = POSTER_URL + sThumbnail
            else:
                sThumbnail = ''

            if sFanart:
                sFanart = FANART_URL + sFanart
            else : sFanart = ''

            sTitle = sTitle.encode("utf-8")

            sSiteUrl = 'tv/' + str(sId)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sId', str(sId))
            oOutputParameterHandler.addParameter('sFanart', str(sFanart))
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            #oOutputParameterHandler.addParameter('searchtext', sTitle)
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))


            #oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesSaison', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName(SITE_IDENTIFIER) # a activer pour  saisons
            #oGuiElement.setSiteName('globalSearch') # a desactiver pour saison
            oGuiElement.setFunction('showSeriesSaison')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setMetaAddon('true')
            #oGuiElement.setThumbnail(sThumbnail)
            #oGuiElement.setPoster(sThumbnail)
            #oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(2)
            #oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            if sSearch:
                oOutputParameterHandler.addParameter('sSearch', sSearch)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', oOutputParameterHandler)

    #test pr chnagement mode
    #xbmc.executebuiltin('Container.SetViewMode(500)')

    oGui.setEndOfDirectory(view)

def showSeriesSaison():

    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')

    sId = oInputParameterHandler.getValue('sId')
    if sId == False:
        sId = sUrl.split('/')[-1]

    if sFanart == False:
        sFanart = ''

    oGui = cGui()

    #recherche la serie complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    #oOutputParameterHandler.addParameter('type', 'serie')
    #oOutputParameterHandler.addParameter('searchtext', sMovieTitle)
    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(cConfig().getlanguage(30414))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    #oGui.addDir('cHome', 'showSearch', cConfig().getlanguage(30414), 'searchtmdb.png', oOutputParameterHandler)
    #fin

    result = grab.getUrl(sUrl)

    total = len(result)
    dialog = util.createDialog(SITE_NAME)

    if (total > 0):
        for i in result['seasons']:

            total = len(result['seasons'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sdate, sNbreEp, sIdSeason, sThumbnail, SSeasonNum = i['air_date'], i['episode_count'], i['id'], i['poster_path'], i['season_number']

            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = ''

            sTitle = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            sUrl = 'tv/' + sId + '/season/' + str(SSeasonNum)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sSeason', str(SSeasonNum))
            oOutputParameterHandler.addParameter('sFanart', str(sFanart))
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)


            #oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesEpisode', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeriesEpisode')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setMetaAddon('true')
            #oGuiElement.setThumbnail(sThumbnail)
            #oGuiElement.setPoster(sThumbnail)
            #oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(7)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)
    #test pr chnagement mode
    #xbmc.executebuiltin('Container.SetViewMode(500)')

    oGui.setEndOfDirectory(view)

def showSeriesEpisode():

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')

    sSeason = oInputParameterHandler.getValue('sSeason')
    #sId = oInputParameterHandler.getValue('sId')
    if sSeason == False:
        sSeason = sUrl.split('/')[-1]

    if sFanart == False:
        sFanart = ''

    oGui = cGui()

    #recherche saison complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    #oOutputParameterHandler.addParameter('type', 'serie')
    search = '%s S%02d' % (sMovieTitle, int(sSeason))
    #oOutputParameterHandler.addParameter('searchtext', search)
    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(search))


    oGuiElement = cGuiElement()
    oGuiElement.setSiteName('globalSearch')
    oGuiElement.setFunction('searchMovie')
    oGuiElement.setTitle(cConfig().getlanguage(30415))
    oGuiElement.setCat(2)
    oGuiElement.setIcon("searchtmdb.png")
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    #oGui.addDir('cHome', 'showSearch', cConfig().getlanguage(30415), 'searchtmdb.png', oOutputParameterHandler)
    #fin

    result = grab.getUrl(sUrl)

    total = len(result)
    dialog = util.createDialog(SITE_NAME)
    if (total > 0):
        for i in result['episodes']:

            total = len(result['episodes'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #sId, sTitle, sOtitle, sThumbnail, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            sdate, sIdEp, sEpNumber, sName, sThumbnail, SResume = i['air_date'], i['id'], i['episode_number'], i['name'], i['still_path'], i['overview']

            sName = sName.encode("utf-8")
            if sName == '':
                sName = sMovieTitle

            if sThumbnail:
                sThumbnail = POSTER_URL + sThumbnail
            else: sThumbnail = ''

            #sTitle = '[COLOR coral]S' + sSeason + 'E' + str(sEpNumber) + '[/COLOR] - ' + sName
            sTitle = 'S%s E%s %s' % (sSeason, str(sEpNumber) , sName)

            sExtraTitle = ' S' + "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpNumber)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sMovieTitle + '|' + sExtraTitle) #Pour compatibilite Favoris
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sEpisode', str(sEpNumber))
            oOutputParameterHandler.addParameter('type', 'serie')
            #oOutputParameterHandler.addParameter('searchtext', showTitle(sMovieTitle,  sMovieTitle + '|' + sExtraTitle))
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))

            #oGui.addTVDB('globalSearch', 'showHosters', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "tvshows"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sTmdbId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sMovieTitle)
            oGuiElement.setIcon('series.png')
            oGuiElement.setMeta(2)
            oGuiElement.setMetaAddon('true')
            #oGuiElement.setThumbnail(sThumbnail)
            #oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(2)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)
    #test pr chnagement mode
    #xbmc.executebuiltin('Container.SetViewMode(50)')

    oGui.setEndOfDirectory(view)

def showActors():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    result = grab.getUrl(sUrl, iPage)

    total = len(result)
    dialog = util.createDialog(SITE_NAME)

    if (total > 0):
        for i in result['results']:

            total = len(result['results'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sName, sThumbnail = i['name'], i['profile_path']

            if sThumbnail:
                sThumbnail = POSTER_URL + sThumbnail
            else: sThumbnail = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))

            sName = sName.encode('utf-8')

            oOutputParameterHandler.addParameter('siteUrl', 'person/' + str(i['id']) + '/movie_credits')
            #oGui.addMovieDB(SITE_IDENTIFIER, 'showFilmActor', '[COLOR red]'+str(sName)+'[/COLOR]', '', sThumbnail, '', oOutputParameterHandler)
            sTitle = '[COLOR red]' + str(sName) + '[/COLOR]'

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showFilmActor')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sName)
            oGuiElement.setIcon('actors.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)
            oGuiElement.setCat(7)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)


        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showActors', '[COLOR teal]Page ' + str(iNextPage) + ' >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory(view)

def showFilmActor():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    result = grab.getUrl(sUrl, iPage)

    total = len(result)
    dialog = util.createDialog(SITE_NAME)

    if (total > 0):
        for i in result['cast']:

            total = len(result['cast'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break


            sId, sTitle, sThumbnail, sFanart, sDesc = i['id'], i['title'], i['poster_path'], i['backdrop_path'], i['overview']


            try:
                sTitle = unicodedata.normalize('NFKD', sTitle).encode('ascii','ignore')

            except: sTitle = "Aucune information"

            try:
                sThumbnail = POSTER_URL + sThumbnail
            except:
                sThumbnail = ''

            try:
                sFanart = FANART_URL + sFanart
            except :
                sFanart = ''

            #sTitle = sTitle.encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('type', 'film')
            #oOutputParameterHandler.addParameter('searchtext', showTitle(sTitle,  str('none')))
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            #oGui.addMovieDB('globalSearch', 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('actors.png')
            oGuiElement.setMeta(1)
            oGuiElement.setMetaAddon('true')
            #oGuiElement.setThumbnail(sThumbnail)
            #oGuiElement.setPoster(sThumbnail)
            #oGuiElement.setFanart(sFanart)
            oGuiElement.setCat(1)
            #oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)
         #pas de paramettre de page
        # if (iPage > 0):
            # iNextPage = int(iPage) + 1
            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', sUrl)
            # oOutputParameterHandler.addParameter('page', iNextPage)
            # oGui.addDir(SITE_IDENTIFIER, 'showFilmActor', '[COLOR teal]Page '+str(iNextPage)+' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory(view)


def showLists():
    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')


    result = grab.getUrl('list/'+sUrl, iPage, '')

    oGui = cGui()

    total = len(result)
    dialog = util.createDialog(SITE_NAME)

    if (total > 0):
        for i in result['items']:

            total = len(result['items'])
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sId, sType, sThumbnail, sFanart, sVote, sDesc = i['id'], i['media_type'], i['poster_path'], i['backdrop_path'], i['vote_average'], i['overview']

            if sThumbnail:
                sThumbnail = POSTER_URL + sThumbnail
            else:
                sThumbnail = ''

            if sFanart:
                sFanart = FANART_URL + sFanart
            else : sFanart = ''

            sTitle = "None"

            if 'name' in i:
                sTitle = i['name'].encode("utf-8")
            if 'title' in i:
                sTitle = i['title'].encode("utf-8")

            sDisplayTitle = "%s (%s)" % (sTitle, sVote)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://tmdb/%s' % sId)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sId', str(sId))
            oOutputParameterHandler.addParameter('sFanart', str(sFanart))
            oOutputParameterHandler.addParameter('sTmdbId', sId)
            #oOutputParameterHandler.addParameter('searchtext', sTitle)
            oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

            #oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesSaison', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)

            cGui.CONTENT = "movies"
            oGuiElement = cGuiElement()
            oGuiElement.setTmdbId(sId)
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('showSearch')
            oGuiElement.setTitle(sDisplayTitle)
            oGuiElement.setFileName(sTitle)
            oGuiElement.setIcon('series.png')
            if sType == 'movie':
                oGuiElement.setMeta(1)
                oGuiElement.setCat(1)
            elif sType == 'tv':
                oGuiElement.setMeta(2)
                oGuiElement.setCat(2)
            oGuiElement.setMetaAddon('true')
            #oGuiElement.setThumbnail(sThumbnail)
            #oGuiElement.setPoster(sThumbnail)
            #oGuiElement.setFanart(sFanart)
            oGuiElement.setDescription(sDesc)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        util.finishDialog(dialog)

    oGui.setEndOfDirectory(view)


def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span><a class='page-numbers' href='([^<]+)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showTitle(sMovieTitle, sUrl):

    sExtraTitle = ''
    #si c'est une serie
    if sUrl != 'none':
        sExtraTitle = sUrl.split('|')[1]
        sMovieTitle = sUrl.split('|')[0]

    #nettoyage du nom pr la recherche

    #ancien decodage
    sMovieTitle = unicode(sMovieTitle, 'utf-8')#converti en unicode pour aider aux convertions
    sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sMovieTitle = sMovieTitle.encode("utf-8").lower() #on repasse en utf-8

    sMovieTitle = urllib.quote(sMovieTitle)

    sMovieTitle = re.sub('\(.+?\)',' ', sMovieTitle) #vire les tags entre parentheses

    #modif venom si le titre comporte un - il doit le chercher
    sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle) #vire les caracteres a la con qui peuvent trainer
    #Mais on le vire si entre 2 espaces
    sMovieTitle=sMovieTitle.replace(' - ','')

    #sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)',' ', sMovieTitle) #vire les articles

    sMovieTitle = re.sub(' +',' ',sMovieTitle) #vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +

    #je pense pas que ce soir utile car la fonction de le ligne 595 vire les accent, a tester
    sMovieTitle = sMovieTitle.replace('%C3%A9','e').replace('%C3%A0','a')

    if (False):
        if sExtraTitle:
            sMovieTitle = sMovieTitle + sExtraTitle
        else:
            sMovieTitle = sMovieTitle

    return sMovieTitle
