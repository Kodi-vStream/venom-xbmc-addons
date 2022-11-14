# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons


import base64
import json
import re
import time
from datetime import datetime, timedelta

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.util import Quote

try:  # Python 2
    from urlparse import urlparse
except ImportError:  # Python 3
    from urllib.parse import urlparse


URL_MAIN = 'https://daddyhd.com/'
def GetUrlMain():
    return URL_MAIN


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'daddyhd'
SITE_NAME = 'DaddyHD'
SITE_DESC = 'Chaines de Sport et de Divertissement'


SPORT_SPORTS = ('/', 'load')
# TV_TV = ('/', 'load')
# SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showMovies')
#CHAINE_CINE = ('2370162-chaines-tv-streaming-tf1-france-2-canal-plus.html', 'showMovies')
# SPORT_LIVE = ('/', 'showMovies')
SPORT_GENRES = ('/', 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    # oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', CHAINE_CINE[0])
    # oGui.addDir(SITE_IDENTIFIER, CHAINE_CINE[1], 'Chaines TV Ciné', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    sUrl = GetUrlMain()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<h2 style="background-color:cyan">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        
        sportGenre = []
        
        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle in aResult[1]:
            if 'Schedule' in sTitle:
                break
            if 'Tv Show' in sTitle:
                continue
            
            sportGenre.append(sTitle)

        for sTitle in sorted(sportGenre):
            sDisplayTitle = sTitle
            sDisplayTitle = sDisplayTitle.replace('Soccer', 'Football')
            sDisplayTitle = sDisplayTitle.replace('Darts', 'Flechettes')
            sDisplayTitle = sDisplayTitle.replace('Boxing', 'Boxe')
            sDisplayTitle = sDisplayTitle.replace('Cycling', 'Cyclisme')
            sDisplayTitle = sDisplayTitle.replace('Horse Racing', 'Course de chevaux')
            sDisplayTitle = sDisplayTitle.replace('Ice Hockey', 'Hockey sur glace')
            sDisplayTitle = sDisplayTitle.replace('Rugby Union', 'Rugby à XV')
            sDisplayTitle = sDisplayTitle.replace('Sailing / Boating', 'Voile')
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)

            oGui.addLink(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'genres.png', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies():
    oGui = cGui()
    oParser = cParser()
    sUrl = GetUrlMain()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<h2 style="background-color:cyan">%s</h2>' % sTitle
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '</p>')


# <hr>16:00 Romania Liga 1 : CFR 1933 Timisoara vs. CS United Galati <span style="color: #ff0000;"><a style="color: #ff0000;" href="/stream/stream-401.php" target="_blank" rel="noopener">Digi Sport 2 Romania (CH-401)</a></span><br />
# <hr>21:00 Portugal 1a Divisao : Sporting CP vs. SC Braga/Aaum <span style="color: #ff0000;"><a style="color: #ff0000;" href="/stream/stream-21.php" target="_blank" rel="noopener">Canal 11 Portugal (CH-21)</a></span></p>

    sPattern = '<hr>(\d+:\d+) (.+?)<'#span.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        # total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sDate = aEntry[0]
            sTitle = aEntry[1]
#            sUrl2 = aEntry[2].replace('/stream/', '/embed/')
            sDisplayTitle = sDate + ' - ' + sTitle.strip()
            sTitle = sDate + ' ' + sTitle

            # if 'http' not in sUrl2:
            #     sUrl2 = urlMain[:-1] + sUrl2

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)

            oGui.addLink(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, 'sport.png', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oParser = cParser()
    urlMain = GetUrlMain()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(urlMain)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<hr>%s<' % sTitle
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '<br')

    sPattern = 'href="([^"]+).+?rel=".+?>([^\(]+)'
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '</p>')
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        # total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0].replace('/stream/', '/embed/')
            sDisplayTitle = sTitle + ' (' + aEntry[1].strip() + ')'

            if 'http' not in sUrl:
                sUrl = urlMain[:-1] + sUrl

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)

            oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    siterefer = oInputParameterHandler.getValue('siterefer')
    sHosterUrl = ''

    bvalid, shosterurl = getHosterIframe(sUrl, siterefer)
    if bvalid:
        sHosterUrl = shosterurl
        

    if sHosterUrl:
        sHosterUrl = sHosterUrl.strip()
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster is not False:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


# Traitement générique
def getHosterIframe(url, referer):
    
    if not url.startswith('http'):
        url = GetUrlMain( )+ url
    
    oRequestHandler = cRequestHandler(url)
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False, False

    # import xbmcvfs
    # f = xbmcvfs.File('special://userdata/addon_data/plugin.video.vstream/test.txt','w')
    # f.write(sHtmlContent)
    # f.close()

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        code = aResult[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
            return True, code + '|Referer=' + url
        except Exception as e:
            pass
    
    sPattern = '<iframe src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        referer = url
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//'+referer.split('/')[2] + url  # ajout du nom de domaine
                url = "https:" + url
            b, url = getHosterIframe(url, referer)
            if b:
                return True, url

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return True, url # + '|User-Agent=' + UA + '&Referer=' + referer

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return True, aResult[0] + '|referer=' + url

    return False, False
