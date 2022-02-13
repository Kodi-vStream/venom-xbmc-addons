# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 40 https://www.streamonsport version 2

import base64
import json
import re
import time
import ast
from datetime import datetime, timedelta
from resources.lib.comaddon import isMatrix
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

SITE_IDENTIFIER = 'streamonsport'
SITE_NAME = 'Streamonsport'
SITE_DESC = 'Site pour regarder du sport en direct'

URL_MAIN = 'https://my.streamonsport.biz/'

SPORT_SPORTS = (True, 'load')
SPORT_TV = (URL_MAIN + '31-site-pour-regarder-les-chaines-de-sport.html', 'showMovies')
CHAINE_TV = (URL_MAIN + '2370162-chaines-tv-streaming-tf1-france-2-canal-plus.html', 'showMovies')
SPORT_LIVE = (URL_MAIN, 'showMovies')
SPORT_GENRES = (URL_MAIN, 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', CHAINE_TV[0])
    oGui.addDir(SITE_IDENTIFIER, CHAINE_TV[1], 'Chaines TV Ciné', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<a href="(.+?)"><img alt="(.+?)".+?src="(.+?)">'
    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="teams"', '</div></div>')
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            title = aEntry[1].replace('streaming', '').strip()
            sThumb = aEntry[2].replace(',', '%2C').replace('?v=so', '')
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', title)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', title, 'genres.png', sThumb, title, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # THUMB ref title desc1 desc2
    sPattern = '<img class=".+?src="([^"]+)".+?href="([^"]+).+?<span>([^<]+)<.+?data-time="(?:([^<]+)|)".+?>([^<]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2].replace(' streaming gratuit', '').replace(' foot', '')
            sDate = aEntry[3]
            sdesc1 = aEntry[4]
            
            bChaine = False
            if sUrl != CHAINE_TV[0] and sUrl != SPORT_TV[0]:
                sDisplayTitle = sTitle
                if sdesc1:
                    sDisplayTitle += ' (' + sdesc1.replace(' · ', '') + ')'
                if sDate:
                    try:
                        d = datetime(*(time.strptime(sDate, '%Y-%m-%dT%H:%M:%S+01:00')[0:6]))
                        sDate = d.strftime("%d/%m/%y %H:%M")
                    except Exception as e:
                        pass
                    sDisplayTitle = sDate + ' - ' + sDisplayTitle
            else:
                bChaine = True
                sTitle = sTitle.upper()
                sDisplayTitle = sTitle

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sDisplayTitle, 'tv.png', sThumb, sDisplayTitle, oOutputParameterHandler)

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
    sPattern = "btn btn-(success|warning) btn-sm.+?src='([^\']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    i = 0
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        if aResult[1]:
            for aEntry in aResult[1]:
                i += 1
                sUrl2 = aEntry[1]
                sDisplayTitle = sMovieTitle + ' - Lien ' + str(i)
    
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('siterefer', sUrl)
                oGui.addLink(SITE_IDENTIFIER, 'Showlink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # 1 seul liens tv telerium
    sPattern = 'iframe id="video".src.+?id=([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        url2 = aResult[1][0]
        oRequestHandler = cRequestHandler(url2)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] == True:

            sUrl2 = aResult[1][0]  # https://telerium.tv/embed/35001.html
            sDisplayTitle = sMovieTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siterefer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'Showlink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def Showlink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    siterefer = oInputParameterHandler.getValue('siterefer')
    sHosterUrl = ''
                    
    if 'yahoo.php' in sUrl:  # redirection
        sUrl = URL_MAIN + sUrl
    
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
            sUrl = "https://www.pkcast123.me/footy.php?player=desktop&live=" +  aResult[1][0] + "&vw=649&vh=460"
        else:
            sPattern = '<iframe.+?src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sUrl = aResult[1][0]

    shosterurl = ''
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

    if sHosterUrl:
        sHosterUrl = sHosterUrl.strip()
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if(oHoster != False):
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
    sPattern = 'play\(\).+?return\((.+?)\.join'
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

    sPattern = 'var\s+cid[^\'"]+[\'"]{1}([0-9]+)'
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
        except:
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
        return Hoster_Wigistream(aResult[1][0], url)

    sPattern = '<script>fid="(.+?)".+?src="\/\/fclecteur\.com\/footy\.js">'
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

    sPattern = "atob\('([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        url2 = base64.b64decode(aResult[0])
        return True, url2.strip() + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    # fichier vu mais ne sait plus dans quel cas
    sPattern = "source:\s'(https.+?m3u8)"
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        return True, aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False, False


def Hoster_Wigistream(url, referer):
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

    sPattern = '<iframe.+?src="([^"]+)' # iframe imbriqué
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
    except:
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
