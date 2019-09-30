#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

import re

SITE_IDENTIFIER = 'fullstream'
SITE_NAME = 'FullStream'
SITE_DESC = 'Films, Séries et Mangas Gratuit en streaming sur Full stream'

URL_MAIN = 'https://vfspace.me/'

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')

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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'xfsearch/genre/Action/'] )
    liste.append( ['Animation', URL_MAIN + 'xfsearch/genre/Animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'xfsearch/genre/Aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'xfsearch/genre/Biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'xfsearch/genre/Comedie/'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'xfsearch/genre/Comedie%20musicale/'] )
    liste.append( ['Comédie dramatique', URL_MAIN + 'xfsearch/genre/Comedie%20dramatique/'] )
    liste.append( ['Documentaire', URL_MAIN + 'xfsearch/genre/Documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'xfsearch/genre/Drame/'] )
    liste.append( ['Divers', URL_MAIN + 'xfsearch/genre/Divers/'] )
    liste.append( ['Horreur', URL_MAIN + 'xfsearch/genre/Epouvante-horreur/'] )
    liste.append( ['Famille', URL_MAIN + 'xfsearch/genre/Famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'xfsearch/genre/Fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'xfsearch/genre/Guerre/'] )
    liste.append( ['Policier', URL_MAIN + 'xfsearch/genre/Policier/'] )
    liste.append( ['Romance', URL_MAIN + 'xfsearch/genre/Romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'xfsearch/genre/Science%20fiction/'] )
    liste.append( ['Thriller', URL_MAIN + 'xfsearch/genre/Thriller/'] )
    liste.append( ['Western', URL_MAIN + 'xfsearch/genre/Western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = URL_MAIN 

        pdata = 'story=' + sSearch + '&do=search&subaction=search'

        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
        oRequest.addParameters('Referer', URL_MAIN)

        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="short-poster" href="([^"]+)" title="([^"]+)">.+?<img src="([^"]+)"'

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

            sThumb = URL_MAIN[:-1] + aEntry[2]
            sTitle = aEntry[1].replace('Regarder','').replace('en ligne gratuitement','')
            sUrl2 = aEntry[0]

            sDisplayTitle = ('%s') % (sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'serie' in sUrl2 or 'saison' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

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
    sPattern = '<span class="page_next".+?<a href="([^"]+)">'
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
    sPattern = '<div class="full-text".+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]

    sHtmlContent = oParser.abParse(sHtmlContent, 'class="movie-tabs">', 'similaires</h3>')

    #recuperation des suivants
    sPattern = 'button class="llien">Lien(.+?)</button>|<a title=.+?target="seriePlayer" href="([^"]+)">([^<]+)</a>'
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
                sUrl2 = URL_MAIN[:-1] + aEntry[1]
                SxE = re.sub('lecteur (\d+)', '', aEntry[2]).upper().replace(' ','')
                sTitle = sMovieTitle + '[' + SxE + ']'

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    sDesc = ''
    sPattern = '<div class="full-text".+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = re.sub('.+? : ','',aResult[1][0])
        
    sPattern = '<a title="([^"]+)" target="seriePlayer" href="([^"]+)">([^<]+)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN[:-1] + aEntry[1]
            sHost = aEntry[2].replace(' ','')
            sLang = aEntry[0][-2:]
            sTitle = ('%s [%s] [%s]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)
            
        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)

    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:66.0) Gecko/20100101 Firefox/66.0')
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Referer', URL_MAIN)

    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
