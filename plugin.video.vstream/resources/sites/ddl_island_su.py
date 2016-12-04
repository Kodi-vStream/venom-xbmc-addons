#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import urllib,re,urllib2
import xbmcgui
import xbmc
import xbmcaddon,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'ddl_island_su' 
SITE_NAME = '[COLOR violet]DDL-Island[/COLOR]' 
SITE_DESC = 'Fichier en DDL, HD' 

URL_MAIN = 'http://www.ddl-island.su/telechargement/'
URL_PROTECT = 'http://protect.ddl-island.su'

URL_SEARCH_MOVIES = ('http://www.ddl-island.su/recherche.php?categorie=99&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')
URL_SEARCH_SERIES = ('http://www.ddl-island.su/recherche.php?categorie=98&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')


URL_SEARCH = (URL_MAIN + 'index.php?q=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_SD = (URL_MAIN + 'telechargement/films-1.html&order=2', 'showMovies') # derniers films en SD
MOVIE_HD = (URL_MAIN + 'telechargement/films-hd-13.html&order=2', 'showMovies') # derniers films en HD
MOVIE_3D = (URL_MAIN + 'telechargement/films-3d-21.html&order=2', 'showMovies') # derniers films en 3D
MOVIE_SD_VIEWS = (URL_MAIN + 'telechargement/films-1.html&order=3', 'showMovies') # derniers films en SD
MOVIE_HD_VIEWS = (URL_MAIN + 'telechargement/films-hd-13.html&order=3', 'showMovies') # derniers films en HD
MOVIE_3D_VIEWS = (URL_MAIN + 'telechargement/films-3d-21.html&order=3', 'showMovies') # derniers films en 3D
MOVIE_TOP = ('http://www.ddl-island.su/telechargement-top-films', 'showMovies') # derniers films en 3D

SERIES_SD = (URL_MAIN + 'telechargement/series-tv-6.html&order=2', 'showMovies') # derniers films en SD
SERIES_HD = (URL_MAIN + 'telechargement/series-hd-20.html&order=2', 'showMovies') # derniers films en HD
SERIES_SD_VIEWS = (URL_MAIN + 'telechargement/series-tv-6.html&order=3', 'showMovies') # derniers films en SD
SERIES_HD_VIEWS = (URL_MAIN + 'telechargement/series-tv-6.html&order=3', 'showMovies') # derniers films en HD
SERIES_TOP = ('http://www.ddl-island.su/telechargement-top-series', 'showMovies') # derniers films en 3D

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de films', 'search.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche de series', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD[1], 'Derniers Films SD ajoutes', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Derniers Films HD ajoutes', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Derniers Films en 3D ajoutes', 'news.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VIEWS[1], 'Films SD les plus vus', 'films.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD_VIEWS[1], 'Films HD les plus vus', 'films.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D_VIEWS[1], 'Films 3D les plus vus', 'films.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Top Films du Mois', 'films.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD[1], 'Dernieres Séries SD ajoutees', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD[1], 'Dernieres Series HD ajoutees', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD_VIEWS[1], 'Series SD les plus vues', 'films.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD_VIEWS[1], 'Series HD les plus vues', 'films.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_TOP[1], 'Top Series du Mois', 'films.png', oOutputParameterHandler)  
        
    oGui.setEndOfDirectory() 

def showSearchMovies(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return
    
def showSearchSeries(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    bGlobal_Search = False
    if sSearch:
        
        #par defaut
        sUrl = sSearch
        
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
        
        #partie en test
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type') 
      
        if sType:
            if sType == "film":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_MOVIES[0])
            if sType == "serie":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_SERIES[0])
            if sType == "anime":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_ANIMS[0])

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 
        
    #print sUrl
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request()
    #print sHtmlContent
    sCom = ''
    sQual = ''
    if 'top' in sUrl:
        sPattern = '<div class="fiche_top20"><a class="top20" href="([^"]+)"><img src="([^"]+)" title="([^\|]+)\|\|[^\|]+?\|\|([^\|]+)\|\|[^\|]+?\|\|([^"]+)" /></a></div>'
    else:
        sPattern = '<div class="fiche_listing"><a href="([^"]+)"><img src="([^"]+)" alt="Télécharger([^"]+)"[^\|]+?\| *Qualité : ([^<]+)<br /><br />([^<]+)<br /><br />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult 
    
    if (aResult[0] == True):
        total = len(aResult[1])        
        for aEntry in aResult[1]:
            sQual = str(aEntry[3])
            sCom = str(aEntry[4])
            sTitle = str(aEntry[2])
            sUrl2 = aEntry[0]
            #print sUrl2
            #sFanart =aEntry[1]
            sThumbnail=aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sCom', sCom)
            sDisplayTitle = cUtil().DecoTitle(sTitle+' ('+sQual+')')
            
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
            

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #tPassage en mode vignette sauf en cas de recherche globale
    if not bGlobal_Search:
        xbmc.executebuiltin('Container.SetViewMode(500)')
    
     
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="page">.+?</div></td><td align="center"><a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        #print aResult
        return URL_MAIN+aResult[1][0]
        
    return False

