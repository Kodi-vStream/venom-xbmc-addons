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
from HTMLParser import HTMLParser

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

SITE_IDENTIFIER = 'frenchddl_com' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = '[COLOR violet]FRENCHDDL.com[/COLOR]' # nom que xbmc affiche
SITE_DESC = 'films en ddl' #description courte de votre source

URL_MAIN = 'http://www.frenchddl.com/' # url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle seras affichee.
URL_SEARCH = ('http://www.frenchddl.com/index.php?Query=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    #Ajoute lien dossier (identifant, function a attendre, nom, icon, parametre de sortie)
    #Puisque nous ne voulons pas atteindre une url on peut mettre ce qu'on veut dans le parametre siteUrl

    oOutputParameterHandler.addParameter('siteUrl', 'http://www.frenchddl.com/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films', 'films.png', oOutputParameterHandler)

    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Genres', 'films_genres.png', oOutputParameterHandler)

    xbmc.executebuiltin('Container.SetViewMode(500)')
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch(): #function de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #apelle le clavier xbmx
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  #modifi l'url de recherche
        showMovies(sUrl) #apelle la function qui pouras lire la page de resultats
        oGui.setEndOfDirectory()
        return

def showGenres(): #affiche les genres
    oGui = cGui()

    oRequestHandler = cRequestHandler(URL_MAIN) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi
    sHtmlContent = sHtmlContent.decode('iso-8859-1').encode('utf8') # Site en latin1
    sPattern = '<td class="GenresCell"><a href=(.+?) class.+?>(.+?)</a></td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    liste = []
    if aResult[0]:
        for aEntry in aResult[1]:
            title = aEntry[1].replace('&eacute;', 'é')
            liste.append( [title,'http://www.frenchddl.com/'+aEntry[0]] )

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
    sHtmlContent = sHtmlContent.decode('iso-8859-1').encode('utf8') # Site en latin1

    sPattern = '<td class="FilmsTitre">(.+?)</tr>.+?<a href="([^"]+?)"><img src="(.+?)"'

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
            sTitle = re.sub('<[^<]+?>', '', aEntry[0])
            sUrl = URL_MAIN + '/' + aEntry[1]
            sThumbnail = aEntry[2]
            cConfig().updateDialog(dialog, total) #dialog update

            #L'array affiche vos info dans l'orde de sPattern en commencant a 0
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail) #sortie du poster

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
    sPattern = '<a href="([^"]+?)">></a>';
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult #affiche le result dans le log
    if (aResult[0] == True):
        print 'KKK '+aResult[1][0]
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
    sHtmlContent = sHtmlContent.decode('iso-8859-1').encode('utf8') # Site en latin1
    #supprimer a l'aide de replace toute les entrer qui corresponde a votre recherche mais ne doivent pas etre pris en compte

    oParser = cParser()
    #                             0:URL                                                                          1:lang                                               2:Type                                                 3:fmt                                                4:size
    sPattern = '<a href="([^"]+?)" rel=\'nofollow\' target=\'_blank\'.+?>T.+?<td align=\'center\' class=\'TextLink\'>(.+?)</td>.*?<td align=\'center\' class=\'TextLink\'>(.+?)</td>.*?<td align=\'center\' class=\'TextLink\'>(.+?)</td>.*?<td align=\'center\' class=\'TextLink\'>(.+?)</td>'
    #ici nous cherchont toute les sources iframe
    aResult = oParser.parse(sHtmlContent, sPattern)
    #penser a faire un print aResult pour verifier

    #si un lien ne s'affiche pas peux etre que l'hote n'est pas supporte par l'addon
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry[0])
            sLang = str(aEntry[1]).upper()
            sType = str(aEntry[2]).upper()
            sFmt = str(aEntry[3]).upper()
            sSize = str(aEntry[4]).upper()
            print 'KKK '+sHosterUrl
            sDisplay = '[COLOR teal]['+sType+']['+sLang+']['+sType+']['+sSize+'][/COLOR] '+sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
            if (oHoster != False):
                oHoster.setDisplayName(sDisplay) #nom affiche
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
