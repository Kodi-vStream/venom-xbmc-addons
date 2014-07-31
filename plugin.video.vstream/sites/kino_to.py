import urllib
import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'kino_to'
SITE_NAME = 'Kino.to'

URL_MAIN = 'http://kino.to'
URL_CINEMA_PAGE = 'http://kino.to/Cine-Films.html'
URL_GENRE_PAGE = 'http://kino.to/Genre.html'
URL_MOVIE_PAGE = 'http://kino.to/Movies.html'
URL_SERIE_PAGE = 'http://kino.to/Series.html'
URL_DOCU_PAGE = 'http://kino.to/Documentations.html'

URL_FAVOURITE_MOVIE_PAGE = 'http://kino.to/Popular-Movies.html'
URL_FAVOURITE_SERIE_PAGE = 'http://kino.to/Popular-Series.html'
URL_FAVOURITE_DOCU_PAGE = 'http://kino.to/Popular-Documentations.html'

URL_LATEST_SERIE_PAGE = 'http://kino.to/Latest-Series.html'
URL_LATEST_DOCU_PAGE = 'http://kino.to/Latest-Documentations.html'

URL_SEARCH = 'http://kino.to/Search.html'
URL_MIRROR = 'http://kino.to/aGET/Mirror/'
URL_EPISODE_URL = 'http://kino.to/aGET/MirrorByEpisode/'
URL_AJAX = 'http://kino.to/aGET/List/'
URL_LANGUAGE = 'http://kino.to/aSET/PageLang/1'

