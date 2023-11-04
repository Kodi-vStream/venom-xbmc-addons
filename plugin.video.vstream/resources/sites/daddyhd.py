# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import siteManager, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'daddyhd'
SITE_NAME = 'DaddyHD'
SITE_DESC = 'Chaines de Sport et de Divertissement'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_GENRES = ('/', 'showGenres')

TV_TV = ('/', 'load')
SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showTV')

# chaines
channels = {
    116: ['bein Sports 1', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],
    117: ['bein Sports 2', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    118: ['bein Sports 3', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    119: ['RMC Sport 1', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    120: ['RMC Sport 2', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    121: ['Canal+', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    122: ['Canal+ Sport', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG']
    }

# PROBLEME DE DEBIT et fait planter kodi
    # 463: ['Canal+ Foot', 'https://thumb.canalplus.pro/bran/unsafe/870x486/image/62dab6a90b84c/uploads/media/C+FOOT_213x160.png'],
    # 645: ["L'équipe", 'https://upload.wikimedia.org/wikipedia/commons/4/4a/L%27Equipe_logo.png'],
    # 494: ['bein Sports MAX 4', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png'],
    # 495: ['bein Sports MAX 5', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png'],
    # 496: ['bein Sports MAX 6', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png'],
    # 497: ['bein Sports MAX 7', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png'],
    # 498: ['bein Sports MAX 8', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png'],
    # 499: ['bein Sports MAX 9', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png'],
    # 500: ['bein Sports MAX 10', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png']


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()

    sUrl = URL_MAIN + '/cast/stream-%d.php'
    chaines = [116, 117, 118, 119, 120, 121, 122]

    oOutputParameterHandler = cOutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        sDisplayTitle = channel[0]
        sThumb = channel[1]
        oOutputParameterHandler.addParameter('siteUrl', sUrl % iChannel)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    sUrl = URL_MAIN
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<h2 style="background-color:cyan">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        sportGenre = {}
        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle in aResult[1]:
            if 'Schedule' in sTitle:
                break
            if 'Tv Show' in sTitle:
                continue

            sDisplayTitle = sTitle.replace('Soccer', 'Football')
            sDisplayTitle = sDisplayTitle.replace('Darts', 'Flechettes')
            sDisplayTitle = sDisplayTitle.replace('Boxing', 'Boxe')
            sDisplayTitle = sDisplayTitle.replace('Cycling', 'Cyclisme')
            sDisplayTitle = sDisplayTitle.replace('Horse Racing', 'Course de chevaux')
            sDisplayTitle = sDisplayTitle.replace('Ice Hockey', 'Hockey sur glace')
            sDisplayTitle = sDisplayTitle.replace('Alpine Ski', 'Ski')
            sDisplayTitle = sDisplayTitle.replace('Rugby Union', 'Rugby à XV')
            sDisplayTitle = sDisplayTitle.replace('Sailing / Boating', 'Voile')
            sportGenre[sDisplayTitle] = sTitle

        for sDisplayTitle, sTitle in sorted(sportGenre.items()):
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()
    sUrl = URL_MAIN

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<h2 style="background-color:cyan">%s</h2>' % sTitle
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '<h2 style="background-color:cyan">')

    sPattern = '<hr>(<strong>|)(\d+:\d+) (.+?)<'#span.+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sDate = aEntry[1]
            sTitle = aEntry[2]
            
            sTitle = sDate + ' ' + sTitle
            
            # heure d'été/hiver
            heure = int(sDate[0:2])
            heure += 1
            if heure == 24:
                heure = 0
            sDate = '%02d:%s' % (heure, sDate[3:])
            sDisplayTitle = sDate + ' - ' + aEntry[2].strip()

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oParser = cParser()
    urlMain = URL_MAIN

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(urlMain)
    sHtmlContent = oRequestHandler.request()

    # enlève les accents qui gènent
    sTitle2 = re.sub('[^a-zA-Z0-9:. ]', '#', sTitle)
    if sTitle2 != sTitle:
        sTitle2 = sTitle[:sTitle2.index('#')]
    sPattern = '>%s' % sTitle2

    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '<br')

    sPattern = 'href="([^"]+).+?rel=".+?>([^\(]+)'
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '</p>')
    aResult = oParser.parse(sHtmlContent, sPattern)

    # on enleve l'heure qui peut être fausse, heure d'été/hiver
    sTitle = sTitle[5:]
    
    if not aResult[0]:
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

            oGui.addDir(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', oOutputParameterHandler)

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
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


# Traitement générique
def getHosterIframe(url, referer):

    if not url.startswith('http'):
        url = URL_MAIN + url

    oRequestHandler = cRequestHandler(url)
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False, False

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        from resources.lib.packer import cPacker
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
                if '.m3u8' in code:
                    return True, code + '|Referer=' + url
            except Exception as e:
                pass

    referer = url
    sPattern = '<iframe src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//' + referer.split('/')[2] + url  # ajout du nom de domaine
                url = "https:" + url
            b, url = getHosterIframe(url, referer)
            if b:
                return True, url

    sPattern = 'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            referer = url
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return True, sHosterUrl + '|referer=' + referer

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return True, url

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        sHosterUrl = sHosterUrl.replace('index', 'mono')
        return True, sHosterUrl + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return True, sHosterUrl + '|referer=' + referer

    return False, False
