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
 
#Si vous créer une source et la déposer dans le dossier sites elle seras directement visible sous xbmc
 
SITE_IDENTIFIER = 'voirfilms_org' #identifant nom de votre fichier remplacer les espaces et les . par _ aucun caractere speciale
SITE_NAME = 'VoirFilms.org' # nom que xbmc affiche
SITE_DESC = 'Films en streaming' #description courte de votre source
 
URL_MAIN = 'http://www.voirfilms.org/' # url de votre source

MOVIE_NEWS = ('http://www.voirfilms.org/', 'showMovies')
MOVIE_ALLMOVIES = ('http://www.voirfilms.org/lesfilms1', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
  
URL_SEARCH = ('', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
 
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
 
def load(): #function charger automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage
 
    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortis du parametres siteUrl oublier pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ALLMOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ALLMOVIES[1], 'Tout les films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films par Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showAlpha', 'Films par Alphabet', 'genre.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory() #ferme l'affichage
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return  
            
   
def showGenre(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer c'est caterorie et les lien qui vont bien
    liste = []
    liste.append( ['Action','http://www.voirfilms.org/action_1'] )
    liste.append( ['Animation','http://www.voirfilms.org/animation_1'] )
    liste.append( ['Arts Martiaux','http://www.voirfilms.org/arts-martiaux_1'] )
    liste.append( ['Aventure','http://www.voirfilms.org/aventure_1'] )
    liste.append( ['Biopic','http://www.voirfilms.org/biopic_1'] )
    liste.append( ['Comedie','http://www.voirfilms.org/comedie_1'] )
    liste.append( ['Comedie Dramatique','http://www.voirfilms.org/comedie-dramatique_1'] )
    liste.append( ['Documentaire','http://www.voirfilms.org/documentaire_1'] )
    liste.append( ['Drame','http://www.voirfilms.org/drame_1'] )
    liste.append( ['Epouvante Horreur','http://www.voirfilms.org/epouvante-horreur_1'] )
    liste.append( ['Espionnage','http://www.voirfilms.org/espionnage_1'] )
    liste.append( ['Fantastique','http://www.voirfilms.org/fantastique_1'] )  
    liste.append( ['Guerre','http://www.voirfilms.org/guerre_1'] )
    liste.append( ['Historique','http://www.voirfilms.org/historique_1'] )
    liste.append( ['Musical','http://www.voirfilms.org/musical_1'] )
    liste.append( ['Policier','http://www.voirfilms.org/policier_1'] )
    liste.append( ['Romance','http://www.voirfilms.org/romance_1'] )
    liste.append( ['Science Fiction','http://www.voirfilms.org/science-fiction_1'] )
    liste.append( ['Serie','http://www.voirfilms.org/series_1'] )
    liste.append( ['Thriller','http://www.voirfilms.org/thriller_1'] )
    liste.append( ['Western','http://www.voirfilms.org/western_1'] )
    liste.append( ['Divers','http://www.voirfilms.org/non-classe_1'] )
               
    for sTitle,sUrl in liste:#boucle
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortis de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showAlpha(): #affiche les genres
    oGui = cGui()
 
    #juste a entrer c'est caterorie et les lien qui vont bien
    liste = []
    liste.append( ['0','http://www.voirfilms.org/alphabet/0/1'] )
    liste.append( ['1','http://www.voirfilms.org/alphabet/1/1'] )
    liste.append( ['2','http://www.voirfilms.org/alphabet/2/1'] )
    liste.append( ['3','http://www.voirfilms.org/alphabet/3/1'] )
    liste.append( ['4','http://www.voirfilms.org/alphabet/4/1'] )
    liste.append( ['5','http://www.voirfilms.org/alphabet/5/1'] )
    liste.append( ['6','http://www.voirfilms.org/alphabet/6/1'] )
    liste.append( ['7','http://www.voirfilms.org/alphabet/7/1'] )
    liste.append( ['8','http://www.voirfilms.org/alphabet/8/1'] )
    liste.append( ['9','http://www.voirfilms.org/alphabet/9/1'] )
    liste.append( ['A','http://www.voirfilms.org/alphabet/a/1'] )
    liste.append( ['B','http://www.voirfilms.org/alphabet/b/1'] )  
    liste.append( ['C','http://www.voirfilms.org/alphabet/c/1'] )
    liste.append( ['D','http://www.voirfilms.org/alphabet/d/1'] )
    liste.append( ['E','http://www.voirfilms.org/alphabet/e/1'] )
    liste.append( ['F','http://www.voirfilms.org/alphabet/f/1'] )
    liste.append( ['G','http://www.voirfilms.org/alphabet/g/1'] )
    liste.append( ['H','http://www.voirfilms.org/alphabet/h/1'] )
    liste.append( ['I','http://www.voirfilms.org/alphabet/i/1'] )
    liste.append( ['J','http://www.voirfilms.org/alphabet/j/1'] )
    liste.append( ['K','http://www.voirfilms.org/alphabet/k/1'] )
    liste.append( ['L','http://www.voirfilms.org/alphabet/l/1'] )
    liste.append( ['M','http://www.voirfilms.org/alphabet/m/1'] )
    liste.append( ['N','http://www.voirfilms.org/alphabet/n/1'] )
    liste.append( ['O','http://www.voirfilms.org/alphabet/o/1'] )
    liste.append( ['P','http://www.voirfilms.org/alphabet/p/1'] )
    liste.append( ['R','http://www.voirfilms.org/alphabet/r/1'] )
    liste.append( ['S','http://www.voirfilms.org/alphabet/s/1'] )
    liste.append( ['T','http://www.voirfilms.org/alphabet/t/1'] )
    liste.append( ['U','http://www.voirfilms.org/alphabet/u/1'] )
    liste.append( ['V','http://www.voirfilms.org/alphabet/v/1'] )
    liste.append( ['W','http://www.voirfilms.org/alphabet/w/1'] )
    liste.append( ['X','http://www.voirfilms.org/alphabet/x/1'] )
    liste.append( ['Y','http://www.voirfilms.org/alphabet/y/1'] )
    liste.append( ['Z','http://www.voirfilms.org/alphabet/z/1'] )
               
    for sTitle,sUrl in liste:#boucle
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)#sortis de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui() #ouvre l'affichage
   
    if sSearch:
        #print 'ok'
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)
 
        query_args = { 'do' : 'search' , 'subaction' : 'search' , 'story' : str(sSearch) , 'x' : '0', 'y' : '0'}
        
        #print query_args
        
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = 'http://www.voirfilms.org/rechercher'
        request = urllib2.Request(url,data,headers)
     
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
     
        sHtmlContent = reponse.read()

        sPattern = '<div class="imagefilm">.+?<a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"'
 
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = '<div class="imagefilm"> *<a href="(.+?)" title="(.+?)".+?<img src="(.+?)"'
    
    sHtmlContent = sHtmlContent.replace('\n','')    
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    #print aResult
   
    if not (aResult[0] == False):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
           
            sTitle = unescape(aEntry[1])
            sTitle = sTitle.replace('film ','')
            sTitle = sTitle.replace(' streaming','')
            sPicture = str(aEntry[2])
            if not 'http' in sPicture:
                sPicture = str(URL_MAIN) + sPicture
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sPicture) #sortis du poster
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            sNextPage = __checkForNextPage(sUrl)#cherche la page suivante
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
                #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc
 
    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage
   
