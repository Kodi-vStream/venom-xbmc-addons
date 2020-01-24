#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'streamingdivx'
SITE_NAME = 'Streamingdivx'
SITE_DESC = 'Films VF en streaming.'

URL_MAIN = 'https://ww1.streamingdivx.ch/'

MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')


URL_SEARCH = (URL_MAIN + '/recherche?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/recherche?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Action', sUrl + 'action/'] )
    liste.append( ['Animation', sUrl + 'animation/'] )
    liste.append( ['Aventure', sUrl + 'aventure/'] )
    liste.append( ['Biopic', sUrl + 'biopic/'] )
    liste.append( ['Comédie', sUrl + 'comedie/'] )
    liste.append( ['Comédie-dramatique', sUrl + 'comedie-dramatique/'] )
    liste.append( ['Comédie-musicale', sUrl + 'comedie-musicale/'] )
    liste.append( ['Documentaire', sUrl + 'documentaire/'] )
    liste.append( ['Drame', sUrl + 'drame/'] )
    liste.append( ['Divers', sUrl + 'divers/'] )
    liste.append( ['Epouvante Horreur', sUrl + 'epouvante-horreur/'] )
    liste.append( ['Famille', sUrl + 'famille/'] )
    liste.append( ['Fantastique', sUrl + 'fantastique/'] )
    liste.append( ['Guerre', sUrl + 'guerre/'] )
    liste.append( ['Opera', sUrl + 'opera/'] )
    liste.append( ['Policier', sUrl + 'policier/'] )
    liste.append( ['Romance', sUrl + 'romance/'] )
    liste.append( ['Science-fiction', sUrl + 'science-fiction/'] )
    liste.append( ['Thriller', sUrl + 'thriller/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ','+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="short-images.+?<a href="([^"]+)" title="([^"]+)" class=.+?<img src="([^"]+)".+?(?:<div class="short-content">|<a href=.+?qualite.+?>([^<>]+?)</a>.+?<a href=.+?langue.+?>([^<]+)<\/a>)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            sTitle = aEntry[1].replace('Streaming', '').replace('streaming', '').replace('série', '')

            # sTitle = sTitle.decode('utf-8').encode("latin-1")


            sThumb = aEntry[2]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sQual = ''
            if aEntry[3]:
                sQual = aEntry[3]

            sLang = ''
            if aEntry[4]:
                sLang = aEntry[4]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'series/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "pages-next\"><a href='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        if aResult[1][0].startswith('/'):
            return URL_MAIN[:-1] + aResult[1][0]
        else:
            return aResult[1][0]

    return False

def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #syno
    sDesc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<div class="short-images.+?<a href="([^"]+)" class="short-images.+?<img src="([^"]+)" alt="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2].replace('Streaming', '').replace('streaming', '').replace('série', '')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEp', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEp():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="episode-list">', 'Series similaires')

    sPattern = '<div class="sai.+?<a href="([^"]+)".+?<span>(.+?)<\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + 'series/' + sUrl

            sTitle = aEntry[1]

            sDisplayTitle = ('%s %s') % (sMovieTitle, sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks():
    #streamer.php?p=169&c=V1RJeGMxcHVSbmhhUnpGMFltNU9kMWxYVW5sWlVUMDk=
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    #syno
    sDesc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern2 = '<li class="stream.+?"><div data-num=".+?" data-code=".+?".+?<i class="([^"]+)">.+?<img *src="([^"]+)".+?<input name="levideo" value="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern2)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHost = aEntry[0].replace('server player-', '').capitalize()
            sLang = aEntry[1].split('/')[-1].replace('.png', '')

            sDisplayTitle = ('%s (%s) [COLOR %s]%s[/COLOR]') % (sMovieTitle, sLang, sColor, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('datacode', aEntry[2])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    datacode = oInputParameterHandler.getValue('datacode')

    if not sUrl[:11] == URL_MAIN[:11]:
        sUrl = re.sub(sUrl[:11],URL_MAIN[:11],sUrl)


    # import urllib2

    # sUrl = ('%s%s%s%s%s' % (URL_MAIN, 'streamer.php?p=', datanum, '&c=', datacode))
    
    # class NoRedirection(urllib2.HTTPErrorProcessor):
            # def http_response(self, request, response):
                # return response

            # https_response = http_response

    # opener = urllib2.build_opener(NoRedirection)
    # opener.addheaders = [('User-Agent', UA)]
    # opener.addheaders = [('Referer', URL_MAIN)]
    # response = opener.open(sUrl)
    # response.close()
    # if response.code == 302:
        # redirection_target = response.headers['Location']
        # if redirection_target:

            # sHosterUrl = redirection_target

    oParser = cParser()        
    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')

    oRequest.addParametersLine('levideo=' + datacode)

    sHtmlContent = oRequest.request()

    sPattern = '<iframe id=.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHosterUrl = aResult[1][0]
    
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        oGui.setEndOfDirectory()
