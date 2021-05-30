# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 05 10072020
# update 15012021 - uniquement format mpd disponible

import re
import time
from hashlib import sha1
import hmac
import binascii
import xbmcvfs

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, isMatrix

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
SITE_IDENTIFIER = 'viki_com'
SITE_NAME = 'Viki'
SITE_DESC = 'Emissions TV, Séries et films asiatiques'

URL_MAIN = 'https://www.viki.com/'
URL_API = 'https://api.viki.io/v4/'

DRAMA_DRAMAS = (True, 'load')

# il n'existe qu'une vingtaine de films
MOVIE_GENRES = (True, 'showMovieGenre')
MOVIE_PAYS = (True, 'showMoviePays')
MOVIE_NEWS = (URL_API + 'movies.json?sort=newest_video&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_RECENT = (URL_API + 'movies.json?sort=views_recent&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_POPULAR = (URL_API + 'movies.json?sort=trending&page=1&per_page=50&app=100000a&t=', 'showMovies')
MOVIE_BEST = (URL_API + 'movies.json?sort=views&page=1&per_page=50&app=100000a&t=', 'showMovies')

DRAMA_GENRES = (True, 'showSerieGenre')
DRAMA_PAYS = (True, 'showSeriePays')
DRAMA_NEWS = (URL_API + 'series.json?sort=newest_video&page=1&per_page=50&app=100000a&t=', 'showMovies')
DRAMA_RECENT = (URL_API + 'series.json?sort=views_recent&page=1&per_page=50&app=100000a&t=', 'showMovies')
DRAMA_POPULAR = (URL_API + 'series.json?sort=trending&page=1&per_page=50&app=100000a&t=', 'showMovies')
DRAMA_BEST = (URL_API + 'series.json?sort=views&page=1&per_page=50&app=100000a&t=', 'showMovies')

URL_SEARCH = (URL_API + 'search.json?page=1&per_page=50&app=100000a&term=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
URL_SEARCH_DRAMAS = (URL_SEARCH[0], 'showMovies')

se = 'true'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (News)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Pays)', 'lang.png', oOutputParameterHandler)

    # 8 results
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_POPULAR[1], 'Films (Populaires)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DRAMA_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_PAYS[1], 'Séries (Pays)', 'lang.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_NEWS[1], 'Séries (News)', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_RECENT[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_RECENT[1], 'Séries (Récentes)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_POPULAR[1], 'Séries (Populaires)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_BEST[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_BEST[1], 'Séries (Best)', 'notes.png', oOutputParameterHandler)

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

    if 'search.json' not in url:
        url = url + timestamp

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    if not jsonrsp:
        oGui.addText(SITE_IDENTIFIER)

    oOutputParameterHandler = cOutputParameterHandler()
    if len(jsonrsp['response']) > 0:
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
                        sUrl2 = URL_API + 'series/' + jsonrsp['response'][movie]['id'] + '/episodes.json?page=1&per_page=50&app=100000a&t=' + str(timestamp)
                        
                        try:
                            sDesc = jsonrsp['response'][movie]['descriptions']['fr']
                        except:
                            sDesc = ''
                        

                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        if not isMatrix():
                            oOutputParameterHandler.addParameter('sDesc', sDesc.encode('utf-8', 'ignore'))
                        else:
                            oOutputParameterHandler.addParameter('sDesc', sDesc)

                        oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                    else:
                        if (jsonrsp['response'][movie]['blocked'] == False):
                            subtitle_completion1 = '0'
                            try:
                                subtitle_completion1 = str(jsonrsp['response'][movie]['subtitle_completions']['fr'])
                            except:
                                pass
                            subtitle_completion2 = '0'
                            try:
                                subtitle_completion2 = str(jsonrsp['response'][movie]['subtitle_completions']['en'])
                            except:
                                pass
                            mt = ''
                            try:
                                mt = jsonrsp['response'][movie]['titles']['fr']
                            except:
                                pass

                            sDesc = str(mt)
                            sTitle = str(jsonrsp['response'][movie]['titles']['en'])
                            sThumb = str(jsonrsp['response'][movie]['images']['poster']['url'])
                            sUrlApi = str(jsonrsp['response'][movie]['id'] + '@' +
                                          jsonrsp['response'][movie]['images']['poster']['url'] + '@' +
                                          subtitle_completion1 + '@' + subtitle_completion2 + '@' + mt)

                            oOutputParameterHandler.addParameter('siteUrl', sUrlApi)
                            
                            if not isMatrix():
                                oOutputParameterHandler.addParameter('sMovieTitle', sTitle.encode('utf-8', 'ignore'))
                            else:
                                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)  

                            oOutputParameterHandler.addParameter('sThumb', sThumb)
                            oOutputParameterHandler.addParameter('sDesc', sDesc)
                            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            except:
                pass

        progress_.VSclose(progress_)

    if not sSearch:
        if (jsonrsp['more'] == True):
            getpage = re.compile('(.+?)&page=(.+?)&per_page=(.+?)&t=').findall(url)
            for frontUrl, page, backurl in getpage:
                iNumberPage = int(page) + 1
                url = frontUrl + '&page=' + str(iNumberPage) + '&per_page=' + backurl + '&t='
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', url)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNumberPage), oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    url = sUrl + '&direction=asc'
    timestamp = str(int(time.time()))

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for episode in range(0, len(jsonrsp['response'])):
        try:
            if (jsonrsp['response'][episode]['blocked'] == False):
                subtitle_completion1 = '0'
                try:
                    subtitle_completion1 = str(jsonrsp['response'][episode]['subtitle_completions']['fr'])
                except:
                    pass
                subtitle_completion2 = '0'
                try:
                    subtitle_completion2 = str(jsonrsp['response'][episode]['subtitle_completions']['en'])
                except:
                    pass
                et = ''
                try:
                    et = jsonrsp['response'][episode]['titles']['en']
                except:
                    pass

                sTitle = jsonrsp['response'][episode]['container']['titles']['en'] + ' Episode ' + str(jsonrsp['response'][episode]['number'])
                sUrl = str(jsonrsp['response'][episode]['id'] + '@' +
                           jsonrsp['response'][episode]['images']['poster']['url'] + '@' +
                           subtitle_completion1 + '@' + subtitle_completion2 + '@' + et)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                pass

        except:
            pass

    if len(jsonrsp['response']) == 0:
        pass

    if (jsonrsp['more'] == True):
        getpage = re.compile('(.+?)page=(.+?)&per_page').findall(url)
        for frontUrl, page in getpage:
            newPage = int(page) + 1
            url = frontUrl + 'page=' + str(newPage) + '&per_page=50&app=100000a&t=' + timestamp
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieGenre():
    oGui = cGui()

    sGenre = 'movies'
    url = URL_API + 'videos/genres.json?app=100000a'
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in range(0, len(jsonrsp)):
        typeGenre = jsonrsp[genre]['name']['fr']  # or jsonrsp[genre]['name']['en']
        urlGenre = URL_API + sGenre + '.json?sort=newest_video&page=1&per_page=50&app=100000a&genre=' + jsonrsp[genre]['id'] + '&t='

        oOutputParameterHandler.addParameter('siteUrl', urlGenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', typeGenre.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenre():
    oGui = cGui()

    sGenre = 'series'
    url = URL_API + 'videos/genres.json?app=100000a'
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in range(0, len(jsonrsp)):
        urlGenre = URL_API + sGenre + '.json?sort=newest_video&page=1&per_page=50&app=100000a&genre=' + jsonrsp[genre]['id'] + '&t='
        typeGenre = jsonrsp[genre]['name']['fr']

        oOutputParameterHandler.addParameter('siteUrl', urlGenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', typeGenre.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviePays():
    showPays('movies')

def showSeriePays():
    showPays('series')

def showPays(genre):

    oGui = cGui()
    url = URL_API + 'videos/countries.json?app=100000a'
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', '')
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    # site ou il n'y a jamais rien
    sBlaccountryList = ['tw', 'ca', 'us', 'gb', 'th', 'ph', 'es']

    oOutputParameterHandler = cOutputParameterHandler()
    for country, subdict in jsonrsp.items():
        if country in sBlaccountryList:
            continue

        else:
            urlcountry = URL_API + genre + '.json?sort=newest_video&page=1&per_page=50&app=100000a&origin_country=' + country + '&t='
            country = jsonrsp[country]['name']['en']
            oOutputParameterHandler.addParameter('siteUrl', urlcountry)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', country.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# Signature des demandes au nom de Flash player
def SIGN(url, pth):
    timestamp = str(int(time.time()))
    key = 'MM_d*yP@`&1@]@!AVrXf_o-HVEnoTnm$O-ti4[G~$JDI/Dc-&piU&z&5.;:}95=Iad'
    rawtxt = '/v4/videos/'+url+pth+'?app=100005a&t='+timestamp+'&site=www.viki.com'
    hashed = hmac.new(key.encode('utf-8'), rawtxt.encode('utf-8'), sha1)
    signatura = binascii.hexlify(hashed.digest())
    fullurl = 'https://api.viki.io' + rawtxt+'&sig='+signatura.decode('utf-8')
    return fullurl

def GET_SUBTILES(url, subtitle_completion1, subtitle_completion2):
    if (int(subtitle_completion1)) != 0 or (int(subtitle_completion2)) != 0:
        if (int(subtitle_completion1) == 100 and se == 'true'):
            srtsubs_path1 = 'special://temp/vstream_viki_SubFrench.srt'
            urlreq = SIGN(url, '/subtitles/fr.srt')
            oRequestHandler = cRequestHandler(urlreq)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            data = oRequestHandler.request()

            if isMatrix():
                data = data.encode('latin-1')

            subfile = xbmcvfs.File("special://temp/vstream_viki_SubFrench.srt", "w")
            subfile.write(data)
            subfile.close()

        elif (int(subtitle_completion2) > 0 and se == 'true'):
            srtsubs_path1 = "special://temp/vstream_viki_SubEnglish.srt"
            urlreq = SIGN(url, '/subtitles/en.srt')
            oRequestHandler = cRequestHandler(urlreq)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            data = oRequestHandler.request()

            if isMatrix():
                data = data.encode('latin-1')

            subfile = xbmcvfs.File("special://temp/vstream_viki_SubEnglish.srt", "w")
            subfile.write(data)
            subfile.close()

        return srtsubs_path1
    else:
        return False

def GET_URLS_STREAM(url):
    streamUrlList = []
    validq = []

    urlreq = SIGN(url, '/streams.json')
    oRequestHandler = cRequestHandler(urlreq)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('authority', 'manifest-viki.viki.io')
    oRequestHandler.addHeaderEntry('accept', '*/*')
    oRequestHandler.addHeaderEntry('x-viki-app-ver', '6.0.0')
    oRequestHandler.addHeaderEntry('origin', 'https://www.viki.com')
    oRequestHandler.addHeaderEntry('referer', url)
    jsonrsp = oRequestHandler.request(jsonDecode=True)

    testeurl = ''
    testeq = ''
    for qual in jsonrsp:
        basehttp = 'https'
        if qual in jsonrsp:
            if qual == 'mpd':
                basehttp = 'http'
            streamUrlList.append(jsonrsp[qual][basehttp]['url'])
            validq.append(qual)
            testeurl = jsonrsp[qual][basehttp]['url']
            testeq = qual

    # ajout du teste à enlever + 1 à revoir et
    streamUrlList.append(testeurl)
    validq.append(testeq)
    return validq, streamUrlList


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    dataList = []

    url, thumbnail, sub_pourcent1, sub_pourcent2, stitle = sUrl.split("@")
    sSubPath = GET_SUBTILES(url, sub_pourcent1, sub_pourcent2)
    qualityList2, streamList2 = GET_URLS_STREAM(url)

    dataList.append(sSubPath)

    for item in qualityList2:
        dataList.append(item)

    for item in streamList2:
        dataList.append(item)

    if sSubPath == "special://temp/vstream_viki_SubEnglish.srt":
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Les sous-titres Francais ne sont pas encore terminés ce contenu est donc en sous-titrés Anglais.[/COLOR]')
    elif sSubPath == False:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Aucun sous-titre n\'est disponible pour ce contenu.[/COLOR]')

    oHoster = cHosterGui().checkHoster('viki')
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, dataList, sThumb)

    oGui.setEndOfDirectory()
