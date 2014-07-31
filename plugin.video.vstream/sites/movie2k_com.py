from resources.lib.util import cUtil
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler


SITE_IDENTIFIER = 'movie2k_com'
SITE_NAME = 'Movie2k.com'

URL_MAIN = 'http://www.movie2k.com/'
URL_TOP_MOVIES = 'http://www.movie2k.com/movies-top.html'
URL_GENRE = 'http://www.movie2k.com/genres-movies.html'
URL_MOVIES_ALL_WITH_CHARACTER = 'http://www.movie2k.com/movies-all'

URL_SERIES = 'http://www.movie2k.com/tvshows_featured.php'
URL_SERIES_ALL = 'http://www.movie2k.com/tvshows-all.html'
URL_SERIES_TOP = 'http://www.movie2k.com/tvshows-top.html'
URL_SERIES_GENRE = 'http://www.movie2k.com/genres-tvshows.html'

URL_SEARCH = 'http://www.movie2k.com/movies.php?list=searchnew534'

def load():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Filme', '', 'showMovieMenu')
    __createMainMenuItem(oGui, 'Serien', '', 'showSeriesMenu')
    __createMainMenuItem(oGui, 'Suche', '', 'showSearch')
    oGui.setEndOfDirectory()

def showMovieMenu():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Kinofilme', URL_MAIN, 'showMoviesAndSeries')
    __createMainMenuItem(oGui, 'Alle Filme', URL_MAIN, 'showCharcacters')
    __createMainMenuItem(oGui, 'Top Filme', URL_TOP_MOVIES, 'parseMovieSimpleList')
    __createMainMenuItem(oGui, 'Genre', URL_GENRE, 'showGenre')
    oGui.setEndOfDirectory()

def showSeriesMenu():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Featured', URL_SERIES, 'showMoviesAndSeries')
    __createMainMenuItem(oGui, 'Alle Serien', URL_SERIES_ALL, 'showAllSeries')
    __createMainMenuItem(oGui, 'Top Serien', URL_SERIES_TOP, 'parseMovieSimpleList')
    __createMainMenuItem(oGui, 'Genre', URL_SERIES_GENRE, 'showGenre')
    oGui.setEndOfDirectory()


def showCharcacters():
    oGui = cGui()
    __createCharacters(oGui, '#')
    __createCharacters(oGui, 'A')
    __createCharacters(oGui, 'B')
    __createCharacters(oGui, 'C')
    __createCharacters(oGui, 'D')
    __createCharacters(oGui, 'E')
    __createCharacters(oGui, 'F')
    __createCharacters(oGui, 'G')
    __createCharacters(oGui, 'H')
    __createCharacters(oGui, 'I')
    __createCharacters(oGui, 'J')
    __createCharacters(oGui, 'K')
    __createCharacters(oGui, 'L')
    __createCharacters(oGui, 'N')
    __createCharacters(oGui, 'O')
    __createCharacters(oGui, 'Q')
    __createCharacters(oGui, 'R')
    __createCharacters(oGui, 'S')
    __createCharacters(oGui, 'T')
    __createCharacters(oGui, 'U')
    __createCharacters(oGui, 'V')
    __createCharacters(oGui, 'W')
    __createCharacters(oGui, 'X')
    __createCharacters(oGui, 'Y')
    __createCharacters(oGui, 'Z')    
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('parseMovieSimpleList')
    oGuiElement.setTitle(sCharacter)

    if (sCharacter == '#'):
        sUrl = URL_MOVIES_ALL_WITH_CHARACTER + '-1-1.html'
    else:
        sUrl = URL_MOVIES_ALL_WITH_CHARACTER + '-' + str(sCharacter) + '-1.html'

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showAllSeries():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        __parseMovieSimpleList(sHtmlContent, 1)

def showSearch():    
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __callSearch(sSearchText)

    oGui.setEndOfDirectory()

def __callSearch(sSearchText):
    oRequest = cRequestHandler(URL_SEARCH)
    oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequest.addParameters('search', sSearchText)
    sHtmlContent = oRequest.request()

    __parseMovieSimpleList(sHtmlContent, 1)
    

def __checkForNextPage(sHtmlContent, iCurrentPage):
    iNextPage = int(iCurrentPage) + 1
    iNextPage = str(iNextPage) + ' '
    
    sPattern = '<a href="([^"]+)">' + iNextPage + '</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
    return False

def showGenre():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<TR>.*?<a href="([^"]+)">(.*?)</a>.*?<TD id="tdmovies" width="50">(.*?)</TD>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieSimpleList')

                sTitle = aEntry[1] + ' (' + aEntry[2] + ')'

                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', URL_MAIN + aEntry[0])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def parseMovieSimpleList():
    oInputParameterHandler = cInputParameterHandler()

    if (oInputParameterHandler.exist('iPage')):
        iPage = oInputParameterHandler.getValue('iPage')
    else:
        iPage = 1

    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        __parseMovieSimpleList(sHtmlContent, iPage)

