# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 05 10072020
# update 09012021 - uniquement format mpd disponible

import re
import time
import json
from hashlib import sha1
import hmac
import binascii

from resources.lib.gui.hoster import cHosterGui 
from resources.lib.gui.gui import cGui 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.lib.comaddon import progress, dialog, xbmc, VSPath #, VSlog


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
SITE_IDENTIFIER = 'viki_com'
SITE_NAME = 'Viki'
SITE_DESC = 'Emissions TV, Series et films asiatiques' 

URL_MAIN = 'https://www.viki.com/'

URLMAIN_API = 'https://api.viki.io/v4/'
MOVIE_GENRES = (True, 'showMovieGenre')
MOVIE_PAYS = (True, 'showMoviePays')

MOVIE_NEW = (URLMAIN_API + 'movies.json?sort=newest_video&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_RECENT = (URLMAIN_API + 'movies.json?sort=views_recent&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_POPULAR = (URLMAIN_API + 'movies.json?sort=trending&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_BEST = (URLMAIN_API + 'movies.json?sort=views&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_DATE_CREATED = (URLMAIN_API + 'movies.json?sort=created_at&page=1&per_page=50&app=100000a&t=', 'showMovies')

SERIE_GENRES = (True, 'showSerieGenre')
SERIE_PAYS = (True, 'showSeriePays')

SERIE_NEW = (URLMAIN_API + 'series.json?sort=newest_video&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_RECENT = (URLMAIN_API + 'series.json?sort=views_recent&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_POPULAR = (URLMAIN_API + 'series.json?sort=trending&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_BEST = (URLMAIN_API + 'series.json?sort=views&page=1&per_page=50&app=100000a&t=', 'showMovies')
SERIE_DATE_CREATED = (URLMAIN_API + 'series.json?sort=created_at&page=1&per_page=50&app=100000a&t=', 'showMovies')

URL_SEARCH = (URLMAIN_API + 'search.json?page=1&per_page=50&app=100000a&term=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuSeries')

se = 'true'  # activation des sous titres
# lang = 'en' ou 'fr'

def load():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Pays)', 'films.png', oOutputParameterHandler)

    # 21 results
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEW[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEW[1], 'Films (News)', 'news.png', oOutputParameterHandler)

    # no result
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_RECENT[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_RECENT[1], 'Films (Récents)', 'news.png', oOutputParameterHandler)

    # 8 results
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_POPULAR[1], 'Films (Populaires)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():

    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Série (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAYS[1], 'Séries (Pays)', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEW[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEW[1], 'Séries (News)', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_RECENT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_RECENT[1], 'Séries (Recent)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_POPULAR[1], 'Séries (Populaire)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_BEST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_BEST[1], 'Séries (Best)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch(): 
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):

    oGui = cGui()  
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch

    url = sUrl
    timestamp = str(int(time.time()))

    if not 'search.json' in url:
        url = url + timestamp

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    sJsonContent = oRequestHandler.request()
    jsonrsp = json.loads(sJsonContent)

    if not jsonrsp:
        oGui.addText(SITE_IDENTIFIER)

    if len(jsonrsp['response']) >= 0:
        total = len(jsonrsp['response'])
        progress_ = progress().VScreate(SITE_NAME)
        for movie in range(0, len(jsonrsp['response'])):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                    break  

            try:
                if (jsonrsp['response'][movie]['flags']['licensed'] == True):
                    if jsonrsp['response'][movie]['type'] == 'series':
    
                        sTitle = jsonrsp['response'][movie]['titles']['en']
                        # sTitle = jsonrsp['response'][movie]['titles']['fr']  # résultats melangés en/fr
                        sThumb = jsonrsp['response'][movie]['images']['poster']['url']  # thumb size 120ko
                        # sThumb = jsonrsp['response'][movie]['images']['atv_cover']['url']  # thumb size 800 ko
                        sUrl2 = 'https://api.viki.io/v4/series/' + jsonrsp['response'][movie]['id'] + '/episodes.json?page=1&per_page=50&app=100000a&t=' + str(timestamp)
                        sDesc = jsonrsp['response'][movie]['descriptions']['fr'].encode('utf-8', 'ignore')
                        # sDesc = jsonrsp['response'][movie]['descriptions']['en'].encode('utf-8', 'ignore')
    
                        sDisplayTitle = sTitle
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('sDesc', sDesc)
                        oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                    else:
                        if (jsonrsp['response'][movie]['blocked'] == False): 
                            try:
                                subtitle_completion1 = '0'
                                subtitle_completion1 = str(jsonrsp['response'][movie]['subtitle_completions']['fr'])
                            except:
                                pass
                            try: 
                                subtitle_completion2 = '0'
                                subtitle_completion2 = str(jsonrsp['response'][movie]['subtitle_completions']['en'])
                            except:
                                pass
                            try:
                                mt = ''
                                mt = jsonrsp['response'][movie]['titles']['fr']
                            except:
                                pass
    
                            sDesc = str(mt)
                            sTitle = str(jsonrsp['response'][movie]['titles']['en'].encode('utf-8', 'ignore'))
                            sThumb = str(jsonrsp['response'][movie]['images']['poster']['url'])
                            sUrlapi = str(jsonrsp['response'][movie]['id'] \
                                        + '@' + jsonrsp['response'][movie]['images']['poster']['url'] \
                                        + '@' + subtitle_completion1 + '@' + subtitle_completion2 + '@' + mt)
    
                            sDisplayTitle = sTitle
                            oOutputParameterHandler = cOutputParameterHandler()
                            oOutputParameterHandler.addParameter('siteUrl', sUrlapi)
                            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oOutputParameterHandler.addParameter('sDesc', sDesc)
                            oGui.addMovie(SITE_IDENTIFIER, 'Showlinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            except:
                pass

        progress_.VSclose(progress_)

    if not sSearch:
        if jsonrsp['more'] == True:
            getpage = re.compile('(.+?)&page=(.+?)&per_page=(.+?)&t=').findall(url)
            for fronturl, page, backurl in getpage:
                iNumberPage = int(page) + 1
                url = fronturl + '&page=' + str(iNumberPage) + '&per_page=' + backurl + '&t='
                oOutputParameterHandler.addParameter('siteUrl', url)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNumberPage), oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSaisons():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')  # à recomparer

    url = sUrl 
    url = url + '&direction=asc'
    timestamp = str(int(time.time()))

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    sJsonContent = oRequestHandler.request()
    jsonrsp = json.loads(sJsonContent)

    for episode in range(0, len(jsonrsp['response'])):
        try:
            if (jsonrsp['response'][episode]['blocked'] == False):

                try:
                    subtitle_completion1 = '0'
                    subtitle_completion1 = str(jsonrsp['response'][episode]['subtitle_completions']['fr'])
                except:
                    pass
                try:
                    subtitle_completion2 = '0'
                    subtitle_completion2 = str(jsonrsp['response'][episode]['subtitle_completions']['en'])
                except:
                    pass
                try:
                    et = ''
                    et = jsonrsp['response'][episode]['titles']['en']
                except:
                    pass

                sTitle = jsonrsp['response'][episode]['container']['titles']['en'] + ' Episode ' + str(jsonrsp['response'][episode]['number']) 
                sUrl = str(jsonrsp['response'][episode]['id'] \
                            + '@' + jsonrsp['response'][episode]['images']['poster']['url'] \
                            + '@' + subtitle_completion1 + '@' + subtitle_completion2 + '@' + et)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'Showlinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                # VSlog('showSaisons() block = true')
                pass

        except:
            # VSlog('showSaisons() excepted ')
            pass

    if len(jsonrsp['response']) == 0:
        # VSlog('pas d'episodes')
        pass

    if jsonrsp['more'] == True:
        getpage = re.compile('(.+?)page=(.+?)&per_page').findall(url)
        for fronturl, page in getpage:
            newpage = int(page) + 1
            url = fronturl + 'page=' + str(newpage) + '&per_page=50&app=100000a&t=' + timestamp
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieGenre():
    oGui = cGui()
    showgenre = 'movies'
    url = 'https://api.viki.io/v4/videos/genres.json?app=100000a'

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    sJsonContent = oRequestHandler.request()
    jsonrsp  = json.loads(sJsonContent)

    for genre in range(0, len(jsonrsp)):

        typegenre = jsonrsp[genre]['name']['fr']  # or jsonrsp[genre]['name']['en']
        urlgenre = 'https://api.viki.io/v4/' + showgenre + '.json?sort=newest_video&page=1&per_page=50&app=100000a&genre=' + jsonrsp[genre]['id'] + '&t='

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', urlgenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', typegenre.capitalize(), 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showSerieGenre():
    oGui = cGui()

    showgenre = 'series'
    url = 'https://api.viki.io/v4/videos/genres.json?app=100000a'
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    sJsonContent = oRequestHandler.request()
    jsonrsp  = json.loads(sJsonContent)

    for genre in range(0, len(jsonrsp)):
        urlgenre = 'https://api.viki.io/v4/' + showgenre + '.json?sort=newest_video&page=1&per_page=50&app=100000a&genre=' + jsonrsp[genre]['id'] + '&t='
        typegenre = jsonrsp[genre]['name']['fr']
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', urlgenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', typegenre.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviePays():
    showPays('movies')


def showSeriePays():
    showPays('series')


def showPays(genre):

    oGui = cGui()
    url = 'https://api.viki.io/v4/videos/countries.json?app=100000a'
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    sJsonContent = oRequestHandler.request()
    jsonrsp  = json.loads(sJsonContent)
    # site ou il n'y a jamais rien
    sBlaccountryList = ['tw', 'ca', 'us', 'gb', 'th', 'ph', 'es']

    for country, subdict in jsonrsp.items():
        if country in sBlaccountryList:
            continue

        else:
            urlcountry = 'https://api.viki.io/v4/' + genre + '.json?sort=newest_video&page=1&per_page=50&app=100000a&origin_country=' + country + '&t='
            country = jsonrsp[country]['name']['en']
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlcountry)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', country.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

# Signature des demandes au nom de Flash player
def SIGN(url, pth):
    timestamp = str(int(time.time()))
    key = 'MM_d*yP@`&1@]@!AVrXf_o-HVEnoTnm$O-ti4[G~$JDI/Dc-&piU&z&5.;:}95=Iad'
    rawtxt = '/v4/videos/' + url + pth + '?app=100005a&t=' + timestamp + '&site=www.viki.com'
    hashed = hmac.new(key, rawtxt, sha1)
    fullurl = 'https://api.viki.io' + rawtxt + '&sig=' + binascii.hexlify(hashed.digest())
    return fullurl

def GET_SUBTILES(url, subtitle_completion1, subtitle_completion2):

    try:
        srtsubs_path1 = VSPath('special://temp/vstream_viki_SubFrench.srt')
        srtsubs_path2 = VSPath('special://temp/vstream_viki_SubEnglish.srt')
        if (int(subtitle_completion1)>79 and se == 'true'):
            urlreq = SIGN(url, '/subtitles/fr.srt')
            oRequestHandler = cRequestHandler(urlreq)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            data = oRequestHandler.request()
            with open(srtsubs_path1, "w") as subfile:
                subfile.write(data)

        if (int(subtitle_completion2)>0 and se == 'true'):
            urlreq = SIGN(url, '/subtitles/en.srt')
            oRequestHandler = cRequestHandler(urlreq)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            data = oRequestHandler.request()
            with open(srtsubs_path2, "w") as subfile:
                subfile.write(data)
        else:
            # VSlog('GET_SUBTILES:erreur completion')
            pass
    except:
        # VSlog('GET_SUBTILES:erreur exception')
        pass
    return srtsubs_path1, srtsubs_path2


def GET_URLS_STREAM(url):
    qlist = ['480p', '360p', '240p', 'mpd']  # plus de '480p', '360p', '240p ?
    streamUrllist = []
    validq = []

    urlreq = SIGN(url, '/streams.json')
    oRequestHandler = cRequestHandler(urlreq)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sJsonContent = oRequestHandler.request()
    jsonrsp  = json.loads(sJsonContent)

    testeurl = ''
    testeq = ''
    for qual in qlist:
        basehttp = 'https'
        if qual in jsonrsp:
            if qual == 'mpd':
                basehttp = 'http'
            streamUrllist.append(jsonrsp[qual][basehttp]['url'])
            validq.append(qual)
            testeurl = jsonrsp[qual][basehttp]['url']
            testeq = qual

    # ajout du teste à enlever + 1 à revoir et
    streamUrllist.append(testeurl)
    validq.append(testeq)

    return validq, streamUrllist


def Showlinks():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Datalist = []

    url, thumbnail, sub_pourcent1, sub_pourcent2, stitle = sUrl.split("@")
    sSubPathFr2, sSubPathEn2 = GET_SUBTILES(url, sub_pourcent1, sub_pourcent2)
    qualityList2, streamList2 = GET_URLS_STREAM(url)

    Datalist.append(sSubPathFr2)
    Datalist.append(sSubPathEn2)

    for item in qualityList2:
        Datalist.append(item)

    for item in streamList2:
        Datalist.append(item)

    oHoster = cHosterGui().checkHoster('viki')
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, Datalist, sThumb)

    oGui.setEndOfDirectory()
