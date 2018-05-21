#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re

SITE_IDENTIFIER = 'streaming_series_org'
SITE_NAME = 'Streaming Séries'
SITE_DESC = 'Séries en streaming vf gratuitement sur Série Streaming'

URL_MAIN = 'http://www.seriestreaming.watch/'

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = ('http://', 'load')
SERIE_VFS = (URL_MAIN + 'version-francaise-vf/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'version-francaise-vf/?sort=views', 'showMovies')
SERIE_COMMENTS = (URL_MAIN + 'version-francaise-vf/?sort=comments', 'showMovies')


URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerieSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus Vues)', 'series_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus Commentées)', 'series_comments.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showListe', 'Séries (Liste)', 'series.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSerieSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_SEARCH[0] + sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return
            
def showListe():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<li class="cat-item cat-item-.+?"><a href="([^"]+)" *>(.+?)<\/a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[1])
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', aEntry[1], 'series.png', oOutputParameterHandler)

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
   
    sPattern = '<div class="movie-poster">.+?<a href="(.+?)">.+?<img src="(.+?)" alt="(.+?)"'

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
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[0]) == 0:
                    continue


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumb', aEntry[1])

            oGui.addTV(SITE_IDENTIFIER, 'showSeries', aEntry[2], '', aEntry[1], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<div class=".+?oadnavi.+?"></div><a href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries():#episode
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent,'<div class="single-content video">','</div></div></div></div>')
    #active hidden
    sHtmlContent = re.sub('<div class="part-name">(?:Part 1|Épisode 1)</div>','<a href="'+sUrl+'"><div class="part "> <div class="part-name">episode 1</div>',sHtmlContent)

    sPattern = '<a href="(.+?)"><div class="part ">.+?<div class="part-name">(.+?)<\/div>' #vire non épisode

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1].replace('\xc3\x89pisode','episode')
            sTitle = sTitle.replace('Part','episode')
            sTitle = sMovieTitle + sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')
    sHtmlContent = sHtmlContent.replace('\r', '')
    sHtmlContent = sHtmlContent.replace('VF</strong>','VF</b>')

    sPattern = '(VF|VOSTFR)<\/b><\/p>|<iframe.+?=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #langue
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            #episode
            else:
                sHosterUrl = str(aEntry[1])
                if '//goo.gl' in sHosterUrl:
                    import urllib2
                    try:

                        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                        request = urllib2.Request(sHosterUrl, None, headers)
                        reponse = urllib2.urlopen(request)
                        sHosterUrl = reponse.geturl()
                    except:
                        pass

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
