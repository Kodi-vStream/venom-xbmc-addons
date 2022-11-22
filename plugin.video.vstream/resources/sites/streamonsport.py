# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import ast
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


URL_MAIN = ''
def GetUrlMain():
    global URL_MAIN
    if URL_MAIN != '':
        return URL_MAIN
    
    oRequestHandler = cRequestHandler(siteManager().getUrlMain(SITE_IDENTIFIER))
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="(.+?)"'
    oParser = cParser()
    URL_MAIN = oParser.parse(sHtmlContent, sPattern)[1][0]
    return URL_MAIN


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'streamonsport'
SITE_NAME = 'Streamonsport'
SITE_DESC = 'Site pour regarder du sport en direct'


SPORT_SPORTS = ('/', 'load')
TV_TV = ('/', 'load')
SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showMovies')
#CHAINE_CINE = ('2370162-chaines-tv-streaming-tf1-france-2-canal-plus.html', 'showMovies')
SPORT_LIVE = ('/', 'showMovies')
SPORT_GENRES = ('/', 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)
    #
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', CHAINE_CINE[0])
    # oGui.addDir(SITE_IDENTIFIER, CHAINE_CINE[1], 'Chaines TV Ciné', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    urlMain = GetUrlMain()

    genreURL = '-basketball-streaming-regarder-le-basket-en-streaming.html'
    genres = [('Basket', '3'), ('Football', '1'), ('Rugby', '2'), ('Tennis', '5')]
    
    oOutputParameterHandler = cOutputParameterHandler()
    for title, url in genres:
        sUrl = urlMain + url + genreURL
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', title)
        oGui.addMisc(SITE_IDENTIFIER, 'showMovies', title, 'genres.png', '', title, oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    urlMain = GetUrlMain()
    if 'http' not in sUrl:
        sUrl = urlMain + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # THUMB ref title desc1 desc2
    sPattern = '<img class=".+?src="([^"]+)".+?href="([^"]+).+?<span>([^<]+)<.+?data-time="(?:([^<]+)|)".+?>([^<]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        # total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2].replace(' streaming gratuit', '').replace(' foot', '').replace('🆚', '/')
            sDate = aEntry[3]
            sDesc1 = aEntry[4]

            # bChaine = False
            #if sUrl != CHAINE_CINE[0] and sUrl != SPORT_TV[0]:
            if sUrl != SPORT_TV[0]:
                sDisplayTitle = sTitle
                if sDesc1 and 'chaîne' not in sDesc1 and 'chaine' not in sDesc1:
                    sDisplayTitle += ' (' + sDesc1.replace(' · ', '') + ')'
                if sDate:
                    try:
                        d = datetime(*(time.strptime(sDate, '%Y-%m-%dT%H:%M:%S+01:00')[0:6]))
                        sDate = d.strftime("%d/%m/%y %H:%M")
                    except Exception:
                        pass
                    sDisplayTitle = sDate + ' - ' + sDisplayTitle
            else:
                # bChaine = True
                sTitle = sTitle.upper()
                sDisplayTitle = sTitle

            if 'http' not in sUrl2:
                sUrl2 = urlMain[:-1] + sUrl2

            if 'http' not in sThumb:
                sThumb = urlMain[:-1] + sThumb

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showLive', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showLive():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # liens visibles
    sPattern = r"btn btn-(success|warning) *btn-sm.+?src='([^\']*).+?img src=\".+?lang\/([^\"]*)\.gif.+?this\.src='.+?lang\/([^\']*)\.gif"
    aResult = oParser.parse(sHtmlContent, sPattern)

    i = 0
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        if aResult[1]:
            for aEntry in aResult[1]:
                i += 1
                sUrl2 = aEntry[1]
                sLang1 = aEntry[2].upper()
                sLang2 = aEntry[3].upper()
                sDisplayTitle = '%s - Lien %d (%s)' % (sMovieTitle, i, sLang1 if len(sLang1) == 2 else sLang2 if len(sLang2) == 2 else '')

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('siterefer', sUrl)
                oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # # 1 seul liens tv telerium
    # sPattern = 'iframe id="video" src.+?id=([^"]+)'
    # aResult = oParser.parse(sHtmlContent, sPattern)
    # if aResult[0] is True:
    #     sUrl2 = GetUrlMain() + 'go/' + aResult[1][0]
    #     sDisplayTitle = sMovieTitle
    #     oOutputParameterHandler = cOutputParameterHandler()
    #     oOutputParameterHandler.addParameter('siteUrl', sUrl2)
    #     oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    #     oOutputParameterHandler.addParameter('sThumb', sThumb)
    #     oOutputParameterHandler.addParameter('siterefer', sUrl)
    #     oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    siterefer = oInputParameterHandler.getValue('siterefer')
    sHosterUrl = ''

    if 'yahoo' in sUrl:  # redirection
        urlMain = GetUrlMain()
        sUrl = urlMain + sUrl

    if 'allfoot' in sUrl or 'streamonsport' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        # oRequestHandler.addHeaderEntry('Referer', siterefer) # a verifier
        sHtmlContent = oRequestHandler.request()

        siterefer = sUrl
        oParser = cParser()
        if "pkcast123.me" in sHtmlContent:
            sPattern = 'fid="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            sUrl = "https://www.pkcast123.me/footy.php?player=desktop&live=" + aResult[1][0] + "&vw=649&vh=460"
        else:
            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sUrl = aResult[1][0]

    shosterurl = ''
    if 'hola.php' in sUrl:
        urlMain = GetUrlMain()
        sUrl = urlMain + sUrl

    if 'pkcast123' in sUrl:
        bvalid, shosterurl = Hoster_Pkcast(sUrl, siterefer)
        if bvalid:
            sHosterUrl = shosterurl

    if "leet365.cc" in sUrl or 'casadelfutbol' in sUrl:
        bvalid, shosterurl = Hoster_Leet365(sUrl, siterefer)
        if bvalid:
            sHosterUrl = shosterurl

    if 'telerium' in sUrl:
        bvalid, shosterurl = Hoster_Telerium(sUrl, siterefer)
        if bvalid:
            sHosterUrl = shosterurl

    if 'andrhino' in sUrl:
        bvalid, shosterurl = Hoster_Andrhino(sUrl, siterefer)
        if bvalid:
            sHosterUrl = shosterurl

    if 'wigistream' in sUrl or 'cloudstream' in sUrl:
        bvalid, shosterurl = Hoster_Wigistream(sUrl, siterefer)
        if bvalid:
            sHosterUrl = shosterurl

    # a verifier
    if 'laylow' in sUrl:
        bvalid, shosterurl = Hoster_Laylow(sUrl, siterefer)
        if bvalid:
            sHosterUrl = shosterurl

    if not sHosterUrl:
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


def Hoster_Pkcast(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(referer)))
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = r'play\(\).+?return\((.+?)\.join'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult:
        return True, ''.join(ast.literal_eval(aResult[1][0])) + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False, False


