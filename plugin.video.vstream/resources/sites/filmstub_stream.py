#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog
import re

SITE_IDENTIFIER = 'filmstub_stream'
SITE_NAME = 'Filmstub'
SITE_DESC = 'Films, Séries & Mangas en streaming'
URL_MAIN = 'https://www.filmstub.cc/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = ('http://film', 'showGenres')
MOVIE_LIST = (True, 'showAlpha')

SERIE_SERIES = (URL_MAIN + 'series-streaming/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')
SERIE_GENRES = ('http://serie', 'showSerieGenres')

ANIM_ANIMS = (URL_MAIN + 'anime-streaming/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'anime-streaming/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films & Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'serie' in sUrl:
        sType = '?tr_post_type=2'
    else:
        sType = '?tr_post_type=1'

    liste = []
    liste.append( ['Action', URL_MAIN + 'category/action/' + sType] )
    liste.append( ['Action & Adventure', URL_MAIN + 'category/action-adventure/' + sType] )
    liste.append( ['Animation', URL_MAIN + 'category/animation/' + sType] )
    liste.append( ['Aventure', URL_MAIN + 'category/aventure/' + sType] )
    liste.append( ['BoxOffice', URL_MAIN + 'category/boxoffice/' + sType] )
    liste.append( ['Comédie', URL_MAIN + 'category/comedie/' + sType] )
    liste.append( ['Comedy', URL_MAIN + 'category/comedy/' + sType] )
    liste.append( ['Crime', URL_MAIN + 'category/crime/' + sType] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire/' + sType] )
    liste.append( ['Drama', URL_MAIN + 'category/drama/' + sType] )
    liste.append( ['Drame', URL_MAIN + 'category/drame/' + sType] )
    liste.append( ['Erotique', URL_MAIN + 'category/erotic/' + sType] )
    liste.append( ['Etranger', URL_MAIN + 'category/etranger/' + sType] )
    liste.append( ['Familial', URL_MAIN + 'category/familial/' + sType] )
    liste.append( ['Fantastique', URL_MAIN + 'category/fantastique/' + sType] )
    liste.append( ['Fantasy', URL_MAIN + 'category/fantasy/' + sType] )
    liste.append( ['Guerre', URL_MAIN + 'category/guerre/' + sType] )
    liste.append( ['Histoire', URL_MAIN + 'category/histoire/' + sType] )
    liste.append( ['Horreur', URL_MAIN + 'category/horreur/' + sType] )
    liste.append( ['Kids', URL_MAIN + 'category/kids/' + sType] )
    liste.append( ['Musique', URL_MAIN + 'category/musique/' + sType] )
    liste.append( ['Music', URL_MAIN + 'category/music/' + sType] )
    liste.append( ['Mystère', URL_MAIN + 'category/mystere/' + sType] )
    liste.append( ['Mystery', URL_MAIN + 'category/mystery/' + sType] )
    liste.append( ['News', URL_MAIN + 'category/news/' + sType] )
    liste.append( ['Reality', URL_MAIN + 'category/reality/' + sType] )
    liste.append( ['Romance', URL_MAIN + 'category/romance/' + sType] )
    liste.append( ['Sci-Fi & Fantasy', URL_MAIN + 'category/sci-fi-fantasy/' + sType] )
    liste.append( ['Science Fiction', URL_MAIN + 'category/science-fiction/' + sType] )
    liste.append( ['Science Fiction & Fantastique', URL_MAIN + 'category/science-fiction-fantastique/' + sType] )
    liste.append( ['Soap', URL_MAIN + 'category/soap/' + sType] )
    liste.append( ['Téléfilm', URL_MAIN + 'category/telefilm/' + sType] )
    liste.append( ['Thriller', URL_MAIN + 'category/thriller/' + sType] )
    liste.append( ['War & Politics', URL_MAIN + 'category/war-politics/' + sType] )
    liste.append( ['Western', URL_MAIN + 'category/western/' + sType] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()

    liste = []
    liste.append( ['#', URL_MAIN + 'letters/0-9/'] )
    liste.append( ['A', URL_MAIN + 'letters/a/'] )
    liste.append( ['B', URL_MAIN + 'letters/b/'] )
    liste.append( ['C', URL_MAIN + 'letters/c/'] )
    liste.append( ['D', URL_MAIN + 'letters/d/'] )
    liste.append( ['E', URL_MAIN + 'letters/e/'] )
    liste.append( ['F', URL_MAIN + 'letters/f/'] )
    liste.append( ['G', URL_MAIN + 'letters/g/'] )
    liste.append( ['H', URL_MAIN + 'letters/h/'] )
    liste.append( ['I', URL_MAIN + 'letters/i/'] )
    liste.append( ['J', URL_MAIN + 'letters/j/'] )
    liste.append( ['K', URL_MAIN + 'letters/k/'] )
    liste.append( ['L', URL_MAIN + 'letters/l/'] )
    liste.append( ['M', URL_MAIN + 'letters/m/'] )
    liste.append( ['N', URL_MAIN + 'letters/n/'] )
    liste.append( ['O', URL_MAIN + 'letters/o/'] )
    liste.append( ['P', URL_MAIN + 'letters/p/'] )
    liste.append( ['Q', URL_MAIN + 'letters/q/'] )
    liste.append( ['R', URL_MAIN + 'letters/r/'] )
    liste.append( ['S', URL_MAIN + 'letters/s/'] )
    liste.append( ['T', URL_MAIN + 'letters/t/'] )
    liste.append( ['U', URL_MAIN + 'letters/u/'] )
    liste.append( ['V', URL_MAIN + 'letters/v/'] )
    liste.append( ['W', URL_MAIN + 'letters/w/'] )
    liste.append( ['X', URL_MAIN + 'letters/x/'] )
    liste.append( ['Y', URL_MAIN + 'letters/y/'] )
    liste.append( ['Z', URL_MAIN + 'letters/z/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    if 'letters' in sUrl:
        sPattern = '<a href="([^"]+)" class="MvTbImg".+?<noscript><img src="([^"]+)" alt=.+?(?:|class="TpTv BgA">([^<]+)<.+?)strong>([^<]+)<.+?</td><td>([^<]+)<'
    else:
        sPattern = 'class="TPost C"> *<a href="([^"]+)".+?data-lazy-src="([^"]+)".+?class="Title">([^<]+)<.+?<span class="Year">([^<]+)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'letters' in sUrl:
                sUrl2 = aEntry[0]
                sThumb = aEntry[1].replace('w92', 'w342')
                sTitle = aEntry[3]
                sYear = aEntry[4]

                sDisplayTitle = ('%s (%s)') % (sTitle, sYear)
            else:
                sUrl2 = aEntry[0]
                sThumb = aEntry[1].replace('w185', 'w342')
                sTitle = aEntry[2]
                sYear = aEntry[3]

                sDisplayTitle = ('%s (%s)') % (sTitle, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'letters' in sUrl and 'Serie' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory() #arriver la

def __checkForNextPage(sHtmlContent):
    sPattern = 'href="*([^">]+)"*>Next'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showEpisode():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sDesc = ''
    try:
        sPattern = '<div class="Description"><p>([^<]+)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    sPattern = '<div class="Title AA-Season.+?tab=".+?">([^<]+)<span>(\d+)</span>|<li class="[0-9a-zA-Z]+"> *<a href="([^"]+)">([^<]+)<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if (aEntry[0] and aEntry[1]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + ' ' + aEntry[1] + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                sTitle = sMovieTitle + ' ' + aEntry[3]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #resume
    sDesc = ''
    try:
        sPattern = '<div class="Description"><p>([^<]+)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:

            sDesc = aResult[1][0]
            sDesc = sDesc.replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    sHtmlContent = oParser.abParse(sHtmlContent, 'TPost Sing', '<span class="btnsplyr">')#film serie
    sHtmlContent = re.sub(' SERVEUR <strong>[0-9]</strong>', ' SERVEUR', sHtmlContent)#Liste
    #sHtmlContent = re.sub('<img class="imgfav" *src="https://www.google.com/s2/favicons\?domain=.+?">', '', sHtmlContent)#film
    sHtmlContent = sHtmlContent.replace('&quot;', '"').replace('#038;', '').replace('&amp;', '&')

    #1
    if 'episode' in sUrl:
        sPattern = 'data-tplayernv=".+?"><span>([^<]+)<\/span><span>([^<]+)<\/span>'
    else:
        sPattern = 'data-tplayernv=".+?</noscript>([^<]+)<\/span><span>([^<]+)<\/span>'

    aResult1 = re.findall(sPattern, sHtmlContent)

    #2
    sPattern1 = 'src="(https:\/\/www.filmstub.+?)"'
    aResult2 = re.findall(sPattern1, sHtmlContent)

    aResult = []
    aResult = zip(aResult2, [x[1] + ' ' + x[0] for x in aResult1])
    if (aResult):
        for aEntry in aResult:

            sUrl = aEntry[0]
            sHost = aEntry[1]
            if 'FileBebo' in sHost:
                continue
            sTitle = '%s (%s)' % (sMovieTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        oRequestHandler = cRequestHandler(aResult[1][0])
        sHtmlContent = oRequestHandler.request()

        sPattern = 'defer.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            oRequestHandler = cRequestHandler(aResult[1][0])
            sHtmlContent = oRequestHandler.request()

            sPattern = "id=trde\('([^']+)'\)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sUrl = URL_MAIN + '?trhide=1&trhex=' + decoded(aResult[1][0])


                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()

                sHosterUrl = oRequest.getRealUrl()

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def decoded(trde):
    #a = '13839373636353939373735313f2465626d656f656469667f25727e2b6f6f2f2a33707474786'
    b = int(len(trde) - 1)
    start = ''
    while (b >= 0):
        start += trde[b]
        b -= 1

    return start
