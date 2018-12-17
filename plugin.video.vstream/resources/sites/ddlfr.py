#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog
from resources.lib.util import cUtil
import base64

#17/12/18 #ATTENTION site utiliant un mineur.
return False

SITE_IDENTIFIER = 'ddlfr'
SITE_NAME = 'DDLFR (beta)'
SITE_DESC = 'Films, séries, documentaires, replay et sports en streaming'

URL_MAIN = 'https://ddlfr.pw/'

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
#recherche global films
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
#recherche global serie, manga
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
#recherche global divers
URL_SEARCH_MISC = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
#
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_MOVIE = ('http://', 'load')
MOVIE_HD = (URL_MAIN + 'bluray/hd-1080p/', 'showMovies') #films HD
MOVIE_VOSTFR = (URL_MAIN + 'films/vo-vostfr/', 'showMovies')

SERIE_SERIES = ('http://', 'load') #séries (load source)
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'series/vf/', 'showMovies') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr/', 'showMovies') #serie VOSTFR

ANIM_ENFANTS = (URL_MAIN + 'dessins-animes/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')

#avec capTcha
#DOC_NEWS = (URL_MAIN + 'replay-tv/documentaires/', 'showMovies')

#SPORT_SPORTS = (URL_MAIN + 'replay-tv/sports/', 'showMovies')

#REPLAYTV_REPLAYTV = (URL_MAIN + 'replay-tv/emissions-tv-tele/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ENFANTS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ENFANTS[1], 'Dessins animés', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    # oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Replay TV', 'replay.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Sports', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #Vslog(sHtmlContent)
    #supprime la pub dans les émissions tv
    sHtmlContent = sHtmlContent.replace(' alt="ABONNEMENT IPTV"', '')
    #la fonction replace est pratique pour supprimer un code du resultat

    sPattern = '<a class="short-poster.+?" href="([^"]+)"><img itemprop="image" src="([^"]+)" alt="([^"]+)"\/>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2]
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''

            sTitle = sTitle.replace('FRENCH', '')
            sTitle = sTitle.replace('BDRIP', '')
            sTitle = sTitle.replace('WEBRIP', '')
            sTitle = sTitle.replace('HDRIP', '')
            sTitle = sTitle.replace('DVDRIP', '')
            sTitle = sTitle.replace('HDTV', '')
            sTitle = sTitle.replace('720p', '')
            sTitle = sTitle.replace('1080p', '')

            #tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="pnext"><a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)
    oParser = cParser()

    sDesc = ''

    sPattern = 'data-re_idnews="([^"]+)" data-re_xfn="video" data-re_page="([^"]+)">([^<]+)</div>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)


    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            #VSlog(aEntry)
            sId = aEntry[0]
            sPage = aEntry[1]
            sTitle = sMovieTitle + ' (' + aEntry[2] + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sPage', sPage)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if (sPage != '0'):
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    #VSlog('showHosters')
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sId = oInputParameterHandler.getValue('sId')
    sPage = oInputParameterHandler.getValue('sPage')

    sUrl2 = URL_MAIN + 'engine/ajax/re_video_part.php'
    #VSlog(sUrl2)
    #VSlog(sId)
    #VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl2)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    oRequestHandler.addHeaderEntry('Origin', URL_MAIN)
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addParameters('block', 'video')
    oRequestHandler.addParameters('page', sPage)
    oRequestHandler.addParameters('id', sId)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)

    sHosterUrl = sHtmlContent
    #VSlog(sHosterUrl)

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    #VSlog(oHoster)
    if (oHoster != False):
        sHosterUrl = sHosterUrl
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

#Pour les series, il y a generalement une etape en plus pour la selection des episodes ou saisons.
def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '?????????????????????'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle + aEntry[0]
            sUrl2 = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<dd><a href="([^<]+)" class="zoombox.+?" title="(.+?)"><button class="btn">.+?</button></a></dd>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(aEntry[1])
                oHoster.setFileName(aEntry[1])
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
