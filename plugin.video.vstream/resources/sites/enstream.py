#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'enstream'
SITE_NAME = 'Enstream'
SITE_DESC = 'Regarder, Voir Films En Streaming VF 100% Gratuit.'

URL_MAIN = 'https://ww1.enstream.co/' 

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'tags/', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_SEARCH[0], FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText.replace(' ', '+')
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action/'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'genre/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'genre/comedie-musical/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'genre/epouvante-horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'genre/espionnage/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'genre/historique/'] )
    liste.append( ['Judiciaire', URL_MAIN + 'genre/judiciaire/'] )
    liste.append( ['Musical', URL_MAIN + 'genre/musical/'] )
    liste.append( ['Péplum', URL_MAIN + 'genre/peplum/'] )
    liste.append( ['Policier', URL_MAIN + 'genre/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genre/science-fiction/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genre/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

       
    sHtmlContent = sHtmlContent
    oParser = cParser()

    sPattern = 'film-uno"><a href="([^"]+)".+?data-src="([^"]+)".+?alt="([^"]+)".+?short-story">([^<]+)'
    if 'genre/' in sUrl :
      sPattern = 'film-uno"><a href="([^"]+)".+?data-src="([^"]+)".+?alt="([^"]+)"'
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
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            
            sDesc = ''
            if len(aEntry)>3:
                sDesc = aEntry[3]
            
            
            

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHoster', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    oParser = cParser()
    sPattern = 'class="pagination".+?a href=\'([^"]+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False
def showHoster():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    
    sPattern = 'data-url="([^"]+)".+?data-code="([^"]+)".+?domain=([^"]+).+?mobile">([^<]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sDataUrl = aEntry[0]
            sDataCode = aEntry[1]
            lienhost = aEntry[2]
            sHost = aEntry[3]
            sDesc = ''
            # filtrage des hosters
            #oHoster = cHosterGui().checkHoster(sHost)
            if (sHost=='ENSTREAM'):
                continue

            sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            lien = URL_MAIN + 'Players.php?PPl=' + sDataUrl + '&CData=' + sDataCode

            oOutputParameterHandler = cOutputParameterHandler()

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', lien)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'showHostersLinks', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHostersLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', referer)
   
    
       
    

    oRequestHandler.request()
    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