def showLinks():
    print 'showLinks'
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'series' in sUrl:
        showSeriesReleases()
    else:
        showMoviesReleases()
    
    return

def showMoviesReleases():
    xbmc.log('showMoviesReleases')
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sCom = oInputParameterHandler.getValue('sCom')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl.replace('.html','')
    #print sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oGui = cGui()
    
    oParser = cParser()
    #cut de la zone des releases
    sPattern = 'Toutes</option>(.+?)>Hébergeur'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]
    
    sPattern = '<option value="([^"]+)"  id="([^"]+)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
	
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Releases disponibles pour ce film :[/COLOR]')

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            if ('rapidgator' not in aEntry[1]) and ('turbobit' not in aEntry[1]) and ('uploaded' not in aEntry[1]) and ('uptobox' not in aEntry[1]) :
                sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[1]+'[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
            cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()    
	


def showSeriesReleases():
    xbmc.log('showSeriesReleases')
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sCom = oInputParameterHandler.getValue('sCom')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl.replace('.html','')
    #print sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oGui = cGui()
    
    oParser = cParser()
    #cut de la zone des releases
    sPattern = 'Episode :</span>(.+?)>Hébergeur :'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]==False:
        sPattern = 'Release :</span>(.+?)>Hébergeur :'
        aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]
    
    sPattern = '<option value="([^"]+)"  id="([^"]+)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
	
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Releases disponibles pour ce film :[/COLOR]')

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            if ('rapidgator' not in aEntry[1]) and ('turbobit' not in aEntry[1]) and ('uploaded' not in aEntry[1]) and ('uptobox' not in aEntry[1]) :
                sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[1]+'[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
            cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()    

def showSeriesLinks():
    xbmc.log('mode serie')
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #print sUrl

    oParser = cParser()
    
    #Mise àjour du titre
    sPattern = '<h1 style="font-family:\'Ubuntu Condensed\',\'Segoe UI\',Verdana,Helvetica,sans-serif;">(?:<span itemprop="name">)*([^<]+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sMovieTitle = aResult[1][0]
    
    #Utile ou pas ?
    sMovieTitle = sMovieTitle.replace('[Complete]','').replace('[Complète]','')
    
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')
    
    #on recherche d'abord la qualité courante
    sPattern = '<span style="color:#[0-9a-z]{6}"><b>(?:<strong>)* *\[[^\]]+?\] ([^<]+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    
    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0]

    sDisplayTitle = cUtil().DecoTitle(sMovieTitle) +  ' - [COLOR skyblue]' + sQual + '[/COLOR]'
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)

	
def showHosters():# recherche et affiche les hotes
    print "showHosters"
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    #print sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #sPattern = '<span class=\'providers[^\']+?\' title=\'([^\']+\')\'></span>&nbsp;<a href=\'([^\']+)\' target=\'_blank\' title="([^"]+)"'
    sPattern = '<span class=\'providers.+?\' title=\'([^\']+)\'><\/span> *<a href=\'([^\']+)\' target=\'_blank\' title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    
        
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = '[COLOR skyblue]' + aEntry[0]+ '[/COLOR] ' + aEntry[2]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumbnail, '', oOutputParameterHandler)
   
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeriesHosters():# recherche et affiche les hotes

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Fonction pour recuperer uniquement les liens
    sHtmlContent = Cutlink(sHtmlContent)
    
    #Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)
   
    oParser = cParser()
    
    sPattern = '<a href="([^"]+?)" target="_blank">([^<]+)<|<span style="color:#.{6}">([^<]+)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    

    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            #print aEntry
            if dialog.iscanceled():
        
