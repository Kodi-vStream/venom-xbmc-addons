#-*- coding: utf-8 -*-
# Par chataigne73
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib, urllib2
import xbmc

SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et series recentes en streaming et en telechargement'

URL_MAIN = 'http://www.libertyland.tv/'

URL_SEARCH = ('http://www.libertyland.tv/v2/recherche/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/nouveautes/', 'showMovies') # films nouveautés
MOVIE_VIEWS = (URL_MAIN + 'films/plus-vus-mois/', 'showMovies') # films + plus
MOVIE_NOTES = (URL_MAIN + 'films/les-mieux-notes/', 'showMovies') # films mieux notés
MOVIE_GENRES = (True, 'showGenre')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies') # films VOSTFR

SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'v2/mangas/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'typsearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vus', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films Les mieux notes', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes', 'series.png', oOutputParameterHandler)
              
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def typsearch():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('disp', 'search1')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Film', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('disp', 'search2')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Serie', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('disp', 'search3')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Anime', 'films.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
    
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action','http://www.libertyland.tv/films/genre/action.html'] )
    liste.append( ['Animation','http://www.libertyland.tv/films/genre/animation.html'] )
    liste.append( ['Aventure','http://www.libertyland.tv/films/genre/aventure.html/'] )
    liste.append( ['Biopic','http://www.libertyland.tv/films/genre/biopic.html'] )
    liste.append( ['Comedie','http://www.libertyland.tv/films/genre/comedie.html'] )
    liste.append( ['Comedie Dramatique','http://www.libertyland.tv/films/genre/comedie-dramatique.html'] )
    liste.append( ['Comedie Musicale','http://www.libertyland.tv/films/genre/comedie-musicale.html'] )
    liste.append( ['Drame','http://www.libertyland.tv/films/genre/drame.html'] )
    liste.append( ['Epouvante Horreur','http://www.libertyland.tv/films/genre/epouvante-horreur.html'] ) 
    liste.append( ['Espionnage','http://www.libertyland.tv/films/genre/espionnage.html'] )
    liste.append( ['Famille','http://www.libertyland.tv/films/genre/famille.html'] )
    liste.append( ['Fantastique','http://www.libertyland.tv/films/genre/fantastique.html'] )  
    liste.append( ['Guerre','http://www.libertyland.tv/films/genre/guerre.html'] )
    liste.append( ['Historique','http://www.libertyland.tv/films/genre/historique.html'] )
    liste.append( ['Judiciaire','http://www.libertyland.tv/films/genre/historique.html'] )
    liste.append( ['Medical','http://www.libertyland.tv/films/genre/musical.html'] )
    liste.append( ['Policier','http://www.libertyland.tv/films/genre/policier.html'] )
    liste.append( ['Peplum','http://www.libertyland.tv/films/genre/peplum.html'] )
    liste.append( ['Romance','http://www.libertyland.tv/films/genre/romance.html'] )
    liste.append( ['Science Fiction','http://www.libertyland.tv/films/genre/science-fiction.html'] )
    liste.append( ['Thriller','http://www.libertyland.tv/films/genre/thriller.html'] )
    liste.append( ['Western','http://www.libertyland.tv/films/genre/western.html'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        
        sPOST = ''
        sUrl2 = URL_SEARCH[0]
        sUrl = ''
        
        sDisp = oInputParameterHandler.getValue('disp')
       
        if (sDisp == 'search3'):#anime
            sPOST = 'categorie=mangas'
            sUrl = '/mangas/'
        elif (sDisp == 'search2'):#serie
            sPOST = 'categorie=series'
            sUrl = '/series/'
        elif (sDisp == 'search1'):#film
            sPOST = 'categorie=films'
        else:#tout le reste
            sPOST = 'categorie=films'
        
        sPOST = sPOST + '&mot_search=' + sSearch.replace(URL_SEARCH[0],'')    
        #sPOST = urllib.urllib.quote_plus(sPOST)
        
        request = urllib2.Request(sUrl2,sPOST)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        sHtmlContent = ''
        try: 
            reponse = urllib2.urlopen(request)
            sHtmlContent = reponse.read()
            reponse.close()
        except URLError, e:
            print e.read()
            print e.reason
    
        sPattern = '<h2 class="heading">\s*<a href="([^<>"]+)">([^<]+)<\/a>.+?<img class="img-responsive" *src="(.+?)"'
        
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = '<h2 class="heading"><a href="[^<>"]+?">([^<]+)<\/a>.+?<img class="img-responsive" src="([^<]+)" alt.+?(?:<font color="#00CC00">(.+?)<\/font>.+?)*<div class="divstreaming"><a href="([^<>"]+?)">'

    if '/mangas' in sUrl:
        sPattern = '<h2 class="heading"><a href="([^<>"]+?)">([^<]+)<\/a>.+?<img class="img-responsive" src="(.+?)" alt='
        
    #xbmc.log(sUrl)
    #fh = open('c:\\test.txt', "w")
    #sHtmlContent = sHtmlContent.replace('\n','').replace('\t','')
    #fh.write(sHtmlContent)
    #fh.close()
        
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            
            if sSearch or '/mangas' in sUrl:
                sTitle = aEntry[1]
                sUrl2 = str(aEntry[0])
                sThumb = str(aEntry[2])
                sQual = ''
            else:
                sTitle = aEntry[0]
                sUrl2 = str(aEntry[3])
                sThumb = str(aEntry[1])
            
                sQual = aEntry[2]
                if sQual:
                    sQual = sQual.decode("utf-8").replace(u' qualit\u00E9','').replace('et ','/')
                    sQual = sQual.replace('Bonne','MQ').replace('Haute','HQ').replace('Mauvaise','SD').encode("utf-8")
                    sQual = ' ('+ sQual + ')'
                    
            sTitle = sTitle.decode("utf-8").replace(u'T\u00E9l\u00E9charger ','')
            sTitle = sTitle.encode("utf-8")
            
            sDisplayTitle = sTitle + sQual
            sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            if '/series/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif '/mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)               
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            
        cConfig().finishDialog(dialog)
           
    sNextPage = __checkForNextPage(sHtmlContent)
    if (sNextPage != False):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent): 
    oParser = cParser()
    #sPattern = '</a></li><li class="active"><a href=\'#\'>.+?<\/a><\/li><li><a href="(.+?)">'
    sPattern = '<li><a href="([^<>"]+?)" class="next">Suivant &#187;<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def ReformatUrl(link):
    if '/v2/mangas' in link:
        return link
    if '/telecharger/' in link:
        return link.replace('telecharger','streaming')
    if '-telecharger-' in link:
        f = link.split('/')[-1]
        return '/'.join(link.split('/')[:-1])+ '/streaming/' + f.replace('-telecharger','')
    if '/v2/' in link:
        return link.replace('/v2/','/streaming/')   
    return link
    
    
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #refomatage url
    sUrl = ReformatUrl(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #sPattern = 'src="http:\/\/www\.libertyland\.tv\/v2\/hebergeur\/[^<>]+?"> ([^<>]+?) <font style=\'color:#f00\'>(.+?)<\/font><\/h4>.+?data-fancybox-type="ajax" href="(.+?)" class="fancybox fancybox\.iframe">'
    sPattern = 'src="http:\/\/www\.libertyland\.tv\/v2\/hebergeur\/[^>]+"> ([^<]+) <|data-fancybox-type="ajax" href="(.+?)" class="fancybox fancybox\.iframe">.+?<td data-title="Langue" class="separateur[^"]+">(.+?)<\/td><td data-title="Qualité" class="separateur[^"]+">(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    sPlayer = ''
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            if aEntry[0]:
                sPlayer = aEntry[0]
            else:
                sUrlLink = URL_MAIN+aEntry[1]
                sLang = aEntry[2].replace('French','VF')
                sLang = cUtil().removeHtmlTags(sLang)
                
                sTitle = ' (' + sLang + '/' + aEntry[3] + ')' + ' - [COLOR skyblue]' + sPlayer +'[/COLOR] ' + sMovieTitle
                #sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrlLink)
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
 
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
 
def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    
    oParser = cParser()
    sPattern = '(?:<h2 class="heading-small">(Saison .+?)</h2>)|(?:<li><a title="Titre \| (.+?)" class="num_episode" href="(.+?)">.+?<\/a><\/li>)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showSaisons', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)                
            else:
                sTitle = sMovieTitle + ' '+ aEntry[1].replace(',','')
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', aEntry[2])
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'seriesLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
 
