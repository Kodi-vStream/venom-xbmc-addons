# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'skyanimes'
SITE_NAME = 'Sky-Animes'
SITE_DESC = 'Animés, Dramas en Direct Download'

URL_MAIN = 'http://www.sky-animes.com/'

STREAM = 'index.php?file=Media&nuked_nude=index&op=do_dl&dl_id='

URL_SEARCH_ANIMS = (URL_MAIN + 'index.php?file=Search&op=mod_search&searchtype=matchand&autor=&module=Download&limit=100&main=', 'showEpisode')
FUNCTION_SEARCH = 'showEpisode'

ANIM_VOSTFRS = (URL_MAIN + '', 'showMenuAnims')
ANIM_GENRES = (True, 'showGenresA')

DRAMA_VOSTFRS = (URL_MAIN + '', 'showMenuDramas')
DRAMA_GENRES = (True, 'showGenresD')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DRAMA_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_VOSTFRS[1], 'Dramas', 'dramas.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnims():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    liste = []
    liste.append(['En Cours', URL_MAIN + 'streaming-animes-en-cours?p=-1'])
    liste.append(['Terminés', URL_MAIN + 'download-animes-termines?p=-1'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuDramas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DRAMA_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_GENRES[1], 'Dramas (Genres)', 'genres.png', oOutputParameterHandler)

    liste = []
    liste.append(['En Cours', URL_MAIN + 'download-dramas-en-cours?p=-1'])
    liste.append(['Terminés', URL_MAIN + 'download-dramas-termines?p=-1'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'dramas.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenresA():
    oGui = cGui()
    oParser = cParser()

    sUrl = URL_MAIN + 'streaming-animes-en-cours'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = 'id="id_genre"'
    sEnd = '<select id="triGenre"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showGenresD():
    oGui = cGui()
    oParser = cParser()

    sUrl = URL_MAIN + 'download-dramas-en-cours?p=-1'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = 'id="id_genre"'
    sEnd = '<select id="triGenre"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText.replace(' ', '+')
        showEpisode(sUrl)
        oGui.setEndOfDirectory()
        return


def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('+', '%2B').replace('é', 'e').replace('ô', 'o')\
                                                     .replace('É', 'E').replace('ï', 'i').replace('è', 'e')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^"]+)"><img src="([^"]+)" width.+?alt="([^"]+).+?></a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2]
            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1].replace(' ', '%20')
            sDesc = ''

            sTitle = sTitle.replace(', telecharger en ddl', '')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '-animes-' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()


def showEpisode(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    if sSearch:
        sPattern = '<a href=".+?id=([^"]+)"><b>(.+?)</b>'
    else:
        sPattern = '<td style="padding-left: 12px;"><a href="([^"]+).+?><b><img.+?>(.+?)</b>.+?</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in sorted(aResult[1]):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch:
                sTitle = aEntry[1]
                sTitle, sTitle1 = sTitle.replace('1080p', '').replace('BD', '').replace('V2', '').replace('FIN', '')\
                                       .replace('Fin', '').replace('fin', '').replace('OAV', '').replace('Bluray', '')\
                                       .replace('Blu-Ray', '').rstrip().rsplit(' ', 1)
                sTitle = 'E' + sTitle1 + ' ' + sTitle
                sUrl2 = URL_MAIN + STREAM + aEntry[0]
                sThumb = ''
            else:
                sTitle = aEntry[1]
                sTitle, sTitle1 = sTitle.replace('1080p', '').replace('BD', '').replace('V2', '').replace('FIN', '')\
                                        .replace('Fin', '').replace('fin', '').replace('OAV', '').replace('Bluray', '')\
                                        .replace('Blu-Ray', '').rstrip().rsplit(' ', 1)
                sTitle = 'E' + sTitle1 + ' ' + sTitle
                sUrl2 = URL_MAIN + STREAM + aEntry[0]
                sUrl2 = sUrl2.replace('#', '')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
    if not sSearch:
        oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster('m3u8')

    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

    oGui.setEndOfDirectory()
