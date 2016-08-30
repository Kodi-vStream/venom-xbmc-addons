#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'you_exclus_net'
SITE_NAME = 'You-Exclus.net'
SITE_DESC = 'Exclus Film serie sans limite de temps gratuit !!! (Vk,Netu,youwatch HD-Exashare)'

URL_MAIN = 'http://www.you-exclus.net/'

#definis les url pour les catégories principale ceci et automatique si la deffition et présente elle seras afficher.
MOVIE_NEWS = 'http://www.you-exclus.net/films/' # films nouveautés
MOVIE_NOTES = 'http://www.you-exclus.net/films/hd-720p/' # films mieux notés
SERIE_SERIES = 'http://www.you-exclus.net/series/' # serie nouveautés
SERIE_VFS = 'http://www.you-exclus.net/series/version-french/' # serie VF
SERIE_VOSTFRS = 'http://www.you-exclus.net/series/vostf/' # serie Vostfr
ANIM_MOVIES = 'http://www.you-exclus.net/films/animation/' #anim film
MOVIE_GENRES = True # ou http://url

def load(): #function charger automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series VF', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series VOSTFR', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory() 

def showSearch(): 
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.you-exclus.net/xfsearch/'+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenre(): #affiche les genres
    oGui = cGui()
 
    liste = []
    liste.append( ['Action','http://www.you-exclus.net/films/action/'] )
    liste.append( ['Animation','http://www.you-exclus.net/films/animation/'] )
    liste.append( ['hd-720p','http://www.you-exclus.net/films/hd-720p/'] )
    liste.append( ['Arts Martiaux','http://www.you-exclus.net/films/art-martiaux/'] )
    liste.append( ['Aventure','http://www.you-exclus.net/films/aventure/'] )
    liste.append( ['Biopic','http://www.you-exclus.net/films/biopic/'] )
    liste.append( ['Comedie','http://www.you-exclus.net/films/comedie/'] )
    liste.append( ['Documentaire','http://www.you-exclus.net/films/documentaire/'] )
    liste.append( ['Drame','http://www.you-exclus.net/films/drame/'] )
    liste.append( ['Epouvante Horreur','http://www.you-exclus.net/films/epouvante-horreur/'] ) 
    liste.append( ['Famille','http://www.you-exclus.net/films/famille/'] )
    liste.append( ['Fantastique','http://www.you-exclus.net/films/fantastique/'] )  
    liste.append( ['Guerre','http://www.you-exclus.net/films/guerre/'] )
    liste.append( ['Historique','http://www.you-exclus.net/films/historique/'] )
    liste.append( ['Musical','http://www.you-exclus.net/films/musical/'] )
    liste.append( ['Policier','http://www.you-exclus.net/films/policier/'] )
    liste.append( ['Romance','http://www.you-exclus.net/films/romance/'] )
    liste.append( ['Science Fiction','http://www.you-exclus.net/films/science-fiction/'] )
    liste.append( ['Thriller','http://www.you-exclus.net/films/thriller/'] )
    liste.append( ['Western','http://www.you-exclus.net/films/westerns/'] ) 
                
    for sTitle,sUrl in liste:#boucle
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortis de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        #ajouter un dossier vers la function showMovies avec le titre de chaque categorie.
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui() 
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request(); 
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')

    sPattern = '<a href="([^<]+)"><img data-src="([^<]+)" alt="([^<]+)"></a>.+?SYNOPSIS:([^<]+)</h2>.+?<a href=".+?">(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0])) #sortis de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2])) #sortis du titre
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1])) #sortis du poster

            if '/series' in sUrl:
                sTitle = aEntry[2]+' [COLOR azure]'+aEntry[4]+'[/COLOR]'
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', aEntry[1], aEntry[3], oOutputParameterHandler)
            else:
                sTitle = aEntry[2]+' [COLOR khaki]'+aEntry[4]+'[/COLOR]'
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[1], aEntry[3], oOutputParameterHandler)
                
            #il existe aussis addMisc(identifiant, function, titre, icon, poster, description, sortis parametre)
            #la difference et pour les metadonner serie, films ou sans
            
        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc

    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage


def __checkForNextPage(sHtmlContent): #cherche la page suivante
    sPattern = '<span>.+?<a href="(.+?)">.+?</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
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
    sHtmlContent = sHtmlContent.replace('<iframe src="" width="540" height="368" frameborder="0">','').replace('src="//www.youtube.com/','') 

    sPattern = '<iframe.+?src="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

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
    sHtmlContent = sHtmlContent.replace('<iframe src="http://youwatch.org/embed--540x368.html"','')
               
    sPattern = '<h2 style=".+?">([^<]+)<span.+?<iframe.+?src="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sEp = aEntry[0].replace('Vous regarder L\'', '').replace('de:', '')
            sTitle = sMovieTitle+' [COLOR azure]'+sEp+'[/COLOR]'
            sHosterUrl = str(aEntry[1])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
    