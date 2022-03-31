# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'youtitou_com'
SITE_NAME = 'YouTitou'
SITE_DESC = 'Plus de 900 dessins animés gratuits classés par âge'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ENFANTS = ('http://', 'load')

AGE_2A4ANS = (URL_MAIN + 'pages/dessins-animes-2-a-4-ans/jolies-histoires-pour-enfants-de-2-a-4-ans.html', 'showMovies')
VIDEO_EDU2_4 = (URL_MAIN + 'pages/dessins-animes-2-a-4-ans/videos-educatives-pour-enfant-de-2-a-4-ans.html', 'showEdu')

AGE_4A6ANS = (URL_MAIN + 'pages/dessins-animes-4-a-6-ans/dessins-animes-pour-enfants-de-4-a-6-ans.html', 'showMovies')
VIDEO_EDU4_6 = (URL_MAIN + 'pages/dessins-animes-4-a-6-ans/videos-educatives-pour-enfants-de-4-a-6-ans.html', 'showEdu')

AGE_6A8ANS = (URL_MAIN + 'pages/dessins-animes-6-a-8-ans/dessins-animes-pour-enfants-de-6-a-8-ans.html', 'showMovies')
VIDEO_EDU6_8 = (URL_MAIN + 'pages/dessins-animes-6-a-8-ans/videos-educatives-pour-enfants-de-6-a-8-ans.html', 'showEdu')

COMPIL = (URL_MAIN + 'videos/compilations-longues/', 'showEpisode')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', AGE_2A4ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_2A4ANS[1], 'Dessins animés 2 à 4 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', VIDEO_EDU2_4[0])
    oGui.addDir(SITE_IDENTIFIER, VIDEO_EDU2_4[1], 'Vidéos éducative 2 à 4 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', AGE_4A6ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_4A6ANS[1], 'Dessins animés 4 à 6 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', VIDEO_EDU4_6[0])
    oGui.addDir(SITE_IDENTIFIER, VIDEO_EDU4_6[1], 'Vidéos éducative 4 à 6 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', AGE_6A8ANS[0])
    oGui.addDir(SITE_IDENTIFIER, AGE_6A8ANS[1], 'Dessins animés 6 à 8 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', VIDEO_EDU6_8[0])
    oGui.addDir(SITE_IDENTIFIER, VIDEO_EDU6_8[1], 'Vidéos éducative 6 à 8 ans', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', COMPIL[0])
    oGui.addDir(SITE_IDENTIFIER, COMPIL[1], 'Compilation dessins animés', 'enfants.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtml = oRequestHandler.request()
    sPattern = '<p style="text-align: center;"><a href="(http.//www.youtitou.com/videos.+?)">.+?<img.+?src="([^"]+)'
    aResult = oParser.parse(sHtml, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            if sUrl.endswith('//'):
                sUrl = sUrl[:-1]

            sThumb = aEntry[1]
            sTitle = sUrl.rsplit('/', 2)[1]  # on prend le titre de l'url plus fiable site bordelique

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showEpisode', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtml = oRequestHandler.request()
    sPattern = 'class="media-object">.+?href="(http.//www.youtitou.com/videos.+?)".+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtml, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if sUrl.endswith('//'):
                sUrl = sUrl[:-1]

            sThumb = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, 'enfants.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="(.+?)".+?</iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'https:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showEdu():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h2 class="row-title">(.+?)</h2>.+?<iframe.+?src="([^"]+)".+?</iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        sPattern = '<iframe title="([^"]+)".+?src="([^"]+)".+?</iframe>'  # pas de titre 6_8
        aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry[1]
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'https:' + sHosterUrl

            sId = sHosterUrl.rsplit('/', 1)[1]
            sTitle = aEntry[0]
            sThumb = 'https://i.ytimg.com/vi/' + sId + '/mqdefault.jpg'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
