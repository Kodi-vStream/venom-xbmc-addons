# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto et Arias800 02/06/2019
import re

from resources.lib.comaddon import progress, addon, isMatrix, siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'animeultime'
SITE_NAME = 'Anime Ultime'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'

URL_SEARCH = ('search-0-1+', 'showSeries')
URL_SEARCH_DRAMAS = ('search-drama', 'showSeries')
URL_SEARCH_ANIMS = ('search-anime', 'showSeries')

ANIM_ANIMS = (True, 'showMenuAnimes')
ANIM_ANNEES = (True, 'ShowYearsAnimes')
ANIM_GENRES = (True, 'ShowGenreAnimes')
ANIM_ALPHA = (True, 'ShowAlphaAnimes')

DRAMA_DRAMAS = (True, 'showMenuDramas')
DRAMA_ANNEES = (True, 'ShowYearsDramas')
DRAMA_GENRES = (True, 'ShowGenreDramas')
DRAMA_ALPHA = (True, 'ShowAlphaDramas')

TOKUSATSU_TOKUSATSUS = (True, 'showMenuTokusatsu')
TOKUSATSU = ('series-0-1/tokusatsu/0---', 'showSeries')
TOKUSATSU_ALPHA = ('true', 'ShowAlphaTokusatsu')

adulteContent = addon().getSetting('contenu_adulte')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_DRAMAS[1], 'Dramas', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', TOKUSATSU_TOKUSATSUS[0])
    oGui.addDir(SITE_IDENTIFIER, TOKUSATSU_TOKUSATSUS[1], 'Tokusatsu', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnimes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés  (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuDramas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_ALPHA[1], 'Dramas (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_GENRES[1], 'Dramas (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_ANNEES[1], 'Dramas (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTokusatsu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TOKUSATSU[0])
    oGui.addDir(SITE_IDENTIFIER, TOKUSATSU[1], 'Tokusatsu', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', TOKUSATSU_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, TOKUSATSU_ALPHA[1], 'Tokusatsu (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def loadTypelist(typemovie, typelist):
    # typelist genre ou year
    # <select name="genre"
    # <select name="year"
    sUrl = URL_MAIN + 'series-0-1/' + typemovie

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<select name="([^"]+)|<option value=\'([^\']+).*?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    list_typelist = {}

    if aResult[0]:
        for aEntry in aResult[1]:
            if aEntry[0]:
                if aEntry[0] == typelist:
                    bfind = True
                else:
                    bfind = False

            if bfind and aEntry[1]:
                if not isMatrix():
                    title = aEntry[2].decode('iso-8859-1').encode('utf8')
                else:
                    title = aEntry[2]
                title = title.replace('e', 'E').strip()
                list_typelist[title] = aEntry[1]

    list_typelist = sorted(list_typelist.items(), key=lambda typeList: typeList[0])

    return list_typelist


def ShowGenreAnimes():
    ShowGenre('anime')


def ShowGenreDramas():
    ShowGenre('drama')


def ShowGenre(typemovie):
    oGui = cGui()
    list_listgenre = loadTypelist(typemovie, 'genre')
    oOutputParameterHandler = cOutputParameterHandler()
    for ilist in list_listgenre:
        url = 'series-0-1/' + typemovie + '/-' + ilist[1] + '---'
        sTitle = ilist[0].title()
        oOutputParameterHandler.addParameter('siteUrl', url)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowYearsAnimes():
    ShowYears('anime')


def ShowYearsDramas():
    ShowYears('drama')


def ShowYears(typemovie):
    oGui = cGui()
    list_year = loadTypelist(typemovie, 'year')
    # http://www.anime-ultime.net/series-0-1/anime/--626--    2019
    oOutputParameterHandler = cOutputParameterHandler()
    for liste in reversed(list_year):
        url = 'series-0-1/' + typemovie + '/--' + liste[1] + '--'
        sTitle = liste[0]
        oOutputParameterHandler.addParameter('siteUrl', url)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowAlphaAnimes():
    ShowAlpha('anime')


def ShowAlphaDramas():
    ShowAlpha('drama')


def ShowAlphaTokusatsu():
    ShowAlpha('tokusatsu')


# http://www.anime-ultime.net/series-0-1/anime/c---
def ShowAlpha(typemovie):
    oGui = cGui()

    import string
    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)
    liste = [['#', 'series-0-1/' + typemovie + '/1---']]
    for alpha in listalpha:
        liste.append([str(alpha).upper(), 'series-0-1/' + typemovie + '/' + alpha + '---'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSeries(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    bAnime = bDrama = False
    if sSearch:
        oUtil = cUtil()
        bAnime = URL_SEARCH_ANIMS[0] in sSearch
        bDrama = URL_SEARCH_DRAMAS[0] in sSearch
        sSearchText = sSearch.replace(URL_SEARCH_DRAMAS[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = URL_MAIN + URL_SEARCH[0] + sSearchText.replace(' ', '+').replace('%20', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if sSearch:     # la résultats qui correspondent au type recherché
        sPattern = '<th width="80%">' + ('anime' if bAnime else 'drama')
        sHtmlContent = oParser.abParse(sHtmlContent, sPattern, ' </table>')
        sPattern = '<td class=".+?<a href="([^"]+)".+?<img src=.+?img=([^>]+)\/>.+?onMouseOut.+?>(.+?)<\/a>.+?<td class="" align="center">([^<]+)<'
    else:           # certaines pages ont le contenu en double
        sPattern = '<div id="principal">'
        sHtmlContent = oParser.abParse(sHtmlContent, sPattern, sPattern)
        sPattern = '<td class=".+?<a href="([^"]+)".+?<img src=([^>]+)\/>.+?alt="([^"]+).+?align="center">([^<]+)<'

    aResult = oParser.parse(sHtmlContent, sPattern)

    # Si il y a qu'un seule resultat alors le site fait une redirection.
    if not aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        if sSearch and "sultats anime" not in sHtmlContent:
            sTitle = ''
            try:
                sTitle = re.search('<h1>([^<]+)', sHtmlContent).group(1)
            except:
                pass
            if sTitle:
                sUrl2 = sUrl
                sThumb = ''

                # Enleve le contenu pour adultes.
                if 'Public Averti' in sTitle or 'Interdit' in sTitle:
                    if adulteContent == "false":
                        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Contenu pour adultes désactivé[/COLOR]')
                        return

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                if '/anime/' in sUrl:
                    oGui.addAnime(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)
                else:
                    oGui.addDrama(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

            else:
                oGui.addText(SITE_IDENTIFIER)
        else:
            oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()

        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=True)
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sTitle = aEntry[2]
            if sSearch:
                # Enleve les balise.
                try:
                    sTitle = re.sub('<.*?>', '', sTitle)
                except:
                    pass

            try:
                sTitle = sTitle.decode('iso-8859-1').encode('utf8')
            except:
                pass

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]

            if adulteContent == "false":
                # Enleve le contenu pour adulte.
                if 'Public Averti' in sTitle or 'Interdit' in sTitle:
                    continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sType = aEntry[3].strip()
            sTitle += ' [%s]' % sType

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if sType == 'Film':
                oGui.addMovie(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif bAnime or '/anime/' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addDrama(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()


def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sDesc = ''
    try:
        sPattern = 'src="images.+?(?:<br />)(.+?)(?:<span style|TITRE ORIGINAL|ANNÉE DE PRODUCTION|STUDIO|GENRES)'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('<br>', '').replace('<br />', '')
            sDesc = sDesc.replace('Synopsis', '').replace('synopsis', '').replace(':', ' ')
            sDesc = ('[I][COLOR coral]%s[/COLOR][/I] %s') % ('Synopsis :', sDesc)

            # Enleve les balises.
            try:
                sDesc = re.sub('<.*?>', '', sDesc)
            except:
                pass
    except:
        pass

    sPattern = '<tr.+?align="left">.+?align="left">([^"]+)</td>.+?nowrap>+?<.+?</td>.+?<.+?/td>.+?<.+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        links = set()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[1]
            if sUrl2 in links:
                continue
            links.add(sUrl2)
            
            sTitle = aEntry[0]
            try:
                sTitle = sTitle.decode('iso-8859-1').encode('utf8')
            except:
                pass

            sLang = ''
            if ' vostfr' in sTitle:
                sLang = 'VOSTFR'
            if ' vf' in sTitle:
                sLang = 'VF'
            sTitle = aEntry[0].replace('[', '').replace(']', '').replace('FHD', '').replace('vostfr', '').replace('vf', '').replace('HD', '').replace('HQ', '').strip()
            if '(saison' in sTitle: 
                sTitle = sTitle.replace('(', '').replace(')', '')
            sEpisode = sTitle.split(' ')[-1]
            sTitle = sTitle.replace(sEpisode, ' Episode ' + sEpisode).strip()
            sDisplayTtitle = sTitle + ' [' + sLang + ']'
                

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTtitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id="stream">Streaming <span itemprop="name">([^<]+)<.+?thumbnailUrl" content="([^\"]+)".+?contentURL" content="([^\"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        urls = set()
        for aEntry in aResult[1]:
            sTitle = aEntry[0].strip()
            if ' vostfr' in sTitle:
                sLang = 'VOSTFR'
            if ' vf' in sTitle:
                sLang = 'VF'
            sTitle = ('%s - [%s]') % (sMovieTitle, sLang)
            
            sThumb = aEntry[1]
            sHosterUrl = aEntry[2]
            
            if sHosterUrl in urls:
                continue            # trier les liens en doublon
            urls.add(sHosterUrl)
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
