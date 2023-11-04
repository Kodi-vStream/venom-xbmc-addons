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

SITE_IDENTIFIER = 'french_stream_lol'
SITE_NAME = 'French-stream-lol'
SITE_DESC = 'Films & séries'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'xfsearch/genre-1/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'xfsearch/version-film/VOSTFR/', 'showMovies')
MOVIE_VF_FRENCH = (URL_MAIN + 'xfsearch/version-film/French/', 'showMovies')
MOVIE_VF_TRUEFRENCH = (URL_MAIN + 'xfsearch/version-film/TrueFrench/', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'xfsearch/qualit/HDLight/', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + 'film/film-netflix/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'xfsearch/version-serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VFS = (URL_MAIN + 's-tv/s-vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 's-tv/s-vostfr/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (key_search_series, 'showMovies')

# recherche utilisée quand on utilise directement la source
MY_SEARCH_MOVIES = (True, 'showSearchMovie')
MY_SEARCH_SERIES = (True, 'showSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_FRENCH[1], 'Films (Netflix)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_TRUEFRENCH[1], 'Films (True French)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (HD Light)', 'films.png', oOutputParameterHandler)

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


def showSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = []
    listegenre = ['action', 'animation', 'arts-martiaux', 'aventure', 'biopic', 'comedie', 'drame', 'documentaire',
                  'epouvante-horreur', 'espionnage', 'famille', 'fantastique', 'guerre', 'historique', 'policier',
                  'romance', 'science-fiction', 'thriller', 'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + 'xfsearch/genre-1/' + igenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'serie-action'], ['Animation', 'animation-serie'], ['Aventure', 'aventure-serie'],
             ['Biopic', 'biopic-serie'], ['Comédie', 'serie-comedie'], ['Drame', 'drame-serie'],
             ['Famille', 'familles-serie'], ['Fantastique', 'serie-fantastique'], ['Historique', 'serie-historique'],
             ['Horreur', 'serie-horreur'], ['Judiciaire', 'serie-judiciare'], ['Médical', 'serie-medical'],
             ['Policier', 'serie-policier'], ['Romance', 'serie-romance'], ['Science-fiction', 'serie-science-fiction'],
             ['Thriller', 'serie-thriller'], ['Western', 'serie-western'], ['K-Drama', 'serie/k-drama']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
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
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        # sUrl = URL_SEARCH[0]  # ne sert à rien
        sSearch = sSearch.replace(' ', '+').replace('%20', '+')

        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        sUrl = URL_MAIN + 'index.php?story=' + sSearch + '&do=search&subaction=search'
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        # la méthode suivante fonctionne mais pas à 100%
        # pdata = 'do=search&subaction=search&search_start=1&full_search=0&result_from=1&story=' + sSearch
        # oRequest = cRequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        # oRequest.addHeaderEntry('Referer', URL_MAIN)
        # oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        # oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        # oRequest.addParametersLine(pdata)
        # sHtmlContent = oRequest.request()

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'with-mask" href="([^"]+).+?src="([^"]*).+?title">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1].replace('/red.php?src=', '').replace('&.webp', '')
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = aEntry[2].replace('Saisn', 'Saison')

            if bSearchMovie:  # il n'y a jamais '/serie' dans sUrl2
                if '- Saison' in sTitle:
                    continue
            if bSearchSerie:
                if '- Saison' not in sTitle:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl2 or 'serie/' in sUrl or '/serie' in sUrl or 's-tv' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif bSearchSerie is True or '- Saison' in sTitle:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '(\d+)</a>\s*</span><span class="pnext"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


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

    sPattern = '</style><p class="desc-text">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'french stream lol'
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', cleanDesc(aResult[1][0]))

    sPattern = '<div class="episode-title">([^:]+).+?episode=.+?-([^"]+).+?data-url.+?"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sLang = ''
    bFind = ''

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[1].replace('-tab', '').replace('"', '')
                bFind = True
                sEpisode = aEntry[0]

            if bFind and aEntry[0]:
                sFirst_Url = aEntry[2]
                if not 'http' in sFirst_Url :
                    continue
            
                sHoster = re.findall('https:\/\/([^.]+)', sFirst_Url) 
                sHoster = sHoster[0]
                oHoster = cHosterGui().checkHoster(sHoster)
            if not oHoster:
                continue 
                
                #sRel_Episode = aEntry[2]
                #if sRel_Episode == "ABCDE":
                    #sEpisode = 'Episode 2'
                #else:
                    #sEpisode = aEntry[3]

            sTitle = sMovieTitle + ' ' + sEpisode
            sDisplayTitle = ' %s (%s) [COLOR skyblue]%s[/COLOR]' % (sTitle,  sLang,  sHoster )

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sLang', sLang)
            #oOutputParameterHandler.addParameter('sRel_Episode', sRel_Episode)
            oOutputParameterHandler.addParameter('sFirst_Url', sFirst_Url)

            oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sLang = oInputParameterHandler.getValue('sLang')
    sFirst_Url = oInputParameterHandler.getValue('sFirst_Url')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sRel_Episode = oInputParameterHandler.getValue('sRel_Episode')
    if not sRel_Episode:
        numEpisode = oInputParameterHandler.getValue('sEpisode')  # Gestion Up_Next
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

    if not aResult[0]:
        # dans cas où il n'y a qu'un seul lien, il n'y a pas de référence dans <div id="episodexx" class="fullsfeature">
        # le pattern devient alors normalement hs
        if sFirst_Url:
            sHosterUrl = sFirst_Url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    if aResult[0]:
        html = aResult[1][0]
        sPattern = 'href="([^"]+).*?aria-hidden'
        aResultUrl = oParser.parse(html, sPattern)
        if aResultUrl[0] is True:
            for aEntry in aResultUrl[1]:
                sHosterUrl = aEntry

                if 'http' not in sHosterUrl:  # liens naze du site url
                    continue

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
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
    sPattern = '<li>\s*<a.*?href="([^"]+).+?<\/i>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            #  supprime le premier lien qui est ensuite reproposé avec la langue
            if 'FRENCH' not in aEntry[1] and 'VOSTFR' not in aEntry[1]:
                continue
            sLang = aEntry[1].strip()
            sDisplayTitle = '%s (%s)' %(sMovieTitle, sLang)

            sHosterUrl = aEntry[0]
            if 'http' not in sHosterUrl:  # liens nazes du site url
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def cleanDesc(sDesc):
    oParser = cParser()
    sPattern = '(Résumé.+?</p> )'
    aResult = oParser.parse(sDesc, sPattern)

    if aResult[0]:
        sDesc = sDesc.replace(aResult[1][0], '')

    list_comment = [':', 'en streaming', 'Voir Serie ']

    for s in list_comment:
        sDesc = sDesc.replace(s, '')

    return sDesc
