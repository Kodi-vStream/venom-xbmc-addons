# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib import util
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import siteManager, VSlog, addon

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

# On garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'

URL_MAIN = 'URL_MAIN'
URL_HOST = siteManager().getUrlMain(SITE_IDENTIFIER)
PATH_SITE = 'c/%s/' % util.urlHostName(URL_HOST).split('.')[0]

# pour l'addon
MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_VIEWS = (URL_MAIN + PATH_SITE + '29/0', 'showMovies')
MOVIE_LAST = (URL_MAIN, 'showMovies')
MOVIE_LAST_ID = 'Movies Last'
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_NEWS_ID = 'Movies News'
MOVIE_GENRES = (True, 'showGenres')

DOC_DOCS = (True, 'showMenuDivers')
DOC_NEWS = (URL_MAIN + PATH_SITE + '26/0', 'showMovies')
SHOW_SHOWS = (URL_MAIN + PATH_SITE + '3/0', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_MISC = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LAST[0])
    oOutputParameterHandler.addParameter('sMovieTitle', MOVIE_LAST_ID)
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LAST[1], addons.VSlang(30101), 'boxoffice.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oOutputParameterHandler.addParameter('sMovieTitle', MOVIE_NEWS_ID)
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], addons.VSlang(30112), 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SHOW_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, SHOW_SHOWS[1], addons.VSlang(30136), 'spectacle.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LAST[0])
    oOutputParameterHandler.addParameter('sMovieTitle', MOVIE_LAST_ID)
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LAST[1], addons.VSlang(30101), 'boxoffice.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oOutputParameterHandler.addParameter('sMovieTitle', MOVIE_NEWS_ID)
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    

def showMenuDivers():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SHOW_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, SHOW_SHOWS[1], 'Spectacles', 'spectacle.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', 1])
    liste.append(['Animation', 2])
    liste.append(['Aventure', 4])
    # liste.append(['Biographie', 5])  # aucun
    liste.append(['Comédie', 6])
    liste.append(['Documentaire', 26])
    liste.append(['Drame', 7])
    liste.append(['Epouvante et Horreur', 9])
    liste.append(['Fantastique', 8])
    liste.append(['Policier', 10])
    liste.append(['Science Fiction', 11])
    liste.append(['Spectacle', 3])
    liste.append(['Thriller', 12])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, iGenre in liste:
        sUrl = URL_MAIN + PATH_SITE + '%d/0' % iGenre
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    # L'url change tres souvent donc faut la retrouver
    oRequestHandler = cRequestHandler(URL_HOST)
    data = oRequestHandler.request()
    aResult = oParser.parse(data, '<a.+?href="(/*[0-9a-zA-Z]+)"')  # Compatible avec plusieurs clones
    if not aResult[0]:
        return   # Si ca ne marche pas, pas la peine de continuer

    # memorisation pour la suite
    sMainUrl = URL_HOST + aResult[1][0] + '/'
    # correction de l'url

    # En cas de recherche direct OU lors de la navigation dans les differentes pages de résultats d'une recherche
    if sSearch:
        oUtil = cUtil()
        sSearch = sSearchText = oUtil.CleanName(sSearch)
        sSearch = sSearch[:20]  # limite de caractere sinon bug de la recherche
        sSearch = sSearch.replace(' ', '%') # recherche multi-mots

        siteName = sMainUrl.split('/')[2].split('.')[0]
        sUrl = sMainUrl + 'home/{0!s}'.format(siteName)
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('searchword', sSearch)
        oRequestHandler.addParameters('Referer', sUrl)
        oRequestHandler.addHeaderEntry('Cookie', 'g=true')
        sABPattern = '<div class="column24"'
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if sUrl == URL_MAIN:  # page d'accueil
            sABPattern = '<div class="column1"'
        else:
            sABPattern = '<div class="column20"'

        sUrl = sUrl.replace(URL_MAIN, sMainUrl)
        oRequestHandler = cRequestHandler(sUrl)

    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, sABPattern, '<div class="column2"')
    hasPages = True
    if sTitle == MOVIE_LAST_ID:
        hasPages = False
        sPattern = '-card" href="([^"]+)".+?-card-img" src="([^"]+)" alt="([^"]+)".+?film-card-new-badge">.+?"trend-card-date">([^<>]+)<'
    elif sTitle == MOVIE_NEWS_ID:
        hasPages = False
        sPattern = '<a class="trend-card" href="([^"]+)">.+?<img class="trend-card-img" src="([^"]+)" alt="([^"]+)".+?class="trend-card-overlay"></div>        <div class="trend-card-info">.+?trend-card-date">([^<>]+)<'
    else:
        sPattern = '<a class="film-card" href="([^"]+)">\s*<img class="film-card-img" src="([^"]+)" alt="([^"]+)".+?"trend-card-date">([^<>]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        titles = [] # permet de filtrer les doublons
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[2]
            if sTitle in titles:
                continue
            titles.append(sTitle)
            sUrl2 = URL_HOST[:-1] + aEntry[0]
            sYear = aEntry[3]
            sThumb = aEntry[1]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        if hasPages:
            sNextPage = sUrl.split('/')[-1]
            sNextPage = str(int(sNextPage) + 1)
            if sNextPage:
                sUrlPage = '/'.join(sUrl.split('/')[:-1]) + '/' + sNextPage
    
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrlPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Suivant', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showHosters():
    from urllib.parse import urlparse
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    # sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    # sYear = oInputParameterHandler.getValue('sYear')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sHtmlContent = sHtmlContent.replace('<br/>', '')  # traitement de sDesc

    # Recuperation info film, commentaires
    sDesc = ''
    sPattern = 'id="film-synopsis-text">([^<>]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sDesc = aResult[1][0]

    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        sLink = aResult[1][0]

        if sLink.startswith('/'):
            sLink = URL_HOST[:-1] + sLink

        oRequestHandler = cRequestHandler(sLink)
        data = oRequestHandler.request()

        sPattern = 'document\.location\.href="([^"]+)'
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:
            sLink = aResult[1][0]
            if sLink.startswith('/'):
                sLink = URL_HOST[:-1] + sLink
            oRequestHandler = cRequestHandler(sLink)
            data = oRequestHandler.request()
    
        sPattern = 'file: *"(.+?)"'
        aResult = oParser.parse(data, sPattern)

        if aResult[0]:
            for sLink2 in aResult[1]:
                oHoster = cHosterGui().checkHoster(sLink2)
                sLink2 += '|Referer=' + urlparse(sLink2).netloc
                
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sLink2, sThumb)

    oGui.setEndOfDirectory()