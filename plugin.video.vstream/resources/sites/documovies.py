#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import util
import re

SITE_IDENTIFIER = 'documovies'
SITE_NAME = 'Documovies'
SITE_DESC = 'Documovies référence les meilleurs films documentaires disponibles sur le web'

URL_MAIN = 'http://fr.documovies.net/'

DOC_NEWS = ('http://fr.documovies.net/', 'showMovies')
DOC_GENRES = ('http://fr.documovies.net/', 'showGenres')
DOC_DOCS = ('http://', 'load')
URL_SEARCH = ('', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires (Derniers ajouts)', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Documentaires (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN+'videos/?playid=27')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires Sélection', 'doc.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sHowResultSearch(str(sSearchText)) 
        oGui.setEndOfDirectory()
        return  

def showGenres():
    oGui = cGui()
    oParser = cParser()
    
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<a title="Accueil"','')

    sPattern = '<a title="([^"]+)" href="([^"]+)">.+?<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[0]
            sUrl = aEntry[1]
        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def sHowResultSearch(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    if not '&search=Recherche' in sUrl:
        sUrl = ('%s?s=%s&search=Recherche' % (URL_MAIN,sSearch))

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a class="link_image" *href="([^"]+)" *title="([^"]+)".+?<img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            sTitle = re.sub('Permalink to(?: -| )','',sTitle)
            sTitle = sTitle.decode("utf-8")
            sTitle = util.cUtil().unescape(sTitle).encode("utf-8")
            if sTitle.startswith(' '):
                sTitle = sTitle[1:]

            sThumb = aEntry[2]
            sThumb = util.QuoteSafe(sThumb)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oOutputParameterHandler.addParameter('sVidCode', False)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage2(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'sHowResultSearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)  

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #sPattern = 'class="video_play".+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="(.+?)" *data.+?flashvars="([^"]+)"'
    sPattern = 'class="video_play".+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="(.+?)" *(?:data|>).+?flashvars="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            if '?w=' in sThumb or '?resize=' in sThumb:
                sThumb = re.sub('((?:jpe*g|png))(\?.+)','\g<1>',sThumb)
            if '.wp.com/' in sThumb:
                sThumb = re.sub('http://.+?.wp.com/','http://',sThumb)

            sThumb = util.QuoteSafe(sThumb)    
            sTitle = aEntry[2]
            sCode = re.sub('(.+?vid=)','',aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oOutputParameterHandler.addParameter('sVidCode', sCode)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, '', oOutputParameterHandler)
  
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers".+?href="(.+?)">(?:&raquo;|>>)<\/a></div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False
    
def __checkForNextPage2(sHtmlContent):
    sPattern = '<span class="(?:page-numbers current|current)">\d+<\/span>.+?href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
 
    return False    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sVidCode = oInputParameterHandler.getValue('sVidCode')

    if sVidCode:
        sHosterUrl = GetFinalUrl(sVidCode)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
  
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<embed *src=.+?vid=(\d+).+?function *current_video'
        aResult = re.search(sPattern,sHtmlContent,re.DOTALL)
        if (aResult):
            sHosterUrl = GetFinalUrl(aResult.group(1))
        else:
            sPattern ='<iframe.+?src="([^"]+)".+?<\/iframe>'
            aResult = re.search(sPattern,sHtmlContent,re.DOTALL)
            if (aResult):
                sHosterUrl = aResult.group(1)        

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
  
    oGui.setEndOfDirectory()

def GetFinalUrl(sVidCode):
    sUrl = ('%swp-admin/admin-ajax.php?action=myextractXML&vid=%s' % (URL_MAIN,sVidCode))
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'video_id *= *"' + sVidCode + '".+?video_url *= *"([^"]+)"'
    aResult = re.search(sPattern,sHtmlContent,re.DOTALL)
    if (aResult):
        return aResult.group(1)
 
    return False
