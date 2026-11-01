# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import time
import datetime
import requests

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil, HEURE_HIVER


##################################
import json
import ssl
import sys

test_url = "https://jn306.sportvideodata.com/6781996426432173495_AN6MDOwAjMzkjN/p4.m3u8"
test_Referer = test_url

test_headers = {
    'Referer': test_Referer,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36',
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, identity;q=1, *;q=0',
    # 'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pt;q=0.5,it;q=0.4,ru;q=0.3',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'Sec-Fetch-Dest': 'video',
    # 'Sec-Fetch-Mode': 'cors',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'Range': 'bytes=0-',
    # 'sec-ch-ua': '"Not:A-Brand";v="8", "Chromium";v="156", "Google Chrome";v="156"',
    # 'sec-ch-ua-mobile': '?0',
    # 'cache-control': 'no-cache',
    # 'Pragma': 'no-cache',
    # 'Priority': 'i',
}

test_urllib3 = requests.packages.urllib3
print("Python :", sys.version.split()[0], "| OpenSSL :", ssl.OPENSSL_VERSION)
print("requests :", requests.__version__, requests.__file__)
print("urllib3 :", test_urllib3.__version__, test_urllib3.__file__)
print("SSLContext :", test_urllib3.util.ssl_.SSLContext)


class _TestAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        test_context = test_urllib3.util.ssl_.create_urllib3_context(
            ciphers=('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:'
                     'ECDH+AESGCM:DH+AESGCM:ECDH+AES:DH+AES:RSA+AESGCM:'
                     'RSA+AES:!aNULL:!eNULL:!MD5:!DSS'))
        test_context.minimum_version = ssl.TLSVersion.TLSv1_2
        pool_kwargs['ssl_context'] = test_context
        return super(_TestAdapter, self).init_poolmanager(
            connections, maxsize, block=block, **pool_kwargs)


try:
    with requests.Session() as test_session:
        test_session.mount('https://', _TestAdapter())
        with test_session.get(test_url, headers=test_headers, stream=True, timeout=5) as response:
            # print("HTTP :", response.status_code, "| Protocol :", response.raw.version)
            # print("Redirected :", response.url != test_url)
            # test_connection = getattr(response.raw, '_connection', None)
            # test_socket = getattr(test_connection, 'sock', None)
            # if test_socket is not None:
            #     print("Peer :", test_socket.getpeername()[0])
            #     print("TLS :", test_socket.version(), "| ALPN :", test_socket.selected_alpn_protocol())
            #     print("Cipher :", test_socket.cipher()[0])
            # print("Headers :", response.headers)
            test_body = response.raw.read(300, decode_content=True)
            # print("Body :", repr(test_body))
except requests.RequestException as error:
    print("Request error :", error)
    
###################################

    
SITE_IDENTIFIER = 'sportplus'
SITE_NAME = 'Sport +'
SITE_DESC = 'Regarder le sport en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_API')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36'
                      
SPORT_SPORTS = (True, 'load')
SPORT_GENRES = ('v3/fr/sidebar.json', 'showGenres')
SPORT_LIVE = ('v3.1/matches/index?fw=3.1&lang=fr&offset=7200&sport_id=top', 'showLive')  # streaming Actif



