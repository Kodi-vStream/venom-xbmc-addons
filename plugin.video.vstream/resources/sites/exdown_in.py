#-*- coding: utf-8 -*-

# Fait par vic1997
#
# Pas fait mais peut-être possible à faire (il faut voir avec le site mais j'ai pas trouvé) :
# - Recherche pour Series, Anime/Manga, Documentaire et Emissions TV
# - Par genre pour Series, Anime/Manga, Documentaire et Emissions TV

# C'est ma première source, je ne garantie pas que ça marche !


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

SITE_IDENTIFIER = 'exdown_in' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Extreme-down.in' # nom que xbmc affiche
SITE_DESC = 'films hd, streaming 720p , streaming 1080p , Films/series, recent' #description courte de votre source

URL_MAIN = 'https://www.extreme-down.in/' # url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle seras affichee.
URL_SEARCH = (URL_MAIN + '1/recherche1/1.html?rech_fiche=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


#Films
MOVIE_SD = (URL_MAIN + 'films-sd/', 'showMovies') # films SD
MOVIE_HD = (URL_MAIN + 'films-hd/', 'showMovies') # films HD
MOVIE_HDLIGHT720 = (URL_MAIN + 'films-hdlight/hdlight-720p/', 'showMovies') # films HDlight 720p
MOVIE_HDLIGHT1080 = (URL_MAIN + 'films-hdlight/hdlight-1080p/', 'showMovies') # films HDlight 1080p
MOVIE_CLASS_SD = (URL_MAIN + 'films-classique/classiques-sd/', 'showMovies')# films classiques SD
MOVIE_CLASS_HD = (URL_MAIN + 'films-classique/classiques-hd/', 'showMovies')# films classiques HD
MOVIE_GENRES = (True, 'showGenre')


#Series
SERIE_SD = (URL_MAIN + 'series/', 'showSeries') # serie SD
SERIE_HD = (URL_MAIN + 'series-hd/', 'showSeries') # serie HD
SERIE_SD_VOSTFR = (URL_MAIN + 'series/vostfr/', 'showSeries') # serie SD VOSTFR
SERIE_SD_VF = (URL_MAIN + 'series/vf/', 'showSeries') # serie SD VF
SERIE_HD720_VOSTFR = (URL_MAIN + 'series-hd/hd-series-vostfr/', 'showSeries') # serie hd 720p VOSTFR
SERIE_HD1080_VOSTFR = (URL_MAIN + 'series-hd/1080p-series-vostfr/', 'showSeries') # serie hd 1080p VOSTFR
SERIE_HD720_VF = (URL_MAIN + 'series-hd/hd-series-vf/', 'showSeries') # serie hd 720p VF
SERIE_HD1080_VF = (URL_MAIN + 'series-hd/1080p-series-vf/', 'showSeries') # serie hd 1080p VF
SERIE_X265 = (URL_MAIN + 'series-hd/hd-x265-hevc/', 'showSeries') # serie X265 HEVC
#SERIE_GENRE = (True, 'showGenre')

#Autres
DOC_DOCS = (URL_MAIN + 'documentaires/', 'showOthers') # documentaire
EMI_TV = (URL_MAIN + 'emissions-tv/', 'showOthers') # emission-tv

#Anime/Manga
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showAnimes') #anime/manga
ANIM_FILMS = (URL_MAIN + 'mangas/manga-films/', 'showAnimes') #anime/manga films
ANIM_VOSTFR = (URL_MAIN + 'mangas/series-vostfr/', 'showAnimes') #anime/manga VOSTFR
ANIM_VF = (URL_MAIN + 'mangas/series-vf/', 'showAnimes') #anime/manga VF
#ANIM_GENRES = (True, 'showGenre') #anime genre



def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Series', 'series.png', oOutputParameterHandler)       
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSpectacles', 'Spectacles', 'films.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuEmissionsTV', 'Emissions TV', 'tv.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch(): #function de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  #modifi l'url de recherche
        showMovies(sUrl) #apelle la function qui pourra lire la page de resultats
        oGui.setEndOfDirectory()
        return  

def showMenuFilms():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'film') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de films', 'search.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD[1], 'Films SD', 'films.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'films.png', oOutputParameterHandler)  
    
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT720[1], 'Films HDLight 720p', 'films.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT1080[1], 'Films HDLight 1080p', 'films.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASS_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASS_SD[1], 'Films Classique SD', 'films.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASS_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASS_HD[1], 'Films Classique HD', 'films.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films par genre', 'films.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()     		
		
