#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig

SITE_IDENTIFIER = 'streaming_series_org'
SITE_NAME = 'Streaming Séries'
SITE_DESC = 'Séries en streaming vf gratuitement sur Série Streaming'

URL_MAIN = 'http://www.streamingseries.biz/'

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = (URL_MAIN, 'showMovies')
SERIE_VFS = (URL_MAIN + 'version-francaise-vf/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'series-les-plus-vues/', 'showMovies')
SERIE_COMMENTS = (URL_MAIN + 'seriestv-les-plus-commentees/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'series-streaming-les-plus-aimees/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerieSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus Vues)', 'series_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus Commentées)', 'series_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux Notées)', 'series_notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_SEARCH[0] + sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
#    sHtmlContent = sHtmlContent.replace('//ad.advertstream.com/', '').replace('http://www.adcash.com/', '').replace('http://regie.espace-plus.net/', '')
    sPattern = '<div class="moviefilm"><a href=".+?"><img src="(.+?)".+?<a href="([^<]+)">([^<]+)</a>.+?<small>(.+?)</small>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[2]) == 0:
                    continue

            sThumb = aEntry[0].replace('-119x125','') #qual thumbs
            sSmall = aEntry[3].replace('<span class="likeThis">', '').replace('</span>', '')
            sSmall = sSmall.replace('Yorum','Commentaires')
            sTitle = aEntry[2] + ' [COLOR azure]- ' + sSmall + '[/COLOR]'
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?<a class="page larger".+?href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl = sUrl + '100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)"><span>([^"]+(?<!Infos série))</span></a>' #vire non épisode
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumb', str(sThumb))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')
    sHtmlContent = sHtmlContent.replace('\r', '')

    sPattern = '(VF|VOSTFR)<\/b><\/p>|<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #langue
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            #episode
            else:
                sHosterUrl = str(aEntry[1])
                if '//goo.gl' in sHosterUrl:
                    import urllib2
                    try:
                        cConfig().log('ok ' + sHosterUrl)
                        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                        request = urllib2.Request(sHosterUrl, None, headers)
                        reponse = urllib2.urlopen(request)
                        sHosterUrl = reponse.geturl()
                    except:
                        pass

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
