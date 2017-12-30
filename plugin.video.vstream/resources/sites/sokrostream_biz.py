#-*- coding: utf-8 -*-
# Par chataigne73
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig

import re,urllib,urllib2,xbmc

SITE_IDENTIFIER = 'sokrostream_biz'
SITE_NAME = 'Sokrostream'
SITE_DESC = 'Films & Séries en streaming en vf et Vostfr'

URL_MAIN = 'http://sokrostream.tv/'

MOVIE_NEWS = (URL_MAIN + 'categories/films-streaming', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'categories/films-streaming', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-films-les-plus-vues-2', 'showMovies')
MOVIE_VF = (URL_MAIN + 'langues/french', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'les-films-les-plus-commentes-2', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films-les-mieux-notes-2', 'showMovies')
MOVIE_GENRES = (URL_MAIN , 'showGenres')
MOVIE_ANNEES = (URL_MAIN , 'showMovieYears')
MOVIE_LANG = (URL_MAIN , 'showLang')
MOVIE_QLT = (URL_MAIN , 'showQlt')
MOVIE_PAYS = (URL_MAIN , 'showPays')
MOVIE_PLT = (URL_MAIN , 'showPlt')

SERIE_NEWS = (URL_MAIN + 'categories/series-streaming', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'categories/series-streaming', 'showMovies')
SERIE_VFS = (URL_MAIN + 'series-tv/langues/french', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series-tv/langues/vostfr', 'showMovies')
SERIE_HD = (URL_MAIN + 'series-tv/qualites/hd-720p', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series-tv/', 'showGenres')
SERIE_ANNEES = (URL_MAIN + 'series-tv/', 'showSerieYears')
SERIE_LANG = (URL_MAIN + 'series-tv/', 'showLang')
SERIE_QLT = (URL_MAIN + 'series-tv/', 'showQlt')
SERIE_PAYS = (URL_MAIN + 'series-tv/', 'showPays')
SERIE_PLT = (URL_MAIN + 'series-tv/', 'showPlt')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films (Menu)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries (Menu)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'films_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'films_notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Par Pays)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QLT[1], 'Films (Qualités)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LANG[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LANG[1], 'Films (Langues)', 'lang.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PLT[1], 'Films (Plateformes)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAYS[1], 'Séries (Par Pays)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_QLT[1], 'Séries (Qualités)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LANG[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LANG[1], 'Séries (Langues)', 'lang.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PLT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PLT[1], 'Séries (Plateformes)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Action', sUrl + 'genre/action'] )
    liste.append( ['Animation', sUrl + 'genre/animation'] )
    liste.append( ['Aventure', sUrl + 'genre/aventure'] )
    liste.append( ['Biopic', sUrl + 'genre/biopic'] )
    liste.append( ['Comédie', sUrl + 'genre/comedie'] )
    liste.append( ['Comédie Dramatique', sUrl + 'genre/comedie-dramatique'] )
    liste.append( ['Comédie Musicale', sUrl + 'genre/comedie-musicale'] )
    liste.append( ['Drame', sUrl + 'genre/drame'] )
    liste.append( ['Epouvante Horreur', sUrl + 'genre/epouvante-horreur'] )
    liste.append( ['Espionnage', sUrl + 'genre/espionnage'] )
    liste.append( ['Famille', sUrl + 'genre/famille'] )
    liste.append( ['Fantastique', sUrl + 'genre/fantastique'] )
    liste.append( ['Guerre', sUrl + 'genre/guerre'] )
    liste.append( ['Historique', sUrl + 'genre/historique'] )
    liste.append( ['Judiciaire', sUrl + 'genre/judiciaire'] )
    liste.append( ['Médical', sUrl + 'genre/musical'] )
    liste.append( ['Policier', sUrl + 'genre/policier'] )
    liste.append( ['Péplum', sUrl + 'genre/peplum'] )
    liste.append( ['Romance', sUrl + 'genre/romance'] )
    liste.append( ['Science-Fiction', sUrl + 'genre/science-fiction'] )
    liste.append( ['Thriller', sUrl + 'genre/thriller'] )
    liste.append( ['Western', sUrl + 'genre/western'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showPays():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Américain', sUrl + 'pays/americain'] )
    liste.append( ['Allemand', sUrl + 'pays/allemand'] )
    liste.append( ['Britannique', sUrl + 'pays/britannique'] )
    liste.append( ['Canadien', sUrl + 'pays/canadien'] )
    liste.append( ['Espagnol', sUrl + 'pays/espagnol'] )
    liste.append( ['Français', sUrl + 'pays/francais'] )
    liste.append( ['Italien', sUrl + 'pays/italien'] )
    liste.append( ['Japonais', sUrl + 'pays/japonnais'] )
    liste.append( ['Norvégien', sUrl + 'pays/norvegien'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1913, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annees/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'films_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1940, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series-tv/annees/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'series_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showQlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['DVDRip', sUrl + 'qualites/dvdrip'] )
    liste.append( ['BDRip', sUrl + 'qualites/bdrip'] )
    liste.append( ['HD 720p', sUrl + 'qualites/hd-720p'] )
    liste.append( ['HD 1080p', sUrl + 'qualites/hd-1080p'] )
    liste.append( ['R6', sUrl + 'qualites/r6'] )
    #la suite fonctionne mais n'est pas sur la page d'acceuil du site
    liste.append( ['DVDSCR', sUrl + 'qualites/dvdscr'] )
    liste.append( ['WEB-DL', sUrl + 'qualites/web-dl'] )
    liste.append( ['WEBRIP', sUrl + 'qualites/webrip'] )
    liste.append( ['HDRIP', sUrl + 'qualites/hdrip'] )
    liste.append( ['HDTV', sUrl + 'qualites/hdtv'] )
    liste.append( ['HDCAM', sUrl + 'qualites/hdcam'] )
    liste.append( ['TVRIP', sUrl + 'qualites/tvrip'] )
    liste.append( ['BRRIP', sUrl + 'qualites/brrip'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLang():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['FRENCH', sUrl + 'langues/french'] )
    liste.append( ['VOSTFR', sUrl + 'langues/vostfr'] )
    liste.append( ['VO', sUrl + 'langues/vo'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showPlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['OK.RU', sUrl + 'plateformes/ok-ru'] )
    liste.append( ['FlashX', sUrl + 'plateformes/flashx'] )
    liste.append( ['Netu', sUrl + 'plateformes/netu'] )
    liste.append( ['OpenLoad', sUrl + 'plateformes/openload'] )
    liste.append( ['Youwatch', sUrl + 'plateformes/youwatch'] )
    liste.append( ['Vidup', sUrl + 'plateformes/vidup'] )
    liste.append( ['Uptobox', sUrl + 'plateformes/uptobox'] )
    # les suivants n'apparaissent plus sur le site mais fonctionnent
    liste.append( ['DivxStage', sUrl + 'plateformes/divxstage'] )
    liste.append( ['Exashare', sUrl + 'plateformes/exashare'] )
    liste.append( ['Firedrive', sUrl + 'plateformes/firedrive'] )
    liste.append( ['MovShare', sUrl + 'plateformes/movshare'] )
    liste.append( ['NovaMov', sUrl + 'plateformes/novamov'] )
    liste.append( ['NowVideo', sUrl + 'plateformes/nowvideo'] )
    liste.append( ['Putlocker', sUrl + 'plateformes/putlocker'] )
    liste.append( ['RapidVideo', sUrl + 'plateformes/rapidvideo'] )
    liste.append( ['SockShare', sUrl + 'plateformes/sockshare'] )
    liste.append( ['SpeedVideo', sUrl + 'plateformes/speedvideo'] )
    liste.append( ['UploadHero', sUrl + 'plateformes/uploadhero'] )
    liste.append( ['UptoStream', sUrl + 'plateformes/uptostream'] )
    liste.append( ['VideoMega', sUrl + 'plateformes/videomega'] )
    liste.append( ['VideoWeed', sUrl + 'plateformes/videoweed'] )
    liste.append( ['Vidto', sUrl + 'plateformes/vidto'] )
    liste.append( ['Vimple', sUrl + 'plateformes/vimple'] )
    liste.append( ['Vodlocker', sUrl + 'plateformes/vodlocker'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch
        sUrl = re.sub( r".*\/(.+)$", r"\1", sUrl )
        sUrl = urllib.quote( sUrl.rstrip(), safe='' )
        sUrl = URL_SEARCH[0] + sUrl

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent2 = oRequestHandler.request()

    oParser = cParser()

    sHtmlContent = oParser.abParse(sHtmlContent2,'<section class="box"','<div class="pagination-fix"')
    sPattern = 'data-v-.+?<a href="([^"]+)".+?<img src="(.+?)" alt="(.+?)" class='

    aResult = oParser.parse(sHtmlContent, sPattern)

    datas = None
    if sSearch:
        datas = __getDataFromHtmlContent( sHtmlContent2 )
        datas = [[ __genUrl(x,'series'), x['poster'], x['name'].encode('utf-8')]
                    for x in datas['series']]
        if len( datas ) > 0:
            aResult = list( aResult ) # aResult: tuple -> list
            aResult[0] = True
            aResult[1] += datas

    #cConfig().log( repr(aResult) )
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sUrl2 = URL_MAIN[:-1] + aEntry[0]

            sThumb = str(aEntry[1])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2 )
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if ('/series/' in sUrl2):
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle,'', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent2)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="pagination-link is-current".+?<a href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN[:-1]+aResult[1][0]

    return False

def __getDataFromHtmlContent( sHtmlContent ):
    """ extrait les datas du code source html au format json """

    import json
    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent,'window.__NUXT__=',';</script>',16)
    datas = json.loads( sHtmlContent )
    datas = datas["data"][0]
    return datas

def __genUrl( e, t ):
    """ Génere une url depuis l'element et le type passé en paramètre.
        e: element ( dict )
        t: type    ( string )

        > /[type]/[name]-[id].html
        type: 'films' ou 'series'
        name: e['name'] en minuscule et formaté
        id  : e['customID']
    """
    url = e['name']

    # remplace les caractères et les espaces pour former une url valide ...
    # caractères à surveiller: #!&:,-,%'
    # ( voir d'autres que je n'ai pas trouvé ou oublié )
    url = re.sub(ur"[ëèéê]", 'e', url)
    url = re.sub(ur"[âäà]", 'a', url)
    url = re.sub(ur"[ùûü]", 'u', url)
    url = re.sub(ur"[öô]", 'o', url)
    url = re.sub(ur"[ïî]", 'i', url)
    url = re.sub(ur"ç", 'c', url)
    url = re.sub(r"[#!&:,]", '', url)
    url = re.sub(r"\s+$", '', url)
    url = re.sub(r"[\'\/%]|\s+", '-', url)

    url = '/'+ t + '/' + url.lower() + '-' + str(e['customID']) + '.html'
    #cConfig().log( url )
    return url

def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent,'</section><!----><section class="box"','<section class="box box-fix')

    sPattern = 'data-v-.+?<a href="([^"]+)".+?>(S.+?)</button>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' ' + aEntry[1]
            sUrl = URL_MAIN[:-1] + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent,'</section><!----><section class="box"','<section class="box box-fix')

    sPattern = '<a href="([^"]+)".+?>(E.+?)</button>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #cConfig().log(aResult)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' ' + aEntry[1]
            sUrl = URL_MAIN[:-1] + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    import json
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent,'window.__NUXT__=',';</script>',16)

    page = None
    if '-episode-' in sUrl:
        page = json.loads(sHtmlContent)
        page = page["data"][0]["data"]["episode"][0]["videos"]
        #aResult = [x["link"] for x in page]
    else:
        page = json.loads(sHtmlContent)
        page = page["data"][0]["data"]["videos"]
        #aResult = [x["link"] for x in page]

    #cConfig().log(str(page))

    if (page):
        total = len(page)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in page:

            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = aEntry["link"]
            #sDisplayTitle = cUtil().DecoTitle(sMovieTitle + ' (' + aEntry["language"] + ')' )
            sDisplayTitle = "%s (%s)" % (sMovieTitle, str(aEntry["language"]))

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
