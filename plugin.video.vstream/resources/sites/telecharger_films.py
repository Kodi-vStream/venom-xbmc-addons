#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui #system de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #system de recherche pour l'hote
from resources.lib.gui.gui import cGui #system d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #system d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entrer des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortis des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code

#Si vous créer une source et la déposer dans le dossier sites elle seras directement visible sous xbmc

SITE_IDENTIFIER = 'telecharger_films' #identifant nom de votre fichier remplacer les espaces et les . par _ aucun caractere speciale
SITE_NAME = 'telecharger films' # nom que xbmc affiche
SITE_DESC = 'films en streaming' #description courte de votre source

URL_MAIN = 'http://www.telecharger-films.ws/' # url de votre source

#definis les url pour les catégories principale ceci et automatique si la deffition et présente elle seras afficher.
MOVIE_NEWS = ('http://www.telecharger-films.ws/telecharger-films-gratuit/', 'showMovies') # films nouveautés
MOVIE_VIEWS = ('http://www.telecharger-films.ws/telecharger-films-exclu/', 'showMovies') # films + plus
MOVIE_COMMENTS = ('http://www.telecharger-films.ws/telecharger-films-gratuit/films-vo-anglais/', 'showMovies') # films + commentés
MOVIE_NOTES = ('http://www.telecharger-films.ws/telecharger-films-gratuit/films-vostfr/', 'showMovies') # films mieux notés
MOVIE_GENRES = True # ou http://url

SERIE_SERIES = ('http://www.telecharger-films.ws/telecharger-serie/', 'showMovies') # serie nouveautés
SERIE_VFS = ('http://www.telecharger-films.ws/telecharger-serie/series-fr/', 'showMovies') # serie VF
SERIE_VOSTFRS = ('http://www.telecharger-films.ws/telecharger-serie/sries-vostfr/', 'showMovies') # serie Vostfr

ANIM_ANIMS = ('http://www.telecharger-films.ws/telecharger-films-animation/', 'showMovies') #anim nouveautés

DOC_DOCS = ('http://www.telecharger-films.ws/films-documentaires-spectacle/', 'showMovies') #Documentaire
URL_SEARCH = ('http://www.telecharger-films.ws/index.php?do=search&mode=advanced','showMovies')
FUNCTION_SEARCH = 'showMovies'

def load(): 
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch(): #function de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #apelle le clavier xbmx
    if (sSearchText != False):
            sUrl = 'http://www.telecharger-films.ws/index.php?story={'+sSearchText'}&do=search&subaction=search'  #modifier l'url de recherche
            showMovies(sUrl) #apelle la function qui pouras lire la page de resulta
            oGui.setEndOfDirectory()
            return  
    
    
def showGenre(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer c'est caterorie et les lien qui vont bien
    liste = []
    liste.append( ['Action','http://www.telecharger-films.ws/telecharger-films-action/'] )
    liste.append( ['Animation','http://www.telecharger-films.ws/telecharger-films-animation/'] )
    liste.append( ['Arts Martiaux','http://www.telecharger-films.ws/telecharger-films-arts-martiaux/'] )
    liste.append( ['Aventure','http://www.telecharger-films.ws/telecharger-films-aventure/'] )
    liste.append( ['Biopic','http://www.telecharger-films.ws/telecharger-films-biopic/'] )
    liste.append( ['Comedie','http://www.telecharger-films.ws/telecharger-films-comdie/'] )
    liste.append( ['Comedie Dramatique','http://www.telecharger-films.ws/telecharger-films-comdie-dramatique/'] )
    liste.append( ['Documentaire','http://www.telecharger-films.ws/films-documentaires-spectacle/'] )
    liste.append( ['Drame','http://www.telecharger-films.ws/telecharger-films-drame/'] )
    liste.append( ['Epouvante Horreur','http://www.telecharger-films.ws/telecharger-films-epouvante-horreur/'] ) 
    liste.append( ['Erotique','http://full-streaming.org/erotique'] )
    liste.append( ['Espionnage','http://www.telecharger-films.ws/telecharger-films-espionnage/'] )
    liste.append( ['Famille','http://www.telecharger-films.ws/telecharger-films-famille/'] )
    liste.append( ['Fantastique','http://www.telecharger-films.ws/telecharger-films-fantastique/'] )  
    liste.append( ['Guerre','http://www.telecharger-films.ws/telecharger-films-guerre/'] )
    liste.append( ['Historique','http://www.telecharger-films.ws/telecharger-films-historique/'] )
    liste.append( ['Musical','http://www.telecharger-films.ws/telecharger-films-musical/'] )
    liste.append( ['Policier','http://www.telecharger-films.ws/telecharger-films-policier/'] )
    liste.append( ['Romance','http://www.telecharger-films.ws/telecharger-films-romance/'] )
    liste.append( ['Science Fiction','http://www.telecharger-films.ws/telecharger-films-science-fiction/'] )
    liste.append( ['Sports','http://www.telecharger-films.ws/telecharger-films-sport/'] )
    liste.append( ['Thriller','http://www.telecharger-films.ws/telecharger-films-thriller/'] )
    liste.append( ['Western','http://www.telecharger-films.ws/telecharger-film-western/'] )
     
                
    for sTitle,sUrl in liste:#boucle
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortis de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        #ajouter un dossier vers la function showMovies avec le titre de chaque categorie.
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui() #ouvre l'affichage
    if sSearch:#si une url et envoyer directement garce a la function showSearch
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') # recupere l'url sortis en parametre
   
    oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request(); #requete aussi
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    #la function replace et pratique pour supprimer un code du resultat
    sPattern = '|--><img src="([^<]+)" alt=".+?" title="([^<]+)" .+? /><br /><i>([^<]+) (.+?)<br /><br /><br /></div></div>'

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
        total = len(aResult[1]) #dialog
        dialog = cConfig().createDialog(SITE_NAME) #dialog
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
            #L'array affiche vos info dans l'orde de sPattern en commencant a 0
            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2])) #sortis de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1])) #sortis du titre
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0])) #sortis du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', aEntry[0], aEntry[3], oOutputParameterHandler)
                #addTV pour sortir les serie tv (identifiant, function, titre, icon, poster, description, sortis parametre)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], aEntry[3], oOutputParameterHandler)
                #addMovies pour sortir les films (identifiant, function, titre, icon, poster, description, sortis parametre)
                
            #il existe aussis addMisc(identifiant, function, titre, icon, poster, description, sortis parametre)
            #la difference et pour les metadonner serie, films ou sans
        cConfig().finishDialog(dialog)#dialog
           
        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc

    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage


def __checkForNextPage(sHtmlContent): #cherche la page suivante
    sPattern = '<div class="navigation".+? <span.+? <a href="(.+?)">'
    # .+? je ne veut pas cette partis et peux importe ceux qu'elle contient
    #- (.+?) je veut cette partis et c'est la fin
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult #affiche le result dans le log naviguer un peux sur votre source pour voir si tous ce passe bien
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    

def showHosters():# recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entre de paramettre
    sUrl = oInputParameterHandler.getValue('siteUrl')  # apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #apelle le titre
    sThumbnail = oInputParameterHandler.getValue('sThumbnail') # apelle le poster
    
    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request(); #requete sur l'url
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
    #supprimer a l'aide de replace toute les entrer qui corresponde a votre recherche mais ne doivent pas etre pris en compte      

    sPattern = '<iframe.+?src="(.+?)"'
    #ici nous cherchont toute les sources iframe
    oParser = cParser()
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
