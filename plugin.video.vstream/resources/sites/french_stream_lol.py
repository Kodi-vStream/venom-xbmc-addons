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
MOVIE_VOSTENG = (URL_MAIN + 'xfsearch/version-film/VOSTENG/', 'showMovies')

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

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (HD Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_FRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_FRENCH[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_TRUEFRENCH[1], 'Films (True French)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTENG[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTENG[1], 'Films (VOSTENG)', 'vostfr.png', oOutputParameterHandler)

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
    listegenre = ['action', 'animation', 'arts+martiaux', 'aventure', 'biopic', 'comedie', 'drame', 'documentaire',
                  'epouvante-horreur', 'espionnage', 'famille', 'fantastique', 'guerre', 'historique', 'policier',
                  'romance', 'science-fiction', 'thriller', 'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize().replace('+','-'), URL_MAIN + 'xfsearch/genre-1/' + igenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'action-serie'], ['Animation', 'animation-serie'], ['Aventure', 'aventure-series'],
             ['Biopic', 'serie-biopic'], ['Comédie', 'comedie-serie'], ['Documentaire', 'documentaire-serie'], ['Drame', 'drame-serie'],
             ['Famille', 'familles-series'], ['Fantastique', 'fantastique-series'], ['Historique', 'serie-historiques'],
             ['Horreur', 'horreur-serie'], ['Judiciaire', 'judiciare-series'], ['K-Drama', 'k-drama'], ['Médical', 'medical-series'],
             ['Policier', 'policier-series'], ['Romance', 'romance-series'], ['Science-fiction', 'science-fiction-series'],
             ['Thriller', 'thriller-series'], ['Western', 'western-series']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '-/')
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

        # sUrl = URL_SEARCH[0] # ne sert à rien
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
            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2
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
                if '- Saison' in sTitle:
                    oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
                else:
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

    sPattern = '</style> *<p class="desc-text">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = ''
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', cleanDesc(aResult[1][0]))

    numEpisodes = []
    sPatternTab = 'fa-play-circle-o"></i> *(.+?) *</div>(.+?)</div></div>'
    sPattern = 'target="seriePlayer".+?</i>.+?(\d+)'
    aResultTab = oParser.parse(sHtmlContent, sPatternTab)
    if aResultTab[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntryTab in aResultTab[1]:
            aResult = oParser.parse(aEntryTab[1], sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    sEpisode = aEntry
                    if sEpisode in numEpisodes:
                        continue
                    numEpisodes.append(sEpisode)
                    sTitle = sMovieTitle + ' Episode' + sEpisode
                    sDisplayTitle = sTitle
        
                    oOutputParameterHandler.addParameter('siteUrl', sUrl + "|" + sEpisode)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        
                    oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSerieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl, sEpisode = sUrl.split('|')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    hasEpisode = False
    sPatternTab = '!-- episode %s .+?(border-color:|clear:both).+?>(.+?)<(.+?)!-- episode %s ' % (sEpisode, sEpisode)
    aResultTab = oParser.parse(sHtmlContent, sPatternTab)
    if aResultTab[0]:
        sPattern = '<li>.+?href="(.+?)".+?class="(fsctab|fstab).+?<\/i>(.+?) <'
        for aEntryTab in aResultTab[1]:
            if 'clear' in aEntryTab[0]:
                continue
            
            sLang = aEntryTab[1].strip().split(' ')[-1]
            aResult = oParser.parse(aEntryTab[2], sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    sClass = aEntry[1]
                    if 'fstab' in sClass:
                        continue
                    hasEpisode = True
                    sTitle = sMovieTitle + '(%s)' % (sLang)
                    sHosterUrl = aEntry[0]
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    if not hasEpisode:
        sPatternTab = 'fa-play-circle-o"></i> *(.+?) *</div>(.+?)</div></div>'
        aResultTab = oParser.parse(sHtmlContent, sPatternTab)
        if aResultTab[0]:
            sPattern = 'href="(.+?)".+?target="seriePlayer".+?<\/i>.+?(\d+)(.+?)<'
            for aEntryTab in aResultTab[1]:
                sLang = aEntryTab[0].strip()
                
                aResult = oParser.parse(aEntryTab[1], sPattern)
                if aResult[0]:
                    for aEntry in aResult[1]:
                        numEpisode = aEntry[1]
                        if sEpisode != numEpisode:
                            continue
                        
                        sLangEp = aEntry[2].strip().split(' ')[-1]
                        if 'VO' in sLangEp:
                            sLang = sLangEp
                            
                        sTitle = sMovieTitle + '(%s)' % (sLang)
                        sHosterUrl = aEntry[0]
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
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
            if 'FRENCH' not in aEntry[1] and 'VOSTFR' not in aEntry[1] and 'VOSTENG' not in aEntry[1]:
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
