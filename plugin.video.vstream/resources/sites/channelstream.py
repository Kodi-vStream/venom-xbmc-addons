# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re
import json
import time
import resources.sites.freebox

from resources.lib.packer import cPacker
from resources.lib.comaddon import addon, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote

from datetime import datetime, timedelta

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channel Stream'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = "https://channelstream.es"
SPORT_SPORTS = (True, 'load')
SPORT_LIVE = (URL_MAIN + '/programme.php', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sFiltre = oInputParameterHandler.getValue('sFiltre')
    bAdulte = oInputParameterHandler.getValue('bAdulte')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix():
        sHtmlContent = sHtmlContent.replace('Ã®', 'î').replace('Ã©', 'é')

    sPattern = "colspan=\"7\".+?<b>([^<]+)<\/b>.+?location\.href = '([^']+).+?text-align.+?>(.+?)<\/td>.+?text-align.+?>([^<]+).+?text-align: left.+?>([^<]+).+?<span class=\"t\">([^<]+)<\/span>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[1]
            sDate = aEntry[2].replace('<br />', ' ')
            sdesc1 = aEntry[3]
            sdesc2 = aEntry[4]
            sTime = aEntry[5]

            sTitle = ''
            if sDate:
                try:
                    sDate +=  ' ' + sTime
                    d = datetime(*(time.strptime(sDate, '%Y-%m-%d %H:%M')[0:6]))
                    d +=  timedelta(hours=6)
                    sDate = d.strftime("%d/%m/%y %H:%M")
                except Exception as e:
                    pass
                sTitle += sDate +' '
            sTitle += ' - '

            if sdesc1:
                sTitle += sdesc1 + ' - ' + sdesc2 + ' - '
            sTitle += '(' + aEntry[0] + ')'
            sDisplayTitle = sTitle
            sDesc = sDisplayTitle
            sThumb = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "/programme.php" in sUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, sThumb, sDisplayTitle, oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sCat = 6
    sMeta = 0

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Double Iframe a passer.
    sPattern = "document\.getElementById\('video'\)\.src='([^']+)'.+?>([^<]+)<"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[1]:  # Pas de flux
        oGui.setEndOfDirectory()
        return

    for entry in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        iframeURL1 = entry[0]
        canal = entry[1]
        sMovieTitle = sTitle
        if canal not in sMovieTitle:
            sMovieTitle += ' [' + canal + ']'
            
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumbnail', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)

        oGuiElement = cGuiElement()
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setFileName(sMovieTitle)
        oGuiElement.setSiteName(resources.sites.freebox.SITE_IDENTIFIER)
        oGuiElement.setFunction('play__')
        oGuiElement.setIcon('tv.png')
        oGuiElement.setMeta(sMeta)
        oGuiElement.setThumbnail(sThumb)
        oGuiElement.setDirectTvFanart()
        oGuiElement.setCat(sCat)
        oGuiElement.setMeta(sMeta)

        if 'dailymotion' in iframeURL1:
            oOutputParameterHandler.addParameter('sHosterIdentifier', 'dailymotion')
            oOutputParameterHandler.addParameter('sMediaUrl', iframeURL1)
            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('sFileName', sMovieTitle)
            oGuiElement.setFunction('play')
            oGuiElement.setSiteName('cHosterGui')
            oGui.addHost(oGuiElement, oOutputParameterHandler)
            cGui.CONTENT = 'movies'
            oGui.setEndOfDirectory()
            return

        oRequestHandler = cRequestHandler(iframeURL1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        # oRequestHandler.addHeaderEntry('Referer', siterefer) # a verifier
        sHtmlContent = oRequestHandler.request()

        sHosterUrl = ''
        oParser = cParser()
        sPattern = '<iframe.+?src="([^"]+)'
        aResult2 = oParser.parse(sHtmlContent, sPattern)
        try:
            # Lien telerium qui ne marche pas, mais qui n'est pas toujours present
            iframeURL1 = aResult2[1][1]
        except:
            iframeURL1 = aResult2[1][0]

        oRequestHandler = cRequestHandler(iframeURL1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
    
        oParser = cParser()
        sPattern = '<iframe.+?src="([^"]+)'
        aResult2 = oParser.parse(sHtmlContent, sPattern)
    
        if aResult2[1]:
            sHosterUrl = Hoster_Wigistream(aResult2[1][0], iframeURL1)
            if sHosterUrl:
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
            
    cGui.CONTENT = 'files'
    oGui.setEndOfDirectory()


def Hoster_Wigistream(url, referer):
    url = url.strip()
    if not url.startswith('http'):
        url = 'http:'+url
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sUnpack = cPacker().unpack(sstr)
        sPattern = 'src="(.+?)"'
        aResult = re.findall(sPattern, sUnpack)
        if aResult:
            return aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False


def getRealTokenJson(link, referer):
    # cookies = {'elVolumen': '100', '__ga': '100'}

    # headers = {'Host': 'telerium.tv',
               # 'User-Agent': UA, 'Accept': 'application/json, text/javascript, */*; q=0.01',
               # 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'X-Requested-With': 'XMLHttpRequest',
               # 'Referer': referer}

    oRequestHandler = cRequestHandler(link)
    # oRequestHandler.addHeaderEntry('Host', 'telerium.tv')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    # oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
    oRequestHandler.addHeaderEntry('Accept-Language', 'pl,en-US;q=0.7,en;q=0.3')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', referer)
    oRequestHandler.addCookieEntry('elVolumen', '100')
    oRequestHandler.addCookieEntry('__ga', '100')
    realResp = oRequestHandler.request()
    return json.loads(realResp)


def getTimer():
    datenow = datetime.utcnow().replace(second=0, microsecond=0)
    datenow = datenow + timedelta(days=1)
    epoch = datetime(1970, 1, 1)

    return (datenow - epoch).total_seconds() // 1
