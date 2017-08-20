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
import re

SITE_IDENTIFIER = 'french_stream_com'
SITE_NAME = 'French-stream'
SITE_DESC = 'films en streaming'

URL_MAIN = 'http://french-stream.co/'

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_VF = (URL_MAIN + 'film-en-streaming/vf/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film-en-streaming/vostfr/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'film-en-streaming/hd-vf/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_NEWS = (URL_MAIN + 'serie-tv-en-streaming/', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'serie-tv-en-streaming/', 'showSeries')
SERIE_VFS = (URL_MAIN + 'serie-tv-en-streaming/serie-en-vf-streaming/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'serie-tv-en-streaming/serie-en-vostfr-streaming/', 'showSeries')
SERIE_GENRES = (True, 'showSerieGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'films_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'films_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD-Light)', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'xfsearch/genre-1/action/'] )
    liste.append( ['Animation',URL_MAIN +'xfsearch/genre-1/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'xfsearch/genre-1/arts+Martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'xfsearch/genre-1/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'xfsearch/genre-1/biopic/'] )
    liste.append( ['Comédie',URL_MAIN + 'xfsearch/genre-1/comédie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'xfsearch/genre-1/comédie+dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'xfsearch/genre-1/comédie+musicale/'] )
    liste.append( ['Documentaire',URL_MAIN + 'xfsearch/genre-1/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'xfsearch/genre-1/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'xfsearch/genre-1/epouvante-horreur/'] )
    liste.append( ['Erotique',URL_MAIN + 'xfsearch/genre-1/erotique/'] )
    liste.append( ['Espionnage',URL_MAIN + 'xfsearch/genre-1/espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'xfsearch/genre-1/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'xfsearch/genre-1/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'xfsearch/genre-1/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'xfsearch/genre-1/historique/'] )
    liste.append( ['Musical',URL_MAIN + 'xfsearch/genre-1/musical/'] )
    liste.append( ['Policier',URL_MAIN + 'xfsearch/genre-1/policier/'] )
    liste.append( ['Péplum',URL_MAIN + 'xfsearch/genre-1/peplum/'] )
    liste.append( ['Romance',URL_MAIN + 'xfsearch/genre-1/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'xfsearch/genre-1/science+fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + 'xfsearch/genre-1/spectacle/'] )
    liste.append( ['Thriller',URL_MAIN + 'xfsearch/genre-1/thriller/'] )
    liste.append( ['Walt Disney',URL_MAIN + 'xfsearch/Walt+Disney+Animation/'] )
    liste.append( ['Western',URL_MAIN + 'xfsearch/genre-1/western/'] )
    liste.append( ['Divers',URL_MAIN + 'xfsearch/genre-1/divers/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN +'xfsearch/genre-serie/Action/'] )
    liste.append( ['Animation',URL_MAIN+'xfsearch/genre-serie/Animation/'])
    liste.append( ['Arts Martiaux',URL_MAIN + 'xfsearch/genre-serie/Arts+Martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'xfsearch/genre-serie/Aventure/'])
    liste.append( ['Biopic',URL_MAIN + 'xfsearch/genre-serie/Biopic/'])
    liste.append( ['Comédie',URL_MAIN + 'xfsearch/genre-serie/Comédie/'])
    liste.append( ['Comédie Dramatique',URL_MAIN + 'xfsearch/genre-serie/Comédie+dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'xfsearch/genre-serie/Comédie+musicale/'] )
    liste.append( ['Documentaire',URL_MAIN + 'xfsearch/genre-serie/Documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'xfsearch/genre-serie/Drame/'])
    liste.append( ['Epouvante Horreur',URL_MAIN + 'xfsearch/genre-serie/Epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'xfsearch/genre-serie/Espionnage/'])
    liste.append( ['Famille',URL_MAIN + 'xfsearch/genre-serie/Famille/'])
    liste.append( ['Fantastique',URL_MAIN + 'xfsearch/genre-serie/Fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'xfsearch/genre-serie/Guerre/'])
    liste.append( ['Historique',URL_MAIN + 'xfsearch/genre-serie/Historique/'])
    liste.append( ['Judiciaire',URL_MAIN + 'xfsearch/genre-serie/Judiciaire/'])
    liste.append( ['Médical',URL_MAIN + 'xfsearch/genre-serie/Médical/'])
    liste.append( ['Musical',URL_MAIN + 'xfsearch/genre-serie/Musical/'] )
    liste.append( ['Policier',URL_MAIN + 'xfsearch/genre-serie/Policier/'] )
    liste.append( ['Romance',URL_MAIN + 'xfsearch/genre-serie/Romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'xfsearch/genre-serie/Science+fiction/'] )
    liste.append( ['Soap',URL_MAIN + 'xfsearch/genre-serie/Soap/'] )
    liste.append( ['Sport',URL_MAIN + 'xfsearch/genre-serie/Sport+event/'] )
    liste.append( ['Thriller',URL_MAIN + 'xfsearch/genre-serie/Thriller/'] )
    liste.append( ['Western',URL_MAIN + 'xfsearch/genre-serie/Western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'film-ripz"><a href=".+?">(.+?)</a>.+?film-verz"><a href=".*?">(.+?)</a>.*?href="(.+?)"><img src="(.+?)" alt="(.+?)"/>'

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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH[0], ''), aEntry[4]) == 0:
                    continue

            sQual = str(aEntry[0])
            sLang = str(aEntry[1])
            sUrl2 = str(aEntry[2])
            sThumb = str(aEntry[3]).replace('/img/french-stream.com.php?src=', '')
            sThumb = sThumb.split('&')[0]
            if sThumb.startswith ('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = str(aEntry[4]) + ' (' + sQual + '/' + sLang + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[4]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="short-in nl">.+?"short-poster img-box with-mask" href="(.+?)"><img src="([^<]+)" alt="(.+?)"/>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH[0], ''), aEntry[3]) == 0:
                    continue

            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[1]).replace('/img/french-stream.com.php?src=', '')
            sThumb = sThumb.split('&')[0]
            if sThumb.startswith ('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = str(aEntry[2])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="pnext"><a href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="([^<]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #pensez a faire un cConfig().log(str(aResult)) pour verifier
    #cConfig().log(str(sUrl))
    #cConfig().log(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def serieHostersNew():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<\/i> (VOSTFR|VF) *<\/div>|<a class="fs.+?" href="([^"]+)".+?target="seriePlayer".+?<\/i>\s+([^<>]+?)\s+<\/a>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #pensez a faire un cConfig().log(str(aResult)) pour verifier
    #cConfig().log(str(sUrl))
    #cConfig().log(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            else:
                sTitle = str(aEntry[2]) + ' ' + sMovieTitle

            sHosterUrl = str(aEntry[1])
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    oParser = cParser()

    sPattern = '<\/i> (VOSTFR|VF) *<\/div>|<a class="fs.+?" href="([^"]+)".+?target="seriePlayer".+?<\/i>\s+([^<>]+?)\s+<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            elif aEntry[1]:

                sTitle = str(aEntry[2]) + ' ' + sMovieTitle

                sHosterUrl = aEntry[1]
                sHosterName = ''

                if '9animeonline' in sHosterUrl or 'sibeol.com' in sHosterUrl or 'belike.pw' in sHosterUrl:
                    sHosterName = 'Google'

                if 'cloudvid.co' in sHosterUrl:
                    sHosterName = 'Cloudvid'

                else:
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        sHosterName = str(oHoster.getDisplayName())

                if sHosterName:
                    sDisplayTitle = sTitle + '(' + sHosterName + ')'

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                    oGui.addTV(SITE_IDENTIFIER, 'Showlink', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]indisponible[/COLOR]')

    oGui.setEndOfDirectory()

def Showlink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    if 'sibeol.com' in sUrl:
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'sources:.+?{"type":".+?","label":.+?,"file":"([^"]+)"}'
        aResult = re.findall(sPattern,sHtmlContent)
        if (aResult):
            sUrl = aResult[0]

    if '9animeonline' in sUrl:
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = 'file: "([^"]+)"'
        aResult = re.findall(sPattern,sHtmlContent)
        if (aResult):
            sUrl = aResult[0]

    if 'belike.pw' in sUrl:
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = 'src="([^"]+)"'
        aResult = re.findall(sPattern,sHtmlContent)
        if (aResult):
            sUrl = aResult[0]

    if 'cloudvid.co' in sUrl:
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = 'src="([^"]+)"'
        aResult = re.findall(sPattern,sHtmlContent)
        if (aResult):
            sUrl = aResult[0]

            #lien youtube mais non resolvable, convertion
            if 'docid' in sUrl:
                sPattern = 'docid=([\w-]+)'
                aResult = re.findall(sPattern,sUrl)
                if (aResult):
                    sUrl = 'https://drive.google.com/' + aResult[0]

    oHoster = cHosterGui().checkHoster(sUrl)

    if (oHoster != False):
        sDisplayTitle = cUtil().DecoTitle(sMovieTitle)

        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

    oGui.setEndOfDirectory()
