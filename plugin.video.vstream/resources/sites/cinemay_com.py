# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
# import unicodedata

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

SITE_IDENTIFIER = 'cinemay_com'
SITE_NAME = 'Cinemay'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'film-vf-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'serie-streaming/', 'showMovies')
# SERIE_LIST = (URL_MAIN + 'serie-streaming/', 'showSeriesList')

URL_SEARCH = (URL_MAIN + '?keyword=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Aventure', 'aventure'], ['Comédie', 'comédie'],
             ['Crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'familial'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Horreur', 'horreur'],
             ['Enfants', 'kids'], ['Musique', 'musique'], ['Mystère', 'mystère'], ['Téléfilm', 'telefilm'],
             ['Romance', 'romance'], ['Science-Fiction', 'science_fiction'], ['Soap', 'soap'], ['Thriller', 'thriller'],
             ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sUrl = sSearch.replace(' ', '+')
        sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH[0], ''))

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" data-url=".+?" class=".+?" title="([^"]+)"><img.+?src="([^"]*)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            # Nettoyage du titre
            sTitle = aEntry[1].replace(' en streaming', '').replace('- Saison ', ' S')
            if sTitle.startswith('Film'):
                sTitle = sTitle.replace('Film ', '')

            # filtre search
            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, sTitle):
                    continue

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                sMovieTitle = re.sub('  S\d+', '', sTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addSeason(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    # jusqu'au 5 dernières pages on utilise cette regex
    sPattern = 'href="([^"]+)">>><.+?">(\d+)</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    # à partir des 5 dernières pages on change de regex
    sPattern = '>([^<]+)</a> <a class="inactive" style="margin-bottom:5px;" href="([^"]+)">>>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSeriesNews():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="titleE".+?<a href="([^"]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = re.sub('(\d+)&#215;(\d+)', 'S\g<1>E\g<2>', aEntry[1])
            sTitle = sTitle.replace(':', '')
            cCleantitle = re.sub('- Saison \d+', '', sTitle)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', cCleantitle)
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="alpha-title"><h3>([^<]+)</h3>|</li><li class="item-title">.+?href="([^"]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                sTitle = aEntry[2]

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # on remplace pour afficher la langue
    sHtmlContent = sHtmlContent.replace('width: 50%;float: left;', 'VF')
    sHtmlContent = sHtmlContent.replace('width: 50%;float: right;', 'VOSTFR')

    oParser = cParser()

    sDesc = ''
    try:
        sPattern = '<p>Résumé.+?omplet : (.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].split('Résumé')[0]
    except:
        pass

    sPattern = 'class="episodios" style="([^"]+)">|class="numerando" style="margin: 0">([^<]+)<.+?data-target="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        sLang = ''
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:  # Affichage de la langue
                sLang = aEntry[0]
            else:
                # on vire le double affichage de la saison
                sTitle = sMovieTitle + ' ' + aEntry[1].replace(' x ', '').replace(' ', '')
                sDisplayTitle = sTitle + ' ' + '(' + sLang + ')'
                sData = aEntry[2]

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sData', sData)
                oOutputParameterHandler.addParameter('sLang', sLang)
                oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sRefUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sRefUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sDesc = ''
    try:
        sPattern = '<p>([^<>"]+)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = 'var movie.+?id.+?"(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        movieUrl = URL_MAIN + 'playery/?id=' + aResult[1][0]

        oRequestHandler = cRequestHandler(movieUrl)
        oRequestHandler.addHeaderEntry("User-Agent", UA)
        oRequestHandler.addHeaderEntry("Referer", sRefUrl)
        sHtmlContent = oRequestHandler.request()
        head = oRequestHandler.getResponseHeader()
        cookies = getCookie(head)

    sPattern = 'hidden" name="videov" id="videov" value="([^"]+).+?</b>([^<]+)<span class="dt_flag">.+?/flags/(.+?)\.'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oHosterGui = cHosterGui()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sHost = aEntry[1].replace(' ', '').replace('.ok.ru', 'ok.ru')
            sHost = re.sub('\.\w+', '', sHost)
            sHost = sHost.capitalize()
            if not oHosterGui.checkHoster(sHost):
                continue

            sLang = aEntry[2].upper()
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sRefUrl', sRefUrl)
            oOutputParameterHandler.addParameter('cookies', cookies)
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

    oParser = cParser()
    sPattern = 'id="videov" value="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sData = oInputParameterHandler.getValue('sData')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    # Decoupage pour cibler l'épisode
    sPattern = sData + '">(.+?)</ul>'
    sHtmlContent = oParser.parse(sHtmlContent, sPattern)

    sPattern = 'id="videov" value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def getCookie(head):
    # get cookie
    cookies = ''
    if 'Set-Cookie' in head:
        oParser = cParser()
        sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
        aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
        if aResult[0]:
            for cook in aResult[1]:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'
            return cookies


# author @NizarAlaoui
def decode_js(k, i, s, e):
    varinc = 0
    incerement2 = 0
    finalincr = 0
    firsttab = []
    secondtab = []
    while True:
        if varinc < 5:
            secondtab.append(k[varinc])
        elif varinc < len(k):
            firsttab.append(k[varinc])
        varinc = varinc + 1
        if incerement2 < 5:
            secondtab.append(i[incerement2])
        elif incerement2 < len(i):
            firsttab.append(i[incerement2])
        incerement2 = incerement2 + 1
        if finalincr < 5:
            secondtab.append(s[finalincr])
        elif finalincr < len(s):
            firsttab.append(s[finalincr])
        finalincr = finalincr + 1
        if (len(k) + len(i) + len(s) + len(e)) == (len(firsttab) + len(secondtab) + len(e)):
            break

    firststr = ''.join(firsttab)
    secondstr = ''.join(secondtab)
    incerement2 = 0
    finaltab = []
    for varinc in range(0, len(firsttab), 2):
        localvar = -1
        if ord(secondstr[incerement2]) % 2:
            localvar = 1
        finaltab.append(chr(int(firststr[varinc: varinc+2], base=36) - localvar))
        incerement2 = incerement2 + 1
        if incerement2 >= len(secondtab):
            incerement2 = 0

    return ''.join(finaltab)