def seriesLinks():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #refomatage url
    sUrl = ReformatUrl(sUrl)
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Gros calcul donc on delimite la zone
    sPattern = 'Choisissez une langue(.+?)Postez votre commentaires ici'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not (aResult[0] == True):
        xbmc.log('erreur de regex')
        sHtmlContent = ''
    else:
        sHtmlContent =  aResult[1][0]
    
    sPattern = 'data-fancybox-type="ajax" href="(.+?)" class="fancybox fancybox\.iframe">.+?Regarder sur:<\/span> <b>(.+?)<\/b> *<\/a> *<\/p> *<\/td><td data-title="Langue" class="[^"]+">(.+?)<\/td> *<td data-title="Qualité" class="separateur[^"]+">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        sPattern2 = '<a class="fancybox" href="(.+?)" data-fancybox-type="ajax".+?<td class=.separateu[^>]+>(.+?)<\/td><td class=.separateur[^>]+>(.+?)e<'
        aResult = oParser.parse(sHtmlContent, sPattern2)
        
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrlLink = aEntry[0]
            if not URL_MAIN in sUrlLink:
                sUrlLink = URL_MAIN + sUrlLink
            

            if len(aEntry) > 3:
                sLang = aEntry[2].replace('French','VF')
                sLang = cUtil().removeHtmlTags(sLang)
                
                sQual = aEntry[3]
                sQual = sQual.replace('Inconnue','???').replace('inconnu','???')
                
                sDisplayTitle = '(' + sLang + '/' + sQual + ')' + sMovieTitle
                sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
                
                sDisplayTitle = sDisplayTitle + ' [COLOR skyblue]' + aEntry[1] +'[/COLOR]'
            else:
                sLang = aEntry[1].replace('French','VF')
                sLang = cUtil().removeHtmlTags(sLang)

                sQual = aEntry[2]
                sQual = sQual.replace('Inconnue','???').replace('inconnu','???')
                
                sDisplayTitle = '(' + sLang + '/' + sQual + ')' + sMovieTitle
                sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
                
                sDisplayTitle = sDisplayTitle + ' [COLOR skyblue]' + '???' +'[/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', sUrlLink)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Plus de videos disponible[/COLOR]')

    oGui.setEndOfDirectory()
