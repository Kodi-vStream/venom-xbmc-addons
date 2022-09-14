# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import base64
import re
import xbmc

from resources.lib.comaddon import progress, isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote

try:
    import json
except:
    import simplejson as json

SITE_IDENTIFIER = 'livetv'
SITE_NAME = 'Live TV'
SITE_DESC = 'Evénements sportifs en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

SPORT_GENRES = (URL_MAIN + '/frx/allupcoming/', 'showMovies')  # Liste de diffusion des sports
SPORT_LIVE = (URL_MAIN + '/frx/', 'showLive')  # streaming Actif
SPORT_SPORTS = (True, 'load')


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Les sports (Genres)', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Les sports (En direct)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLive():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a class="live" href="([^"]+)">([^<]+)<.a>\s*<br>\s*<a\s*class="live.+?span class="evdesc">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl3 = URL_MAIN + aEntry[0]
            sTitle2 = aEntry[1] + ' ' + aEntry[2]

            try:
                sTitle2 = sTitle2.decode("iso-8859-1", 'ignore')
            except:
                pass
            sTitle2 = cUtil().unescape(sTitle2)
            try:
                sTitle2 = sTitle2.encode("utf-8", 'ignore')
                sTitle2 = str(sTitle2, encoding="utf-8", errors='ignore')
            except:
                pass

            oOutputParameterHandler.addParameter('siteUrl3', sUrl3)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle2)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies3', sTitle2, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showMovies():  # affiche les catégories qui ont des lives'
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a class="main" href="([^"]+)"><b>([^<]+)</b>.+?\s*</td>\s*<td width=.+?>\s*<a class="small" href=".+?"><b>([^<]+)</b></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            try:
                sTitle = sTitle.decode("iso-8859-1", 'ignore')
            except:
                pass

            sTitle = cUtil().unescape(sTitle)
            try:
                sTitle = sTitle.encode("utf-8", 'ignore')
                sTitle = str(sTitle , encoding="utf-8", errors='ignore')
            except:
                pass

            oOutputParameterHandler.addParameter('siteUrl2', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies2', sTitle, 'sport.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showMovies2():  # affiche les matchs en direct depuis la section showMovie

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl2 = oInputParameterHandler.getValue('siteUrl2')

    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="live" href="([^"]+)">([^<]+)</a>\s*(<br><img src=".+?/img/live.gif"><br>|<br>)\s*<span class="evdesc">([^<]+)\s*<br>\s*([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        mois = ['filler', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=True)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = ''
            taglive = ''
            sTitle2 = aEntry[1].replace('<br>', ' ')
            sUrl3 = URL_MAIN + aEntry[0]

            if 'live.gif' in aEntry[2]:
                taglive = ' [COLOR limegreen] Online[/COLOR]'

            sDate = aEntry[3]
            sQual = aEntry[4]

            if not isMatrix():
                try:
                    sTitle2 = sTitle2.decode("iso-8859-1", 'ignore')
                    sQual = sQual.decode("iso-8859-1", 'ignore')
                    sDate = sDate.decode("iso-8859-1", 'ignore')
                except:
                    pass

                sTitle2 = cUtil().unescape(sTitle2)
                sTitle2 = sTitle2.encode("utf-8", 'ignore')

                sQual = cUtil().unescape(sQual)
                sQual = str(sQual.encode("utf-8", 'ignore'))

                sDate = sDate.encode('utf-8')

            if sDate:
                try:
                    sDateTime = re.findall('(\d+) ([\S]+).+?(\d+)(:\d+)', str(sDate))
                    if sDateTime:
                        sMonth = mois.index(sDateTime[0][1])
                        sDate = '%02d/%02d %02d%s' % (int(sDateTime[0][0]), sMonth, int(sDateTime[0][2]), sDateTime[0][3])
                except Exception as e:
                    pass

            sTitle2 = ('%s - %s [COLOR yellow]%s[/COLOR]') % (sDate, sTitle2, sQual)
            sDisplayTitle = sTitle2 + taglive

            oOutputParameterHandler.addParameter('siteUrl3', sUrl3)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies3', sDisplayTitle, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showMovies3():  # affiche les videos disponible du live
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl3 = oInputParameterHandler.getValue('siteUrl3')

    oRequestHandler = cRequestHandler(sUrl3)
    sHtmlContent = oRequestHandler.request()
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')

    sPattern = '<td width=16><img title="(.*?)".+?<a title=".+?" *href="(.+?)"'
    oParser = cParser()

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sLang = aEntry[0]
            sLang = cUtil().unescape(sLang)
            sLang = sLang .encode("utf-8", 'ignore')
            try:
                sLang = str(sLang, encoding="utf-8", errors='ignore')
            except:
                pass

            sUrl4 = aEntry[1]
            if not (sUrl4.startswith("http")):
                sUrl4 = "http:" + sUrl4
            sTitle = ('%s (%s)') % (sMovieTitle2, sLang[:4])
            sThumb = ''

            oOutputParameterHandler.addParameter('siteUrl4', sUrl4)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addDir(SITE_IDENTIFIER, 'showHosters', sTitle, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():  # affiche les videos disponible du live
    oGui = cGui()
    UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    oInputParameterHandler = cInputParameterHandler()
    sUrl4 = oInputParameterHandler.getValue('siteUrl4')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl4)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?(?:allowFullScreen=|width).+?src="([^"]+)".+?</iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        sHosterUrl = ''
        Referer = ''
        url = aResult[1][0]
        if not (url.startswith("http")):
            url = "http:" + url

        if 'popofthestream' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()
            sPattern = 'src="([^"]+)'
            aResult = re.findall(sPattern, sHtmlContent)
            if aResult:
                url2 = url.replace('-', '/')
                urlChannel = url2.replace('html', 'json')
                oRequestHandler = cRequestHandler(urlChannel)
                sHtmlContent = oRequestHandler.request()
                
                if not sHtmlContent.startswith('<!'):   # ce n'est pas du json
                    result = json.loads(sHtmlContent)
                    if 'id' in result:
                        idChannel = result['id']
                        oRequestHandler = cRequestHandler(url2)
                        sHtmlContent2 = oRequestHandler.request()
                        sPattern = '<iframe.+?src="([^\']+)'
                        aResult = re.findall(sPattern, sHtmlContent2)
                        if aResult:
                            url = aResult[0] + idChannel

        if 'sportlevel' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = "manifestUrl: '(.+?)',"
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = 'http://d.sportlevel.com' + aResult[0]
            else:
                sPattern2 = '(http:\/\/embedded.+?)"'
                aResult = oParser.parse(sHtmlContent2, sPattern2)
                if aResult[0] is True:
                    url2 = aResult[1][0]
                    oRequestHandler = cRequestHandler(url2)
                    sHtmlContent3 = oRequestHandler.request()
                    sPattern = "RESOLUTION=(\w+)\s*(http.+?)(#|$)"
                    aResult2 = oParser.parse(sHtmlContent3, sPattern)
                    if aResult2[0] is True:
                        for aResult in aResult2[1]:
                            q = aResult[0]
                            sHosterUrl = aResult[1]
                            sDisplayTitle = sMovieTitle2 + ' [' + q + '] '

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster != False:
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle2)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                        oGui.setEndOfDirectory()
                        return

        if 'tv.rushandball' in url:
            sPattern = '\/(\d+)'
            aResult = re.findall(sPattern, url)
            if aResult:
                id = aResult[0]
                url2 = 'https://tv.rushandball.ru/api/v2/content/' + id + '/access'

                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent = oRequestHandler.request()
                sPattern = 'stream.+?"(https.+?)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] is True:
                    sHosterUrl = aResult[1][0]

        if 'seenow.tv' in url:
            sPattern = 'api.(.+?)$'
            aResult = re.findall(sPattern, url)
            if aResult:
                data = 'url=' + aResult[0] + '&type=tv'  # url=itv-4&type=tv]
                oRequestHandler = cRequestHandler(url)
                oRequestHandler.addHeaderEntry('Referer', url)
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                sHtmlContent = oRequestHandler.request()
                cook = oRequestHandler.GetCookies()
                xbmc.sleep(200)
                oRequestHandler = cRequestHandler(url)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Content-Length', len(data))
                oRequestHandler.addHeaderEntry('Referer', url)
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                # oRequestHandler.addHeaderEntry('Content-Type', 'application/json; charset=utf-8')
                oRequestHandler.addHeaderEntry('Cookie', cook)
                # oRequestHandler.addHeaderEntry('Connection', 'keep-alive')
                oRequestHandler.addParametersLine(data)
                sHtmlContent2 = oRequestHandler.request()  # json

                sPattern = 'stream_id.+?(\d+)'
                aResult = re.findall(sPattern, sHtmlContent2)
                if aResult:
                    stream_id = aResult[0]
                    url2 = 'https://www.filmon.com/api-v2/channel/' + stream_id + '?protocol=hls'
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('Referer', url)
                    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                    sHtmlContent2 = oRequestHandler.request()
                    sPattern = 'quality"."(\w+)".*?url.*?"(https.+?)"'
                    aResult = re.findall(sPattern, sHtmlContent2)
                    if aResult:
                        for Result in aResult:
                            q = Result[0]
                            sHosterUrl = Result[1]
                            sDisplayTitle = sMovieTitle2 + ' [' + q + '] '

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster != False:
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle2)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                        oGui.setEndOfDirectory()
                        return

        if 'faraoni1' in url:
            # type de chaine : eurosport
            # plusieurs suivi  de liens  possibles 5 max vus
            # ex :
            # http://faraoni1.ru/1/10.html ,20.html 5 requetes
            # LiveTV/live2/1.html 3 requetes
            # etc

            nextlink = url
            for x in range(0, 6):  # 6 reqs max pour trouver lhost (normalement 5 )
                oRequestHandler = cRequestHandler(nextlink)
                sHtmlContent = oRequestHandler.request()
                sPattern = 'url.+?(http.+?m3u8)'
                aResult = re.findall(sPattern, sHtmlContent)
                if aResult:
                    sHosterUrl = str(aResult[0])
                    break
                else:
                    sPattern = '<iframe.+?src="([^"]+)'
                    aResult = re.findall(sPattern, sHtmlContent)
                    if aResult:
                        nextlink = 'http://faraoni1.ru' + aResult[0]

        if 'embed.tvcom.cz' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()
            sPattern = "source.+?hls.+?'(https.+?m3u8)"
            aResult = re.findall(sPattern, sHtmlContent)
            if aResult:
                sHosterUrl = aResult[0]

        if 'allsports.icu' in url:
            sPattern = 'ch(\d+).php'
            aResult = re.findall(sPattern, url)
            if aResult:
                id = aResult[0]
                url2 = 'http://allsports.icu/stream/ch' + id + '.html'
                sHosterUrl = getHosterIframe(url2, url2)

        # old host
        if 'espn-live.stream' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            aResult = re.findall(sPattern, sHtmlContent2)
            if aResult:
                url = aResult[0]  # redirection vers un autre site ci-dessous

        if 'footballreal.xyz' in url or 'cdnz.one' in url:# or 'sports247' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '<iframe src=["\'](.+?)["\']'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                Referer = url
                url = aResult[0]  # redirection vers un autre site

        if 'dailydeports.pw' in url:
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', sUrl4)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                if 'cdnz.one' in aResult[0]:
                    url = aResult[0]  # redirection vers un autre site
            else:
                sPattern2 = "str='([^']+)'"
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    for aEntry in aResult:
                        aEntry = aEntry.replace('@', '')
                        data = bytearray.fromhex(aEntry).decode()
                        sPattern3 = '<iframe src="([^"]+)"'
                        aResult1 = re.findall(sPattern3, data)
                        if aResult1:
                            url = aResult1[0]  # redirection vers un autre site
                            break

        if 'emb.apl' in url:  # Terminé - Supporte emb.aplayer et emb.apl3
            Referer = url
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: *\'(.+?)\''
            
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + Referer
            else:
                sPattern2 = "pl\.init\('([^']+)'\);"
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + Referer

        if 'sport7.pw' in url or 'vip7stream' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + url

        if 'totalsport.me' in url or 'airhdx' in url or 'givemenbastreams' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            if Referer:
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: ["\'](.+?)["\']'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'sportsbar.pw' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'livesoccers.pw' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', sHosterUrl2)
                sHtmlContent3 = oRequestHandler.request()
                sPattern3 = '<source src="([^"]+)"'
                aResult1 = re.findall(sPattern3, sHtmlContent3)
                if aResult1:
                    sHosterUrl = aResult1[0]

        if 'assia' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'file:"([^"]+)"|source: \'([^\']+)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0][1] + '|User-Agent=' + UA + '&referer=' + url
            else:
                sPattern2 = '<source src=\'([^\']+)\''
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + url

        if 'sawlive' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'src="([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl3 = aResult[0]
                oRequestHandler = cRequestHandler(sHosterUrl3)
                sHtmlContent3 = oRequestHandler.request()
                sPattern3 = 'var .+? = "([^;]+);([^\"]+)";'
                aResult = re.findall(sPattern3, sHtmlContent3)
                if aResult:
                    sHosterUrl3 = "http://www.sawlive.tv/embedm/stream/" + aResult[0][1] + '/' + aResult[0][0]
                    oRequestHandler = cRequestHandler(sHosterUrl3)
                    sHtmlContent4 = oRequestHandler.request()

                    sPattern4 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
                    aResult = re.findall(sPattern4, sHtmlContent4)
                    if aResult:
                        str2 = aResult[0]
                        if not str2.endswith(';'):
                            str2 = str2 + ';'

                        strs = cPacker().unpack(str2)
                        sPattern5 = 'var .+?=([^;]+);'
                        aResult1 = re.findall(sPattern5, strs)
                        if aResult1:
                            jameiei = eval(aResult1[0])
                            data = ''
                            for c in jameiei:
                                data += chr(c)
                            sHosterUrl = data

        if 'sportlive.site' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                oRequestHandler = cRequestHandler(sHosterUrl2)
                sHtmlContent3 = oRequestHandler.request()
                sPattern3 = '<script type=\'text/javascript\'>id=\'(.+?)\''
                aResult2 = re.findall(sPattern3, sHtmlContent3)
                if aResult2:
                    sHosterUrl3 = aResult2[0]
                    sHosterUrl3 = "http://hdcast.pw/stream_jw2.php?id=" + sHosterUrl3
                    oRequestHandler = cRequestHandler(sHosterUrl3)
                    sHtmlContent4 = oRequestHandler.request()
                    sPattern4 = 'curl = "([^"]+)";'
                    aResult3 = re.findall(sPattern4, sHtmlContent4)
                    if aResult3:
                        sHosterUrl = aResult3[0]
                        sHosterUrl = base64.b64decode(sHosterUrl)

        if 'stream365' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'var a[ 0-9]+="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                gameId = int(aResult[2]) + int(aResult[0]) - int(aResult[1]) - int(aResult[2])
                sHosterUrl = 'http://91.192.80.210/edge0/xrecord/' + str(gameId) + '/prog_index.m3u8'

        if 'youtube' in url:  # Je sais pas
            sPattern2 = 'youtube.com/embed/(.+?)[?]autoplay=1'
            aResult = re.findall(sPattern2, url)

            if aResult:
                video_id = aResult[0]
                url2 = url.replace('/embed/', '/watch?v=').replace('?autoplay=1', '')
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent3 = Unquote(str(oRequestHandler.request()))

                sPattern3 = 'hlsManifestUrl":"(.+?)"'
                aResult = re.findall(sPattern3, sHtmlContent3)

                if aResult:
                    sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&Host=manifest.googlevideo.com'
                else:
                    url2 = 'https://youtube.com/get_video_info?video_id=' + video_id + '&sts=17488&hl=fr'
    
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    sHtmlContent3 = Unquote(str(oRequestHandler.request()))
    
                    sPattern3 = 'hlsManifestUrl":"(.+?)"'
                    aResult = re.findall(sPattern3, sHtmlContent3)
    
                    if aResult:
                        sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&Host=manifest.googlevideo.com'

        if 'streamup.me' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                oRequestHandler = cRequestHandler(sHosterUrl2)
                sHtmlContent3 = oRequestHandler.request()
                sHtmlContent3 = Unquote(sHtmlContent3)
                sPattern3 = 'src: "\/\/(.+?)"'
                aResult = re.findall(sPattern3, sHtmlContent3)
                if aResult:
                    sHosterUrl = 'http://' + aResult[0]

        if 'livestream' in url:  # fixé
            sPattern2 = '<td bgcolor=".+?" *align="center".+?\s*<iframe.+?src="https://([^"]+)/player?.+?</iframe>'
            aResult = re.findall(sPattern2, sHtmlContent)
            if aResult:
                accountid = aResult[0]
                jsonUrl = 'https://player-api.new.' + accountid + '?format=short'
                oRequestHandler = cRequestHandler(jsonUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern3 = '"m3u8_url":"(.+?)"'
                aResult = re.findall(sPattern3, sHtmlContent)
            if aResult:
                sHosterUrl = aResult[0]

        if 'forbet.tv' in url:  # Probleme ssl
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'file: "([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'p.hd24.watch' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'data-channel="([^"]+)">'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                Host = '190-2-146-56.livesports24.online'
                sHosterUrl = 'https://' + Host + '/' + aResult[0] + '.m3u8'

        if 'hdsoccerstreams.net' in url:  # Pas terminer
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<script>fid="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                fid = aResult[0]
                url2 = 'http://webtv.ws/embed.php?live=spstream' + fid + '&vw=700&vh=440'
                Referer = url
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = oRequestHandler.request()

        if 'lato.sx' in url:  # Pas terminer
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<script>fid=["\'](.+?)["\']'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                fid = aResult[0]
                url2 = 'https://yourjustajoo.com/embedred.php?player=desktop&live=' + fid
                Referer = url
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = oRequestHandler.request()

                sPattern2 = 'player.load\({source: (.+?)\('
                aResult = re.findall(sPattern2, sHtmlContent3)
                if aResult:
                    func = aResult[0]
                 
                    sPattern2 = 'function %s\(\) +{ +return\(\[(.+?)\]' % func
                    sPattern2 = 'function %s\(\) +{ +return\(\[([^\[]+)\]' % func
                    sPattern2 = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
                    aResult = re.findall(sPattern2, sHtmlContent3)
                    
                    import xbmcvfs
                    f = xbmcvfs.File('special://userdata/addon_data/plugin.video.vstream/test.txt','w')
                    f.write(sHtmlContent3)
                    f.close()
                
                    
                    if aResult:
                        sHosterUrl = aResult[0].replace('"', '').replace(',', '')
    
        if 'thesports4u.net' in url or 'soccerstreams' in url or 'all.ive' in url:  # Fini
            if 'all.ive' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = oRequestHandler.request()
                sPattern2 = "<script>fid='(.+?)'"
                aResult = re.findall(sPattern2, sHtmlContent2)

                if aResult:
                    Referer = 'https://ragnaru.net/'
                    url2 = 'https://ragnaru.net/embed.php?player=desktop&live=' + aResult[0]
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', 'https://all.ive.zone/')
                    sHtmlContent3 = oRequestHandler.request()

            if 'thesports4u' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = oRequestHandler.request()
                sPattern2 = '<script>fid="(.+?)"'
                aResult = re.findall(sPattern2, sHtmlContent2)

                if aResult:
                    url2 = 'http://wlive.tv/embed.php?player=desktop&live=' + aResult[0] + '&vw=700&vh=440'
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', 'http://thesports4u.net/')
                    oRequestHandler.addHeaderEntry('Host', 'www.wlive.tv')
                    sHtmlContent3 = oRequestHandler.request()

            if 'soccerstreams' in url:
                url = url.replace('/hds', '/hdss/ch')

                oRequestHandler = cRequestHandler(url)
                sHtmlContent1 = oRequestHandler.request()
                sPattern2 = '<script>fid="(.+?)"'
                aResult = re.findall(sPattern2, sHtmlContent1)

                if aResult:
                    url2 = 'http://wlive.tv/embedra.php?player=desktop&live=' + aResult[0] + '&vw=700&vh=440'
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', url)
                    oRequestHandler.addHeaderEntry('Host', 'www.wlive.tv')
                    sHtmlContent3 = oRequestHandler.request()

            if sHtmlContent3:
                m = re.search('return.*?\[(.*?)\].*?\+\s+(.*)\.join.*document.*?"(.*?)"', sHtmlContent3)
                if m:
                    timeVar = m.group(2)
                    hashVar = m.group(3)

                    # http://tv.wlive.tv/tv/lu2mIWw6KZ20180321/playlist.m3u8?hlsendtime=1542297480&hlsstarttime=0&hlshash=jhTrgemr-kGm9E01YIVfqkZ9VPobibqbDRiov2psf_A=
                    url3 = ''.join(m.group(1).split(','))
                    url3 = url3.replace('"', '').replace('\/', '/')
                    if not url3.startswith('http'):
                        url3 = 'http:' + url3

                    m = re.search(timeVar + '.*?\[(.*?)\]', sHtmlContent3)
                    if m:
                        timeStr = ''.join(m.group(1).split(',')).replace('"', '')
                        url3 += timeStr

                    m = re.search(hashVar + '>(.*?)<', sHtmlContent3)
                    if m:
                        hashStr = ''.join(m.group(1).split(',')).replace('"', '')
                        url3 += hashStr
                        sHosterUrl = url3
                        if Referer:
                            sHosterUrl += '|referer=' + Referer

        if 'sports-stream.net' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'sports-stream.+?ch=(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0]
                url2 = 'http://webtv.ws/embeds.php?live=spstream' + fid + '&vw=700&vh=440'
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'http://www.sports-stream.net/chtv/sps.php?ch=' + fid)
                sHtmlContent2 = oRequestHandler.request()

                sPattern3 = 'source src="(.+?)".+?">'
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]

        if 'sports-stream.link' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'sports-stream.+?ch=(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0]
                url2 = 'https://www.airhdx.com/embedd.php?live=spstream' + fid + '&vw=700&vh=440'
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'http://www.sports-stream.link/chtv/sps.php?ch=' + fid)
                sHtmlContent2 = oRequestHandler.request()

                sPattern3 = 'source: "(.+?)",'
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0] + '|referer=' + url2

        if 'foot.futbol' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                Referer = sHosterUrl2
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = oRequestHandler.request()
                sPattern3 = '<source src="([^"]+)"'
                aResult2 = re.findall(sPattern3, sHtmlContent3)
                if aResult2:
                    sHosterUrl = aResult2[0]

        if 'viewhd.me' in url:  # Pas terminer je sais pas comment on trouve le m3u dans hdstream
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<script>fid="([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = 'http://www.hdstream.live/embed.php?player=desktop&live=' + aResult[0] + '&vw=620&vh=490'
                Referer = sHosterUrl2
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = oRequestHandler.request()

        if 'socolive.pro' in url:  # OK
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'channel=\'(.+?)\', g=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                for aEntry in aResult:
                    channel = aEntry[0]
                    g = aEntry[1]

            url2 = 'https://web.uctnew.com/hembedplayer/' + channel + '/' + g + '/700/480'
            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', 'http://new.socolive.pro/')
            sHtmlContent2 = oRequestHandler.request()

            sPatternUrl = 'hlsUrl = "https:\/\/" \+ ea \+ "([^"]+)"'
            sPatternPK = 'var pk = "([^"]+)"'
            sPatternEA = 'ea = "([^"]+)";'
            aResultUrl = re.findall(sPatternUrl, sHtmlContent2)
            aResultEA = re.findall(sPatternEA, sHtmlContent2)
            aResultPK = re.findall(sPatternPK, sHtmlContent2)
            if aResultUrl and aResultPK and aResultEA:
                aResultPK = aResultPK[0][:53] + aResultPK[0][54:]   # une lettre s'est glissé dans le code :D
                url3 = aResultEA[0] + aResultUrl[0] + aResultPK
                sHosterUrl = 'https://' + url3

        if 'socolive.xyz' in url or 'sportsfix' in url or 'bartsim' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'iframe src="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                url2 = aResult[0]
                if not url.startswith('http'):
                    url2 = "http:" + url2
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()

                sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
                aResult = re.findall(sPattern2, sHtmlContent2)

                if aResult:
                    str2 = aResult[0]
                    if not str2.endswith(';'):
                        str2 = str2 + ';'

                    strs = cPacker().unpack(str2)
                    sPattern3 = '{source:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, strs)
                    if aResult1:
                        sHosterUrl = aResult1[0] + '|User-Agent=' + UA + '&referer=' + url2
                    else:
                        sPattern3 = 'src="([^"]+)"'
                        aResult1 = re.findall(sPattern3, strs)
                        if aResult1:
                            sHosterUrl = aResult1[0] + '|User-Agent=' + UA + '&referer=' + url2

        if '1me.club' in url or 'sportz' in url or 'streamhd' in url or 'hdsportslive' in url or 'cricfree' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()

            if 'hdsportslive' in url or 'cricfree' in url:
                sPattern2 = 'document.write\(unescape\(\'(.+?)\'\)\)'
                aResult = re.findall(sPattern2, sHtmlContent2)
                unQuote = Unquote(aResult[0])

                sPattern2 = '<iframe.+?src="(.+?)"'
                aResult = re.findall(sPattern2, unQuote)

                url = aResult[0]
                if not url.startswith('http'):
                    url = 'https:' + url

                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = oRequestHandler.request()

                sPattern2 = '<iframe.+?src=\'(.+?)\''
                aResult = re.findall(sPattern2, sHtmlContent2)

            else:
                sPattern2 = '<iframe src="(.+?)"'
                aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:

                if 'wstream.to' in aResult[0] or 'streamcdn' in aResult[0]:  # Terminé
                    embedUrl = aResult[0]

                    if embedUrl.startswith('//'):
                        embedUrl = 'https:' + embedUrl

                    if 'sportz' in url or 'hdsportslive' in url or 'cricfree' in url:
                        Referer = url
                    else:
                        Referer = 'http://1me.club'

                    oRequestHandler = cRequestHandler(embedUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', Referer)
                    sHtmlContent3 = oRequestHandler.request()

                    sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
                    aResult = re.findall(sPattern2, sHtmlContent3)

                    if aResult:
                        str2 = aResult[0]
                        if not str2.endswith(';'):
                            str2 = str2 + ';'

                    strs = cPacker().unpack(str2)
                    sPattern3 = '{source:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, strs)
                    if aResult1:
                        sHosterUrl = aResult1[0]

                if 'widestream.io' in aResult[0]:  # Terminé
                    oRequestHandler = cRequestHandler(aResult[0])
                    sHtmlContent3 = oRequestHandler.request()
                    sPattern3 = 'file:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, sHtmlContent3)
                    if aResult1:
                        sHosterUrl = aResult1[0]

        if ('shd' in url) or ('hd' in url and 'streamhd' not in url and 'hdsportslive' not in url and 'airhdx'
                              not in url and 'wizhd' not in url):

            urlApi = 'https://api.livesports24.online/gethost'
            sHtmlContent2 = ''
            channel = url.split('/')[4]
            try:
                oRequestHandler = cRequestHandler(urlApi)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                oRequestHandler.addHeaderEntry('Origin', 'https://' + url.split('/')[2])
                sHtmlContent2 = oRequestHandler.request()
            except:
                pass
            if sHtmlContent2:

                sPattern1 = '([^"]+)'
                aResult = re.findall(sPattern1, sHtmlContent2)
                if aResult:
                    host = aResult[0]
            else:
                urlApi = 'https://api.livesports24.online:8443/gethost'
                channel = url.split('/')[4]
                oRequestHandler = cRequestHandler(urlApi)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                oRequestHandler.addHeaderEntry('Origin', 'https://' + url.split('/')[2])
                sHtmlContent2 = oRequestHandler.request()

                sPattern1 = '([^"]+)'
                aResult = re.findall(sPattern1, sHtmlContent2)
                if aResult:
                    host = aResult[0]

            sHosterUrl = 'https://' + host + '/' + channel + '.m3u8'

        if 'sportgol7' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '<source src="(.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'nowlive.pro' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent3 = oRequestHandler.request()
            sPattern3 = 'src%3A%20%22//([^"]+)%3A([^"]+)m3u8'
            aResult1 = re.findall(sPattern3, sHtmlContent3)
            if aResult1:
                ip = aResult1[0][0]
                name = aResult1[0][1]
                sHosterUrl = 'http://' + ip + ':' + name + 'm3u8'

        if 'harleyquinn' in url or 'joker' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'fid="(.+?)"; v_width=(.+?); v_height=(.+?);'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0][0]
                vw = aResult[0][1]
                vh = aResult[0][2]

                url2 = 'http://www.jokersplayer.xyz/embed.php?u=' + fid + '&vw=' + vw + '&vh=' + vh
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()
                sPattern3 = 'src=http://(.+?)/(.+?) '
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    ip = aResult[0][0]
                    url3 = 'http://' + ip + '/' + aResult[0][1]
                    oRequestHandler = cRequestHandler(url3)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', url2)
                    oRequestHandler.addHeaderEntry('Connection', 'keep-alive')
                    sHtmlContent2 = oRequestHandler.request()
                    sPattern3 = 'src=.+?e=(.+?)&st=(.+?)&'
                    aResult = re.findall(sPattern3, sHtmlContent2)
                    if aResult:
                        e = aResult[0][0]
                        st = aResult[0][1]
                        sHosterUrl = 'http://' + ip + '/live/' + fid + '.m3u8'+'?e=' + e + '&st=' + st

                if sHosterUrl == '':
                    url2 = 'http://player.jokehd.com/one.php?u=' + fid + '&vw=' + vw + '&vh=' + vh
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', url)
                    sHtmlContent2 = oRequestHandler.request()
                    sPattern3 = 'source: \'(.+?)\''
                    aResult = re.findall(sPattern3, sHtmlContent2)
                    if aResult:
                        sHosterUrl = aResult[0]

        if 'baltak.biz' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="\/blok.php\?id=(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                url2 = aResult[0]
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'http://baltak.biz/blok.php?id=' + url2)
                sHtmlContent2 = oRequestHandler.request()

                sPattern2 = 'source: \'(.+?)\''
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]
            else:
                sPattern2 = 'source: \"(.+?)\"'
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]

        if 'footballstream' in url:  # Terminé
            url = url.replace('/streams', '/hdstreams')
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'fid="(.+?)"; v_width=(.+?); v_height=(.+?);'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0][0]
                vw = aResult[0][1]
                vh = aResult[0][2]

                embedded = "mobile"  # "desktop"

                url2 = 'http://www.b4ucast.me/embedra.php?player=' + embedded + '&live=' + fid + '&vw=' + vw + '&vh=' + vh
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()

                sPattern3 = 'source: *["\'](.+?)["\']'
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    sHosterUrl = 'http:' + aResult[0]

        if 'tennistvgroup' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()

            sPattern2 = 'source: *["\'](.+?)["\']'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'box-live.stream' in url:  # Terminé
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', sUrl4)

            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + url
            else:
                sPattern2 = 'var source = \"(.+?)\"'
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]
                else:
                    sPattern2 = '<iframe.+?src="(http.+?)".+?</iframe>'
                    aResult = re.findall(sPattern2, sHtmlContent2)
                    if aResult:
                        Referer = url
                        url = aResult[0]  # decryptage plus bas (telerium)

        if 'telerium.tv' in url:  # WIP
            oRequestHandler = cRequestHandler(url)
            if Referer:
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                str2 = aResult[0]
                if not str2.endswith(';'):
                    str2 = str2 + ';'

                strs = cPacker().unpack(str2)

                sPattern3 = '{url:window\.atob\((.+?)\)\.slice.+?\+window\.atob\((.+?)\)'
                aResult1 = re.findall(sPattern3, strs)
                if aResult1:
                    m3u = aResult1[0][0]
                    sPatternM3u = m3u + '="(.+?)"'
                    m3u = re.findall(sPatternM3u, strs)
                    m3u = base64.b64decode(m3u[0])[14:]

                    token = aResult1[0][1]
                    sPatterntoken = token + '="(.+?)"'
                    token = re.findall(sPatterntoken, strs)
                    token = base64.b64decode(token[0])

                    sHosterUrl = 'https://telerium.tv/' + m3u + token + '|referer=' + url

        # TODO A TESTER
        if 'usasports.live' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = 'var sou = "  (.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        # TODO A TESTER
        if 'wiz1' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '"iframe" src="(.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'var16.ru' in url:
            sHosterUrl = getHosterVar16(url, url)

        # TODO A TESTER
        if 'livesportone' in url:
            url = url.replace('livesportone.com', 'sportes.pw')

            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0] + '|User-Agent=' + UA + '&referer=' + url
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent3 = oRequestHandler.request()
                sPattern3 = 'source: "([^"]+)"'
                aResult1 = re.findall(sPattern3, sHtmlContent3)
                if aResult1:
                    sHosterUrl = aResult1[0] + '|User-Agent=' + UA + '&referer=' + url

        # Tentative avec les pattern les plus répendus
        if not sHosterUrl:
            sHosterUrl = getHosterIframe(url, url)

        if sHosterUrl:
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(".m3u8")
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle2)  # nom affiche
                oHoster.setFileName(sMovieTitle2)  # idem
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        oGui.setEndOfDirectory()


def getHosterVar16(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'file:\"([^"]+)\"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + url

    sPattern = 'src=\"(.+?)\"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        referer = url
        url = 'http://var16.ru/' + aResult[0]
        return getHosterVar16(url, referer)


# Traitement générique
def getHosterIframe(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + url

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
            url = getHosterIframe(url, referer)
            if url:
                return url

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return url

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
            return code + '|Referer=' + url
        except Exception as e:
            pass
    
    return False


