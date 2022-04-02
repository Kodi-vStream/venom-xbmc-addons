# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 08 update 14/01/2021
# return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
import re
import string

TimeOut = 10  # requetes avec time out utilisées seulement dans show movies : on attend plus 30s
SITE_IDENTIFIER = 'mystream_zone'
SITE_NAME = 'My Stream'
SITE_DESC = 'Films et Series en Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
imdmovies = '#movies'  # tag request
imdseries = '#series'

# variables globales
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')
# variables internes
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'movies/', 'showMovies')
# serie&movie a revoir
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_NOTES = (URL_MAIN + 'imdb/' + imdmovies, 'showMovies')
MOVIE_ALPHA = (True, 'showAlphaMovies')
MOVIE_TENDANCE = (URL_MAIN + 'tendance/', 'showMovies')
MOVIE_FEATURED = (URL_MAIN, 'showMovies')
MOVIE_TOP_IMD = (URL_MAIN + 'imdb/' + imdmovies, 'showMovies')  # = globale MOVIE_NOTES

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tvshows/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'imdb/' + imdseries, 'showMovies')
SERIE_ALPHA = (True, 'showAlphaSeries')
SERIE_TOP_IMD = (URL_MAIN + 'imdb/' + imdseries, 'showMovies')
SERIE_NEWS_SAISONS = (URL_MAIN + 'seasons/', 'showMovies')
SERIE_NEWS_EPISODES = (URL_MAIN + 'episodes/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Séries (Par Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TENDANCE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TENDANCE[1], 'Films & Séries (Populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films & Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], ' Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FEATURED[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FEATURED[1], 'Films (En vedette)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP_IMD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP_IMD[1], 'Films (Top IMDb)', 'tmdb.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ALPHA[1], 'Films (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_SAISONS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_SAISONS[1], 'Séries (Saisons récentes)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODES[1], 'Séries (Episodes récents)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TOP_IMD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TOP_IMD[1], 'Séries (Top IMDd)', 'tmdb.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ALPHA[1], 'Séries (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + key_search_series + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + key_search_movies + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Action & Adventure', 'action-adventure'], ['Adventure', 'adventure'],
             ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comedie', 'comedie'], ['Comedy', 'comedie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Documentary', 'documentary'], ['Drama', 'drama'],
             ['Drame', 'drame'], ['Familial', 'familial'], ['Family', 'family'], ['Fantastique', 'fantastique'],
             ['Fantasy', 'fantasy'], ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['History', 'history'],
             ['Horreur', 'horreur'], ['Horror', 'horror'], ['Kids', 'kids'], ['Music', 'music'], ['Musique', 'musique'],
             ['Mystère', 'mystere'], ['Mystery', 'mystery'], ['Reality', 'reality'], ['Romance', 'romance'],
             ['Sci-Fi & Fantasy', 'sci-fi-fantasy'], ['Sci-Fi', 'science-fiction'],
             ['Sci-Fi & Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Talk', 'talk'],
             ['Telefilm', 'telefilm'], ['Thriller', 'thriller'], ['Tv Movie', 'tv-movie'], ['Guerre', 'war'],
             ['Guerre & politique', 'war-politics'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrlGenre in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'genre/' + sUrlGenre + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showAlphaMovies():
    showAlpha('movies')


def showAlphaSeries():
    showAlpha('tvshows')


def showAlpha(stype):
    oGui = cGui()
    # requete json 20 resultat max
    # https://www3.mystream.zone/wp-json/dooplay/glossary/?term=g&nonce=2132c17353&type=tvshows
    url1 = URL_MAIN + 'wp-json/dooplay/glossary/?term='
    url2 = '&nonce='
    snonce = '2132c17353'  # a surveiller si jamais cela change
    url3 = '&type='

    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = []
    for alpha in listalpha:
        liste.append([str(alpha).upper(), url1 + str(alpha) + url2 + snonce + url3 + stype])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    # https://www3.mystream.zone/release/2020
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1982, 2022)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'release/' + sYear + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    bSearchMovie = False
    bSearchSerie = False

    if sSearch:
        sUrl = sSearch.replace(' ', '%20')
        if key_search_movies in sUrl:
            sUrl = str(sUrl).replace(key_search_movies, '')
            bSearchMovie = True

        if key_search_series in sUrl:
            sUrl = str(sUrl).replace(key_search_series, '')
            bSearchSerie = True

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'wp-json' in sUrl and not sSearch:
        try:
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setTimeout(TimeOut)
            jsonrsp = oRequestHandler.request(jsonDecode=True)
        except Exception as e:
            if str(e) == "('The read operation timed out',)":
                oGui.addText(SITE_IDENTIFIER, 'site Inaccessible')
                oGui.setEndOfDirectory()
                return
            else:
                oGui.addText(SITE_IDENTIFIER, 'Request Failed')
                oGui.setEndOfDirectory()
                return

        oOutputParameterHandler = cOutputParameterHandler()
        for i, idict in jsonrsp.items():
            sTitle = str(jsonrsp[i]['title'].encode('utf-8', 'ignore')).replace(' mystream', '')  # I Know This Much Is True mystream
            sTitle = sTitle[2:-1]
            sUrl2 = str(jsonrsp[i]['url'])
            sThumb = str(jsonrsp[i]['img'])
            sThumb = re.sub('https:..ml2o99dkuow5.i.optimole.+?/https', 'https', sThumb)
            sYear = str(jsonrsp[i]['year'])
            sDisplayTitle = sTitle + ' (' + sYear + ')'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if 'type=tvshows' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
        # 1 result with <= 20 items
        oGui.setEndOfDirectory()
        return

    if '/tendance/' in sUrl:  # thumb; title; url; year #regex ok
        sPattern = 'asyncsrc="([^"]*)" alt="([^"]*).+?ahref="([^"]*).+?<span>([^<]*)'

    elif sUrl == URL_MAIN:  # thumb; title; url; year #regex ok
        sPattern = 'post-featured.+?src="(h[^"]+).+?alt="([^"]+).+?href="([^"]+).+?<span>([^<]*)'

    elif '/seasons/' in sUrl:  # thumb; url; number; title #regex ok
        sPattern = 'se seasons.+?src="(h[^"]*).+?href="([^"]*).+?class="b">([^<]*).+?c">([^<]*)'

    elif '/episodes/' in sUrl:  # thumb; url; 'S* E*'; title; #regex ok
        sPattern = 'se episodes".+?src="(h[^"]*).+?href="([^"]+).+?<span>([^/]+).+?">([^<]+)'

    elif '?s=' in sUrl:  # thumb; url; title; year; desc #regex ok
        sPattern = 'asyncsrc="(h[^"]+).+?ref="([^"]*)">([^<]*).+?year">([^<]*).*?contenido.><p>([^<]*)'

    elif '/genre/' in sUrl or '/release/' in sUrl:  # thumb; url; title; year; desc #regex ok
        sPattern = 'asyncsrc="(h[^"]*).+?href="([^"]+)">([^<]+).+?span>.+?,.([^<]*).+?texto">([^<]*)'

    elif '/imdb/' in sUrl:  # url; thumb; title; rate #regex ok
        sPattern = "poster'.+?ref='([^']*).+?src='(h[^']*).+?alt='([^']*).+?rating'>([^<]*)"

    elif '/tvshows/' in sUrl or '/movies/' in sUrl:  # thumb; title; url; year; desc #regex ok
        sPattern = 'noscript>.+?src="([^"]+).+?alt="([^"]+).+?href="([^"]+).+?class="metadata".+?<span>(\d+).+?class="texto">([^<]*)'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setTimeout(TimeOut)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # filtrage sHtmlContent
    sStart = '<h2>Recently added</h2>'
    sEnd = 'class="pagination"><span>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # pour les sThumb
    # sHtmlContent = re.sub('https:..ml2o99dkuow5.i.optimole.+?/https', 'https', sHtmlContent)

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        sDesc = ''
        sYear = ''
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if '/tendance/' in sUrl:  # thumb; title; url; year
                sThumb = aEntry[0]
                sTitle = aEntry[1].replace(' mystream', '')
                sUrl2 = aEntry[2]
                sYear = aEntry[3]
                if sYear != '':
                    sYear = re.search('(\d{4})', sYear).group(1)
                sDisplayTitle = sTitle + ' (' + sYear + ')'

            elif sUrl is URL_MAIN:  # thumb; title; url; year
                sThumb = aEntry[0]
                sTitle = aEntry[1].replace(' mystream', '')
                sUrl2 = aEntry[2]
                sYear = aEntry[3]
                sDisplayTitle = sTitle + ' (' + sYear + ')'

            elif '/seasons/' in sUrl:  # thumb; url; number; title
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sTitle = aEntry[3].replace(' mystream', '')
                sDisplayTitle = sTitle + ' Saison ' + aEntry[2]

            elif '/episodes/' in sUrl:  # thumb; url; 'S* E*'; title
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sYear = ''  # inutile pour les séries
                sTitle = aEntry[3] + ' ' + aEntry[2]
                sDisplayTitle = sTitle + '(' + sYear + ')'

            elif '?s=' in sUrl:  # thumb; url; title; year; desc
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sTitle = aEntry[2].replace(' mystream', '')
                sYear = aEntry[3]
                sDesc = aEntry[4]
                sDisplayTitle = sTitle + ' (' + sYear + ')'

            elif '/genre/' in sUrl or '/release/' in sUrl:  # thumb; url; title; year; desc
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sTitle = aEntry[2].replace(' mystream', '')
                sYear = aEntry[3]
                sDesc = aEntry[4]
                sDisplayTitle = sTitle + ' (' + sYear + ')'

            elif '/imdb/' in sUrl:  # url; thumb; title; rate
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

            elif '/tvshows/' in sUrl or '/movies/' in sUrl:  # thumb; title; url; year; desc
                sThumb = aEntry[0]
                sTitle = aEntry[1].replace(' mystream', '')
                sUrl2 = aEntry[2]
                sYear = aEntry[3]
                if sYear != '':
                    sYear = re.search('(\d{4})', sYear).group(1)
                sDesc = aEntry[4]
                sDisplayTitle = sTitle + ' (' + sYear + ')'

            if sSearch or '/release/' in sUrl or '/genre/' in sUrl or '/tendance/' in sUrl:
                if 'movies' in sUrl2 and not bSearchMovie:
                    sDisplayTitle = sDisplayTitle + ' (Film)'
                if 'tvshows' in sUrl2 and not bSearchSerie:
                    sDisplayTitle = sDisplayTitle + ' (Série)'

            # filtre recherche par type
            if bSearchMovie:
                if 'tvshows' in sUrl2:
                    continue
                else:
                    sDisplayTitle = sDisplayTitle
            if bSearchSerie:
                if 'movies' in sUrl2:
                    continue
                else:
                    sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if 'mystream.zone/tvshows' in sUrl2:  # inutile mais ne pas enlever resoudre regex
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'mystream.zone/seasons' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'pagination"><span>Page \d+ de (\d+)</span>.+?current">\d+</span><ahref=.([^"|\']+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    # probleme temps de la requete aleatoire normale, lent, ou tps de connexion > max autorisé
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # temps qui peu depasser 10 secondes parfois

    # on passe ts les liens des épisodes dans chaque dossier saisons créés ds un liste
    # car pas de liens existants ds la page pour acceder aux pages de chaque saison
    if not sDesc:
        try:
            sPattern = '<h2>Synopsis.+?content"> <p>([^<]*)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            pass

    # '2 - 11'   href   title
    # class='numerando'>([^<]*).+?href='([^']*).>([^<]*) #
    sPattern = "class='numerando'>(\d+) - (\d+)<.+?href='([^']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            iSaison = aEntry[0]
            iEpisode = aEntry[1]
            sUrl = aEntry[2]

            sTitle = sMovieTitle + ' Saison ' + str(iSaison) + ' Episode ' + str(iEpisode)

            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showListEpisodes():  # plus utilisé
    # parent https://www3.mystream.zone/tvshows
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
    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            listeUrlEpisode2.append(aEntry)

    aResult = oParser.parse(listeStitle, sPattern)
    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            listeStitle2.append(aEntry)
    i = 0
    oOutputParameterHandler = cOutputParameterHandler()
    for itemurl in listeUrlEpisode2:
        sTitle = listeStitle2[i]
        i = i + 1
        oOutputParameterHandler.addParameter('siteUrl', itemurl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    # parents https://www3.mystream.zone/saisons/    # SERIE_NEWS_SAISONS
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
    # '2 - 11'   url
    sPattern = "class='numerando'>([^<]*).+?href='([^']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            iSaison = re.search('([0-9]+)', aEntry[0]).group(1)
            iEpisode = re.search('([0-9]+)$', aEntry[0]).group(1)
            sUrl = aEntry[1]
            sDisplayTitle = sMovieTitle + ' ' + ' Saison ' + str(iSaison) + ' Episode ' + str(iEpisode)

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
            pass

    sPattern = "data-type='([^']*).*?post='([^']*).*?nume='([^']*).*?title'>([^<]*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            datatype = aEntry[0]
            datapost = aEntry[1]
            datanum = aEntry[2]
            sHost = aEntry[3]
            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            pdata = 'action=doo_player_ajax&post=' + datapost + '&nume=' + datanum + '&type=' + datatype
            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, sHost.capitalize())

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('pdata', pdata)
            oGui.addLink(SITE_IDENTIFIER, 'hostersLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def hostersLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    referer = oInputParameterHandler.getValue('referer')
    pdata = oInputParameterHandler.getValue('pdata')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)
    sHtmlContent = oRequest.request(jsonDecode=True)

    sHosterUrl = sHtmlContent["embed_url"]

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
