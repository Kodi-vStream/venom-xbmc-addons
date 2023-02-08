# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'frenchanimes'
SITE_NAME = 'French Animes'
SITE_DESC = 'Mangas en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showAnimes')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showAnimes')
ANIM_MOVIE = (URL_MAIN + 'films-vf-vostfr/', 'showAnimes')
ANIM_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?do=search&mode=advanced&subaction=search&story=', 'showSearch')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showAnimes')
FUNCTION_SEARCH = 'showSearch'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://animes')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE[1], 'Animés (Films)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showAnimes(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sStart = '</span><b>Animes par genre</b></div>'
    sEnd = '<div class="side-b">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sTitle = aEntry[1].capitalize()
            TriAlpha.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle, sUrl in TriAlpha:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showAnimes', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showAnimes(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'mov clearfix.+?src="([^"]*)" *alt="([^"]*).+?link="([^"]+).+?(?:sai">([^<]+[0-9]).+?|)Version'
    sPattern += '.+?desc">([^<]*).+?Synopsis:.+?desc">(.*?)</d'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = aEntry[1].replace(' wiflix', '')
            sUrl = aEntry[2]
            sSaison = aEntry[3].replace('Saison', 'Saison ')
            sLang = aEntry[4]
            sDesc = str(aEntry[5])

            # la langue est parfois dans le titre
            if sLang in sTitle:
                sTitle = sTitle.replace(sLang, '')

            sDisplaytitle = '%s %s (%s)' % (sTitle, sSaison, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'films-vf-vostfr' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showAnimes', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a> *</span>.*?<span class="pnext"><a href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sStart = 'class="eps" style="display: none">'
    sEnd = '/div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # Pour les liens myvi
    sHtmlContent = sHtmlContent.replace('!//', '!https://').replace(',//', ',https://')
    
    # Besoin des saut de ligne
    sHtmlContent = sHtmlContent.replace('\n', '@')

    sPattern = '([0-9]+)!|(https:.+?)[,|<@]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ep = 0

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                ep = 'Episode ' + aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + ep + '[/COLOR]')
            if aEntry[1]:
                sTitle = sMovieTitle + ' ' + ep
                sHosterUrl = aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'class="eps" style="display: none">'
    sEnd = '/div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # Pour les liens myvi
    sHtmlContent = sHtmlContent.replace('!//', '!https://').replace(',//', ',https://')

    sPattern = '(https:.+?)[,|<]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
