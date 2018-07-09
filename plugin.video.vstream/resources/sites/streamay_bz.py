#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, dialog

import urllib, unicodedata

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'streamay_bz'
SITE_NAME = 'Streamay'
SITE_DESC = 'Films, Séries & Mangas en streaming'
URL_MAIN = 'http://streamay.la/'

MOVIE_NEWS = (URL_MAIN + 'films/recents', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films?p=populaire', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films', 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'films?y=', 'showMovies')
MOVIE_PAYS = (True, 'showPays')

SERIE_NEWS = (URL_MAIN + 'series', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series/alphabet', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series', 'showGenres')
SERIE_ANNEES = (URL_MAIN + 'series?y=', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'mangas', 'showMovies')
ANIM_GENRES = (URL_MAIN + 'mangas', 'showGenres')
ANIM_ANNEES = (URL_MAIN + 'mangas/annee/', 'showMovies')

URL_SEARCH = ('', 'showResultSearch')
URL_SEARCH_MOVIES = ('', 'showResultSearch')
URL_SEARCH_SERIES = ('', 'showResultSearch')
FUNCTION_SEARCH = 'showResultSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Par Pays)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par Années)', 'animes_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showResultSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def showNumBoard(sDefaultNum=''):
    dialogs = dialog()
    numboard = dialogs.numeric(0, 'Entrer une année ex: 2005', sDefaultNum)
    if numboard != None:
       return numboard
    return False

def selectMovieAnnees():
    oGui = cGui()
    newNum = showNumBoard()
    sUrl = MOVIE_ANNEES[0] + newNum
    return sUrl

def selectSerieAnnees():
    oGui = cGui()
    newNum = showNumBoard()
    sUrl = SERIE_ANNEES[0] + newNum
    return sUrl