def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Par genres', 'genre_sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'En cours', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oUtil = cUtil()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oUtil.formatUTF8(sHtmlContent)
    genres = json.loads(sHtmlContent)

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in sorted(genres, key=lambda genre: genre['name']):
        if 'type' in genre:
            continue
        sUrl = genre['alias']
        sTitle = genre['name']
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLive():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_API + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    tournaments = sHtmlContent['resolve']['mapTournaments']
    t2 = {}
    for t in tournaments:
        t2[t] = tournaments[t]['alias']
    tournaments = t2

    oOutputParameterHandler = cOutputParameterHandler()
    for item in sHtmlContent['items']:
        sTitle = item['name'].replace(u'—', u'-')
        sportId = item['sport_id']
        sUrl = 'id=%s&sport_id=%s' % (item['id'], sportId)
        sDate = item['start']
        sDisplayTitle = sTitle
        if sDate:
            # Parse avec timezone
            dt = datetime.datetime(*(time.strptime(sDate[:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
            # Timezone France
            dt = dt - datetime.timedelta(hours= (2 if HEURE_HIVER else 1))
            # Conversion
            sDate = dt.strftime("%d/%m %H:%M")
            sDisplayTitle = ('%s - %s') % (sDate, sTitle)
        
        tournamentId = item['tournament_id']
        if tournamentId:
            tournamentId = str(tournamentId)
            tournament = tournaments.get(tournamentId, None)
            sUrl += '&tournament_id=' + (tournament if tournament else tournamentId)
            if tournament:
                sDisplayTitle += ' [COLOR yellow][%s][/COLOR]' % tournament.replace('-', ' ').upper()

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sportId = oInputParameterHandler.getValue('siteUrl')
    sUrl = URL_API + 'v3.1/matches/index?fw=3.1&lang=fr&offset=7200&sport_id=' + sportId

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    tournaments = sHtmlContent['resolve']['mapTournaments']
    t2 = {}
    for t in tournaments:
        t2[t] = tournaments[t]['alias']
    tournaments = t2

    oOutputParameterHandler = cOutputParameterHandler()
    for item in sHtmlContent['items']:
        taglive = item['status'] == 'live'
        sTitle = item['name'].replace(u'—', u'-')
        sUrl = 'id=%s&sport_id=%s' % (item['id'], sportId)
        sDate = item['start']
        sDisplayTitle = sTitle
        if sDate:
            # Parse avec timezone
            dt = datetime.datetime(*(time.strptime(sDate[:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
            # Timezone France
            dt = dt - datetime.timedelta(hours= (2 if HEURE_HIVER else 1))
            # Conversion
            sDate = dt.strftime("%d/%m %H:%M")
            sDisplayTitle = ('%s - %s') % (sDate, sTitle)
        
        tournamentId = item['tournament_id']
        if tournamentId:
            tournamentId = str(tournamentId)
            tournament = tournaments.get(tournamentId, None)
            sUrl += '&tournament_id=' + (tournament if tournament else tournamentId)
            if tournament:
                sDisplayTitle += ' [COLOR yellow][%s][/COLOR]' % tournament.replace('-', ' ').upper()

        if taglive:
            sDisplayTitle += ' [COLOR green][En cours][/COLOR]'

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = URL_API + 'v3.1/matches/view?' + sUrl +'&lang=fr&fw=3.1&has_regions=0'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    item = sHtmlContent['item']
    if item:
        oHoster = cHosterGui().checkHoster(".m3u8")
        links = item.get('ls')
        if links:
            for sHosterUrl in links:
                oHoster.setDisplayName(sMovieTitle)  # nom affiche
                oHoster.setFileName(sMovieTitle)  # idem
                testUrl = sHosterUrl#.replace('pl.m3', 'output-0.m3')
#                testUrl = 'https://jn297.sportvideodata.com/11654316931697566728_wM0YWZjFWYzQmZwEWLyETZ50SNwUDNtgDO2UTL3QTZjVWMzE2L1JnLpBXYzRncvB3cu8WZklmd/pl.m3u8'

                oRequestHandler = cRequestHandler(testUrl)
                oRequestHandler.addHeaderEntry('Referer', testUrl)#'https://jn315.sportvideodata.com/')#https://apisplus.live/')
                oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36')
                oRequestHandler.addHeaderEntry('Accept', '*/*')
                oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, identity;q=1, *;q=0')
                oRequestHandler.addHeaderEntry('Sec-Fetch-Site', 'same-origin')
                oRequestHandler.addHeaderEntry('Sec-Fetch-Dest', 'video')
                oRequestHandler.addHeaderEntry('Sec-Fetch-Mode', 'cors')
                oRequestHandler.addHeaderEntry('sec-ch-ua-platform', '"Windows"')
                oRequestHandler.addHeaderEntry('Range', 'bytes=0-')
                oRequestHandler.addHeaderEntry('sec-ch-ua', '"Not:A-Brand";v="8", "Chromium";v="156", "Google Chrome";v="156"')
                oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0')
                oRequestHandler.addHeaderEntry('cache-control', 'no-cache')
                oRequestHandler.addHeaderEntry('Pragma', 'no-cache')
                oRequestHandler.addHeaderEntry('Priority', 'i')




                # oRequestHandler.addHeaderEntry('access-control-allow-methods', 'GET, OPTIONS')
                # oRequestHandler.addHeaderEntry('access-control-allow-origin', '*')
                # oRequestHandler.addHeaderEntry('content-type', 'application/vnd.apple.mpegurl; charset=utf-8')
                # oRequestHandler.addHeaderEntry('cache-control', 'public, max-age=1')

                sHtmlContent = oRequestHandler.request()

#                r = requests.get(sHosterUrl, timeout=15)


                
                sHosterUrl += '|User-Agent=' + UA + '&Referer=' + URL_MAIN
                
#                sHosterUrl += '|Referer=' + sHosterUrl
#                sHosterUrl += '|Referer=https://fr.sportplus.live'
                # sHosterUrl = 'https://jn255.sportvideodata.com/1708759367206891621_gTdz0mL0NXaslXYsB3L5ITbhVmc0N3Lx82Lt92YuUWbhdGN0Z2bz5ibkNmY/p9.m3u8'
                #
                # oRequestHandler = cRequestHandler(sHosterUrl)
                # oRequestHandler.addHeaderEntry('Referer', 'https://apisplus.live/')
                # oRequestHandler.addHeaderEntry('Sec-Fetch-Dest', 'document')
                # oRequestHandler.addHeaderEntry('Sec-Fetch-Mode', 'navigate')
                # oRequestHandler.addHeaderEntry('Sec-Fetch-Site', 'cross-site')
                # oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
                # oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
                # oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36')
                # sHtmlContent = oRequestHandler.request()
                #
                #
                # oRequestHandler = cRequestHandler(sHosterUrl)
                # oRequestHandler.addCookieEntry('_cq_duid', '1.1787503367.GKM2o3GhB5zPdB9b')
                # oRequestHandler.addCookieEntry('_cq_session', '1.1787503367693.8ID2P1K8nILdc5IG.1787503370574')
                # oRequestHandler.addHeaderEntry('Referer', sHosterUrl)
                # oRequestHandler.addHeaderEntry('Cookie', '_cq_duid=1.1787503367.GKM2o3GhB5zPdB9b; _cq_session=1.1787503367693.8ID2P1K8nILdc5IG.1787503370574')
                # oRequestHandler.addHeaderEntry('Sec-Fetch-Dest', 'video')
                # oRequestHandler.addHeaderEntry('Sec-Fetch-Mode', 'cors')
                # oRequestHandler.addHeaderEntry('Sec-Fetch-Site', 'same-origin')
                # oRequestHandler.addHeaderEntry('Cache-Control', 'no-cache')
                # oRequestHandler.addHeaderEntry('Pragma', 'no-cache')
                # oRequestHandler.addHeaderEntry('Priority', 'i')
                # oRequestHandler.addHeaderEntry('Range', 'bytes=0-')
                # oRequestHandler.addHeaderEntry('Accept', '*/*')
                # oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, identity;q=1, *;q=0')
                # oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pt;q=0.5,it;q=0.4,ru;q=0.3')
                # oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36')
                # oRequestHandler.addHeaderEntry('sec-ch-ua', 'Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"')
                # oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0')
                # oRequestHandler.addHeaderEntry('sec-ch-ua-platform', 'windows')
                # sHtmlContent = oRequestHandler.request()

                
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