def Display_protected_link():
    print "Display_protected_link"
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()
    sUrl = sUrl.replace(URL_PROTECT,URL_PROTECT+'/other?id=')
    #print sUrl
    #xbmc.log(sUrl)
    
    #Est ce un lien dl-protect ?
    if URL_PROTECT in sUrl:
        sHtmlContent = DecryptddlProtect(sUrl) 
        #print sHtmlContent
        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = 'Lien :</b></td><td><a href="(.+?)"'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)
            
        else:
            oDialog = cConfig().createDialogOK('Desole, probleme de captcha.\n Veuillez en rentrer un directement sur le site, le temps de reparer')
            aResult_dlprotect = (False, False)

    #Si lien normal       
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl]) 
        
    #print aResult_dlprotect
        
    if (aResult_dlprotect[0]):
            
        episode = 1
        
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry
            #print sHosterUrl
            
            sTitle = sMovieTitle
            if len(aResult_dlprotect[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + str(episode)
            
            episode+=1
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                        
    oGui.setEndOfDirectory()

def DecryptddlProtect(url):
    print "DecryptddlProtect"
    if not (url): return ''
    
    cookies = ''
    #try to get previous cookie
    cookies = Readcookie('protect_ddl_island.su')
    
    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie',cookies)
    sHtmlContent = oRequestHandler.request()
    
    #Si ca demande le captcha
    if 'value="Submit form"' in sHtmlContent:
        if cookies:
		DeleteCookie('protect_ddl_island.su')	
        cookies = oRequestHandler.GetCookies()
        
        #save cookies
        SaveCookie('protect_ddl_island.su',cookies)

        s = re.findall('<img id="captcha" src="([^<>"]+?)"',sHtmlContent)
        if URL_PROTECT in s[0]:
            image = s[0]
        else:
            image = URL_PROTECT + s[0]
            
        captcha = get_response(image,cookies)
        id = url[-7:]

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParameters( 'captcha_code' , captcha)
        oRequestHandler.addParameters( 'submit' , 'Valider')
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        sHtmlContent = oRequestHandler.request()

        #print sHtmlContent    
        if 'Erreur : Le code n\'est pas valide' in sHtmlContent:
            cGui().showInfo("Erreur", 'Mauvais Captcha' , 5)
            return 'rate'
            
        #si captcha reussi
        #save cookies
        SaveCookie('protect_ddl_island.su',cookies)        
    
    return sHtmlContent  

    
def DeleteCookie(Domain):
    file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
    os.remove(os.path.join(PathCache,file))
    
def SaveCookie(Domain,data):
    Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

    #save it
    file = open(Name,'w')
    file.write(data)

    file.close()
    
def Readcookie(Domain):
    Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
    
    try:
        file = open(Name,'r')
        data = file.read()
        file.close()
    except:
        return ''
    
    return data
		

		
def get_response(img,cookie):    
    print "get_reponse"
    #on telecharge l'image
    filename  = os.path.join(PathCache,'Captcha.png')

    headers2 = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
        #'Referer' : url ,
        'Host' : 'protect.ddl-island.su',
        'Accept' : 'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Encoding' : 'gzip, deflate',
        #'Content-Type' : 'application/x-www-form-urlencoded',
        'Cookie' : cookie
        }
        
    try:
        req = urllib2.Request(img,None,headers2)
        image_on_web = urllib2.urlopen(req)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            downloaded_image = file(filename, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return ''
    except:
        return ''

    #on affiche le dialogue
    solution = ''
    try:
        img = xbmcgui.ControlImage(450, 0, 400, 130, filename)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        #xbmc.sleep(3000)
        kb = xbmc.Keyboard('', 'Tapez les Lettres/chiffres de l\'image', False)
        kb.doModal()
        if (kb.isConfirmed()):
            solution = kb.getText()
            if solution == '':
                cGui().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
        else:
            cGui().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
    finally:
        wdlg.removeControl(img)
        wdlg.close()
        
    return solution
