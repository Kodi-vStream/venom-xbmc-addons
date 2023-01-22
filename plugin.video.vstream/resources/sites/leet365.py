# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import ast
import re

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

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'leet365'
SITE_NAME = 'Leet365'
SITE_DESC = 'Tous les sports'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = (True, 'load')
TV_TV = (True, 'load')
SPORT_TV = ('sport', 'showTV')
CHAINE_CINE = ('cinema', 'showTV')
SPORT_LIVE = ('/', 'showMovies')
SPORT_GENRES = ('/', 'showGenres')

# chaines dans l'ordre d'affichage
channels = {
    1: ['bein Sports 1', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png'],
    4: ['RMC Sport 1', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    21: ['prime video ligue 1', 'https://i.imgur.com/PvpkxgG.png'],
    20: ['prime video ligue 2', 'https://i.imgur.com/PvpkxgG.png'],
    5: ['Canal+', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    6: ['Canal+ sport', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_177.PNG'],
    17: ['Canal+ decale', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_257.PNG'],
    7: ['eurosport 1', 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg'],
    8: ['eurosport 2', 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg'],
    18: ['L\'equipe TV', 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png'],
    19: ['Automoto', 'https://moto-station.com/wp-content/uploads/2021/05/05/Automoto-La-Chaine-logo_0.png.jpg'],
    9: ['RMC Sport 2', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    2: ['bein Sports 2', 'https://images.beinsports.com/dZ2ESOsGlqynphSgs7MAGLwFAcg=/788711-HD2.png'],
    3: ['bein Sports 3', 'https://images.beinsports.com/G4M9yQ3f4vbFINuKGIoeJQ6kF_I=/788712-HD3.png'],
    10: ['bein Sports MAX 4', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png'],
    11: ['bein Sports MAX 5', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png'],
    12: ['bein Sports MAX 6', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png'],
    13: ['bein Sports MAX 7', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png'],
    14: ['bein Sports MAX 8', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png'],
    15: ['bein Sports MAX 9', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png'],
    16: ['bein Sports MAX 10', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png'],
    22: ['prime video ligue 1/2 (LDC4)', 'https://i.imgur.com/PvpkxgG.png'],
    23: ['prime video ligue 1/2 (LDC5)', 'https://i.imgur.com/PvpkxgG.png'],
    24: ['prime video ligue 1/2 (LDC6)', 'https://i.imgur.com/PvpkxgG.png'],
    25: ['prime video ligue 1/2 (LDC7)', 'https://i.imgur.com/PvpkxgG.png'],
    26: ['prime video ligue 1/2 (LDC8)', 'https://i.imgur.com/PvpkxgG.png'],
    27: ['prime video ligue 1/2 (LDC9)', 'https://i.imgur.com/PvpkxgG.png'],
    28: ['prime video ligue 1/2 (LDC10)', 'https://i.imgur.com/PvpkxgG.png'],
    37: ['foot+', 'https://matchpint-cdn.matchpint.cloud/shared/imagenes/channels/284_logo_1599851988.png'],
    31: ['multisport+ 1', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    32: ['multisport+ 2', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    33: ['multisport+ 3', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    34: ['multisport+ 4', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    35: ['multisport+ 5', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    36: ['multisport+ 6', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    29: ['TF1', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/TF1_logo_2013.png/800px-TF1_logo_2013.png'],
    30: ['France 2', 'https://www.ffp.asso.fr/wp-content/uploads/2018/10/France-2.png'],
    38: ['France 3', 'https://static.wikia.nocookie.net/hdl-logopedia/images/0/0a/Logo-france-3.png/revision/latest/scale-to-width-down/220?cb=20180220171302&path-prefix=fr'],
    39: ['TMC', 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Tmc_2016.png']
    }


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', CHAINE_CINE[0])
    oGui.addDir(SITE_IDENTIFIER, CHAINE_CINE[1], 'Chaines TV Ciné', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Besoin des saut de ligne
    sHtmlContent = sHtmlContent.replace('\n', '@')
    sPattern = '\d+-\d+-\d+ \(.+?\) (.+?) : .+?@'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
        oGui.setEndOfDirectory()
        return

    genres = set()
    for sGenre in aResult[1]:
        genres.add(sGenre)

    oOutputParameterHandler = cOutputParameterHandler()
    for sGenre in sorted(genres):
        sTitle = sGenre
        sDisplayTitle = sTitle

        oOutputParameterHandler.addParameter('siteUrl', 'genre=' + sGenre)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
        oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'sport.png', '', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'sport' in sUrl:
        chaines = [1, 4, 21, 20, 5, 6, 7, 8, 18, 19, 9, 2, 3, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 37, 31, 32, 33, 34, 35, 36]
    else: # Chaines ciné
        chaines = [29, 30, 38, 5, 17, 39]

    oOutputParameterHandler = cOutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        sDisplayTitle = channel[0]
        sThumb = channel[1]
        oOutputParameterHandler.addParameter('siteUrl', iChannel)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sGenre = ''

    if 'genre=' in sUrl:
        sUrl, sGenre = sUrl.split('genre=')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Besoin des saut de ligne
    sHtmlContent = sHtmlContent.replace('\n', '@')
    sPattern = '(\d+-\d+-\d+ \(.+?\)) (.+?) : (.+?)\(CH(.+?)@'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sDate = aEntry[0].replace('-20', '/').replace('-', '/').replace('(', '').replace(')', '')
            sDesc1 = aEntry[1]
            if sGenre and sGenre != sDesc1:
                continue
            sDesc2 = aEntry[2]
            sUrl2 = "('" + aEntry[3].replace(') (', "', '").replace('(CH', "('").replace(')', "')")
            sTitle = '%s (%s)' % (sDesc2, sDesc1)
            sDisplayTitle = sDate + ' - ' + sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sDisplayTitle, 'sport.png', '', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLive():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    links = []
    if ',' in sUrl:
        links.extend(eval(sUrl))
    else:
        links.append(eval(sUrl))

    oOutputParameterHandler = cOutputParameterHandler()
    for link in links:
        aEntry = re.findall('(\d+)(.+)', link)
        iChannel = aEntry[0][0]
        sLang = aEntry[0][1]
        channel = channels.get(int(iChannel))
        sChannel = sThumb = ''
        if channel:
            sChannel = channel[0]
            sThumb = channel[1]
        sDisplayTitle = '%s - [%s] (%s)' % (sMovieTitle, sChannel, sLang)

        oOutputParameterHandler.addParameter('siteUrl', iChannel)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addMisc(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if not sThumb:
        sThumb = ''

    sHoster = 'https://leet365.cc/fr/%d/%s'
# alternative    sHoster = 'https://1rowsports.com/player/%d/%s'

    oOutputParameterHandler = cOutputParameterHandler()
    
    # jusqu'à 6 hosters, mais on vStream ne sait décoder que le 1 et le 5.
    hosters = [1, 5]
#    for numHost in range(1, 7):
    i=0
    for numHost in hosters:
        i += 1
        sDisplayTitle = '%s [Lien %d]' % (sMovieTitle, i)
        sHosterUrl = sHoster % (numHost, sUrl)
        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, 'sport.png', sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if not sThumb:
        sThumb = ''

    bvalid, sHosterUrl = Hoster_Leet365(sUrl, sUrl)

    if sHosterUrl:
        sHosterUrl = sHosterUrl.strip()
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster != False:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def Hoster_Leet365(url, referer):
    oParser = cParser()
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        hostUrl = aResult[1][0]
        if 'dailymotion' in hostUrl:
            return True, hostUrl
        if 'fclecteur.com' in hostUrl:
            return Hoster_Laylow(hostUrl, url)
        return Hoster_Wigistream(hostUrl, url)

    sPattern = '<script>fid="(.+?)".+?src="\/\/fclecteur\.com\/footy\.js">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        referer = url
        url = 'https://fclecteur.com/footy.php?player=desktop&live=%s' % aResult[1][0]
        return Hoster_Laylow(url, referer)

    return False, False


def Hoster_Wigistream(url, referer):
    
    if not url.startswith('http'):
        url = 'https:' + url
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
            return True, aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    sPattern = '<iframe.+?src="([^"]+)'  # iframe imbriqué
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return Hoster_Wigistream(aResult[0], url)

    return False, False


def Hoster_Pkcast(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(referer)))
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'play\(\).+?return\((.+?)\.join'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult:
        return True, ''.join(ast.literal_eval(aResult[1][0])) + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False, False


def Hoster_Laylow(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = "source:.+?'(https.+?m3u8)"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        return True, aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return Hoster_Pkcast(url, referer)
