# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager
from resources.lib.parser import cParser
from resources.lib.util import QuotePlus, cUtil

SITE_IDENTIFIER = 'mesfilms'
SITE_NAME = 'Mes Films'
SITE_DESC = 'Mes Films - Films en streaming HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'

URL_SEARCH = (URL_MAIN + '?s=', 'showSearchResult')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'evaluations/?get=movies', 'showMovies')
MOVIE_CLASS = (URL_MAIN + 'films-classiques/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
# MOVIE_LIST = (True, 'showList')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASS[1], 'Films Classiques', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    # ne fonctionne plus sur le site
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + QuotePlus(sSearchText)
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Action & aventure', 'action-adventure'], ['Animation', 'animation'],
             ['Aventure', 'aventure'], ['Comédie', 'comedie'], ['Crime', 'crime'], ['Documentaire', 'documentaire'],
             ['Drame', 'drame'], ['Etranger', 'etranger'], ['Familial', 'familial'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Horreur', 'horreur'], ['Musique', 'musique'],
             ['Mystère', 'mystere'], ['News', 'news'], ['Policier', 'policier'], ['Reality', 'reality'],
             ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Science Fiction & Fantastique', 'science-fiction-fantastique'], ['Soap', 'soap'], ['Talk', 'talk'],
             ['Téléfilm', 'telefilm'], ['Thriller', 'thriller'], ['War & Politics', 'war-politics'],
             ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showList():
    oGui = cGui()

    liste = [['09', '09'], ['A', 'a'], ['B', 'b'], ['C', 'c'], ['D', 'd'], ['E', 'e'], ['F', 'f'], ['G', 'g'],
             ['H', 'h'], ['I', 'i'], ['J', 'j'], ['K', 'k'], ['L', 'l'], ['M', 'm'], ['N', 'n'], ['O', 'o'], ['P', 'p'],
             ['Q', 'q'], ['R', 'r'], ['S', 's'], ['T', 't'], ['U', 'u'], ['V', 'v'], ['W', 'w'], ['X', 'x'], ['Y', 'y'],
             ['Z', 'z']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '?letter=true&s=title-' + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1963, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchResult(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    sUrl = sSearch

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'animation-2".+?href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?(?:|year">([^<]*)<.+?)<p>(.*?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = re.sub('/w\d+/', '/w342/', aEntry[1], 1)  # meilleure qualité
            sTitle = aEntry[2].replace(': Season', ' Saison')
            sYear = aEntry[3]
            if sYear != '':  # on ne récupere que l'année
                sYear = re.search('(\d{4})', sYear).group(1)
            sDesc = aEntry[4]

            # on ne recherche que des films même si séries et animés disponible
            if '/film/' not in sUrl:
                continue

            # Filtrer les résultats
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)  # permet à addMovie d'afficher l'année en Meta

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'poster"><img src="([^"]+)" alt="([^"]+).+?(?:|quality">([^<]+).+?)href="([^"]+).+?<span>([^<]+).+?(texto">(.*?)<|</article)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = re.sub('/w\d+/', '/w342/', aEntry[0], 1)  # ameliore la qualité
            sTitle = aEntry[1]
            sQual = aEntry[2]
            sUrl2 = aEntry[3]
            sYear = aEntry[4]
            sDesc = ''  # cas ou la sdesc n'est pas presente
            if aEntry[6]:
                sDesc = aEntry[6]
            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="pagination"><span>Page.+?de ([^<]+).+?href="([^"]+)"><i id=.nextpagination'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = 'og:description" content="(.+?)" /><meta'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = "type='([^']+)' data-post='([^']+)' data-nume='([^']+).+?title'>([^<]+)</span>\s*<span class='server'>([^<]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sType = aEntry[0]
            sPost = aEntry[1]
            sNume = aEntry[2]
            sQual = aEntry[3]
            sHost = re.sub('\.\w+', '', aEntry[4]).capitalize()
            if 'Youtube' in sHost:
                continue

            sTitle = ('%s [%s] [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sType', sType)
            oOutputParameterHandler.addParameter('sPost', sPost)
            oOutputParameterHandler.addParameter('sNume', sNume)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sType = oInputParameterHandler.getValue('sType')
    sPost = oInputParameterHandler.getValue('sPost')
    sNume = oInputParameterHandler.getValue('sNume')

    # trouve la vraie url
    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.request()
    sUrl2 = oRequestHandler.getRealUrl() + 'wp-admin/admin-ajax.php'

    oRequestHandler = cRequestHandler(sUrl2)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    oRequestHandler.addParameters('action', 'doo_player_ajax')
    oRequestHandler.addParameters('type', sType)
    oRequestHandler.addParameters('post', sPost)
    oRequestHandler.addParameters('nume', sNume)
    sHtmlContent = oRequestHandler.request()
    sPattern = "(http[^'\"]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
