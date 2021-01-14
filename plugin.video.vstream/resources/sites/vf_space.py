# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'vf_space'
SITE_NAME = 'VF.Space'
SITE_DESC = 'Films, Séries et Mangas Gratuit en streaming'

URL_MAIN = 'https://vww.vfspace.me/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0] + '&subaction=search&titleonly=3&catlist%5B%5D=9&story=', FUNCTION_SEARCH)
URL_SEARCH_SERIES = (URL_SEARCH[0] + '&subaction=search&catlist%5B%5D=10&catlist%5B%5D=12&catlist%5B%5D=13&story=', FUNCTION_SEARCH)

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'xfsearch/genre/Action/'])
    liste.append(['Animation', URL_MAIN + 'xfsearch/genre/Animation/'])
    liste.append(['Aventure', URL_MAIN + 'xfsearch/genre/Aventure/'])
    liste.append(['Biopic', URL_MAIN + 'xfsearch/genre/Biopic/'])
    liste.append(['Comédie', URL_MAIN + 'xfsearch/genre/Comedie/'])
    liste.append(['Comédie musicale', URL_MAIN + 'xfsearch/genre/Comedie%20musicale/'])
    liste.append(['Comédie dramatique', URL_MAIN + 'xfsearch/genre/Comedie%20dramatique/'])
    liste.append(['Documentaire', URL_MAIN + 'xfsearch/genre/Documentaire/'])
    liste.append(['Drame', URL_MAIN + 'xfsearch/genre/Drame/'])
    liste.append(['Divers', URL_MAIN + 'xfsearch/genre/Divers/'])
    liste.append(['Horreur', URL_MAIN + 'xfsearch/genre/Epouvante-horreur/'])
    liste.append(['Famille', URL_MAIN + 'xfsearch/genre/Famille/'])
    liste.append(['Fantastique', URL_MAIN + 'xfsearch/genre/Fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'xfsearch/genre/Guerre/'])
    liste.append(['Policier', URL_MAIN + 'xfsearch/genre/Policier/'])
    liste.append(['Romance', URL_MAIN + 'xfsearch/genre/Romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'xfsearch/genre/Science%20fiction/'])
    liste.append(['Thriller', URL_MAIN + 'xfsearch/genre/Thriller/'])
    liste.append(['Western', URL_MAIN + 'xfsearch/genre/Western/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    for i in reversed(range(2015, 2021)):  # avant 2015 hosts HS
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'xfsearch/year/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    nextPageSearch = oInputParameterHandler.getValue('nextPageSearch')

    if nextPageSearch:
        sSearch = sUrl

    if sSearch or 'do=search' in sUrl:
        if sSearch:
            sUrl = sSearch
        oRequest = cRequestHandler(sUrl + '&search_start=' + str(nextPageSearch))
        sHtmlContent = oRequest.request()
    else:
        oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
        sHtmlContent = oRequestHandler.request()

    # reprise du fichier html pour récupérer les films et les séries en cas d'absence d'argument
    sHtmlContent = re.sub('<li class="red">\d+</li>', '', sHtmlContent)
    sHtmlContent = sHtmlContent.replace(' class="red"', '')

    sPattern = 'short-poster" href="([^"]+)" title="([^"]+).+?(?:|<li>([^<]*)</li.+?)class="white">([^<]*)<.+?data-src="([^"]*)'
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

            sUrl2 = aEntry[0]
            sTitle = aEntry[1].replace('Regarder', '').replace('en ligne gratuitement', '').replace('Saion', 'Saison')\
                              .replace(' - Saison', ' Saison')
            sQual = aEntry[2]
            sYear = aEntry[3]
            sThumb = aEntry[4]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            # on test aussi sUrl car parfois Saion au lieu de Saison dans sUrl2
            if '/series/' in sUrl or 'serie' in sUrl2 or 'saison' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = '<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\);'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSearch)
                oOutputParameterHandler.addParameter('nextPageSearch', aResult[1][0])
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                number = re.search('page/([0-9]+)', sNextPage).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

    if nextPageSearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()


# Pas habituel mais compatible pour gérer plusieurs pages lors d'une recherche
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="page_next"(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] and 'href' in aResult[1][0]:
        sPattern = 'href="(.+?)"'
        aResult = oParser.parse(aResult[1][0], sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
    return False


def showEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sPattern = '<div class="full-text".+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]

    sHtmlContent = oParser.abParse(sHtmlContent, 'class="movie-tabs">', 'similaires</h3>')

    sPattern = 'button class="llien">Lien([^<]+)</button>|<a title=.+?target="seriePlayer" data-id="([^"]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if aEntry[0]:  # affichage de l'episode
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl2 = aEntry[1]
                if sUrl2.startswith('/'):
                    sUrl2 = URL_MAIN[:-1] + aEntry[1]

                sLang = re.sub('lecteur (\d+)', '', aEntry[2]).upper().replace(' ', '')
                sTitle = sMovieTitle + '(' + sLang + ')'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequest = cRequestHandler(sUrl.replace('https', 'http'))
    sHtmlContent = oRequest.request()

    sDesc = ''
    sPattern = '<div class="full-text".+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = re.sub('.+? : ', '', aResult[1][0])

    sPattern = '<a title="([^"]+)" target="seriePlayer" data-id="([^"]+)">([^<]+)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl2 = aEntry[1]
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN[:-1] + aEntry[1]  # ou a voir https://4kvfsplayer.xyz

            # On ne propose que les hosts qu'on sait décoder
            sHost = aEntry[2].replace(' ', '').capitalize()
            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sLang = aEntry[0][-2:]
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)  # utilisé pour les metadata
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:66.0) Gecko/20100101 Firefox/66.0')
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Referer', URL_MAIN)

    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        sHosterUrl = aResult[1][0]
        if 'https://woof.tube' in sHosterUrl:
            sHosterUrl = sHosterUrl.replace('https://woof.tube', 'https://verystream.com')

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
