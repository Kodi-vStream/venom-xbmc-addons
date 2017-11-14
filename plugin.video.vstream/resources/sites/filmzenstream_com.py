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
from resources.lib.sucuri import SucurieBypass
import re,urllib

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

SITE_IDENTIFIER = 'filmzenstream_com'
SITE_NAME = 'Filmzenstream'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = 'https://filmzenstream.com/'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_MOVIE = (URL_MAIN , 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action/Aventure',URL_MAIN + 'action/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'crime/'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Etranger',URL_MAIN + 'etranger/'] )
    liste.append( ['Famille',URL_MAIN + 'familial/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'horreurr/'] )
    liste.append( ['Musique',URL_MAIN + 'musique/'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science-fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Téléfilm',URL_MAIN + 'telefilm/'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller/'] )
    liste.append( ['Western',URL_MAIN + 'western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()

    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = '<h3>Année de sortie'
    sEnd = '<h3>Qualité'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ','+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    #sHtmlContent = SucurieBypass().GetHtml(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class="item"> *<a href="([^<]+)">.+?<img src="([^<>"]+?)" alt="([^"]+?)".+?<span class="calidad2">(.+?)<\/span>'
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

            sName = str(aEntry[2])#.replace(' Streaming Ultra-HD', '').replace(' Streaming Full-HD', '')
#            sName = sName.replace(' en Streaming HD', '').replace(' Streaming HD', '').replace(' streaming HD', '')
#            sName = sName.decode('utf8')
#            sName = cUtil().unescape(sName)
#            try:
#                sName = sName.encode("utf-8")
#            except:
#                pass

            sTitle = sName + ' [' + aEntry[3] + ']'
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH_MOVIES[0], ''), sName) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sName)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^"]+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHtmlContent = SucurieBypass().GetHtml(sUrl)

    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="//www.youtube.com/', '')

    sPattern = '<iframe.+?src="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'belike.pw' in aEntry:
                #print 'belike redirection'
                if aEntry.startswith('/'):
                    oRequestHandler = cRequestHandler('https:' + str(aEntry))
                else:
                    oRequestHandler = cRequestHandler(str(aEntry))
                sHtmlContent = oRequestHandler.request()
                sPattern = '{file: "(.+?)", type: ".+?", label: "'
                aResult = oParser.parse(sHtmlContent, sPattern)
                #print aResult
                if (aResult[0] == True):
                    sHosterUrl = aResult[1][0]

            else:
                sHosterUrl = str(aEntry)
            #print sHosterUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
