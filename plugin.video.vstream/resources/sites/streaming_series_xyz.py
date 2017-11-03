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

import urllib,urllib2,xbmc

SITE_IDENTIFIER = 'streaming_series_xyz'
SITE_NAME = 'Streaming-Series.cx'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = 'http://dpstreaming.cx/'

SERIE_SERIES = (URL_MAIN, 'showMovies')
SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (URL_MAIN + 'serie-category/series/dessin-anime/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def ProtectstreamBypass(url):

    #lien commencant par VID_
    Codedurl = url
    oRequestHandler = cRequestHandler(Codedurl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        cGui().showInfo("Patientez", 'Decodage en cours' , 5)
        xbmc.sleep(5000)

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        headers = {'User-Agent': UA ,
                   'Host' : 'www.protect-stream.com',
                   'Referer': Codedurl ,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Encoding' : 'gzip, deflate',
                   #'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Content-Type': 'application/x-www-form-urlencoded'}

        postdata = urllib.urlencode( { 'k': aResult[1][0] } )

        req = urllib2.Request('http://www.protect-stream.com/secur2.php',postdata,headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.read()
            print e.reason

        data = response.read()
        response.close()

        #Test de fonctionnement
        aResult = oParser.parse(data, sPattern)
        if aResult[0]:
            cGui().showInfo("Erreur", 'Lien encore protegé' , 5)
            return ''

        #recherche du lien embed
        sPattern = '<iframe src=["\']([^<>"\']+?)["\']'
        aResult = oParser.parse(data, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        #recherche d'un lien redirigee
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(data, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

    return ''

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'serie-category/series/action/'] )
    liste.append( ['Animation',URL_MAIN + 'serie-category/series/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'serie-category/series/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'serie-category/series/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'serie-category/series/biopic/'] )
    liste.append( ['Classique',URL_MAIN + 'serie-category/series/classique/'] )
    liste.append( ['Comédie',URL_MAIN + 'serie-category/series/comedie/'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'serie-category/series/comedie-dramatique/'] )
    liste.append( ['Comédie musicale',URL_MAIN + 'serie-category/series/comedie-musicale/'] )
    liste.append( ['Dessin animés',URL_MAIN + 'serie-category/series/dessin-anime/'] )
    liste.append( ['Divers',URL_MAIN + 'serie-category/series/divers/'] )
    liste.append( ['Documentaires',URL_MAIN + 'serie-category/series/documentaire/'] )
    liste.append( ['Drama',URL_MAIN + 'serie-category/series/drama/'] )
    liste.append( ['Drame',URL_MAIN + 'serie-category/series/drame/'] )
    liste.append( ['Epouvante-Horreur',URL_MAIN + 'serie-category/series/epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'serie-category/series/espionnage/'] )
    liste.append( ['Expérimental',URL_MAIN + 'serie-category/series/experimental/'] )
    liste.append( ['Famille',URL_MAIN + 'serie-category/series/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'serie-category/series/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'serie-category/series/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'serie-category/series/historique/'] )
    liste.append( ['Judiciaire',URL_MAIN + 'serie-category/series/judiciaire/'] )
    liste.append( ['Médical',URL_MAIN + 'serie-category/series/medical/'] )
    liste.append( ['Musical',URL_MAIN + 'serie-category/series/musical/'] )
    liste.append( ['Péplum',URL_MAIN + 'serie-category/series/peplum/'] )
    liste.append( ['Policier',URL_MAIN + 'serie-category/series/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'serie-category/series/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'serie-category/series/science-fiction/'] )
    liste.append( ['soap',URL_MAIN + 'serie-category/series/soap/'] )
    liste.append( ['Thriller',URL_MAIN + 'serie-category/series/thriller/'] )
    liste.append( ['Websérie',URL_MAIN + 'serie-category/series/webserie/'] )
    liste.append( ['Western',URL_MAIN + 'serie-category/series/western/'] )

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
        sUrl = sUrl.replace('%20','+')

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<div class="moviefilm".+?<a href="(.+?)".+?<img src="([^<>"]+)" alt="(.+?)"'

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

            sTitle = aEntry[2].replace(' Streaming','')

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', aEntry[1])

            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', aEntry[1], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">»</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^<]+)"><span>(.+?)</span></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' episode ' + aEntry[1]

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
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
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')

    sPattern = '<td class="lg" width=".+?">(?:(VF|VOSTFR|VO))<\/td>.+?<td class="lg" width=".+?">(.+?)</td>.+?<a href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break


            sDisplayTitle = ('[%s] %s [%s]') % (aEntry[0],sMovieTitle,aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sHosterUrl = ProtectstreamBypass(sUrl)

    oHoster = cHosterGui().checkHoster(sHosterUrl)

    if (oHoster != False):

        sMovieTitle = cUtil().DecoTitle(sMovieTitle)

        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
