# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 34 https://french-stream.lol/  french-stream.lol 29112020
# update 02042021
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog


SITE_IDENTIFIER = 'french_stream_lol'
SITE_NAME = 'French-stream-lol'
SITE_DESC = 'Films & séries'

URL_MAIN = 'https://french-stream.re/'

MOVIE_NEWS = (URL_MAIN + 'xfsearch/qualit/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/vostfr/', 'showMovies')

MOVIE_VF_FRENCH = (URL_MAIN + 'xfsearch/version-film/French/', 'showMovies')
MOVIE_VF_TRUEFRENCH = (URL_MAIN + 'xfsearch/version-film/TrueFrench/', 'showMovies')

MOVIE_HDLIGHT = (URL_MAIN + 'xfsearch/qualit/HDLight/', 'showMovies')
MOVIE_DVD = (URL_MAIN + 'xfsearch/qualit/DVDSCR/', 'showMovies')
MOVIE_CAM = (URL_MAIN + 'xfsearch/qualit/CAM/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'xfsearch/version-serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VFS = (URL_MAIN + 'serie/serie-en-vf-streaming/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie/serie-en-vostfr-streaming/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on utilise directement la source
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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_FRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_FRENCH[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_TRUEFRENCH[1], 'Films (True French)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (HD Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_DVD[1], 'Films (DVD)', 'films.png', oOutputParameterHandler)

    # Aucun intérêt
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (CAM)', 'films.png', oOutputParameterHandler)

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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_FRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_FRENCH[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_TRUEFRENCH[1], 'Films (True French)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (HD Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_DVD[1], 'Films (DVD)', 'films.png', oOutputParameterHandler)

    # Aucun intérêt
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (CAM)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
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


def myShowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def myShowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = []  # 'romance'
    listegenre = ['action', 'animation', 'arts-martiaux', 'aventure', 'biopic', 'comedie', 'drame',
                  'documentaire', 'epouvante-horreur', 'espionnage', 'famille', 'fantastique',
                  'guerre', 'historique', 'policier', 'science-fiction', 'thriller', 'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + igenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = []
    listegenre = ['action', 'animation', 'aventure', 'biopic', 'comedie', 'drame', 'famille', 'fantastique',
                  'historique', 'horreur', 'judiciaire', 'medical', 'policier', 'romance', 'science-fiction',
                  'thriller', 'western']

    # https://french-stream.lol/serie-judiciare/
    # https://french-stream.lol/serie/serie-judiciare/
    for igenre in listegenre:
        urlgenre = igenre
        if igenre == 'judiciaire':
            urlgenre = 'judiciare'
        liste.append([igenre.capitalize(), URL_MAIN + 'serie/serie-' + urlgenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):

    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        # sUrl = URL_SEARCH[0]  # sert a rien
        sSearch = sSearch.replace(' ', '+').replace('%20', '+')

        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        pdata = 'do=search&subaction=search&search_start=1&full_search=0&result_from=1&story=' + sSearch
        oRequest = cRequestHandler(URL_SEARCH[0])
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'with-mask" href="([^"]+).+?src="([^"]*).+?title">([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2].replace('- Saison', ' Saison')  # uniquement pour les séries

            if bSearchMovie:
                if '/serie' in sUrl2:
                    continue
            if bSearchSerie:
                if '/serie' not in sUrl2:
                    continue

            sDisplayTitle = sTitle
            if sSearch and not bSearchMovie and not bSearchSerie:
                if '/serie' in sUrl2 or 'serie/' in sUrl or '/serie' in sUrl:
                    sDisplayTitle = sDisplayTitle + ' [Série]'
                else:
                    sDisplayTitle = sDisplayTitle + ' [Film]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl2 or 'serie/' in sUrl or '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bNextPage, sNextPage, sNumPage = __checkForNextPage(sHtmlContent)
        if (bNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sNumberNext = ''
    sNumberMax = ''
    sNumPage = ''

    sPattern = '(\d+)<.a>\s*<.span>\s*<span class="pnext">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0]

    sPattern = '<span class="pnext"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNextPage = aResult[1][0]  # minimum requis
        try:
            sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
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
        if (aResult[0] == True):
            sMovieTitle = sMovieTitle + ' Saison ' + aResult[1][0]

    sPattern = 'id="s-desc">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'french stream lol'
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', cleanDesc(aResult[1][0]))

    sPattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\d+)"\s*href="([^"]+).+?data-rel="([^"]+).+?</i>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sLang = ''
    bFind = ''

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0].replace('-tab', '').replace('"', '')
                bFind = True

            if bFind and aEntry[1]:
                sFirst_Url = aEntry[1]
                sRel_Episode = aEntry[2]
                if sRel_Episode == "ABCDE":
                    sEpisode = 'Episode 2'
                else:
                    sEpisode = aEntry[3]

                sTitle = sMovieTitle.replace('- Saison', ' Saison') + ' ' + sEpisode
                sDisplayTitle = sTitle + ' (' + sLang + ')'

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sLang', sLang)
                oOutputParameterHandler.addParameter('sRel_Episode', sRel_Episode)
                oOutputParameterHandler.addParameter('sFirst_Url', sFirst_Url)

                oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieLinks():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sLang = oInputParameterHandler.getValue('sLang')
    sFirst_Url = oInputParameterHandler.getValue('sFirst_Url')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sRel_Episode = oInputParameterHandler.getValue('sRel_Episode')
    if not sRel_Episode:
        numEpisode = oInputParameterHandler.getValue('sEpisode') # Gestion Up_Next
        if numEpisode:
            numEpisode = int(numEpisode)
            if 'VO' in sLang:
                numEpisode += 32 
            if numEpisode == 2:
                sRel_Episode = 'ABCDE'
            else:
                sRel_Episode = 'episode%d' % numEpisode

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sRel_Episode + '" class="fullsfeature".*?<li><a (id="singh.*?<div style="height)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        # dans cas ou il n'y a qu'un seul lien il n'y a pas de reference  dans <div id="episodexx" class="fullsfeature">
        # le pattern devient alors normalement hs
        if sFirst_Url:
            sHosterUrl = sFirst_Url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        

    if (aResult[0] == True):
        html = aResult[1][0]
        sPattern = 'href="([^"]+).*?aria-hidden'
        aResulturl = oParser.parse(html, sPattern)
        if (aResulturl[0] == True):
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResulturl[1]:
                sHosterUrl = aEntry

                if isBlackHost(sHosterUrl):
                    continue

                if 'http' not in sHosterUrl:  # liens naze du site url
                    continue

                if 'hqq.tv' in sHosterUrl:
                    continue
                    # pass

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showMovieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'id="s-desc">([^<]+)|Date de sortie:<.span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'french stream lol'
    if (aResult[0] == True):
        try:  # a verifier
            if len(aResult[1]) == 2:
                sYear = aResult[1][1][1]
                sDesc = cleanDesc(aResult[1][0][0])
                sDesc = ('%s [I][COLOR grey]%s[/COLOR][/I] %s') % ('Année : ' + sYear + '\r\n', 'Synopsis :', sDesc)
            else:
                sDesc = (' [I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', cleanDesc(aResult[1][0][0]))
        except:
            pass

    sPattern = '<li>\s*<a.*?href="([^"]+).+?hidden="true'
    aResult = oParser.parse(sHtmlContent, sPattern)

    valide_host = []

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if isBlackHost(sHosterUrl):
                continue

            if 'http' not in sHosterUrl:  # liens nazes du site url
                continue
            if 'hqq.tv' in sHosterUrl:
                continue

            if sHosterUrl not in valide_host:  # à cause de l'url par défaut
                valide_host.append(sHosterUrl)
            else:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def isBlackHost(url):
    black_host = ['playzer.xyz']  # à rajouter
    urlLower = url.lower()
    for host in black_host:
        if host.lower() in urlLower:
            return True
    return False


def cleanDesc(sDesc):

    oParser = cParser()
    sPattern = '(Résumé.+?streaming Complet)'
    aResult = oParser.parse(sDesc, sPattern)

    if (aResult[0] == True):
        sDesc = sDesc.replace(aResult[1][0], '')

    list_comment = [':', 'en streaming', 'Voir Serie ']

    for s in list_comment:
        sDesc = sDesc.replace(s, '')

    return sDesc
