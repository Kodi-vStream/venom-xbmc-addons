#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress
import re

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films, Séries & Mangas en Streaming'

URL_MAIN = 'https://filmstreamvk.bz/'

MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_EXCLUS = (URL_MAIN + 'tendance/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_EPISODES = (URL_MAIN + 'episodes/', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'network/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'network/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'network/apple-tv/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'network/canal/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'network/youtube-premium/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Films (Populaire)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

#     Inutilisable
#     oOutputParameterHandler = cOutputParameterHandler()
#     oOutputParameterHandler.addParameter('siteUrl', SERIE_EPISODES[0])
#     oGui.addDir(SITE_IDENTIFIER, SERIE_EPISODES[1], 'Séries (Episodes)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NETFLIX[1], 'Séries (Netflix)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AMAZON[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_AMAZON[1], 'Séries (Amazon Prime)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_CANAL[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CANAL[1], 'Séries (Canal+)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DISNEY[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_DISNEY[1], 'Séries (Disney+)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_APPLE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_APPLE[1], 'Séries (Apple TV+)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_YOUTUBE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_YOUTUBE[1], 'Séries (Youtube Originals)', 'news.png', oOutputParameterHandler)

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
    liste.append( ['Action', URL_MAIN + 'genre/action'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie'] )
    liste.append( ['Crime', URL_MAIN + 'genre/crime'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame'] )
    liste.append( ['Familial', URL_MAIN + 'genre/familial'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre'] )
    liste.append( ['Horreur', URL_MAIN + 'genre/horreur'] )
    liste.append( ['Histoire', URL_MAIN + 'genre/histoire'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'genre/science-fiction'] )
    liste.append( ['Western', URL_MAIN + 'genre/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch
        sPattern = '<div class="image">.*?<a href="([^"]+)">\s*<img src="([^"]+)" alt="([^"]+)".+?<p>(.+?)<'
    elif 'episodes' in sUrl:
        sPattern = '<div class="poster">.*?<img src="([^"]+)" alt="(.+?)".+?<a href="([^"]+)">'
    else:
        sPattern = '<div class="poster"> *<img src="([^"]+)".+?<a href="([^"]+)" *title="([^"]+)".+?class="texto">([^<]+)'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[2]) == 0:
                    continue

            sDesc = ''
            if sSearch:
                sThumb = aEntry[1]
                sUrl = aEntry[0]
                sTitle = aEntry[2]
                sDesc = aEntry[3]
            elif 'episodes' in sUrl:
                sThumb = aEntry[0]
                sUrl = aEntry[2]
                sTitle = aEntry[1]
            else:
                sThumb = aEntry[0]
                sUrl = aEntry[1]
                sTitle = aEntry[2].replace('streaming', ' ')
                sDesc = aEntry[3]

            if sDesc:
                sDesc = cUtil().unescape(sDesc.decode('utf8'))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSxE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'episodes' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '\'arrow_pag\' *href="([^"]+)"><i id=\'nextpagination\''
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSxE():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<span class="title">(.+?)<|<div class="numerando">([^"]+)</div><div class="episodiotitle"><a href="([^"]+)">'
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
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                SxE = re.sub('(\d+) - (\d+)', 'saison \g<1> Episode \g<2>', aEntry[1])
                sTitle = sMovieTitle + ' ' + SxE

                sDisplaytitle = sMovieTitle + ' ' + re.sub('saison \d+ ', '', SxE)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplaytitle, '', sThumb, '', oOutputParameterHandler)


        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    if 'episodes' in sUrl:
        sPattern = 'dooplay_player_option.+?data-post="(\d+)".+?data-nume="(.+?)">.+?"title">(.+?)<'
    else:
        sPattern = "dooplay_player_option.+?data-post='(\d+)'.+?data-nume='(.+?)'>.+?'title'>(.+?)<"
    oParser = cParser()        
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if ('trailer' in aEntry[1]): 
                continue
            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            if 'episodes' in sUrl:
                dtype = 'tv'
            else:
                dtype = 'movie'
            dpost = aEntry[0]
            dnum = aEntry[1]
            sHoster = aEntry[2]
            
            #trie des hosters
            oHoster = cHosterGui().checkHoster(sHoster)
            if not oHoster:
                continue
            
            sDisplaytitle = '%s [COLOR coral]%s[/COLOR]' % (sMovieTitle, sHoster)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('data1', dtype)
            oOutputParameterHandler.addParameter('data2', dpost)
            oOutputParameterHandler.addParameter('data3', dnum)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    dtype = oInputParameterHandler.getValue('data1')
    dpost = oInputParameterHandler.getValue('data2')
    dnum = oInputParameterHandler.getValue('data3')

    pdata = 'action=doo_player_ajax&post=' + dpost + '&nume=' + dnum + '&type=' + dtype
    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()
    sPattern = "<iframe.+?src='(.+?)'"
    aResult = re.findall(sPattern, sHtmlContent)

    if (aResult):
        for aEntry in aResult:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

