#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto et Arias800
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog
from resources.lib.util import cUtil

import re

SITE_IDENTIFIER = 'animeultime'
SITE_NAME = 'Anime-Ultime'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = 'http://www.anime-ultime.net/'

ANIM_VOSTFRS = (URL_MAIN + 'series-0-1/anime/0---', 'ShowAlpha')
SERIE_VOSTFRS = (URL_MAIN + 'series-0-1/drama/0---', 'ShowAlpha')
TOKUSATSU = (URL_MAIN + 'series-0-1/tokusatsu/0---', 'ShowAlpha')

URL_SEARCH = (URL_MAIN + 'search-0-1+', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addTV(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addTV(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés', 'animes.png', '', '', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addTV(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Dramas', 'series.png', '', '', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TOKUSATSU[0])
    oGui.addTV(SITE_IDENTIFIER, TOKUSATSU[1], 'Tokusatsu', 'vostfr.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText.replace(' ','+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def ShowAlpha(url = None):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (url == None):
        sUrl = oInputParameterHandler.getValue('siteUrl')
    else:
        sUrl = url

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="letter" href="([^"]+)">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sLetter = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [B][COLOR red]' + sLetter + '[/COLOR][/B]', 'listes.png', oOutputParameterHandler)

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

    oParser = cParser()
    if sSearch:
        sPattern = '<td class=".+?<a href="([^"]+)".+?<img src=([^>]+)/>.+?onMouseOut.+?>(.+?)</a>'
    else:
        sPattern = '<td class=".+?<a href="([^"]+)".+?<img src=([^>]+)/>.+?title="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    #Si il y a qu'un seule resultat alors le site fait une redirection.
    if (aResult[0] == False):
        if sSearch and not "sultats anime" in sHtmlContent:
            sTitle = re.search('<h1>([^<]+)',sHtmlContent).group(1)
            sUrl2 = sUrl
            sThumb = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        else:
            oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch:
                sTitle = re.sub('<.*?>', '', aEntry[2])
                sUrl2 = URL_MAIN + aEntry[0]
                sThumb = aEntry[1]
            else:
                sTitle = aEntry[2]
                sUrl2 = URL_MAIN + aEntry[0]
                sThumb = aEntry[1]

            #Enleve le contenu pour adulte.
            if 'Inderdit -' in sTitle or 'Public Averti' in sTitle  or 'Interdit' in sTitle:
                continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
      oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('showSeries')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    sDesc = ''
    try:
        sPattern = '<strong><br />([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<tr.+?align="left">.+?align="left">([^"]+)</td>.+?<a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[0]
            sUrl2 = URL_MAIN + aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    ids = sUrl.split('/')[4]
    oRequestHandler = cRequestHandler('https://v5.anime-ultime.net/VideoPlayer.html')
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addParameters('idfile',ids)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"([0-9p]+)".+?url":"(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sTitle = ('%s [%s]') % (sMovieTitle, aEntry[0])
            sHosterUrl = aEntry[1].replace('\\/','/')
            oHoster = cHosterGui().checkHoster("mp4")

            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
