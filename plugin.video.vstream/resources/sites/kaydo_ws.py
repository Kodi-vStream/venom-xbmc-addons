#-*- coding: utf-8 -*-
#Venom & johngf.
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,xbmc,base64

#copie du site http://www.film-streaming.co/
#copie du site http://www.streaming-club.com/
#copie du site http://www.hd-stream.in/
#copie du site http://www.kaydo.ws/

SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo'
SITE_DESC = 'Site de streaming en HD 720p 100% Gratuit'

URL_MAIN = 'http://www.kaydo.ws/'

MOVIE_NEWS = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'populaires.php', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'best-rating.php', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'top-films.php', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_NEWS = (URL_MAIN + 'series-latest.php', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series.php', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

URL_SEARCH = (URL_MAIN + 'search.php?q=', 'sHowResultSearch')
URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?q=', 'sHowResultSearch')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?q=', 'sHowResultSearch')
FUNCTION_SEARCH = 'sHowResultSearch'

def Decode(chain):
    chain = 'aHR' + chain
    chain = 'M'.join(chain.split('7A4c1Y9T8c'))
    chain = 'V'.join(chain.split('8A5d1YX84A428s'))
    chain = ''.join(chain.split('$'))

    return base64.b64decode(chain)

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Top Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText
        sHowResultSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def sHowResultSearch(sSearch = ''):
    oGui = cGui()

    sUrl = sSearch

    oParser = cParser()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="login-box">(.+?)<footer class="page-footer center">'
    aResult = re.search(sPattern,sHtmlContent,re.DOTALL)
    if (aResult):
        sHtmlContent = aResult.group(1)

    sPattern = '<a href="([^"]+)"><img src="([^"]+).+?class="name">(.+?)<\/a>.+?class="genre">([^<]+)<\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = URL_MAIN+aEntry[0]
            sThumb = URL_MAIN+aEntry[1]
            sCom = aEntry[3]
            sTitle = ('%s (%s)') % (str(aEntry[2]) , str(aEntry[3]).replace(' - ', ' '))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[2])
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovieGenres():
    oGui = cGui()

    liste = []


    liste.append( ['Action',URL_MAIN + 'films.php?s=go&sort=add&g=Action'] )
    liste.append( ['Animation',URL_MAIN + 'films.php?s=go&sort=add&g=Animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films.php?s=go&sort=add&g=Arts%20Martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'films.php?s=go&sort=add&g=Aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'films.php?s=go&sort=add&g=Biopic'] )
    liste.append( ['Comédie',URL_MAIN + 'films.php?s=go&sort=add&g=Com%C3%A9die'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'films.php?s=go&sort=add&g=Com%C3%A9die%20dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + 'films.php?s=go&sort=add&g=Documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'films.php?s=go&sort=add&g=Drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'films.php?s=go&sort=add&g=Epouvante-horreur'] )
    liste.append( ['Espionnage',URL_MAIN + 'films.php?s=go&sort=add&g=Espionnage'] )
    liste.append( ['Fantastique',URL_MAIN + 'films.php?s=go&sort=add&g=Fantastique'] )
    liste.append( ['Famille',URL_MAIN + 'films.php?s=go&sort=add&g=Famille'] )
    liste.append( ['Guerre',URL_MAIN + 'films.php?s=go&sort=add&g=Guerre'] )
    liste.append( ['Historique',URL_MAIN + 'films.php?s=go&sort=add&g=Historique'] )
    liste.append( ['Musical',URL_MAIN + 'films.php?s=go&sort=add&g=Musical'] )
    liste.append( ['Policier',URL_MAIN + 'films.php?s=go&sort=add&g=Policier'] )
    liste.append( ['Romance',URL_MAIN + 'films.php?s=go&sort=add&g=Romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'films.php?s=go&sort=add&g=Science%20fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'films.php?s=go&sort=add&g=Thriller'] )
    liste.append( ['Western',URL_MAIN + 'films.php?s=go&sort=add&g=Western'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'series.php?g=Action'] )
    liste.append( ['Animation',URL_MAIN + 'series.php?g=Animation'] )
    liste.append( ['Aventure',URL_MAIN + 'series.php?g=Aventure'] )
    liste.append( ['Comédie',URL_MAIN + 'series.php?g=Com%C3%A9die'] )
    liste.append( ['Drame',URL_MAIN + 'series.php?g=Drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'series.php?g=Epouvante-horreur'] )
    liste.append( ['Fantastique',URL_MAIN + 'series.php?g=Fantastique'] )
    liste.append( ['Historique',URL_MAIN + 'series.php?g=Historique'] )
    liste.append( ['Judiciaire',URL_MAIN + 'series.php?g=Judiciaire'] )
    liste.append( ['Policier',URL_MAIN + 'series.php?g=Policier'] )
    liste.append( ['Romance',URL_MAIN + 'series.php?g=Romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'series.php?g=Science%20fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'series.php?g=Thriller'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    # modif url par Gregwar
    if '?' in sUrl:
        sUrl += '&r=n'
    else:
        sUrl += '?r=n'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    sPattern1 = '<img src="([^"]+?)" width=".+?<h2>(.+?)</h2>.*?<h3>(.+?)</h3>.+?<p>([^<]+)</p><a class="btn.+?href="(.+?)"'

    sPattern2 = '<img src="([^"]+)" width=".+?<a href="([^"]+)">.+?title="(.+?)".+?data-tooltip="Synopsis *: *([^<]+)">.+?<h3>(.+?)</h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern2)

    if not (aResult[0] == True):
        aResult = oParser.parse(sHtmlContent, sPattern1)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if  'genre' in sUrl:

                sThumbnail = URL_MAIN + str(aEntry[0])
                siteUrl = URL_MAIN + str(aEntry[4])
                sCom = str(aEntry[3])
                sTitle = ('%s (%s)') % (str(aEntry[1]) , str(aEntry[2]).replace(' - COMP', 'COMP'))
                title = aEntry[1]
            else:
                sThumbnail = URL_MAIN + str(aEntry[0])
                siteUrl = URL_MAIN + str(aEntry[1])
                sCom = str(aEntry[3])
                sTitle = ('%s (%s)') % (str(aEntry[2]) , str(aEntry[4]))
                title = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', title)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if 'details-serie.php' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, 'series.png', sThumbnail, sCom, oOutputParameterHandler)
            elif '/series' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'class="pagination">.*?<li class="active">.+?<li><a href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = URL_MAIN + aResult[1][0]
        return sUrl

    return False

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<img src="([^"]+)" width=".+?<span class.+?>(.+?)<\/span>.+?<a href="([^"]+)">.+?<h2>(.+?)</h2>.*?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sThumbnail = URL_MAIN + str(aEntry[0])
            siteUrl = URL_MAIN + str(aEntry[2])
            sCom = str(aEntry[4])
            sTitle = ('%s (%s) (%s)') % (sMovieTitle , str(aEntry[1].replace(' COMP', 'COMP')), str(aEntry[4]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def seriesHosters():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #modif url par Gregwar
    if '?' in sUrl:
        sUrl += '&r=n'
    else:
        sUrl += '?r=n'
    oRequestHandler = cRequestHandler(sUrl + '&ep=0')
    sHtmlContent = oRequestHandler.request();


    oParser = cParser()
    result = re.search('^(.+?)(|col s4 hide-on-med-and-down(.+?))$', sHtmlContent, re.DOTALL)

    result.group(1)

    sHtmlContent = result.group(1)
    sPattern = '<div class="truncate.+?</i>(.+?)</div>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)


    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if 'ep=0&' in aEntry[1]:
                continue

            links = []
            result = re.search('href="(.+?ver=vf)"', aEntry[1])
            if result:
                links += [['VF', result.group(1)]]
            result = re.search('href="(.+?ver=vo)"', aEntry[1])
            if result:
                links += [['VOST', result.group(1)]]

            for t, link in links:
                oOutputParameterHandler = cOutputParameterHandler()
                sUrl = URL_MAIN+'/series/'+link+'&r=n'
                #name = aEntry[0] + ' ('+t+')'
                name = ('%s (%s)') % (aEntry[0], t)

                name = name.replace('Ep. ','E')

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

                oGui.addTV(SITE_IDENTIFIER, 'showHosters', name, 'series.png', sThumbnail, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail  = oInputParameterHandler.getValue('sThumbnail')

    #modif url par Gregwar
    if 'r=n' not in sUrl:
        if '?' in sUrl:
            sUrl += '&r=n'
        else:
            sUrl += '?r=n'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<video><source type="video/mp4" src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        BA = aResult[1][0]
    else:
        BA = False

    sPattern = '<script>\s*function [a-zA-Z]{2}\(\)(.+?)</script>'
    aResult = re.search(sPattern,sHtmlContent,re.DOTALL)

    sHtmlContent = aResult.group(1).replace('return de("$")','') #serie
    #redirection sur hdstream pour les new videos
    sPattern = '"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            url = Decode(str(aEntry))
            if 'manifest.mpd' in url:
                continue

            if '/mp4/' in url: #lien upto,1fich,direct ou inutilisable
                sId = re.search('\/mp4\/([^-]+)',url)
                if sId:
                    chaine = sId.group(1)
                    vUrl = base64.b64decode(chaine + "==")

                    if 't411.li' in vUrl:
                        continue
                    elif 'uptobox' in vUrl:
                        sHosterUrl = vUrl
                    elif '1fichier' in vUrl:
                        sHosterUrl = vUrl
                    else:
                        sHosterUrl = url

            else:
                sHosterUrl = url

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(xbmc.getInfoLabel('ListItem.title'))
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

        if (BA != False):
            sHosterUrl2 = str(BA)
            oHoster2 = cHosterGui().checkHoster(sHosterUrl2)
            if (oHoster2 != False):
                oHoster2.setDisplayName(sMovieTitle + '[COLOR coral]' + (' [Bande Annonce] ') + '[/COLOR]')
                oHoster2.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster2, sHosterUrl2, '')

    oGui.setEndOfDirectory()
