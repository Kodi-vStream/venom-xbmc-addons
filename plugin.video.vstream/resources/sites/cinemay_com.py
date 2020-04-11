#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import cUtil
import re, unicodedata

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

SITE_IDENTIFIER = 'cinemay_com'
SITE_NAME = 'Cinemay'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = 'https://www.cinemay.li/'

MOVIE_NEWS = (URL_MAIN + 'film-vf-streaming/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-vf-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'serie-streaming/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie-streaming/', 'showMovies')
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

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action/'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Crime', URL_MAIN + 'genre/crime/'] )
    liste.append( ['Documentaire', URL_MAIN + 'genre/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame/'] )
    liste.append( ['Familial', URL_MAIN + 'genre/familial/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre/'] )
    # liste.append( ['Guerre & politics', URL_MAIN + 'genre/war-politics/'] )
    liste.append( ['Histoire', URL_MAIN + 'genre/histoire/'] )
    liste.append( ['Horreur', URL_MAIN + 'genre/horreur/'] )
    liste.append( ['Enfants', URL_MAIN + 'genre/kids/'] )
    liste.append( ['Musique', URL_MAIN + 'genre/musique/'] )
    liste.append( ['Mystère', URL_MAIN + 'genre/mystère/'] )
    liste.append( ['Téléfilm', URL_MAIN + 'genre/telefilm/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance/'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'genre/science_fiction/'] )
    liste.append( ['Soap', URL_MAIN + 'genre/soap/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genre/western/'] )

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" data-url=".+?" class=".+?" title="([^"]+)"><img.+?src="([^"]*)"'
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

            #encode/decode pour affichage des accents
            sTitle = unicode(aEntry[1], 'utf-8')
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore').decode('unicode_escape')
            sTitle = sTitle.encode('latin-1')
            #Nettoyage du titre
            sTitle = sTitle.replace(' en streaming', '')
            if sTitle.startswith('Film'):
                sTitle = sTitle.replace('Film ', '')

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[2]

            #tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^"]+)">>><'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False

def showSeriesNews():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="titleE".+?<a href="([^"]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = re.sub('(\d+)&#215;(\d+)', 'S\g<1>E\g<2>', aEntry[1])
            sTitle = sTitle.replace(':', '')
            cCleantitle = re.sub('S\d+E\d+', '', sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', cCleantitle)
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

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
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                sTitle =  aEntry[2]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #on remplace pour afficher la langue
    sHtmlContent = sHtmlContent.replace('width: 50%;float: left;', 'VF')
    sHtmlContent = sHtmlContent.replace('width: 50%;float: right;', 'VOSTFR')

    oParser = cParser()

    sDesc = ''
    try:
        sPattern = '<p>Résumé.+?treaming : (.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    sPattern = '<ul class="episodios" style="([^"]+)">|<div class="numerando" style="margin: 0">([^<]+)<.+?data-target="([^"]+)"'
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

            if aEntry[0]:#Affichage de la langue
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')
            else:
                #on vire le double affichage de la saison
                sMovieTitle = re.sub('- Saison \d+', '', sMovieTitle)
                sTitle = sMovieTitle + ' ' + aEntry[1].replace(' x ', '').replace(' ', '')
                sData = aEntry[2]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sData', sData)
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

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
        sPattern = '<p>([^<>"]+)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    sPattern = 'var movie.+?id.+?"(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        MovieUrl = URL_MAIN + 'playery/?id=' + aResult[1][0]

        oRequestHandler = cRequestHandler(MovieUrl)
        oRequestHandler.addHeaderEntry("User-Agent", UA)
        oRequestHandler.addHeaderEntry("Referer", sRefUrl)
        sHtmlContent = oRequestHandler.request()
        head = oRequestHandler.getResponseHeader()
        cookies = getcookie(head)

    sPattern = '<input type="hidden" name="videov" id="videov" value="([^"]+)">.+?<\/b>([^<]+)<span class="dt_flag">.+?\/flags\/(.+?)\.'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHost = aEntry[1].replace(' ', '').replace('.ok.ru', 'ok.ru')
            sHost = re.sub('\.\w+', '', sHost)
            if 'nowvideo' in sHost:
                continue
            sHost = sHost.capitalize()
            sLang = aEntry[2].upper()

            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            sUrl = URL_MAIN[:-1] + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
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

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            if 'opsktp' in aEntry:# redirection vers ==> fsimg
                oRequestHandler = cRequestHandler(aEntry)
                oRequestHandler.request()
                sHosterUrl = oRequestHandler.getRealUrl()

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
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
    #Decoupage pour cibler l'épisode
    sPattern = sData + '">(.+?)</ul>'
    sHtmlContent = oParser.parse(sHtmlContent, sPattern)

    sPattern = 'id="videov" value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHostersOld():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sRefUrl = oInputParameterHandler.getValue('sRefUrl')
    sCookie = oInputParameterHandler.getValue('cookies')

    #validation
    oRequestHandler = cRequestHandler(URL_MAIN + 'image/logo.png')
    oRequestHandler.addHeaderEntry("User-Agent", UA)
    oRequestHandler.addHeaderEntry("Referer", sRefUrl)
    oRequestHandler.addHeaderEntry("Cookie", sCookie)
    sHtmlContent = oRequestHandler.request()

    #final
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry("User-Agent", UA)
    oRequestHandler.addHeaderEntry("Referer", sRefUrl)
    oRequestHandler.addHeaderEntry("Cookie", sCookie)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<script type=\"text\/javascript\">;(.+?)<\/script>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.setEndOfDirectory()
        return

    if (aResult[0] == True):
        jscode = aResult[1][0]
        maxretries = 5
        while 'url=' not in jscode:
            sPattern = "join\(\'\'\)\;\}\('(.+?)','(.+?)','(.+?)','(.+?)'\)\)"
            args = re.findall(sPattern, jscode, re.DOTALL)
            jscode = decode_js(args[0][0], args[0][1], args[0][2], args[0][3])
            maxretries = maxretries -1

        sPattern='url=([^"]+)\"'
        oParser = cParser()
        aResult = oParser.parse(jscode, sPattern)
        if (aResult[0] == True):
            sHosterUrl = aResult[1][0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def getcookie(head):
    #get cookie
    cookies = ''
    if 'Set-Cookie' in head:
        oParser = cParser()
        sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
        aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
        if (aResult[0] == True):
            for cook in aResult[1]:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'
            return cookies

#author @NizarAlaoui
def decode_js(k, i, s, e):
    varinc = 0
    incerement2 = 0
    finalincr = 0
    firsttab = []
    secondtab = []
    while True :
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
        finaltab.append(chr(int(firststr[varinc:varinc+2], base=36) - localvar))
        incerement2=incerement2 + 1
        if incerement2 >= len(secondtab):
            incerement2 = 0

    return ''.join(finaltab)
