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
from resources.lib.comaddon import siteManager
from resources.lib.util import urlEncode, cUtil

try:
    xrange
except NameError:
    xrange = range


SITE_IDENTIFIER = 'animesultra'
SITE_NAME = 'Animes Ultra'
SITE_DESC = 'Regarder gratuitement vos animes VF/VOSTFR préférés'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN + 'dernier-episodes/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'anime-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime-vostfr/', 'showMovies')
ANIM_ANNEES = (True, 'showYears')
ANIM_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', "Recherche d'animés", 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Dernier ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

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

    liste = [['Action', 'Action'], ['Aventure', 'Aventure'], ['Comédie', 'Comédie'],
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
    for i in reversed(xrange(1982, 2026)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'xfsearch/year/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if not sSearch:
        sSearch = oInputParameterHandler.getValue('sSearch') or ''
    
    bSearch = bool(sSearch)
    
    current_page = 1
    if bSearch:
        sPage = oInputParameterHandler.getValue('sPage')
        if sPage and sPage.isdigit():
            current_page = int(sPage)
    
    if bSearch:
        sUrl = URL_SEARCH[0]
        oUtil = cUtil()
        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')
        sSearchText = oUtil.CleanName(sSearch)
        
        query_args = [('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '0'), ('full_search', '1')]
        if current_page > 1:
            query_args.append(('search_start', str(current_page)))
            result_from = (current_page - 1) * 12 + 1
            query_args.append(('result_from', str(result_from)))
        else:
            query_args.append(('search_start', '0'))
            query_args.append(('result_from', '1'))
        
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
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    
    if "/films/" in sUrl:
        sPattern = '<article class="short__story.+?href="([^"]+).+?data-src="([^"]+)" alt="([^"]+).+?pg">([^<]+).+?text">([^<]+)'
    else:
        sPattern = r'<div class="flw-item">[\s\S]*?<img data-src="([^"]*)"[^>]*alt="([^"]*)"[\s\S]*?<div class="film-detail">[\s\S]*?<a href="([^"]+)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            
            if "/films/" in sUrl:
                sTitle = aEntry[2]
                sQual = aEntry[3]
                sDesc = aEntry[4]
                sLang = ""
            else:
                sLang = aEntry[1].split(" ")[-1]
                sTitle = aEntry[1].replace(" VF", "").replace(" VOSTFR", "")
            
            sDisplayTitle = ('%s (%s)') % (sTitle, sLang.upper())
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addAnime(SITE_IDENTIFIER, 'ShowSxE', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
    
    next_page = __checkForNextPage(sHtmlContent, current_page, bSearch)
    if next_page:
        oOutputParameterHandler = cOutputParameterHandler()
        if bSearch:
            oOutputParameterHandler.addParameter('sSearch', sSearch)
            oOutputParameterHandler.addParameter('sPage', str(next_page))
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(next_page), oOutputParameterHandler)
        else:
            oOutputParameterHandler.addParameter('siteUrl', next_page)
            sNumPage = re.search('/page/([0-9]+)', next_page).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)
    
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent, current_page=1, bSearch=False):
    """
    Retourne la pagination selon le mode:
    - bSearch=True: retourne le numéro de page suivant (int) depuis onclick="list_submit(N)"
    - bSearch=False: retourne l'URL de la page suivante (str) depuis href=".../page/N/"
    """
    oParser = cParser()
    if bSearch:
        sPattern = r'onclick="javascript:list_submit\((\d+)\)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            pages = [int(x) for x in aResult[1] if x.isdigit()]
            pages.sort()
            for p in pages:
                if p > current_page:
                    return p
        return False
    else:
        sPattern = r'<a\s+(?=[^>]*?title\s*=\s*["\']next["\'])(?=[^>]*?class\s*=\s*["\']page-link["\'])[^>]*?href\s*=\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return False


def ShowSxE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    sID = sUrl.split('/')[4].split('-')[0]

    oRequestHandler = cRequestHandler(URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)['html']

    sPattern = 'href="(.+?)".+?title="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace(" VF", "").replace(" VOSTFR", "")
            sUrl2 = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('id', sID)

            oGui.addEpisode(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def seriesHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sID = oInputParameterHandler.getValue('id')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-class="(.+?) ".+?data-server-id="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    oRequestHandler = cRequestHandler(URL_MAIN + 'engine/ajax/full-story.php?newsId=' + sID)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)['html']


    if aResult[0]:
        for aEntry in aResult[1]:
            sPattern = '<div id=\\"content_player_' + aEntry[1] + '\\".+?>(.+?)<'
            aResult1 = oParser.parse(sHtmlContent, sPattern)
            hostClass = aEntry[0]

            for aEntry1 in aResult1[1]:
                if 'https' in aEntry1:
                    sHosterUrl = aEntry1
                elif hostClass == "cdnt":
                    sHosterUrl = "https://lb.toonanime.xyz/playlist/" + aEntry1 + "/" + str(round(time.time() * 1000))
                elif hostClass == "sibnet":
                    sHosterUrl = "https://video.sibnet.ru/shell.php?videoid=" + aEntry1 + "/"
                else:
                    continue

                sHosterUrl = sHosterUrl.replace("////", "//")

                if "toonanime" in sHosterUrl:
                    oHoster = cHosterGui().checkHoster(".mp4")
                else:
                    oHoster = cHosterGui().checkHoster(sHosterUrl)

                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
