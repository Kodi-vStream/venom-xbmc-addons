#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
#from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog

import re, urllib2

SITE_IDENTIFIER = 'gum_gum_streaming_com'
SITE_NAME = 'Gum-Gum-Streaming'
SITE_DESC = 'Animés VF/VOSTFR'

URL_MAIN = 'https://gum-gum-streaming.com/'

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

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (A/G)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr2/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (H/N)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr3/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (O/Z)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
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
    sPattern = '<h3 style="color: .+?;">.+? : <a title="([^"]+)" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            #traitement pour affichage de la langue
            sLang = ''
            if '/vf/' in sUrl or '/vostfr/' in sUrl:
                sLang = ''
            elif 'VF' in aEntry[0]:
                sLang = 'VF'
            elif 'VOSTFR' in aEntry[0]:
                sLang = 'VOSTFR'

            sUrl = aEntry[1]
            sTitle = aEntry[0].replace(' VOSTFR', '').replace(' VF', '')
            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)

            sFilter = re.search('(\d+)-(\d+)', sUrl)
            if sFilter:
                continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sites/gum_gum_streaming_com.png', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()

def showAnimes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="menublocks".+?Synopsis:([^"]+)" *href="([^"]+)">([^<]+)</a>.+?data-lazy-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDesc = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]
            sThumb = aEntry[3]

            #traitement du titre pour compatibilite
            sTitle = sTitle.replace('(', ' ').replace(')', ' ')
            sTitle = re.sub('([0-9]+) .. ([0-9\?]+)', '\\1-\\2', sTitle)
            sTitle = re.sub('([0-9]+) & ([0-9\?]+)', '\\1-\\2', sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('><span', '').replace('span></', '')
    sPattern = '<header class="entry-header">(.+?)<footer class="entry-footer">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sUsentContent = aResult[1][0]

    #récupération du synopsis
    sDesc = ''
    sPattern = 'Synopsis:</span>(.+?)</h5>'
    aSynResult = oParser.parse(sUsentContent, sPattern)
    if aSynResult[0]:
        sDesc = aSynResult[1][0]
        sDesc = sDesc.replace('<br />', '').replace('&#8216;', '\'').replace('&#8217;', '\'').replace('&#8230;', '...')

    #récupération du poster
    sThumb = ''
    sPattern = '<h4 style=".+?"><img class="alignright".+?data-lazy-src="(.+?)"'
    sThumbResult = oParser.parse(sUsentContent, sPattern)
    if sThumbResult[0]:
        sThumb = sThumbResult[1][0]

    aSeasonsIdx = [m.start() for m in re.finditer('<h2', sUsentContent)]
    aSeasonsEndIdx = aSeasonsIdx[1:] + [-1]
    aSeasonsTitleEnd = [m.start() for m in re.finditer('</h2>', sUsentContent)]
    for idx, val in enumerate(aSeasonsIdx):
        sSeasonTitle = re.split('>', sUsentContent[val:aSeasonsTitleEnd[idx]])[1]
        oGui.addText(SITE_IDENTIFIER, '[COLOR gold]' + sSeasonTitle + '[/COLOR]', 'sites/gum_gum_streaming_com.png')

        sSeasonContent = sUsentContent[val:aSeasonsEndIdx[idx]]
        aArcIdx = [m.start() for m in re.finditer('<h3>', sSeasonContent)]
        if len(aArcIdx) > 0:
            aArcEndIdx = aArcIdx[1:] + [-1]
            aArcTitleEnd = [m.start() for m in re.finditer('</h3>', sSeasonContent)]
            for idxarc, valarc in enumerate(aArcIdx):
                sArcTitle = re.split('>', sSeasonContent[valarc:aArcTitleEnd[idxarc]])[1]
                oGui.addText(SITE_IDENTIFIER, '[COLOR teal]' + sArcTitle + '[/COLOR]', 'sites/gum_gum_streaming_com.png')

                sArcContent = str(sSeasonContent[valarc:aArcEndIdx[idxarc]])
                sTitlePattern = '>• (.+?)</a>'
                sUrlPattern = 'href="(.+?)"'
                oParser = cParser()
                aTitleResult = oParser.parse(sArcContent, sTitlePattern)
                aUrlResult = oParser.parse(sArcContent, sUrlPattern)
                if aTitleResult[0]:
                    aTitle = aTitleResult[1]
                    aUrl = aUrlResult[1]
                    for sIdx, sTitle in enumerate(aTitle):
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', aUrl[sIdx])
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sDesc', sDesc)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        else:
            sTitlePattern = '>• (.+?)</a>'
            sUrlPattern = 'href="(.+?)"'
            oParser = cParser()
            aTitleResult = oParser.parse(sSeasonContent, sTitlePattern)
            aUrlResult = oParser.parse(sSeasonContent, sUrlPattern)
            if aTitleResult[0]:
                aTitle = aTitleResult[1]
                aUrl = aUrlResult[1]
                for sIdx, sTitle in enumerate(aTitle):
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', aUrl[sIdx])
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'style="width: 280px;"><h2><a title="Synopsis: (.+?)" href="([^"]+)">([^<]+)<.+?data-lazy-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDesc = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]
            sThumb = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if sTitle.lower().find('les films') != -1:
                oGui.addDir(SITE_IDENTIFIER, 'showMovieList', sTitle, 'sites/gum_gum_streaming_com.png', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'sites/gum_gum_streaming_com.png', sThumb, sDesc, oOutputParameterHandler)

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

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="video-container"><iframe.+?data-lazy-src="([^<>"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    VSlog(aResult)

    if 'animedigitalnetwork.fr' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]Animés dispo gratuitement et legalement sur :[/COLOR][COLOR coral] anime digital network[/COLOR]")
    elif 'crunchyroll.com' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]Animés dispo gratuitement et legalement sur :[/COLOR][COLOR coral] crunchyroll[/COLOR]")
    elif 'wakanim.tv' in str(aResult[1]):
        oGui.addText(SITE_IDENTIFIER, "[COLOR red]Animés dispo gratuitement et legalement sur :[/COLOR][COLOR coral] wakanim[/COLOR]")
    else:
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http:' + sHosterUrl

                if 'tinyurl' in sHosterUrl:
                    sHosterUrl = GetTinyUrl(sHosterUrl)

                # if 'goo.gl' in sHosterUrl or 'bit.ly' in sHosterUrl:
                #     try:
                #         import requests
                #         url = sHosterUrl
                #         session = requests.Session()  # so connections are recycled
                #         resp = session.head(url, allow_redirects=True)
                #         sHosterUrl = resp.url
                #     except:
                #         pass


                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
    oGui.setEndOfDirectory()

def GetTinyUrl(url):
    if not 'tinyurl' in url:
        return url

    #Lien deja connu ?
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

    #On va chercher le vrai lien
    else:

        #VSlog('Decodage lien tinyurl : ' + str(url))

        class NoRedirection(urllib2.HTTPErrorProcessor):
            def http_response(self, request, response):
                return response
            https_response = http_response

        headers9 = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'), ('Referer', URL_MAIN)]

        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = headers9
        reponse = opener.open(url, None, 5)

        UrlRedirect = reponse.geturl()

        if not(UrlRedirect == url):
            url = UrlRedirect
        elif 'Location' in reponse.headers:
            url = reponse.headers['Location']

        reponse.close()

    return url
