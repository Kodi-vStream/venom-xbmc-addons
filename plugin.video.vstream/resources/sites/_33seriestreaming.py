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

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"

SITE_IDENTIFIER = '_33seriestreaming'
SITE_NAME = '33 Séries'
SITE_DESC = 'Films et Séries en streaming VF et VOSTFR'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

# Sous menus
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = (URL_MAIN, 'showMovieAlpha')

SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (URL_MAIN, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_LIST = (URL_MAIN, 'showSerieAlpha')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&cat=1&story=', FUNCTION_SEARCH)
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&cat=2&story=', FUNCTION_SEARCH)


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
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl += sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieAlpha():
    import string

    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    listalpha = ['1']
    listalpha.extend(list(string.ascii_lowercase))
    for alpha in listalpha:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'catalog/' + alpha + '&cat=1')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + str(alpha).upper() + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieAlpha():
    import string

    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    listalpha = ['1']
    listalpha.extend(list(string.ascii_lowercase))
    for alpha in listalpha:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'catalog/' + alpha + '&cat=2')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + str(alpha).upper() + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'familial'],
             ['Fantastique', 'fantastique'], ['Histoire', 'histoire'], ['Horreur', 'horreur'], ['Musique', 'musique'],
             ['Mystère', 'mystere'], ['Thriller', 'thriller'], ['Téléfilm', 'telefilm'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Horreur', 'horreur'],
             ['Judiciaire', 'judiciare'], ['Musique', 'musical'], ['Policier', 'policier'], ['Romance', 'romance'],
             ['Science-Fiction', 'science-fiction']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/' + sUrl + '-s/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
#    import datetime
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1930, 2023)): #  pas de films apres 2022 int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + sYear + '&cat=1')
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
#    import datetime
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1930, 2023)):  #int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + sYear  + '&cat=2')
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sYear = oInputParameterHandler.getValue('sYear')

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20 ', '+')
    sPattern = 'grid-item" href="([^"]+).+?-src="([^"]+).+?nowrap">([^<]+)'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

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
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            searchSerie = False
            if 'cat=1' in sUrl and not 'uploads' in sThumb:
                continue
            if 'cat=2' in sUrl:
                if not 'images' in sThumb:
                    continue
                searchSerie = True
            
            sTitle = aEntry[2]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/series' in sUrl2 or '/series' in sUrl or searchSerie:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            oOutputParameterHandler = cOutputParameterHandler()
            if '&cat=1' in sUrl:
                sNextPage = sNextPage.replace('/page', '&cat=1/page')
            elif '&cat=2' in sUrl:
                sNextPage = sNextPage.replace('/page', '&cat=2/page')
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'id="pagination".+?\d+</span>.<a href="([^"]+)">(\d+)(</a> *</div|<.+?(\d+)</a> *</div)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        nextPage = aResult[1][0]
        sNextPage = nextPage[0]
        sNumberNext = nextPage[1]
        sNumberMax = nextPage[3]
        if not sNumberMax:
            sNumberMax = sNumberNext
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging
    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = 'fsynopsis"><p>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = re.sub('Regarder ' + sMovieTitle + ' en streaming FR et VOSTFR HD ', '', aResult[1][0])
    except:
        pass

    sPattern = 'grid-item" href="([^"]+).+?src="([^"]+).+?season">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[1]
            sSais = aEntry[2]

            sTitle = sMovieTitle + ' ' + sSais

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'sect__content d-grid'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)" class="episode_btn">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sEp = aEntry[1]

            sTitle = sMovieTitle + ' ' + sEp

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')
    isSerie = '-episode.html' in sUrl

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    sHtmlContent = oRequestHandler.request()

    if not sDesc:
        # récupération du Synopsis pour les films
        sDesc = ''
        try:
            sPattern = 'fsynopsis"><p>([^<]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = re.sub('Regarder gratuit Film ' + sMovieTitle + ' en streaming VF ou VOSTFR Complet ',
                               '', aResult[1][0])
        except:
            pass

    if isSerie:  # episode d'une série
        sPattern = '<li class="ser_pl" data-id="(\d+)" data-name="([^"]+)".+?(\.png|\.ico)">([^<]+).+?\/([^\/]+)\.png'
        sUrl2 = URL_MAIN + 'engine/ajax/Season.php'
        mod = 'xfield_ajaxs'
    else:
        sPattern = '<li class="nopl" data-id="(\d+)" data-name="([^"]+)".+?(\.png|\.ico)">([^<]+).+?\/([^\/]+)\.png'
        sUrl2 = URL_MAIN + 'engine/ajax/getxfield.php'
        mod = 'xfield_ajax'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            dataId = aEntry[0]
            dataName = aEntry[1]
            sHost = aEntry[3]#.capitalize()
            sLang = aEntry[4]
            pdata = {'mod': mod, 'id': dataId, 'name' :  dataName}
            if not cHosterGui().checkHoster(sHost):
                continue

            sDisplayTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang.upper(), sHost.capitalize())

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('pdata', str(pdata))
            oGui.addLink(SITE_IDENTIFIER, 'hostersLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # pas de moyen d'orientation depuis showMovies pour les séries en passant par showAlpha
    if not aResult[0]:
        showSaisons()

    oGui.setEndOfDirectory()


def hostersLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    referer = oInputParameterHandler.getValue('referer')
    pdata = oInputParameterHandler.getValue('pdata')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

    import ast
    pdata = ast.literal_eval(pdata)
    oRequest.addMultipartFiled(pdata)

    sHtmlContent = oRequest.request()

    sPattern = '(http[^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