def load():
    logger.info('load kinoto :)')

    sSecurityValue = __getSecurityCookieValue()
    __initSiteLanguage(sSecurityValue)

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'news')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayNews', 'Neues von Heute', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayCinemaSite', 'Aktuelle KinoFilme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayGenreSite', 'Kategorien', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'movie')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayCharacterSite', 'Filme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SERIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'series')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayCharacterSite', 'Serien', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_DOCU_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'documentation')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayCharacterSite', 'Dokumentationen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_FAVOURITE_MOVIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'movie')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayFavItems', 'Beliebteste Filme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_FAVOURITE_SERIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'series')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayFavItems', 'Beliebteste Serien', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_FAVOURITE_DOCU_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'documentation')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayFavItems', 'Beliebteste Dokumentationen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LATEST_SERIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'series')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayFavItems', 'Neuste Serien', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LATEST_DOCU_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'documentation')
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displayFavItems', 'Neuste Dokumentationen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    __createMenuEntry(oGui, 'displaySearchSite', 'Suche', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createTitleWithLanguage(sLanguage, sTitle):
    sTitle = cUtil().removeHtmlTags(sTitle, '')
    sTitle = str(sTitle).replace('\t', '').replace('&amp;', '&')

    if (sLanguage == '1'):
        return sTitle + ' (de)'
    if (sLanguage == '2'):
        return sTitle + ' (en)'
    if (sLanguage == '7'):
        return sTitle + ' (tu)'

    return sTitle


def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __initSiteLanguage(sSecurityValue):
    oRequestHandler = cRequestHandler(URL_LANGUAGE)
    oRequestHandler.addHeaderEntry('COOKIE', sSecurityValue)
    oRequestHandler.request()

def __getSecurityCookieValue():
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<HTML><HEAD><SCRIPT language="javascript" src="([^"]+)"></SCRIPT></HEAD><BODY onload="scf\(\'(.*?)\',\'/\'\)"></BODY></HTML>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sScriptFile = URL_MAIN + str(aResult[1][0][0])
        sHashSnippet = str(aResult[1][0][1])

        logger.info('scriptfile: ' + str(sScriptFile))
        oRequestHandler = cRequestHandler(sScriptFile)
        oRequestHandler.addHeaderEntry('Referer', 'http://kino.to/')
        oRequestHandler.addHeaderEntry('Accept', '*/*')
        oRequestHandler.addHeaderEntry('Host', 'kino.to')
        sHtmlContent = oRequestHandler.request()

        sPattern = 'escape\(hsh \+ "([^"]+)"\)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sHash = aResult[1][0]

            sHash = sHashSnippet + sHash
            sSecurityCookieValue = 'sitechrx=' + str(sHash) + ';Path=/'

            oRequestHandler = cRequestHandler(URL_MAIN + '/')
            oRequestHandler.addHeaderEntry('Cookie', sSecurityCookieValue)
            oRequestHandler.request()

            logger.info('token: ' + str(sSecurityCookieValue))
            return sSecurityCookieValue

    return False

def displaySearchSite():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        oRequestHandler = cRequestHandler(URL_SEARCH)

        oRequestHandler.addParameters('q', sSearchText)
        sRequestUri = oRequestHandler.getRequestUri();
        logger.info(sRequestUri)

        oRequest = cRequestHandler(sRequestUri)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kino.to/')
        sHtmlContent = oRequest.request()

        __diplayItems(sHtmlContent)
        return

    oGui.setEndOfDirectory()

def __diplayItems(sHtmlContent):
    sHtmlContent = str(sHtmlContent)

    sSecurityValue = ''
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('securityCockie')):
        sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    sPattern = '<td class="Icon"><img width="16" height="11" src="http://res.kino.to/gr/sys/lng/([^"]+).png" alt="language"></td>.*?<td class="Title">.*?<a onclick="return false;" href="([^"]+)">([^<]+)</a>'
    oGui = cGui()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('parseMovieEntrySite')
            oGuiElement.setTitle(__createTitleWithLanguage(aEntry[0], aEntry[2]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[1]))
            oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __getHtmlContent():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl') and oInputParameterHandler.exist('mediaType')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sSecurityValue = oInputParameterHandler.getValue('securityCockie')

        # request
        oRequest = cRequestHandler(siteUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kino.to/')
        oRequest.addHeaderEntry('Accept', '*/*')
        oRequest.addHeaderEntry('Host', 'kino.to')
        return oRequest.request()

    return ''


def displayFavItems():
    #sPattern = '<td class="Icon"><img width="16" height="11" src="http://res.kino.to/gr/sys/lng/([^"]+).png" alt="language"></td>.*?<td class="Title">.*?<a onclick="return false;" href="([^"]+)">([^<]+)</a>'

    sHtmlContent = __getHtmlContent()
    __diplayItems(sHtmlContent)

def displayNews():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    sHtmlContent = __getHtmlContent()

    sPattern = '<div class="ModuleHead mHead"><div class="Opt leftOpt Dummy"></div>.*?<div class="Opt leftOpt Headlne"><h1>(.*?)</h1></div>	<div class="Opt rightOpt Hint">Insgesamt: (.*?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()

    if (aResult[0] == True):
        for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseNews')
                oGuiElement.setTitle(__createTitleWithLanguage('', aEntry[0]) +  ' (' + str(aEntry[1]) + ')')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
                oOutputParameterHandler.addParameter('page', 1)
                oOutputParameterHandler.addParameter('mediaType', 'news')
                oOutputParameterHandler.addParameter('sNewsTitle', aEntry[0])
                oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def parseNews():
    oGui = cGui()
    sHtmlContent = __getHtmlContent()
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    oInputParameterHandler = cInputParameterHandler()
    sNewsTitle = oInputParameterHandler.getValue('sNewsTitle')

    sPatternStart = '<div class="Opt leftOpt Headlne"><h1>' + str(sNewsTitle)
    sPattern = sPatternStart + '(.*?)<div class="ModuleFooter">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        #sPattern = '<td class="Icon"><img src="http://res.kino.to/gr/sys/lng/([^"]+).png" alt="language" width="16" height="11".*?<td class="Title">.*?"([^"]+)" class="OverlayLabel">(.*?)</td>'
	sPattern = '<td class="Icon"><img src="http://res.kino.to/gr/sys/lng/([^"]+).png" alt="language" width="16" height="11".*?<td class="Title">.*?href ="([^"]+)".*?class="OverlayLabel">(.*?)</td>'

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieEntrySite')
                oGuiElement.setTitle(__createTitleWithLanguage(aEntry[0], aEntry[2]))

                oOutputParameterHandler = cOutputParameterHandler()

                sUrl = str(aEntry[1])
                aUrl = sUrl.split(',')
                if (len(aUrl) > 0):
                    sUrl = aUrl[0]

                oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + sUrl)
                oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def displayCharacterSite():
    logger.info('load displayCharacterSite')
    sPattern = 'class="LetterMode.*?>([^>]+)</a>'
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl') and oInputParameterHandler.exist('page') and oInputParameterHandler.exist('mediaType')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        iPage = oInputParameterHandler.getValue('page')
        sMediaType = oInputParameterHandler.getValue('mediaType')

        # request
        oRequest = cRequestHandler(siteUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kino.to/')
        sHtmlContent = oRequest.request()

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('ajaxCall')
                oGuiElement.setTitle(aEntry[0])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('character', aEntry[0])
                oOutputParameterHandler.addParameter('page', iPage)
                oOutputParameterHandler.addParameter('mediaType', sMediaType)
                oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def displayGenreSite():
    logger.info('load displayGenreSite')
    sPattern = '<td class="Title"><a href="/Genre/([^Poular]+)">([^"]+)</a>'

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    # request
    oRequest = cRequestHandler(URL_GENRE_PAGE)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kino.to/')
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showCharacters')
            oGuiElement.setTitle(aEntry[1])

            iGenreId = aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('page', 1)
            oOutputParameterHandler.addParameter('mediaType', 'fGenre')
            oOutputParameterHandler.addParameter('mediaTypePageId', iGenreId)
            oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def displayCinemaSite():
    logger.info('load displayCinemaSite')
    sPattern = '<div onclick="location.href=\'([^>]+)\';.*?<div class="Opt leftOpt Headlne"><h1>([^>]+)</h1></div>.*?<img src="([^"]+)" class="Thumb".*?"Descriptor">([^"]+)</div>'

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    oRequest = cRequestHandler(URL_CINEMA_PAGE)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kino.to/')
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    # iterated result and create GuiElements
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('parseMovieEntrySite')
            oGuiElement.setTitle(aEntry[1])
            oGuiElement.setThumbnail(aEntry[2])
            oGuiElement.setDescription(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def parseMovieEntrySite():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('movieUrl')):
        sUrl = oInputParameterHandler.getValue('movieUrl')
	
        # get movieEntrySite content
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kino.to/')
        sHtmlContent = oRequest.request()

	sMovieTitle = __createMovieTitle(sHtmlContent)

        bIsSerie = __isSerie(sHtmlContent)
        if (bIsSerie):
            aSeriesItems = parseSerieSite(sHtmlContent)

            if (len(aSeriesItems) > 0):
                __createInfoItem(oGui, sHtmlContent)
                for aSeriesItem in aSeriesItems:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setTitle(aSeriesItem[0])
                    oGuiElement.setFunction('displayHoster')

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', aSeriesItem[1])
                    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
		    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
        else:
            displayHoster(sHtmlContent, sMovieTitle)


    oGui.setEndOfDirectory()

def __createMovieTitle(sHtmlContent):
    sPattern = '<h1><span style="display: inline-block">(.*?)</h1>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
        
    if (aResult[0] == True):
	sTitle = cUtil().removeHtmlTags(str(aResult[1][0]))
	return sTitle
    
    return False

    #http://kino.to/aGET/Mirror/Love_and_Other_Drugs-Nebenwirkungen_inklusive&Hoster=2&Mirror=1

def __createInfoItem(oGui, sHtmlContent):
    sThumbnail = __getThumbnail(sHtmlContent)
    sDescription = __getDescription(sHtmlContent)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle('info (press Info Button)')
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setFunction('dummyFolder')
    oGuiElement.setDescription(sDescription)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
    oOutputParameterHandler.addParameter('sDescription', sDescription)

    # [('Jeff Tremaine', 'United States', '~ 94 min.', 'Action', '509.648')]
    #aDetails = __getDetails(sHtmlContent)
    #oOutputParameterHandler.addParameter('aDetails', aDetails)

    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def dummyFolder():
    oGui = cGui()    
    oGui.setEndOfDirectory()

def displayHoster(sHtmlContent = '', sMovieTitle = False):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')
    if (sMovieTitle == False):
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kino.to/')
        sHtmlContent = oRequest.request()


    aHosters = __getMovieHoster(sHtmlContent);

    if (len(aHosters) > 0):
        __createInfoItem(oGui, sHtmlContent)

    for aHoster in aHosters:
        if (len(aHoster) > 0):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(aHoster[0])
            oGuiElement.setFunction('parseHosterSnippet')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('hosterName', aHoster[0])
            oOutputParameterHandler.addParameter('hosterUrlSite', aHoster[1])
            oOutputParameterHandler.addParameter('hosterParserMethode', aHoster[2])
            oOutputParameterHandler.addParameter('hosterFileName', aHoster[3])
            oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
	    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def parseSerieSite(sHtmlContent):
    aSeriesItems = []

    sPattern = 'id="SeasonSelection" rel="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aSeriesUrls = aResult[1][0].split("&amp;")
        sSeriesUrl = '&' + str(aSeriesUrls[1]) + '&' + str(aSeriesUrls[2])

        sPattern = '<option.*?rel="([^"]+)".*?>Staffel ([^<]+)</option'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                aSeriesIds = aEntry[0].split(",")
                for iSeriesIds in aSeriesIds:
                    aSeries = []
                    iSeriesId = iSeriesIds
                    iSeasonId = aEntry[1]

                    sTitel = 'Staffel '+ str(iSeasonId) + ' - ' + str(iSeriesId)
                    sUrl = URL_EPISODE_URL + sSeriesUrl + '&Season=' + str(iSeasonId) + '&Episode=' + str(iSeriesId)

                    aSeries.append(sTitel)
                    aSeries.append(sUrl)
                    aSeriesItems.append(aSeries)
    return aSeriesItems

def __isSerie(sHtmlContent):
    sPattern = 'id="SeasonSelection" rel="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
            return True
    else:
            return False


def parseHosterSnippet():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('hosterName')
        and oInputParameterHandler.exist('hosterUrlSite')
        and oInputParameterHandler.exist('hosterParserMethode')
        and oInputParameterHandler.exist('hosterFileName')):
        sHosterName = oInputParameterHandler.getValue('hosterName')
        sHosterUrlSite = oInputParameterHandler.getValue('hosterUrlSite')
        sHosterParserMethode = oInputParameterHandler.getValue('hosterParserMethode')
        sHosterFileName = oInputParameterHandler.getValue('hosterFileName')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
        if (sHosterParserMethode == 'parseHosterDefault'):
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, False, sSecurityValue, sMovieTitle)
        if (sHosterParserMethode == 'parseMegaVideoCom'):
            sPattern = 'value=\\\\"http:\\\\/\\\\/www.megavideo.com\\\\/v\\\\/([^"]+)\\\\'
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, sPattern, sSecurityValue, sMovieTitle)

