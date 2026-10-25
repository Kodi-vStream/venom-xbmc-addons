# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import time
import re

SITE_IDENTIFIER = 'witv'
SITE_NAME = 'witv'
SITE_DESC = 'Chaines TV en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


SPORT_SPORTS = ('chaines-live/sport/', 'showTV')
SPORT_TV = ('chaines-live/sport/', 'showTV')

#DOC_DOCS = (True, 'load')
DOC_TV = ('chaines-live/documentaire/', 'showTV')
KID_TV = ('chaines-live/enfants/', 'showTV')
    
def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines sportives', 'sport.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', DOC_TV[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_TV[1], 'Chaines documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_TV[0])
    oGui.addDir(SITE_IDENTIFIER, KID_TV[1], 'Chaines jeunesse', 'enfants.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()
    oParser = cParser()
    oUtil = cUtil()

    oInputParameterHandler = cInputParameterHandler()
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    siteUrl = URL_MAIN + siteUrl
    oRequestHandler = cRequestHandler(siteUrl)
    sHtmlContent = oRequestHandler.request()
    
    # url title thumb
    sPattern = 'Live<\/span>    <a href="([^"]+).+?class="ann-short_price">([^<]+).+?src="([^"]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    oOutputParameterHandler = cOutputParameterHandler()
    if aResult[0]:

        # on ajoute canal+ dans les chaines sportives
        if SPORT_TV[0] in siteUrl:
            aResult[1].append(['chaines-live/23-canal.html', 'CANAL +', 'images/logo/canal-plus-logo.png'])
        
        result = sorted(aResult[1], key = lambda chaine : chaine[1])
        for aEntry in result:
            sUrl = aEntry[0]
            sTitle = aEntry[1].split('-')[0].strip()
            if aEntry[2]:
                sThumb = URL_MAIN + aEntry[2]
            else:
                sThumb = oUtil.getIconDefault(sTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showLink', sTitle, sThumb, sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    import json

    oGui = cGui()
    oParser = cParser()
    oHosterGui = cHosterGui()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, 'id="player\d" data-v="([^"]+)')

    import xbmcvfs
    f = xbmcvfs.File('special://userdata/addon_data/plugin.video.vstream/test.txt','w')
    f.write(sHtmlContent)
    f.close()

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        sUrlDecode = URL_MAIN + 'ajax_player.php'
        oRequest = cRequestHandler(sUrlDecode)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Referer', sUrl)
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    
        html = oParser.abParse(sHtmlContent, '(function(){var _a=', '</script>')

        for dataV in aResult[1]:
            fx_k, _sl, _mu, _in = getFk(sHtmlContent)
            fx_s = getFs(fx_k, _sl, _mu, _in, dataV)
    
            postdata = 'k=%s&b=1&t=1&s=%s&v=%s' % (fx_k, fx_s, dataV)
            oRequest.addParametersLine(postdata)
            ret = oRequest.request()
            if ret.startswith('{'):
                ret = json.loads(ret)
                sHosterUrl = ret.get('u', '')
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addLink(SITE_IDENTIFIER, 'showHoster', sMovieTitle, sThumb, sMovieTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = 'https://witv.eu/player/source2/?id=960'

    sUrl += '&t=%d' % int(time.time() * 1000)

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-url="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for sHosterUrl in aResult[1]:
            
            if '.php?' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern = 'iframe.+?src *= *"([^"]+)'
                aResult2 = oParser.parse(sHtmlContent, sPattern)
                if not aResult2[0]:
                    continue
                sHosterUrl = aResult2[1][0]
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern = 'streamUrl: *"([^"]+)'
                aResult3 = oParser.parse(sHtmlContent, sPattern)
                if aResult3[0]:
                    sHosterUrl = aResult3[1][0]
            
            oHoster = oHosterGui.checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showLink_OLD():
    oGui = cGui()
    oParser = cParser()
    oHosterGui = cHosterGui()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, '<iframe src="([^"]*)" data-src="([^"]+)')

    if aResult[0]:
        for links in aResult[1]:
            sHosterUrl = links[0]
            if not sHosterUrl:
                sHosterUrl = links[1]
            if sHosterUrl.startswith('/'):
                sHosterUrl = URL_MAIN[0:-1] + sHosterUrl
            
            oRequestHandler = cRequestHandler(sHosterUrl)
            sHtmlContent = oRequestHandler.request()

            urlM3u = None
            
            aResult = oParser.parse(sHtmlContent, 'm3u8Url = "([^"]+)')
            if aResult[0]:
                urlM3u = aResult[1][0] + '&_t=' + str(round(time.time() * 1000))
            else:
                aResult = oParser.parse(sHtmlContent, 'streamUrl *= *"([^"]+)')
                if aResult[0]:
                    sHosterUrl = aResult[1][0]
                    sHosterUrl2 = None
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = URL_MAIN + sHosterUrl 
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                sHtmlContent = oRequestHandler.request()
                
                # redirection de lien
                if sHtmlContent[0] != '#':
                    sHosterUrl2 = oRequestHandler.getRealUrl()
                    
                    # 2eme tentative
                    if sHosterUrl2 == sHosterUrl:
                        time.sleep(2)
                        oRequestHandler = cRequestHandler(sHosterUrl)
                        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                        sHtmlContent = oRequestHandler.request()
                        sHosterUrl2 = oRequestHandler.getRealUrl()
            
                        # 3eme tentative
                        if sHosterUrl2 == sHosterUrl:
                            time.sleep(2)
                            oRequestHandler = cRequestHandler(sHosterUrl)
                            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                            sHtmlContent = oRequestHandler.request()
                            sHosterUrl2 = oRequestHandler.getRealUrl()
        
                if sHosterUrl2 != sHosterUrl:
                    urlM3u = sHosterUrl
            
            if urlM3u:
                if not urlM3u.startswith('http'):
                    urlM3u = URL_MAIN + urlM3u 
                oHoster = oHosterGui.getHoster('lien_direct')
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                oHosterGui.showHoster(oGui, oHoster, urlM3u, sThumb)

    
    oGui.setEndOfDirectory()


def getFk(html):
    oParser = cParser()
    html = oParser.abParse(html, '(function(){var _a=', '</script>')

    match_a = re.search(r'var\s+_a\s*=\s*\[([^\]]+)\]', html)
    match_m = re.search(r'\b_m\s*=\s*(\d+)', html)
    match_in = re.search(r'\b_in\s*=\s*(\d+)', html)
    match_mu = re.search(r'\b_mu\s*=\s*(\d+)', html)

    if not (match_a and match_m and match_in and match_mu):
        return None, None, None, None

    _a = [int(x.strip()) for x in match_a.group(1).split(',')]
    _m = int(match_m.group(1))
    _in = int(match_in.group(1))
    _mu = int(match_mu.group(1))

    # Décodage
    _d = ''.join(chr(x ^ _m) for x in _a)
    _sp = _d.split('|', 1)
    _k = _sp[0]
    _sl = _sp[1] if len(_sp) > 1 else ''

    return _k, _sl, _mu, _in
    
    
# Calcul de la signature
def getFs(_k, _sl, _mu, _in, v):
    s = v + '|' + _k + '|' + _sl
    for c in s:
        _in = ((_in * _mu) + ord(c)) & 0x7fffffff
    return ('00000000' + format(_in, 'x'))[-8:]
