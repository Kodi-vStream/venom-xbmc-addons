#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
#import urllib2

SITE_IDENTIFIER = 'yourfilms'
SITE_NAME = 'Yourfilms'
SITE_DESC = 'Films & Séries'

URL_MAIN = 'https://www.n1streaming.co/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'recherche-', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_MOVIE = (URL_MAIN , 'showMovies')
MOVIE_GENRES = (URL_MAIN , 'showGenres')
#MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (URL_MAIN + 'Series.html', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'Series.html', 'showMovies')
#SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
#SERIE_ANNEES = (True, 'showSerieYears')

# UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    # Résultat identique à MOVIE_MOVIE
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

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

    liste = []
    liste.append( ['Action', URL_MAIN + 'recherche-Genre-Action.html'] )
    liste.append( ['Animation', URL_MAIN + 'recherche-Genre-Animation.html'] )
    liste.append( ['Aventure', URL_MAIN + 'recherche-Genre-aventure.html'] )
    liste.append( ['Biopic', URL_MAIN + 'recherche-Genre-Biopic.html'] )
    liste.append( ['Comédie', URL_MAIN +'recherche-Genre-comedie.html'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'recherche-Genre-comedie-dramatique.html'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'recherche-Genre-comedie-musicale.html'] )
    #liste.append( ['Divers', URL_MAIN + 'recherche-Genre-Divers.html'] )
    liste.append( ['Documentaire', URL_MAIN + 'recherche-Genre-Documentaire.html'] )
    liste.append( ['Drame', URL_MAIN + 'recherche-Genre-Drame.html'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'recherche-Genre-Epouvante-horreur.html'] )
    liste.append( ['Famille', URL_MAIN + 'recherche-Genre-Famille.html'] )
    liste.append( ['Fantastique', URL_MAIN + 'recherche-Genre-Fantastique.html'] )
    liste.append( ['Guerre', URL_MAIN + 'recherche-Genre-Guerre.html'] )
    liste.append( ['Policier', URL_MAIN + 'recherche-Genre-Policier.html'] )
    liste.append( ['Romance', URL_MAIN +'recherche-Genre-Romance.html'] )
    liste.append( ['Science Fiction', URL_MAIN + 'recherche-Genre-science-fiction.html'] )
    liste.append( ['Thriller', URL_MAIN + 'recherche-Genre-Thriller.html'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1918, 2020)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1936, 2020)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(' ', '-') + '.html'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'img src="([^"]+)".+?alt="([^"]+)".+?<span.+?class="film-rip.+?html">([^"]+)<\/a.+?short.+?href="([^"]+)"'

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

            sThumb = aEntry[0]
            if sThumb.startswith('pagefilm'):
                sThumb = URL_MAIN + sThumb
            sUrl = aEntry[3]
            sQual = aEntry[2]
            sTitle = aEntry[1]
            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/Series/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    # if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'pages-next".+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = '<div class="fsynopsis"><p>(.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('&#884;', '\'').replace('&#8217;', '\'').replace('&#8230;', '...').replace('<p>', '').replace('<span>', '').replace('</span>', '')
    except:
        pass

    sPattern = 'class="short-link".+?a href="([^"]+)".+?>([^<]+)<\/a'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in reversed(aResult[1]):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2   = aEntry[0]
            sTitle  = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'ShowEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def ShowEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sTitle = ''
    sPattern = '<h1 class="fstory-h1">([^<]+)<a'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if ( aResult[0] == True ):
        sTitle = aResult[1][0]

    sPattern = 'streaming" href="([^"]+)".+?class="arrow-right"><\/span>([^<]+)<\/span'
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

            sUrl2 =  aEntry[0]
            sEpisode = 'Episode' + aEntry[1]

            sDisplayTitle = ('%s %s') % (sEpisode, sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = URL_MAIN + sUrl

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    #recuperation pour les films du synopsis
    sDesc = ''
    try:
        sPattern = '<div class="fsynopsis"><p>(.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('&#884;', '\'').replace('&#8217;', '\'').replace('&#8230;', '...').replace('<p>', '').replace('<span>', '').replace('</span>', '')
    except:
        pass

    sPattern = 'class="lectt " src="([^"]+)".+?"lect1">([^<]+)<\/span.+?class="bdpr">([^<]+)<\/span.+?\/img\/([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sHost = aEntry[1].capitalize()
            sQual = aEntry[2]
            sLang = aEntry[3].replace('.png', '').upper()
            sTitle = ('%s [%s] (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