def ajaxCall():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    if (oInputParameterHandler.exist('page') and oInputParameterHandler.exist('mediaType')):
        iPage = oInputParameterHandler.getValue('page')
        sMediaType = oInputParameterHandler.getValue('mediaType')

        iMediaTypePageId = False
        if (oInputParameterHandler.exist('mediaTypePageId')):
            iMediaTypePageId = oInputParameterHandler.getValue('mediaTypePageId')

        sCharacter = 'A'
        if (oInputParameterHandler.exist('character')):
            sCharacter = oInputParameterHandler.getValue('character')


        logger.info('MediaType: ' + sMediaType + ' , Page: ' + str(iPage) + ' , iMediaTypePageId: ' + str(iMediaTypePageId) + ' , sCharacter: ' + str(sCharacter))

        sAjaxUrl = __createAjaxUrl(sMediaType, iPage, iMediaTypePageId, sCharacter)
        logger.info(sAjaxUrl)

        oRequest = cRequestHandler(sAjaxUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kino.to/')
        sHtmlContent = oRequest.request()

        # parse content
        sPattern = '\["([^"]+)".*?<a href=\\\\"\\\\([^"]+)\\\\".*?onclick=\\\\"return false;\\\\">([^<]+)<\\\\/a>'
        oParser = cParser()

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):

            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieEntrySite')
                oGuiElement.setTitle(__createTitleWithLanguage(aEntry[0], aEntry[2]))

                sUrl = URL_MAIN + str(aEntry[1])
                sUrl = oParser.replace('\\\\/', '/', sUrl)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('movieUrl', sUrl)
                oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)


        # check for next site
        sPattern = '"iTotalDisplayRecords":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                iTotalCount = aEntry[0]
                iNextPage = int(iPage) + 1
                iCurrentDisplayStart = __createDisplayStart(iNextPage)
                if (iCurrentDisplayStart < iTotalCount):
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('ajaxCall')
                    oGuiElement.setTitle('next ..')

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('page', iNextPage)
                    oOutputParameterHandler.addParameter('character', sCharacter)
                    oOutputParameterHandler.addParameter('mediaType', sMediaType)
                    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
                    if (iMediaTypePageId != False):
                        oOutputParameterHandler.addParameter('mediaTypePageId', iMediaTypePageId)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showCharacters():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('mediaType')):
        sMediaType = oInputParameterHandler.getValue('mediaType')

    iMediaTypePageId = False
    if (oInputParameterHandler.exist('mediaTypePageId')):
        iMediaTypePageId = oInputParameterHandler.getValue('mediaTypePageId')

    oGui = cGui()
    __createCharacters(oGui, 'A', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'B', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'C', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'D', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'E', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'F', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'G', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'H', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'I', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'J', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'K', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'L', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'M', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'N', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'O', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'P', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'Q', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'R', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'S', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'T', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'U', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'V', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'W', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'X', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'Y', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, 'Z', sMediaType, iMediaTypePageId, sSecurityValue)
    __createCharacters(oGui, '0', sMediaType, iMediaTypePageId, sSecurityValue)
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter, sMediaType, iMediaTypePageId, sSecurityValue):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('ajaxCall')
    oGuiElement.setTitle(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('character', sCharacter)
    oOutputParameterHandler.addParameter('mediaType', sMediaType)
    oOutputParameterHandler.addParameter('mediaTypePageId', iMediaTypePageId)
    oOutputParameterHandler.addParameter('securityCockie', sSecurityValue)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __createDisplayStart(iPage):
    return (25 * int(iPage)) - 25

def __createAjaxUrl(sMediaType, iPage, iMediaTypePageId, sCharacter='A'):
    iDisplayStart = __createDisplayStart(iPage)

    oRequestHandler = cRequestHandler(URL_AJAX)
    if (iMediaTypePageId == False):
        #{"fType":"movie","fLetter":"A"}
        oRequestHandler.addParameters('additional', '{"fType":"' + str(sMediaType) + '","fLetter":"' + str(sCharacter) + '"}')
    else:
        #{"foo":"bar","fGenre":"2","fType":"","fLetter":"A"}
        oRequestHandler.addParameters('additional', '{"foo":"bar","' + str(sMediaType) + '":"' + iMediaTypePageId + '","fType":"","fLetter":"' + str(sCharacter) + '"}')

    oRequestHandler.addParameters('bSortable_0', 'true')
    oRequestHandler.addParameters('bSortable_1', 'true')
    oRequestHandler.addParameters('bSortable_2', 'true')
    oRequestHandler.addParameters('bSortable_3', 'false')
    oRequestHandler.addParameters('bSortable_4', 'false')
    oRequestHandler.addParameters('bSortable_5', 'false')
    oRequestHandler.addParameters('bSortable_6', 'true')
    oRequestHandler.addParameters('iColumns', '7')
    oRequestHandler.addParameters('iDisplayLength', '25')
    oRequestHandler.addParameters('iDisplayStart', iDisplayStart)
    oRequestHandler.addParameters('iSortCol_0', '2')
    oRequestHandler.addParameters('iSortingCols', '1')
    oRequestHandler.addParameters('sColumns', '')
    oRequestHandler.addParameters('sEcho', iPage)
    oRequestHandler.addParameters('sSortDir_0', 'asc')
    return oRequestHandler.getRequestUri()

def __parseHosterDefault(sUrl, sHosterName, sHosterFileName, sPattern, sSecurityValue, sMovieTitle):
    if (sPattern == False):
        #sPattern = 'div><a href=\\\\"([^"]+)\\\\'
        sPattern = 'href=\\\\"([^"]+)\\\\" alt=\\\\"Watch\\\\"'

    sUrl = sUrl.replace('&amp;', '&')
    logger.info(sUrl)

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kino.to/')
    sHtmlContent = oRequest.request()

    oParser = cParser()
    aMovieParts = oParser.parse(sHtmlContent, sPattern)

    iCounter = 0
    oGui = cGui()
    if (aMovieParts[0] == True):

        for sPartUrl in aMovieParts[1]:
            sPartUrl = sPartUrl.replace('\\/', '/')
            iCounter = iCounter + 1

            oHoster = cHosterHandler().getHoster(sHosterFileName)
	    if (sMovieTitle != False):
		oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sPartUrl)            

    oGui.setEndOfDirectory()


