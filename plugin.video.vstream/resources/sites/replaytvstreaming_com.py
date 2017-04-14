#-*- coding: utf-8 -*-
#Venom.kodigoal
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig



SITE_IDENTIFIER = 'replaytvstreaming_com'
SITE_NAME = 'ReplayTVstreaming'
SITE_DESC = 'Replay TV'

URL_MAIN = 'http://replaytvstreaming.com'

REPLAYTV_NEWS = ('http://replaytvstreaming.com', 'showMovies')

REPLAYTV_REPLAYTV = ('http://', 'load')

REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '/index.php?do=search&subaction=search&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay (Derniers ajouts)', 'replay.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Replay (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText.replace(' ', '+')
        
        sUrl = URL_SEARCH[0]  + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["Emissions et Magazines", URL_MAIN + "/emission-magazine"] )
    liste.append( ["Documentaires", URL_MAIN + "/documentaire"] )
    liste.append( ["Spectacles", URL_MAIN + "/spectacle"] )
    liste.append( ["Sports", URL_MAIN + "/sport"] )
    liste.append( ["Téléfilms Fiction", URL_MAIN + "/telefilm-fiction"] )

    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
       sUrl = sSearch
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="shortstory"><div class="shortstory-images"><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
  
            sUrl = str(aEntry[0])
            sTitle = ('%s') % (str(aEntry[1]))
            sThumbnail = str(aEntry[2])

            if not sThumbnail.startswith('http'):
               sThumbnail = URL_MAIN + sThumbnail

            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<div class=".+?pages-next"><a href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def showLinks(page, video):

    sUrl = 'http://replaytvstreaming.com/engine/ajax/re_video_part.php?block=video&page=' + page + '&id=' + video

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url  = sHtmlContent
    return url


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<div id="video_[0-9]+" class="epizode re_poleta.+?" data-re_idnews="([^"]+)" data-re_xfn="video" data-re_page="([^"]+)">(.+?)</div>'
    
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTest = ''

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            
            sPage = str(aEntry[1])
            sVideoID = str(aEntry[0])
            sHosterUrl = showLinks(sPage, sVideoID)
            
            sTitle = ('%s') % (str(aEntry[2]))
            
            if not ('Lecteur' in sTitle) and (sTest != sTitle): 
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]' + sTitle + '[/COLOR]')
                sTest = sTitle
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
  
    oGui.setEndOfDirectory()
