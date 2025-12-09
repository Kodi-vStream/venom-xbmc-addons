# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'cpasmal'
SITE_NAME = 'CPasMal'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('films-streaming/', 'showMenuMovies')
MOVIE_NEWS = ('films-streaming/', 'showMovies')
MOVIE_GENRES = (MOVIE_MOVIE[0] , 'showMovieGenres')

SERIE_SERIES = ('series-streaming/', 'showMenuTvShows')
SERIE_NEWS = ('series-streaming/', 'showMovies')
SERIE_GENRES = (SERIE_SERIES[0] , 'showSerieGenres')

URL_SEARCH = (False, 'showMovies')
URL_SEARCH_MOVIES = ('index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s&cat=Film', 'showMovies')
URL_SEARCH_SERIES = ('index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s&cat=Serie', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl %= sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'],
             ['Comédie', 'comedie'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Espionnage', 'espionnage'], ['Familial', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Histoire', 'historique'], ['Horreur', 'epouvante-horreur'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0] + '/genre/' + sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'action_s'], ['Animation', 'animation_s'], ['Aventure', 'aventure_s'],
             ['Comédie', 'comedie_s'], ['Documentaire', 'documentaire-s'], ['Drame', 'drame_s'],
             ['Familial', 'famille-s'], ['Fantastique', 'fantastique_s'], ['Guerre', 'guerre_s'], ['Judiciaire', 'judiciare-s'], 
             ['Historique', 'historique_s'], ['Horreur', 'horreur_s'], ['Musical', 'musical_s'],
             ['Policier', 'policier_s'], ['Romance', 'romance_s'], ['Science-Fiction', 'science_fiction_s'],
             ['Thriller', 'thriller_s'], ['Western', 'western_s']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0] + '/genre/' + sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()
    bShow = False
    if sSearch:
        sUrl, catSearch = sSearch.split('&cat=')
        a, sSearchText = sUrl.split('&story=')
        sUrl = sUrl.replace(' ', '%20')
        bShow = catSearch == 'Serie'
        # url img title cat
        sPattern = 'th-img img-resp-v" href="([^"]+).+?<img src="([^"]+).+?alt="([^"]+)" \/> <span class="th-([^"]+)'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        bShow = SERIE_SERIES[0] in sUrl
        # url img title
        sPattern = 'th-img img-resp-v" href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+)" \/> '

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    # en cas de recherche vide, deuxieme tentative avec le mot le plus long
    if sSearch and not aResult[0]:
        if ' ' in sSearch:
            termes = sSearch.split(' ')
            termes = sorted(termes, key=lambda terme: len(terme))[::-1]
            sUrl = URL_MAIN + URL_SEARCH[0] + termes[0]
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        titles = set()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            # tri des doublons
            cleanTitle = oUtil.CleanName(sTitle).replace(' ', '')
            if cleanTitle in titles:
                continue
            titles.add(cleanTitle)

            # non fonctionnel
            if 'F1 2024' in sTitle or 'F1 2025' in sTitle:
                continue

            # filtre search
            if sSearch:
                sCat = aEntry[3]
                if sCat != catSearch:
                    continue
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

            if not 'http' in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            
            if bShow:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="navigation".+?href="([^"]+)">suiv'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        return sNextPage, sNumberNext

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = ''
    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, 'class="seasons"', 'smart-text-s')

    # url  /  thumb  /  title
    sPattern = 'href="([^"]+)"><div class="thumb"><div class="th-in th-seas.+?data-src="([^"]+)".+?th-count">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            if not 'http' in sThumb:
                sThumb = URL_MAIN + sThumb
            sTitle = sMovieTitle + " " +aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showMovieLinks()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, 'class="seasons"', 'class="seasons"')

    # url numEp
    sPattern = 'href="([^"]+)"> <div class="fsa-ep">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = "%s %s" % (sMovieTitle, aEntry[1])
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showMovieLinks()    # liens films ?


def showMovieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    oParser = cParser()
    sPattern = 'fx-row" onclick="getxfield\(\'(\d+)\', \'(.+?)\', \'(.+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        oHosterGui = cHosterGui()
        for aEntry in aResult[1]:
            videoId = aEntry[0]
            xfield = aEntry[1]
            token = aEntry[2]
            hosterName = sLang = sDesc = ''
            if ('_') in xfield:
                hosterName, sLang = xfield.strip().split('_')
                sLang = sLang.upper()

            oHoster = oHosterGui.checkHoster(hosterName)
            if not oHoster:
                continue
            
            sUrl2 = URL_MAIN + 'engine/ajax/getxfield.php?'
            postData = 'id=%s&xfield=%s&token=%s' % (videoId, xfield, token)
            sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, hosterName.capitalize())
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('cook', cook)
            oOutputParameterHandler.addParameter('postdata', postData)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def showSerieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    oParser = cParser()
    sPattern = 'fx-row" onclick="playEpisode\(this, \'(\d+)\', \'(.+?)\'\)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        oHosterGui = cHosterGui()
        for aEntry in aResult[1]:
            videoId = aEntry[0]
            xfield = aEntry[1]
            hosterName = sLang = sDesc = ''
            if ('_') in xfield:
                hosterName, sLang = xfield.strip().split('_')
                sLang = sLang.upper()

            oHoster = oHosterGui.checkHoster(hosterName)
            if not oHoster:
                continue
            
            
            postData = 'id=' + videoId + '&xfield=' + xfield + '&action=playEpisode'
            sUrl2 = URL_MAIN + 'engine/inc/serial/app/ajax/Season.php'
            
            # sUrl2 = URL_MAIN + 'engine/ajax/getxfield.php?'
            # postData = 'id=%s&xfield=%s' % (videoId, xfield)
            sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, hosterName.capitalize())
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('cook', cook)
            oOutputParameterHandler.addParameter('postdata', postData)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)
            
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    cook = oInputParameterHandler.getValue('cook')
    postdata = oInputParameterHandler.getValue('postdata')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addHeaderEntry('Cookie', cook)
    oRequest.addParametersLine(postdata)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = '<iframe src=\"([^\"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
