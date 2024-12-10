# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import json

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'french_stream'
SITE_NAME = 'French Stream'
SITE_DESC = 'Films & séries'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = ('xfsearch/genre-1/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = ('xfsearch/version-film/VOSTFR/', 'showMovies')

SERIE_NEWS = ('xfsearch/version-serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VOSTFRS = ('s-tv/s-vostfr/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = ('index.php?do=search', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'VOSTFR', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'VOSTFR', 'vostfr.png', oOutputParameterHandler)

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
        liste.append([igenre.capitalize().replace('+',' '), 'xfsearch/genre-1/' + igenre + '/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

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
        oOutputParameterHandler.addParameter('siteUrl', sUrl + '-/')
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

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
    else:
        if '-serie' in sUrl or 'serie-' in sUrl or '-drama' in sUrl or 's-tv' in sUrl:
            bSearchSerie = True
        oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
        sHtmlContent = oRequestHandler.request()
                    
    sPattern = 'with-mask" href="([^"]+).+?src="([^"]*).+?title">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        if bSearchSerie:
            series = set()  # une seule fois la série
            
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:
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
                sTitle = sTitle.split('- Saison')[0].strip()
                cleanTitle = cUtil().CleanName(sTitle)
                if cleanTitle in series:
                    continue
                series.add(cleanTitle)

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if bSearchSerie:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)


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
        result = re.search('/([0-9]+)/', sNextPage)
        sNumberNext = result.group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if not '/page/' in sUrl:
        sHtmlContent = cRequestHandler(sUrl).request()
        aResult = oParser.parse(sHtmlContent, '<a href="/(xfsearch/s-\d+)')
        sUrl = URL_MAIN + aResult[1][0] if aResult[0] else None

    if sUrl:
        sHtmlContent = cRequestHandler(sUrl).request()
        
        # url    title    thumb
        sPattern = 'img-box with-mask" href="([^"]+)" alt="([^"]+)"> *<img src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for saison in aResult[1][::-1]:
                sUrl = saison[0]
                sDisplayTitle = saison[1]
                sThumb = saison[2]

                # certaines séries sont mal rangées, voir Breaking Bad
                if not oUtil.CheckOccurence(sMovieTitle, sDisplayTitle.split('- Saison')[0]):
                    continue
    
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

            sNextPage, sPaging = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addNext(SITE_IDENTIFIER, 'showSaisons', 'Page ' + sPaging, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
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
        sDesc = cleanDesc(aResult[1][0])

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
        sPattern = '<li>.+?href="(.+?)".+?class="(fsctab|fstab).+?<\/i>(.+?) *<'
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
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHtmlContent = cRequestHandler(sUrl).request()
    sHtmlContent = cParser().parse(sHtmlContent, 'const playerUrls = (.+?);')

    if sHtmlContent[0]:
        hosters = json.loads(sHtmlContent[1][0])

        if len(hosters):
            for hosterName, links in hosters.items():
                liens = set()
                for sLang in sorted(links):
                    if 'Default' in sLang:
                        continue    #  le lien par défaut est ensuite reproposé avec la langue
                    
                    # suppression des liens vide ou en en doublon
                    link = links[sLang]
                    if not link:
                        continue
                    if link in liens:
                        continue
                    liens.add(link)
                    
                    sDisplayTitle = '%s (%s)' % (sMovieTitle, sLang)
        
                    oHoster = cHosterGui().checkHoster(hosterName)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, link, sThumb)

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
