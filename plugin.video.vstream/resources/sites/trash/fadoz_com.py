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
from resources.lib.util import cUtil
import urllib2,urllib,re
import xbmcgui
#from t0mm0.common.net import Net
#import unicodedata
 
 
SITE_IDENTIFIER = 'fadoz_com' #identifant nom de votre fichier remplacer les espaces et les . par _ aucun caractere speciale
SITE_NAME = 'Fadoz.com' # nom que xbmc affiche
SITE_DESC = 'Film en streaming' #description courte de votre source
 
URL_MAIN = 'http://www.fadoz.com' # url de votre source
 
#definis les url pour les catégories principale ceci et automatique si la deffition et présente elle seras afficher.
 
MOVIE_NEWS = ('http://www.fadoz.com/rva/', 'showMovies')
 
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = ('http://www.fadoz.com/rva/index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
 
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
 
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortis du parametres siteUrl oublier pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
           
    oGui.setEndOfDirectory() #ferme l'affichage
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://www.fadoz.com/rva/index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=' + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showGenre(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer c'est caterorie et les lien qui vont bien
    liste = []
    liste.append( ['Action','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=1:action-&Itemid=13&layout=default'] )
    liste.append( ['Animation','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=2&Itemid=2'] )    
    liste.append( ['Aventure','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=4:aventure-&Itemid=14&layout=default'] )
    liste.append( ['Comedie','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=4:aventure-&Itemid=14&layout=default'] )
    liste.append( ['Documentaires','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=26&Itemid=4'] )
    liste.append( ['Drame','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=7:drame-&Itemid=16&layout=default'] )
    liste.append( ['Fantastique','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=8:fantastique-&Itemid=17&layout=default'] )    
    liste.append( ['Horreur','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=9:horreur-&Itemid=18&layout=default'] )
    liste.append( ['Policier','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=10:policier-&Itemid=19&layout=default'] )
    liste.append( ['Science Fiction','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=11:science-fiction-&Itemid=20&layout=default'] )
    liste.append( ['Spectacle','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=3&Itemid=5'] )    
    liste.append( ['Thriller','http://www.fadoz.com/rva/index.php?option=com_content&view=category&id=12:thriller-&Itemid=21&layout=default'] )
               
    for sTitle,sUrl in liste:#boucle
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortis de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui() #ouvre l'affichage
 
    if sSearch :
        sUrl = sSearch
        sPattern = '<fieldset>(\t|\n)+<div>(?:\t|\n)+<span class="small">(?:\r|\n|.)+?<.span>(\t|\n)+<a href="(.+?)">(\t|\n)+(.+?)<.a>'
    else :
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
       
        if (sUrl == 'http://www.fadoz.com/rva/') :
            sPattern = '<b><a style="font-size: 14px;" href="(.+?)" class="latestnews">(\t|\n)+(.+?)<.a><.b>'
        else:
            sPattern = '<td headers="tableOrdering">(\t|\n)+<a href="(.+?)">(\t|\n)+(.+?)<.a>'
 
    #print sUrl
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
       
    #oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sPattern)
   
    aResult = re.findall(sPattern, sHtmlContent)
   
    #print aResult
   
    if not (aResult == False):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            if sSearch:
                sTitle2 = aEntry[4]
                sUrl2 = aEntry[2]
            elif sUrl == 'http://www.fadoz.com/rva/' :
                sTitle2 = aEntry[2]
                sUrl2 = aEntry[0]
            else :
                sTitle2 = aEntry[3]
                sUrl2 = aEntry[1]
               
            #sTitle = sTitle.replace('film ','')
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle2))
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle2, 'films.png', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc
 
    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage
   
def __checkForNextPage(sHtmlContent): #cherche la page suivante
    sPattern = '<a href="([^<]+)" title="Suivant">Suivant<.a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return str(URL_MAIN) + aResult[1][0]
 
    return False
 
def showHosters():
    oGui = cGui()
   
    sLink = ''
    sThumb = ''
    sComm = ''
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
 
    #print sUrl
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
   
    sPattern = '<div class="article-content">(\t|\n)*<p style="text-align: center;"><img src="(.+?)" border="0"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sThumb = aResult[0][1]
       
    sHtmlContent = sHtmlContent.replace('\r','')
   
    #sPattern = '>>>>> histoire <<<< :(.|\r|)+center;">\r+(.+?)\r+<.p>'
    sPattern = '>>> histoire <<<(?:.+?)center;">(.+?)<.p>(?:.+?)>>>> Illimit'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sComm = unescape(aResult[0])
 
    sPattern = 'class="jwts_tabbertab" title="(.+?)">.+?<iframe src="(\/rva\/.+?)" width='
    aResult = re.findall(sPattern, sHtmlContent)
 
    #Si il n'a pas de selection de qualitéé
    if (aResult == []):
        sPattern = '<iframe src="(\/rva\/.+?)" width='
        aResult = re.findall(sPattern, sHtmlContent)
        aResult = [('???',aResult[0])]
 
       
    #print aResult
 
    if not (aResult == [] ):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sLink = str(URL_MAIN) + urllib.unquote(aEntry[1]).decode('utf8')
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sLink)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', '[COLOR teal][' + str(aEntry[0]) + '][/COLOR] ' + sMovieTitle, sThumb, sThumb, sComm, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
   
def showHostersLink():
    #En fait ici, tout leur lien sont sur le meme hebergeur d'ou le lien deja traduit
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')  
   
    #recuperation urls
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
   
    url = re.findall('"file":"(.+?)", "label":"(.+?)",', sHtmlContent)
   
    #dialogue final
   
    if (url):
        for aEntry in url:
 
            sTitle = '[COLOR teal][' + str(aEntry[1]) + '][/COLOR] ' + sMovieTitle
            sUrl = aEntry[0]
 
            sHosterUrl = str(sUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
           
        oGui.setEndOfDirectory()
