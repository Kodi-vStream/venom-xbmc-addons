# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import siteManager, VSlog, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, urlEncode
import re
import base64
import json
import threading
import sys
from collections import OrderedDict
try:
    import Queue
except ImportError:
    import queue as Queue
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
from resources.sites import elitegol
import time


SITE_IDENTIFIER = 'witv'
SITE_NAME = 'witv'
SITE_DESC = 'Chaines TV en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
PLAYER_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/156.0.0.0 Safari/537.36')


SPORT_SPORTS = ('chaines-live/sport/', 'showTV')
SPORT_TV = ('chaines-live/sport/', 'showTV')
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
        
        result = sorted(aResult[1], key = lambda chaine : chaine[1].upper())
        for aEntry in result:
            sUrl = aEntry[0]
            sTitle = aEntry[1].split('-')[0].strip()#.capitalize()
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
    oGui = cGui()
    oHosterGui = cHosterGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, 'id="player\d" data-v="([^"]+)')

    if not aResult[0]:
        oGui.setEndOfDirectory()
        return
        
    sUrlDecode = URL_MAIN + 'ajax_player.php'
    oRequest = cRequestHandler(sUrlDecode)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    
    fx_k, _sl, _mu, _in, mb = getFk(sHtmlContent)
    
    sourceUrls = [] # ne pas utiliser de set() pour assurer l'ordre lorsqu'on revient sur la page
    if mb:
        urlsJson = base64.b64decode(mb)
        urlsJson = json.loads(urlsJson, object_pairs_hook=OrderedDict)
        urls = urlsJson.values()
        for url in urls:
            sourceUrls.append(url)
    else:
        for dataV in aResult[1]:
            fx_s = getFs(fx_k, _sl, _mu, _in, dataV)
            postdata = 'k=%s&b=1&t=1&s=%s&v=%s' % (fx_k, fx_s, dataV)
            oRequest.addParametersLine(postdata)
            ret = oRequest.request()
            if ret.startswith('{'):
                ret = json.loads(ret)
                sHosterUrl = ret.get('u', '')
                sourceUrls.append(sHosterUrl)

    def collect_links(sourceUrl, onlyM3u):
        if not sourceUrl:
            return []
        if sourceUrl.endswith('.m3u8'):
            if '?url=' in sourceUrl:
                sourceUrl = sourceUrl.split('?url=', 1)[1]
            return [sourceUrl]
        if onlyM3u:
            return []
        return [streamUrl for streamUrl in
                getHosterUrls(urljoin(URL_MAIN, sourceUrl)) if streamUrl]

    bMatrix = isMatrix()
    links = []
    for sourceUrl in sourceUrls[1:]:
        for linkUrl in collect_links(sourceUrl, not bMatrix):
            if linkUrl not in links:
                links.append(linkUrl)

    if not links and sourceUrls:
        for linkUrl in collect_links(sourceUrls[0], False):
            if linkUrl not in links:
                links.append(linkUrl)

    oHosterDirect = None
    for linkIndex, streamUrl in enumerate(links):
        displayTitle = '%s - Lien %d' % (sMovieTitle, linkIndex + 1)
        if not oHosterDirect:
            oHosterDirect = oHosterGui.getHoster('lien_direct')
        oHosterDirect.setDisplayName(displayTitle)
        oHosterDirect.setFileName(sMovieTitle)
        oHosterGui.showHoster(oGui, oHosterDirect, streamUrl, sThumb, bUseInputstream=True)

    oGui.setEndOfDirectory()