def __checkForNextPage(sUrl): #cherche la page suivante
    sPattern = 'http:..www.voirfilms.org(.+?)([0-9]+)'
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        nbre = int(aResult[1][0][1])
        nbre = nbre + 1
        return 'http://www.voirfilms.org' + aResult[1][0][0] + str(nbre)
 
    return False
 
def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    #sPattern = 'submit\(\)"><span>([^<]+)<.span><.a>.+?name="levideo" value="(.+?)" type="hidden">'
    sPattern = 'uppercase;">(.+?)<\/span><span class="selected".+?name="levideo" value="(.+?)" type="hidden">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('data', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail) #sortis du poster
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', '[COLOR teal][' + str(aEntry[0]) + '][/COLOR] ' + sMovieTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
    
    
def showHostersLink():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sData = oInputParameterHandler.getValue('data')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    headers = {'User-Agent' : 'Mozilla 5.10'}
    data = None
    
    if not sData =='' :
        query_args = { 'levideo' : str(sData)}
        data = urllib.urlencode(query_args)
        
        url = sUrl + '#plateformes'
    else:
        url = sUrl
        
    request = urllib2.Request(url,data,headers)
          
    try: 
        reponse = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.read()
        print e.reason
          
    sHtmlContent = reponse.read()
    
    # fh = open('c:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    sPattern = '<div id="playerslist">\n<div class=".+?"><iframe src="([^<]+)".+?<\/iframe>'
    aResult = re.findall(sPattern, sHtmlContent)
    
    if len(aResult) > 0 :
        aResult = aResult[0]
        total = 1
        dialog = cConfig().createDialog(SITE_NAME)

        cConfig().updateDialog(dialog, total)

        #convertion pour vk
        aResult = aResult.replace('http://www.streamingentier.com/vk.php?code=','')
        
        sHosterUrl = str(aResult)
        print sHosterUrl
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()   
    
