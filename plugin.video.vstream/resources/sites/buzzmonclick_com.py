#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import progress#, VSlog
#from resources.lib.util import cUtil
import re, unicodedata

SITE_IDENTIFIER = 'buzzmonclick_com'
SITE_NAME = 'BuzzMonClick'
SITE_DESC = 'Films & Séries en Streaming de qualité entièrement gratuit.'

URL_MAIN = 'https://buzzmonclick.net/category/replay-tv/'

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

DOC_DOCS = ('http://', 'load')
DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')

URL_SEARCH = ('https://buzzmonclick.net/?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay TV', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'divertissement/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Divertissement', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'infos-magazine/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Infos/Magazines', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'tele-realite/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Télé-Réalité', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Documentaires', URL_MAIN + 'documentaires/'] )
    liste.append( ['Divertissement', URL_MAIN + 'divertissement/'] )
    liste.append( ['Infos/Magazines', URL_MAIN + 'infos-magazine/'] )
    liste.append( ['Télé-Réalité', URL_MAIN + 'tele-realite/'] )

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

    sPattern ='<div id="(post-[0-9]+)".+?<a class="clip-link".+?title="([^"]+)" href="([^"]+)".+?img src="([^"]+)"'
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

            sTitle = unicode(aEntry[1], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            #sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")

            #mise en page
            sTitle = sTitle.replace('Permalien pour', '').replace('&prime;', '\'')
            sTitle = re.sub('(?:,)* (?:Replay |Video )*du ([0-9]+ [a-zA-z]+ [0-9]+)', ' (\\1)', sTitle)
            sTitle = re.sub(', (?:Replay|Video)$', '', sTitle)
            sUrl = aEntry[2]
            sThumb = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'class="nextpostslink" rel="next" href="([^"]+)"'
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
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^"]+)" target="_blank" rel="noreferrer noopener">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        sPattern = 'iframe src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
    else:
        oRequestHandler = cRequestHandler(''.join(aResult[1]))
        sHtmlContent = oRequestHandler.request()

        sPattern = '<a href="([^"]+)" target="_blank" class="link link--external" rel="nofollow '
        aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'gounlimited' in aEntry:
                oRequestHandler = cRequestHandler(aEntry)
                sHtmlContent = oRequestHandler.request()

                sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    sHtmlContent = cPacker().unpack(aResult[1][0])

                    sPattern = '{sources:\["([^"]+)"'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if (aResult[0] == True):
                        sHosterUrl = aResult[1][0]
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if (oHoster != False):
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            else:
                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
