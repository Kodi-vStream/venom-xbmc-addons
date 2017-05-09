#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,urllib,base64

SITE_IDENTIFIER = 'papystreaming_org'
SITE_NAME = 'Papystreaming'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = 'http://papystreaming.org/'

MOVIE_NEWS = (URL_MAIN + 'nouveaux-films/','showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-streaming/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'populaire/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'de-visite/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'de-vote/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'series-streaming/', 'showSeries')
SERIE_COMMENTS = (URL_MAIN + 'populaire/', 'showSeries')
SERIE_VIEWS = (URL_MAIN + 'de-visite/', 'showSeries')
SERIE_NOTES = (URL_MAIN + 'de-vote/', 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH2 = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
#serie et film melangé sur certaine fonction tri obligatoire qui bloque l'optimisation
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = { 'User-Agent' : UA }

def load():
    oGui = cGui()
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSSearch', 'Recherche Série', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'films_comments.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'films_notes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus commentées)', 'series_comments.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'series_views.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux notées)', 'series_notes.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'category/action/'] )
    liste.append( ['Animation',URL_MAIN + 'category/animation/'] )
    liste.append( ['Aventure',URL_MAIN + 'category/aventure/'] )
    liste.append( ['Comédie',URL_MAIN + 'category/comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'category/crime/'] )
    liste.append( ['Documentaire',URL_MAIN + 'category/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'category/drame/'] )
    liste.append( ['Etranger',URL_MAIN + 'category/etranger/'] )
    liste.append( ['Familial',URL_MAIN + 'category/familial/'] )
    liste.append( ['Fantastique',URL_MAIN + 'category/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'category/guerre/'] )
    liste.append( ['Histoire',URL_MAIN + 'category/histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'category/papystreaming_horreur/'] )
    liste.append( ['Musique',URL_MAIN + 'category/musique/'] )
    liste.append( ['Mystère',URL_MAIN + 'category/mystere/'] )
    liste.append( ['Romance',URL_MAIN + 'category/romance/'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'category/science-fiction/'] )
    liste.append( ['Soap',URL_MAIN + 'category/soap/'] )
    liste.append( ['Sport',URL_MAIN + 'category/Sport/'] )
    liste.append( ['Téléfilm',URL_MAIN + 'category/telefilm/'] )
    liste.append( ['Thriller',URL_MAIN + 'category/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'category/western/'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH2[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
    sPattern = '<a class="poster" href="([^"]+)"\s+title="([^"]+)".+?<img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sUrl = aEntry[0]
            if 'serie' in sUrl:
                continue
            sThumb = aEntry[2]
            sTitle =  aEntry[1]

            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
		
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?<\/span><\/li><li><a href="([^"]+)"'
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

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('http://www.google.com/s2/favicons?domain=','').replace('\\','')
    oParser = cParser()
	
    sPattern1 = '{"link":"([^"]+)","type":".+?"}'
    sPattern2 = 'src="([^"]+)"/><\/td>.+?<td>(.+?)<\/td>'

    aResult1 = re.findall(sPattern1, sHtmlContent,re.DOTALL)
    aResult2 = re.findall(sPattern2, sHtmlContent,re.DOTALL)

    aResult = zip(aResult1,aResult2)
    if (aResult):
        for aEntry in aResult:
            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
                sUrl = 'http:' + sUrl

            sQual = aEntry[1][1]
            if 'vf' in aEntry[1][0]:
                sLang = 'Vf'
            else:
                sLang = 'Vostfr'

            if 'papystreaming' in sUrl or 'mmfilmes.com' in sUrl or 'belike.pw' in sUrl:
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle + ' [' + sQual + '/' + sLang + ']')
                sDisplayTitle = sDisplayTitle + ' [COLOR skyblue]Papyplayer[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMisc(SITE_IDENTIFIER, 'ShowPapyLink', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
				
            else:
                sHosterUrl = sUrl
                
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle + ' [' + aEntry[1][1] + '/' + sLang + ']')
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()

def ShowPapyLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    oParser = cParser()

    if 'papystreaming' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = sHtmlContent.replace('http://www.film-streaming.mmfilmes.com/embed2.php?f=','')

        sPattern = "var links = *'(.+?)';"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            if 'mmfilmes' in aResult[1][0]:
                sDisplayTitle = sMovieTitle + ' [COLOR skyblue]PapyLink[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aResult[1][0])
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMisc(SITE_IDENTIFIER, 'ShowPapyLink', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sHtmlContent = base64.b64decode(aResult[1][0])
                sPattern = '"src":"([^"]+)",.+?"label":"(\d+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    link2 = aResult[1][0][0]
                    sLabel = aResult[1][0][1]

                    import urllib2
                    req = urllib2.Request(link2,None,headers)
                    req.add_header('Referer', sUrl)
                    response = urllib2.urlopen(req)
                    sHosterUrl = response.geturl()
                    response.close()

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle + '[' + sLabel + ']')
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    elif 'belike.pw' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'file: *"([^"]+)",label:"(\d+p)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = aEntry[0]
                sLabel = aEntry[1]
                
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle + ' [' + sLabel + ']')
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
    else:
        
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        sHtmlContent = sHtmlContent.replace('\\','')
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        sPattern = '"label":"([0-9p]+)"[^<>]+?"file":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            listurl = []
            listqual = []
            
            listurl.append(aResult[1][0][1])
            listqual.append(aResult[1][0][0])

            tab = zip(listurl,listqual)

            for url,qual in tab:
                sHosterUrl = url
                
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = sMovieTitle + ' [' + qual + ']'
                    sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
        else:
            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Lien vidéo HS[/COLOR]')

    oGui.setEndOfDirectory()

def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
    sSyn = ''
    sPattern = '<p class=".+?">([^<]+)<\/p>'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sSyn = aResult[1][0]

    sPattern = '<a class="expand-season-trigger" data-toggle="collapse".+?href="([^"]+)".+?<\/span>([^<]+)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            vUrl = sUrl + aEntry[0]
            sSaison = sMovieTitle + aEntry[1]
            sSaison = sSaison.replace('N/A','')
            sFilter = oParser.getNumberFromString(aEntry[1])
            sFilter = 'saison-' + sFilter + '/'
            
            sDisplayTitle = cUtil().DecoTitle(sSaison)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', vUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sSyn', sSyn)
            oOutputParameterHandler.addParameter('sFilter', sFilter)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumbnail, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sFilter = oInputParameterHandler.getValue('sFilter')
    sSyn = oInputParameterHandler.getValue('sSyn')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class="larr episode-header">.+?<a href="([^"]+)"\s+title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = sMovieTitle + aEntry[1]
            sTitle = sTitle.replace('N/A','').replace(',','')
            if not sFilter in sUrl:
               continue
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sSyn, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a class="poster" href="([^"]+)"\s+title="([^"]+)".+?<img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            if 'film' in sUrl:
                continue
            sThumb = aEntry[2]
            sTitle =  aEntry[1]

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage2(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage2(sHtmlContent):
    sPattern = '<span class="current">.+?<\/span><\/li><li><a href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
