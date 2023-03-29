# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.comaddon import progress  # , VSlog
import re
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
return False


SITE_IDENTIFIER = 'monde_des_cartoons'
SITE_NAME = 'Le monde des cartoons'
SITE_DESC = 'dessins animés en streaming 720P'

URL_MAIN = 'https://monde-des-cartoons.blogspot.com/'

ANIM_ENFANTS = ('http://', 'load')
ANIM_LISTE = (URL_MAIN, 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LISTE[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LISTE[1], 'Liste des cartoons', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-original-height=".+?" data-original-width=".+?" src="([^"]+).+?center;">.+?;">([^<]+).+?var x="([^"]+)".+?="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0]):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2]
            sUrl2 = aEntry[3]
            sThumb = aEntry[0]
            sDesc = re.sub('&#.+?;', '', aEntry[1].replace('&#39;', "'").replace('&#8217;', "'"))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<td><a href="([^"]+)".+?>([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = ('%s [%s]') % (sMovieTitle, aEntry[1].replace('<br />', ' : ').replace('&#9830;', ''))
            sUrl2 = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Utilisation de re car avec le parser de Vstream il ne veux pas prendre correctement le 'vostfr'
    aResult = re.findall('<img.+?src=".+?/_(?:0001|0002)_(.+?).png|<iframe.+?src="([^"]+)"', str(sHtmlContent))

    if (aResult):
        for aEntry in aResult:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0].upper() + '[/COLOR]')
            else:
                sHosterUrl = aEntry[1]
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'https:' + sHosterUrl
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
