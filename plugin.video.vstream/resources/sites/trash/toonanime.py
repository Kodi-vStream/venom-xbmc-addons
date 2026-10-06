# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'toonanime'
SITE_NAME = 'Toon Anime'
SITE_DESC = 'anime en VF/VOSTFR'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = ('anime?type=animes&sort=date_sortie_desc', 'showMovies')
ANIM_GENRES = ('anime?type=animes&sort=popularite_desc&genres=', 'showGenres')
ANIM_FILM = ('anime?type=film&sort=date_sortie_desc', 'showMovies')
ANIM_OAV = ('anime?type=ova', 'showMovies')


URL_SEARCH = ('anime?q=', 'showMovies')
URL_SEARCH_ANIMS = ('anime?type=animes&q=', 'showMovies')
URL_SEARCH_MOVIES = ('anime?type=animes&q=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', "Rechercher (Animés)", 'search-animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', "Rechercher (Films)", 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Nouveautés)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_FILM[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_FILM[1], "Films (Nouveautés)", 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_OAV[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_OAV[1], "Films (OAV)", 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        showMovies(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'Action'], ['Aventure', 'Aventure'], ['Comédie', 'Comedie'], ['Drame', 'Drame'],
             ['Ecchi', 'Ecchi'],['Fantastique', 'Fantastique'], ['Horreur', 'Horreur'], ['Mahou Shoujo', 'Mahou Shoujo'], ['Musique', 'Musique'],
             ['Mecha', 'Mecha'],['Mystère', 'Mystere'], 
             ['Psychologique', 'Psychologique'], ['Romance', 'Romance'], 
             ['Science-Fiction', 'Science-Fiction'], ['Sports', 'Sports'],  ['Surnaturel', 'Surnaturel'], ['Thriller', 'Thriller'], ['Tranche de Vie', 'Tranche de vie']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', '%s%s%s' % (URL_MAIN, ANIM_GENRES[0], sUrl))
        oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    bAnime = 'type=animes' in sUrl

    # titre    url    thumb
    oParser = cParser()
    sPattern = '<article class="relative group.+?title="([^"]+).+?href="([^"]+).+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oUtil = cUtil()
        oOutputParameterHandler = cOutputParameterHandler()
        titles = []
        for aEntry in aResult[1]:
            sTitle = aEntry[0]
            # une seule série par saison, la saison se sélectionne ensuite 
            sTitle = oUtil.unescape(re.sub('Saison \d+', '', sTitle[:sTitle.rfind('')])).strip()
            if sTitle in titles:
                continue
            titles.append(sTitle)

            sUrl2 = aEntry[1]
            sThumb = aEntry[2]
            sLang = ''
            sQual = ''
            sDesc = ''

            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang.upper())

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if bAnime:
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oGui.addAnime(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                sUrl2 += '&ep=1'
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            hasNextPage = re.search('/page=([0-9]+)', sNextPage)
            sNumPage = '2'
            if hasNextPage:
                sNumPage = hasNextPage.group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'next page" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def showSaisons():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    if not sUrl.startswith('http'):
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    # url    thumb    titre
    sPattern = 'children":\["\d+"," épisodes.+?href":"([^"]+).+?"src":"([^"]+)","alt":"([^"]+)'
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('\\', '')
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if not aResult[0]:  # pas de saisons, renvoie vers les épisodes
        return showEpisodes()
        
    oOutputParameterHandler = cOutputParameterHandler()
    oUtil = cUtil()
    for aEntry in aResult[1]:
        sUrl2 = URL_MAIN + aEntry[0]
        sThumb = aEntry[1]
        sTitle = oUtil.unescape(aEntry[2])
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    if not sUrl.startswith('http'):
        sUrl = URL_MAIN + sUrl

    sHtmlContent = cRequestHandler(sUrl).request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    aResult = oParser.abParse(sHtmlContent, '"eps":[{', '}]')
    aResult = aResult.replace('" vostfr', '"vostfr').replace('" fr', '"fr')
    aResult = aResult.replace('""', '"').replace(' "', ' ').replace('" ', ' ').replace('".', '.').replace('", ', ', ')
    aResult = aResult.replace('"img":",', '"img":"",').replace('"desc":",', '"desc":"",')

    try:
        episodes = json.loads('{' + aResult + '}]}')
        if episodes:
            oOutputParameterHandler = cOutputParameterHandler()
            for episode in episodes['eps']:
                numEp = episode['n']
                sTitle = '%s Episode %d' % (sMovieTitle, numEp)
                sThumb = episode['img']
                sDesc = episode['desc']
                oOutputParameterHandler.addParameter('siteUrl', '%s&ep=%d' % (sUrl, numEp))
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addSeason(SITE_IDENTIFIER, 'showLinks', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
    except:
        pass

    oGui.setEndOfDirectory()




def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl, numEpSearch = oInputParameterHandler.getValue('siteUrl').split('&ep=')
    if not sUrl.startswith('http'):
        sUrl = URL_MAIN + sUrl

    sHtmlContent = cRequestHandler(sUrl+'/watch').request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    aResult = oParser.abParse(sHtmlContent, '"episodes":[{', '}]')
    aResult = aResult.replace('" vostfr', '"vostfr').replace('" vf', '"vf')
    aResult = aResult.replace('""', '"').replace(' "', ' ').replace('" ', ' ').replace('".', '.').replace('", ', ', ')
    aResult = aResult.replace('"img":",', '"img":"",').replace('"desc":",', '"desc":"",')

    try:
        episodes = json.loads('{' + aResult + '}]}')
        if episodes:
            for episode in episodes['episodes']:
                numEp = str(episode['n'])
                if numEpSearch == numEp:
                    sThumb = episode['img']
                    for numLink in episode['srv']:
                        link = episode['srv'][numLink]
                        sLang = link.get('stp', '')
                        #sQual = link.get('quality', '').replace('720', 'HD')
                        sHosterUrl = link.get('surl', '')
                        sDisplayTitle = '%s [%s]' % (sMovieTitle, sLang.upper())
    
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
        
                        if oHoster:
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                    break
    except:
        pass
    

    oGui.setEndOfDirectory()


