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

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

SITE_IDENTIFIER = 'full_streaming_org' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Full-Streaming.org' # nom que xbmc affiche
SITE_DESC = 'films en streaming, vk streaming, youwatch, vimple , streaming hd , streaming 720p , streaming sans limite' #description courte de votre source

URL_MAIN = 'http://full-streaming.org/' # url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle seras affichee.
URL_SEARCH = ('http://www.fullmoviz.org/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = ('http://url', 'showMovies') # films nouveautés
MOVIE_MOVIE = ('http://url', 'showMovies') # films vrac
MOVIE_VIEWS = ('http://url', 'showMovies') # films + plus
MOVIE_COMMENTS = ('http://url', 'showMovies') # films + commentés
MOVIE_NOTES = ('http://url', 'showMovies') # films mieux notés
MOVIE_GENRES = (True, 'showGenre')
MOVIE_VF = ('http://url', 'showMovies') # films VF
MOVIE_VOSTFR = ('http://url', 'showMovies') # films VOSTFR

SERIE_NEWS = ('http://url', 'showSeries') # serie nouveautés
SERIE_SERIES = ('http://url', 'showSeries') # serie vrac
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

def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 
    #Ajoute lien dossier (identifant, function a attendre, nom, icon, parametre de sortie)
    #Puisque nous ne voulons pas atteindre une url on peut mettre ce qu'on veut dans le parametre siteUrl
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    #ici la function showMovies a besoin d'une url ici le racourci MOVIE_NEWS
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    #showGenre n'a pas besoin d'une url pour cette methode 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
              
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch(): #function de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #apelle le clavier xbmx
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  #modifi l'url de recherche
        showMovies(sUrl) #apelle la function qui pouras lire la page de resultats
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer les caterories et les liens qui vont bien
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
        #ajouter un dossier vers la function showMovies avec le titre de chaque categorie.
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui() #ouvre l'affichage
    if sSearch:#si une url et envoyer directement grace a la function showSearch
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') # recupere l'url sortie en parametre
   
    oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi
    
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    #la function replace et pratique pour supprimer un code du resultat
    
    sPattern = 'class="movie movie-block"><img src="([^<]+)" alt=".+?" title="([^<]+)"/>.+?<h2 onclick="window.location.href=\'([^<]+)\'">.+?<div style="color:#F29000">.+?<div.+?>(.+?)</div>'
    #pour faire simple recherche ce bout de code dans le code source de l'url
    #- ([^<]+) je veut cette partie de code mais y a une suite
    #- .+? je ne veut pas cette partis et peux importe ceux qu'elle contient
    #- (.+?) je veut cette partis et c'est la fin
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    # le plus simple et de faire un print aResult 
    # dans le fichier log d'xbmc vous pourez voir un array de ce que recupere le script
    # et modifier sPattern si besoin
    print aResult #Commenter ou supprimer cette ligne une foix fini
    
    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog update
            
            #L'array affiche vos info dans l'orde de sPattern en commencant a 0
            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2])) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1])) #sortie du titre
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0])) #sortie du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', aEntry[0], aEntry[3], oOutputParameterHandler)
                #addTV pour sortir les series tv (identifiant, function, titre, icon, poster, description, sortie parametre)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], aEntry[3], oOutputParameterHandler)
                #addMovies pour sortir les films (identifiant, function, titre, icon, poster, description, sortie parametre)
                
            #il existe aussis addMisc(identifiant, function, titre, icon, poster, description, sortie parametre)
            #la difference et pour les metadonner serie, films ou sans
            
        cConfig().finishDialog(dialog)# fin du dialog
           
        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entree pour le lien Next | pas de addMisc pas de poster et de description inutile donc

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
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
    #supprimer a l'aide de replace toute les entrer qui corresponde a votre recherche mais ne doivent pas etre pris en compte      

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'
    #ici nous cherchont toute les sources iframe
    aResult = oParser.parse(sHtmlContent, sPattern)
    #penser a faire un print aResult pour verifier
    
    #si un lien ne s'affiche pas peux etre que l'hote n'est pas supporte par l'addon
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle) #nom affiche
                oHoster.setFileName(sMovieTitle) # idem
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                #affiche le lien (oGui, oHoster, url du lien, poster)
                
    oGui.setEndOfDirectory() #fin
   
def seriesHosters(): #cherche les episode de series
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
               
    sPattern = '<dd><a href="([^<]+)" class="zoombox.+?" title="(.+?)"><button class="btn">.+?</button></a></dd>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(aEntry[1])
                oHoster.setFileName(aEntry[1])
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
    
#Voila c'est un peux brouillon mais ça devrais aider un peux, n'esiter a poser vos question et meme a partager vos source    
