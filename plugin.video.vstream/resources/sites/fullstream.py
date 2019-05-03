#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

import urllib2, re

SITE_IDENTIFIER = 'fullstream'
SITE_NAME = 'FullStream'
SITE_DESC = 'Films, Séries et Mangas Gratuit en streaming sur Full stream'

#URL_MAIN = 'https://vf.full-stream.cc/'
URL_MAIN = 'https://w1.full-stream.cc/'

URL_SEARCH = (URL_MAIN + 'wp-json/dooplay/search/?keyword=', 'AlphaDisplay')
URL_SEARCH_MOVIES = (URL_MAIN + 'wp-json/dooplay/search/?keyword=', 'AlphaDisplay')
URL_SEARCH_SERIES = (URL_MAIN + 'wp-json/dooplay/search/?keyword=', 'AlphaDisplay')

FUNCTION_SEARCH = 'AlphaDisplay'

MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (URL_MAIN + 'film', 'AlphaSearch')

SERIE_NEWS = (URL_MAIN + 'episode', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix', 'showMovies')
SERIE_LIST = (URL_MAIN + 'serie', 'AlphaSearch')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Films (Liste) ', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NETFLIX[1], 'Séries Netflix', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste) ', 'az.png', oOutputParameterHandler)



    oGui.setEndOfDirectory()

def showSearch():

    oGui = cGui()
    nonce = get_nonce()
    if not nonce == False:
        sSearchText = oGui.showKeyBoard()
        if (sSearchText != False):
            sUrl = URL_MAIN + 'wp-json/dooplay/search/?keyword=' + sSearchText + '&nonce=' + nonce
            AlphaDisplay(sUrl)
            oGui.setEndOfDirectory()
            return

def get_nonce(sHtmlContent = ''):
    oParser = cParser()
    if not sHtmlContent:
        oRequestHandler = cRequestHandler(URL_MAIN)
        sHtmlContent = oRequestHandler.request()

    sPattern1 = '"nonce":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern1)
    if (aResult[0] == True):
        return aResult[1][0]
    else:
        return False

def AlphaSearch():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'serie' in sUrl:
        type = 'tvshows'
    else:
        type = 'movies'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    nonce = get_nonce()
    if not nonce == False:
       sPattern = '<a class="lglossary" data-type=".+?" data-glossary="([^"]+)">([^<]+)<\/a>'
       aResult = oParser.parse(sHtmlContent, sPattern)
       if (aResult[0] == True):
            for aEntry in aResult[1]:
                sLetter = aEntry[1]
                sUrl = URL_MAIN + 'wp-json/dooplay/glossary/?term=' + aEntry[0].replace('#', '09') + '&nonce=' + nonce + '&type=' + type

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'az.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def AlphaDisplay(sSearch = ''):
    import json
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sSite = oInputParameterHandler.getValue('site')#globalsearch

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if not '&nonce=' in sUrl:#globalsearch
        sUrl = sUrl + '&nonce=' + get_nonce()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    content = json.loads(sHtmlContent)
    for x in content:
        sTitle = content[x]['title'].encode('utf-8')
        sUrl2 = content[x]['url']
        sThumb = content[x]['img'].replace('w92', 'w342')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        if '/serie/' in sUrl2:
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '',oOutputParameterHandler)
        else:
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSite == 'globalSearch':#globalsearch
        oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie'] )
    liste.append( ['Crime', URL_MAIN + 'genre/crime'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame'] )
    liste.append( ['Horreur', URL_MAIN + 'genre/horreur'] )
    liste.append( ['Familial', URL_MAIN + 'genre/familial'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre'] )
    liste.append( ['Histoire', URL_MAIN + 'genre/histoire'] )
    liste.append( ['Mystère', URL_MAIN + 'genre/mystere'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance'] )
    liste.append( ['Science Fiction & Fantastique', URL_MAIN + 'genre/science-fiction-fantastique'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genre/science-fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-src="([^"]+)" alt="([^"]+)".+?(?:|<span class="quality">([^<]+)</span>.+?)<div class="see">.+?<a href="([^"]+)"'

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

            sThumb = aEntry[0].replace('w185', 'w342')
            sTitle = aEntry[1]
            sQual = aEntry[2]
            sUrl2 = aEntry[3]

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif '/episode' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="current">.+?</span><a href=\'([^"]+)\''
    aResult = oParser.parse(sHtmlContent, sPattern)
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
    sPattern = '<div id="info".+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]

    sHtmlContent = oParser.abParse(sHtmlContent, '<h2>Seasons and episodes</h2>', '<h2>titres similaires</h2>')
    #recuperation des suivants
    sPattern = '<span class="title">([^<]+)<i>|<a href="([^"]+)"><img src=".+?">.+?<div class="numerando">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl2 = aEntry[1]
                SxE = re.sub('(\d+) - (\d+)', 'S\g<1>E\g<2>', aEntry[2])
                sTitle = sMovieTitle + SxE

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    cookie = oRequest.GetCookies().split(';')
    cooka = ''
    for i in cookie:
        if not 'wordpress' in i:
            cooka = cooka + i + '; '

    if '/film/' in sUrl:
        sPattern = '<a id="player-.+?" class="server.+?" data-post="([^"]+)" data-nume="([^"]+)">([^<]+)<.+?<img src=\'http.+?img/flags/(.+?).png\'>'
    else:
        sPattern = 'id="player-[^<>]+data-post="([^"]+)" data-nume="([^"]+)".*?"title">([^<]+)<\/*span.+?<img src=\'http.+?img\/flags\/(.+?).png\'>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    VSlog(aResult)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            sLang = aEntry[3].upper()
            sHost = aEntry[2].capitalize()

            data = 'action=doo_player_ajax&post=' + aEntry[0] + '&nume=' + aEntry[1]

            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sdata', data)
            oOutputParameterHandler.addParameter('sRef', sUrl)
            oOutputParameterHandler.addParameter('sCook', cooka)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    pdata = oInputParameterHandler.getValue('sdata')
    sRef = oInputParameterHandler.getValue('sRef')
    sCook = oInputParameterHandler.getValue('sCook')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0')
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequest.addHeaderEntry('Referer', sRef)
    oRequest.addHeaderEntry('Content-Length', len(pdata))
    oRequest.addHeaderEntry('Connection', 'keep-alive')
    oRequest.addHeaderEntry('Cookie', sCook)
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    cookie = oRequest.GetCookies().split(';')
    cooka = ''
    for i in cookie:
        if not 'wordpress' in i:
            cooka = cooka + i + '; '

    oParser = cParser()
    sPattern = "<iframe.+?src='([^']+)'"

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = URL_MAIN[:-1] + aResult[1][0]

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
        headers = {'User-Agent': UA, 'Referer': sRef, 'Cookie': cooka}
        req = urllib2.Request(sUrl, None, headers)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            return ''

        sHosterUrl = ''
        if not response.geturl() == sUrl:
            sHosterUrl = response.geturl()
        else:
            c = str(response.read())
            sPattern = 'src="([^"]+)"'
            aResult = oParser.parse(c, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]

        VSlog(sHosterUrl)

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
