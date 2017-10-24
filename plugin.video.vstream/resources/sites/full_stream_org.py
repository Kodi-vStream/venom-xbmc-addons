#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import xbmcgui
import re

SITE_IDENTIFIER = 'full_stream_org'
SITE_NAME = 'Full-Stream'
SITE_DESC = 'Films, Séries & Animés en Streaming HD'

URL_MAIN = 'http://full-stream.nu/'

MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'movie/rating/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'movie/news_read/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'movie/comm_num/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN + 'quality/Haute-qualité/', 'showMovies')

SERIE_SERIES = (URL_MAIN + 'liste-des-series/', 'AlphaSearch')
SERIE_NEWS = (URL_MAIN + 'seriestv/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'seriestv/vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'seriestv/vostfr/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'liste-des-mangas/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'mangas/mangas-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'mangas/mangas-vostfr/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&titleonly=3&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&titleonly=3&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&titleonly=3&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def DecodeURL_old(data):

    oParser = cParser()
    sPattern = '([a-z0-9A-Z]{2})\(\'([^\']*)\'\)'
    aResult = oParser.parse(data, sPattern)

    if not aResult[0]:
        return ''

    f = aResult[1][0][0]
    d = aResult[1][0][1]

    url = ''

    if f == 'f1':
        url = "http://www.flashx.tv/embed-" + d + ".html"

    if f == 'f2':
        url = d

    if f == 'f3':
        url = "https://openload.co/embed/" + d

    if f == 'f4':
        url = "https://vidoza.net/embed-" + d + ".html"

    if f == 'f5':
        url = "http://estream.to/embed-" + d + ".html"

    if f == 'f6':
        url = "http://vidlox.tv/embed-" + d + ".html"

    if f == 'f7':
        url = "http://watchers.to/embed-" + d + ".html"

    if f == 'f8':
        url = "http://mystream.la/embed-" + d + ".html"

    if f == 'AA':
        url = "https://streamango.com/embed/" + d

    if f == 'BB':
        url = "http://easyvid.org/embed-" + d + "-600x360.html"

    return url

def DecodeURL(data):

    oParser = cParser()
    sPattern = '([a-z0-9A-Z]{2})\(\'([^\']*)\'\)'
    aResult = oParser.parse(data, sPattern)

    if not aResult[0]:
        return ''

    f = aResult[1][0][0]
    d = aResult[1][0][1]

    url = ''

    if f == 'aw':
        url = "http://www.flashx.tv/embed-" + d + ".html"

    if f == 'en':
        url = d

    if f == 'ae':
        url = "https://openload.co/embed/" + d

    if f == 'tq':
        url = "https://vidoza.net/embed-" + d + ".html"

    if f == 'bg':
        url = "http://estream.to/embed-" + d + ".html"

    if f == 'jh':
        url = "http://vidlox.tv/embed-" + d + ".html"

    if f == 'yu':
        url = "https://streamango.com/embed/" + d

    if f == 'ru':
        url = "http://easyvid.org/embed-" + d + "-600x360.html"

    return url

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les plus Notés)', 'films_notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus Vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus Commentés)', 'films_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'animes_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes_vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def getPremiumUser():
    sUrl = URL_MAIN
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('login_name', 'vstream')
    oRequestHandler.addParameters('login_password', 'vstream')
    oRequestHandler.addParameters('Submit', '')
    oRequestHandler.addParameters('login', 'submit')
    oRequestHandler.request()

    aHeader = oRequestHandler.getResponseHeader()
    sReponseCookie = aHeader.getheader("Set-Cookie")

    return sReponseCookie

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['HD/HQ',URL_MAIN + 'quality/Haute-qualit%C3%A9/'] )
    liste.append( ['Action',URL_MAIN + 'action/'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Biopic',URL_MAIN + 'biopic/'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'comedie-musicale/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/'] )
    liste.append( ['Famille',URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'historique/'] )
    liste.append( ['Horreur',URL_MAIN + 'horreur/'] )
    liste.append( ['Musical',URL_MAIN + 'musical/'] )
    liste.append( ['Policier',URL_MAIN + 'policier/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Spectacles Sketchs',URL_MAIN + 'spectacles/'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller/'] )
    liste.append( ['Walt Disney',URL_MAIN + 'film/Walt+Disney/'] )
    liste.append( ['Western',URL_MAIN + 'western/'] )

    liste.append( ['En VOSTFR',URL_MAIN + 'xfsearch/VOSTFR/'] )
    liste.append( ['En VFSTF',URL_MAIN + 'xfsearch/VFSTF/'] )
    #liste.append( ['Derniers ajouts',URL_MAIN + 'lastnews/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0, 36) :
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break

        if (i < 10):
            sTitle = chr(48+i)
        else:
            sTitle = chr(65+i-10)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.lower() + '.html')
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]' + sTitle + '[/COLOR]', 'genres.png', oOutputParameterHandler)

    cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def AlphaDisplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    #recuperation de la page
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="(.+?)" class="list-name">&raquo;(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            #sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHostersSerie', sTitle, '', '', 'az.png', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    dlenewssortby = False
    sType = ''

    if sSearch:
        sUrl = sSearch

        #partie en test
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

#    sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
    sPattern = 'fullstreaming".*?img src="(.+?)".+?href="(.+?)">(.+?)<\/a>.*?(?:Version</strong> :([^<]+)<hr/>.*?)*style="font-family:.*?>(.+?)<\/span>'
    #recuperation des tris

    # les plus noter dlenewssortby=rating&dledirection=desc&set_new_sort=dle_sort_cat&set_direction_sort=dle_direction_cat
    # les plus vue dlenewssortby=news_read&dledirection=desc&set_new_sort=dle_sort_cat&set_direction_sort=dle_direction_cat
    #les plus commenter dlenewssortby=comm_num&dledirection=desc&set_new_sort=dle_sort_main&set_direction_sort=dle_direction_main

    if ("rating" in sUrl or "news_read" in sUrl or "comm_num" in sUrl):

        oRequestHandler = cRequestHandler(URL_MAIN + 'movie')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)

        oRequestHandler.addParameters('dledirection', 'desc')
        oRequestHandler.addParameters('set_new_sort', 'dle_sort_cat')
        oRequestHandler.addParameters('set_direction_sort', 'dle_direction_cat')

        if ("rating" in sUrl):
            dlenewssortby = "rating"
        elif ("news_read" in sUrl):
            dlenewssortby = "news_read"
        elif ("comm_num" in sUrl):
            dlenewssortby = "comm_num"

        oRequestHandler.addParameters('dlenewssortby', dlenewssortby)

    else :
        oRequestHandler = cRequestHandler(sUrl)

        if sType:
            if sType == "film":
                oRequestHandler.addParameters('catlist[]', '43')
            if sType == "serie":
                oRequestHandler.addParameters('catlist[]', '2')
            if sType == "anime":
                oRequestHandler.addParameters('catlist[]', '36')

    if oInputParameterHandler.getValue('dlenewssortby'):

        dlenewssortby = oInputParameterHandler.getValue('dlenewssortby')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('dlenewssortby', dlenewssortby)
        oRequestHandler.addParameters('dledirection', 'desc')
        oRequestHandler.addParameters('set_new_sort', 'dle_sort_cat')
        oRequestHandler.addParameters('set_direction_sort', 'dle_direction_cat')

    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
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

            sThumb = str(aEntry[0])#.replace('/IMG/full-stream.php?src=', '')
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
#                sThumb = sThumb.split('&')[0]

            sDesc = aEntry[4]
            sQual = str(aEntry[3]).replace('Haute-qualité', 'HQ').replace(' ', '')
            sTitle = str(aEntry[2])
            sDisplayTitle = sTitle
            if (aEntry[3]):
                sDisplayTitle = sTitle + ' (' + sQual + ')'

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH[0], ''), aEntry[2]) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/seriestv/' in sUrl or 'saison' in sTitle or re.match('.+?saison [0-9]+', sTitle, re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'showHostersSerie', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/mangas/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHostersSerie', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHostersFilm', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oOutputParameterHandler.addParameter('dlenewssortby', dlenewssortby)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)">Suivant.+?<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHostersFilm():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #cConfig().log(sUrl)

    sPattern = '<i class="fa fa-play-circle-o"><\/i>([^<]+)<\/div>|onclick="([^;]+);"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            else:
                sHosterUrl = DecodeURL(str(aEntry[1]))
                oHoster = cHosterGui().checkHoster(sHosterUrl)

                if (oHoster != False):
                    try:
                        oHoster.setHD(sHosterUrl)
                    except: pass
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)

                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHostersSerie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    #pour accelerer traitement
    sPattern = '<div id="fsElementsContainer">(.+?)<div class="series-player">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContentListFile = aResult[1][0]

        
    if "/mangas/" in sUrl:
        sPattern = '<\/i> ([^<>"]+)<\/div>|<a href="([^<>"]+)" title="([^<]+)" target="serieplayer".+?>|onclick="javascript:return false;" href="#" title="([^<>"]+)".*?data-rel="episode([0-9]+)"'
    else:
        sPattern = '<\/i> ([^<>"]+)<\/div>|<a href="([^<>"]+)" title="([^<]+)" target="seriePlayer".+?>|onclick="javascript:return false;" href="#" title="([^<>"]+)".*?data-rel="episode([0-9]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            elif aEntry[1]:
                sHosterUrl = str(aEntry[1])
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sMovieTitle2 = aEntry[2]
                sMovieTitle2 = re.sub(' en (VOSTFR|VF)', '', sMovieTitle2)
                sMovieTitle2 = re.sub(' oav en vostfr', '', sMovieTitle2)
                #sDisplayTitle = cUtil().DecoTitle(sMovieTitle2)

                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle2)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            elif aEntry[3]:
                    sPattern = '<div id="episode' + str(aEntry[4]) + '" class="fullsfeature">(.+?)<\/ul>'
                    aResult3 = oParser.parse(sHtmlContentListFile, sPattern)

                    if (aResult3[0] == True):
                        sPattern = '<a href="([^<>"]+?)" target="seriePlayer" class="fsctab">'
                        aResult2 = oParser.parse(aResult3[1][0], sPattern)

                        if (aResult2[0] == True):
                            for aEntry2 in aResult2[1]:
                                sMovieTitle2 = str(sMovieTitle) + ' ' + str(aEntry[3])
                                #sDisplayTitle = cUtil().DecoTitle(sMovieTitle2)

                                sHosterUrl = aEntry2
                                oHoster = cHosterGui().checkHoster(sHosterUrl)

                                if (oHoster != False):
                                    oHoster.setDisplayName(sMovieTitle2)
                                    oHoster.setFileName(sMovieTitle2)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
