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
import xbmc, re
#from resources.lib.util import cUtil #outils pouvant etre utiles

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc
SITE_IDENTIFIER = 'zone_telechargement_eu' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = '[COLOR violet]Zone-Telechargement.eu[/COLOR]' # nom que xbmc affiche
SITE_DESC = 'Films en DDL et streaming' #description courte de votre source

URL_MAIN = 'http://www.zone-telechargement.eu/' # url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle seras affichee.
URL_SEARCH = ('http://www.zone-telechargement.eu/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://www.zone-telechargement.eu/trending/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Tendances', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://www.zone-telechargement.eu/series/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://www.zone-telechargement.eu/films/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://www.zone-telechargement.eu/ratings/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Evaluations', 'films_comments.png', oOutputParameterHandler)

    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Genres', 'films_genres.png', oOutputParameterHandler)

    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Année de sortie', 'news.png', oOutputParameterHandler)

    xbmc.executebuiltin('Container.SetViewMode(500)')
    oGui.setEndOfDirectory() #ferme l'affichage

def showGenres(): #affiche les genres
    oGui = cGui()

    oRequestHandler = cRequestHandler('http://www.zone-telechargement.eu/') # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi

    sPattern = '<li class="cat-item.+?<a href="(.+?)">(.+?)</a>.+?</li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #juste a entrer les caterories et les liens qui vont bien
    liste = []
    if aResult[0]:
        for aEntry in aResult[1]:
            liste.append([aEntry[1], aEntry[0]])

    for sTitle,sUrl in liste:#boucle
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        #ajouter un dossier vers la function showMovies avec le titre de chaque categorie.

    oGui.setEndOfDirectory()

def showYears(): #affiche les genres
    oGui = cGui()

    oRequestHandler = cRequestHandler('http://www.zone-telechargement.eu/') # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi

    sPattern = '<a href="(http://www.zone-telechargement.eu/release/(\d+?)/)">.+?</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #juste a entrer les caterories et les liens qui vont bien
    liste = []
    if aResult[0]:
        for aEntry in aResult[1]:
            liste.append([aEntry[1], aEntry[0]])

    for sTitle,sUrl in liste:#boucle
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'searchtmdb.png', oOutputParameterHandler)
        #ajouter un dossier vers la function showMovies avec le titre de chaque categorie.

    oGui.setEndOfDirectory()

def showSearch(): #function de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #apelle le clavier xbmx
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  #modifi l'url de recherche
        showMovies(sUrl) #apelle la function qui pouras lire la page de resultats
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = '', page = 1):
    oGui = cGui() #ouvre l'affichage

    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl') # recupere l'url sortie en parametre

    oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi

    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    #la function replace et pratique pour supprimer un code du resultat

    sPattern = '<article.+?<img src="(.+?)".+?<a href="(.+?)">(.+?)</a>.+?</article>'

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
            sTitle = aEntry[2]
            sUrl = aEntry[1]
            sThumbnail = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail) #sortie du poster

            result = re.search('eu/series', sUrl)
            if result:
                oGui.addMovie(SITE_IDENTIFIER, 'showSeriesHosters', sTitle, '', sThumbnail, sUrl, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sUrl, oOutputParameterHandler)

            #il existe aussis addMisc(identifiant, function, titre, icon, poster, description, sortie parametre)
            #la difference et pour les metadonner serie, films ou sans

        cConfig().finishDialog(dialog)# fin du dialog

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entree pour le lien Next | pas de addMisc pas de poster et de description inutile donc

    xbmc.executebuiltin('Container.SetViewMode(500)')
    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage

def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = '<div class=\'resppages\'>.+?href="(.+?)".+?</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult #affiche le result dans le log
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeriesHosters():# recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sUrl = oInputParameterHandler.getValue('siteUrl')  # apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #apelle le titre
    sThumbnail = oInputParameterHandler.getValue('sThumbnail') # apelle le poster
    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request(); #requete sur l'url

    oParser = cParser()
    #                            0:url              #1:image                     2:number                    3:title
    sPattern = '<li>.+?<a href="(.+?)".+?<img src="(.+?)".+?<div class="numerando">(.+?)</div>.+?<a href=".+?">(.+?)</a>.+?</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumbnail = aEntry[1]
            sNumber = aEntry[2]
            parts = sNumber.split('-')
            if len(parts) == 2:
                sNumber = 'S%02dE%02d' % (int(parts[0]), int(parts[1]))
            sTitle = aEntry[3]
            sDisplayTitle = '[COLOR yellow]['+sNumber+'][/COLOR] '+sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            title = sMovieTitle+' ['+sNumber+'] '+sTitle
            oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', title) #sortie du titre
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail) #sortie du poster

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sUrl, oOutputParameterHandler)

    oGui.setEndOfDirectory() #ferme l'affichage

def showHosters():# recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sUrl = oInputParameterHandler.getValue('siteUrl')  # apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #apelle le titre
    sThumbnail = oInputParameterHandler.getValue('sThumbnail') # apelle le poster

    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request(); #requete sur l'url
    #supprimer a l'aide de replace toute les entrer qui corresponde a votre recherche mais ne doivent pas etre pris en compte

    oParser = cParser()
    #                                      0:url                     1:hoster           2:type           3:langue          4:size
    sPattern = '<tr id=.+?<td><a .+?href="(.+?)".+?</td>.*?<td><img.+?>(.+?)</td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.+?</tr>'
    #ici nous cherchont toute les sources iframe
    aResult = oParser.parse(sHtmlContent, sPattern)
    #penser a faire un print aResult pour verifier

    #si un lien ne s'affiche pas peux etre que l'hote n'est pas supporte par l'addon
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sHoster = aEntry[1]
            sType = aEntry[2]
            sLang = aEntry[3]
            sSize = aEntry[4]

            sDisplayTitle = '[COLOR teal]['+sType+']['+sLang+']['+sSize+'] '+sHoster+'[/COLOR] '+sMovieTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'decodeLink', sDisplayTitle, '', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory() #fin

def decodeLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request(); #requete sur l'url

    oParser = cParser()
    sPattern = 'window.location.href=\'(.+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle) #nom affiche
            oHoster.setFileName(sMovieTitle) # idem
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
