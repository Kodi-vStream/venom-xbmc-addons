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

SITE_IDENTIFIER = 'libre_stream_org'
SITE_NAME = 'Libre-Streaming'
SITE_DESC = 'Films & Séries en streaming'

#URL_MAIN = 'http://libre-stream.com/'
URL_MAIN = 'http://ls-streaming.com/'

MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_QLT = (True, 'showQlt')

#SERIE_SERIES = (URL_MAIN + 'liste-des-series/', 'AlphaSearch')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'series/version-francaise/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QLT[1], 'Films (Qualités)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    #En panne au 14/06
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (VOSTFR)', 'series_vostfr.png', oOutputParameterHandler)

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
    liste.append( ['Action',URL_MAIN + 'films/action/'] )
    liste.append( ['Animation',URL_MAIN + 'films/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'films/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'films/biopic/'] )
    liste.append( ['Comédie',URL_MAIN + 'films/comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'films/comedie-dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'films/comedie-musicale/'] )
    liste.append( ['Disney',URL_MAIN + 'films/disney/'] )
    liste.append( ['Divers',URL_MAIN + 'films/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + 'films/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'films/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'films/horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'films/espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'films/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'films/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'films/guerre/'] )
    liste.append( ['Historiques',URL_MAIN + 'films/historique/'] )
    liste.append( ['Horreur',URL_MAIN + 'films/horreur/'] )
    liste.append( ['Musicale',URL_MAIN + 'films/musical/'] )
    liste.append( ['Policier',URL_MAIN + 'films/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'films/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'films/science-fiction/'] )
    liste.append( ['Spectacles',URL_MAIN + 'films/spectacles/'] )
    liste.append( ['Thriller',URL_MAIN + 'films/triller/'] )
    liste.append( ['Western',URL_MAIN + 'films/western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showQlt():
    oGui = cGui()

    liste = []
    liste.append( ['HD',URL_MAIN + 'films-hd/'] )
    liste.append( ['DvdRip',URL_MAIN + 'quality/dvdrip/'] )
    liste.append( ['BdRip',URL_MAIN + 'quality/bdrip/'] )
    liste.append( ['R5',URL_MAIN + 'quality/R5/'] )
    liste.append( ['Cam Rip',URL_MAIN + 'quality/camrip/'] )
    liste.append( ['TS',URL_MAIN + 'quality/ts/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0,36) :
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break

        if (i < 10):
            sTitle = chr(48+i)
        else:
            sTitle = chr(65+i-10)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.lower() + '.html' )
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]' + sTitle + '[/COLOR][/COLOR]', 'series_az.png', oOutputParameterHandler)

    cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def AlphaDisplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^<>"]+?)">([^<>"]+?)<\/a><br\/>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="libre-movie.+?data-src="(.+?)".+?title="(.+?)".+?onclick="window.location.href=\'(.+?)\'">.+?class="maskhr">Synopsis.+?</span>(.+?)</div>'
    if '/films' in sUrl:
        sPattern = sPattern + '.+?<div class="maskquality (.+?)">'
    if '/series' in sUrl:
        sPattern = sPattern + '.+?>Séries</a>.+?<a href=".+?">(.+?)</a>'

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
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[1]) == 0:
                    continue

            sTitle = str(aEntry[1])
            sDesc = str(aEntry[3])
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not '/series/' in sUrl and not '/films/' in sUrl:
                sDisplayTitle = sTitle

            if '/films/' in sUrl:
                sQual = str(aEntry[4])
                #on supprime [VOSTFR], [HD 720p] et DVDRIP du titre car affiche en tant que qualite sinon doublons
                sMovieTitle = sTitle.replace('[VOSTFR]', '').replace('[HD 720p]', '').replace('DVDRIP ', '')
                sDisplayTitle = sMovieTitle + ' [' + sQual + ']'

            if '/series/' in sUrl:
                if not '/vostfr/' in sUrl and not '/version-francaise/' in sUrl:
                    sLang = str(aEntry[4])
                    sLang = sLang.replace('Version Française', 'VF')
                    sDisplayTitle = sTitle + ' [' + sLang + ']'
                else:
                    sDisplayTitle = sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series/' in sUrl or '-saison-' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<>""]+?)"><i class="fa fa-angle-right"></i></a>'
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
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('http://creative.rev2pub.com', '')

    sPattern = '<iframe.+?src=[\'"]([^<>\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="e-number">.+?<iframe src="(.+?)".+?class="episode-id">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' ' + str(aEntry[1])

            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