def Hoster_Telerium(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    urlrederict = oRequestHandler.getRealUrl()
    urlmain = 'https://' + urlrederict.split('/')[2]  # ex https://telerium.club

    sPattern = r'var\s+cid[^\'"]+[\'"]{1}([0-9]+)'
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        str2 = aResult[0]
        datetoken = int(getTimer()) * 1000

        jsonUrl = urlmain + '/streams/' + str2 + '/' + str(datetoken) + '.json'
        tokens = getRealTokenJson(jsonUrl, urlrederict)
        m3url = tokens['url']
        nxturl = urlmain + tokens['tokenurl']
        realtoken = getRealTokenJson(nxturl, urlrederict)[10][::-1]
        try:
            m3url = m3url.decode("utf-8")
        except Exception:
            pass

        sHosterUrl = 'https:' + m3url + realtoken
        sHosterUrl += '|User-Agent=' + UA + '&Referer=' + Quote(urlrederict)  # + '&Sec-F'

        return True, sHosterUrl

    return False, False


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
        return Hoster_Wigistream(hostUrl, url)

    sPattern = r'<script>fid="(.+?)".+?src="\/\/fclecteur\.com\/footy\.js">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        referer = url
        url = 'https://fclecteur.com/footy.php?player=desktop&live=%s' % aResult[1][0]
        return Hoster_Laylow(url, referer)

    return False, False


def Hoster_Andrhino(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = r"atob\('([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        url2 = base64.b64decode(aResult[0])
        return True, url2.strip() + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    # fichier vu mais ne sait plus dans quel cas
    sPattern = r"source:\s'(https.+?m3u8)"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        return True, aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False, False


def Hoster_Wigistream(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = r'(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
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


def getRealTokenJson(link, referer):

    realResp = ''
    oRequestHandler = cRequestHandler(link)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'pl,en-US;q=0.7,en;q=0.3')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', referer)
    oRequestHandler.addCookieEntry('elVolumen', '100')
    oRequestHandler.addCookieEntry('__ga', '100')

    try:
        realResp = oRequestHandler.request()
    except Exception:
        pass

    if not realResp:
        oRequestHandler = cRequestHandler(link)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept', 'application/json')
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



# Traitement générique
def getHosterIframe(url, referer):
    
    if not url.startswith('http'):
        url = GetUrlMain( )+ url
    
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False, False

    import xbmcvfs
    f = xbmcvfs.File('special://userdata/addon_data/plugin.video.vstream/test.txt','w')
    f.write(sHtmlContent)
    f.close()

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
    
    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
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


