#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress
import re

SITE_IDENTIFIER = 'regarder_films'
SITE_NAME = 'Regarder-films-gratuit'
SITE_DESC = 'Série streaming gratuit illimité vf et vostfr.'

URL_MAIN = 'http://regarder-film-gratuit.online/'

SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_SERIES = (URL_MAIN, 'load')
SERIE_LIST = (URL_MAIN + 'liste-de-series/', 'showAlpha')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png',oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showAlpha():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(SERIE_LIST[0])
    sHtmlContent = oRequestHandler.request()

    sPattern = '<font color="red".+?>(.+?)<\/font>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sLetter = str(aEntry).replace('=', '')
            dAZ = str(aEntry)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('dAZ', dAZ)
            oGui.addDir(SITE_IDENTIFIER, 'showList', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'az.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showList():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    oRequestHandler = cRequestHandler(SERIE_LIST[0])
    dAZ = oInputParameterHandler.getValue('dAZ')
    sHtmlContent = oRequestHandler.request()
    
    #Decoupage pour cibler la partie selectionnée
    sPattern = '<font color="red".+?>' + dAZ + '</font>(.+?)<p><strong>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #regex pour listage series sur la partie decoupée
    sPattern = '<a href="([^"]+)".+?>(.+?)<\/a>'
    aResult = oParser.parse(aResult, sPattern)
    
    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sUrl = str(aEntry[0])
            #on filtre, les liens streamzzz.online sont hs
            if 'streamzzz' in sUrl:
                continue
            sTitle = str(aEntry[1]).decode("unicode_escape").encode("latin-1").replace('&#8217;', '\'').replace('&#8212;', '-')
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'az.png', oOutputParameterHandler)
            
        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Dessin animés', URL_MAIN + 'category/dessins-animes/'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire/'] )
    liste.append( ['News', URL_MAIN + 'category/news/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
      sUrl = sSearch

    else:
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="post".+?<h2><a class="title" href="(.+?)" rel="bookmark">(.+?)</a>.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[1]) == 0:
                    continue

            sUrl = str(aEntry[0])
            sTitle = str(aEntry[1]).replace('&#8212;', '-').replace('&#8217;', '\'')
            sThumb = str(aEntry[2])
            #on filtre, les liens streamzzz.online sont hs
            if 'streamzzz' in sThumb:
                continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">..<'
    aResult = re.findall(sPattern, sHtmlContent, re.UNICODE)
    if (aResult):
        return aResult[0]

    return False

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    #recuperation thumb
    sThumb = ''
    sPattern = '<p><img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumb = aResult[1][0]

    #if 'streamzz' in sUrl:
        #sPattern = '<div class="boton reloading"><a href="([^"]+)">'
    #else:
    sPattern = '<center><.+?<stron.+?((?:VF|VOSTFR|VO)).+?trong>|<p><a href="([^"]+)".+?target="_blank">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                sLang = aEntry[0].replace('&#8230;', '').replace(':', '')
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sLang + '[/COLOR]')
            else:
                sHosterUrl = aEntry[1]
                oHoster = cHosterGui().checkHoster(sHosterUrl)

                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
