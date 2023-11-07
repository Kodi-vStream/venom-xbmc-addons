# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re
import time
import resources.sites.freebox

from resources.lib.packer import cPacker
from resources.lib.comaddon import isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Quote, urlHostName

from datetime import datetime, timedelta

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channel Stream'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_SPORTS = (True, 'load')
SPORT_LIVE = ('/programme.php', 'showMovies')

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
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix():
        sHtmlContent = sHtmlContent.replace('Ã®', 'î').replace('Ã©', 'é')

    # récupérer les drapeaux pour en faire des thumb
    sPattern = "\.flag\.([^{]+){.+?url\(([^)]+)\)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    flags = dict(aResult[1])

    sPattern = "colspan=\"7\".+?<b>([^<]+)<\/b>.+?location\.href = '([^']+).+?text-align.+?>(.+?)<\/td>.+?<span class=\"flag ([^\"]+).+?text-align.+?>([^<]+).+?text-align: left.+?>([^<]+).+?<span class=\"t\">([^<]+)<\/span>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[1]
            sDate = aEntry[2].replace('<br />', ' ')
            flag = aEntry[3]
            sdesc1 = aEntry[4]
            sdesc2 = aEntry[5]
            sTime = aEntry[6]

            sThumb = flags.get(flag)
            sTitle = ''
            if sDate:
                try:
                    sDate += ' ' + sTime
                    d = datetime(*(time.strptime(sDate, '%Y-%m-%d %H:%M')[0:6]))
                    d += timedelta(hours=6)
                    sDate = d.strftime("%d/%m/%y %H:%M")
                except Exception as e:
                    pass
                sTitle = sDate + ' - '

            if sdesc1:
                sTitle += sdesc1 + ' - ' + sdesc2 + ' - '
            sTitle += '(' + aEntry[0] + ')'
            sDisplayTitle = sTitle
            sDesc = sDisplayTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addLink(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if not sUrl.startswith ('http'):
        sUrl = URL_MAIN + sUrl
    else:   # remplacer par la bonne adresse
        domain = urlHostName(sUrl)
        sUrl = sUrl.replace('https://' + domain, URL_MAIN)

    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sCat = 6
    sMeta = 0

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setTimeout(8)
    sHtmlContent = oRequestHandler.request()

    # Double Iframe a passer.
#    sPattern = "document\.getElementById\('video'\)\.src='([^']+)'.+?>([^<]+)<"
    sPattern = 'document\.getElementById\(\'video\'\)\.src=\'([^\']+)\'.+?>([^<]+)<.+?<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[1]:  # Pas de flux
        oGui.setEndOfDirectory()
        return

    for entry in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        
        iframeURL1 = entry[2]
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

        # if 'dailymotion' in iframeURL1:
        #     oOutputParameterHandler.addParameter('sHosterIdentifier', 'dailymotion')
        #     oOutputParameterHandler.addParameter('sMediaUrl', iframeURL1)
        #     oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)  # variable manquante
        #     oOutputParameterHandler.addParameter('sFileName', sMovieTitle)
        #     oGuiElement.setFunction('play')
        #     oGuiElement.setSiteName('cHosterGui')
        #     oGui.addHost(oGuiElement, oOutputParameterHandler)  # addHost absent ???? del 20/08/2021
        #     cGui.CONTENT = 'movies'
        #     oGui.setEndOfDirectory()
        #     return

        oRequestHandler = cRequestHandler(iframeURL1)
        oRequestHandler.setTimeout(8)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        # oRequestHandler.addHeaderEntry('Referer', siterefer) # a verifier
        sHtmlContent = oRequestHandler.request()

        sHosterUrl = ''
        oParser = cParser()
        sPattern = '<iframe.+?src="([^"]+)'
        aResult2 = oParser.parse(sHtmlContent, sPattern)

        if not aResult2[0]:
            sPattern = "playStream\('iframe','([^']+)'\)"
            aResult2 = oParser.parse(sHtmlContent, sPattern)

        if aResult2[0]:
            iframeURL1 = aResult2[1][0]
    
            if 'cloudstream' in iframeURL1:
                sHosterUrl = getHosterWigistream(iframeURL1, sUrl)
    
            if not sHosterUrl:
                oRequestHandler = cRequestHandler(iframeURL1)
                oRequestHandler.setTimeout(2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent = oRequestHandler.request()
    
                oParser = cParser()
                sPattern = '<iframe.+?src="([^"]+)'
                aResult2 = oParser.parse(sHtmlContent, sPattern)
    
                if aResult2[0]:
                    urlHoster = aResult2[1][0]
                    if 'primetubsub' in urlHoster or 'sportcast' in urlHoster:
                        sHosterUrl = getHosterPrimetubsub(urlHoster, iframeURL1)
                    else:
                        sHosterUrl = getHosterWigistream(urlHoster, iframeURL1)

        if not sHosterUrl:
            sHosterUrl = getHosterIframe(iframeURL1, sUrl)

        if sHosterUrl:
            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    cGui.CONTENT = 'files'
    oGui.setEndOfDirectory()


def getHosterWigistream(url, referer):
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

    else:
        sPattern = "source:'(.+?)'"
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            return aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False


def getHosterPrimetubsub(url, referer):
    oParser = cParser()

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return

    referer = url
    url = aResult[1][0]

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()
    sPattern = "(src|[^/]source):'([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        return

    referer = url
    url = aResult[1][0][1]

    return url + '|User-Agent=' + UA + '&Referer=' + Quote(referer)


# Traitement générique
def getHosterIframe(url, referer):

    if not url.startswith('http'):
        url = URL_MAIN + url

    oRequestHandler = cRequestHandler(url)
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    referer = url
    
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
        for code in aResult:
            try:
                if isMatrix():
                    code = base64.b64decode(code).decode('ascii')
                else:
                    code = base64.b64decode(code)
                if '.m3u' in code:
                    return code + '|Referer=' + referer
            except Exception as e:
                pass
    
    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//'+referer.split('/')[2] + url  # ajout du nom de domaine
                url = "https:" + url
            url = getHosterIframe(url, referer)
            if url:
                return url

    sPattern = 'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            referer = url
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return sHosterUrl + '|referer=' + referer

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return url

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
#        sHosterUrl = sHosterUrl.replace('index', 'mono')
        return sHosterUrl + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return sHosterUrl + '|referer=' + referer

    return False


