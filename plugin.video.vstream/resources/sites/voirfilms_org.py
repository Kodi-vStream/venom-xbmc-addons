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
import urllib2,urllib,re

SITE_IDENTIFIER = 'voirfilms_org'
SITE_NAME = 'VoirFilms'
SITE_DESC = 'Films, Séries & Animés en Streaming'

URL_MAIN = 'http://www.voirfilms.ws/'

MOVIE_MOVIE = (URL_MAIN + 'alphabet', 'showAlpha')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')

SERIE_SERIES = (URL_MAIN + 'series/alphabet', 'showAlpha')
SERIE_NEWS = (URL_MAIN + 'series/page-1', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series', 'showGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')

ANIM_ANIMS = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Par ordre Alphabétique)', 'films_az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Par ordre Alphabétique)', 'series_az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Par ordre Alphabétique)', 'animes_az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0,27) :
        cConfig().updateDialog(dialog, 36)

        if (i > 0):
            sTitle = chr(64+i)
        else:
            sTitle = '09'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.upper())
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'series' in sUrl:
        code = URL_MAIN + 'series/'
    else:
        code = URL_MAIN

    liste = []
    liste.append( ['Action',code + 'action_1'] )
    liste.append( ['Animation',code + 'animation_1'] )
    liste.append( ['Arts Martiaux',code + 'arts-martiaux_1'] )
    liste.append( ['Aventure',code + 'aventure_1'] )
    liste.append( ['Biopic',code + 'biopic_1'] )
    liste.append( ['Comédie',code + 'film-comedie'] )
    liste.append( ['Comédie Dramatique',code + 'comedie-dramatique_1'] )
    liste.append( ['Documentaire',code + 'documentaire_1'] )
    liste.append( ['Drame',code + 'drame_1'] )
    liste.append( ['Epouvante Horreur',code + 'epouvante-horreur_1'] )
    liste.append( ['Erotique',code + 'erotique_1'] )
    liste.append( ['Espionnage',code + 'espionnage_1'] )
    liste.append( ['Fantastique',code + 'fantastique_1'] )
    liste.append( ['Guerre',code + 'guerre_1'] )
    liste.append( ['Historique',code + 'historique_1'] )
    liste.append( ['Musical',code + 'musical_1'] )
    liste.append( ['Policier',code + 'policier_1'] )
    liste.append( ['Romance',code + 'romance_1'] )
    liste.append( ['Science Fiction',code + 'science-fiction_1'] )
    liste.append( ['Série',code + 'series_1'] )
    liste.append( ['Thriller',code + 'thriller_1'] )
    liste.append( ['Western',code + 'western_1'] )
    liste.append( ['Non classé',code + 'non-classe_1'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1913, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1936, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'series' in sUrl:
        code = 'series/alphabet/'
    else:
        code = 'alphabet/'

    liste = []
    liste.append( ['0',URL_MAIN + code + '0'] )
    liste.append( ['1',URL_MAIN + code + '1'] )
    liste.append( ['2',URL_MAIN + code + '2'] )
    liste.append( ['3',URL_MAIN + code + '3'] )
    liste.append( ['4',URL_MAIN + code + '4'] )
    liste.append( ['5',URL_MAIN + code + '5'] )
    liste.append( ['6',URL_MAIN + code + '6'] )
    liste.append( ['7',URL_MAIN + code + '7'] )
    liste.append( ['8',URL_MAIN + code + '8'] )
    liste.append( ['9',URL_MAIN + code + '9'] )
    liste.append( ['A',URL_MAIN + code + 'A'] )
    liste.append( ['B',URL_MAIN + code + 'B'] )
    liste.append( ['C',URL_MAIN + code + 'C'] )
    liste.append( ['D',URL_MAIN + code + 'D'] )
    liste.append( ['E',URL_MAIN + code + 'E'] )
    liste.append( ['F',URL_MAIN + code + 'F'] )
    liste.append( ['G',URL_MAIN + code + 'G'] )
    liste.append( ['H',URL_MAIN + code + 'H'] )
    liste.append( ['I',URL_MAIN + code + 'I'] )
    liste.append( ['J',URL_MAIN + code + 'J'] )
    liste.append( ['K',URL_MAIN + code + 'K'] )
    liste.append( ['L',URL_MAIN + code + 'L'] )
    liste.append( ['M',URL_MAIN + code + 'M'] )
    liste.append( ['N',URL_MAIN + code + 'N'] )
    liste.append( ['O',URL_MAIN + code + 'O'] )
    liste.append( ['P',URL_MAIN + code + 'P'] )
    liste.append( ['Q',URL_MAIN + code + 'Q'] )
    liste.append( ['R',URL_MAIN + code + 'R'] )
    liste.append( ['S',URL_MAIN + code + 'S'] )
    liste.append( ['T',URL_MAIN + code + 'T'] )
    liste.append( ['U',URL_MAIN + code + 'U'] )
    liste.append( ['V',URL_MAIN + code + 'V'] )
    liste.append( ['W',URL_MAIN + code + 'W'] )
    liste.append( ['X',URL_MAIN + code + 'X'] )
    liste.append( ['Y',URL_MAIN + code + 'Y'] )
    liste.append( ['Z',URL_MAIN + code + 'Z'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)

        #pdata = 'action=recherche&story=' + sSearch

        oRequest = cRequestHandler(URL_MAIN + 'recherche?story=' + sSearch)
        #oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent',UA)
        oRequest.addHeaderEntry('Host','www.voirfilms.info')
        oRequest.addHeaderEntry('Referer',URL_MAIN)
        oRequest.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        #oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()

        sPattern = '<div class="imagefilm">.+?<img src="(.+?)".+?<a href="([^<>]+?)".+?titreunfilm" style="width:145px;"> *(.+?) *<\/div>'
        type = '1'

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        if 'animes/' in sUrl:
            sPattern = '<div class="imagefilm">.+?<a href="([^<>]+?)".+?<img src="(.+?)".+?titreunfilm" style="width:145px;">(.+?)<\/div>'
            type = '2'
        else:
            sPattern = '<div class="imagefilm">.+?<img src="(.+?)".+?<a href="([^<>]+?)".+?titreunfilm" style="width:145px;">(.+?)<\/div>'
            type = '1'

    sHtmlContent = sHtmlContent.replace('\n','')

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if not (aResult[0] == False):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if type == '2':
               sPicture = str(aEntry[1])
               sUrl = str(aEntry[0])
            else:
                sPicture = str(aEntry[0])
                sUrl = str(aEntry[1])

            sTitle = cUtil().unescape(aEntry[2])

            if not 'http' in sPicture:
                sPicture = URL_MAIN + sPicture

            if not 'http' in sUrl:
                sUrl = URL_MAIN[:-1] + sUrl

            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')

            #Vstream don't work with unicode url for the moment
            sPicture = unicode(sPicture,"UTF-8")
            sPicture = sPicture.encode('ascii', 'ignore').decode('ascii')
            #sPicture=sPicture.decode('utf8')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sPicture)

            if '/serie' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
            elif 'anime' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^'<>]+?)' rel='nofollow'>suiv »</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        next = aResult[1][0].replace(URL_MAIN, '')
        return URL_MAIN + next

    return False

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    # patch for unicode url
    sUrl = urllib.quote(sUrl,':/')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern='class="([vostfrL]+)"><\/span>.+?<a href="[^"]+" data-src="(.+?)" target="filmPlayer" class=.+?<span class="([^"]+)"><\/span>'
    sPattern='data-src="(.+?)" target="filmPlayer" class=.+?<span class="([^"]+)"><\/span>.+?class="([vostfrL]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHost = aEntry[1]
            sLang = aEntry[2].replace('L','')
            #sTitle = '(' + str(aEntry[1]) + ') [' + sHost + '] ' + sMovieTitle
            sTitle = '[%s] %s [COLOR coral]%s[/COLOR]' %(sLang.upper(),sMovieTitle,sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sDisplayTitle , sThumbnail, sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace("\n","")
    sHtmlContent = sHtmlContent.replace("\r\t","")

    if '-saison-' in sUrl or '/anime/' in sUrl:
        sPattern = '<li class="description132"><a class="n_episode2" title=".+?" href="(.+?)">(.+?)<\/a><\/li>'
    else:
        sMovieTitle = ''
        sPattern = '<div class="unepetitesaisons"><a href="(.+?)" title="(.+?)"><div class="saisonimage">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sEp = str(aEntry[1])
            sEp = re.sub('<span>(.+?)<\/span>','Episode \\1', str(sEp))

            sTitle = sMovieTitle + sEp
            sUrl = str(aEntry[0])
            if 'http' not in sUrl:
                sUrl = URL_MAIN + sUrl

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            if '-episode-' in aEntry[0] or '/anime' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHostersLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #On recupere la redirection
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-agent',UA)
    oRequestHandler.addHeaderEntry('Referer',URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    redirection_target = oRequestHandler.getRealUrl()

    #opener = urllib2.build_opener(NoRedirection)
    #opener.addheaders = [('User-agent', UA)]
    #response = opener.open(sUrl)
    #sHtmlContent = response.read()
    #if response.code == 302:
    #    redirection_target = response.headers['Location']
    #response.close()

    #cConfig().log('red > ' + redirection_target)
    #cConfig().log('cod > ' + sHtmlContent)

    #attention fake redirection
    #sUrl = redirection_target
    m = re.search(r'url=([^"]+)',sHtmlContent)
    if m:
        sUrl = m.group(1)

    #Modifications
    sUrl = sUrl.replace('1wskdbkp.xyz','youwatch.org')
    if '1fichier' in sUrl:
        sUrl = re.sub('(http.+?\?link=)','https://1fichier.com/?',sUrl)

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
