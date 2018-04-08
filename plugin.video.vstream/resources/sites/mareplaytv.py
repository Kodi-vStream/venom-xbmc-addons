#-*- coding: utf-8 -*-
#Venom.
#rien ne fonctionne, video pas héberger par le site.
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'mareplaytv'
SITE_NAME = 'Ma Replay TV'
SITE_DESC = 'Replay TV Divers: peu de sources'

URL_MAIN = 'http://mareplaytv.com/'

URL_SEARCH = (URL_MAIN + '?post_type=video&s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?post_type=video&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_GENRES = (True, 'showGenre')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_NEWS = (URL_MAIN + 'videos/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Divertissement', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oRequestHandler = cRequestHandler(URL_MAIN + 'categorie/')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'shorthm"><a title="([^<>]+)" href="([^"]+\/)">.+?imgshorthm".+?src="([^><]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            oOutputParameterHandler = cOutputParameterHandler()
            sub = "Voir toutes les vidéos pour "
            sTitle = str(aEntry[0])
            sThumb = str(aEntry[2])
            
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle.replace(sub, "") , 'genres.png', sThumb, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies(sSearch = ''):

    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl = sUrl.replace('https','http')

    if not (sUrl == URL_MAIN):
        
        if sUrl.find('/categorie') != -1:
            sPattern = '<div class="item-img"[^"]+href="([^"]+)".+?class=.+?responsive.+?srcset="([^"]+)".+?h3><a.+?">([^"]+)<\/a>'
        else:
            sPattern = '<div class="item-img">.+?<img.+?src="([^"]+)".+?<h3><a href="([^"]+)\/*">([^<>]+)<'
        
    else:
        sPattern = '<div class="item-img"> *<a title="([^"]+)" href="([^"]+)"><img.+?src="([^"]+)"'


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            if not (sUrl == URL_MAIN):
                if sUrl.find('/categorie') != -1:
                    sTitle = aEntry[2]
                    sUrl2 = str(aEntry[0])
                    # La plus grande image dans le srcset.
                    sThumb = str(aEntry[1])[:str(aEntry[1]).find(" ")]
                else:
                    sTitle = aEntry[2]
                    sUrl2 = str(aEntry[1])
                    sThumb = str(aEntry[0])
            else:
                sTitle = aEntry[0]
                sUrl2 = str(aEntry[1])
                sThumb = str(aEntry[2])

            sTitle = sTitle.replace('Replay du ','')
            sTitle = sTitle.replace('Emission du ','')
            sTitle = sTitle.replace(',','')
            sTitle = sTitle.replace('Vidéo','')
            sTitle = re.sub('(?:du )*([0-9]+ [a-zA-Zéèû]+ [0-9]{4})','[\\1]', sTitle)

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'replay.png',  sThumb,  sThumb, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class=.page-numbers current.>[0-9]+<\/span><\/li><li><a class=.page-numbers. href=["\']([^"\']+)["\']>[0-9]+<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^"<]+tape=.+?)">(\d+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #Si pas plusieurs liens on affiche direct les hosts.
    if (aResult[0] == False):
        showHosters()
        return

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            sTitle =  '(' + aEntry[1] + ')' + sMovieTitle
            sUrl = str(aEntry[0])

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'replay.png',  sThumbnail,  sThumbnail, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="(http[^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)

            if 'opentostream.com' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                sHtmlContent = oRequestHandler.request()

                sPattern = '<iframe.+?src="([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    sHosterUrl = aResult[1][0]

            oHoster = cHosterGui().checkHoster(sHosterUrl)

            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)

            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
