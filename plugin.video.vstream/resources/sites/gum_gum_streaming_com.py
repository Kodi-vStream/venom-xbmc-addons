#-*- coding: utf-8 -*-
# Norton-breman

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
#from resources.lib.util import cUtil

import xbmc, re

SITE_IDENTIFIER = 'gum_gum_streaming_com'
SITE_NAME = 'Gum-Gum-Streaming'
SITE_DESC = 'Animés VF/VOSTFR'

URL_MAIN = 'http://gum-gum-streaming.com/'

ANIM_NEWS = (URL_MAIN, 'showNews')
ANIM_ANIMS = (URL_MAIN, 'showNews')
ANIM_VFS = (URL_MAIN + 'vf', 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + 'vostfr', 'showAnimes')
ANIM_MOVIES = (URL_MAIN + 'films', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    #oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'animes_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIES[1], 'Films', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showNews():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h3 style="color: .+?;">.+? : <a title="([^"]+)" href="(.+?)">.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[1]
            filter = re.search('(\d+)-(\d+)', sUrl)
            if filter:
                continue
            sTitle = aEntry[0]
            #sTitle = cUtil().removeHtmlTags(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, 'sites/gum_gum_streaming_com.png', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
    oGui.setEndOfDirectory()

def showAnimes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h2 style="text-align: center;"><a href="([^"]+)">(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sTitle = str(aEntry[1])
            #sTitle = cUtil().removeHtmlTags(sTitle)
            sUrl = str(aEntry[0])

            #traitement du titre pour compatibilite
            sTitle = sTitle.replace('(',' ').replace(')',' ').replace('-',' ')
            sTitle = re.sub('([0-9]+) .. ([0-9\?]+)','\\1-\\2',sTitle)
            sTitle = re.sub('([0-9]+) & ([0-9\?]+)','\\1-\\2',sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            # oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'anime.png', oOutputParameterHandler)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, 'sites/gum_gum_streaming_com.png', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
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

    sSyn = ''
    sPattern = 'Synopsis:.+? ([^<]+)</h5>'
    aSynResult = oParser.parse(sUsentContent, sPattern)
    if aSynResult[0]:
        sSyn = aSynResult[1][0]

    sThumb = ''
    sPattern = '<h4 style=".+?"><img class="alignright" src="(.+?)"'
    sThumbResult = oParser.parse(sUsentContent, sPattern)
    if sThumbResult[0]:
        sThumb = sThumbResult[1][0]

    aSeasonsIdx = [m.start() for m in re.finditer('<h2', sUsentContent)]
    aSeasonsEndIdx = aSeasonsIdx[1:] + [-1]
    aSeasonsTitleEnd = [m.start() for m in re.finditer('</h2>', sUsentContent)]
    for idx, val in enumerate(aSeasonsIdx):
        sSeasonTitle = re.split('>', sUsentContent[val:aSeasonsTitleEnd[idx]])[1]
        oGui.addText(SITE_IDENTIFIER, '[COLOR gold]' + sSeasonTitle + '[/COLOR]', sThumb)

        sSeasonContent = sUsentContent[val:aSeasonsEndIdx[idx]]
        aArcIdx = [m.start() for m in re.finditer('<h3>', sSeasonContent)]
        if len(aArcIdx) > 0:
            aArcEndIdx = aArcIdx[1:] + [-1]
            aArcTitleEnd = [m.start() for m in re.finditer('</h3>', sSeasonContent)]
            for idxarc, valarc in enumerate(aArcIdx):
                sArcTitle = re.split('>', sSeasonContent[valarc:aArcTitleEnd[idxarc]])[1]
                oGui.addText(SITE_IDENTIFIER, '[COLOR teal]' + str(sArcTitle) + '[/COLOR]', sThumb)

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
                        #sDisplayTitle = cUtil().DecoTitle(sTitle)
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', aUrl[sIdx])
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sDesc', sSyn)
                        oOutputParameterHandler.addParameter('sThumbnail', sThumb)
                        oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sSyn, oOutputParameterHandler)

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
                    #sDisplayTitle = cUtil().DecoTitle(sTitle)
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', aUrl[sIdx])
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sDesc', sSyn)
                    oOutputParameterHandler.addParameter('sThumbnail', sThumb)
                    # oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sSyn, oOutputParameterHandler)
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sSyn, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h2 style="text-align: center;"><a href="([^"]+)">(.+?)</a></h2>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sTitle = str(aEntry[1])
            sUrl = str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if sTitle.lower().find('les films') != -1:
                oGui.addDir(SITE_IDENTIFIER, 'showMovieList', sTitle, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
    oGui.setEndOfDirectory()

def showMovieList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a title=".+?" href="([^"]+)">(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sTitle = str(aEntry[1])
            sUrl = str(aEntry[0])
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = '<div class="video-container"><iframe.+?src="([^<>"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)


    if (aResult[0] == True):
        for aEntry in aResult[1]:
            #xbmc.log(aEntry)
            sHosterUrl = str(aEntry)
            if not sHosterUrl.startswith('http:') and not sHosterUrl.startswith('https:'):
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
