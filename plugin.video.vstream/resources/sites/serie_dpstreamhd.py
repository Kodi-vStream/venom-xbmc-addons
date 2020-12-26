# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 22 https://serie.dpstreamhd.com/

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress # ,VSlog


SITE_IDENTIFIER = 'serie_dpstreamhd'
SITE_NAME = 'Dpstream HD'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = 'https://serie.dpstreamhd.com/'
URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

MOVIE_VIEWS = (URL_MAIN + 'box-office', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series-en-streaming', 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuSeries')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les plus vus)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les plus vus)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'news.png', oOutputParameterHandler)

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
    # https://serie.dpstreamhd.com/categories/romance
    # recherche nulle war-politics ,soap, kids ,talk ,news ,science-fiction-fantastique
    listegenre = ['action ', 'action-adventure ', 'animation', 'aventure', 'comedie', 'crime', 'documentaire', 'drame ', 'familial'
                , 'fantastique', 'guerre', 'histoire', 'horreur', 'musique', 'Musical', 'mystere ', 'reality', 'romance', 'science-fiction'
                , 'telefilm', 'thriller', 'western']

    url1g = URL_MAIN + 'categories/'

    for igenre in listegenre:
        liste.append([igenre.capitalize(), url1g + igenre])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        bvalid, stoken, scookie = GetTokens()
        if bvalid:
            pdata = '_token=' + stoken + '&search=' + sSearch
            sUrl = URL_MAIN + 'search'

            oRequestHandler = cRequestHandler(sUrl )
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
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

    # thumb title note ref
    sPattern = '<article class="post.+?src=(.+?)\.jpg.*?title="([^"]+).+?svg><.i>([^<]+).+?href="([^"]+)'  

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

            sYear = ''
            sDesc = ''
            sThumb = aEntry[0] + '.jpg' # bug parfois pas de jpg  à revoir ?
            sTitle = cleanDesc(aEntry[1])
            sDesc = 'note :' + aEntry[2]
            sUrl2 = aEntry[3]
            sDisplayTitle = sTitle

            if 'http' not in sUrl2:  # search
                sUrl2 = URL_MAIN[:-1] + sUrl2

            # VSlog('url = ' + sUrl2);VSlog('title = '+ sTitle);VSlog('thumb = '+ sThumb);VSlog('desc'+ sDesc )

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '-serie-' not in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSXE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bNextPage, urlNextpage, sPagination = __checkForNextPage(sHtmlContent, sUrl)
        if (bNextPage != False):

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlNextpage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] ' + sPagination  + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent, sUrl):

    oParser = cParser()
    urlNextpage = ''
    snumberNext = ''
    sNumberMax = ''
    bfailed1 = False
    sPagination = ''
    if 'next page-nav' not in sHtmlContent:
        return False, 'none', 'none'
    # on tente de prendre le n max et l'url next ainsi que le numero de page
    sPattern = '(\d+)<.a><a\s+href="([^"]+).+?class="next page-nav">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        urlNextpage = aResult[1][0][1]
        sNumberMax = aResult[1][0][0]
        try:
            snumberNext = re.search('page=([0-9]+)', urlNextpage).group(1)
        except:
            bfailed1 = True
            pass  
    # sinon on se contente du next page
    if (aResult[0] == False or bfailed1):
        sPattern = 'href="([^"]+)" class="next page-nav'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            urlNextpage = aResult[1][0] # minimum requis
            try:
                snumberNext = re.search('page=([0-9]+)', urlNextpage).group(1)
            except:
                pass
    if snumberNext:
        sPagination = 'Page ' + str(snumberNext)
        if sNumberMax:
            sPagination = sPagination + '/' + sNumberMax
    if urlNextpage:
        return True, urlNextpage, sPagination

    return False, 'none', 'none'


def showSXE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sYear = ''
    sPattern = 'année<.span>([^<]+).+?résume de.+?<br>([^<]+)'
    aResult_ = oParser.parse(sHtmlContent, sPattern)
    if (aResult_[0] == True):
        aresult = aResult_[1][0]
        sYear = aresult[0]
        sDescColor = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aresult[1])
        if  sDesc:
            sDesc = sDesc + '\r\n' + sDescColor
        else:
            sDesc = sDescColor

    sPattern = 'class="numep">([^<]+).+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    list_saison = []

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if 'x' in aEntry[0]:
                # class="numep">1x13<
                saison, episode = aEntry[0].split('x')
                if saison not in list_saison:
                    list_saison.append(saison )
                    sSaison = 'Saison ' + saison
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]' + sSaison + '[/COLOR]')

                sUrl2 = aEntry[1]

                sDisplayTitle = sMovieTitle + ' Episode' + episode

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sDisplayTitle', sDisplayTitle)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sDisplayTitle = oInputParameterHandler.getValue('sDisplayTitle')

    if sDisplayTitle:
        sMovieTitle = sDisplayTitle

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sYear = ''
    sPattern = 'année<.span>([^<]+).+?résume de.+?<br>([^<]+)'
    aResult_ = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'no description'
    if (aResult_[0] == True):
        sDesc = ''
        aresult = aResult_[1][0]
        sYear = aresult[0]
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aresult[1])

    sPattern = 'data-url="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            skey = aEntry[0]
            sHost = aEntry[1]

            sUrl2 = URL_MAIN + 'll/captcha?hash=' + skey
            sTitle = sMovieTitle
            if sYear:
                sTitle = sTitle + '(' + sYear + ')'

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

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
    sHeader = oRequestHandler.getResponseHeader()

    cook = ''
    token = ''
    XSRF_TOKEN = ''
    site_session = ''

    sHeader = oRequestHandler.getResponseHeader()
    sPattern = 'name=_token.+?value="([^"]+).+?class="filter-options'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        return False, 'none', 'none'

    if (aResult[0] == True):
        token = aResult[1][0]

    sPattern = 'XSRF-TOKEN=([^;]+).+?dpstreamhd_session=([^;]+)'
    aResult = oParser.parse(sHeader, sPattern)

    if (aResult[0] == False):
        return False, 'none', 'none'

    if (aResult[0] == True):
        XSRF_TOKEN = aResult[1][0][0]
        site_session = aResult[1][0][1]

    cook = 'XSRF-TOKEN=' + XSRF_TOKEN + '; dpstreamhd_session=' + site_session + ';'
    return True, token, cook


def cleanDesc(sdesc):
    list_comment = [
                  'Voir film '
                , 'en streaming'
                , 'Voir Serie '
                    ] 
    for s in list_comment:
        sdesc = sdesc.replace(s, '')

    return sdesc
