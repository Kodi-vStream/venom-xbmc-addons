#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
import re

SITE_IDENTIFIER = 'toro'
SITE_NAME = 'Toro'
SITE_DESC = 'Regarder Films et Séries en Streaming gratuit'

URL_MAIN = 'https://voir.torostreaming.com/'


FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')

URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')

URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_MOVIE = ('http://', 'showMenuMovies')

MOVIE_GENRES = (URL_MAIN + 'genre/', 'showGenres')



SERIE_SERIES = ('http://', 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + '/series-streaming/', 'showMovies')

SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films (Menu)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries (Menu)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

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

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Action', sUrl + '/action/'] )
    liste.append( ['Animation', sUrl + '/animation/'] )
    liste.append( ['Arts Martiaux', sUrl + '/arts-martiaux/'] )
    liste.append( ['Aventure', sUrl + '/aventure/'] )
    liste.append( ['Comédie', sUrl + '/comedie/'] )
    liste.append( ['Documentaire', sUrl + '/documentaire/'] )
    liste.append( ['Biopic', sUrl + '/biopic/'] )
    liste.append( ['Drame', sUrl + '/drame/'] )
    liste.append( ['Epouvante Horreur', sUrl + '/epouvante-horreur/'] )
    liste.append( ['Erotique', sUrl + '/erotique/'] )
    liste.append( ['Espionnage', sUrl + '/espionnage/'] )
    liste.append( ['Famille', sUrl + '/famille_1'] )
    liste.append( ['Fantastique', sUrl + '/fantastique/'] )
    liste.append( ['Guerre', sUrl + '/guerre/'] )
    liste.append( ['Historique', sUrl + '/historique/'] )
    liste.append( ['Musical', sUrl + '/musical/'] )
    liste.append( ['Policier', sUrl + '/policier/'] )
    liste.append( ['Romance', sUrl + '/romance/'] )
    liste.append( ['Science Fiction', sUrl + '/science-fiction/'] )
    liste.append( ['Spectacle', sUrl + '/spectacles/'] )
    liste.append( ['Thriller', sUrl + '/thriller/'] )
    liste.append( ['Comédie Dramatique', sUrl + '/comedie-dramatique/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showYears():
    oGui = cGui()

    for i in reversed (xrange(1918, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesYears():
    oGui = cGui()

    for i in reversed (xrange(1980, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="TPost C"> .+?href="([^"]+)".+?img src="([^"]+)".+?title">([^<]+).+?year">([^<]+)'
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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDisplayTitle = sTitle + ' (' + sYear + ')'

            sDesc = ''
            if not sThumb.startswith('http'):
                sThumb = 'https:' + sThumb

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)


            if 'series-/' in sUrl2 or '/serie-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSXE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)">>>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showSXE():
    #Uniquement saison a chaque fois
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="Title AA-Season.+?tab="(\d)|class="Num">(\d{1,2}).+?href="([^"]+)".+?span>(\d{4})'
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
                sSaison = 'Saison ' + aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sSaison + '[/COLOR]')
            else:
                sUrl = aEntry[2]
               
                Ep = aEntry[1]
                sTitle = sMovieTitle + ' Episode' + Ep 

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
        progress_.VSclose(progress_)
        
    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-tplayernv.+?span>([^<]+)'
    aResult0 = re.findall(sPattern,sHtmlContent)
    sPattern = 'id="Opt\d.+?src=.+?trembed=(\d).+?trid=(\d{5})'
    aResult1 = re.findall(sPattern,sHtmlContent)
           
    aResult = aResult0 + aResult1        
     
    nbElement = len(aResult0)
    for i in range(nbElement):
        
        sHost = aResult0[i]
        sCode = aResult1[i][0]
        sCode1 = aResult1[i][1]
        sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
        sUrl = URL_MAIN + '?trembed=' + sCode + '&trid=' + sCode1 + '&trtype=1'
        sDesc = ''

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        #oOutputParameterHandler.addParameter('referer', sUrl)

        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    #referer = oInputParameterHandler.getValue('referer')
    oRequestHandler = cRequestHandler(sUrl)
    #oRequestHandler.addHeaderEntry('Referer', referer)

    
    oRequestHandler.request()
    sHtmlContent = oRequestHandler.request()
    sPattern = 'src="([^"]+)"'
    sHosterUrl = oRequestHandler.getRealUrl()
    oParser = cParser()
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
