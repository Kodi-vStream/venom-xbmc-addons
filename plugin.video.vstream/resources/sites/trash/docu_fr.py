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

SITE_IDENTIFIER = 'docu_fr'
SITE_NAME = 'Docu Fr'
SITE_DESC = 'Documentaire streaming sur YT'

URL_MAIN = 'https://docu-fr.com/'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
THUMBDEF = 'https://github.com/Kodi-vStream/venom-xbmc-addons/raw/Beta/plugin.video.vstream/resources/art/doc.png'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

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
    liste.append( ['Animaux', URL_MAIN + 'category/animaux/'] )
    liste.append( ['Art', URL_MAIN + 'category/art/'] )
    liste.append( ['Ecologie', URL_MAIN + 'category/ecologie'] )
    liste.append( ['Histoire', URL_MAIN + 'category/histoire/'] )
    liste.append( ['Santé', URL_MAIN + 'category/sante/'] )
    liste.append( ['Sciences', URL_MAIN + 'category/sciences/'] )
    liste.append( ['Société', URL_MAIN + 'category/societe/'] )
    liste.append( ['Technologie', URL_MAIN + 'category/technologie/'] )
    liste.append( ['Voyage', URL_MAIN + 'category/voyage/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'doc.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#8217;', '\'').replace('&#8212;', '-').replace('&laquo;', '<<').replace('&raquo;', '>>').replace('&nbsp;', '').replace('&hellip;','...')

    #if 'category' in sUrl or sSearch:
    sPattern = 'class="post-title".+?<a href="([^"]+)"\s*rel="bookmark">([^<]+)<\/a>.+?class="post-excerpt">\s*<p>(.+?)<\/p>'


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


            sUrl2 = aEntry[0]
            if 'private-video' in sUrl2:
                continue
                
            sTitle = aEntry[1]
            sDesc = aEntry[2]
            # thumb 
            sThumb = THUMBDEF
            thumb = re.search('<div class="post-thumbnail".+?<a href="'+sUrl2+'"\s*class="post-list-item-thumb\s*">\s*<img\s*width=.+?src="([^"]+)"',sHtmlContent,re.DOTALL)
            if thumb:
                sThumb = thumb.group(1)


            sDesc = re.sub('<a\s*class="read-more".+','' ,sDesc).replace('<br />','')
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<div\s*class="next-navigation"><a href="([^"]+)"\s*>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters(): #YT pas vu un autre hébergeur
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in list(set(aResult[1])):
            sHosterUrl = str(aEntry)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