def __getMovieHoster(sHtmlContent):
    aHosters = []

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'megavideo.com', 'Hoster_2', 'parseMegaVideoCom', 'megavideo')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'duckload.com', 'Hoster_6', 'parseHosterDefault', 'duckload')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'loaded.it (Flash)', 'Hoster_37', 'parseHosterDefault', 'loadedit')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'loaded.it (Divx)', 'Hoster_19', 'parseHosterDefault', 'loadedit')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'sharehoster.com', 'Hoster_3', 'parseHosterDefault', 'sharehoster')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'dataup.to', 'Hoster_8', 'parseHosterDefault', 'dataup')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'quickload.to', 'Hoster_9', 'parseHosterDefault', 'quickload')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'mystream.to (Flash)', 'Hoster_22', 'parseHosterDefault', 'mystream')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'mystream.to (Divx)', 'Hoster_10', 'parseHosterDefault', 'mystream')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'tubeload.to (Flash)', 'Hoster_21', 'parseHosterDefault', 'tubeload')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'tubeload.to (Divx)', 'Hoster_18', 'parseHosterDefault', 'tubeload')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'archive.to (Flash)', 'Hoster_4', 'parseHosterDefault', 'archive')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'archive.to (Divx)', 'Hoster_1', 'parseHosterDefault', 'archive')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'skyload.net (Divx)', 'Hoster_41', 'parseHosterDefault', 'skyload')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'filestage.to', 'Hoster_40', 'parseHosterDefault', 'filestage')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    aHosterItem = __parseHosterSiteFromSite(sHtmlContent, 'fullshare.net', 'Hoster_12', 'parseHosterDefault', 'fullshare')
    if (aHosterItem != False):
        aHosters.append(aHosterItem)

    return aHosters


