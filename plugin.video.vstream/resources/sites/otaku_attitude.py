#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Makoto
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress#, VSlog

import re

SITE_IDENTIFIER = 'otaku_attitude'
SITE_NAME = 'Otaku-Attitude'
SITE_DESC = 'Animes, Drama et OST en DDL et Streaming'

URL_MAIN = 'http://www.otaku-attitude.net/'
OST_MAIN = 'https://forum.otaku-attitude.net/musicbox/playlists/'

URL_SEARCH_SERIES = (URL_MAIN + 'recherche.html?cat=1&q=', 'showSeries')
URL_SEARCH_DRAMAS = (URL_MAIN + 'recherche.html?cat=2&q=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'

ANIM_ANIMS = ('http://', 'load')
ANIM_VOSTFRS  = (URL_MAIN + 'liste-dl-animes.php', 'showSeries')

SERIE_SERIES = ('http://', 'load')
DRAMAS = (URL_MAIN + 'liste-dl-dramas.php', 'showSeries')

OST_ANIME =(True, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animés)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Dramas)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS [0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS [1], 'Animés (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMAS[1], 'Dramas (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', OST_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, OST_ANIME[1], 'Musicbox (OST)', 'music.png',  oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Animés', OST_MAIN + '1-anime/'] )
    liste.append( ['Dramas', OST_MAIN + '6-drama/'] )
    liste.append( ['Jeux Vidéo', OST_MAIN + '7-jeu-vidéo/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showOst', sTitle, 'music.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText.replace(' ', '+')
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    #On memorise le liens de base ce qui permets d'avoir un next page fonctionnel sans modif et peut importe la categorie
    if not sSearch:
        if not 'scroll' in sUrl:
            MemorisedUrl = sUrl
            Page = 1
        else:
            MemorisedUrl = oInputParameterHandler.getValue('MemorisedUrl')
            Page = oInputParameterHandler.getValue('Page')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    if sSearch:
        sPattern = '<a href="([^"]+)" class="liste_dl"><img src="([^"]+)".+?alt=".+?strong>([^<]+)<.+?all">([^<]+)</.+?>'
    else:
        sPattern = 'href="([^"]+)".+?><img src="([^"]+)".+?alt=".+?strong>([^<]+)<.+?all">([^<]+)<br.+?>'

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

            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2].replace('-...', '').replace('...', '').replace('!', ' !')
            sDesc = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        Page = int(Page) + 1
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', MemorisedUrl + '?&scroll=' + str(Page))
        #On renvoi l'url memoriser et le numero de page pour l'incrementer a chaque fois
        oOutputParameterHandler.addParameter('MemorisedUrl', MemorisedUrl)
        oOutputParameterHandler.addParameter('Page', Page)
        oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showOst():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if not 'page' in sUrl:
        MemorisedUrl = sUrl
        Page = 1
    else:
        MemorisedUrl = oInputParameterHandler.getValue('MemorisedUrl')
        Page = oInputParameterHandler.getValue('Page')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "<div class='plWrapper'>.+?href='([^']+)' title='([^']+)'.+?src=\"([^\"]+)\""
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

            sUrl2 = aEntry[0]
            sTitle = aEntry[1].replace('- Artiste non défini', '')
            sThumb = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showMusic', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        Page = int(Page) + 1
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', MemorisedUrl + '?page=' + str(Page))
        #On renvoi l'url memoriser et le numero de page pour l'incrementer a chaque fois
        oOutputParameterHandler.addParameter('MemorisedUrl', MemorisedUrl)
        oOutputParameterHandler.addParameter('Page', Page)
        oGui.addNext(SITE_IDENTIFIER, 'showOst', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #On recupere l'id de l'anime dans l'url
    serieID = re.search('fiche-.+?-(\d+)-.+?.html', sUrl).group(1)
    sPattern = 'class="(?:download cell_impaire|download)" id="([^"]+)".+?(\d+).+?class="cell".+?>([^<]+)</td'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in sorted(aResult[1], key=lambda aResult: aResult[1]):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sQual = aEntry[2]
            #Changemement de formats ...x... -> ....P
            if '1920×' in sQual or '1440×' in sQual or '1904×' in sQual:
                sQual = re.sub('(\d+×\d+)px', '[1080P]', sQual)
            elif '1728×' in sQual:
                sQual = re.sub('(\d+×\d+)px', '[800P]', sQual)
            elif '1280×' in sQual:
                # VSlog(sQual)
                sQual = re.sub('(\d+×\d+)px', '[720P]', sQual)
            elif '1024×' in sQual:
                sQual = re.sub('(\d+×\d+)px', '[600P]', sQual)
            elif '480×' in sQual:
                sQual = re.sub('(\d+×\d+)px', '[360P]', sQual)
            else:
                sQual = re.sub('(\d+×\d+)px', '[480P]', sQual)

            sTitle = 'E' + aEntry[1] + ' ' + sMovieTitle + ' ' + sQual
            idEpisode = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('serieID',serieID)
            oOutputParameterHandler.addParameter('idEpisode', idEpisode)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showMusic():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div data-track-file="([^"]+)".+?data-track-name="([^"]+)".+?"><span.+?>([^<]+)</span>'
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

            sTitle = aEntry[2] + ' ' + aEntry[1]
            mp3Url = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('mp3Url', mp3Url)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showMp3', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showMp3():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    mp3Url = oInputParameterHandler.getValue('mp3Url')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'mp3' in mp3Url:
        sHosterUrl = mp3Url

    oHoster = cHosterGui().checkHoster('m3u8')
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, mp3Url, sThumb)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    serieID = oInputParameterHandler.getValue('serieID')
    idEpisode = oInputParameterHandler.getValue('idEpisode')

    if 'fiche-anime' in sUrl:
        sHosterUrl = URL_MAIN + 'launch-download-1-' + serieID + '-ddl-' + idEpisode + '.html'
    elif 'fiche-drama' in sUrl:
        sHosterUrl = URL_MAIN + 'launch-download-2-' + serieID + '-ddl-' + idEpisode + '.html'

    oHoster = cHosterGui().checkHoster('m3u8')
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
