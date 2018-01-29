#-*- coding: utf-8 -*-
#Venom.
#desactiver le 13/11
return False
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

URL_MAIN = 'http://www.regarder-film-gratuit.eu/'

SERIE_NEWS = (URL_MAIN + 'category/series/', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'liste-de-series/', 'showAlpha')

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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Liste AZ)', 'series_az.png',oOutputParameterHandler)

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
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="main">(.+?)<div id="comments">'
    aResult = re.search(sPattern,sHtmlContent,re.DOTALL)
    if (aResult):
        sHtmlContent = aResult.group(1)

    sPattern = '<font color="red".+?>\=(.+?)\=<\/font>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sLetter = str(aEntry)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('AZ', sLetter)
            oGui.addDir(SITE_IDENTIFIER, 'showAZ', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'series_az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    dAZ = oInputParameterHandler.getValue('AZ')

    oRequestHandler = cRequestHandler(URL_MAIN + 'liste-de-series/')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^"]+)".+?>(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True) :
        for aEntry in aResult[1]:
            uaE = cUtil().CleanName(aEntry[1])
            if uaE.upper()[0] == dAZ or aEntry[1][0].isdigit() and dAZ == '0-9':

               sUrl = aEntry[0]
               sTitle =  aEntry[1]
               if 'Liste de' in sTitle:
                    continue
               oOutputParameterHandler = cOutputParameterHandler()
               oOutputParameterHandler.addParameter('siteUrl', sUrl)
               oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
               oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'series_az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        showSeries()
        return
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('Programme', '').replace('F.A.Q', '').replace('Séries', '')
    sPattern = '<li class="cat-item cat-item-.+?"><a href="(.+?)">([^<]+)</a>'
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

            sTitle = str(aEntry[1])
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/series-tv/' in sUrl or 'saison' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, 'series.png', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    if not sSearch:
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
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[1]) == 0:
                    continue

            sTitle = aEntry[1]
            sUrl = str(aEntry[0])
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            if ('Information' not in sTitle) and ('/liste-de-series/' not in sUrl) and ('/versions-francaises/' not in sUrl):
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
    sThumbnail = ''
    sPattern = '<p><img src="([^"]+)" *alt=".+?".+?><\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumbnail = aResult[1][0]

    if 'streamzz' in sUrl:
		sPattern = '<div class="boton reloading"><a href="([^"]+)">'
    else:
        sPattern = '<span id=.+?<stron.+?((?:VF|VOSTFR|VO)).+?trong>|<p><a href="([^"]+)".+?target="_blank">'
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
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
