# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 03 update 10/11/2020


from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress #,VSlog


SITE_IDENTIFIER = 'filmstoon_pro'
SITE_NAME = 'Films toon'
SITE_DESC = 'Films en streaming'

# URL_MAIN = 'https://ww.filmstoon.cam/'
URL_MAIN = 'https://filmstoon.in/'


MOVIE_NEWS = (URL_MAIN + 'movies/#page/1/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_MOVIE = (True, 'load')

SERIE_NEWS = (URL_MAIN + 'series/#page/1/', 'showMovies')
SERIE_NEWS_EPISODE = (URL_MAIN + 'episode/#page/1/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
# variables globales
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')

# variables internes
MY_SEARCH_MOVIES = (True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = (True, 'MyshowSearchSerie')


# on rajoute le tag #page/1/ sur les premieres pages
# pour la fonction nextpage pas de liens next 

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Series', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODE[1], 'Episode (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Series (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films & Series (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_series + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    #https://filmstoon.in/genre/action/

    liste = []
    listegenre = ['action', 'animation', 'aventure', 'comedie', 'crime', 'Documentaire'
                  ,'drame', 'familial', 'fantastique', 'guerre', 'horreur'
                  ,'musique', 'romance', 'thriller', 'science-fiction'
                ]

    url1g = URL_MAIN + 'genre/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre + '/#page/1/'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    # https://www.filmstoon.pw/2020/
    # https://filmstoon.in/release-year/2020/
    for i in reversed(range(1935, 2021)):
        sYear = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'release-year/' + sYear + '/#page/1/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    
    bSearchMovie = False
    bSearchSerie = False
    
    if sSearch:
        sUrl = sSearch.replace(' ', '+').replace('%20', '+')
        if key_search_movies in sUrl:
            sUrl = str(sUrl).replace(key_search_movies, '')
            bSearchMovie = True

        if key_search_series in sUrl:
            sUrl = str(sUrl).replace(key_search_series, '')
            bSearchSerie = True

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #url image alt desc
    sPattern = 'class="ml-item">.+?href="([^"]+).+?img src="([^"]+).+?alt="([^"]+).+?desc.+?p>([^<]*)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDesc = ''
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sDesc = aEntry[3]

            if bSearchMovie:
                if 'series' in sUrl2:
                    continue
            if bSearchSerie:
                if 'series' not in sUrl2:
                    continue

            if sDesc:
                sDesc= ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', sDesc )

            sDislpayTitle = sTitle
            if sSearch or 'genre/' in sUrl or 'release-year/' in sUrl:
                if 'series' in sUrl2:
                    sDislpayTitle = sDislpayTitle + ' [serie]'
                else:
                    sDislpayTitle = sDislpayTitle + ' [film]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2 )
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'series' not in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDislpayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSXE', sDislpayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalid,sUrlNextPage,number = __checkForNextPage(sHtmlContent,sUrl)
        if (bvalid == True):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(shtml,surl):
    # pas de lien next page on crée l'url et on verifie  l'index de la derniere page 
    smax = ''
    imax = 0
    scurrent = ''
    icurrent = 0
    inext = 0
    snext = ''
    surlnext = ''
    sPattern = "page/(\d+)/"
    oParser = cParser()
    aResult = oParser.parse(shtml, sPattern)
    if (aResult[0] == True):
        for aresult in aResult[1]:
            scurrentmax = aresult
            icurentmax = int(scurrentmax)
            if icurentmax > imax:
                imax = icurentmax
                smax = scurrentmax

    sPattern = 'page.(\d+)'
    oParser = cParser()
    aResult = oParser.parse(surl, sPattern)
    if (aResult[0] == True):
        scurrent = aResult[1][0]
        icurrent = int(scurrent)
        inext = icurrent + 1 
        snext = str (inext)
        pcurrent ='page/' + scurrent
        pnext = 'page/' + snext
        surlnext = surl.replace(pcurrent, pnext)

    else:
        return False, False, False

    if imax != 0 and imax >= inext:
        return True, surlnext , snext + '/' + smax

    elif inext == 0 : # c'est un bug de programmation
        return False, False, False

    return False, False, False


def showSXE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<strong>Season.+?(\d+)|a>\s*<a href="([^"]+).+?Episode.+?(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            saison=''
            if aEntry[0]:
                sSaison = ' Saison ' + aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]' + sSaison + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                Ep = aEntry[2]
                sDisplayTitle = sMovieTitle + sSaison + ' Episode' + Ep

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)

                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle , '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # 1 seul host constaté 10112020 : uqload

    sHosterUrl = ''
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = 'data-lazy-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if 'embedo' in aResult[1][0]:

            # url1 https://embedo.to/e/QW9RSEhEeEZFUTJXVXo0dzBhdzhVZz09
            # url2 https://embedo.to/s/cTJtdlNDY2J5aGM9
            # url3 https://embedo.to/r/cTJtdlNDY2J5aGM9

            url1 = aResult[1][0]
            oRequestHandler = cRequestHandler(url1)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'iframe src="([^"]+)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):

                url2 = 'https://embedo.to' + aResult[1][0]
                url3 = url2.replace('/s/', '/r/')

                oRequestHandler = cRequestHandler(url3)
                oRequestHandler.addHeaderEntry('Referer', url2)
                oRequestHandler.request()
                getreal=oRequestHandler.getRealUrl()

                if 'http' in getreal:
                    sHosterUrl = getreal
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sDisplayTitle = sMovieTitle
                    if (oHoster != False):
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
