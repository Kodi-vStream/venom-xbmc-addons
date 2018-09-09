#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
#from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
#from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import re, urllib, urllib2

SITE_IDENTIFIER = 'filmcomplet'
SITE_NAME = 'Film Complet'
SITE_DESC = 'Film Complet - film en streaming HD'

URL_MAIN = 'https://filmcomplet.club/'
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + '?s=', 'showSearchResult')
#recherche global films
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/?get=movies', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'evaluations/?get=movies', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
#MOVIE_LIST = (True, 'showList')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    #ne fonctionne plus sur le site
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action/'] )
    liste.append( ['Action & aventure', URL_MAIN + 'genre/action-adventure/'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Crime', URL_MAIN + 'genre/crime/'] )
    liste.append( ['Documentaire', URL_MAIN + 'genre/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame/'] )
    liste.append( ['Etranger', URL_MAIN + 'genre/etranger/'] )
    liste.append( ['Familial', URL_MAIN + 'genre/familial/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre/'] )
    liste.append( ['Histoire', URL_MAIN + 'genre/histoire/'] )
    liste.append( ['Horreur', URL_MAIN + 'genre/horreur/'] )
    liste.append( ['Musique', URL_MAIN + 'genre/musique/'] )
    liste.append( ['Mystère', URL_MAIN + 'genre/mystere/'] )
    liste.append( ['News', URL_MAIN + 'genre/news/'] )
    liste.append( ['Policier', URL_MAIN + 'genre/policier/'] )
    liste.append( ['Reality', URL_MAIN + 'genre/reality/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genre/science-fiction/'] )
    liste.append( ['Science Fiction & Fantastique', URL_MAIN + 'genre/science-fiction-fantastique/'] )
    liste.append( ['Soap', URL_MAIN + 'genre/soap/'] )
    liste.append( ['Talk', URL_MAIN + 'genre/talk/'] )
    liste.append( ['Téléfilm', URL_MAIN + 'genre/telefilm/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller/'] )
    liste.append( ['War & Politics', URL_MAIN + 'genre/war-politics/'] )
    liste.append( ['Western', URL_MAIN + 'genre/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showList():
    oGui = cGui()

    liste = []
    liste.append( ['09', URL_MAIN + '?letter=true&s=title-09'] )
    liste.append( ['A', URL_MAIN + '?letter=true&s=title-a'] )
    liste.append( ['B', URL_MAIN + '?letter=true&s=title-b'] )
    liste.append( ['C', URL_MAIN + '?letter=true&s=title-c'] )
    liste.append( ['D', URL_MAIN + '?letter=true&s=title-d'] )
    liste.append( ['E', URL_MAIN + '?letter=true&s=title-e'] )
    liste.append( ['F', URL_MAIN + '?letter=true&s=title-f'] )
    liste.append( ['G', URL_MAIN + '?letter=true&s=title-g'] )
    liste.append( ['H', URL_MAIN + '?letter=true&s=title-h'] )
    liste.append( ['I', URL_MAIN + '?letter=true&s=title-i'] )
    liste.append( ['J', URL_MAIN + '?letter=true&s=title-j'] )
    liste.append( ['K', URL_MAIN + '?letter=true&s=title-k'] )
    liste.append( ['L', URL_MAIN + '?letter=true&s=title-l'] )
    liste.append( ['M', URL_MAIN + '?letter=true&s=title-m'] )
    liste.append( ['N', URL_MAIN + '?letter=true&s=title-n'] )
    liste.append( ['O', URL_MAIN + '?letter=true&s=title-o'] )
    liste.append( ['P', URL_MAIN + '?letter=true&s=title-p'] )
    liste.append( ['Q', URL_MAIN + '?letter=true&s=title-q'] )
    liste.append( ['R', URL_MAIN + '?letter=true&s=title-r'] )
    liste.append( ['S', URL_MAIN + '?letter=true&s=title-s'] )
    liste.append( ['T', URL_MAIN + '?letter=true&s=title-t'] )
    liste.append( ['U', URL_MAIN + '?letter=true&s=title-u'] )
    liste.append( ['V', URL_MAIN + '?letter=true&s=title-v'] )
    liste.append( ['W', URL_MAIN + '?letter=true&s=title-w'] )
    liste.append( ['X', URL_MAIN + '?letter=true&s=title-x'] )
    liste.append( ['Y', URL_MAIN + '?letter=true&s=title-y'] )
    liste.append( ['Z', URL_MAIN + '?letter=true&s=title-z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1963, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchResult(sSearch = ''):
    oGui = cGui()
    sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="thumbnail animation-2".+?href="([^"]+)".+?img src="([^"]+)" alt="([^"]+)".+?<p>(.+?)<'

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

            sUrl = aEntry[0]
            sThumb = aEntry[1].replace('w90', 'w342')
            sTitle = aEntry[2]
            sDesc = aEntry[3]

            #tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="poster"><img src="([^<]+)" alt="([^<]+)".+?(?:|class="quality">([^<]+)<.+?)<a href="([^"]+)"'

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
            sDesc = ''

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showLinks():
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
        sPattern = '<p>([^<>]+)&#.+?<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<li id="player-option-.+?" class="dooplay_player_option " data-post="(.+?)" data-nume="(.+?)">\s*.+?\s*<span class="title">(.+?)</span>\s*<span class="server">(.+?)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sPost = aEntry[0]
            sNume = aEntry[1]
            sQual = aEntry[2]
            sHost = re.sub('\.\w+', '', aEntry[3])
            sHost = sHost.capitalize()
            sTitle = ('%s [%s] [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sPost', sPost)
            oOutputParameterHandler.addParameter('sNume', sNume)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sPost = oInputParameterHandler.getValue('sPost')
    sNume = oInputParameterHandler.getValue('sNume')

    sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'

    oRequestHandler = cRequestHandler(sUrl2)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
    oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    oRequestHandler.addParameters('action', 'doo_player_ajax')
    oRequestHandler.addParameters('post', sPost)
    oRequestHandler.addParameters('nume', sNume)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)

    sPattern = "<iframe.+?src='(.+?)'"
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
