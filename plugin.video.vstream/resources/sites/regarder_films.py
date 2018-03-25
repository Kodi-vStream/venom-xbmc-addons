#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'regarder_films'
SITE_NAME = 'Regarder-films-gratuit'
SITE_DESC = 'Streaming ou Téléchargement de Séries & Mangas.'

URL_MAIN = 'http://regarder-film-gratuit.online/'

SERIE_NEWS = (URL_MAIN, 'showSeries')
SERIE_SERIES = (URL_MAIN, 'load')
SERIE_LIST = (URL_MAIN + 'liste-de-series/', 'showAlpha')

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
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste AZ)', 'series_az.png',oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<font color="red".+?>(.+?)<\/font>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sLetter = str(aEntry).replace('=', '')
            dAZ = str(aEntry)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('AZ', dAZ)
            oGui.addDir(SITE_IDENTIFIER, 'showAZ', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'series_az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    oRequestHandler = cRequestHandler(URL_MAIN + 'liste-de-series/')
    dAZ = oInputParameterHandler.getValue('AZ')
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    #Decoupage pour cibler la partie selectionnée
    sPattern = '<font color="red".+?>' + dAZ + '</font>(.+?)<p><strong>'
	
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    #regex pour listage series sur la partie decoupée
    sPattern = '<a href="([^"]+)".+?>(.+?)<\/a>'
    
    aResult = oParser.parse(aResult, sPattern)
    
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sUrl = str(aEntry[0])
            sTitle = str(aEntry[1]).decode("unicode_escape").encode("latin-1").replace('&#8217;', '\'').replace('&#8212;', '-')
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'series_az.png', oOutputParameterHandler)
            
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch

    else:
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    if 'streamzz' in sUrl:
        sPattern = '<li><a href="(http:..streamzzz.online\/page[^<]+)" title=".+?">([^<]+)<.a><.li>'
    else:
        sPattern = '<div class="post".+?<h2><a class="title" href="(.+?)" rel="bookmark">(.+?)</a></h2>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

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

            sTitle = aEntry[1]
            sUrl = str(aEntry[0])
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, 'series.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">..<'
    aResult = re.findall(sPattern,sHtmlContent,re.UNICODE)
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

    if 'streamzz' in sUrl:
		sPattern = '<div class="boton reloading"><a href="([^"]+)">'
    else:
        sPattern = '<center><.+?<stron.+?((?:VF|VOSTFR|VO)).+?trong>|<p><a href="([^"]+)".+?target="_blank">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sLang = aEntry[0].replace('&#8230;','').replace(':','')
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sLang + '[/COLOR]')
            else:
                sHosterUrl = aEntry[1]
                oHoster = cHosterGui().checkHoster(sHosterUrl)

                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
