from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'ustream_tv'
SITE_NAME = 'Ustream.tv'

URL_MAIN = 'http://www.ustream.tv'
URL_LIVE_DISCOVERY = 'http://www.ustream.tv/discovery/live/all'
URL_SEARCH = 'http://www.ustream.tv/discovery/live/all'
URL_CATEGORY_ALL = 'http://www.ustream.tv/discovery/live/all'
URL_CATEGORY_SPORTS = 'http://www.ustream.tv/discovery/live/sports'
URL_CATEGORY_ENTERTAINMENT = 'http://www.ustream.tv/discovery/live/entertainment'
URL_CATEGORY_GAMING = 'http://www.ustream.tv/discovery/live/gaming'
URL_CATEGORY_MUSIC = 'http://www.ustream.tv/discovery/live/music'
URL_CATEGORY_ANIMALS = 'http://www.ustream.tv/discovery/live/animals'
URL_CATEGORY_24 = 'http://www.ustream.tv/discovery/live/24-7-broadcasts'
URL_CATEGORY_NEWS = 'http://www.ustream.tv/discovery/live/news'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sSiteUrl', URL_LIVE_DISCOVERY)
    __createMenuEntry(oGui, 'showLiveVideos', 'Live', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sSiteUrl', URL_LIVE_DISCOVERY)
    __createMenuEntry(oGui, 'showCategories', 'Categories', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sSiteUrl', URL_SEARCH)
    __createMenuEntry(oGui, 'showSearch', 'Search', oOutputParameterHandler)    
 
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCategories():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('sSiteUrl')

    oRequestHandler = cRequestHandler(sSiteUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="discoveryHead clr">.*?<a href="#" class="button select blue">(.*?)</div>'
    sNextFunction = 'showSubCategories'

    __showCategories(sHtmlContent, sPattern, sNextFunction)

def showSubCategories():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('sSiteUrl')

    oRequestHandler = cRequestHandler(sSiteUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="discoveryHead clr">.*?<a href="#" class="button select">(.*?)</div>'
    sNextFunction = 'showLiveVideos'

    __showCategories(sHtmlContent, sPattern, sNextFunction)

def __showCategories(sHtmlContent, sPattern, sNextFunction):
    oGui = cGui()
  
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
	sHtmlContent = str(aResult[1][0])

	sPattern = '<a href="([^"]+)">([^"]+)</a>'
	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)

	if (aResult[0] == True):
	    for aEntry in aResult[1]:
		oGuiElement = cGuiElement()
		oGuiElement.setSiteName(SITE_IDENTIFIER)
		if (str(aEntry[1]) == 'All'):
		    oGuiElement.setFunction('showLiveVideos')
		else:
		    oGuiElement.setFunction(sNextFunction)
		oGuiElement.setTitle(aEntry[1])

		oOutputParameterHandler = cOutputParameterHandler()
		oOutputParameterHandler.addParameter('sSiteUrl', URL_MAIN + str(aEntry[0]))
		oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showLiveVideos():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('sSiteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('iPage')):
	iPage = oInputParameterHandler.getValue('iPage')

    oRequestHandler = cRequestHandler(sSiteUrl)
    oRequestHandler.addParameters('page', str(iPage))
    sHtmlContent = oRequestHandler.request()
    __parseSite(sHtmlContent, sSiteUrl, iPage)

def showSearch():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('sSiteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('iPage')):
	iPage = oInputParameterHandler.getValue('iPage')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText.replace(' ', '+')
	oRequestHandler = cRequestHandler(sSiteUrl)	
	oRequestHandler.addParameters('q', str(sSearchText))
	sSiteUrl = oRequestHandler.getRequestUri()

	oRequestHandler = cRequestHandler(sSiteUrl)
	oRequestHandler.addParameters('page', str(iPage))
	sHtmlContent = oRequestHandler.request()
        __parseSite(sHtmlContent, sSiteUrl, iPage)
	return

    oGui.setEndOfDirectory()

def __parseSite(sHtmlContent, sSiteUrl, iCurrentPage):
    oGui = cGui()

    sPattern = '<a href="/channel/(.*?)">.*?<span class="img"><img.*?rel="([^"]+)".*?<span>(.*?)</span>.*?<span class="liveViewers">(.*?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
	for aEntry in aResult[1]:
	    oGuiElement = cGuiElement()
	    oGuiElement.setSiteName(SITE_IDENTIFIER)
	    oGuiElement.setThumbnail(str(aEntry[1]))
	    oGuiElement.setFunction('showHoster')
	    sTitle = __createTitle(aEntry[2], aEntry[3])
	    oGuiElement.setTitle(sTitle)

	    oOutputParameterHandler = cOutputParameterHandler()
	    oOutputParameterHandler.addParameter('sSiteUrl', URL_MAIN + '/channel/' + str(aEntry[0]))
	    oGui.addFolder(oGuiElement, oOutputParameterHandler)

	iNextPage = __checkForNextPage(sHtmlContent, iCurrentPage)
	if (iNextPage != False):
	    oGuiElement = cGuiElement()
	    oGuiElement.setSiteName(SITE_IDENTIFIER)
	    oGuiElement.setFunction('showLiveVideos')
	    oGuiElement.setTitle('next..')
	    oOutputParameterHandler = cOutputParameterHandler()
	    oOutputParameterHandler.addParameter('sSiteUrl', sSiteUrl)
	    oOutputParameterHandler.addParameter('iPage', str(iNextPage))
	    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent, iCurrentPage):
    sPattern = '<a href="([^"]+)" class="pagerButton next rightSide"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
	sUrl = str(aResult[1][0])
	sPattern = 'page=([^"]+)'
	oParser = cParser()
	aResult = oParser.parse(sUrl, sPattern)	

	iNextPage = int(aResult[1][0])
	if (int(iCurrentPage) + 1 == iNextPage):	    
	    return iNextPage

    return False

def showHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('sSiteUrl')
    
    oHoster = cHosterHandler().getHoster('ustream')
    cHosterGui().showHoster(oGui, oHoster, sSiteUrl)

    oGui.setEndOfDirectory()

def __createTitle(sTitle, sViewers):
    return str(sTitle) + ' - ' + str(sViewers).replace('\t', '')