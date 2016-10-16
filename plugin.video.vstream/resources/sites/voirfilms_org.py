#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import urllib2,urllib,re,xbmc
 
 
SITE_IDENTIFIER = 'voirfilms_org'
SITE_NAME = 'VoirFilms.org'
SITE_DESC = 'Films et serie en streaming'
 
URL_MAIN = 'http://www.voirfilms.co/'

MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_MOVIE = ('http://', 'showAlpha')
MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIES = (URL_MAIN + 'series/alphabet/', 'AlphaSearch')
SERIE_NEWS = (URL_MAIN + 'series/page-1', 'showMovies')
  
ANIM_ANIMS = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'animes/page-1', 'showMovies')
  
URL_SEARCH = ('', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Tout les films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films par Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries nouveautees', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries liste complete', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes Nouveautes', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes Liste complete', 'series.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return
        
def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    for i in range(0,27) :
        cConfig().updateDialog(dialog, 36)
        
        if (i > 0):
            sTitle = chr(64+i)
        else:
            sTitle = '09'
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.upper() )
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]', 'genres.png', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()           
   
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'action_1'] )
    liste.append( ['Animation',URL_MAIN + 'animation_1'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux_1'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure_1'] )
    liste.append( ['Biopic',URL_MAIN + 'biopic_1'] )
    liste.append( ['Comedie',URL_MAIN + 'comedie_1'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'comedie-dramatique_1'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire_1'] )
    liste.append( ['Drame',URL_MAIN + 'drame_1'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur_1'] )
    liste.append( ['Espionnage',URL_MAIN + 'espionnage_1'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique_1'] )  
    liste.append( ['Guerre',URL_MAIN + 'guerre_1'] )
    liste.append( ['Historique',URL_MAIN + 'historique_1'] )
    liste.append( ['Musical',URL_MAIN + 'musical_1'] )
    liste.append( ['Policier',URL_MAIN + 'policier_1'] )
    liste.append( ['Romance',URL_MAIN + 'romance_1'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction_1'] )
    liste.append( ['Serie',URL_MAIN + 'series_1'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller_1'] )
    liste.append( ['Western',URL_MAIN + 'western_1'] )
    liste.append( ['Divers',URL_MAIN + 'non-classe_1'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showAlpha():
    oGui = cGui()
 
    liste = []
    liste.append( ['0',URL_MAIN + 'alphabet/0/1'] )
    liste.append( ['1',URL_MAIN + 'alphabet/1/1'] )
    liste.append( ['2',URL_MAIN + 'alphabet/2/1'] )
    liste.append( ['3',URL_MAIN + 'alphabet/3/1'] )
    liste.append( ['4',URL_MAIN + 'alphabet/4/1'] )
    liste.append( ['5',URL_MAIN + 'alphabet/5/1'] )
    liste.append( ['6',URL_MAIN + 'alphabet/6/1'] )
    liste.append( ['7',URL_MAIN + 'alphabet/7/1'] )
    liste.append( ['8',URL_MAIN + 'alphabet/8/1'] )
    liste.append( ['9',URL_MAIN + 'alphabet/9/1'] )
    liste.append( ['A',URL_MAIN + 'alphabet/a/1'] )
    liste.append( ['B',URL_MAIN + 'alphabet/b/1'] )
    liste.append( ['C',URL_MAIN + 'alphabet/c/1'] )
    liste.append( ['D',URL_MAIN + 'alphabet/d/1'] )
    liste.append( ['E',URL_MAIN + 'alphabet/e/1'] )
    liste.append( ['F',URL_MAIN + 'alphabet/f/1'] )
    liste.append( ['G',URL_MAIN + 'alphabet/g/1'] )
    liste.append( ['H',URL_MAIN + 'alphabet/h/1'] )
    liste.append( ['I',URL_MAIN + 'alphabet/i/1'] )
    liste.append( ['J',URL_MAIN + 'alphabet/j/1'] )
    liste.append( ['K',URL_MAIN + 'alphabet/k/1'] )
    liste.append( ['L',URL_MAIN + 'alphabet/l/1'] )
    liste.append( ['M',URL_MAIN + 'alphabet/m/1'] )
    liste.append( ['N',URL_MAIN + 'alphabet/n/1'] )
    liste.append( ['O',URL_MAIN + 'alphabet/o/1'] )
    liste.append( ['P',URL_MAIN + 'alphabet/p/1'] )
    liste.append( ['R',URL_MAIN + 'alphabet/r/1'] )
    liste.append( ['S',URL_MAIN + 'alphabet/s/1'] )
    liste.append( ['T',URL_MAIN + 'alphabet/t/1'] )
    liste.append( ['U',URL_MAIN + 'alphabet/u/1'] )
    liste.append( ['V',URL_MAIN + 'alphabet/v/1'] )
    liste.append( ['W',URL_MAIN + 'alphabet/w/1'] )
    liste.append( ['X',URL_MAIN + 'alphabet/x/1'] )
    liste.append( ['Y',URL_MAIN + 'alphabet/y/1'] )
    liste.append( ['Z',URL_MAIN + 'alphabet/z/1'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
   
    if sSearch:
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)
 
        query_args = { 'action' : 'recherche' , 'story' : str(sSearch) }
        
        xbmc.log(str(query_args))
        
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = URL_MAIN + 'rechercher'
        request = urllib2.Request(url,data,headers)
     
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
     
        sHtmlContent = reponse.read()

        sPattern = '<div class="imagefilm">.+?<img src="(.+?)".+?<a href="([^<>]+?)".+?titreunfilm" style="width:145px;"> *(.+?) *<\/div>'
 
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        #sPattern = '<div class="imagefilm"> *<a href="(.+?)" title="(.+?)".+?<img src="(.+?)" alt="(.+?)"'
        sPattern = '<div class="imagefilm">.+?<img src="(.+?)".+?<a href="([^<>]+?)".+?titreunfilm" style="width:145px;">(.+?)<\/div>'
    
    sHtmlContent = sHtmlContent.replace('\n','')

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if not (aResult[0] == False):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sTitle = cUtil().unescape(aEntry[2])
            sPicture = str(aEntry[0])
            if not 'http' in sPicture:
                sPicture = URL_MAIN + sPicture
                
            sUrl = str(aEntry[1])
            if not 'http' in sUrl:
                sUrl = URL_MAIN + sUrl
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sPicture) #sortis du poster
 
            if '/serie/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
            elif '/anime/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
                #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^'<>]+?)' rel='nofollow'>suiv »</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        next = aResult[1][0].replace(URL_MAIN, '')
        return URL_MAIN + next
 
    return False
 
def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<a href="([^<>"]+?)" target="filmPlayer".+?class="([a-zA-Z]+)L"><\/span> *<\/div><span class="gras">.+?>(.+?)<\/span>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = '(' + str(aEntry[1]) + ') [' + str(aEntry[2]) + '] ' + sMovieTitle
            sUrl = aEntry[0].replace('https://', 'http://')
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sDisplayTitle , sThumbnail, sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()   
    

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #xbmc.log(sUrl)
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    if '-saison-' in sUrl or '/anime/' in sUrl:
        sPattern = '<li class="description132"><a class="n_episode2" title=".+?" href="(.+?)">(.+?)<\/a><\/li>'
    else:
        sMovieTitle = ''
        sPattern = '<div class="unepetitesaisons"> +<a href="(.+?)" title="(.+?)"> +<div class="saisonimage">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sEp = str(aEntry[1])
            sEp = re.sub('<span>(.+?)<\/span>','Episode \\1', str(sEp))
                
            sTitle = sMovieTitle + sEp
            sUrl = str(aEntry[0])
            if 'http' not in sUrl:
                sUrl = URL_MAIN + sUrl
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
 
            if '-episode-' in aEntry[0] or '/anime/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)    

    oGui.setEndOfDirectory()
    
def showHostersLink():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #patch a virer a la V17 de kodi
    import ssl
    ssl.PROTOCOL_SSLv23 = ssl.PROTOCOL_TLSv1
    
    #On recupere la redirection
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sUrl = oRequestHandler.getRealUrl()
    
    #Modifications
    sUrl = sUrl.replace('1wskdbkp.xyz','youwatch.org')

    xbmc.log(sUrl)
   
    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
    