def __parseMovieSimpleList(sHtmlContent, iPage):
    oGui = cGui()
    sPattern = '<TR>.*?<a href="([^"]+)">(.*?)</a>.*?<img border=0 src="http://www.movie2k.com/img/(.*?).png'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHoster')

            sTitle = aEntry[1].strip().replace('\t', '') +  __getLanmguage(aEntry[2])
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', aEntry[0])
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    sNextUrl = __checkForNextPage(sHtmlContent, iPage)    
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('parseMovieSimpleList')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sUrl', sNextUrl)
        oOutputParameterHandler.addParameter('iPage', int(iPage) + 1)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesAndSeries():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')


        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<div style="float:left"><a href="([^"]+)".{0,1}><img src="([^"]+)".*?alt="([^"]+)".*?<img src="http://www.movie2k.com/img/(.*?).png"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHoster')

                sThumbnail = URL_MAIN + aEntry[1]
                oGuiElement.setThumbnail(sThumbnail)

                sTitle = aEntry[2].strip().replace('kostenlos', '') +  __getLanmguage(aEntry[3])
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', aEntry[0])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __createInfo(oGui, sHtmlContent):
    sPattern = '<img src="thumbs/([^"]+)".*?<div class="beschreibung">(.*?)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(URL_MAIN + 'thumbs/' + str(aEntry[0]))
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(cUtil().removeHtmlTags(str(aEntry[1])))
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def showHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        __createInfo(oGui, sHtmlContent)
        
        sPattern = '<tr id="tablemoviesindex2">.*?<a href="([^"]+)">([^<]+)<.*?width="16">(.*?)</a>.*?alt="([^"]+)"'
        #sPattern = '<tr id="tablemoviesindex2">.*?<a href="([^"]+)">.*?width="16">(.*?)</a>.*?alt="([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHoster = aEntry[2].strip()
                if (__checkHoster(sHoster) == True):

                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('parseHoster')

                    sTitle = aEntry[1] + ' - ' + aEntry[2] + ' - ' + aEntry[3]
                    oGuiElement.setTitle(sTitle)

                    sUrl = URL_MAIN + aEntry[0]
                    
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sTitle', sTitle)
                    oOutputParameterHandler.addParameter('sHoster', sHoster)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkHoster(sHoster):
    if (sHoster == 'Mystream'):
        return True

    if (sHoster == 'loaded.it'):
        return True

    if (sHoster == 'Novamov'):
        return True

    if (sHoster == 'Stream2k'):
        return True

    #if (sHoster == 'UploadC'):
    #    return True

    #if (sHoster == 'Loombo'):
    #    return True

    if (sHoster == 'VideoWeed'):
        return True

    if (sHoster == 'Streamesel'):
        return True

    if (sHoster == 'MegaVideo'):
        return True

    if (sHoster == 'Duckload'):
        return True

    if (sHoster == 'Movshare'):
        return True

    if (sHoster == 'FileStage'):
        return True

    if (sHoster == 'Tubeload'):
        return True

    if (sHoster == 'Screen4u'):
        return True

    if (sHoster == 'CheckThisV'):
        return True

    if (sHoster == 'Xvidstage'):
        return True

    if (sHoster == 'DivX Hoste'):
        return True

    return False

def __getMovieTitle(sHtmlContent):
    sPattern = '<h1 style="font-size:18px;">(.*?)<img'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
	return str(aResult[1][0]).strip()

    return False

def parseHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sHoster')):
        sUrl = oInputParameterHandler.getValue('sUrl')
	        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

	sMovieTitle = __getMovieTitle(sHtmlContent)

        bFoundHoster = __getHosterFile(oGui, 'mystream', 'http://www.mystream.to/', '<a href="http://www.mystream.to/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'loadedit', 'http://loaded.it/', '<a href="http://loaded.it/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'novamov', 'http://www.novamov.com/', "src='http://www.novamov.com/([^']+)'", sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'stream2k', 'http://www.stream2k.com/', '<param name="flashvars" value="config=.*?stream2k.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'videoweed', 'http://www.videoweed.com/', 'src="http://www.videoweed.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'streamesel', 'http://www.streamesel.com/', '<a href="http://www.streamesel.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'megavideo', False, 'value="http://www.megavideo.com/v/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'duckload', 'http://www.duckload.com/', '<a href="http://duckload.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'duckload', 'http://www.duckload.com/', '<a href="http://www.duckload.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'movshare', 'http://www.movshare.net/', 'src="http://www.movshare.net/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'movshare', 'http://www.movshare.net/', 'src="http://movshare.net/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'filestage', 'http://www.filestage.to/', '<a href="http://www.filestage.to/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'tubeload', 'http://www.tubeload.to/', '<a href="http://www.tubeload.to/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'screen4u', 'http://www.screen4u.net/', '<a href="http://www.screen4u.net/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'checkthisvid', 'http://www.checkthisvid.com/', '<a href="http://www.checkthisvid.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return
             
        bFoundHoster = __getHosterFile(oGui, 'xvidstage', 'http://xvidstage.com/', '<a href="http://xvidstage.com/([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        bFoundHoster = __getHosterFile(oGui, 'filezup', 'http://www.filezup.com', '<a href="http://www.filezup.com([^"]+)"', sHtmlContent, sMovieTitle)
        if (bFoundHoster == True):
            return

        

        '''
         Uploadc.com MUSS >NOCH
        if (sHoster == 'UploadC'):
            sPattern = '<a href="http://uploadc.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://uploadc.com/' + aResult[1][0]
                __play('uploadc', sStreamUrl, sTitle, bDownload)
                return

        # Loombo.com MUSS NOCH
        if (sHoster == 'Loombo'):
            sPattern = '<a href="http://loombo.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://loombo.com/' + aResult[1][0]
                __play('loombo', sStreamUrl, sTitle, bDownload)
                return'''

def __getHosterFile(oGui, sHoster, sUrl, sPattern, sHtmlContent, sMovieTitle):
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        if (sUrl == False):
            sStreamUrl = aResult[1][0]
        else:
            sStreamUrl = sUrl + aResult[1][0]

        oHoster = cHosterHandler().getHoster(sHoster)
	if (sMovieTitle != False):
	    oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sStreamUrl)
        oGui.setEndOfDirectory()
        return True

    return False

def __getLanmguage(sString):
    if (sString == 'us_ger_small'):
        return ' (DE)'
    return ' (EN)'

def __createMainMenuItem(oGui, sTitle, sUrl, sFunction):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)    
    oGui.addFolder(oGuiElement, oOutputParameterHandler)