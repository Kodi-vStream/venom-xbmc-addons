#-*- coding: utf-8 -*-
#johngf.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib,re

SITE_IDENTIFIER = 'otakufr_com'
SITE_NAME = 'OtakuFR'
SITE_DESC = 'OtakuFR animés en streaming et téléchargement'

URL_MAIN = 'http://otakufr.com/'

ANIM_NEWS = (URL_MAIN + 'latest-episodes/' , 'showMovies')
ANIM_ANIMS = ('http://', 'load')
ANIM_POPULAR = (URL_MAIN + 'anime-list/all/any/most-popular/' , 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime-list-all/', 'showAlpha')

URL_SEARCH = (URL_MAIN + 'anime-list/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'anime-list/search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_POPULAR[1], 'Animés (Populaire)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes_vostfr.png', oOutputParameterHandler)

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
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    if '/latest-episodes/' in sUrl:
        sPattern = '<a href="([^"]+)" class="anm" title="([^"]+)">[^<]+<\/a>.+?<img src="([^"]+)" alt="(.+?)">' #news
    else:
        sPattern = '<h2><a href="([^<]+)">([^<]+)</a></h2>.+?<img src="(.+?)"' #populaire et search

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

            sUrl = aEntry[0]
            sThumb = aEntry[2]
            sThumb = urllib.quote(sThumb, safe=':/')
            sType = ''
            if 'vostfr' in sUrl or 'Vostfr' in sUrl:
                sType = 'VOSTFR'
            elif 'VF' in sUrl or 'vf' in sUrl:
                sType = 'VF'
            else:
                sType = 'VOSTFR'

            sTitle =  aEntry[1] + ' (' + sType + ')'
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, 'animes.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^<]+)">([A-Z#])<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sLetter = aEntry[1]
            Link = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + Link)
            oOutputParameterHandler.addParameter('AZ', sLetter)
            oGui.addDir(SITE_IDENTIFIER, 'showAZ', 'Lettre - [COLOR coral]' + sLetter + '[/COLOR]', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    dAZ = oInputParameterHandler.getValue('AZ')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<li><a href="([^<]+)" title="([^<]+)" rel="([^<]+)" class="anm_det_pop">([^<]+)<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True) :
        for aEntry in aResult[1]:
            if aEntry[1].upper()[0] == dAZ or aEntry[1][0].isdigit() and dAZ == '#':

               sUrl = aEntry[0]
               sTitle =  aEntry[1] + ' (' + 'VOSTFR' + ')'
               sDisplayTitle = cUtil().DecoTitle(sTitle)

               oOutputParameterHandler = cOutputParameterHandler()
               oOutputParameterHandler.addParameter('siteUrl', sUrl)
               oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
               oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a href="([^<]+)">Suivant<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #thumbetsyno
    try:
       oParser = cParser()
       sThumb = ''
       sSyn = ''
       sPattern = '<img class="cvr" src="([^"]+)".+?<div class="det"><p><b>Synopsis</b>:<br/>([^<]+)<\/p>'
       aResult = oParser.parse(sHtmlContent, sPattern)
       if aResult[0]:
          sThumb = aResult[1][0][0]
          sSyn = aResult[1][0][1]
    except:
       pass

    oParser = cParser()
    #sPattern = '<a class="lst" href="([^"]+)" title="([^"]+)"><b class="val">'ok
    sPattern = '<a class="lst" href="([^"]+)" title="([^"]+(?<!Episode Date)(?<!Episode News))"><b class="val">'#vire les non épisode
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
               break

            p = re.search(r'(\d+)[ +](\d+)',aEntry[1])
            if p:
                sTitle = re.sub(r'(\d+)[ +](\d+)', p.group(1) + "-" + p.group(2) ,aEntry[1])
            else:
                sTitle = aEntry[1]
            iliste = ['Ep-','-Vostfr','Vostfr-','-Non-Censure','VF-']
            for item in iliste:
                if item in aEntry[1]:
                   sTitle = sTitle.replace(item,'')

            sUrl  = aEntry[0]
            sThumb = sThumb.replace(' ','%20')
            sTitle = sTitle.replace('Episode SP','[ Episode Spécial ] episode').replace(' + ','-')
            sTitle = sTitle.replace('Episode ONA','[ Episode ONA ] episode').replace('Episode OVA','[ Episode OVA ] episode').replace('Episode NC','Episode')
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks',sDisplayTitle, 'animes.png', sThumb, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sUrl = urllib.quote(sUrl, safe=':/')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent,'<div class="nav_ver">','<div class="vdo_wrp">')

    sPattern = '<a href="([^"<>]+/[0-9]/)">([^"]+)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            filter = aEntry[1].lower()
            if 'brightcove' in filter or 'purevid' in filter or 'videomega' in filter:
                continue

            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[1] +' [/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters',sDisplayTitle, 'animes.png',sThumbnail, '', oOutputParameterHandler)

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
    sHtmlContent = sHtmlContent.replace('<iframe src="http://www.facebook.com','')
    sHtmlContent = sHtmlContent.replace('<div class="vdo_wrp"><div style=','<div class="vdo_wrp"><iframe ')
    sHtmlContent = sHtmlContent.replace('data-videoid="','src="https://embed.tune.pk/vid=')
    #pour Tune en test

    oParser = cParser()
    sPattern = '<div class="vdo_wrp"><iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHosterUrl = aResult[1][0]

        if sHosterUrl.startswith('//'):
            sHosterUrl = 'http:' + sHosterUrl

        if '//goo.gl' in sHosterUrl: #netu
            import urllib2
            try:
                class NoRedirection(urllib2.HTTPErrorProcessor):
                    def http_response(self, request, response):
                        return response

                url8 = sHosterUrl.replace('https','http')

                opener = urllib2.build_opener(NoRedirection)
                opener.addheaders.append (('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'))
                opener.addheaders.append (('Connection', 'keep-alive'))

                HttpReponse = opener.open(url8)
                sHosterUrl = HttpReponse.headers['Location']
            except:
                pass

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl,sThumbnail)

    oGui.setEndOfDirectory()
