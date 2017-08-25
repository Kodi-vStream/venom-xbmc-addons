#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui 
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser

 
SITE_IDENTIFIER = 'coco_streaming_com'
SITE_NAME = 'Coco-streaming'
SITE_DESC = 'Films en streaming.'
 
URL_MAIN = 'http://coco-stream.com'
 
URL_SEARCH = (URL_MAIN + '/films-en-streaming?search=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NEWS = (URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos', 'showMovies')
MOVIE_CULTE_NEWS = (URL_MAIN + '/films-culte-en-streaming?search=&filters%5BorderBy%5D=new_films', 'showMovies')
MOVIE_CULTE_MOVIE = (URL_MAIN + '/films-culte-en-streaming?search=&filters%5BorderBy%5D=new_videos', 'showMovies')
MOVIE_CULTE_GENRES = (True, 'showCulteGenres')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_VF = (URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Blanguages%5D%5BVF%5D=VF','showMovies')
MOVIE_VOSTFR = (URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Blanguages%5D%5BVOSTFR%5D=VOSTFR','showMovies')
SERIES = (URL_MAIN + '/series-en-streaming','showSeries')
SERIES_ACTUEL =('')
 
def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Les + recent)', 'films_news.png', oOutputParameterHandler)	

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CULTE_MOVIE[1], 'Films (Liens + recent)', 'films_news.png', oOutputParameterHandler)	
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)	
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films VOSTFR', 'films_news.png', oOutputParameterHandler)	
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films VF', 'films_news.png', oOutputParameterHandler)	
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CULTE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CULTE_NEWS[1], 'Films cultes (Les + recent)', 'films_news.png', oOutputParameterHandler)	

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CULTE_MOVIE[1], 'Films Culte (Liens + recent)', 'films_news.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CULTE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CULTE_GENRES[1], 'Films Culte (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES[1], 'Series', 'series_news.png', oOutputParameterHandler)	
	
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
    
    liste = []	
    liste.append( ['Action',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=15'] )
    liste.append( ['Animation',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=18'] )
    liste.append( ['Arts Martiaux',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=25'] )
    liste.append( ['Aventure',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=5'] )
    liste.append( ['Biopic',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=20'] )
    liste.append( ['Comédie',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=6'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=4'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=23'] )
    liste.append( ['Documentaire',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=16'] )
    liste.append( ['Drame',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=2'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=9'] )
    liste.append( ['Erotique',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=13'] )
    liste.append( ['Espionnage',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=14'] )
    liste.append( ['Famille',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=24'] )
    liste.append( ['Fantastique',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=12'] )  
    liste.append( ['Guerre',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=19'] )
    liste.append( ['Historique',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=11'] )
    liste.append( ['Judiciare',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=26'] )
    liste.append( ['Musical',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=10'] )
    liste.append( ['Policier',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=1'] )
    liste.append( ['Péplum',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=30'] )
    liste.append( ['Romance',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=7'] )
    liste.append( ['Science Fiction',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=17'] )
    liste.append( ['Sport Event',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=33'] )
    liste.append( ['Thriller',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=3'] )
    liste.append( ['Western',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=21'] )
    liste.append( ['Divers',URL_MAIN + '/films-en-streaming?search=&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=8'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()
	
def showCulteGenres():
    oGui = cGui()
    
    liste = []	
    liste.append( ['Action',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=15'] )
    liste.append( ['Animation',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=18'] )
    liste.append( ['Aventure',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=5'] )
    liste.append( ['Biopic',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=20'] )
    liste.append( ['Comédie',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=6'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=4'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=23'] )
    liste.append( ['Drame',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=2'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=9'] )
    liste.append( ['Famille',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=24'] )
    liste.append( ['Fantastique',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=12'] )  
    liste.append( ['Guerre',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=19'] )
    liste.append( ['Historique',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=11'] )
    liste.append( ['Musical',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=10'] )
    liste.append( ['Policier',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=1'] )
    liste.append( ['Romance',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=7'] )
    liste.append( ['Science Fiction',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=17'] )
    liste.append( ['Thriller',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=3'] )
    liste.append( ['Western',URL_MAIN + '/films-culte-en-streaming?search=&filters&filters%5BorderBy%5D=new_videos&filters%5Btypes%5D%5B15%5D=21'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()	
 
 
def showMovieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1913, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1936, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') #recupere l'url sortie en parametre

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    sPattern = 'src="(.+?).jpg">.+?<a class="coco-film-link-see"\s*href="(.+?)"\s*title="(.+?)"'
   
    oParser = cParser()
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

            sTitle = str(aEntry[2])
            sUrl2 = str(aEntry[1])
            sThumb = str(aEntry[0])
            if sThumb.startswith('/'):
				sThumb = URL_MAIN[:-1] + sThumb
            sDesc = ''

            sTitle = sTitle.replace('Voir en streaming', '')

            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumb',sThumb )

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle,'', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()
		
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') #recupere l'url sortie en parametre

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    sPattern = '<div class="col-xs-4">\s*<a href="(.+?)".+?>\s*.+?title="(.+?)".+? src="(.+?)"'
   
    oParser = cParser()
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

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[2])
            if sThumb.startswith('/'):
				sThumb = URL_MAIN[:-1] + sThumb
            sDesc = ''

            sTitle = sTitle.replace('Regarder', '')
            sTitle = sTitle.replace('en streaming', '')
            sUrl2 = sUrl2.replace('https:','http:')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumb',sThumb )

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaison', sTitle,'', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaison', sTitle,'', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()		
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    #sPattern = '</a></li><li class="active"><a href=\'#\'>.+?<\/a><\/li><li><a href="(.+?)">'
    sPattern = '<a rel="next" href="(.+?)">Suivant.+?<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False
   
def ShowSerieSaison():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl') #recupere l'url sortie en parametre

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()	
	
    sPattern = '<li>\s*<a href="(.+?)" title="Voir en streaming (.+?) - (.+?)">.+?</a>\s*</li>'

    oParser = cParser()
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

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[0])
            sTitle2 = str(aEntry[2])
            sDesc = ''

            sTitle = sTitle.replace('Voir en streaming ', '')
            sUrl2 = sUrl2.replace('https:','http:')
            sUrl2 = sUrl + sUrl2
            sTitle = sTitle + sTitle2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumb',sThumb )

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieEpisodes', sTitle,'', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieEpisodes', sTitle,'', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()	

def ShowSerieEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<article class="col-xs-12 col-md-6 preview">\s*<a href="(.+?)" title="Voir en streaming (.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = str(aEntry[1])
            sUrl2 = sUrl + str(aEntry[0])
            sUrl2 = sUrl2.replace('https:','http:')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumb',sThumb )

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()			
	
def seriesHosters(): #cherche les episodes de series
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<button data-src="(.+?)" class="btn btn-primary .+?">Lien(.+?)</button>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(aEntry[1])
                oHoster.setFileName(aEntry[1])
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()   
   
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
	
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    oParser = cParser()
    sPattern = '<li class=.+?" data-embed="(.+?)" title=".+?">'
   
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        for aEntry in aResult[1]:
           
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl) 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle) 
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
               
    oGui.setEndOfDirectory() 
