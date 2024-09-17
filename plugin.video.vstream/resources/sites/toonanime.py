# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import urlEncode

try:
    xrange
except NameError:
    xrange = range

SITE_IDENTIFIER = 'toonanime'
SITE_NAME = 'Toon Anime'
SITE_DESC = 'anime en VF/VOSTFR'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showMovies')
ANIM_VFS = (URL_MAIN + 'anime-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime-vostfr/', 'showMovies')
ANIM_FILM = (URL_MAIN + 'films/', 'showMovies')
ANIM_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', "Recherche d'animés", 'search.png', oOutputParameterHandler)

    # TODO
    # oOutputParameterHandler.addParameter('siteUrl', ANIM_FILM[0])
    # oGui.addDir(SITE_IDENTIFIER, ANIM_FILM[1], "Film d'animation japonais (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Dernier ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'Action'], ['Animation', 'Action'], ['Aventure', 'Aventure'], ['Comédie', 'Comédie'],
             ['Tranche de Vie', 'Tranche de vie'], ['Drame', 'Drame'], ['Fantasy', 'Fantasy'],
             ['Surnaturel', 'Surnaturel'], ['Mystère', 'Mystère'], ['Shonen', 'Shonen'],
             ['Psychologique', 'Psychologique'], ['Romance', 'Romance'], ['Science-Fiction', 'Sci-Fi']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'xfsearch/genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(xrange(1982, 2025)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'xfsearch/year/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = URL_SEARCH[0]
        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '0'), ('full_search', '1'))
        data = urlEncode(query_args)

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addHeaderEntry('Content-Length', str(len(data)))
        sHtmlContent = oRequestHandler.request()
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    if "/films/" in sUrl:
        sPattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" *alt="([^"]+).+?pg">([^<]+).+?text">([^<]+)'
    else:
        sPattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" *alt="([^"]+).+?pg">([^<]+).+?cat">([^<]+).+?text">([^<]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            if "/films/" in sUrl:
                sTitle = aEntry[2]
                sQual = aEntry[3]
                sDesc = aEntry[4]
                sLang = ""
            else:
                sLang = aEntry[2].split(" ")[-1]
                sTitle = re.sub('Saison \d+', '', aEntry[2][:aEntry[2].rfind('')].replace(sLang, "")) + " " + aEntry[4]
                sQual = aEntry[3]
                sDesc = aEntry[5]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang.upper())

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "/films/" in sUrl:
                sID = sUrl.split('/')[3].split('-')[0]
                oOutputParameterHandler.addParameter('id', sID)
                oGui.addMovie(SITE_IDENTIFIER, 'ShowSxE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'ShowSxE', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^"]+)"><span class="md__icon md-arrowr"></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return aResult[1][0]

    return False


def ShowSxE():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    # sMovieTitle = re.sub('Episode \d+', '', sMovieTitle)

    # film ou série ?
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'header">Catégorie.+?>([^<]+)<\/a'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        isFilm = 'Film' in aResult[1][0]


    sID = sUrl.split('/')[3].split('-')[0]

    oRequestHandler = cRequestHandler(URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)['html']

    
    sPattern = 'href="(.+?)".+?title="(.+?)">'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=True)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if isFilm:
                sTitle = sMovieTitle
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addMovie(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                sTitle = aEntry[1]
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addEpisode(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def seriesHosters():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sID = sUrl.replace(URL_MAIN, '').replace('/', '').split('-')[0]

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-class="(.+?) ".+?data-server-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    oRequestHandler = cRequestHandler(URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)['html']

    if aResult[0]:
        sOldHosterUrl = None
        for aEntry in aResult[1]:
            sPattern = '<div id=\\"content_player_' + aEntry[1] + '\\".+?>(.+?)<'
            aResult1 = oParser.parse(sHtmlContent, sPattern)
            hostClass = aEntry[0]

            for aEntry1 in aResult1[1]:
                # sTitle = sMovieTitle  + " [COLOR coral]" + hostClass.capitalize() + "[/COLOR]"

                sHosterUrl = None
                if "https" in aEntry1:
                    sHosterUrl = aEntry1
                    sHosterUrl = sHosterUrl.replace('////', '//')
                elif hostClass == "cdnt":
                    sHosterUrl = "https://lb.toonanime.xyz/playlist/" + aEntry1 + "/" + str(round(time.time() * 1000))
                else:
                    oRequestHandler = cRequestHandler(URL_MAIN + "/templates/toonanime/js/anime.js")
                    sHtmlContent1 = oRequestHandler.request()
                    sPattern = 'player_type=="toonanimeplayer_' + hostClass + '".+?src=\\\\"([^\\\\]+)\\\\"'
                    aResult2 = oParser.parse(sHtmlContent1, sPattern)
                    if aResult2[0]:
                        urlBase = aResult2 [1][0]
                        sHosterUrl = urlBase.replace('"+player_content+"', aEntry1)

            
                if sHosterUrl:

                    if sHosterUrl == sOldHosterUrl:
                        continue # filtre des liens en doublon 
                    sOldHosterUrl = sHosterUrl
                    
                    if 'vidcdn' in sHosterUrl:
                        m = re.search('id=([^&]+)', sHosterUrl)
                        if m:
                            idVid = m.group(1)
                            if sHosterUrl.endswith('cdn'):
                                sUrl = 'https://sr1.vidcdn.xyz/v1/api/get_sources/' + idVid
                            else:
                                sUrl = 'https://cdn2.vidcdn.xyz/azz/' + idVid
                            oRequestHandler = cRequestHandler(sUrl)
                            oRequestHandler.addHeaderEntry('Referer', 'https://play.vidcdn.xyz/')
                            sHtmlContent1 = oRequestHandler.request()
                            sPattern = '"file": "([^"]+)'
                            aResult2 = oParser.parse(sHtmlContent1, sPattern)
                            if aResult2[0]:
                                sHosterUrl = aResult2 [1][0]
                                sHosterUrl = sHosterUrl.replace('%2B', '+')
                        
                    if "toonanime" in sHosterUrl:
                        oHoster = cHosterGui().checkHoster(".mp4")
                    else:
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
    
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
