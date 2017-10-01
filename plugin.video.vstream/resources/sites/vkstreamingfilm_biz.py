#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,urllib2,urllib

SITE_IDENTIFIER = 'vkstreamingfilm_biz'
SITE_NAME = 'Vk Streaming Film'
SITE_DESC = 'Film en Streaming HD'

URL_MAIN = 'http://www.vkstreamingfilm.co/'

MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'lastnews', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
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
    liste.append( ['Action',URL_MAIN + 'films/action/'] )
    liste.append( ['Animation',URL_MAIN + 'films/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'films/aventure/'] )
    liste.append( ['Biographique',URL_MAIN + 'films/biographique/'] )
    liste.append( ['Comédie',URL_MAIN + 'films/comedie/'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'films/comedie-dramatique/'] )
    liste.append( ['Danse',URL_MAIN + 'films/danse/'] )
    liste.append( ['Divers',URL_MAIN + 'films/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + 'films/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'films/drame/'] )
    liste.append( ['Epouvante-Horreur',URL_MAIN + 'films/epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'films/espionnage/'] )
    liste.append( ['Fantastique',URL_MAIN + 'films/fantastique/'] )
    liste.append( ['Famille',URL_MAIN + 'films/famille/'] )
    liste.append( ['Guerre',URL_MAIN + 'films/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'films/historique/'] )
    liste.append( ['Musical',URL_MAIN + 'films/musical/'] )
    liste.append( ['Péplum',URL_MAIN + 'films/peplum/'] )
    liste.append( ['Policier',URL_MAIN + 'films/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'films/romance/'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'films/science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + 'films/spectacle/'] )
    liste.append( ['Sport',URL_MAIN + 'films/sport/'] )
    liste.append( ['Thriller',URL_MAIN + 'films/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'films/western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        #on redecode la recherche codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)
        sSearch = sSearch.replace(' ', '%20')
        query_args = {'do' : 'search' , 'subaction' : 'search' , 'story' : str(sSearch) , 'x' : '0', 'y' : '0'}

        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = URL_MAIN + 'index.php?do=search=' + sSearch
        request = urllib2.Request(url, data, headers)

        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason

        sHtmlContent = reponse.read()
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="img-block border-2">.*?<img src="(.*?)".*?<h5><a href="([^"]+)".+?>(.+?)</a>'

    oParser = cParser()
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
                if cUtil().CheckOccurence(sSearch, aEntry[2]) == 0:
                    continue

            sTitle = str(aEntry[2])
            sUrl2 = str(aEntry[1])
            sThumb = str(aEntry[0])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):

    sPattern = '<div class="navigation">(?:<a href="http:[^<>]+?">[0-9]+<\/a> )*<span>[0-9]+<\/span> <a href="(.+?)">'
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

    oParser = cParser()

    #Recuperation qualitee
    sQual = ''
    sPattern = '<b>QualitÃ© :<\/b><\/span> +?<p class="text">([^<>()|]+)(?:\(.+?\))*[ |]*.+?<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sQual = ' [' + aResult[1][0] + ']'
        sQual = sQual.replace('VF', '').replace('VOSTFR', '')
        sQual = sQual.replace(' ]', ']')

    #Recup langue
    sLang = ''
    sPattern = '<a href="#(video[0-9]+?)" title=".+?" class="border-3"><span>.+?(\[.+?\])<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sLang = aResult[1]

    sPattern = '<div class="fstory-video-block" id="(.+?)">.+?<iframe.+?src=[\'|"](.+?)[\'|"]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sMovieTitle = sMovieTitle + sQual

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sMovieTitle2 = sMovieTitle
            #Rajout langue
            for aEntry9 in sLang:
                if aEntry9[0] == aEntry[0]:
                    sMovieTitle2 = '%s %s' % (sMovieTitle, aEntry9[1])

            sHosterUrl = str(aEntry[1])
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            #sMovieTitle2 = sMovieTitle2

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle2)
                oHoster.setFileName(sMovieTitle2)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()
