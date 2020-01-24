#-*- coding: utf-8 -*-
# Venom.
#Pas top ce site
return False
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.packer import cPacker
import urllib2,urllib,re,unicodedata

SITE_IDENTIFIER = 'series_en_streaming_tv'
SITE_NAME = 'Séries-en-Streaming'
SITE_DESC = 'Séries en Streaming'

URL_MAIN = 'http://www.seriefr.eu/'

SERIE_NEWS = (URL_MAIN + 'ajouts/', 'showLasts')
SERIE_SERIES = (URL_MAIN + 'search/', 'AlphaSearch')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')

URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def CleanTitle(title):
    title = cUtil().unescape(title)
    title = cUtil().removeHtmlTags(title)
    try:
        #title = unicode(title, 'utf-8')
        title = unicode(title, 'iso-8859-1')
    except:
        pass
    title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore')

    return title.encode( "utf-8")

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Liste complète)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0,27) :
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break

        if (i < 1):
            sTitle = '[0-9]'
        else:
            sTitle = chr(64+i)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
        oOutputParameterHandler.addParameter('sLetter', sTitle)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]' + sTitle + '[/COLOR][/COLOR]', 'az.png', oOutputParameterHandler)

    cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def AlphaDisplay():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLetter = oInputParameterHandler.getValue('sLetter')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href=\'\.\.\/(serie\/[^\']+?)\'>(' + sLetter + '[^<>]+?)<\/a><br>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = CleanTitle(aEntry[1])
            sUrl2 = URL_MAIN + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addTV(SITE_IDENTIFIER, 'ShowSaisons', sTitle, 'series.png', '','', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch :
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "<a class='host-a wrap'.+?href='([^']+)'.+?src='([^']+)'.+?<h3.+?>(.+?)</h3>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in list(set(aResult[1])):
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1].replace('=200','=360')
            sTitle = CleanTitle(aEntry[2])

            if not sThumb.startswith('http'):
               sThumb = URL_MAIN + sThumb[1:]

            if not sUrl.startswith('http'):
               sUrl = URL_MAIN + sUrl[1:]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'ShowSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    if not sSearch:
        oGui.setEndOfDirectory()

def showLasts():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<a class="host-a wrap".+?href="([^"]+)".+?src="([^"]+)".+?<span.+?>(.+?)</span><br><span.+?>(.+?)</span><br><span.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in list(set(aResult[1])):
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sThumb = aEntry[1].replace('=110','=360') #qualité image
            sSXXEXX = str(aEntry[3]).replace('-','').split('x')
            sMovieTitle = sSXXEXX[0] + ' ' + aEntry[2]
            sDisplayTitle = ('%s %s') % (sMovieTitle, aEntry[4])

            if not sThumb.startswith('http'):
               sThumb = URL_MAIN + sThumb[1:]

            if not sUrl.startswith('http'):
               sUrl = URL_MAIN + sUrl[1:]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def ShowSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    img = ''
    sPattern = '<img.+?src="([^"]+)" alt=".+?" width=".+?">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        img = URL_MAIN[:-1] + aResult[1][0]


    sPattern = '<a href="([^<>]+?)" class="seasonLink">([^<>]+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' Saison ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            if img:
               sThumb = img

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', str(sThumb), '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    #sPattern = "<a class='various' data-fancybox-type='iframe' href='(.+?)' > *(.+?)<\/a>\t*<\/h3>\t*(.+?)<br>"
    #sPattern = ';" src="([^"]+)" class="img-responsive">.+?<a class="various" data-fancybox-type="iframe" href="(.+?)" *> *(.+?)<\/a> *<\/h3>([^<>]+)<'
    sPattern = '<a class="host-a wrap".+?href="([^<"]+)".+?<img.+?src="/images/\?src=(.+?)" class="img-responsive".+?<h3 style=.+?>(.+?)</h3>([^<"]+)<br'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
               sUrl = URL_MAIN[:-1] + sUrl

            sTitle = sMovieTitle + ' ' + aEntry[2]
            sThumb = URL_MAIN + 'images/?src=' + aEntry[1]

            sCom = aEntry[3]
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR coral]Aucun episode disponible[/COLOR]')

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    cConfig().log(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "<a class=\"host-a wrap\" onclick=\"image\('([^']+)'\).+?<span>([^\.<>]+)\..{1,3}<\/span> *<span style='color: #[0-9A-Z]+'>\[(.+?)\]<\/span>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl2 = URL_MAIN + 'cale/' + aEntry[0]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, aEntry[2], aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addTV(SITE_IDENTIFIER, 'GetLink', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def GetLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHosterUrl = cPacker().unpack(aResult[1][0])

        sHosterUrl = sHosterUrl.replace('"+window.innerWidth+"', '1680')

        sPattern2 = "src=\\\\\'(.+?)\\\\"
        aResult = oParser.parse(sHosterUrl, sPattern2)
        if (aResult[0] == True):
            oHoster = cHosterGui().checkHoster(aResult[1][0])
            sHosterUrl = aResult[1][0]
        else:
            oHoster = False

        if (oHoster != False):
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