def __parseHosterSiteFromSite(sHtmlContent, sHosterName, sHosterId, sHosterMethodeName, sHosterFilename):
    aHoster = []
    sRegex = '<li id="' + sHosterId + '".*?rel="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex, 1)
    if (aResult[0] == True):
        sUrl = URL_MIRROR + urllib.unquote_plus(aResult[1][0])
        aHoster.append(sHosterName)
        aHoster.append(sUrl)
        aHoster.append(sHosterMethodeName)
        aHoster.append(sHosterFilename)
        return aHoster

    return False

def __getDescription(sHtmlContent):
    sRegex = '<div class="Descriptore">([^<]+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex, 1)
    if (aResult[0] == True):
            return aResult[1][0]
    return ''

def __getThumbnail(sHtmlContent):
    sRegex = '<div class="Grahpics">.*? src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)
    if (aResult[0] == True):
            return aResult[1][0]
    return ''

def __getDetails(sHtmlContent):
    sRegex = '<li class="DetailDat" title="Director"><span class="Director"></span>(.*?)</li><li class="DetailDat" title="Country"><span class="Country"></span>(.*?)</li><li class="DetailDat" title="Runtime"><span class="Runtime"></span>(.*?)</li><li class="DetailDat" title="Genre"><span class="Genre"></span>(.*?)</li><li class="DetailDat" title="Views"><span class="Views"></span>(.*?)</li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)


    aDetails = {}

    if (aResult[0] == True):
            aDetails['writer'] = aResult[1][0][0]
            aDetails['country'] = aResult[1][0][1]
            aDetails['duration'] = aResult[1][0][2]
            aDetails['genre'] = aResult[1][0][3]
            aDetails['playcount'] = oParser.getNumberFromString(aResult[1][0][4])

    return aDetails