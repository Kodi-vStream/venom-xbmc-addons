#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'planet_streaming'
SITE_NAME = 'Planet Streaming'
SITE_DESC = 'Films de 1900 jusqu à 2016, contient du HD'

URL_MAIN = 'http://www.2017.planet-streaming.com/'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'regarder-film/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'xfsearch/hd/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('' , 'showMovies')
URL_SEARCH_MOVIES = ('' , 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

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
    liste.append( ['HD/HQ',URL_MAIN + 'xfsearch/hd'] )
    liste.append( ['Action',URL_MAIN + 'action'] )
    liste.append( ['Animation',URL_MAIN + 'animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'biopic'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'comedie-musicale'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur'] )
    liste.append( ['Famille',URL_MAIN + 'famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre'] )
    liste.append( ['Historique',URL_MAIN + 'historique'] )
    liste.append( ['Musical',URL_MAIN + 'musical'] )
    liste.append( ['Policier',URL_MAIN + 'policier'] )
    liste.append( ['Romance',URL_MAIN + 'romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller'] )
    liste.append( ['Western',URL_MAIN + 'western'] )
	#la suite fonctionne mais pas de menu sur le site
    liste.append( ['Espionnage',URL_MAIN + 'espionnage'] )
    liste.append( ['Péplum',URL_MAIN + 'peplum'] )
    liste.append( ['Divers',URL_MAIN + 'divers'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:

        sType = oInputParameterHandler.getValue('type')

        sUrl = URL_SEARCH[0]

        oRequestHandler = cRequestHandler(URL_MAIN)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParameters('Referer', URL_MAIN)
        oRequestHandler.addParameters('do', 'search')
        oRequestHandler.addParameters('subaction', 'search')
        oRequestHandler.addParameters('story', sSearch)

        if (sType):
            if sType == 'serie':
                oRequestHandler.addParameters('catlist[]', '30')
            elif sType == 'film':
                oRequestHandler.addParameters('catlist[]', '3')

        sHtmlContent = oRequestHandler.request()

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<div class="fullstream fullstreaming">\s*<img src="([^><"]+)"[^<>]+alt="([^"<>]+)".+?<h3 class="mov-title"><a href="([^><"]+)">.+?<strong>(?:Qualité|Version)(.+?)<\/*strong>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[1]) == 0:
                    continue

            sThumb = str(aEntry[0])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            siteUrl = str(aEntry[2])
            sTitle = str(aEntry[1])
            sQual = cUtil().removeHtmlTags(str(aEntry[3]))
            sQual = sQual.replace(':', '').replace(' ', '').replace(',', '/')

            sDisplayTitle = sTitle + ' [' + sQual + ']'
            #sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):

    sPattern = '<a href="([^<>"]+)">Suivant &#8594;<\/a>'
    oParser = cParser()
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

    sPattern = '<i class="fa fa-play-circle-o"></i>([^<]+)</div>|<a href="([^<>"]+)" title="([^<]+)" target="seriePlayer".+?>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            sHosterUrl = str(aEntry[1])
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                try:
                    oHoster.setHD(sHosterUrl)
                except: pass
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)

                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
