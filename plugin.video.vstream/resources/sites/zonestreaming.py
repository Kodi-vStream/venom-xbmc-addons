#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

#from base64 import urlsafe_b64encode
import htmlentitydefs,unicodedata

#ancien dpstreaming_tv
SITE_IDENTIFIER = 'zonestreaming'
SITE_NAME = 'ZoneStreaming'
SITE_DESC = 'NC'

URL_MAIN = 'http://zonestreaming.ws/'

MOVIE_NEWS = (URL_MAIN+'category/films-streaming/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'category/films-streaming/vostfr-films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN+'category/films-en-exclus/', 'showMovies')
SERIE_SERIES = (URL_MAIN+'category/series-streaming/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'category/series-streaming/series-streaming-vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'category/series-streaming/series-streaming-vostfr/', 'showMovies')

MOVIE_GENRES = (True, 'showGenre')
REPLAYTV_REPLAYTV = (URL_MAIN+'category/emissions-tv/', 'showMovies')
DOC_DOCS = (URL_MAIN+'category/documentaire/', 'showMovies')

URL_SEARCH = ('http://zonestreaming.ws/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)



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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'films_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showAZ', 'Series A-Z', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Replay tv', 'tv.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://zonestreaming.ws/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ["0-9",URL_MAIN+"category/series-streaming/0-9/"] )
    liste.append( ["A-B-C",URL_MAIN+"category/series-streaming/a-b-c/"] )
    liste.append( ["D-E-F",URL_MAIN+"category/series-streaming/d-e-f/"] )
    liste.append( ["G-H-I",URL_MAIN+"category/series-streaming/g-h-i/"] )
    liste.append( ["J-K-L",URL_MAIN+"category/series-streaming/j-k-l/"] )
    liste.append( ["M-N-O",URL_MAIN+"category/series-streaming/m-n-o/"] )
    liste.append( ["P-Q-R",URL_MAIN+"category/series-streaming/p-q-r/"] )
    liste.append( ["S-T-U",URL_MAIN+"category/series-streaming/s-t-u/"] )
    liste.append( ["V-W-X-Y-Z",URL_MAIN+"category/series-streaming/v-w-x-y-z/"] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Action',URL_MAIN+'category/films-streaming/action/'] )
    liste.append( ['Animation',URL_MAIN+'category/films-streaming/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN+'category/films-streaming/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN+'category/films-streaming/aventure-films/'] )
    liste.append( ['Biopic',URL_MAIN+'category/films-streaming/biopic/'] )
    liste.append( ['Comedie',URL_MAIN+'category/films-streaming/comedie/'] )
    liste.append( ['Comedie Dramatique',URL_MAIN+'category/films-streaming/comedie-dramatique/'] )
    liste.append( ['Documentaire',URL_MAIN+'category/documentaire/'] )
    liste.append( ['Drame',URL_MAIN+'category/films-streaming/drame/'] )
    liste.append( ['Espionnage',URL_MAIN+'category/films-streaming/espionnage/'] )
    liste.append( ['Famille',URL_MAIN+'category/films-streaming/famille/'] )
    liste.append( ['Fantastique',URL_MAIN+'category/films-streaming/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN+'category/films-streaming/guerre/'] )
    liste.append( ['Historique',URL_MAIN+'category/films-streaming/historique/'] )
    liste.append( ['Horreur',URL_MAIN+'category/films-streaming/horreur/'] )
    liste.append( ['Musical',URL_MAIN+'category/films-streaming/musical/'] )
    liste.append( ['Policier',URL_MAIN+'category/films-streaming/policier/'] )
    liste.append( ['Romance',URL_MAIN+'category/films-streaming/romance/'] )
    liste.append( ['Science-Fiction',URL_MAIN+'category/films-streaming/science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN+'category/films-streaming/spectacle/'] )
    liste.append( ['Thriller',URL_MAIN+'category/films-streaming/thriller/'] )
    liste.append( ['Western',URL_MAIN+'category/films-streaming/western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('[Streaming]', '').replace('[Telecharger]', '')
    sPattern = 'item-header.+?<img src="([^"]+)".+?<a href="([^>]+)">([^<]+)</a>.+?<p>(.+?)</p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = unicode(aEntry[2], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")

            sCom = unicode(aEntry[3], 'utf-8')#converti en unicode
            sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
            sCom = unescape(sCom)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            #Mange et Series fonctionnent pareil
            if '/series-tv/' in sUrl or 'saison' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)
            elif '/mangas/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Nettoyage du code, a simplifier, mais je trouve pas ce qui ne va pas
    sHtmlContent = sHtmlContent.decode('utf-8',"replace")
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sHtmlContent = sHtmlContent.encode('utf-8')#On remet en utf-8

    sHtmlContent = sHtmlContent.replace('<strong>Telechargement VOSTFR','').replace('<strong>Telechargement VF','').replace('<strong>Telechargement','')
    sHtmlContent = sHtmlContent.replace('<a href="http://www.multiup.org','')
    sHtmlContent = sHtmlContent.replace('<iframe src="http://ads.affbuzzads.com','')
    sHtmlContent = sHtmlContent.replace('<iframe src="//ads.ad-center.com','')

    #sPattern = '<span style="color: #33cccc;"><strong>([^<]+)|>(Episode[^<]{2,12})<(?!\/a>)(.+?)(?:<.p|<br|<.div)'
    sPattern = '<span style="color: #33cccc;"><strong>([^<]+)|>(Episode[^<]{2,12})<(?!\/a>)(.{0,10}a href="http.+?)(?:<.p|<br|<.div)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #astuce en cas d'episode unique
    if (aResult[0] == False):
        #oGui.setEndOfDirectory()
        showHosters()
        return;

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sTitle = sMovieTitle+' - '+aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'page-numbers.+?current.+?href="(.+?)"'
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
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="http://ads.affbuzzads.com','')
    sHtmlContent = sHtmlContent.replace('<iframe src="//ads.ad-center.com','')

    sPattern = 'large button.+?href="(.+?)"'
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

            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()

    liste = False

    sPattern = 'href="([^<]+)" target="_blank".+?</a>'
    aResult = oParser.parse(sUrl, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        index = 1
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle
            if liste:
                sTitle = sTitle + ' (' + str(index) + ') '
                index = index + 1
            #print aEntry
            sHosterUrl = str(aEntry)
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