def showMenuSeries():
    oGui = cGui()
       
    #oOutputParameterHandler = cOutputParameterHandler() 
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oOutputParameterHandler.addParameter('type', 'serie') 
    #oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de series', 'search.png', oOutputParameterHandler)
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD[1], 'Séries SD', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Séries HD', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_VOSTFR[1], 'Séries SD VOSTFR', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_FR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_FR[1], 'Séries SD VF', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD720_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD720_VOSTFR[1], 'Séries HD 720p VOSTFR', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD1080_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD1080_VOSTFR[1], 'Séries HD 1080p VOSTFR', 'news.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD720_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD720_VF[1], 'Séries HD 720p VF', 'news.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD1080_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD1080_VF[1], 'Séries HD 1080p VF', 'news.png', oOutputParameterHandler)  
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_X265[0])
    oGui.addDir(SITE_IDENTIFIER, SSERIE_X265[1], 'Séries en x265', 'news.png', oOutputParameterHandler)  
	
	#oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRE[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRE[1], 'Séries par genre', 'news.png', oOutputParameterHandler)  


     
    
    oGui.setEndOfDirectory()     
    
def showMenuMangas():
    oGui = cGui()
       
    #oOutputParameterHandler = cOutputParameterHandler() 
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oOutputParameterHandler.addParameter('type', 'anime') 
    #oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche d\'animes', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers Mangas ajoutés', 'news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_FILMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_FILMS[1], 'Mangas films', 'news.png', oOutputParameterHandler) 
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFR[1], 'Mangas VOSTFR', 'news.png', oOutputParameterHandler) 
	
	oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF[1], 'Mangas VF', 'news.png', oOutputParameterHandler) 
	
	

    
        
    oGui.setEndOfDirectory()    
    
	
def showMenuEmissionsTV():
    oGui = cGui()
       
    #oOutputParameterHandler = cOutputParameterHandler() 
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    #oGui.addDir(SITE_IDENTIFIER, 'showSearchEmissionsTV', 'Recherche d Emissions TV', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', EMI_TV[0])
    oGui.addDir(SITE_IDENTIFIER, EMI_TV[1], 'Dernieres Emissions TV', 'news.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()     
  

def showMenuEmissionsTV():
    oGui = cGui()
       
    #oOutputParameterHandler = cOutputParameterHandler() 
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    #oGui.addDir(SITE_IDENTIFIER, 'showSearchDocumentaire', 'Recherche de Documentaire', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Derniers Documentaires', 'news.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()     

	
def showGenre(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer les caterories et les liens qui vont bien
    liste = []
    liste.append( ['Action',URL_MAIN + 'tags/Action/'] )
    liste.append( ['Animation',URL_MAIN + 'tags/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'tags/Arts+Martiaux/'] )
    liste.append( ['Biopic',URL_MAIN + 'tags/Biopic/'] )
    liste.append( ['Comedie',URL_MAIN + 'tags/comedie/'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'tags/comedie+dramatique/'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'tags/comedie+musicale/'] )
    liste.append( ['Drame',URL_MAIN + 'tags/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'tags/epouvante+horreur/'] ) 
    liste.append( ['Espionnage',URL_MAIN + 'tags/espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'tags/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'tags/fantastique/'] )  
    liste.append( ['Guerre',URL_MAIN + 'tags/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'tags/historique/'] )
    liste.append( ['Musical',URL_MAIN + 'tags/musical/'] )
    liste.append( ['Policier',URL_MAIN + 'tags/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'tags/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'tags/science+fiction/'] )
    liste.append( ['Thriller',URL_MAIN + 'tags/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'tags/western/'] )
                
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
