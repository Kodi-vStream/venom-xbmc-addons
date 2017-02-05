#-*- coding: utf-8 -*-
#Venom & johngf.
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
from resources.lib.player import cPlayer
import re,urllib2,urllib,xbmc,base64

#copie du site http://www.film-streaming.co/
#copie du site http://www.streaming-club.com/
#copie du site http://www.hd-stream.in/
#copie du site http://www.kaydo.ws/


SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo.ws (beta)'
SITE_DESC = 'Le seul site de streaming en HD 720p 100% Gratuit'

URL_MAIN = 'http://www.kaydo.ws/'
 
MOVIE_NEWS = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'populaires.php', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'best-rating.php', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films.php', 'showMovies')
 
MOVIE_GENRES = (True, 'showGenre')

SERIE_NEWS = (URL_MAIN + 'last-added-series.php', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series.php', 'showMovies')
 
URL_SEARCH = (URL_MAIN + 'search.php?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def Decode(chain):
    chain = 'aHR' + chain
    chain = 'M'.join(chain.split('7A4c1Y9T8c'))
    chain = 'V'.join(chain.split('8A5d1YX84A428s'))
    chain = ''.join(chain.split('$'))
    #xbmc.log(str(base64.b64decode(chain)))
    return base64.b64decode(chain) 
    
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'top-films.php')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Top Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Tout Les Films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series Nouveautes', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Toutes les Series', 'series.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return 
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Animation',URL_MAIN + 'genre.php?g=Animation'] )    
    liste.append( ['Action',URL_MAIN + 'genre.php?g=Action'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'genre.php?g=Arts%20Martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'genre.php?g=Aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'genre.php?g=Biopic'] )
    liste.append( ['Comedie',URL_MAIN + 'genre.php?g=Com%C3%A9die'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'genre.php?g=Com%C3%A9die%20dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + 'genre.php?g=Documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'genre.php?g=Drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'genre.php?g=Epouvante-horreur'] )
    liste.append( ['Espionage',URL_MAIN + 'genre.php?g=Espionnage'] )  
    liste.append( ['Fantastique',URL_MAIN + 'genre.php?g=Fantastique'] )
    liste.append( ['Famille',URL_MAIN + 'genre.php?g=Famille'] )
    liste.append( ['Guerre',URL_MAIN + 'genre.php?g=Guerre'] )
    liste.append( ['Historique',URL_MAIN + 'genre.php?g=Historique'] )
    liste.append( ['Musical',URL_MAIN + 'genre.php?g=Musical'] )
    liste.append( ['Policier',URL_MAIN + 'genre.php?g=Policier'] )
    liste.append( ['Romance',URL_MAIN + 'genre.php?g=Romance'] )
    liste.append( ['Sciense Fiction',URL_MAIN + 'genre.php?g=Science%20fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'genre.php?g=Thriller'] )
    liste.append( ['Western',URL_MAIN + 'genre.php?g=Western'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #modif url par Gregwar  
    if '?' in sUrl:
        sUrl += '&r=n'
    else:
        sUrl += '?r=n'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # fh = open('C:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    #sPattern = '<div class="box"> *<img src="([^"]+)" width=".+?" height=".+?">.+?<h2>([^<]+)</h2>.+?<p.*?>([^<]+)</p>.+?ref="([^"]+)">'

    sPattern = '<img src="([^"]+?)" width=".+?<h2>(.+?)</h2>.*?<h3>(.+?)</h3>.+?<p>([^<]+)</p><a class="btn.+?href="(.+?)"'
        
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sThumbnail = URL_MAIN+str(aEntry[0])
            siteUrl = URL_MAIN+str(aEntry[4])
            sCom = str(aEntry[3])
            sTitle = [str(aEntry[1]), str(aEntry[2])]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[1])
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail) 
            if 'details-serie.php' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showMovies', sTitle, 'series.png', sThumbnail, sCom, oOutputParameterHandler)
            elif '/series' in siteUrl or '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
    
def seriesHosters():
    oGui = cGui() 
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl') 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #modif url par Gregwar  
    if '?' in sUrl:
        sUrl += '&r=n'
    else:
        sUrl += '?r=n'
    oRequestHandler = cRequestHandler(sUrl+'&ep=0')
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()
    result = re.search('^(.+?)(|col s4 hide-on-med-and-down(.+?))$', sHtmlContent, re.DOTALL)
    sHtmlContent = result.group(1)
    sPattern = '<li><div class="truncate.+?</i>(.+?)</div>(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if 'ep=0&' in aEntry[1]:
                continue

            links = []
            result = re.search('href="(.+?ver=vf)"', aEntry[1])
            if result:
                links += [['VF', result.group(1)]]
            result = re.search('href="(.+?ver=vo)"', aEntry[1])
            if result:
                links += [['VOST', result.group(1)]]

            for t, link in links:
                oOutputParameterHandler = cOutputParameterHandler()
                sUrl = URL_MAIN+'/series/'+link+'&r=n'
                #name = aEntry[0] + ' ('+t+')'
                name = [aEntry[0], t]
                oOutputParameterHandler.addParameter('siteUrl', sUrl) 
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle) 
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail) 

                oGui.addTV(SITE_IDENTIFIER, 'showHosters', name, 'series.png', sThumbnail, sUrl, oOutputParameterHandler)


    oGui.setEndOfDirectory() #fin
         
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="pagination">.*?<li class="active">.+?<li><a href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        sUrl = URL_MAIN+aResult[1][0]     
        return sUrl 
 
    return False
 
def showHosters():
   
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail  = oInputParameterHandler.getValue('sThumbnail')
   
   #modif url par Gregwar  
    if '?' in sUrl:
        sUrl += '&r=n'
    else:
        sUrl += '?r=n'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     
    oParser = cParser()
    sPattern = '<video><source type="video/mp4" src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        BA = aResult[1][0]
    else:
        BA = False

    #sPattern = '{file:"([^\"]+?)"'
    #sPattern = '{file:"([^"]+)",label:"([^"]+)"'
    sPattern = '<script>function(.+?)</script>'
    aResult = re.search(sPattern,sHtmlContent)
    sHtmlContent = aResult.group(1).replace('return de("$")','') #serie
    #redirection sur hdstream pour les new videos
    sPattern = 'return.+?"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            url = Decode(str(aEntry))
            if 'manifest.mpd' in url or 'kaydo.ws/mp4' in url: #mp4 inutilisable pour le moment
                continue
                
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)       
            if (oHoster != False):            
                oHoster.setDisplayName(xbmc.getInfoLabel('ListItem.title'))
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
            
        if (BA != False):
            sHosterUrl2 = str(BA)
            oHoster2 = cHosterGui().checkHoster(sHosterUrl2)
            if (oHoster2 != False):            
                oHoster2.setDisplayName(sMovieTitle + '[COLOR coral]' + (' [Bande Annonce] ') + '[/COLOR]')
                oHoster2.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster2, sHosterUrl2, '') 
                  
        oGui.setEndOfDirectory()
