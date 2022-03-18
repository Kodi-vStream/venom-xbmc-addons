# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#Il faut faire le code pour le nouvel hoster.
return False

import re
import base64
import time

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import Noredirection

# copie du site http://www.kaydo.ws/
# copie du site https://www.hds.to/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo (hdss.to)'
SITE_DESC = 'Site de streaming en HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'populaires/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'mieux-notes/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showMovieGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tv-series-z/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'sHowResultSearch'

UA = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'


def Decode(chain):
    try:
        chain = 'aHR' + chain
        chain = 'M'.join(chain.split('7A4c1Y9T8c'))
        chain = 'V'.join(chain.split('8A5d1YX84A428s'))
        chain = ''.join(chain.split('$'))

        return base64.b64decode(chain)
    except:
        return chain


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films et Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Par lettre)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Par lettre)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()

    liste = []
    liste.append(['#', URL_MAIN + 'letter/0-9/'])
    liste.append(['A', URL_MAIN + 'letter/a/'])
    liste.append(['B', URL_MAIN + 'letter/b/'])
    liste.append(['C', URL_MAIN + 'letter/c/'])
    liste.append(['D', URL_MAIN + 'letter/d/'])
    liste.append(['E', URL_MAIN + 'letter/e/'])
    liste.append(['F', URL_MAIN + 'letter/f/'])
    liste.append(['G', URL_MAIN + 'letter/g/'])
    liste.append(['H', URL_MAIN + 'letter/h/'])
    liste.append(['I', URL_MAIN + 'letter/i/'])
    liste.append(['J', URL_MAIN + 'letter/j/'])
    liste.append(['K', URL_MAIN + 'letter/k/'])
    liste.append(['L', URL_MAIN + 'letter/l/'])
    liste.append(['M', URL_MAIN + 'letter/m/'])
    liste.append(['N', URL_MAIN + 'letter/n/'])
    liste.append(['O', URL_MAIN + 'letter/o/'])
    liste.append(['P', URL_MAIN + 'letter/p/'])
    liste.append(['Q', URL_MAIN + 'letter/q/'])
    liste.append(['R', URL_MAIN + 'letter/r/'])
    liste.append(['S', URL_MAIN + 'letter/s/'])
    liste.append(['T', URL_MAIN + 'letter/t/'])
    liste.append(['U', URL_MAIN + 'letter/u/'])
    liste.append(['V', URL_MAIN + 'letter/v/'])
    liste.append(['W', URL_MAIN + 'letter/w/'])
    liste.append(['X', URL_MAIN + 'letter/x/'])
    liste.append(['Y', URL_MAIN + 'letter/y/'])
    liste.append(['Z', URL_MAIN + 'letter/z/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
    return


def showMovieGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(siteUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent, '"AAIco-movie_creation">Genres</label>', '</div>')
    sPattern = 'data-val="([^"]+)" data-value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sGenre = aEntry[0]
            if sGenre in ('random', 'Uncategorized'):
                continue
            sFilter = aEntry[1]
            sUrl = siteUrl + '?s=trfilter&trfilter=1&geners%5B%5D=' + sFilter

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sGenre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if URL_MAIN + 'letter/' in sUrl:
        sPattern = '<td class="MvTbImg">.+?href="([^"]+).+?src="([^"]*).+?class="MvTbTtl.+?<strong>([^<]*).+?<td>([^<]*).+?Qlty">([^<]+).+?<td>([^<]*)'
    else:
        sPattern = 'class="TPost C".+?href="([^"]+).+?src="([^"]*).+?Title">([^<]+).+?(?:|Year">([^<]*).+?)(?:|Qlty">([^<]*).+?)Description"><p>([^<]+)'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # réécriture pour prendre les séries dans le menu des genres
    # sHtmlContent = sHtmlContent.replace('<span class="Qlty">TV</span></div><h3', '</div><h3')

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

            siteUrl = aEntry[0]
            sThumb = re.sub('/w\d+', '/w342', aEntry[1])
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sQual = aEntry[4]
            sDesc = aEntry[5]
            if sYear.lower() == 'unknown':
                sYear = ''
            if sQual.lower() == 'unknown':
                sQual = ''

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/serie/' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSaisonEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+?)</a><a class="next page-numbers" href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def ShowSaisonEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="Title AA-Season.+?>Season <span>([^<]+)</span>|class="MvTbImg">.+?img src.+?["|;]([^\"]+?)["|;].+?href="([^"]+)">([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]Saison: ' + aEntry[0] + '[/COLOR]')
            else:
                sThumb = re.sub('/w\d+', '/w342', aEntry[1], 1)
                if sThumb.startswith('//'):
                    sThumb = 'https:' + sThumb
                sUrl2 = aEntry[2]
                sTitle = aEntry[3]

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    # UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Recuperer variable pour url de base
    sPattern = 'trembed=(\d+).+?trid=(\d+).+?trtype=(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        list_site_film = []
        for aEntry in aResult[1]:

            site = URL_MAIN + "?trembed=" + aEntry[0] + "&trid=" + aEntry[1] + "&trtype=" + aEntry[2]
            if aEntry[2] == '1':
                if site not in list_site_film:
                    list_site_film.append(site)
                else:
                    continue  # inutile de faire des requetes identiques pour les films

            oRequestHandler = cRequestHandler(site)
            sHtmlContent = oRequestHandler.request()

            slug = re.search('"Video".+?src=".+?v=(.+?)"', sHtmlContent).group(1)

            sHosterUrl = "https://geoip.redirect-ads.com/?v=" + slug

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def decode(t):
    a = len(t) - 1
    trde = ''
    while a >= 0:
        trde = trde + t[a]
        a -= 1

    return trde
