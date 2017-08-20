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

SITE_IDENTIFIER = 'videobuzzy_com'
SITE_NAME = 'Videobuzzy'
SITE_DESC = 'Sélection des vidéos les plus populaires de Videobuzzy'

URL_MAIN = 'http://www.videobuzzy.com/'

MOVIE_NETS = (URL_MAIN , 'showMovies')
NETS_NEWS =  (URL_MAIN + 'top-video.php', 'showMovies')
NETS_GENRES = (True, 'showGenres')

#URL_SEARCH = ('http://www.notre-ecole.net/?s=', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'

def load():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NETS[1], 'Vidéos du net', 'buzz.png',oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Vidéos du net (Genres)', 'genres.png',oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_MAIN + sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Galerie',URL_MAIN + 'galerie.htm'] )
    liste.append( ['Football',URL_MAIN + 'football.htm'] )
    liste.append( ['Humour',URL_MAIN + 'humour.htm'] )
    liste.append( ['Animaux',URL_MAIN + 'animaux.htm'] )
    liste.append( ['Insolite',URL_MAIN + 'insolite.htm'] )
    liste.append( ['Télévision',URL_MAIN + 'television.htm'] )
    liste.append( ['Musique',URL_MAIN + 'musique.htm'] )
    liste.append( ['Sport',URL_MAIN + 'sport.htm'] )
    liste.append( ['Cinéma',URL_MAIN + 'cinema.htm'] )
    #liste.append( ['Bref.',URL_MAIN + 'BREF-tous-les-episodes-de-la-serie-de-canal-+-4902.news'] )
    liste.append( ['Top Vidéo',URL_MAIN + 'top-video.php'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = "<a class='titre_news_index' href='(.+?)' title='(.+?)'>.+?<img class=\"thumbnail\" src='(.+?)'.+?>.+?<span class='corps_news_p2'>(.+?)</span>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)
    #print aResult
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?</span><a href="(.+?)" title=\'.+?\'>.+?</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        print aResult[1][0]
        return URL_MAIN + aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = 'file: "(.+?)", label: "(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry[0])
            sTitle = sMovieTitle + ' | ' + aEntry[1]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
