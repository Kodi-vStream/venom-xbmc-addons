from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'anime_proxer_me'
SITE_NAME = 'Anime.Proxer.Me'

URL_MAIN = 'http://anime.proxer.me'
URL_ANIME_LIST = 'http://anime.proxer.me/animeliste.html'
URL_MOVIES = 'http://anime.proxer.me/movies.html'
URL_OVA = 'http://anime.proxer.me/ova.html'
URL_SEARCH = 'http://anime.proxer.me/animesuche.html?set=suche&sprache=alle&genre='

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_ANIME_LIST)
    oOutputParameterHandler.addParameter('nextFunction', 'showSeries')
    __createMenuEntry(oGui, 'showCharacters', 'Animes von A - Z', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIES)
    oOutputParameterHandler.addParameter('nextFunction', 'showMovies')
    __createMenuEntry(oGui, 'showCharacters', 'Movies', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_OVA)
    oOutputParameterHandler.addParameter('nextFunction', 'showOvas')
    __createMenuEntry(oGui, 'showCharacters', 'Ovas', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH)    
    __createMenuEntry(oGui, 'showSearch', 'Suche', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText.replace(' ', '+')
        sUrl = URL_SEARCH + '&name=' + sSearchText        
        __parseList(sUrl, 'getAvaiableTypes')

    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCharacters():
    oInputParameterHandler = cInputParameterHandler()    
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    sNextFunction = oInputParameterHandler.getValue('nextFunction')

    oGui = cGui()
    __createCharacters(oGui, '0-9', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'A', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'B', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'C', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'D', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'E', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'F', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'G', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'H', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'I', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'J', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'K', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'L', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'N', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'O', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'Q', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'R', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'S', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'T', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'U', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'V', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'W', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'X', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'Y', sSiteUrl, sNextFunction)
    __createCharacters(oGui, 'Z', sSiteUrl, sNextFunction)

    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter, sSiteUrl, sNextFunction):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('parseList')
    oGuiElement.setTitle(sCharacter)

    sUrl = sSiteUrl + '?set=abc&abc=' + str(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('nextFunction', sNextFunction)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def parseList():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sNextFunction = oInputParameterHandler.getValue('nextFunction')
    __parseList(sUrl, sNextFunction)

def __parseList(sUrl, sNextFunction):
    oGui = cGui()
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('\\', '')
    
    sPattern = '<tr  align=left onmouseover="Tip\(\'<img src=\\\'(.*?)\'.*?<td ><a href="([^"]+)".*?>(.*?)</a></td><td>.*?</td><td>(.*?)</td><td>.*?</td><td>(.*?)</td></tr>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction(sNextFunction)
            oGuiElement.setThumbnail(str(aEntry[0]))

            sTitle = cUtil().removeHtmlTags(aEntry[2])
            sTitle = sTitle + ' SUBS(' + __getLanguage(str(aEntry[3])) + ')'
            sTitle = sTitle + ' DUBS(' + __getLanguage(str(aEntry[4])) + ')'

            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()            
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[1]).replace('#top', ''))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getAvaiableTypes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl.replace('&amp;', '&')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = 'top">SERIE</a>(.*?)>'
    __getAvaiableTypes(oGui, sUrl, sHtmlContent, sPattern, 'Serie', 'showSeries')
    
    sPattern = 'top">MOVIE</a>(.*?)>'
    __getAvaiableTypes(oGui, sUrl, sHtmlContent, sPattern, 'Movie', 'showMovies')

    sPattern = 'top">OVA</a>(.*?)>'
    __getAvaiableTypes(oGui, sUrl, sHtmlContent, sPattern, 'Ova', 'showOvas')

    oGui.setEndOfDirectory()

def __getAvaiableTypes(oGui, sUrl, sHtmlContent, sPattern, sTitle, sNextFunction):
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction(sNextFunction)
        oGuiElement.setTitle(sTitle)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('showSeries', sNextFunction)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showSeries():    
    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
	iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl + '&medium=serie'    
    __parseMediaSite(sUrl, iPage)

def showMovies():
    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
	iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl + '&medium=movie'    
    __parseMediaSite(sUrl, iPage)

