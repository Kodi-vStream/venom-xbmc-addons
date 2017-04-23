#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films & Série en Streaming uniquement sur Netu'

URL_MAIN = 'http://filmstreamvk.com/'

MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-plus-vues-films', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'serie', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'serie', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'manga', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'manga', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load(): 
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les Plus Vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Série (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'category/action/'] )
    liste.append( ['Animation',URL_MAIN + 'category/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'category/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'category/aventure/'] )
    liste.append( ['Bande annonce',URL_MAIN + 'category/bande-annonce/'] )
    liste.append( ['Biographie',URL_MAIN + 'category/biography/'] )
    liste.append( ['Biopic',URL_MAIN + 'category/biopic/'] )
    liste.append( ['Capes et épées',URL_MAIN + 'category/capes-et-epees/'] )
    liste.append( ['Comédie',URL_MAIN + 'category/comedie/'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'category/comedie-dramatique/'] )
    liste.append( ['Comédie musicale',URL_MAIN + 'category/comedie-musicale/'] )
    liste.append( ['Concert',URL_MAIN + 'category/concert/'] )
    liste.append( ['Crime',URL_MAIN + 'category/crime/'] )
    liste.append( ['Days (TV)',URL_MAIN + 'category/days-tv/'] )
    liste.append( ['Divers',URL_MAIN + 'category/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + 'category/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'category/drame/'] )
    liste.append( ['Enigme',URL_MAIN + 'category/enigme/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'category/epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'category/espionnage/'] )
    liste.append( ['Exclues',URL_MAIN + 'category/exclues/'] )
    liste.append( ['Famille',URL_MAIN + 'category/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'category/fantastique/'] )
    liste.append( ['Fantasy',URL_MAIN + 'category/fantasy/'] )
    liste.append( ['Film récompensé',URL_MAIN + 'category/film-recompense/'] )
    liste.append( ['Guerre',URL_MAIN + 'category/guerre/'] )
    liste.append( ['Histoire vraie',URL_MAIN + 'category/histoire-vraie/'] )
    liste.append( ['Historique',URL_MAIN + 'category/historique/'] )
    liste.append( ['Horreur',URL_MAIN + 'category/horreur/'] )
    liste.append( ['Judiciaire',URL_MAIN + 'category/judiciaire/'] )
    liste.append( ['Musical',URL_MAIN + 'category/musical/'] )
    liste.append( ['Mystery',URL_MAIN + 'category/mystery/'] )
    liste.append( ['Non classé',URL_MAIN + 'category/non-classe/'] )
    liste.append( ['Péplum',URL_MAIN + 'category/peplum/'] )
    liste.append( ['Pixar',URL_MAIN + 'category/pixar/'] )
    liste.append( ['Policier',URL_MAIN + 'category/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'category/romance/'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'category/science-fiction/'] )
    liste.append( ['Série',URL_MAIN + 'category/serie/'] )
    liste.append( ['Spectacle',URL_MAIN + 'category/spectacle/'] )
    liste.append( ['Sport',URL_MAIN + 'category/sport/'] )
    liste.append( ['Sport event',URL_MAIN + 'category/sport-event/'] )
    liste.append( ['Survival',URL_MAIN + 'category/survival/'] )
    liste.append( ['Thriller',URL_MAIN + 'category/thriller/'] )
    liste.append( ['Top films',URL_MAIN + 'category/exclues/top-films/'] )
    liste.append( ['Walt Disney',URL_MAIN + 'category/walt-disney/'] )
    liste.append( ['Western',URL_MAIN + 'category/western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        sUrl = sSearch
        sUrl = sUrl.replace('%20','+')

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="moviefilm"><a href=".+?".+?<img src="([^<"]+)".+?<a href="([^<]+)">([^<]+)<\/a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue
                
            sTitle = aEntry[2]
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            
            if '/serie/' in aEntry[1] or '/manga/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', aEntry[0], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl

    return False

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    ListeUrl = []
    #recuperation du hoster de base
    sPattern = '<div class="keremiya_part"> <span>(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        ListeUrl = [(sUrl,aResult[1][0])]
    
    #Recuperation des suivants
    sPattern = '<a href="([^<]+)"><span>(.+?)</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]
    
    #si quedale on tente le tout pour le tout
    if (aResult[0] == False):
        showHosters()

    if (aResult[0] == True):
        total = len(ListeUrl)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in ListeUrl:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle + ' (' + aEntry[1] + ')'
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
        
def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<td class="liste_episode" width="10%">(.+?)<\/td>|<a href="([^<>"]+?)" title="" class="num_episode">([0-9]+)<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            if aEntry[0]:
                sTitle = aEntry[0].decode("utf8")
                sTitle = cUtil().unescape(sTitle).encode("utf8")
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showEpisode', '[COLOR red]' + sTitle + '[/COLOR]', 'host.png', oOutputParameterHandler)
            else:
                sTitle = sMovieTitle + ' episode ' + aEntry[2]
                
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHostersSerie', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHostersSerie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')

    sPattern = 'onclick="lecteur_serie\([0-9]+,\'((?:http|\/)[^<>]+?)\'\);">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #si quedale on tente le tout pour le tout
    if (aResult[0] == False):
        showHosters()

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            if not sHosterUrl.startswith('http'):
               sHosterUrl = 'http:' + str(aEntry)
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')

    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
