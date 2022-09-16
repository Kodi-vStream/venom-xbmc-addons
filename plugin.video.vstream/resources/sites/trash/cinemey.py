# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 27 https://cinemey.com/
return False  # HS voir https://cinemay.cc/ memes films et series

import re
import xbmc
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'cinemey'
SITE_NAME = 'Cinemey'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = 'https://cinemey.com/'
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'top-films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_VIEWS = (URL_MAIN + 'classement-box-office-film', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'les-series-en-streaming', 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuSeries')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les plus vus)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    # https://cinemey.com/categorie/romance
    # Aucun résultats war-politics, soap, kids, talk, news, science-fiction-fantastique, reality, action-adventure
    listegenre = ['action', 'animation', 'aventure', 'comedie', 'crime', 'documentaire', 'drame', 'familial',
                  'fantastique', 'guerre', 'histoire', 'horreur', 'musique', 'Musical', 'mystere', 'romance',
                  'science-fiction', 'telefilm', 'thriller', 'western']

    url1g = URL_MAIN + 'categorie/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()
    # https://cinemey.com/annee/2020
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(2001, 2022)):  # pas grand chose 32 - 90
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:

        bvalid, stoken, scookie = GetTokens()
        if bvalid:
            pdata = '_token=' + stoken + '&search=' + sSearch
            sUrl = URL_MAIN + 'search'
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
            oRequestHandler.addHeaderEntry('Cookie', scookie)
            oRequestHandler.addParametersLine(pdata)
            oRequestHandler.request()

            # constatation : on est oblige de faire 2 requetes
            # dans le cas ou le mot recherché est composé ?
            xbmc.sleep(500)
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('Cookie', scookie)
            oRequestHandler.addParametersLine(pdata)

            sHtmlContent = oRequestHandler.request()

        else:
            oGui.addText(SITE_IDENTIFIER)
            return

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # title img year surl
    sPattern = '<article class.+?data-url.+?title="([^"]*).+?img src=([^\s]*).+?year">([^<]+).+?href="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sDesc = ''
            sTitle = aEntry[0]
            sThumb = aEntry[1]
            sYear = aEntry[2]
            sUrl2 = aEntry[3]
            sDisplayTitle = sTitle + '(' + sYear + ')'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if sSearch:
                oGui.addLink(SITE_IDENTIFIER, 'showSelectType', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)
            elif SERIE_NEWS[0] in sUrl:
                sDisplayTitle = sTitle
                oGui.addTV(SITE_IDENTIFIER, 'showSXE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+?)</a><a href="([^"]+?)" class="next page-numbers'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSelectType():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sDesc = ''
    oParser = cParser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oOutputParameterHandler.addParameter('sYear', sYear)

    if 'class="num-epi">' in sHtmlContent:

        oGui.addTV(SITE_IDENTIFIER, 'showSXE', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
        oGui.addMovie(SITE_IDENTIFIER, 'showLink', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSXE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    sPattern = 'class="num-epi">([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    list_saison = []

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'x' in aEntry[0]:
                # class="numep">1x13<
                saison, episode = aEntry[0].split('x')
                if saison not in list_saison:
                    list_saison.append(saison)
                    sSaison = 'Saison ' + saison
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]' + sSaison + '[/COLOR]')

                sUrl2 = aEntry[1]
                sTitle = sMovieTitle + ' ' + sSaison + ' Episode' + episode

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = 'class="description">.*?<br>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # dans le cas d'une erreur si serie (pas de controle année et genre)
    if False and 'class="num-epi">' in sHtmlContent and 'episode' not in sUrl:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addTV(SITE_IDENTIFIER, 'showSXE', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
        return

    sPattern = 'data-url="([^"]+).+?server.+?alt="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oHosterGui = cHosterGui()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sKey = aEntry[0]
            sHost = aEntry[1].replace('www.', '').replace('embed.mystream.to', 'mystream')
            sHost = re.sub('\.\w+', '', sHost).capitalize()

            oHoster = oHosterGui.checkHoster(sHost)
            if not oHoster:
                continue
            
            sLang = aEntry[2].upper()
            sUrl2 = URL_MAIN + 'll/captcha?hash=' + sKey

            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.*?src=([^\s]+)'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def GetTokens():
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = '<nav id="menu.+?name=_token.+?value="([^"]+).+?<div class="typeahead'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        return False, 'none', 'none'

    if (aResult[0] == True):
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?cinemay_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if (aResult[0] == False):
        return False, 'none', 'none'

    if (aResult[0] == True):
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; cinemay_session=' + site_session + ';'
    return True, token, cook


def cleanDesc(sDesc):
    list_comment = ['Voir film ', 'en streaming', 'Voir Serie ']
    for s in list_comment:
        sDesc = sDesc.replace(s, '')

    return sDesc
