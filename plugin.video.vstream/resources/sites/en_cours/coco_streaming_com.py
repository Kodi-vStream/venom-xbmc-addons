#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code
#from resources.lib.util import cUtil #outils pouvant etre utiles
 
SITE_IDENTIFIER = 'coco_streaming_com' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Coco-streaming.com' # nom que xbmc affiche
SITE_DESC = 'films en streaming, vk streaming, youwatch, vimple , streaming hd , streaming 720p , streaming sans limite' #description courte de votre source
 
URL_MAIN = 'http://coco-stream.com' # url de votre source
 
URL_SEARCH = ('http://coco-stream.com/films-en-streaming?search=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NEWS = ('http://coco-stream.com', 'showMovies') 
MOVIE_MOVIE = ('http://coco-stream.com/films-en-streaming', 'showMovies')
MOVIE_VIEWS = ('http://url', 'showMovies')
MOVIE_COMMENTS = ('http://url', 'showMovies')
MOVIE_NOTES = ('http://url', 'showMovies') 
MOVIE_GENRES = (True, 'showGenre')
MOVIE_VF = ('http://url', 'showMovies') 
MOVIE_VOSTFR = ('http://url', 'showMovies') 
MOVIE_CULTE = ('http://coco-stream.com/films-culte-en-streaming','showMovies')
 
SERIE_NEWS = ('http://url', 'showSeries') # serie nouveautés
SERIE_SERIES = ('http://coco-stream.com/series-en-streaming', 'showSeries') # serie vrac
SERIE_VFS = ('http://url', 'showSeries') # serie VF
SERIE_VOSTFRS = ('http://url', 'showSeries') # serie Vostfr
SERIE_GENRE = (True, 'showGenre')
 
ANIM_NEWS = ('http://url', 'showAnimes') #anime nouveautés
ANIM_ANIMS = ('http://url', 'showAnimes') #anime vrac
ANIM_VFS = ('http://url', 'showAnimes') #anime VF
ANIM_VOSTFRS = ('http://url', 'showAnimes') #anime VOSTFR
ANIM_MOVIES = ('http://url', 'showAnimes') #anime film
ANIM_GENRES = (True, 'showGenre') #anime genre
 
DOC_DOCS = ('http://url', 'showOthers') #Documentaire
SPORT_SPORTS = ('http://url', 'showOthers') #sport
MOVIE_NETS = ('http://url', 'showOthers') #video du net
REPLAYTV_REPLAYTV = ('http://url', 'showOthers') #Replay
 
def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER,MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
 
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films en vrac', 'genres.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CULTE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CULTE[1], 'Films cultes ', 'genres.png', oOutputParameterHandler)
   
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showGenre(): #affiche les genres
    oGui = cGui()
    
    liste = []
    liste.append( ['Action','http://full-streaming.org/action/'] )
    liste.append( ['Animation','http://full-streaming.org/animation/'] )
    liste.append( ['Arts Martiaux','http://full-streaming.org/arts-martiaux/'] )
    liste.append( ['Aventure','http://full-streaming.org/aventure/'] )
    liste.append( ['Biopic','http://full-streaming.org/biopic/'] )
    liste.append( ['Comedie','http://full-streaming.org/comedie/'] )
    liste.append( ['Comedie Dramatique','http://full-streaming.org/comedie-dramatique/'] )
    liste.append( ['Comedie Musicale','http://full-streaming.org/comedie-musicale/'] )
    liste.append( ['Documentaire','http://full-streaming.org/documentaire/'] )
    liste.append( ['Drame','http://full-streaming.org/drame/'] )
    liste.append( ['Epouvante Horreur','http://full-streaming.org/epouvante-horreur/'] )
    liste.append( ['Erotique','http://full-streaming.org/erotique'] )
    liste.append( ['Espionnage','http://full-streaming.org/espionnage/'] )
    liste.append( ['Famille','http://full-streaming.org/famille/'] )
    liste.append( ['Fantastique','http://full-streaming.org/fantastique/'] )  
    liste.append( ['Guerre','http://full-streaming.org/guerre/'] )
    liste.append( ['Historique','http://full-streaming.org/historique/'] )
    liste.append( ['Musical','http://full-streaming.org/musical/'] )
    liste.append( ['Policier','http://full-streaming.org/policier/'] )
    liste.append( ['Peplum','http://full-streaming.org/peplum/'] )
    liste.append( ['Romance','http://full-streaming.org/romance/'] )
    liste.append( ['Science Fiction','http://full-streaming.org/science-fiction/'] )
    liste.append( ['Spectacle','http://full-streaming.org/spectacle/'] )
    liste.append( ['Thriller','http://full-streaming.org/thriller/'] )
    liste.append( ['Western','http://full-streaming.org/western/'] )
    liste.append( ['Divers','http://full-streaming.org/divers/'] )
               
    for sTitle,sUrl in liste:#boucle
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()
 
 
def showMovies(sSearch = ''):
    oGui = cGui() 
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') # recupere l'url sortie en parametre
   
    oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi
   
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    #la function replace et pratique pour supprimer un code du resultat
   
    sPattern = '<a href="([^<]+)<img alt="([^<]+)src="(.+?)"'
    #pour faire simple recherche ce bout de code dans le code source de l'url
    #- ([^<]+) je veut cette partie de code mais y a une suite
    #- .+? je ne veut pas cette partis et peux importe ceux qu'elle contient
    #- (.+?) je veut cette partis et c'est la fin
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult #Commenter ou supprimer cette ligne une foix fini
   
    if (aResult[0] == True):
        total = len(aResult[1])
        
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
           
           
            sTitle = aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://coco-stream.com'+aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0])) #sortie du titre
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2])) #sortie du poster
 
            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle,'', aEntry[0], aEntry[2], oOutputParameterHandler)

            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], aEntry[2], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage
 
 
def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = '<div class="navigation".+? <span.+? <a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult #affiche le result dans le log
    if (aResult[0] == True):
        return aResult[1][0]
 
    return False
   
def showHosters():# recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sUrl = oInputParameterHandler.getValue('siteUrl')  # apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #apelle le titre
    sThumbnail = oInputParameterHandler.getValue('sThumbnail') # apelle le poster
   
    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request(); #requete sur l'url
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')   
 
    oParser = cParser()
    sPattern = 'src="(.+?)" alt="(.+?)" title="(.+?)"'
   
    aResult = oParser.parse(sHtmlContent, sPattern)
    #penser a faire un print aResult pour verifier
    print aResult
   
    if (aResult[0] == True):
        for aEntry in aResult[1]:
           
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl) 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle) 
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
               
    oGui.setEndOfDirectory() 
