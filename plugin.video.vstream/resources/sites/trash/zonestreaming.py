#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.multihost import cJheberg
from resources.lib.util import cUtil
import re

#from base64 import urlsafe_b64encode
import htmlentitydefs, unicodedata

#ancien dpstreaming_tv
SITE_IDENTIFIER = 'zonestreaming'
SITE_NAME = 'Zone Streaming'
SITE_DESC = 'NC'

URL_MAIN = 'https://megastreaming.ws/'

MOVIE_MOVIE = (True, 'showMoviesMenu')
MOVIE_NEWS = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'category/films/vostfr-films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'category/films-en-exclus/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (True, 'showSeriesMenu')
SERIE_NEWS = (URL_MAIN + 'category/series-tv/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'category/series-tv/series-streaming-vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'category/series-tv/series-streaming-vostfr/', 'showMovies')
SERIE_VFQ = (URL_MAIN + 'category/series-tv/vfq/', 'showMovies')
SERIE_LIST = (URL_MAIN + 'category/series-tv/', 'showAZ')

REPLAYTV_NEWS = (URL_MAIN + 'category/emissions-tv/', 'showMovies')
REPLAYTV_TELE = (URL_MAIN + 'category/emissions-tv/telerealite/', 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')

DOC_NEWS = (URL_MAIN + 'category/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Menu)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Menu)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay tv', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showMoviesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFQ[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFQ[1], 'Séries (VFQ)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showAZ():
    oGui = cGui()

    liste = []
    liste.append( ["0-9", URL_MAIN + "category/series-streaming/0-9/"] )
    liste.append( ["A-B-C", URL_MAIN + "category/series-streaming/a-b-c/"] )
    liste.append( ["D-E-F", URL_MAIN + "category/series-streaming/d-e-f/"] )
    liste.append( ["G-H-I", URL_MAIN + "category/series-streaming/g-h-i/"] )
    liste.append( ["J-K-L", URL_MAIN + "category/series-streaming/j-k-l/"] )
    liste.append( ["M-N-O", URL_MAIN + "category/series-streaming/m-n-o/"] )
    liste.append( ["P-Q-R", URL_MAIN + "category/series-streaming/p-q-r/"] )
    liste.append( ["S-T-U", URL_MAIN + "category/series-streaming/s-t-u/"] )
    liste.append( ["V-W-X-Y-Z", URL_MAIN + "category/series-streaming/v-w-x-y-z/"] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'category/films-streaming/action/'] )
    liste.append( ['Animation', URL_MAIN + 'category/films-streaming/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'category/films-streaming/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'category/films-streaming/aventure-films/'] )
    liste.append( ['Biopic', URL_MAIN + 'category/films-streaming/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'category/films-streaming/comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'category/films-streaming/comedie-dramatique/'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'category/films-streaming/drame/'] )
    liste.append( ['Espionnage', URL_MAIN + 'category/films-streaming/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'category/films-streaming/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/films-streaming/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'category/films-streaming/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'category/films-streaming/historique/'] )
    liste.append( ['Horreur', URL_MAIN + 'category/films-streaming/horreur/'] )
    liste.append( ['Musical', URL_MAIN + 'category/films-streaming/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'category/films-streaming/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'category/films-streaming/romance/'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'category/films-streaming/science-fiction/'] )
    liste.append( ['Spectacle', URL_MAIN + 'category/films-streaming/spectacle/'] )
    liste.append( ['Thriller', URL_MAIN + 'category/films-streaming/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'category/films-streaming/western/'] )

    for sTitle, sUrl in liste:

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
    sHtmlContent = oRequestHandler.request()
    
    sHtmlContent = sHtmlContent.replace(' [Streaming]', '').replace(' [Streaming', '').replace(' [Telecharger]', '').replace(' [Téléchargement]', '').replace(' [Telechargement]', '')
    sPattern = '<div class="post-thumb is-image"><a href="([^"]+)".+?title="([^"]+)".+?src="([^"]+)".+?<p>([^<]+)<\/p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addNone(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1].replace('&prime;', '\'')
            sTitle = sTitle.replace('Saiosn', 'Saison')
            sThumb = aEntry[2]
            sDesc = aEntry[3]
            #Filtre recherche
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            #Mangas et Series fonctionnent pareil
            if '/series-tv/' in sUrl or '-saison-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSeries():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Nettoyage du code, a simplifier, mais je trouve pas ce qui ne va pas
    sHtmlContent = sHtmlContent.decode('utf-8', 'replace')
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode('unicode_escape')#vire accent et '\'
    sHtmlContent = sHtmlContent.encode('utf-8')#On remet en utf-8

    sHtmlContent = sHtmlContent.replace('<strong>Telechargement VOSTFR', '').replace('<strong>Telechargement VF', '').replace('<strong>Telechargement', '')
    sHtmlContent = sHtmlContent.replace('<a href="http://www.multiup.org', '')
    #supprimme pour récuperer les new regex different
    sHtmlContent = sHtmlContent.replace('<span style="color: #ff9900;">New</span>', '')
    sHtmlContent = sHtmlContent.replace('<span class="su-lightbox" data-mfp-src', '<a href')

    #récupération des Synopsis
    sDesc = ''
    try:
        sPattern = '(?:<p style="text-align: center;"|<p align="center")>([^<]+)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    sPattern = '<span style="color: #33cccc; font-size: large;"><b>([^<]+)|>(.pisode[^<]{2,12})<(?!\/a>)(.{0,10}a href="http.+?)(?:<.p>|<br|<.div)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #astuce en cas d'episode unique
    if not aResult[0]:
        #oGui.setEndOfDirectory()
        showHosters()
        return

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sMovieTitle = sMovieTitle.replace('[Complete]', '')
                sTitle = sMovieTitle + ' ' + aEntry[1]
                sUrl = aEntry[2]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addLink(SITE_IDENTIFIER, 'serieHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

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

    sPattern = '<span style="color: #ff990.+?>([^<]+)<|large button.+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                #nettoyage du titre
                sMovieTitle = re.sub('\[\w+ \w+]', '', sMovieTitle)
                sMovieTitle = re.sub('\[\w+]', '', sMovieTitle)

                sHosterUrl = aEntry[1]
                #pour récuperer tous les liens
                if '&url=' in sHosterUrl:
                    sHosterUrl = sHosterUrl.split('&url=')[1]

                #pour récuperer le lien jwplayer(GoogleDrive)
                if 'filmhdstream' in sHosterUrl:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    sHtmlContent = oRequestHandler.request()
                    sPattern = '<iframe.+?src="([^"]+)"'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        for aEntry in aResult[1]:
                            sHosterUrl = aEntry

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if (oHoster):
                                oHoster.setDisplayName(sMovieTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                #pour récuperer les liens jheberg
                elif 'jheberg' in sHosterUrl:
                    aResult = cJheberg().GetUrls(sHosterUrl)
                    if aResult:
                        for aEntry in aResult:
                            sHosterUrl = aEntry

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if (oHoster):
                                oHoster.setDisplayName(sMovieTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                else:
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()

    sPattern = 'href="([^"]+)"'
    aResult = oParser.parse(sUrl, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sHosterUrl = aEntry
            #pour récuperer tous les liens 2 variantes
            if '&url==' in sHosterUrl:
                sHosterUrl = sHosterUrl.split('&url==')[1]
            elif '&url=' in sHosterUrl:
                sHosterUrl = sHosterUrl.split('&url=')[1]

            #pour récuperer le lien jwplayer(GoogleDrive)
            if 'filmhdstream' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern = '<iframe.+?src="([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    for aEntry in aResult[1]:
                        sHosterUrl = aEntry

                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if (oHoster):
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            #pour récuperer les liens jheberg
            elif 'jheberg' in sHosterUrl:
                aResult = cJheberg().GetUrls(sHosterUrl)
                if aResult:
                    for aEntry in aResult:
                        sHosterUrl = aEntry

                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if (oHoster):
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
