# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.packer import cPacker
from resources.lib.comaddon import isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'elitegol'
SITE_NAME = 'Elitegol'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_SPORTS = (True, 'load')
SPORT_GENRES = ('/', 'showGenres')  # FOOT
SPORT_LIVE = ('/', 'showMovies')
SPORT_TV = ('lecteur/', 'showTV')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

# chaines dans l'ordre d'affichage
channels = {
    1: ['bein Sports 1', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],
    20: ['DAZN1', 'https://miguia.tv/channels/big_329@2x.png'],
    21: ['prime video ligue 1', 'https://i.imgur.com/PvpkxgG.png'],
    #20: ['prime video ligue 2', 'https://i.imgur.com/PvpkxgG.png'],
    5: ['Canal+', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    17: ['Canal+ Foot', 'https://thumb.canalplus.pro/bran/unsafe/870x486/image/62dab6a90b84c/uploads/media/C+FOOT_213x160.png'],
    6: ['Canal+ sport', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG'],
    28: ['Canal+ sport 360', 'https://matchpint-cdn.matchpint.cloud/shared/imagenes/channels/284_logo_1599851988.png'],
    #17: ['Canal+ décalé', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_257.PNG'],
    7: ['eurosport 1', 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg'],
    8: ['eurosport 2', 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg'],
    4: ['RMC Sport 1', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    9: ['RMC Sport 2', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    18: ['L\'equipe TV', 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png'],
    19: ['Automoto', 'https://moto-station.com/wp-content/uploads/2021/05/05/Automoto-La-Chaine-logo_0.png.jpg'],
    #24: ['RMC Sport 3', 'https://www.monpetitforfait.com/comparateur-box-internet/wp-content/uploads/2020/06/rmcsport32.png'],
    #25: ['RMC Sport 3', 'https://i.imgur.com/PvpkxgG.png'],
    #26: ['prime video ligue 1/2 (LDC8)', 'https://i.imgur.com/PvpkxgG.png'],
    #27: ['prime video ligue 1/2 (LDC9)', 'https://i.imgur.com/PvpkxgG.png'],
    #28: ['prime video ligue 1/2 (LDC10)', 'https://i.imgur.com/PvpkxgG.png'],
    2: ['bein Sports 2', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    3: ['bein Sports 3', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    10: ['bein Sports MAX 4', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png'],
    11: ['bein Sports MAX 5', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png'],
    12: ['bein Sports MAX 6', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png'],
    13: ['bein Sports MAX 7', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png'],
    14: ['bein Sports MAX 8', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png'],
    15: ['bein Sports MAX 9', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png'],
    16: ['bein Sports MAX 10', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png'],
    # 31: ['multisport+ 1', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 32: ['multisport+ 2', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 33: ['multisport+ 3', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 34: ['multisport+ 4', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 35: ['multisport+ 5', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 36: ['multisport+ 6', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    29: ['TF1', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/TF1_logo_2013.png/800px-TF1_logo_2013.png'],
    22: ['France 2', 'https://i.imgur.com/PvpkxgG.png'],
    23: ['France 3', 'https://i.imgur.com/PvpkxgG.png'],
    30: ['France 2', 'https://www.ffp.asso.fr/wp-content/uploads/2018/10/France-2.png'],
    38: ['France 3', 'https://static.wikia.nocookie.net/hdl-logopedia/images/0/0a/Logo-france-3.png/revision/latest/scale-to-width-down/220?cb=20180220171302&path-prefix=fr']
#    40: ['FFFtv', 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Tmc_2016.png']
    }

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Football', 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showTV():
    oGui = cGui()

    chaines = [20, 1, 5, 17, 6, 28, 7, 8, 4, 9, 18, 19, 2, 3, 10, 11, 12, 13, 14, 15, 16]
    
    # if 'sport' in sUrl:
    #     chaines = [1, 4, 21, 20, 5, 6, 7, 8, 18, 19, 9, 2, 3, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 37, 31, 32, 33, 34, 35, 36]
    # else: # Chaines ciné
    #     chaines = [21, 22, 23, 29, 30, 38, 5, 17, 39]

    oOutputParameterHandler = cOutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        sThumb = channel[1]

        sDisplayTitle = channel[0]
        sHostUrl = 'lec/2/%d' % iChannel
        oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTVLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oOutputParameterHandler = cOutputParameterHandler()
    for numChannel in range(1, 6):
        sHostUrl = "lec/%d/%s" % (numChannel, sUrl)
        sDisplayTitle = '%s - Lien %d' % (sTitle, numChannel)
        oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # titre / heure / id / lang
    sPattern = 'href="#">([^<]+).+?>(\d+:\d+).+?STREAM (\d+) ([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[0]
            sTime = aEntry[1]
            sUrl2 = 'lec/2/%s' % aEntry[2]
            sLang = aEntry[3]
            sThumb = ''

            sDisplayTitle = '%s - %s (%s)' %(sTime, sTitle, sLang)
            sDesc = sDisplayTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addDir(SITE_IDENTIFIER, 'showLink', sDisplayTitle, "sport.png", oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHosterUrl = getHosterIframe(sUrl, sUrl)
    if sHosterUrl:
        sHosterUrl = sHosterUrl.strip()
        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



# Traitement générique
def getHosterIframe(url, referer):
    
    if 'youtube.com' in url:
        return None

    if not url.startswith('http'):
        url = URL_MAIN + url

    oRequestHandler = cRequestHandler(url)
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent or sHtmlContent == 'False':
        return False

    referer = oRequestHandler.getRealUrl()
    
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
        for sHosterUrl in aResult:
            if '.m3u8' in sHosterUrl:
                if 'fls/cdn/' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('/playlist.', '/tracks-v1a1/mono.')
                else:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', referer)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()
    #            sHosterUrl = sHosterUrl.replace('index', 'mono')
                return sHosterUrl + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return sHosterUrl + '|referer=' + referer

    sPattern = 'new Player\("100%","100%","player","(.+?)".+?,"([^"]+)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = 'https://%s/hls/%s/live.m3u8' % (aResult[0][1], aResult[0][0])
        return sHosterUrl + '|referer=' + referer

    return False


