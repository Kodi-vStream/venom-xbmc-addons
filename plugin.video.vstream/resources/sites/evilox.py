#-*- coding: utf-8 -*-
#Venom.kodigoal
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.player import cPlayer
from resources.lib import util

import unicodedata

SITE_IDENTIFIER = 'evilox'
SITE_NAME = 'Evilox'
SITE_DESC = 'Vidéos drôles, du buzz, des fails et des vidéos insolites'

URL_MAIN = 'http://fr.evilox.com/'

URL_SEARCH = (URL_MAIN , 'showMovies')
URL_SEARCH_MISC = (URL_MAIN , 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN + 'videos/', 'showMovies')
NETS_GENRES = (True, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Vidéos (Derniers Ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Vidéos (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Animaux', URL_MAIN + 'videos/animaux/'] )
    liste.append( ['Automoto', URL_MAIN + 'videos/automoto/'] )
    liste.append( ['Avions', URL_MAIN + 'videos/avions/'] )
    liste.append( ['Crash', URL_MAIN + 'videos/crash/'] )
    liste.append( ['Dédicaces', URL_MAIN + 'videos/dedicaces/'] )
    liste.append( ['Gags', URL_MAIN + 'videos/gags/'] )
    liste.append( ['Jeux', URL_MAIN + 'videos/jeux/'] )
    liste.append( ['Ludiques', URL_MAIN + 'videos/ludiques/'] )
    liste.append( ['People', URL_MAIN + 'videos/people/'] )
    liste.append( ['Pubs', URL_MAIN + 'videos/pubs/'] )
    liste.append( ['Sport', URL_MAIN + 'videos/sport/'] )
    liste.append( ['Travail', URL_MAIN + 'videos/travail/'] )
    liste.append( ['Zapping', URL_MAIN + 'videos/zapping/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
        oRequestHandler = cRequestHandler(URL_MAIN)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParameters('search',sSearch)
        oRequestHandler.addParameters('type_new','')
        #oRequestHandler.addHeaderEntry('Cookie',cookies))
        sHtmlContent = oRequestHandler.request()
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = "<div class='m2'>.+?<a href='(.+?)'><div style='.+?image:url\((.+?)\);position:relative;' class='.+?' alt='(.+?)' id='.+?'.+?<span class='videoduree'>([^<]+)</span>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sTitle = unicode(aEntry[2], 'latin-1')
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')
            sTitle = ('%s') % (sTitle)

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if util.cUtil().CheckOccurence(sSearch,sTitle) == 0:
                    continue

            sUrl    = str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sTime = str(aEntry[3])

            sDisplayTitle = ('%s (%s)') % (sTitle, sTime)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "<a href='([^']+)'>Suivante[^<]+</a>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()

    #lien direct flv
    sPattern = "file=(http.+?\.flv)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl =  cUtil().urlDecode(str(aEntry))

        #On lance la vidéo directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return

    else:
        return

    oGui.setEndOfDirectory()
