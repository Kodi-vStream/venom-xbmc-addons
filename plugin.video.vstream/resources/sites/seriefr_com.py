#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re

SITE_IDENTIFIER = 'seriefr_com'
SITE_NAME = 'Seriefr.com'
SITE_DESC = 'Série en Streaming HD - Vk.Com - Netu.tv - ExaShare - YouWatch'

URL_MAIN = 'http://www.seriefr.com/'

SERIE_SERIES = ('http://www.seriefr.com/liste.html', 'AlphaSearch')
SERIE_NEWS = ('http://www.seriefr.com/index.html', 'showMovies')

#SERIE_VOSTFRS = 'http://full-stream.net/seriestv/vostfr/'
#ANIM_VFS = 'http://full-stream.net/mangas/mangas-vf/'
#ANIM_VOSTFRS = 'http://full-stream.net/mangas/mangas-vostfr/'

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries Liste complete', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries Nouveautees', 'series.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(str(sSearchText))
        oGui.setEndOfDirectory()
        return
        
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
            sTitle = '1'
        else:
            sTitle = chr(64+i)
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://www.seriefr.com/liste-' + sTitle.lower() + '.html')
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]', 'genres.png', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
        
def AlphaDisplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^<>"]+?)" style="display:block">([^<>"]+?)<\/a>.+?<img src="([^<>"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            sThumb = URL_MAIN + aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'saisonHosters', sDisplayTitle, sThumb, sThumb,'', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
        
        oGui.setEndOfDirectory()

    

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)
        
        query_args = { 'serie': str(sSearch) }
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = 'http://www.seriefr.com/serie.html'
        request = urllib2.Request(url,data,headers)

        try: 
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason

        html = reponse.read()
        html = html.replace('\n', '')

        sHtmlContent = html
        
        sPattern = '<h1><a href="(.+?)">(.+?)<.a><.h1><.div><div class="infos"> <div class="image"><a href=".+?"><img src="(.+?)" title=.+?><.a><.div><div class="desc" >(.+?)<.div>'
        
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();
        
        #sHtmlContent = sHtmlContent.replace('streaming','')
    
        sPattern = 'full-stream-view-hover"><img src="(.+?)" alt="(.+?)".+?<h2><a href="(.+?)">.+?</a></h2>.+?class="short-insider">(.+?)</div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if sSearch:
                sTitle = str(aEntry[1])
                sUrl = str(URL_MAIN+aEntry[0])
                sThumb = str(URL_MAIN+aEntry[2])
                sCom = aEntry[3]
            else:
                sTitle = str(aEntry[1])
                sUrl = str(URL_MAIN+aEntry[2])
                sThumb = str(URL_MAIN+aEntry[0])
                sCom = aEntry[3]
            
            sTitle = sTitle.replace('streaming','')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'saisonHosters', sTitle, '', sThumb, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation".+?<span.+?<a href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    if (aResult[0] == True):
        return URL_MAIN+aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/likebox.php','')

    oParser = cParser()
    
    sPattern = '"liens en Version Francaise"(.+?)class="VOST"'
    aResult = re.findall(sPattern,sHtmlContent)
    List_VF = aResult[0]
    
    #sPattern = '<iframe src=."(.+?)."'
    sPattern = '\("#(link[0-9]+)"\).+?<iframe src=."(.+?)."'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry[1])
            oHoster = cHosterGui().checkHoster(sHosterUrl)            
        
            if (oHoster != False):         
                try:
                    oHoster.setHD(sHosterUrl)
                except: pass
                
                if aEntry[0] in List_VF:
                    sTitle = '[VF]' + sMovieTitle
                else:
                    sTitle = '[VOSTFR]' + sMovieTitle
                
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)

                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def saisonHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl.replace('.html', '-saison-50.html')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)" title="">.+?</i>(.+?)</div></a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #sTitle = sMovieTitle+'[COLOR azure]'+aEntry[1]+'[/COLOR]'
            sTitle = sMovieTitle + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            sUrl = URL_MAIN+aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'epHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler) 

        cConfig().finishDialog(dialog)    

    oGui.setEndOfDirectory()

def epHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('streaming','')

    sPattern = '<a href="([^<]+)" title="([^<]+)" class="tilink sinactive"><i class="fa fa-youtube-play"></i>.+?</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1].replace('streaming','')
            sDisplayTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN+aEntry[0]))
            
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler) 

        cConfig().finishDialog(dialog)    

    oGui.setEndOfDirectory()
    