def getHosterUrls(sourceUrl):
    oParser = cParser()
    timeNow = '&t=%d' % int(time.time() * 1000)
    oRequestHandler = cRequestHandler(sourceUrl + timeNow)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    oRequestHandler.addHeaderEntry('sec-fetch-site', 'same-origin')
    oRequestHandler.addHeaderEntry('User-Agent', PLAYER_USER_AGENT)
    sHtmlContent = oRequestHandler.request()
    playerReferer = oRequestHandler.getRealUrl() or sourceUrl + timeNow
    playerCookies = oRequestHandler.GetCookies()
    
    hosterUrls = []
    trouve = False
    sUrlPlayer = sourceUrl.split('?')[0]
    for serveur in ('switchWitvStream', 'switchVavooServer'):
        aResult = oParser.parse(sHtmlContent, "%s\('([^']+)'" % serveur)
        if aResult[0]:
            sHtmlContent = oParser.abParse(sHtmlContent, 'function %s' % serveur, '});')
            sPattern = "window.location.href *= *'([^']+)'"
            aResultVavoo = oParser.parse(sHtmlContent, sPattern)
            if aResultVavoo[0]:
                vavooId = aResultVavoo[1][0]
                candidates = [(sUrlPlayer, vavooId, resultUrl, playerReferer, playerCookies)
                              for resultUrl in aResult[1]]
                if candidates:
                    if sys.version_info[0] < 3:
                        resolvedUrls = [_resolve_witv_candidate(candidate)
                                        for candidate in candidates]
                    else:
                        resultQueue = Queue.Queue()
                        resolvedUrls = [None] * len(candidates)
                        workers = []
                        for resultIndex, candidate in enumerate(candidates):
                            worker = threading.Thread(
                                target=_resolve_witv_candidate_worker,
                                args=(resultQueue, resultIndex, candidate))
                            worker.daemon = True
                            worker.start()
                            workers.append(worker)

                        for _ in candidates:
                            resultIndex, streamUrl = resultQueue.get()
                            resolvedUrls[resultIndex] = streamUrl
                        for worker in workers:
                            worker.join()

                    for sHosterUrl in resolvedUrls:
                        if sHosterUrl and sHosterUrl not in hosterUrls:
                            hosterUrls.append(sHosterUrl)
    
            trouve = True
            break


    if not trouve:
        aResult = oParser.parse(sHtmlContent, 'data-url="([^"]+)')
        if aResult[0]:
            for resultUrl in aResult[1]:
                sHosterUrl = elitegol.getHosterIframe(resultUrl, sourceUrl)
                if sHosterUrl and not sHosterUrl in hosterUrls:
                    hosterUrls.append(sHosterUrl)


    return [streamUrl if '|' in streamUrl else
            streamUrl + '|' + urlEncode({'Referer': sourceUrl, 'sec-fetch-site': 'same-origin'})
            for streamUrl in hosterUrls]


def _resolve_witv_candidate_worker(resultQueue, resultIndex, candidate):
    try:
        streamUrl = _resolve_witv_candidate(candidate)
    except Exception as exc:
        VSlog('Witv candidate resolution failed: %s' % exc)
        streamUrl = None
    resultQueue.put((resultIndex, streamUrl))


def _resolve_witv_candidate(candidate):
    sUrlPlayer, vavooId, resultUrl, playerReferer, playerCookies = candidate
    requestUrl = '%s%s%s&json=1' % (sUrlPlayer, vavooId, resultUrl)
    requestHandler = cRequestHandler(requestUrl)
    requestHandler.addHeaderEntry('Referer', playerReferer)
    requestHandler.addHeaderEntry('sec-fetch-site', 'same-origin')
    requestHandler.addHeaderEntry('User-Agent', PLAYER_USER_AGENT)
    if playerCookies:
        requestHandler.addHeaderEntry('Cookie', playerCookies)
    requestHandler.addHeaderEntry('Cache-Control', 'no-cache')
    requestHandler.addHeaderEntry('Pragma', 'no-cache')

    response = requestHandler.request()
    if not response or not response.startswith('{'):
        return None

    try:
        streamPath = json.loads(response).get('m3u8')
    except (TypeError, ValueError):
        return None
    if not streamPath:
        return None

    streamUrl = urljoin(requestUrl, streamPath)
    playbackHeaders = {'Referer': playerReferer,
                       'sec-fetch-site': 'same-origin',
                       'User-Agent': PLAYER_USER_AGENT}
    if playerCookies:
        playbackHeaders['Cookie'] = playerCookies
    return streamUrl + '|' + urlEncode(playbackHeaders)


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
    _sp = _d.split('|')
    _k = _sp[0]
    _sl = _sp[1] if len(_sp) > 1 else ''
    _mb = _sp[2] if len(_sp) > 2 else ''

    return _k, _sl, _mu, _in, _mb
    
    
# Calcul de la signature
def getFs(_k, _sl, _mu, _in, v):
    s = v + '|' + _k + '|' + _sl
    for c in s:
        _in = ((_in * _mu) + ord(c)) & 0x7fffffff
    return ('00000000' + format(_in, 'x'))[-8:]
