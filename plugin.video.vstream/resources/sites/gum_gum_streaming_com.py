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
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'gum_gum_streaming_com'
SITE_NAME = 'Gum-Gum-Streaming'
SITE_DESC = 'Animés VF/VOSTFR'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = ('showNews')
ANIM_VFS = ('vf/', 'showAnimes')
ANIM_VOSTFRS = ('vostfr/', 'showMenuVOSTFR')
ANIM_MOVIES = ('films/', 'showAnimes')

URL_SEARCH_ANIMS = ('?s=', 'showAnimes')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr1/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (A-F)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr2/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (G-L)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr3/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (M-R)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr4/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (S-Z)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIES[1], 'Films', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuVOSTFR():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'vostfr1/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (A-F)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr2/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (G-L)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr3/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (M-R)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'vostfr4/')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Animés (VOSTFR) (S-Z)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showAnimes(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showNews():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # desc url thumb title
    sPattern = '<a class="fleft" title="Synopsis: (.+?)" href="([^"]+)".+?src="([^&]+).+?link="internal">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sDesc = aEntry[0].replace('=""', '').replace('"="', '')
            sUrl = aEntry[1]
            sThumb = aEntry[2]
            sTitle = aEntry[3]

            # traitement pour affichage de la langue
            sLang = ''
            if 'VF' in sTitle or 'vf' in sTitle:
                sLang = 'VF'
            elif 'VOSTFR' in sTitle:
                sLang = 'VOSTFR'

            sTitle = sTitle.replace(' VOSTFR', '').replace(' VF', '').replace(' vf', '')
            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)

            # sFilter = re.search('(\d+)-(\d+)', sUrl)
            # if sFilter:
            #     continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addLink(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimes(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    bFilm = False
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.split('=')[1].replace('%20', ' ')
        sUrl = URL_MAIN + sSearch
        sPattern = '<header class="entry-header"><h2 class="entry-title"><a href="([^"]+)" data-wpel-link="internal">([^<]+)'        
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
        bFilm = '/films/' in sUrl
        sPattern = 'Synopsis:([^"]+)" href="([^"]+).+?">([^<]+).+?data-lazy-src="([^"]+)'
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sThumb = ''
        sDesc = ''
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=True)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch:
                sUrl = aEntry[0]
                if '-film-' in sUrl:
                    continue
                sTitle = aEntry[1]
            else:
                sDesc = aEntry[0]
                sUrl = aEntry[1]
                sTitle = aEntry[2]
                sThumb = aEntry[3]

            sLang = sTitle.split(' ')[-1]
            if sLang in ['VF', 'VOSTFR']:
                sTitle = sTitle.replace(sLang, '')
            else:
                sLang = ''

            # traitement du titre pour compatibilite
            sTitle = sTitle.replace(', le Film', '')
            sTitle = sTitle.replace('(', ' - ').replace(')', ' ')
            sTitle = re.sub('([0-9]+) .. ([0-9\?]+)', '\\1-\\2', sTitle)
            sTitle = re.sub('([0-9]+) & ([0-9\?]+)', '\\1-\\2', sTitle)

            bList = ', les Films' in sTitle
            sTitle = sTitle.replace(', les Films', '')

            if sSearch: # Filtre de recherche
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue
            if sLang:
                sTitle = '%s (%s)' % (sTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sLang', sLang)

            if bFilm:
                if bList:
                    oGui.addMovie(SITE_IDENTIFIER, 'showMovieList', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSerieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

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
    sPattern = '<h4 style=".+?"><img class="alignright".+?data-lazy-src="(.+?)"'
    sThumbResult = oParser.parse(sUsentContent, sPattern)
    if sThumbResult[0]:
        sThumb = sThumbResult[1][0]

    sPattern = '<h2 style="color: #.+?">([^<]+)|href="http([^"]+)".+?>([^<]+)<\/a>'
    aResult = oParser.parse(sUsentContent, sPattern)

    if aResult[0]:
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

                oOutputParameterHandler.addParameter('siteUrl', aUrl)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                if 'Film' in sSaison:
                    sDisplayTitle = re.sub('Film \d+:', '', sDisplayTitle)
                    sDisplayTitle = sDisplayTitle + " - " + sSerieTitle
                    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                    oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # NONE    hostName    urlHost
    sPattern = 'color: (#00ccff;"|#00ff00;")>([^<]+).+?data-lazy-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    bLang = True

    if not aResult[0]:
        sPattern = '"fitvidscompatible" data-lazy-src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        bLang = False

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if bLang:
                sHosterUrl = aEntry[2]
                sHost, sLang = aEntry[1].split(' ')
            else:
                sHosterUrl = aEntry
                sLang = ''
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if not oHoster:
                continue
            
            sDisplayTitle = sTitle
            if sLang:
                sDisplayTitle += ' (%s)' % sLang
            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            # if sTitle.lower().find('les films') != -1:
            #     oGui.addMovie(SITE_IDENTIFIER, 'showMovieList', sDisplayTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
            # else:
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl)

    oGui.setEndOfDirectory()


def showMovieList():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # url    title
#    sPattern = '<h2 style="text-align: center;"><a[^<]+href="([^"]+)" data-wpel-link="internal">([^<]+)'
    sPattern = '<a[^<]+href="([^"]+)" data-wpel-link="internal">([^<]+)<\/a>(<br \/>|<\/h2)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sDisplayTitle = sTitle = aEntry[1].replace('•', '')
            
            epTitle = re.sub('Film \d+:', '', sTitle)
            if len(epTitle.replace(' ', ''))==0:
                sDisplayTitle = sTitle + ' ' + sMovieTitle
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', '', '', oOutputParameterHandler)

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
        oGui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] anime digital network[/COLOR]", 'animes.png')
    elif 'crunchyroll.com' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] crunchyroll[/COLOR]", 'animes.png')
    elif 'wakanim.tv' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, sTexte + "[COLOR coral] wakanim[/COLOR]", 'animes.png')
    else:
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http:' + sHosterUrl

                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = GetTinyUrl(sHosterUrl)

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
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
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.request()
        UrlRedirect = oRequestHandler.getRealUrl()

        if not(UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in oRequestHandler.getResponseHeader():
            url = oRequestHandler.getResponseHeader()['Location']

    return url
