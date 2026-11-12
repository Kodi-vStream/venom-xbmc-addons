# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.tmdb import cTMDb

SITE_IDENTIFIER = 'vidzy'
SITE_NAME = 'Vidzy'
SITE_DESC = 'Hébergeur direct'

URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')

MOVIE_MOVIE = ('movie', 'showMenuFilms')
SERIE_SERIES = ('tv', 'showMenuTv')
SEARCH_MOVIE = 'movie/%s'
SEARCH_SERIE = 'serie/%s/%d'   #  /serie/{tmdb}/{saison}/{episode}


URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche film', 'search.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', 'tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche film', 'search.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showMenuTv():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showSearch():
    oInputParameterHandler = cInputParameterHandler()
    sCat = oInputParameterHandler.getValue('siteUrl')
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText:
        oGui.setEndOfDirectory()
        return

    oGui = cGui()
    oTMDb = cTMDb()
    results = oTMDb.getUrl('search/' + sCat, term='query=' + sSearchText)

    for item in results.get('results', []):
        item = oTMDb._format(item)
        tmdb_id = item.get('tmdb_id')
        sDisplayTitle = sMovieTitle = item.get('title')
        sThumb = item.get('poster_path')
        sDesc = item.get('overview', '')
        sYear = item.get('year')
        if sYear:
            sDisplayTitle += ' (%s)' % sYear
        
        sUrl = SEARCH_MOVIE % tmdb_id
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sTmdbId', tmdb_id)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        
        if sCat == 'movie':
            oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        else:
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovies(searchId = None):
    oGui = cGui()
    oParser = cParser()

    searchIdTMDB = cInputParameterHandler().getValue('sTmdbId')
    if not searchIdTMDB:
        searchIdTMDB = searchId
    if not searchIdTMDB:
        return

    sUrl = SEARCH_MOVIE % searchIdTMDB
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    data = oRequestHandler.request()
    
    aResult = oParser.parse(data, '<iframe.+?src="([^"]+)')
    if aResult[0]:  # il existe une URL
        aResult = oParser.parse(data, '<title>([^<]+)</title>')
        if aResult[0]:
            sMovieTitle = aResult[1][0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sTmdbId', searchIdTMDB)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sMovieTitle, 'films.png', '', '', oOutputParameterHandler)

    if not searchId:
        oGui.setEndOfDirectory()


def showSeries(searchId = None):
    oGui = cGui()
    oParser = cParser()

    searchIdTMDB = cInputParameterHandler().getValue('sTmdbId')
    if not searchIdTMDB:
        searchIdTMDB = searchId
    if not searchIdTMDB:
        return

    sUrl = '%s%s' % (URL_MAIN, SEARCH_SERIE % (searchIdTMDB, 1))
    oRequestHandler = cRequestHandler(sUrl)
    data = oRequestHandler.request()
    
    aResult = oParser.parse(data, '<iframe.+?src="([^"]+)')
    if aResult[0]:
        siteUrl = aResult[1][0]
    
        aResult = oParser.parse(data, '<title>([^<]+)</title>')
        if aResult[0]:
            sMovieTitle = aResult[1][0].split(' - ')[0]
            sDisplayTitle = sMovieTitle 
        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sTmdbId', searchIdTMDB)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, 'tv.png', '', '', oOutputParameterHandler)

    if not searchId:
        oGui.setEndOfDirectory()


def showSaisons():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    searchIdTMDB = oInputParameterHandler.getValue('sTmdbId')

    oOutputParameterHandler = cOutputParameterHandler()
    for numSaison in range(1, 50):
        sUrl = '%s%s' % (URL_MAIN, SEARCH_SERIE % (searchIdTMDB, numSaison))
        oRequestHandler = cRequestHandler(sUrl + '/1')
        data = oRequestHandler.request()
        aResult = oParser.parse(data, '<iframe.+?src="([^"]+)')
        if not aResult[0]:
            break
        sDisplayTitle = '%s Saison %d ' % (sMovieTitle, numSaison) 
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sTmdbId', searchIdTMDB)
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, 'tv.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(siteUrl)
    data = oRequestHandler.request()
    aResult = oParser.parse(data, '"episodes":([^\]]+])')
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        episodes = eval(aResult[1][0])
        for numEp in episodes:
            sDisplayTitle = '%s Episode %d ' % (sMovieTitle, numEp)
            sUrl = '%s/%d' % (siteUrl, numEp)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHostersSerie', sDisplayTitle, 'tv.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHostersSerie():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    firstLink = None    # si le lien est en double, on garde le premier
    gk = None
    for lang in ('fr', 'vostfr'):
        sUrl = '%s/%s' % (siteUrl, lang)
        oRequestHandler = cRequestHandler(sUrl)
        data = oRequestHandler.request()
        
        aResult = oParser.parse(data, '<iframe.+?src="([^"]+)')
        if not aResult[0]:
            break
        sUrl = aResult[1][0]
        if firstLink and firstLink == sUrl:
            continue
        firstLink = sUrl

        sDisplayTitle = sMovieTitle 
        if lang == 'vostfr':
            sDisplayTitle += ' - [VOSTFR]'

        sHtmlContent = cRequestHandler(sUrl).request()
        if not gk:
            aResult = oParser.parse(sHtmlContent, "fetch\('([^']+)")
            if aResult[0]:
                fetchUrl = aResult[1][0] + 'v=p1&cw=159.56&cw2=170.34&wg=1&ca=e55a64e071fadf14&cl=23946&dpr=1&sw=1680&hw=4&ft=%s&rf=%s' % (URL_MAIN, URL_MAIN)
                data = cRequestHandler(fetchUrl).request(True)
                gk = data.get('gk', None)
        if gk:
            aResult = oParser.parse(sHtmlContent, 'sources: *\[(.+?)\]')
            if aResult[0]:
                aResult = oParser.parse(aResult[1][0], 'src: *"([^"]+)')
                if aResult[0]:
                    sHosterUrl = aResult[1][0]
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sHosterUrl += '&gk=%s' % gk
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        oHosterGui.showHoster(oGui, oHoster, sHosterUrl)
        
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    firstLink = None    # si le lien est en double, on garde le premier
    gk = None
    for lang in ('fr', 'vostfr'):
        sUrl = '%s%s/%s' % (URL_MAIN, siteUrl, lang)
        oRequestHandler = cRequestHandler(sUrl)
        data = oRequestHandler.request()
        aResult = oParser.parse(data, '<iframe.+?src="([^"]+)')
        if not aResult[0]:
            oGui.setEndOfDirectory()
            return
        sUrl = aResult[1][0]
        if firstLink and firstLink == sUrl:
            continue
        firstLink = sUrl
        
        sDisplayTitle = sMovieTitle
        if lang == 'vostfr':
            sDisplayTitle += ' - [VOSTFR]'

        sHtmlContent = cRequestHandler(sUrl).request()
        if not gk:
            aResult = oParser.parse(sHtmlContent, "fetch\('([^']+)")
            if aResult[0]:
                fetchUrl = aResult[1][0] + 'v=p1&cw=159.56&cw2=170.34&wg=1&ca=e55a64e071fadf14&cl=23946&dpr=1&sw=1680&hw=4&ft=%s&rf=%s' % (URL_MAIN, URL_MAIN)
                data = cRequestHandler(fetchUrl).request(True)
                gk = data.get('gk', None)
        if gk:
            aResult = oParser.parse(sHtmlContent, 'sources: *\[(.+?)\]')
            if aResult[0]:
                aResult = oParser.parse(aResult[1][0], 'src: *"([^"]+)')
                if aResult[0]:
                    sHosterUrl = aResult[1][0]
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sHosterUrl += '&gk=%s' % gk
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        oHosterGui.showHoster(oGui, oHoster, sHosterUrl)

    oGui.setEndOfDirectory()
