# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote
import re


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'

SITE_IDENTIFIER = 'tvseriestreaming'
SITE_NAME = 'Tv_seriestreaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = 'https://seriestreamingtv.com/'  #https://seriestreaming.co/

SERIE_SERIES = ('http://', 'load')
SERIE_VIEWS = (URL_MAIN + 'la-top-des-meilleures-serie', 'showMovies')
SERIE_COMMENT = (URL_MAIN + 'meilleurs-serie-populaire-streaming', 'showMovies')
SERIE_LIST = (URL_MAIN, 'showAZ')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH_SERIES = ('', 'searchSerie')

FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENT[1], 'Séries (Populaire)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Series (Liste)', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        searchSerie(sSearchText)
        oGui.setEndOfDirectory()
        return

def showSerieYears():
    #for i in itertools.chain(xrange(5, 7), [8, 9]): afficher dans l'ordre (pense bete ne pas effacer)
    oGui = cGui()
    from itertools import chain
    generator = chain([1936, 1940, 1941, 1950, 1955], xrange(1958, 2021))#desordre

    for i in reversed(list(generator)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()

    for i in range(0, 27):
        if (i < 1):
            sLetter = '\d+'
            aLetter = '0-9'
        else:
            sLetter = chr(64 + i)
            aLetter = sLetter

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sLetter', sLetter)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', "%s [COLOR coral]%s[/COLOR]" % ("Lettre", aLetter), 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaDisplay():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sLetter = oInputParameterHandler.getValue('sLetter')

    oRequestHandler = cRequestHandler(URL_MAIN + 'acceuils-2')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, '<h1>Listes des séries:</h1>', '<div class="container"><br>')

    sPattern = '<a title="(' + sLetter + '.+?)" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        
        series = []
        
        for aEntry in aResult[1]:
            sTitle = aEntry[0].replace('en streaming', '')
            sUrl = aEntry[1]
            series.append((sTitle, sUrl))
            
        # Trie des séries par ordre alphabétique
        series = sorted(series, key=lambda serie: serie[0])
        
        for sTitle,sUrl in series:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showS_E', sTitle, 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def searchSerie(sSearch):
    oGui = cGui()
    oParser = cParser()
    sSearch = Unquote(sSearch)

    oRequestHandler = cRequestHandler(URL_MAIN + 'acceuils-2')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, '<h1>Listes des séries:</h1>', '<div class="container"><br>')

    sPattern = '<a title="([^"]*' + sSearch + '.*?)\" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[0].replace('en streaming', '')
            sUrl = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showS_E', sTitle, 'series.png', oOutputParameterHandler)

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'category/action'] )
    liste.append( ['Animation', URL_MAIN + 'category/animation'] )
    liste.append( ['Anime', URL_MAIN + 'category/anime'] )
    liste.append( ['Aventure', URL_MAIN + 'category/adventure'] )
    liste.append( ['Biographie', URL_MAIN + 'category/biography'] )
    liste.append( ['Comédie', URL_MAIN + 'category/comedy'] )
    liste.append( ['Crime', URL_MAIN + 'category/crime'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentary'] )
    liste.append( ['Drama', URL_MAIN + 'category/drama'] )
    liste.append( ['Drame', URL_MAIN + 'category/drame'] )
    liste.append( ['Enfants', URL_MAIN + 'category/children'] )
    liste.append( ['Famille', URL_MAIN + 'category/family'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/fantasy'] )
    liste.append( ['Guerre', URL_MAIN + 'category/war'] )
    liste.append( ['Historique', URL_MAIN + 'category/history'] )
    liste.append( ['Horreur', URL_MAIN + 'category/horror'] )
    liste.append( ['Music', URL_MAIN + 'category/music'] )
    liste.append( ['Musical', URL_MAIN + 'category/musical'] )
    liste.append( ['Mystère', URL_MAIN + 'category/mystere'] )
    liste.append( ['Policier', URL_MAIN + 'category/policier'] )
    liste.append( ['Réalité', URL_MAIN + 'category/reality'] )
    liste.append( ['Réalité-tv', URL_MAIN + 'category/reality-tv'] )
    liste.append( ['Romance', URL_MAIN + 'category/romance'] )
    liste.append( ['Sci-fi', URL_MAIN + 'category/sci-fi'] )
    liste.append( ['Science-fiction', URL_MAIN + 'category/science-fiction'] )
    liste.append( ['Soap', URL_MAIN + 'category/soap'] )
    liste.append( ['Sport', URL_MAIN + 'category/sport'] )
    liste.append( ['Super-hero', URL_MAIN + 'category/superhero'] )
    liste.append( ['Suspense', URL_MAIN + 'category/suspense'] )
    liste.append( ['Thriller', URL_MAIN + 'category/thriller'] )
    liste.append( ['Western', URL_MAIN + 'category/western'] )
    liste.append( ['Autre', URL_MAIN + 'category/na'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #news
    if 'dernieres-et-meilleures-series-en-streaming' in sUrl:
        sPattern = '<a href="([^"]+)" class="list-group-item.+?>(.+?)<b>(.+?)</b>'
        sHtmlContent = oParser.abParse(sHtmlContent, "<h4>Les derniers episodes", "les plus vues")
    #reste
    else:
        sPattern = '<a class="image" title="(.+?)" href="([^"]+)".+?src="([^"]+)">'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if 'dernieres-et-meilleures-series-en-streaming' in sUrl:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]#.replace(' -', ' ') + aEntry[2].replace(' ', '')
                sThumb = 'news.png'
            else:
                sTitle = aEntry[0].replace('Streaming', '')
                sUrl2 = aEntry[1]
                sThumb = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'dernieres-et-meilleures-series-en-streaming' in sUrl:
                oGui.addDir(SITE_IDENTIFIER, 'showLink', sTitle, sThumb, oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showS_E', sTitle, '', sThumb, '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page-link" href="([^"]+)" rel="next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showS_E():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    rUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(rUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class=".+?src="(http.+?(?:.jpe*g|.png))|<a class="btn btn-primary btn-blo.+?" href="([^"]+)">(.+?)<\/a><\/div>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if '/saison/' in rUrl:#episode
                if aEntry[0]:
                    sThumb = aEntry[0]

                else:
                    sUrl = aEntry[1]
                    sTitle = sMovieTitle + ' ' + aEntry[2]

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oGui.addTV(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler)

            else:#saison
                if aEntry[0]:
                    sThumb = aEntry[0]

                else:
                    sUrl = aEntry[1]
                    sTitle = sMovieTitle + ' ' + aEntry[2]

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addTV(SITE_IDENTIFIER, 'showS_E', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sThumb = ''
    try:
        sPattern = '<img class=".+?" src="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sThumb = aResult[1][0]
    except:
        pass

    sPattern = '<\/i> *Lien.+?</td>.+?alt="([^"]+)".+?(?:|center">([^<]+)</td>.+?)(?:|data-uid="([^"]+)") data-id="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHost = aEntry[0].replace('www.', '')
            sHost = re.sub('\..+', '', sHost).capitalize()

            if aEntry[2] == '':
                sUrl = URL_MAIN + 'll/captcha?hash=' + aEntry[3]
            else:
                sUrl = URL_MAIN + 'll/captcha?hash=' + aEntry[3]

            sLang = aEntry[1].replace(' ', '')
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)

    oRequest.request()
    sHosterUrl = oRequest.getRealUrl()

    if sHosterUrl:
        oHoster = cHosterGui().checkHoster(sHosterUrl)

        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
