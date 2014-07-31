from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler


SITE_IDENTIFIER = 'gstream_in'
SITE_NAME = 'G-Stream.in'

URL_MAIN = 'http://g-stream.in'
URL_SHOW_MOVIE = 'http://g-stream.in/showthread.php?t='
URL_CATEGORIES = 'http://g-stream.in/forumdisplay.php?f='
URL_HOSTER = 'http://g-stream.in/secure/'
URL_SEARCH = 'http://g-stream.in/search.php'


def load():
    oGui = cGui()
    __createMainMenuEntry(oGui, 'Aktuelle KinoFilme', 542)
    __createMainMenuEntry(oGui, 'Action', 591)
    __createMainMenuEntry(oGui, 'Horror', 593)
    __createMainMenuEntry(oGui, 'Komoedie', 592)
    __createMainMenuEntry(oGui, 'Thriller', 595)
    __createMainMenuEntry(oGui, 'Drama', 594)
    __createMainMenuEntry(oGui, 'Fantasy', 655)
    __createMainMenuEntry(oGui, 'Abenteuer', 596)
    __createMainMenuEntry(oGui, 'Animation', 677)
    __createMainMenuEntry(oGui, 'Dokumentation', 751)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySearch')
    oGuiElement.setTitle('Suche')
    oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def __createMainMenuEntry(oGui, sMenuName, iCategoryId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sMenuName)
    oGuiElement.setFunction('parseMovieResultSite')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('normalySiteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=')
    oOutputParameterHandler.addParameter('siteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=1')
    oOutputParameterHandler.addParameter('iPage', 1)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def displaySearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __search(sSearchText)
        return

    oGui.setEndOfDirectory()

def __search(sSearchText):
    sUrl = 'http://g-stream.in/search.php?do=process&childforums=1&do=process&exactname=1&forumchoice[]=528&query=' + str(sSearchText) + '&quicksearch=1&s=&securitytoken=guest&titleonly=1'
        
    oRequestHandler = cRequestHandler(sUrl)
    sUrl = oRequestHandler.getHeaderLocationUrl()

    __parseMovieResultSite(sUrl, sUrl, 1)

def parseMovieResultSite():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        normalySiteUrl = oInputParameterHandler.getValue('normalySiteUrl')
        iPage = oInputParameterHandler.getValue('iPage')
        __parseMovieResultSite(siteUrl, normalySiteUrl, iPage)


def __parseMovieResultSite(siteUrl, normalySiteUrl, iPage):
    oGui = cGui()

    sPattern = '<a class="p1" href=".*?" ><img src="([^"]+)".*?<a href="([^"]+)" id="([^"]+)">([^<]+)<'

    # request
    oRequest = cRequestHandler(siteUrl)
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('parseMovie')
            oGuiElement.setTitle(aEntry[3])
            oGuiElement.setThumbnail(aEntry[0])
            sUrl = str(aEntry[2]).replace('thread_title_', '')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_SHOW_MOVIE + str(sUrl))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)


    # check for next site
    sPattern = '<td class="thead">Zeige Themen .*?von ([^<]+)</td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            iTotalCount = aEntry[0]
            iNextPage = int(iPage) + 1
            iCurrentDisplayStart = __createDisplayStart(iNextPage)
            if (iCurrentDisplayStart < iTotalCount):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieResultSite')
                oGuiElement.setTitle('next ..')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('iPage', iNextPage)
                oOutputParameterHandler.addParameter('normalySiteUrl', normalySiteUrl)
                normalySiteUrl = normalySiteUrl + str(iNextPage)
                oOutputParameterHandler.addParameter('siteUrl', normalySiteUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)


    oGui.setEndOfDirectory()

def __createDisplayStart(iPage):
    return (20 * int(iPage)) - 20

def __createInfo(oGui, sHtmlContent):
    sPattern = '<td class="alt1" id="td_post_.*?<img src="([^"]+)".*?<b>Inhalt:</b>(.*?)<div align="center">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(str(aEntry[0]))
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(cUtil().removeHtmlTags(str(aEntry[1])).replace('\t', ''))
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def parseMovie():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('movieUrl')):
        sSiteUrl = oInputParameterHandler.getValue('movieUrl')
	        
        oRequest = cRequestHandler(sSiteUrl)
        sHtmlContent = oRequest.request()
	sTitle = __getMovieTitle(sHtmlContent)

        __createInfo(oGui, sHtmlContent)

        aHosters = []
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'filebase', 'filebase.to')
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'filestage', 'www.filestage.to')
        __parseHosterByPattern(aHosters, sHtmlContent, 'novamov', '<a href="([^"]+)" title="novamov" target="_blank">novamov</a>')
        __parseHosterByPattern(aHosters, sHtmlContent, 'videoweed', '<a href="([^"]+)" title="videoweed" target="_blank">videoweed</a>')
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'duckload', 'www.duckload.com')
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'mystream', 'www.mystream.to')
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'loadedit', 'loaded.it')
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'tubeload', 'www.tubeload.to')
        __parseHosterSiteFromSite(aHosters, sHtmlContent, 'sharehoster', 'www.sharehoster.com')
        __parseHosterByPattern(aHosters, sHtmlContent, 'megavideo', '<a href="([^"]+)" title="megavideo" target="_blank">megavideo</a>')
        __parseHosterByPattern(aHosters, sHtmlContent, 'zshare', '<a href="([^"]+)" title="zshare" target="_blank">zshare</a>')
        __parseHosterByPattern(aHosters, sHtmlContent, 'movshare', '<a href="([^"]+)" title="movshare" target="_blank">movshare</a>')        

        for aHoster in aHosters:
            if (len(aHoster) > 0):                
                oHoster = aHoster[0];
		if (sTitle != False):
		    oHoster.setFileName(sTitle)

                cHosterGui().showHoster(oGui, oHoster, str(aHoster[1]), True)              
        
    oGui.setEndOfDirectory()

def __getMovieTitle(sHtmlContent):
    sPattern = '<strong><h2>(.*?)</strong></h2>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
	return aResult[1][0]

    return False;

def __parseHosterByPattern(aHosters, sHtmlContent, sHosterIdentifier, sPattern):
    sPattern = '<div style="display: none;" id="ame_noshow_post_.*?' + sPattern

    aHoster = []
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern, 1)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oHoster = cHosterHandler().getHoster(sHosterIdentifier)
            aHoster.append(oHoster)
            aHoster.append(str(aEntry).replace(' ', '+'))
            aHosters.append(aHoster)

    return True

def __parseHosterSiteFromSite(aHosters, sHtmlContent, sHosterIdentifier, sHosterId):
    aHoster = []
    sRegex = '<div style="display: none;" id="ame_noshow_post_.*?<a href="' + URL_HOSTER + sHosterId + '([^ ]+)" target="_blank" rel="nofollow" >'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)    
    if (aResult[0] == True):
        for aEntry in aResult[1]:            
            sUrl = URL_HOSTER + sHosterId + aEntry

            oHoster = cHosterHandler().getHoster(sHosterIdentifier)
            aHoster.append(oHoster)
            aHoster.append(str(sUrl).replace(' ', '+'))
            aHosters.append(aHoster)
      
    return True