def showOvas():
    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
	iPage = oInputParameterHandler.getValue('page')

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl + '&medium=ova'    
    __parseMediaSite(sUrl, iPage)

def showNextPage():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    iPage = 1
    if (oInputParameterHandler.exist('page')):
	iPage = oInputParameterHandler.getValue('page')

    __parseMediaSite(sUrl, iPage)

def __parseMediaSite(sUrl, iPage):
    sCurrentUrl = sUrl + '&page=' + str(iPage)
    
    oGui = cGui()
    oRequestHandler = cRequestHandler(sCurrentUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'id="box-table-a"(.*?)</table>'  

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        sPattern = 'id=box-table-a(.*?)</table>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)        

    if (aResult[0] == True):
        sHtmlContent2 = aResult[1][0]

        sPattern = '</tr><tr><td>(.*?)</td><td align=left>(.*?)</td>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent2, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHoster')

                sTitle = str(aEntry[0]) + '.' + cUtil().removeHtmlTags(aEntry[1])
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sCurrentUrl)
                oOutputParameterHandler.addParameter('number', str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

	if (__checkFoxNextSite(iPage, sHtmlContent) == True):
	    oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showNextPage')
	    oGuiElement.setTitle('next ..')
	    oOutputParameterHandler = cOutputParameterHandler()
	    oOutputParameterHandler.addParameter('siteUrl', sUrl)
	    oOutputParameterHandler.addParameter('page', str(int(iPage) + 1))
	    oGui.addFolder(oGuiElement, oOutputParameterHandler)
	    

    oGui.setEndOfDirectory()

def __checkFoxNextSite(iCurrentPage, sHtmlContent):
    iNextSite = int(iCurrentPage) + 1;
    sPattern = 'page=' + str(iNextSite) + '.*?>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
	return True

    return False;

def showHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sNumber = oInputParameterHandler.getValue('number')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<td>' + str(sNumber) + '</td>(.*?)</tr>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
        
    if (aResult[0] == True):
        sHtmlContent = str(aResult[1][0])
        
        sPattern = '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oHoster = __checkHoster(str(aEntry[1]))
                if (oHoster != False):

                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('getMovieUrl')

                    sTitle = oHoster.getDisplayName() + __getLanguageFromUrl(str(aEntry[0]))
                    oGuiElement.setTitle(sTitle)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]).replace('#top', ''))
                    oOutputParameterHandler.addParameter('hosterIdentifier', oHoster.getPluginIdentifier())
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def getMovieUrl():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHosterIdentifier = oInputParameterHandler.getValue('hosterIdentifier')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<br><br><script type="text/javascript" src="([^"]+)"></script><br>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sMovieUrl = aResult[1][0]
                
        oRequestHandler = cRequestHandler(sMovieUrl)
        sHtmlContent = oRequestHandler.request();
        sPattern = '<embed src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sMovieUrl = aResult[1][0]
            
            oHoster = cHosterHandler().getHoster(sHosterIdentifier)            
            cHosterGui().showHoster(oGui, oHoster, sMovieUrl)


    oGui.setEndOfDirectory()
        

def __getLanguageFromUrl(sUrl):
    sPattern = 'sprache=(.*?)&'
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        return ' - ' + str(aResult[1][0])

    return ''    

def __checkHoster(sHosterName):
    sHosterName = sHosterName.lower()

    if (sHosterName.endswith('rutube.png')):
        return cHosterHandler().getHoster('rutube')

    if (sHosterName.endswith('megavideo.png')):
        return cHosterHandler().getHoster('megavideo')

    #if (sHosterName.endswith('play.png')):
    #    return cHosterHandler().getHoster('sevenload') oder 4shared

    return False

def __getLanguage(sHtmlContent):
    sResult = ''

    sPattern = 'german(.*?).gif'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if (sResult != ''):
            sResult = sResult + ', '
        sResult = sResult + 'de'

    sPattern = 'english(.*?).gif'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if (sResult != ''):
            sResult = sResult + ', '
        sResult = sResult + 'en'
        
    return sResult


