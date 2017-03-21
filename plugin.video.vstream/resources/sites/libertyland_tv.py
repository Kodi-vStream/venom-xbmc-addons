#-*- coding: utf-8 -*-
# Par chataigne73
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re,urllib2


SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et series recentes en streaming et en telechargement'

URL_MAIN = 'http://libertyland.co/'

URL_SEARCH = (URL_MAIN + 'v2/recherche/', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vus', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films Les mieux notés', 'films_notes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('type', 'film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Film', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('type', 'serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Série', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('type', 'anime')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Animé', 'animes.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 
    
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'films/genre/action.html'] )
    liste.append( ['Animation',URL_MAIN + 'films/genre/animation.html'] )
    liste.append( ['Arts martiaux',URL_MAIN + 'films/genre/arts-martiaux.html/'] )
    liste.append( ['Aventure',URL_MAIN + 'films/genre/aventure.html/'] )
    liste.append( ['Biographie',URL_MAIN + 'films/genre/biographie.html'] )
    liste.append( ['Comedie',URL_MAIN + 'films/genre/comedie.html'] )
    liste.append( ['Crime',URL_MAIN + 'films/genre/crime.html'] )
    liste.append( ['Drame',URL_MAIN + 'films/genre/drame.html'] )
    liste.append( ['Espionnage',URL_MAIN + 'films/genre/espionnage.html'] )
    liste.append( ['Fantastique',URL_MAIN + 'films/genre/fantastique.html'] )  
    liste.append( ['Guerre',URL_MAIN + 'films/genre/guerre.html'] )
    liste.append( ['Histoire',URL_MAIN + 'films/genre/histoire.html'] )
    liste.append( ['Horreur',URL_MAIN + 'films/genre/horreur.html'] ) 
    liste.append( ['Musical',URL_MAIN + 'films/genre/musical.html'] )
    liste.append( ['Policier',URL_MAIN + 'films/genre/policier.html'] )
    liste.append( ['Romance',URL_MAIN + 'films/genre/romance.html'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'films/genre/science-fiction.html'] )
    liste.append( ['Sport',URL_MAIN + 'films/genre/sport.html'] )
    liste.append( ['Thriller',URL_MAIN + 'films/genre/thriller.html'] )
    liste.append( ['Western',URL_MAIN + 'films/genre/western.html'] )
	#la suite fonctionnent mais n'est pas répertorié dans le moteur de genre du site
    liste.append( ['Biopic',URL_MAIN + 'films/genre/biopic.html'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'films/genre/comedie-dramatique.html'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'films/genre/comedie-musicale.html'] )
    liste.append( ['Famille',URL_MAIN + 'films/genre/famille.html'] )
    liste.append( ['Historique',URL_MAIN + 'films/genre/historique.html'] )
    liste.append( ['Judiciaire',URL_MAIN + 'films/genre/judiciaire.html'] )
    liste.append( ['Médical',URL_MAIN + 'films/genre/medical.html'] )
    liste.append( ['Péplum',URL_MAIN + 'films/genre/peplum.html'] )

                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        
        scategorie = ''
        sUrl = ''
        
        sType = oInputParameterHandler.getValue('type')
       
        if (sType == 'anime'):#anime
            scategorie = 'mangas'
            sUrl = '/mangas/'
        elif (sType == 'serie'):#serie
            scategorie = 'series'
        elif (sType == 'film'):#film
            scategorie = 'films'
        else:#tout le reste
            scategorie = 'films'
        
        sPOST = 'categorie=' + scategorie + '&mot_search=' + sSearch.replace(URL_SEARCH[0],'')    

        request = urllib2.Request(URL_SEARCH[0],sPOST)
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
        
        sPattern = '<h2 class="heading"> *<a href="[^<>"]+?">([^<]+)<\/a>.+?<img class="img-responsive" *src="([^<]+)" *alt.+?(?:<font color="#00CC00">(.+?)<\/font>.+?)*<div class="divstreaming"> *<a href="([^<>"]+?)">'

    if '/mangas' in sUrl:
        sPattern = '<h2 class="heading"> *<a href="([^<>"]+?)">([^<]+)<\/a>.+?<img class="img-responsive" *src="(.+?)" *alt='  
  
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

            if '/series/' in sUrl or '/series/' in sUrl2:
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
    if ('/v2/' in link) and ('/streaming/' in link):
        return link.replace('/v2/','/')   
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
    sPattern = 'src="http:\/\/libertyland\.co\/v2\/hebergeur\/[^>]+"> ([^<]+) <|data-fancybox-type="ajax" href="(.+?)" class="fancybox fancybox\.iframe">.+?<td data-title="Langue" class="separateur[^"]+">(.+?)<\/td> *<td data-title="Qualité" class="separateur[^"]+">(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    sPlayer = ''
    listdoublon = []
    
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
                
                sUrlLink = aEntry[1]
                if not sUrlLink.startswith('http'):
                    sUrlLink = URL_MAIN + sUrlLink
                    
                sLang = aEntry[2].replace('French','VF')
                sLang = cUtil().removeHtmlTags(sLang)
                
                sTitle = ' (' + sLang + '/' + aEntry[3] + ')' + ' - [COLOR skyblue]' + sPlayer +'[/COLOR] ' + sMovieTitle
                
                #test de doublon
                if sUrlLink not in listdoublon:
                    listdoublon.append(sUrlLink)
                else:
                    continue
                
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
    sPattern = '<(?:iframe|embed).+?src="(.+?)"'
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
    sPattern = '(?:<h2 class="heading-small">(Saison .+?)</h2>)|(?:<li><a title=".+? \| (.+?)" class="num_episode" href="(.+?)">.+?<\/a><\/li>)'
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
    sPattern = 'Choisissez une langue(.+?)<div class="blogmetas" *>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not (aResult[0] == True):
        print 'erreur de regex'

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
        
        listdoublon = []
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrlLink = aEntry[0]
            if not 'http' in sUrlLink:
                sUrlLink = URL_MAIN + sUrlLink
            
            #test de doublon
            if sUrlLink not in listdoublon:
                listdoublon.append(sUrlLink)
            else:
                continue

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
