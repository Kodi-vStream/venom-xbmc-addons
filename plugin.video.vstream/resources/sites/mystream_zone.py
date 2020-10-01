# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 08 update 25/08/2020
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
import re
import string
import json

TimeOut = 10  # requetes avec time out utilisées seulement dans show movies : on attends plus 30s
SITE_IDENTIFIER = 'mystream_zone'
SITE_NAME = 'My Stream'
SITE_DESC = 'Films et Series en Streaming'

URL_MAIN = 'https://mystream.zone/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
imdmovies = '#movies'  # tag request
imdseries = '#series'

# variables globales
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'movies/', 'showMovies')
# serie&movie a revoir
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

MOVIE_NOTES = (URL_MAIN + 'imdb/' + imdmovies, 'showMovies')
SERIE_NOTES = (URL_MAIN + 'imdb/' + imdseries, 'showMovies')
MOVIE_ALPHA = (True, 'showAlphaMovies')
SERIE_ALPHA = (True, 'showAlphaSeries')
#
# variables internes
MY_SEARCH_MOVIES = (True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = (True, 'MyshowSearchSerie')

MOVIE_TENDANCE = (URL_MAIN + 'tendance/', 'showMovies')
MOVIE_MOVIES = (URL_MAIN + 'movies/', 'showMovies')  # = globale MOVIE_NEWS
MOVIE_FEATURED = (URL_MAIN, 'showMovies')
MOVIE_TOP_IMD = (URL_MAIN + 'imdb/' + imdmovies, 'showMovies')  # = globale MOVIE_NOTES

SERIE_SERIES = (URL_MAIN+'tvshows/', 'showMovies')  # = SERIE_NEWS
SERIE_TOP_IMD = (URL_MAIN + 'imdb/' + imdseries, 'showMovies')
SERIE_NEWS_SAISONS = (URL_MAIN + 'seasons/', 'showMovies')
SERIE_NEWS_EPISODES = (URL_MAIN + 'episodes/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Series', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Series (Par Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TENDANCE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TENDANCE[1], 'Films & Series (Populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films & Series (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIES[1], ' Films (Récents)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FEATURED[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FEATURED[1], 'Films (En vedette)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP_IMD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP_IMD[1], 'Films (Top IMDd)', 'tmdb.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ALPHA[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series (Récentes)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_SAISONS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_SAISONS[1], 'Séries (Saisons récentes)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODES[1], 'Séries (Episodes récents)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TOP_IMD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TOP_IMD[1], 'Series (Top IMDd)', 'tmdb.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ALPHA[1], 'Séries (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_series + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_movies + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    # https://mystream.zone/genre/action/    /genre//
    liste = []
    liste.append(['Action', URL_MAIN + 'genre/action/'])
    liste.append(['Action & Adventure', URL_MAIN + 'genre/action-adventure/'])
    liste.append(['Adventure', URL_MAIN + 'genre/adventure/'])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/'])
    liste.append(['Animation', URL_MAIN + 'genre/animation/'])
    liste.append(['Aventure', URL_MAIN + 'genre/aventure/'])
    liste.append(['Comedie', URL_MAIN + 'genre/comedie/'])
    liste.append(['Comedy', URL_MAIN + 'genre/comedie/'])
    liste.append(['Crime', URL_MAIN + 'genre/crime/'])
    liste.append(['Documentaire', URL_MAIN + 'genre/documentaire/'])
    liste.append(['Documentary', URL_MAIN + 'genre/documentary/'])
    liste.append(['Drama', URL_MAIN + 'genre/drama/'])
    liste.append(['Drame', URL_MAIN + 'genre/drame/'])
    liste.append(['Familial', URL_MAIN + 'genre/familial/'])
    liste.append(['Family', URL_MAIN + 'genre/family/'])
    liste.append(['Fantastique', URL_MAIN + 'genre/fantastique/'])
    liste.append(['Fantasy', URL_MAIN + 'genre/fantasy/'])
    liste.append(['Guerre', URL_MAIN + 'genre/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'genre/histoire/'])
    liste.append(['History', URL_MAIN + 'genre/history/'])
    liste.append(['Horreur', URL_MAIN + 'genre/horreur/'])
    liste.append(['Horror', URL_MAIN + 'genre/horror/'])
    liste.append(['Kids', URL_MAIN + 'genre/kids/'])
    liste.append(['Music', URL_MAIN + 'genre/music/'])
    liste.append(['Musique', URL_MAIN + 'genre/musique/'])
    liste.append(['Mystère', URL_MAIN + 'genre/mystere/'])
    liste.append(['Mystery', URL_MAIN + 'genre/mystery/'])
    liste.append(['Reality', URL_MAIN + 'genre/reality/'])
    liste.append(['Romance', URL_MAIN + 'genre/romance/'])
    liste.append(['Sci-Fi & Fantasy', URL_MAIN + 'genre/sci-fi-fantasy/'])
    liste.append(['Sci-Fi', URL_MAIN + 'genre/science-fiction/'])
    liste.append(['Sci-Fi & Fantastique', URL_MAIN + 'genre/science-fiction-fantastique/'])
    liste.append(['Soap', URL_MAIN + 'genre/soap/'])
    liste.append(['Talk', URL_MAIN + 'genre/talk/'])
    liste.append(['Telefilm', URL_MAIN + 'genre/telefilm/'])
    liste.append(['Thriller', URL_MAIN + 'genre/thriller/'])
    liste.append(['Tv Movie', URL_MAIN + 'genre/tv-movie/'])
    liste.append(['Guerre', URL_MAIN + 'genre/war/'])
    liste.append(['Guerre & politique', URL_MAIN + 'genre/war-politics/'])
    liste.append(['Western', URL_MAIN + 'genre/western/'])

    for sTitle, sUrlgenre in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrlgenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showAlphaMovies():
    showAlpha('movies')


def showAlphaSeries():
    showAlpha('tvshows')


def showAlpha(stype):
    oGui = cGui()
    # requete json 20 resultat max
    # https://mystream.zone/wp-json/dooplay/glossary/?term=g&nonce=2132c17353&type=tvshows
    url1 = 'https://mystream.zone/wp-json/dooplay/glossary/?term='
    url2 = '&nonce='
    snonce = '2132c17353'  # a surveiller si jamais cela change
    url3 = '&type='

    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = []
    for alpha in listalpha:
        liste.append([str(alpha).upper(), url1 + str(alpha) + url2 + snonce + url3 + stype])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    # https://mystream.zone/release/2020
    for i in reversed(range(1982, 2021)):
        sYear = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'release/' + sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMenu = ''  # bricolage à revoir pour imdb image lows res

    bSearchMovie = False
    bSearchSerie = False

    if sSearch:
        sUrl = sSearch.replace(' ', '%20')
        if key_search_movies in sUrl:
            sUrl = str(sUrl).replace(key_search_movies, '')
            # ifVSlog('Globale Search movies:' + sUrl)
            bSearchMovie = True

        if key_search_series in sUrl:
            sUrl = str(sUrl).replace(key_search_series, '')
            # ifVSlog('Globale Search serie:' + sUrl)
            bSearchSerie = True

    if 'wp-json' in sUrl and not sSearch:
        try:
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setTimeout(TimeOut)
            sJsonContent = oRequestHandler.request()
        except Exception as e:
            if str(e) == "('The read operation timed out',)":
                oGui.addText(SITE_IDENTIFIER, 'site Inaccessible')
                oGui.setEndOfDirectory()
                return
            else:
                oGui.addText(SITE_IDENTIFIER, 'Request Failed')
                oGui.setEndOfDirectory()
                return

        jsonrsp = json.loads(sJsonContent)
        for i, idict in jsonrsp.items():
            sTitle = str(jsonrsp[i]['title'].encode('utf-8', 'ignore'))  # I Know This Much Is True mystream
            sUrl2 = str(jsonrsp[i]['url'])
            sThumb = str(jsonrsp[i]['img'])
            sYears = str(jsonrsp[i]['year'])
            sDisplayTitle = sTitle + ' (' + sYears + ')'
            sDesc = ''
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYears', sYears)

            if 'type=tvshows' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        # 1 result with <= 20 items
        oGui.setEndOfDirectory()
        return

    if 'https://mystream.zone/tendance/' in sUrl:  # url name years image
        # sPattern = 'class="mepo">.+?class=.data.+?href="([^"]*)".+?([^<]*).+?span>.+?,.([^<]*).+?src="([^"]*)'
        sPattern = 'img src="([^"]*).*?class="mepo">.+?class=.data.+?href="([^"]*)".+?([^<]*).+?span>.+?,.([^<]*)'

    elif sUrl == 'https://mystream.zone/':  # url image title
        sPattern = 'data dfeatur.+?href="([^"]*)".+?src="([^"]*).+?alt="([^"]*)'

    elif 'https://mystream.zone/seasons/' in sUrl:  # image url number title
        sPattern = 'item se seasons.+?src="([^"]*)".+?href="([^"]*).+?class="b">([^<]*).+?c">([^<]*)'

    elif 'https://mystream.zone/episodes/' in sUrl:  # url 'S1.E1.'  years '.2020'   title img
        sPattern = 'div class="season_m.+?data.+?href="([^"]*)"..+?span>([^\/]*).+?,([^<]*).+?serie">([^<]*).+?src="([^"]*)"'

    elif 'https://mystream.zone/?s=' in sUrl:  # thumb url title years desc
        sPattern = 'animation-2.+?img src="([^"]*).+?class="title.+?ref="([^"]*)".([^<]*).+?year">([^<]*).*?contenido.><p>([^<]*)'

    # elif 'genre' in sUrl or 'tvshows' in sUrl or 'movies' in sUrl or 'release' in sUrl:
    elif 'genre' in sUrl or 'release' in sUrl:
        sPattern = 'class="item.+?src="([^"]*).+?class="mepo">.+?class="data".+?href="([^"]*).>([^<]*).+?span>.+?,.([^<]*).+?texto">([^<]*)'
    elif 'mystream.zone/tvshows' in sUrl or 'mystream.zone/movies' in sUrl:
        sPattern = '<h1>.+?</html>'

    elif 'mystream.zone/imdb/' in sUrl:  # url thumb title rate
        sPattern = "class=.poster.+?ref=.([^']*).><img src=.([^']*).+?alt=.([^']*).+?class='rating'>([^<]*)"
        sMenu = 'imdb'

    else:
        oGui.addText(SITE_IDENTIFIER, 'Requete inconnue')
        oGui.setEndOfDirectory()
        return

    try:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setTimeout(TimeOut)
        sHtmlContent = oRequestHandler.request()

    # à eviter : prendre toutes les exceptions
    # mais pas catché l'erreur avec UrlError HttpError socket...peu etre i/o operation ?
    except Exception as e:
        if str(e) == "('The read operation timed out',)":
            oGui.addText(SITE_IDENTIFIER, 'site Inaccessible')
            oGui.setEndOfDirectory()
            return
        else:
            oGui.addText(SITE_IDENTIFIER, 'Request Failed')
            oGui.setEndOfDirectory()
            return

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_1 = progress().VScreate(SITE_NAME)
        bclosedprogress_1 = False
        sDesc = ''
        sYear = ''
        
        for aEntry in aResult[1]:
            progress_1.VSupdate(progress_1, total)
            if progress_1.iscanceled():
                break
            
            if 'https://mystream.zone/tendance/' in sUrl:  # image url title years
                sUrl2 = aEntry[1]
                sTitle = aEntry[2]
                sThumb = aEntry[0]
                sDisplayTitle = sTitle + '(' + aEntry[3] + ')'

            elif sUrl == 'https://mystream.zone/':  # url image title
                sUrl2 = aEntry[0]
                sTitle = str(aEntry[2]).replace(' mystream', '')
                sThumb = aEntry[1]
                sDisplayTitle = sTitle

            elif 'https://mystream.zone/seasons/' in sUrl:  # image  url number title
                sUrl2 = aEntry[1]
                sTitle = aEntry[3]
                sThumb = aEntry[0]
                sDisplayTitle = sTitle + ' Saison ' + aEntry[2]

            elif 'https://mystream.zone/episodes/' in sUrl:  # url ;'S1.E1.' ; years '.2020' ;  title; img
                sUrl2 = aEntry[0]
                sTitle = aEntry[3] + ' ' + aEntry[1]
                sThumb = aEntry[4]
                sDisplayTitle = sTitle + '(' + aEntry[2] + ')'
                sYear = aEntry[2]

            elif 'https://mystream.zone/?s=' in sUrl:  # img url title years desc
                sUrl2 = aEntry[1]
                sTitle = str(aEntry[2]).replace(' mystream', '')
                sThumb = aEntry[0]
                sDesc = aEntry[4]
                sYear = aEntry[3]
                sDisplayTitle = sTitle + ' (' + sYear + ' )'

            elif 'genre' in sUrl or 'release' in sUrl:
                sUrl2 = aEntry[1]
                sTitle = str(aEntry[2]).replace(' mystream', '')
                sThumb = aEntry[0]
                sDesc = aEntry[4]
                sYear = aEntry[3]
                sDisplayTitle = sTitle + ' (' + sYear + ')'

            # a revoir
            elif 'mystream.zone/imdb/' in sUrl:  # url thumb title rate
                if 'movies' in str(aEntry[0]) and 'mystream.zone/imdb/' + imdmovies in sUrl:
                    sUrl2 = aEntry[0]
                    sTitle = str(aEntry[2]).replace(' mystream', '')
                    sThumb = aEntry[1]
                    sDisplayTitle = sTitle + ' [ Imdb ' + str(aEntry[3]) + ' ]'
                elif 'tvshows' in str(aEntry[0]) and 'mystream.zone/imdb/' + imdseries in sUrl:
                    sUrl2 = aEntry[0]
                    sTitle = str(aEntry[2]).replace(' mystream', '')
                    sThumb = aEntry[1]
                    sDisplayTitle = sTitle + ' [ Imdb ' + str(aEntry[3]) + ' ]'
                else:
                    continue

            elif 'tvshows' in sUrl or 'movies':
                progress_1.VSclose(progress_1)
                bclosedprogress_1 = True
                # revoir pattern si simplification avec 'genre' or 'release' (pb image decalage)
                sPattern1 = 'class="item.+?src="([^"]*).+?class="mepo">.+?class="data".+?href="([^"]*).>([^<]*).+?span>.+?,.([^<]*).+?texto">([^<]*)'
                shtml = str(aEntry)
                oParser2 = cParser()
                aResult2 = oParser2.parse(shtml, sPattern1)
                if (aResult2[0] == False):
                    oGui.addText(SITE_IDENTIFIER)
                if (aResult2[0] == True):
                    total = len(aResult2[1])
                    progress_2 = progress().VScreate(SITE_NAME)
                    
                    for aEntry in aResult2[1]:
                        progress_2.VSupdate(progress_2, total)
                        if progress_2.iscanceled():
                            break
                        
                        sUrl2 = aEntry[1]
                        sTitle = str(aEntry[2]).replace(' mystream', '')
                        sThumb = aEntry[0]
                        sDesc = aEntry[4]
                        sYear = aEntry[3]
                        sDisplayTitle = sTitle + ' (' + sYear + ')'
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('sDesc', sDesc)
                        oOutputParameterHandler.addParameter('sYear', sYear)
                        oOutputParameterHandler.addParameter('sMenu', sMenu)
                        if 'mystream.zone/tvshows' in sUrl2:
                            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                        else:
                            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
                    progress_2.VSclose(progress_2)

            else:  # en théorie jamais atteint : a revoir
                sUrl2 = aEntry[1]
                sTitle = str(aEntry[2]).replace(' mystream', '')
                sThumb = aEntry[0]
                sDesc = aEntry[4]
                sYear = aEntry[3]
                sDisplayTitle = sTitle + ' (' + sYear + ')'
            # inutile mais capte genere erreur si url2 = '': a revoir
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN + sUrl2
            if sThumb.startswith('/'):
                sThumb = URL_MAIN + sThumb

            if sSearch or '/release/' in sUrl or '/genre/' in sUrl or '/tendance/' in sUrl:
                # ifVSlog('Try ADD tag Film or serie ')
                if 'movies' in sUrl2:
                    sDisplayTitle = sTitle + ' (Film)'
                if 'tvshows' in sUrl2:
                    sDisplayTitle = sTitle + ' (Serie)'

            if bSearchMovie:
                if 'tvshows' in sUrl2:
                    continue
                else:
                    sDisplayTitle = sTitle
            if bSearchSerie:
                if 'movies' in sUrl2:
                    continue
                else:
                    sDisplayTitle = sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sMenu', sMenu)

            if 'mystream.zone/tvshows' in sUrl2:  # inutile mais ne pas enlever resoudre regex
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

            elif 'mystream.zone/seasons' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        if not bclosedprogress_1:
            progress_1.VSclose(progress_1)
                   
        if not sSearch:
            bNextPage, urlNextpage, pagination = __checkForNextPage(sHtmlContent)
            if (bNextPage):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', urlNextpage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] ' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    bnext = False
    urlNextpage = 'no find'
    # note pas de class=.arrow dans la recherche
    # return false
    sPattern = 'class=.arrow.+?ref="([^"]*)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        urlNextpage = str(aResult[1][0])
        bnext = True
    try:
        numberNext = re.search('page/([0-9]+)', urlNextpage).group(1)
    except:
        numberNext = ''
        pass

    sPattern = 'class="pagination"><span>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        pagination = aResult[1][0]
    try:
        NumberMax = re.search('([0-9]+)$', pagination).group(1)
    except:
        NumberMax = ''
        pass

    if bnext:
        pagination = ''
        if numberNext:
            pagination = 'Page ' + numberNext
        if NumberMax:
            pagination = pagination + '/' + NumberMax + ' '
        return True, urlNextpage, pagination
    else:
        return False, urlNextpage, 'nothing'


def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')

    sMenu = oInputParameterHandler.getValue('sMenu')
    # probleme temps de la requete aleatoire normale, lent, ou tps de connexion > max autorisé
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # temps qui peu depasser 10 secondes parfois

    # on  passe ts les liens  des épisodes dans chaque dossier saisons créés ds un liste
    # car pas de liens existants ds la page pour acceder aux pages de chaque saison
    if not sDesc:
        try:
            sPattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            pass

    if sMenu == 'imdb':  # on remplace l'image de faible resolution
        try:
            sPattern = '<div class="poster">.<img src="([^"]*)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sThumb = aResult[1][0]
        except:
            pass
    # '2 - 11'   href   title
    # class='numerando'>([^<]*).+?href='([^']*).>([^<]*) #
    sPattern = "class='numerando'>([^<]*).+?href='([^']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        ListNumeroSaison = []
        listeUrlEpisode = []
        listeStitle = []
        icurrentsaison = 0
        for aEntry in aResult[1]:
            # ifVSlog(aEntry[0])  # debug si pb episode
            iSaison = re.search('([0-9]+)', aEntry[0]).group(1)
            iEpisode = re.search('([0-9]+)$', aEntry[0]).group(1)
            if not str(iSaison) in ListNumeroSaison:
                ListNumeroSaison.append(str(iSaison))
                sDisplayTitle = sTitle + ' ' + 'Saison' + ' ' + str(icurrentsaison)
                if sYear:
                    sDisplayTitle = sDisplayTitle + ' (' + sYear + ')'

                if len(listeUrlEpisode) > 0:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
                    oOutputParameterHandler.addParameter('sYear', sYear)
                    oOutputParameterHandler.addParameter('listeUrlEpisode', listeUrlEpisode)
                    oOutputParameterHandler.addParameter('listeStitle', listeStitle)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showListEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                    listeUrlEpisode = []
                    listeStitle = []
                icurrentsaison = iSaison

            listeUrlEpisode.append(str(aEntry[1]))
            sTitleEp = sTitle + ' ' + ' Saison ' + str(iSaison) + ' Episode ' + str(iEpisode)
            listeStitle.append(sTitleEp)
            sDisplayTitle = sTitle + ' ' + 'Saison' + ' ' + str(iSaison)
            if sYear:
                sDisplayTitle = sDisplayTitle + ' (' + sYear + ')'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('listeUrlEpisode', listeUrlEpisode)
        oOutputParameterHandler.addParameter('listeStitle', listeStitle)
        oGui.addEpisode(SITE_IDENTIFIER, 'showListEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showListEpisodes():
    # parent https://mystream.zone/tvshows
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')
    listeUrlEpisode = oInputParameterHandler.getValue('listeUrlEpisode')
    listeStitle = oInputParameterHandler.getValue('listeStitle')

    listeUrlEpisode2 = []
    listeStitle2 = []
    sPattern = "'([^']*)'"
    oParser = cParser()

    aResult = oParser.parse(listeUrlEpisode, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            listeUrlEpisode2.append(aEntry)

    aResult = oParser.parse(listeStitle, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            listeStitle2.append(aEntry)
    i = 0
    for itemurl in listeUrlEpisode2:
        sTitle = listeStitle2[i]
        i = i + 1
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', itemurl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    # parents https://mystream.zone/saisons/    # SERIE_NEWS_SAISONS
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if not sDesc:
        try:
            sPattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            pass
    # thumb '2 - 11'   url
    sPattern = "class='imagen'.+?src='([^']*).*?class='numerando'>([^<]*).+?href='([^']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            iSaison = re.search('([0-9]+)', aEntry[1]).group(1)
            iEpisode = re.search('([0-9]+)$', aEntry[1]).group(1)
            sUrl = aEntry[2]
            sDisplayTitle = sMovieTitle + ' ' + ' Saison ' + str(iSaison) + ' Episode ' + str(iEpisode)
            if sYear:
                sDisplayTitle = sDisplayTitle + ' (' + sYear + ')'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')
    sMenu = oInputParameterHandler.getValue('sMenu')
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # if False: no desc MOVIE_TENDANCE
    if not sDesc:
        try:
            sPattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            # ifVSlog('Try exception ')
            pass

    try:  # a revoir
        if sMenu:
            if sMenu == 'imdb':  # on remplace l'image de faible resolution
                sPattern = '<div class="poster">.<img src="([^"]*)'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    sThumb = aResult[1][0]
    except:
        pass
    sPattern = "data-type='([^']*).*?post='([^']*).*?nume='([^']*).*?title'>([^<]*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            datatype = aEntry[0]
            datapost = aEntry[1]
            datanum = aEntry[2]
            sUrl2 = 'https://mystream.zone/wp-admin/admin-ajax.php'
            pdata = 'action=doo_player_ajax&post=' + datapost + '&nume=' + datanum + '&type=' + datatype
            if sYear:
                sDisplayTitle = sTitle + ' (' + sYear + ')'
            else:
                sDisplayTitle = sTitle
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('pdata', pdata)
            oGui.addLink(SITE_IDENTIFIER, 'Hosterslink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def Hosterslink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    referer = oInputParameterHandler.getValue('referer')
    pdata = oInputParameterHandler.getValue('pdata')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    if sYear:
        sMovieTitle = sMovieTitle + ' (' + sYear + ')'

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)
    sHtmlContent = oRequest.request()
    sPattern = '(?:<iframe|<IFRAME).+?(?:src|SRC)=(?:\'|")(.+?)(?:\'|")'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
