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

import xbmc

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

SITE_IDENTIFIER = 'full_streaming_org' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Full-Streaming.org' # nom que xbmc affiche
SITE_DESC = 'films en streaming, streaming hd , streaming 720p , Films/series, recent' #description courte de votre source

URL_MAIN = 'http://le_site.org/' # url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle seras affichee.
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'url', 'showMovies') # films nouveautés
MOVIE_MOVIE = (URL_MAIN + 'url', 'showMovies') # films vrac
MOVIE_VIEWS = (URL_MAIN + 'url', 'showMovies') # films + plus
MOVIE_COMMENTS = (URL_MAIN + 'url', 'showMovies') # films + commentés
MOVIE_NOTES = (URL_MAIN + 'url', 'showMovies') # films mieux notés
MOVIE_GENRES = (True, 'showGenre')
MOVIE_VF = (URL_MAIN + 'url', 'showMovies') # films VF
MOVIE_VOSTFR = (URL_MAIN + 'url', 'showMovies') # films VOSTFR

SERIE_NEWS = (URL_MAIN + 'url', 'showSeries') # serie nouveautés
SERIE_SERIES = (URL_MAIN + 'url', 'showSeries') # serie vrac
SERIE_VFS = (URL_MAIN + 'url', 'showSeries') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'url', 'showSeries') # serie Vostfr
SERIE_GENRE = (True, 'showGenre')

ANIM_NEWS = (URL_MAIN + 'url', 'showAnimes') #anime nouveautés
ANIM_ANIMS = (URL_MAIN + 'url', 'showAnimes') #anime vrac
ANIM_VFS = (URL_MAIN + 'url', 'showAnimes') #anime VF
ANIM_VOSTFRS = (URL_MAIN + 'url', 'showAnimes') #anime VOSTFR
ANIM_MOVIES = (URL_MAIN + 'url'', 'showAnimes') #anime film
ANIM_GENRES = (True, 'showGenre') #anime genre

DOC_DOCS = (URL_MAIN + 'url', 'showOthers') #Documentaire
SPORT_SPORTS = (URL_MAIN + 'url', 'showOthers') #sport
MOVIE_NETS = (URL_MAIN + 'url', 'showOthers') #video du net
REPLAYTV_REPLAYTV = (URL_MAIN + 'url', 'showOthers') #Replay

def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 
    #Ajoute lien dossier (identifant, function a attendre, nom, icone, parametre de sortie)
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

    sSearchText = oGui.showKeyBoard() #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  #modifi l'url de recherche
        showMovies(sUrl) #apelle la function qui pourra lire la page de resultats
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer les caterories et les liens qui vont bien
    liste = []
    liste.append( ['Action',URL_MAIN + 'action/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'biopic/'] )
    liste.append( ['Comedie',URL_MAIN + 'comedie/'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'comedie-dramatique/'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'comedie-musicale/'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur/'] ) 
    liste.append( ['Erotique',URL_MAIN + 'erotique'] )
    liste.append( ['Espionnage',URL_MAIN + 'espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )  
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'historique/'] )
    liste.append( ['Musical',URL_MAIN + 'musical/'] )
    liste.append( ['Policier',URL_MAIN + 'policier/'] )
    liste.append( ['Peplum',URL_MAIN + 'peplum/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + 'spectacle/'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller/'] )
    liste.append( ['Western',URL_MAIN + 'western/'] )
    liste.append( ['Divers',URL_MAIN + 'divers/'] ) 
                
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
    #
    #Pour tester vos Regex, vous pouvez utiliser le site https://regex101.com/ en mettant dans les modifiers "gmis"
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    # le plus simple et de faire un  xbmc.log(str(aResult))
    # dans le fichier log d'xbmc vous pourrez voir un array de ce que recupere le script
    # et modifier sPattern si besoin
    xbmc.log(str(aResult)) #Commenter ou supprimer cette ligne une fois fini
    
    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog update
            
            #L'array affiche vos info dans l'orde de sPattern en commencant a 0
            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[2])
            sThumb = str(aEntry[0])
            SResume = ''
            
            sTitle = sTitle.replace('En streaming', '')
            sUrl2 = URL_MAIN + sUrl2
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumbnail',sThumb ) #sortie du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', sThumb, SResume, oOutputParameterHandler)
                #addTV pour sortir les series tv (identifiant, function, titre, icon, poster, description, sortie parametre)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, SResume, oOutputParameterHandler)
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

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'
    #ici nous cherchont toute les sources iframe
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    #pensez a faire un xbmc.log(str(aResult)) pour verifier
    
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
   
def seriesHosters(): #cherche les episodes de series
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
               
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