def selectAnimAnnees():
    oGui = cGui()
    newNum = showNumBoard()
    sUrl = ANIM_ANNEES[0] + newNum
    return sUrl

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'film' in sUrl:
        reqURL = MOVIE_GENRES[0]
        sStart = '<div class="dropiz films_drop">'
        sEnd = '<h4 class="hido">Par Année</h4>'
    elif 'serie' in sUrl:
        reqURL = SERIE_GENRES[0]
        sStart = '<div class="dropiz series_drop">'
        sEnd = '<div class="dropiz emissions_drop">'
    else:
        reqURL = ANIM_GENRES[0]
        sStart = '<div class="dropiz mangas_drop">'
        sEnd = '<div class="fixed_header_menu"'

    oParser = cParser()

    oRequestHandler = cRequestHandler(reqURL)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li><a href="([^"]+)">(.+?)<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            sTitle = cUtil().unescape(sTitle).encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showPays():
    oGui = cGui()

    liste = []
    liste.append( ['Algérien', URL_MAIN + 'films/origine/algerien'] )
    liste.append( ['Allemand', URL_MAIN + 'films/origine/allemand'] )
    liste.append( ['Américain', URL_MAIN + 'films/origine/americain'] )
    liste.append( ['Belge', URL_MAIN + 'films/origine/belge'] )
    liste.append( ['Britanique', URL_MAIN + 'films/origine/britannique'] )
    liste.append( ['Canadien', URL_MAIN + 'films/origine/canadien'] )
    liste.append( ['Espagnol', URL_MAIN + 'films/origine/espagnol'] )
    liste.append( ['Francais', URL_MAIN + 'films/origine/francais'] )
    liste.append( ['Italien', URL_MAIN + 'films/origine/italien'] )
    liste.append( ['Japonais', URL_MAIN + 'films/origine/japonais'] )
    liste.append( ['Marocain', URL_MAIN + 'films/origine/marocain'] )
    liste.append( ['Néerlandais', URL_MAIN + 'films/origine/neerlandais'] )
    liste.append( ['Norvégien', URL_MAIN + 'films/origine/norvegien'] )
    liste.append( ['Russe', URL_MAIN + 'films/origine/russe'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showResultSearch(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
    post_data = {'k' : sSearch}
    data = urllib.urlencode(post_data)

    oRequest = cRequestHandler(URL_MAIN + 'search')
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    #oRequest.addHeaderEntry('X-CSRF-TOKEN', 'ZEkIadnmogIOiPFzUk')
    oRequest.addParametersLine(data)

    sHtmlContent = oRequest.request()

    # sHtmlContent = unicode(sHtmlContent,'utf-8')
    # sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")
    # sHtmlContent = sHtmlContent.encode("utf-8")
    # sHtmlContent = sHtmlContent.replace("\n", "")
    # sHtmlContent = re.sub('"img":"([^"]+)","synopsis":"([^"]+)"','"synopsis":"\g<2>","img":"\g<1>"', sHtmlContent) #pattern en ordre img et syn inversé parfois

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    # sPattern = '\"id\":.+?,\"title\":\"([^\"]+)\".+?\"qualite\":\"([^\"]+)\",\"img\":\"([^\"]+)\",.+?\"url\":\"([^\"]+)\"'
    # aResult = oParser.parse(sHtmlContent, sPattern)

    #[{"result":{"id":"1082","title":"<strong>Westworld<\/strong>","originalTitle":"Westworld","codeAllo":"16930","slug":"westworld","dateStart":"2016-10-02","format":"0","synopsis":"Un parc d'attractions peupl\u00e9 de robots propose aux visiteurs de se replonger dans plusieurs \u00e9poques. Lanc\u00e9s dans l'ouest sauvage, deux amis se retrouvent plong\u00e9s en plein cauchemar quand l'un des andro\u00efdes se d\u00e9traque et les prend en chasse...","img":"2823_westworld_qONX.jpg","trailer":null,"banner":"7241_westworld_rRTq.jpg","status":"En production","published":true,"views":"255128","votes":"42","rating":"190","urating":"0.000000","stoun":null,"updato":"2018-05-09 10:58:59","created_at":"2016-10-03 21:31:35","updated_at":"2018-05-28 03:04:43","url":"http:\/\/streamay.la\/series\/westworld","count_seasons":[{"serie_id":"1082","count":"2"}],"count_episodes":[{"serie_id":"1082","count":"13"}]},"type":"S\u00e9rie"}]
    #[{"result":{"id":"544","title":"Avatar","originalTitle":null,"codeAllo":null,"story":"Malgr\u00e9 sa paralysie, Jake Sully, un ancien marine immobilis\u00e9 dans un fauteuil roulant, est rest\u00e9 un combattant au plus profond de son \u00eatre. Il est recrut\u00e9 pour se rendre \u00e0 des ann\u00e9es-lumi\u00e8re de la Terre, sur Pandora, o\u00f9 de puissants groupes industriels exploitent un minerai rarissime destin\u00e9 \u00e0 r\u00e9soudre la crise \u00e9nerg\u00e9tique sur Terre. Parce que l'atmosph\u00e8re de Pandora est toxique pour les humains, ceux-ci ont cr\u00e9\u00e9 le Programme Avatar, qui permet \u00e0 des \" pilotes \" humains de lier leur esprit \u00e0 un avatar, un corps biologique command\u00e9 \u00e0 distance, capable de survivre dans cette atmosph\u00e8re l\u00e9tale. Ces avatars sont des hybrides cr\u00e9\u00e9s g\u00e9n\u00e9tiquement en croisant l'ADN humain avec celui des Na'vi, les autochtones de Pandora.Sous sa forme d'avatar, Jake peut de nouveau marcher. On lui confie une mission d'infiltration aupr\u00e8s des Na'vi, devenus un obstacle trop cons\u00e9quent \u00e0 l'exploitation du pr\u00e9cieux minerai. Mais tout va changer lorsque Neytiri, une tr\u00e8s belle Na'vi, sauve la vie de Jake...","slug":"avatarvf","anneeProduction":"2009","dateSortie":null,"qualite":"DVDRIP","img":"3474_avatar_KZU5.jpg","langue":"Fran\u00e7ais (VF)","trailer":null,"duree":"10140","views":"353048","votes":"703","rating":"2920","urating":"0.000000","stoun":"","manual":"0","published":true,"boxoffice":false,"created_at":"2013-01-23 06:21:54","updated_at":"2018-05-28 02:13:02","mafia":"aventure,science-fiction,americain","vv":5,"genre":"Aventure","url":"http:\/\/streamay.la\/544-avatarvf.html","genres":[{"id":"16","name":"Aventure","slug":"aventure","pivot":{"movies_id":"544","genres_id":"16"}},{"id":"9","name":"Science Fiction","slug":"science-fiction","pivot":{"movies_id":"544","genres_id":"9"}}]},"type":"Film"},{"result":{"id":"420","title":"<strong>Avatar<\/strong> : La L\u00e9gende de Korra","originalTitle":"","origine":"","acteurs":"","format":"25","studios":"","dateSortie":"","year":"2012","img":"4406_avatar-la-legende-de-korra_qEEz.jpg","synopsis":"70 ans apr\u00e8s les \u00e9v\u00e9nements d'Avatar, le Dernier Ma\u00eetre de l'Air,\nvoici les aventures du nouvel \u00e9lu, une adolescente passionn\u00e9e,\ncourageuse et intr\u00e9pide de la Tribu d'eau du Sud nomm\u00e9e Korra. \nMa\u00eetrisant 3 des 4 \u00e9l\u00e9ments, c'est sous la tutelle du fils d'Aang,\nTenzin, que Korra commence sa formation pour ma\u00eetriser le dernier \u00e9l\u00e9ment : l'air.\nMais le parcours de notre jeune prodige sera sem\u00e9 d'emb\u00fbches, le danger gronde...","stoun":null,"slug":"avatar-la-legende-de-korra","published":true,"views":"10813","votes":"0","rating":"0","created_at":"2016-04-19 03:18:47","updated_at":"2018-05-28 04:00:07","url":"http:\/\/streamay.la\/mangas\/avatar-la-legende-de-korra"},"type":"Manga"}]
 
    
    content = json.loads(sHtmlContent)    

    sType = "Film"
    

    if not content:
        oGui.addText(SITE_IDENTIFIER)

    if content:
        total = len(content)
        progress_ = progress().VScreate(SITE_NAME)
        for x in content:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = cUtil().removeHtmlTags(x['result']['title']).encode('UTF-8')
            sUrl = x['result']['url']
            sThumb = URL_MAIN + 'cdn/img/' + x['result']['img']
            sDesc = ''
            sType = x['type'].encode('UTF-8')

            try:
                sMovieTitle = '%s [%s]' % (sTitle, x['result']['qualite'])
            except:
                sMovieTitle = sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if 'Série' in sType:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'Manga' in sType:
                oGui.addTV(SITE_IDENTIFIER, 'showAnime', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sMovieTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()

    if 'films?y=' in sUrl:
        sUrl = selectMovieAnnees()
    elif 'series?y=' in sUrl:
        sUrl = selectSerieAnnees()
    elif 'mangas/annee/' in sUrl:
        sUrl = selectAnimAnnees()
    else:
        sUrl = sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = '<a href="([^"]+)" class="mv">.+?(?:<span class="qualitos">([^><]+)<\/span>)*<img src="([^"]+)".+?class="title"><span>([^<>]+)<\/span>.+?<span class="tt">Synopsis: </span>([^<>]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[3].decode("utf-8")
            sTitle = cUtil().unescape(sTitle).encode("utf-8")
            if aEntry[1]:
                sTitle = sTitle + ' [' + aEntry[1] + ']'

            sUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = aEntry[4].decode("utf-8")
            sDesc = cUtil().unescape(sDesc).encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showAnime', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^"]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<a class="head an choseSaison">(.+?)<\/a>|<a class="item" href="([^"]+)">.+?<span class="epitoto">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
               sSaison = aEntry[0]
               oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sSaison + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                sTitle = sMovieTitle + aEntry[2].replace('Regarder', '')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    try:#récupération des Synopsis
        sDesc = ''
        if '/series/' in sUrl:
            sPattern = '<div class="synopsis">(.+?)<\/div>'
        else:
            sPattern = '<div class="synopsis" itemprop="description">(.+?)<\/div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].decode("utf-8")
            sDesc = cUtil().unescape(sDesc).encode("utf-8")
    except:
        pass

    sPattern = '<a href="([^"]+)" data-streamer="([^"]+)" data-v-on=".+?" data-id="([^"]+)"> <i style=".+?"></i> <span>(.+?)</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'stfr' in aEntry[1]:
                sLang = 'VOSTFR'
            else:
                sLang = 'VF'

            sHost = aEntry[3]
            sTitle = '%s (%s) [COLOR coral]%s[/COLOR]' %(sMovieTitle, sLang, sHost)
            if 'serie' in sUrl:
                sUrlv = URL_MAIN + 'streamerSerie/' + aEntry[2] + '/' + aEntry[1]
            else:
                sUrlv = URL_MAIN + 'streamer/' + aEntry[2] + '/' + aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlv)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'GetLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def GetLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'code":"([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showAnime():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="chooseEpisodeManga" data-id="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl2 = URL_MAIN + 'read/mepisodes/' + aResult[1][0]
        oRequestHandler = cRequestHandler(sUrl2)
        sHtmlContent = oRequestHandler.request()
        sPattern = '{"episodeNumber":"([^"]+)","id":"([^"]+)","manga_id":"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                   break

                sTitle = sMovieTitle + 'episode' + ' ' + aEntry[0]
                sUrl3 = URL_MAIN + 'read/mepisode/' + aEntry[2] + '/' + aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl3)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMangaid', aEntry[2])
                oOutputParameterHandler.addParameter('sEp', aEntry[0])
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addMovie(SITE_IDENTIFIER, 'showAnimeHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showAnimeHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMangaid = oInputParameterHandler.getValue('sMangaid')
    sEp = oInputParameterHandler.getValue('sEp')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '{.+?"views":".+?",|"([^"]+)":"([^"]+)"|,"published":".+?".+}'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                if 'stfr' in aEntry[0]:
                    sLang = 'VOSTFR'
                else:
                    sLang = 'VF'

                sHost = aEntry[0].replace('_vostfr', '').capitalize()
                sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)
                sUrl = URL_MAIN + 'streamerMEpisode/' + sEp + '/' + sMangaid + '/' + aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'GetLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
