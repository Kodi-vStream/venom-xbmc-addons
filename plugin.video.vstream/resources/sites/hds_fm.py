# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'hds_fm'
SITE_NAME = 'Hds-fm'
SITE_DESC = 'Films et Séries'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/VOSTFR/', 'showMovies')
MOVIE_VF = (URL_MAIN + 'film/French/', 'showMovies')

MOVIE_HDLIGHT = (URL_MAIN + 'qualit/HDLight/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'serie-tv-streaming/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

SERIE_VFS = (URL_MAIN + 'serie/VF/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie/VOSTFR/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on n'utilise pas le globale
MY_SEARCH_MOVIES = (True, 'myShowSearchMovie')
MY_SEARCH_SERIES = (True, 'myShowSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (HD Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def myShowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def myShowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    # genre enlevés tous les films hs : Walt-Disney, Super_héros
    # arts-martiaux 4 films marche sur 150

    liste = []
    listegenre = ['action', 'animation', 'arts-martiaux', 'aventure', 'biopic', 'comédie', 'comédie-dramatique',
                  'comédie-musicale', 'drame', 'documentaire', 'epouvante_horreur', 'espionnage', 'famille',
                  'fantastique', 'musical', 'guerre', 'historique', 'policier', 'romance', 'science-fiction',
                  'thriller', 'western']

    # https://www1.hds.fm/film-genre/action
    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'film-genre/' + igenre])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()
    liste = []
    listegenre = ['Action', 'Animation', 'Arts-martiaux', 'Aventure', 'Biopic', 'Comédie', 'Drame',
                  'Epouvante_horreur', 'Famille', 'Historique', 'Judiciaire', 'Médical', 'Policier',
                  'Romance', 'Science-fiction', 'Sport-event', 'Thriller', 'Western']

    # https://www1.hds.fm/serie-genre/Drame/
    for igenre in listegenre:
        urlgenre = igenre
        if igenre == 'judiciaire':
            urlgenre = 'judiciare'
        liste.append([igenre.capitalize(), URL_MAIN + 'serie-genre/' + urlgenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        sSearch = sSearch.replace('%20', ' ')
        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch)
        sSearch2 = sSearch.replace('-', '').strip().lower()
        sUrl = URL_SEARCH[0] + sSearch2
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # ref thumb title
    sPattern = 'class="TPostMv">.+?href="([^"]*).+?src="([^"]*).+?class="Qlty".+?class="Qlty.+?>([^<]*).+?center">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # itemss = 0

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sLang = aEntry[2]
            sTitle = aEntry[3]

            if bSearchMovie:
                if ' saison ' in sTitle.lower():
                    continue
            if bSearchSerie:
                if ' saison ' not in sTitle.lower():
                    continue

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

            sDisplayTitle = ('%s (%s)') % (sTitle.replace('- Saison', ' Saison'), sLang)
            if sSearch and not bSearchMovie and not bSearchSerie:
                if '/serie' in sUrl or '- saison ' in sTitle.lower():
                    sDisplayTitle = sDisplayTitle + ' [Série]'
                else:
                    sDisplayTitle = sDisplayTitle + ' [Film]'

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            # pour le debugage source avec bcpdechance d'etre hs
            # films didfficile a obtenir apres id= 18729
            # if not ('/serie' in sUrl or ' saison ' in sTitle.lower()):
                # idmovie = get_id_int_Movie(sUrl2)
                # if idmovie  <= 18729:
                    # sDisplayTitle = sDisplayTitle + ' *'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl or '- saison ' in sTitle.lower():
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bNextPage, sNextPage, sNumPage = __checkForNextPage(sHtmlContent)
        if bNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sNumberNext = ''
    sNumberMax = ''
    sNumPage = ''

    if '<a class="next"' not in sHtmlContent:
        return False, 'none', 'none'

    if 'class="end"' in sHtmlContent:
        sPattern = 'class="end".+?">(\d+)'
    else:
        sPattern = '(\d+)<.a>\s*<a\sclass="next"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0]

    sPattern = 'class="next.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0]  # minimum requis
        if 'htpp' not in sNextPage:
            sNextPage = URL_MAIN[:-1] + sNextPage
            if '/31/32/' in sNextPage:  # bug page 31
                sNextPage = re.sub('/31', '', sNextPage)
        try:
            sNumberNext = re.search('/(\d+)/', sNextPage).group(1)
        except:
            pass

        if sNumberNext:
            sNumPage = sNumberNext
            if sNumberMax:
                sNumPage = sNumPage + '/' + sNumberMax

        if sNextPage:
            return True, sNextPage, sNumPage

    return False, 'none', 'none'


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'saison' not in sMovieTitle.lower():
        sPattern = 'saison-(\d+)'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            sMovieTitle = sMovieTitle + ' Saison ' + aResult[1][0]

    sPattern = '<div class="Description">.*?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'Hds Film'
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', cleanDesc(aResult[1][0]))

    sPattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\d+)"\s*href="([^"]+).+?title="([^"]+).+?data-rel="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    bFind = ''
    validEntry = ''
    sLang = ''

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0].replace('-tab', '').replace('"', '')
                bFind = True

            if bFind and aEntry[1]:
                validEntry = True
                sFirst_Url = aEntry[1]
                sEpisode = aEntry[2]
                sRel_Episode = aEntry[3]

                sTitle = sMovieTitle.replace('- Saison', ' Saison') + ' ' + sEpisode
                sDisplayTitle = sTitle + ' (' + sLang + ')'

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sLang', sLang)
                oOutputParameterHandler.addParameter('sRel_Episode', sRel_Episode)
                oOutputParameterHandler.addParameter('sFirst_Url', sFirst_Url)

                oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not validEntry:
        oGui.addText(SITE_IDENTIFIER, '# Aucune vidéo trouvée #')

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sRel_Episode = oInputParameterHandler.getValue('sRel_Episode')
    sFirst_Url = oInputParameterHandler.getValue('sFirst_Url')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sRel_Episode + '" class="fullsfeature".*?<a (id="singh.*?<div style="height)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        # cas ou il n'y a qu'un seul lien  pas de référence  dans <div id="episodexx" class="fullsfeature">
        # le pattern est normalement hs
        if sFirst_Url:
            sUrl2 = sFirst_Url
            # sHost = '[COLOR coral]' + getHostName(sUrl2) + '[/COLOR]'

            # sDisplayTitle = sMovieTitle + ' ' + sHost
            sHosterUrl = sUrl2
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    if aResult[0]:
        html = aResult[1][0]
        sPattern = 'href="([^"]+).*?aria-hidden'
        aResultUrl = oParser.parse(html, sPattern)
        if aResultUrl[0] is True:
            for aEntry in aResultUrl[1]:
                sUrl2 = aEntry
                # sHost = getHostName(sUrl2)
                if len(aResult[1]) == 1 and 'openload' in sUrl2:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue] openload : site non sécurisé [/COLOR]')
                    continue

                if isBlackHost(sUrl2):
                    continue

                # if 'hqq.tv' in sUrl2:
                    # continue

                # if 'www' in sHost.lower():
                    # sHost = getHostName(sUrl2)

                # sHost = '[COLOR coral]' + sHost + '[/COLOR]'
                # sDisplayTitle = sMovieTitle + ' ' + sHost

                sHosterUrl = sUrl2
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a style=".+?cid="([^"]+).+?fa-play.+?i>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sHost = aEntry[1].strip().capitalize()
            if len(aResult[1]) == 1:
                if 'openload' in sHost.lower():
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue] openload : site non sécurisé [/COLOR]')
                    continue
                if 'oload' in sHost.lower():
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue] oload : site non sécurisé [/COLOR]')
                    continue

            if isBlackHost(sUrl2):
                continue

            # if 'hqq.tv' in sUrl2:
                # continue

            sHosterUrl = sUrl2
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()


# teste id movie
def get_id_int_Movie(url):

    try:
        number = re.search('https.+?\/(\d+)', url).group(1)
        return int(number)
    except:
        return 20000
        pass
    return 20000


def getHostName(url):

    try:
        if 'opsktp' in url:
            sHost = re.search('http.+?opsktp.+?\/([^\/]+)', url).group(1)

        elif 'www' not in url:
            sHost = re.search('http.*?\/\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\/\/(?:www).([^.]*)', url).group(1)
    except:
        sHost = url

    return sHost.capitalize()


def cleanDesc(sDesc):
    oParser = cParser()
    sPattern = '(Résumé.+?streaming Complet)'
    aResult = oParser.parse(sDesc, sPattern)

    if aResult[0]:
        sDesc = sDesc.replace(aResult[1][0], '')

    list_comment = [':', 'en streaming', 'Voir Serie ']

    for s in list_comment:
        sDesc = sDesc.replace(s, '')

    return sDesc


def isBlackHost(url):
    black_host = ['youflix', 'verystream', 'javascript', '4k-pl', 'ffsplayer', 'french-stream.ga', 'oload.stream',
                  'french-player.ga', 'streamango.com', 'hqq.tv']

    urllower = url.lower()
    for host in black_host:
        if host.lower() in urllower:
            return True
    return False
