#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,xbmcgui,urllib,unicodedata

SITE_IDENTIFIER = 'streamay_bz'
SITE_NAME = 'Streamay'
SITE_DESC = 'Films, Séries & Mangas en streaming'
URL_MAIN = 'http://streamay.ws/'

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
    dialog = xbmcgui.Dialog()
    numboard = dialog.numeric(0, 'Entrer une année ex: 2005', sDefaultNum)
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

    sHtmlContent = oParser.abParse(sHtmlContent,sStart,sEnd)

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
    liste.append( ['Algérien',URL_MAIN + 'films/origine/algerien'] )
    liste.append( ['Allemand',URL_MAIN + 'films/origine/allemand'] )
    liste.append( ['Américain',URL_MAIN + 'films/origine/americain'] )
    liste.append( ['Belge',URL_MAIN + 'films/origine/belge'] )
    liste.append( ['Britanique',URL_MAIN + 'films/origine/britannique'] )
    liste.append( ['Canadien',URL_MAIN + 'films/origine/canadien'] )
    liste.append( ['Espagnol',URL_MAIN + 'films/origine/espagnol'] )
    liste.append( ['Francais',URL_MAIN + 'films/origine/francais'] )
    liste.append( ['Italien',URL_MAIN + 'films/origine/italien'] )
    liste.append( ['Japonnais',URL_MAIN + 'films/origine/japonnais'] )
    liste.append( ['Marocains',URL_MAIN + 'films/origine/marocains'] )
    liste.append( ['Néerlandais',URL_MAIN + 'films/origine/neerlandais'] )
    liste.append( ['Norvegien',URL_MAIN + 'films/origine/norvegien'] )
    liste.append( ['Russe',URL_MAIN + 'films/origine/russe'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showResultSearch(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    post_data = {'k' : sSearch}
    data = urllib.urlencode(post_data)

    oRequest = cRequestHandler(URL_MAIN + 'search')
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent',UA)
    oRequest.addHeaderEntry('Referer',URL_MAIN)
    #oRequest.addHeaderEntry('X-CSRF-TOKEN','ZEkIadnmogIOiPFzUk')
    oRequest.addParametersLine(data)

    sHtmlContent = oRequest.request()

    sHtmlContent = unicode(sHtmlContent,'utf-8')
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")
    sHtmlContent = sHtmlContent.encode("utf-8")
    sHtmlContent = sHtmlContent.replace("\n","")
    sHtmlContent = re.sub('"img":"([^"]+)","synopsis":"([^"]+)"','"synopsis":"\g<2>","img":"\g<1>"',sHtmlContent) #pattern en ordre img et syn inversé parfois

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = '\"id\":.+?,\"title\":\"([^\"]+)\".+?\"qualite\":\"([^\"]+)\",\"img\":\"([^\"]+)\",.+?\"url\":\"([^\"]+)\"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[0]
            sTitle = cUtil().removeHtmlTags(sTitle)
            sSyn = aEntry[1]
            sUrl = aEntry[3]
            sThumb = URL_MAIN + 'cdn/img/' + aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            elif 'mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showAnime', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

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

    sPattern = '<a href="([^"]+)" class="mv">.+?(?:<span class="qualitos">([^><]+)<\/span>)*<img src="([^"]+)".+?class="title"><span>([^<>]+)<\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[3].decode("utf-8")
            sTitle = cUtil().unescape(sTitle).encode("utf-8")
            if aEntry[1]:
                sTitle = sTitle + ' [' + aEntry[1] + ']'

            sUrl = aEntry[0]
            sThumb = aEntry[2]
            #sSyn = aEntry[3].decode("utf-8")
            #sSyn = cUtil().unescape(sSyn).encode("utf-8")
            sSyn = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            elif '/mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showAnime', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

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
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<a class="head an choseSaison">(.+?)<\/a>|<a class="item" href="([^"]+)">.+?<span class="epitoto">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
               sSaison = aEntry[0]
               oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sSaison + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                sTitle = sMovieTitle + aEntry[2].replace('Regarder','')
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" data-streamer="([^"]+)" data-v-on=".+?" data-id="([^"]+)"> <i style=".+?"></i> <span>(.+?)</span></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if 'stfr' in aEntry[1]:
                sLang = 'Vostfr'
            else:
                sLang = 'Vf'

            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            sHost = aEntry[3]
            #sTitle = '[COLOR coral]' + sLang + '[/COLOR]' + ' ' + sDisplayTitle + ' ' + '[COLOR coral]>> ' + sHost + '[/COLOR]'
            sTitle = '%s [%s] [COLOR coral]%s[/COLOR]' %(sDisplayTitle, sLang, sHost)
            if 'serie' in sUrl:
                sUrlv = URL_MAIN + 'streamerSerie/' + aEntry[2] + '/' + aEntry[1]
            else:
                sUrlv = URL_MAIN + 'streamer/' + aEntry[2] + '/' + aEntry[1]

            aTitle = sMovieTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlv)
            oOutputParameterHandler.addParameter('sMovieTitle', aTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'GetLink', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def GetLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'code":"([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showAnime():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="chooseEpisodeManga" data-id="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sUrl2 = URL_MAIN + 'read/mepisodes/' + aResult[1][0]
        oRequestHandler = cRequestHandler(sUrl2)
        sHtmlContent = oRequestHandler.request()
        sPattern = '{"episodeNumber":"([^"]+)","id":"([^"]+)","manga_id":"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])
            dialog = cConfig().createDialog(SITE_NAME)
            for aEntry in aResult[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                   break

                sTitle = sMovieTitle + 'episode' + ' ' + aEntry[0]
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                sUrl3 = URL_MAIN + 'read/mepisode/' + aEntry[2] + '/' + aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl3)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oOutputParameterHandler.addParameter('sMangaid', aEntry[2])
                oOutputParameterHandler.addParameter('sEp', aEntry[0])
                oGui.addMovie(SITE_IDENTIFIER, 'showAnimeHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

            cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showAnimeHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sMangaid = oInputParameterHandler.getValue('sMangaid')
    sEp = oInputParameterHandler.getValue('sEp')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '{.+?"views":".+?",|"([^"]+)":"([^"]+)"|,"published":".+?".+}'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                if 'stfr' in aEntry[0]:
                    sLang = '[' + 'Vostfr' + ']'
                else:
                    sLang = '[' + 'Vf' + ']'

                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                sHost = aEntry[0].replace('_vostfr','')
                sTitle = '[COLOR coral]' + sLang + '[/COLOR]' + ' ' + sDisplayTitle + ' ' + '[COLOR coral]>> ' + sHost + '[/COLOR]'
                sUrl = URL_MAIN + 'streamerMEpisode/' + sEp + '/' + sMangaid + '/' + aEntry[0]
                aTitle = sMovieTitle

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', aTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMovie(SITE_IDENTIFIER, 'GetLink', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
