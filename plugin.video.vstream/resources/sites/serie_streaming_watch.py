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

import re,urllib2,urllib,xbmc

SITE_IDENTIFIER = 'serie_streaming_watch'
SITE_NAME = 'Serie-Streaming-Watch'
SITE_DESC = 'Séries & Animés en Streaming'

#meme fichiers que http://dpstreaming.watch
URL_MAIN = 'http://serie-streaming.watch/'

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_GENRES = (True, 'showGenres')

ANIM_ENFANTS = (URL_MAIN + 'category/series/dessin-anime/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(URL_SEARCH[0] + sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'category/series/action/'] )
    liste.append( ['Animation',URL_MAIN + 'category/series/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'category/series/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'category/series/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'category/series/biopic/'] )
    liste.append( ['Classique',URL_MAIN + 'category/series/classique/'] )
    liste.append( ['Comédie',URL_MAIN + 'category/series/comedie/'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'category/series/comedie-dramatique/'] )
    liste.append( ['Comédie musicale',URL_MAIN + 'category/series/comedie-musicale/'] )
    liste.append( ['Dessin animés',URL_MAIN + 'category/series/dessin-anime/'] )
    liste.append( ['Divers',URL_MAIN + 'category/series/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + 'category/series/documentaire/'] )
    liste.append( ['Drama',URL_MAIN + 'category/series/drama/'] )
    liste.append( ['Drame',URL_MAIN + 'category/series/drame/'] )
    liste.append( ['Epouvante-Horreur',URL_MAIN + 'category/series/epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'category/series/espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'category/series/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'category/series/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'category/series/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'category/series/historique/'] )
    liste.append( ['Judiciaire',URL_MAIN + 'category/series/judiciaire/'] )
    liste.append( ['Médical',URL_MAIN + 'category/series/medical/'] )
    liste.append( ['Musical',URL_MAIN + 'category/series/musical/'] )
    liste.append( ['Péplum',URL_MAIN + 'category/series/peplum/'] )
    liste.append( ['Policier',URL_MAIN + 'category/series/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'category/series/romance/'] )
    liste.append( ['Science-fiction',URL_MAIN + 'category/series/science-fiction/'] )
    liste.append( ['Séries',URL_MAIN + 'category/series/'] )
    liste.append( ['Soap',URL_MAIN + 'category/series/soap/'] )
    liste.append( ['Thriller',URL_MAIN + 'category/series/thriller/'] )
    liste.append( ['Webséries',URL_MAIN + 'category/series/webserie/'] )
    liste.append( ['Western',URL_MAIN + 'category/series/western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch
        sUrl = sUrl.replace('%20','+')
        sPattern = '<div class="fixwidth">\s*<a href="([^"]+)">.+?<img class="izimg" src="([^"]+)".+?title="([^"]+)"'

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        if 'category' in sUrl:
            sPattern = '<div class="fixwidth">\s*<a href="([^"]+)">.+?<img class="izimg" src="([^"]+)".+?title="([^"]+)"'
        else:
            sPattern = '<div class="video">.+?<a href="([^"]+)">.+?<img class="izimg" src="([^"]+)".+?title="([^"]+)"'

    oRequestHandler = cRequestHandler(sUrl)
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

            sTitle = str(aEntry[2])
            sTitle = sTitle.replace(' Streaming','')
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            sThumbnail = str(aEntry[1])
            if not sThumbnail.startswith('http'):
                sThumbnail = URL_MAIN + sThumbnail

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'ShowEpisode', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="son bg"><a href="([^"]+)" *>Suivante'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def ShowEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^"]+)"><span>([^<>]+)<\/span><\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' episode ' + str(aEntry[1])
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
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

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    oParser = cParser()
    sPattern = '<span class="lg">(.+?)<\/span>|<span class="myLecteur">Lecteur (?:<b>)*([a-z]+)(?:<\/b>)* *:<\/span> <a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', '[COLOR red]'+ aEntry[0] +'[/COLOR]', 'host.png', oOutputParameterHandler)
            else:

                sDisplayTitle =  cUtil().DecoTitle(sMovieTitle + ' [' + aEntry[1] + ']')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[2])
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
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
            cGui().showInfo("Erreur", 'Lien encore protege' , 5)
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
