# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

import re

SITE_IDENTIFIER = 'gum_gum_streaming_com'
SITE_NAME = 'Gum-Gum-Streaming'
SITE_DESC = 'Animés VF/VOSTFR'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = 'https://gum-gum-streaming.co/'  # sans pub

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showNews')
ANIM_VFS = (URL_MAIN + 'vf/', 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + 'vostfr/', 'showAnimes')
ANIM_MOVIES = (URL_MAIN + 'films/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr1/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (A-F)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr2/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (G-L)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr3/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (M-R)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr4/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (S-Z)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIES[1], 'Films', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showNews():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sPattern = 'Dernier (VF|VOSTFR|OAV|Film)\s*: (?:<a |<a title="([^"]+)" )href="([^"]+)" data-wpel-link="internal">([^<]+)'
    sPattern = 'Dernier (VF|VOSTFR|OAV|Film)\s*: (<a|<a title="([^"]+)") href="([^"]+)" data-wpel-link="internal">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '' == aEntry[2]:  # titre absent donc on le recup dans l'url
                sNum = aEntry[4]
                sTitle = re.sub(URL_MAIN, '', aEntry[3])
                sTitle = sTitle.replace('-', ' ')[:-1] + ' ' + sNum.replace('N°', 'E')
                sUrl = aEntry[3]
            else:
                sTitle = aEntry[2]
                sUrl = aEntry[3]

            # traitement pour affichage de la langue
            sLang = ''
            if 'VF' in sTitle or 'vf' in sTitle:
                sLang = 'VF'
            elif 'VOSTFR' in sTitle:
                sLang = 'VOSTFR'

            sTitle = sTitle.replace(' VOSTFR', '').replace(' VF', '').replace(' vf', '')
            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)

            sFilter = re.search('(\d+)-(\d+)', sUrl)
            if sFilter:
                continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'Synopsis:([^"]+)" href="([^"]+).+?">([^<]+).+?data-lazy-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=True)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDesc = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]
            sThumb = aEntry[3]

            # traitement du titre pour compatibilite
            sTitle = sTitle.replace('(', ' ').replace(')', ' ')
            sTitle = re.sub('([0-9]+) .. ([0-9\?]+)', '\\1-\\2', sTitle)
            sTitle = re.sub('([0-9]+) & ([0-9\?]+)', '\\1-\\2', sTitle)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSerieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('><span', '').replace('span></', '')
    sPattern = '<header class="entry-header">(.+?)<footer class="entry-footer">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sUsentContent = aResult[1][0]

    # récupération du synopsis
    sDesc = ''
    sPattern = 'Synopsis:</span>(.+?)</h5>'
    aSynResult = oParser.parse(sUsentContent, sPattern)
    if aSynResult[0]:
        sDesc = aSynResult[1][0]
        sDesc = sDesc.replace('<br />', '').replace('&#8216;', '\'')

    # récupération du poster
    sThumb = ''
    sPattern = '<h4 style=".+?"><img class="alignright".+?data-lazy-src="(.+?)"'
    sThumbResult = oParser.parse(sUsentContent, sPattern)
    if sThumbResult[0]:
        sThumb = sThumbResult[1][0]

    sPattern = '<h2 style="color: #.+?">([^<]+)|href="http([^"]+)".+?>([^<]+)<\/a>'
    aResult = oParser.parse(sUsentContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        sSaison = ''
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sSaison + '[/COLOR]')
                if ':' in sSaison:
                    sSaison = sSaison[:sSaison.index(':')]
                sSaison = sSaison.capitalize().strip()
            else:
                aUrl = 'http' + aEntry[1]
                sDisplayTitle = aEntry[2].replace('•', '').strip()
                if sDisplayTitle.endswith(':'):
                    sDisplayTitle = sDisplayTitle[:-1]
                
                sTitle = sSerieTitle + ' ' + sDisplayTitle 

                oOutputParameterHandler.addParameter('siteUrl', aUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'style="width: 280px;"><h2><a title="Synopsis: (.+?)" href="([^"]+).+?>([^<]+).+?data-lazy-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=True)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDesc = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]
            sThumb = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if sTitle.lower().find('les films') != -1:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieList', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()


def showMovieList():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a title=".+?" href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="video-container"> ?<iframe.+?data-lazy-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTexte = "[COLOR red]Animés dispo gratuitement et légalement sur :[/COLOR]"
    if 'animedigitalnetwork.fr' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] anime digital network[/COLOR]")
    elif 'crunchyroll.com' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] crunchyroll[/COLOR]")
    elif 'wakanim.tv' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] wakanim[/COLOR]")
    else:
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http:' + sHosterUrl

                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = GetTinyUrl(sHosterUrl)

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
    oGui.setEndOfDirectory()


def GetTinyUrl(url):
    if 'tinyurl' not in url:
        return url

    # Lien deja connu ?
    if '://tinyurl.com/h7c9sr7' in url:
        url = url.replace('://tinyurl.com/h7c9sr7/', '://vidwatch.me/')
    elif '://tinyurl.com/jxblgl5' in url:
        url = url.replace('://tinyurl.com/jxblgl5/', '://streamin.to/')
    elif '://tinyurl.com/q44uiep' in url:
        url = url.replace('://tinyurl.com/q44uiep/', '://openload.co/')
    elif '://tinyurl.com/jp3fg5x' in url:
        url = url.replace('://tinyurl.com/jp3fg5x/', '://allmyvideos.net/')
    elif '://tinyurl.com/kqhtvlv' in url:
        url = url.replace('://tinyurl.com/kqhtvlv/', '://openload.co/embed/')
    elif '://tinyurl.com/lr6ytvj' in url:
        url = url.replace('://tinyurl.com/lr6ytvj/', '://netu.tv/')
    elif '://tinyurl.com/kojastd' in url:
        url = url.replace('://tinyurl.com/kojastd/', '://www.rapidvideo.com/embed/')
    elif '://tinyurl.com/l3tjslm' in url:
        url = url.replace('://tinyurl.com/l3tjslm/', '://hqq.tv/player/')
    elif '://tinyurl.com/n34gtt7' in url:
        url = url.replace('://tinyurl.com/n34gtt7/', '://vidlox.tv/')
    elif '://tinyurl.com/kdo4xuk' in url:
        url = url.replace('://tinyurl.com/kdo4xuk/', '://watchers.to/')
    elif '://tinyurl.com/kjvlplm' in url:
        url = url.replace('://tinyurl.com/kjvlplm/', '://streamango.com/')
    elif '://tinyurl.com/kt3owzh' in url:
        url = url.replace('://tinyurl.com/kt3owzh/', '://estream.to/')

    # On va chercher le vrai lien
    else:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.disableRedirect(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        reponse = oRequestHandler.request()
        UrlRedirect = reponse.GetRealUrl()

        if not(UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.getResponseHeader():
            url = reponse.getResponseHeader()['Location']

    return url
