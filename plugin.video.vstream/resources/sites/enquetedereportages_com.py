#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib import util
import re
import unicodedata

SITE_IDENTIFIER = 'enquetedereportages_com'
SITE_NAME = 'En quête de reportages'
SITE_DESC = 'replay tv'

URL_MAIN = 'http://enquetedereportages.com/'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_DOCS =('http://', 'load')
DOC_GENRES = (True, 'DocGenres')

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'ReplayTV')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Nouveautés', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Documentaires (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Replay (Genres)', 'genres.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
    
def DocGenres():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/documentaire/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/reportage/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Reportages', 'tv.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()  
    
def ReplayTV():

    oGui = cGui()
 
    liste = []
    liste.append( ['Discovery',URL_MAIN + 'category/discovery-channel/'] )
    liste.append( ['Emission',URL_MAIN + 'category/emission/'] )
    liste.append( ['France2',URL_MAIN + 'category/france-2/'] )
    liste.append( ['France3',URL_MAIN + 'category/france-3/'] )
    liste.append( ['France4',URL_MAIN + 'category/france-4/'] )
    liste.append( ['FranceO',URL_MAIN + 'category/france-o/'] )
    liste.append( ['M6',URL_MAIN + 'category/m6/'] )
    liste.append( ['NRJ12',URL_MAIN + 'category/nrj12/'] )
    liste.append( ['NT1',URL_MAIN + 'category/nt1/'] )
    liste.append( ['RMC',URL_MAIN + 'category/rmc-decouvertes/'] )
    liste.append( ['SportMeca',URL_MAIN + 'category/sports-meca/'] )
    liste.append( ['TF1',URL_MAIN + 'category/tf1/'] )
    liste.append( ['TMC',URL_MAIN + 'category/tmc/'] )
    liste.append( ['W9',URL_MAIN + 'category/w9/'] )
    liste.append( ['Autre',URL_MAIN + 'category/uncategorized/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showMoviesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False and sSearchText != 'bad'): #le mot bad seul fait planté kodi
        sUrl = URL_MAIN + '?s=' + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Infrarouge',URL_MAIN + 'category/documentaire/infrarouge/'] )
    liste.append( ['Arte',URL_MAIN + 'category/documentaire/arte/'] )
    liste.append( ['France4',URL_MAIN + 'category/documentaire/france-4-documentaire/'] )
    liste.append( ['France5',URL_MAIN + 'category/france-5/'] )
    liste.append( ['13eme-rue',URL_MAIN + 'category/reportage/13eme-rue/'] )
    liste.append( ['23eme',URL_MAIN + 'category/reportage/23eme/'] )
    liste.append( ['6ter',URL_MAIN + 'category/reportage/6ter/'] )
    liste.append( ['Canal+',URL_MAIN + 'category/reportage/canal/'] )
    liste.append( ['D8',URL_MAIN + 'category/reportage/d8/'] )
    
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
    sHtmlContent = oRequestHandler.request()

    sPattern = '<article class="pexcerpt.+?"><a href="(.+?)" title="(.+?)".+?<img.+?src="(.+?)".+?/></div>.+?<div class="post-content image-caption-format-1">(.+?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = unicode(aEntry[1], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            #sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")

            #sTitle = re.sub('([0-9]+/[0-9]+/[0-9]+)','[COLOR teal]\\1[/COLOR]', str(sTitle))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            sTitle = sTitle.replace('http://enquetedereportages.com/','')
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', aEntry[2], aEntry[3], oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):

    sPattern = "class='page-numbers current'>.+?<a class='page-numbers' href='(.+?)'>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl
 
    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<p><iframe src="(.+?)".+?></iframe></p>'
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
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
