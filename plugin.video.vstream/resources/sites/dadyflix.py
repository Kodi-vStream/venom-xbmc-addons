#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress#, VSlog
import re
from datetime import date


SITE_IDENTIFIER = 'dadyflix'
SITE_NAME = 'DadyFlix'
SITE_DESC = 'Films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'https://www.dadyflix.ws/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = ('http://', 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/','showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'les-plus-populaires/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = ('http://', 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_COMMENTS =  (URL_MAIN + 'les-plus-populaires/?get=tv', 'showMovies')
SERIE_NETFLIX = (URL_MAIN + 'network/netflix/', 'showMovies')

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

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus populaires)', 'comments.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus populaires)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NETFLIX[1], 'Séries de Netflix', 'series.png', oOutputParameterHandler)

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
    liste.append( ['Action', URL_MAIN + 'genre/action/'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Documentaire', URL_MAIN + 'genre/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame/'] )
    liste.append( ['Familial', URL_MAIN + 'genre/familial/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre/'] )
    liste.append( ['Histoire', URL_MAIN + 'genre/histoire/'] )
    liste.append( ['Horreur', URL_MAIN + 'genre/horreur/'] )
    liste.append( ['Mystere', URL_MAIN + 'genre/mystere/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genre/science-fiction/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genre/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieYears():
    oGui = cGui()
    
    for i in reversed (xrange(1971, date.today().year+1)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch
        sPattern = '<a href="([^"]+)"><img src="([^"]+)" alt=.+?<span class="(.+?)".+?href=.+?>([^<]+)<.+?"year">(.+?)<.+?"contenido"><p>(.+?)<'
    elif '/les-plus-populaires/' in sUrl or '/tendance/' in sUrl:
        sPattern = '<img src="([^"]+)" alt="(?:film|serie) ([^"]+)streaming".+?(?:|quality">([^<]+)<.+?)href="([^"]+)".+?<span>(.+?)<'
    else:
        sPattern = '<img src="([^"]+)" alt="(?:film|serie) ([^"]+)streaming".+?(?:|quality">([^<]+)<.+?)href="([^"]+)".+?<span>(.+?)<.+?div class="texto">([^<]+)</div>'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

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

            if sSearch:
                sUrl2 = aEntry[0]
                sThumb = re.sub('/w\d+', '/w342', aEntry[1], 1)
                sQual = aEntry[2].replace('tvshows', 'Série').replace('movies', 'Film')
                sTitle = aEntry[3]
                setDisplayName = ('%s [%s]') % (sTitle, sQual)
            else:
                sThumb = re.sub('/w\d+', '/w342', aEntry[0], 1)
                sTitle = aEntry[1]
                sQual = aEntry[2].replace('Haute-qualité', 'HD')
                sUrl2 = aEntry[3]

            sYear = aEntry[4]
            setDisplayName = ('%s [%s](%s)') % (sTitle, sQual, sYear)
    
            sDesc = ''
            if len(aEntry) > 5:
                sDesc = aEntry[5].replace('&#8217;', '\'').replace('&#8230;', '...').replace('>', '')

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/series/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', setDisplayName, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', setDisplayName, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "<span class=\"current\">.+?</span><a href='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a id="playerlink.+?" data-src-player="([^"]+)" vid-link=".+?">'

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

def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^"]+)"><img src="([^"]+)"></a></div><div class="numerando">(.+?) - (.+?)</div><div class="episodiotitle">'
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

            sTitle = sMovieTitle + ' Saison ' + aEntry[2] + ' Episode' + aEntry[3]
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a id="playerlink.+?" data-src-player="([^"]+)" vid-link=".+?">.+?<img src=".+?/flags/(.+?).png"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle + ' (' + aEntry[1].upper() + ')')
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
