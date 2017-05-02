#-*- coding: utf-8 -*-
#Venom.Kodigoal.Razorex

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,unicodedata

SITE_IDENTIFIER = 'cinemay_com'
SITE_NAME = 'Cinemay'
SITE_DESC = 'Films et séries en streaming'

URL_MAIN = 'http://www.cinemay.com/'

MOVIE_NEWS = (URL_MAIN , 'showMoviesNews')
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_SERIES = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
	
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
    liste.append( ['Action',URL_MAIN + 'action/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'biopic/'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique/'] )
    liste.append( ['Disney',URL_MAIN + 'disney/'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'historique/'] )
    liste.append( ['Manga',URL_MAIN + 'manga/'] )
    liste.append( ['Musical',URL_MAIN + 'musical/'] )
    liste.append( ['Non_classé',URL_MAIN + 'non-classe/'] )
    liste.append( ['Péplum',URL_MAIN + 'peplum-2/'] )
    liste.append( ['Policier',URL_MAIN + 'policier/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science_Fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + 'spectacle/'] )
    liste.append( ['Télé',URL_MAIN + 'tele/'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller/'] )
    liste.append( ['VO-VOST',URL_MAIN + 'vo/'] )
    liste.append( ['Western',URL_MAIN + 'western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'cat/action-3/'] )
    liste.append( ['Animation',URL_MAIN + 'cat/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'cat/arts-martiaux-2/'] )
    liste.append( ['Aventure',URL_MAIN + 'cat/aventure/'] )
    liste.append( ['Comédie',URL_MAIN + 'cat/comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'cat/comedie-dramatique/'] )
    liste.append( ['Documentaire',URL_MAIN + 'cat/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'cat/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'cat/epouvante-horreur/'] )
    liste.append( ['Erotique',URL_MAIN + 'cat/erotique/'] )
    liste.append( ['Espionnage',URL_MAIN + 'cat/espionnage/'] )
    liste.append( ['Fantastique',URL_MAIN + 'cat/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'cat/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'cat/historique-2/'] )
    liste.append( ['Judiciaire',URL_MAIN + 'cat/judiciaire/'] )
    liste.append( ['Manga',URL_MAIN + 'cat/manga/'] )
    liste.append( ['Médical',URL_MAIN + 'cat/medical/'] )
    liste.append( ['Musical',URL_MAIN + 'cat/musical-comedie/'] )
    liste.append( ['Mystères',URL_MAIN + 'cat/mysteres/'] )
    liste.append( ['Péplum',URL_MAIN + 'cat/peplum/'] )
    liste.append( ['Policier',URL_MAIN + 'cat/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'cat/romance-2/'] )
    liste.append( ['Science_Fiction',URL_MAIN + 'cat/science-fiction/'] )
    liste.append( ['Soap',URL_MAIN + 'cat/soap/'] )
    liste.append( ['Spectacle',URL_MAIN + 'cat/spectacle-2/'] )
    liste.append( ['Sport',URL_MAIN + 'cat/sport-2/'] )
    liste.append( ['Télé Réalité',URL_MAIN + 'cat/tele-realite/'] )
    liste.append( ['Thriller',URL_MAIN + 'cat/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'cat/western-2/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesNews():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()
    #Decoupage pour cibler la partie Film ajouté
    sPattern = '<h1>Dernier Films Ajouté</h1>(.+?)</body>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #regex pour listage films sur la partie decoupée
    sHtmlContent = aResult

    sPattern = '<img class="imgpic" src="(.+?)".+?/>.+?<h3.+?><a href="(.+?)"  title=".+?">.+?<strong>(.+?)</strong></a>.+?</h3>.+?<div class="infob">.+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #encode/decode pour affichage des accents
            sTitle = unicode(aEntry[2].replace('streaming','').replace('Streaming',''), 'utf-8')

            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore').decode("unicode_escape")
            sTitle = sTitle.encode("latin-1")

            sCom = aEntry[3]
            sCom = sCom.decode("unicode_escape").encode("latin-1")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<img class="imgpic" src="(.+?)".+?/>.+?<h3.+?><a href="(.+?)"  title=".+?">.+?<strong>(.+?)</strong></a>.+?</h3>.+?<div class="infob">.+?<p>(.+?)</p>'
    oParser = cParser()
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
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue

            sTitle = aEntry[2].replace('streaming','').replace('Streaming','')

            sCom = aEntry[3]
            #sCom = sCom.decode("utf-8", "ignore")
            sCom = sCom.decode("unicode_escape").encode("latin-1")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/serie/' in sUrl or '/serie/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, aEntry[0], aEntry[0], sCom , oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sNext = aResult[1][0]
        return sNext

    return False

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<ul class="css-tabs_series skin3">(.+?)</ul><div class="css-panes_series skin3">(.+?)</div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    list = str(aResult[1][0][0]).split('<li>')
    list2 = str(aResult[1][0][1]).split('<div>')

    newList = ''
    for index, item in enumerate(list):
        item2 = list2[index]
        newList+=( item + item2)
        
    sPattern = '<a href="#">([^<]+)</a>|<li class="bordred"><small><em>.+?</em></small>.+?<a href="([^<]+)" class="link_series_epi">([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(newList, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[0]
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR red]' + str(aEntry[0]) + '[/COLOR]', 'host.png', oOutputParameterHandler)

            else:
                sTitle = sMovieTitle + ' ' + sSaison + aEntry[2]
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)        

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<td><a href="\/(.+?)">(.+?)<\/a>.+?<span class="user-icn">.+?<td>(.+?)<\/td>.+?\/cinema\/images\/([vostfren]+)\.png">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sHoster = aEntry[1].lower().replace(' ','')
            sQual = aEntry[2].replace(' ','')
            sLang = aEntry[3].upper()

            #sTitle = sMovieTitle + '['+ sQual + '-' + sLang + '] - [COLOR skyblue]' + sHoster +'[/COLOR]'
            sTitle = ('%s [%s] [%s] (%s)') % (sMovieTitle, sQual, sLang , sHoster)
            
            sUrl = URL_MAIN + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<iframe src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
