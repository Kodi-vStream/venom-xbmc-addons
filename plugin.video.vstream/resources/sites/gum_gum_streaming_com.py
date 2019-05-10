#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
#from resources.lib.util import cUtil
from resources.lib.comaddon import progress

import re

SITE_IDENTIFIER = 'gum_gum_streaming_com'
SITE_NAME = 'Gum-Gum-Streaming'
SITE_DESC = 'Animés VF/VOSTFR'

URL_MAIN = 'https://gum-gum-streaming.com/'

ANIM_NEWS = (URL_MAIN, 'showNews')
ANIM_ANIMS = (URL_MAIN, 'showNews')
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
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (A/M)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'https://gum-gum-streaming.com/vostfr2/')
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR) (N/Z)', 'vostfr.png', oOutputParameterHandler)

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

    sPattern = '<h3 style="color: .+?;">.+? : <a title="([^"]+)" href="(.+?)">.+?</a>'
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

            filter = re.search('(\d+)-(\d+)', sUrl)
            if filter:
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

    #sPattern = '<h2 style="text-align: center;"><a href="([^"]+)">(.+?)</a>'
    sPattern = 'class="menublocks".+?href="([^"]+)">([^<]+)</a>.+?src="([^"]+)"'
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
            sThumb = aEntry[2]

            #traitement du titre pour compatibilite
            sTitle = sTitle.replace('(', ' ').replace(')', ' ')#.replace('-', ' ')
            sTitle = re.sub('([0-9]+) .. ([0-9\?]+)', '\\1-\\2', sTitle)
            sTitle = re.sub('([0-9]+) & ([0-9\?]+)', '\\1-\\2', sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'anim.png', sThumb, '', oOutputParameterHandler)
        progress_.VSclose(progress_)
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('><span', '').replace('span></', '')

    oParser = cParser()
    sPattern = '<header class="entry-header">(.+?)<footer class="entry-footer">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sUsentContent = aResult[1][0]

    #récupération du synopsis
    sDesc = ''
    sPattern = 'Synopsis:</span>(.+?)</h5>'
    aSynResult = oParser.parse(sUsentContent, sPattern)
    if aSynResult[0]:
        sDesc = aSynResult[1][0]
        sDesc = sDesc.replace('<br />', '').replace('&#8217;', '\'').replace('&#8230;', '...')

    #récupération du poster
    sThumb = ''
    sPattern = '<h4 style=".+?"><img class="alignright".+?src="(.+?)"'
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

    sPattern = '<h2 style="text-align: center;"><a href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if sTitle.lower().find('les films') != -1:
                oGui.addDir(SITE_IDENTIFIER, 'showMovieList', sTitle, 'sites/gum_gum_streaming_com.png', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'sites/gum_gum_streaming_com.png', '', '', oOutputParameterHandler)

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
    sPattern = '<div class="video-container"><iframe.+?src="([^<>"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

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
