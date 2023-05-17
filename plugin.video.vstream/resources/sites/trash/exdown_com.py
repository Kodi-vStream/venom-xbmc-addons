#-*- coding: utf-8 -*-
#From Patoche2025

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

import urllib, re
import xbmcgui
import xbmc

from resources.lib.dl_deprotect import DecryptDlProtect


SITE_IDENTIFIER = 'exdown_com' 
SITE_NAME = '[COLOR violet]Extreme Download[/COLOR]' 
SITE_DESC = 'Fichier en DDL, HD' 

URL_MAIN = 'http://www.exdown.net/'

URL_SEARCH = (URL_MAIN + 'index.php?do=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_BDRIPSD = (URL_MAIN + 'films-sd/dvdrip', 'showMovies') # films BDRIP_DVDRIP
MOVIE_VOSTFRSD = (URL_MAIN + 'films-sd/dvdrip-vostfr', 'showMovies') # films VOSTFR
MOVIE_DVDSCR = (URL_MAIN + 'films-sd/dvdscr-r5', 'showMovies') # films DVDSCR
MOVIE_TSCAM = (URL_MAIN + 'films-sd/ts-cam', 'showMovies') # films TS/CAM
MOVIE_FILMOGRAPHIE = (URL_MAIN + 'films-sd/filmographie', 'showMovies') # filmographie

MOVIE_BDRIPHD = (URL_MAIN + 'films-hd/bdrip-720p', 'showMovies') # films BDRIP 720P
MOVIE_BLURAY720P = (URL_MAIN + 'films-hd/bluray-720p', 'showMovies') # films BluRay 720P
MOVIE_BLURAY1080P = (URL_MAIN + 'films-hd/bluray-1080p', 'showMovies') # films BluRay 1080P
MOVIE_BLURAYVOSTFR = (URL_MAIN + 'films-hd/bluray-vostfr', 'showMovies') # films BluRay VOSTFR
MOVIE_BLURAY3D = (URL_MAIN + 'films-hd/bluray-vostfr', 'showMovies') # films BluRay 3D

MOVIE_CLASSIQUESD = (URL_MAIN + 'films-hd/films-classique/classiques-sd', 'showMovies') # films Classique SD
MOVIE_CLASSIQUEHD = (URL_MAIN + 'films-hd/films-classique/classiques-hd', 'showMovies') # films Classique HD

MOVIE_GENRES = (True, 'showGenre')
#MOVIE_VF = (URL_MAIN + 'langues/french', 'showMovies') # films VF
#MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies') # films VOSTFR
#MOVIE_ANIME = (URL_MAIN + 'dessins-animes.html', 'showMovies') # dessins animes

SERIE_SDVF = (URL_MAIN + 'series/vf', 'showMovies') # serie SD VF
SERIE_SDVOSTFR = (URL_MAIN + 'series/vostfr', 'showMovies') # serie SD VOSTFR
SERIE_PACKSD = (URL_MAIN + 'series-vostfr.html', 'showMovies') # serie PACK SERIES SD

SERIE_HDVF = (URL_MAIN + 'series-hd/hd-series-vf', 'showMovies') # serie HD VF
SERIE_HDVOSTFR = (URL_MAIN + 'series-hd/hd-series-vostfr', 'showMovies') # serie HD VOSTFR
SERIE_PACKHD = (URL_MAIN + 'series-hd/pack-series-hd', 'showMovies') # serie PACK SERIES HD

#SERIE_GENRE = (True, 'showGenre')

ANIM_FILMS = (URL_MAIN + 'mangas/manga-films', 'showMovies') # FILMS MANGAS
ANIM_VF = (URL_MAIN + 'mangas/series-vf', 'showMovies') # ANIMES VF
ANIM_VOSTFR = (URL_MAIN + 'mangas/series-vostfr', 'showMovies') # ANIMES VOSTFR


BLURAY_NEWS = (URL_MAIN + 'films-hd/full-bluray', 'showMovies') # derniers Blu-Rays


def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de films ou series', 'search.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIPSD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIPSD[1], 'films BDRIP_DVDRIP', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFRSD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFRSD[1], 'films VOSTFR', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIPHD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIPHD[1], 'films BDRIP 720P', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAY720P[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAY720P[1], 'films BluRay 720P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAY1080P[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAY1080P[1], 'films BluRay 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAYVOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAYVOSTFR[1], 'films BluRay VOSTFR', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAY3D[0])        
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAY3D[0], 'films BluRay 3D', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', BLURAY_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'BLURAY_NEWS[1]', 'derniers Blu-Rays', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_FILMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'ANIM_FILMS[1]', 'Film MANGAS', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF[0])
    oGui.addDir(SITE_IDENTIFIER, 'ANIM_VF[1]', 'ANIMES VF', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, 'ANIM_VOSTFR[1]', 'ANIMES VOSTFR', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF[1], 'serie SD VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'serie SD VOSTFR', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PACKSD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PACKSD[1], 'serie PACK SERIES SD', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HDVF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HDVF[1], 'serie HD VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HDVOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, 'SERIE_HDVOSTFR[1]', 'serie HD VOSTFR', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()     
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PACKHD[0])     
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'serie PACK SERIES HD', 'films.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 

def showSearchMovies(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText +'&tab=all&orderby_by=popular&orderby_order=desc&displaychangeto=thumb'
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return  
    
def showSearchSeries(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText):
        sUrl = URL_SEARCH_SERIES[0] + sSearchText +'&tab=all&orderby_by=popular&orderby_order=desc&displaychangeto=thumb'
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre(): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'tags/Action'] )
    liste.append( ['Animation',URL_MAIN + 'tags/Animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'tags/Arts+Martiaux'] )
    liste.append( ['Biopic',URL_MAIN + 'tags/Biopic'] )
    liste.append( ['Comedie',URL_MAIN + 'tags/Comédie'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'tags/Comédie+dramatique'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'tags/Comédie+musicale'] )
    liste.append( ['Drame',URL_MAIN + 'tags/Drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'tags/Epouvante-horreur'] ) 
    liste.append( ['Espionnage',URL_MAIN + 'tags/Espionnage'] )
    liste.append( ['Famille',URL_MAIN + 'tags/Famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'tags/Fantastique'] )  
    liste.append( ['Guerre',URL_MAIN + 'tags/Guerre'] )
    liste.append( ['Historique',URL_MAIN + 'tags/Historique'] )
    liste.append( ['Musical',URL_MAIN + 'tags/Musical'] )
    liste.append( ['Policier',URL_MAIN + 'tags/Policier'] )
    liste.append( ['Romance',URL_MAIN + 'tags/Romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'tags/Science+fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'tags/Thriller'] )
    liste.append( ['Western',URL_MAIN + 'tags/Western'] )
                
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
        
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div style="height:[0-9]{3}px;"><a title="" href="([^"]+)[^>]+?><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<a title="" href[^>]+?>([^<]+?)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult 
    
    if aResult[0]:
        total = len(aResult[1])        
        for aEntry in aResult[1]:

            sTitle = str(aEntry[2])
            sUrl2 = aEntry[0]
            sFanart =aEntry[1]
            sThumbnail=aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'films.png', sThumbnail, sFanart, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #tPassage en mode vignette sauf en cas de recherche globale
    if 'index.php?q=' not in sUrl:
        xbmc.executebuiltin('Container.SetViewMode(500)')
    
     
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a style="margin-left:2%;" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        #print aResult
        return aResult[1][0]
        
    return False

    
def showLinks():

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #print sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #Bon ici, grosse bataille, c'est un film ou une serie ?
    #On peut utiliser l'url redirigÃ©e ou cette astuce en test
    
    if 'infos_film.png' in sHtmlContent:
        if 'Ã©pisode par Ã©pisode' in sHtmlContent:
            showSeriesLinks(sHtmlContent)
        else:
            showMoviesLinks(sHtmlContent)
    else:
        showSeriesLinks(sHtmlContent)
    
    return

    
def showMoviesLinks(sHtmlContent):
    xbmc.log('mode film')
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''
    sCom = ''
    sBA = ''

    sPattern = 'itemprop="ratingValue">([0-9,]+)<\/span>.+?synopsis\.png" *\/*></div><br /><div align="center">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,'Note : ' + str(sNote))

    sPattern = '(http:\/\/www\.exdown\.net\/engine\/ba\.php\?id=[0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sBA = aResult[1][0]
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sUrl',sBA)
        oOutputParameterHandler.addParameter('sMovieTitle', 'Bande annonce')
        oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
        oGui.addMovie(SITE_IDENTIFIER, 'ShowBA', 'Bande annonce', '', sThumbnail, '', oOutputParameterHandler)
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]QualitÃ©s disponibles pour ce film :[/COLOR]')

    #on recherche d'abord la qualitÃ© courante
    sPattern = '<b>(?:<strong>)*QualitÃ© (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]

    sTitle = sMovieTitle +  ' - [COLOR skyblue]' + sQual +'[/COLOR]'
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualitÃ©s
    sPattern = '<a title="TÃ©lÃ©chargez.+?en (.+?)" href="(.+?)"><button class="button_subcat"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[0]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeriesLinks(sHtmlContent):
    xbmc.log('mode serie')
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #print sUrl

    oParser = cParser()
    
    #Mise Ã jour du titre
    sPattern = '<h1 style="font-family:\'Ubuntu Condensed\',\'Segoe UI\',Verdana,Helvetica,sans-serif;">(?:<span itemprop="name">)*([^<]+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sMovieTitle = aResult[1][0]
    
    #Utile ou pas ?
    sMovieTitle = sMovieTitle.replace('[Complete]','').replace('[ComplÃ¨te]','')
    
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]QualitÃ©s disponibles pour cette saison :[/COLOR]')
    
    #on recherche d'abord la qualitÃ© courante
    sPattern = '<span style="color:#[0-9a-z]{6}"><b>(?:<strong>)* *\[[^\]]+?\] ([^<]+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    
    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0]

    sDisplayTitle = cUtil().DecoTitle(sMovieTitle) +  ' - [COLOR skyblue]' + sQual + '[/COLOR]'
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addMovie(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
    
    #on regarde si dispo dans d'autres qualitÃ©s
    sPattern1 = '<a title="TÃ©lÃ©chargez.+?en ([^"]+?)" href="([^"]+?)"><button class="button_subcat"'
    aResult1 = oParser.parse(sHtmlContent, sPattern1)
    #print aResult1
    
    if (aResult1[0] == True):
        total = len(aResult1[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult1[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle) +  ' - [COLOR skyblue]' + aEntry[0]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)            
    
    #on regarde si dispo d'autres saisons
    
    sPattern2 = '<a title="TÃ©lÃ©chargez[^"]+?" href="([^"]+?)"><button class="button_subcat" style="font-size: 12px;height: 26px;width:190px;color:666666;letter-spacing:0.05em">([^<]+?)</button>'
    aResult2 = oParser.parse(sHtmlContent, sPattern2)
    #print aResult2
    
    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Saisons aussi disponibles pour cette sÃ©rie :[/COLOR]')
    
        for aEntry in aResult2[1]:

            sTitle = '[COLOR skyblue]' + aEntry[1]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))            
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, 'series.png', sThumbnail, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()    
 
def showHosters():# recherche et affiche les hotes
    #print "ZT:showHosters"
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    xbmc.log( sUrl )

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Fonction pour recuperer uniquement les liens
    sHtmlContent = Cutlink(sHtmlContent)    
    
    #Si ca ressemble aux lien premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)  
    
    oParser = cParser()
    
    sPattern = '<span style="color:#.{6}">([^>]+?)<\/span>(?:.(?!color))+?<a href="([^<>"]+?)" target="_blank">TÃ©lÃ©charger<\/a>|>\[(Liens Premium) \]<|<span style="color:#FF0000">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
        
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            if aEntry[2]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                if 'TÃ©lÃ©charger' in aEntry[2]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[2])+'[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]'+str(aEntry[2])+'[/COLOR]')
                    
            elif aEntry[3]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[3])+'[/COLOR]')
                
            else:
                sTitle = '[COLOR skyblue]' + aEntry[0]+ '[/COLOR] ' + sMovieTitle
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumbnail, '', oOutputParameterHandler)
   
            cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()

def showSeriesHosters():# recherche et affiche les hotes
    #print "ZT:showSeriesHosters"
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
    
    sPattern = '<a href="([^"]+?)" target="_blank">([^<]+)<\/a>|<span style="color:#.{6}">([^<]+)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    

    
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            #print aEntry
            if dialog.iscanceled():
                break
            
            if aEntry[2]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                if 'TÃ©lÃ©charger' in aEntry[2]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[2])+'[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]'+str(aEntry[2])+'[/COLOR]')
            else:
                sName = aEntry[1]
                sName = sName.replace('TÃ©lÃ©charger','')
                sName = sName.replace('pisodes','pisode')
                
                sTitle = sMovieTitle + ' ' + sName
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
   
            cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()
        
def Display_protected_link():
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()

    #xbmc.log(sUrl)
    
    #Est ce un lien dl-protect ?
    if 'dl-protect' in sUrl:
        sHtmlContent = DecryptDlProtect(sUrl) 
        
        if sHtmlContent:
            sPattern_dlprotect = '><a href="(.+?)" target="_blank">'
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
            if (oHoster):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                        
    oGui.setEndOfDirectory()
    
def Cutlink(sHtmlContent):
    oParser = cParser()
    sPattern = '<img src="https*:\/\/www\.exdown\.net\/prez\/style\/v1\/liens\.png"(.+?)<div class="divinnews"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    #ok c'est une page battarde, dernier essais
    else:
        sPattern = '<div  class="maincont">(.+?)<div class="divinnews"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        #print aResult
        if (aResult[0]):
            return aResult[1][0]
    
    return ''
    
def CutNonPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?i)Liens* Premium(.+?)PubliÃ© le '
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]

    #Si ca marche pas on renvois le code complet
    return sHtmlContent
    
def CutPremiumlinks(sHtmlContent):
    oParser = cParser()
    
    sPattern = '(?i)^(.+?)premium'
    aResult = oParser.parse(sHtmlContent, sPattern)
    res = ''
    if (aResult[0]):
        res = aResult[1][0]
    
    #si l'ordre a Ã©tÃ© chnage ou si il ya un probleme    
    if 'dl-protect.com' not in res:
        sPattern = '(?i) par .{1,2}pisode(.+?)$'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sHtmlContent = aResult[1][0]
    else:
        sHtmlContent = res

    #Si ca marche pas on renvois le code complet
    return sHtmlContent    

def ShowBA():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = 'src="(http[^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        oRequestHandler = cRequestHandler(aResult[1][0])
        sHtmlContent = oRequestHandler.request()
        
        sPattern = 'player_gen_cmedia=(.*?)&cfilm'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0]):
            url2 = 'http://www.allocine.fr/ws/AcVisiondataV4.ashx?media=%s' % (aResult[1][0])
            oRequestHandler = cRequestHandler(url2)
            sHtmlContent = oRequestHandler.request()
            
            sPattern = 'md_path="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if (aResult[0]):
                video = aResult[1][0]
                #print video
                
                import xbmcplugin
                import sys
                
                __handle__ = int(sys.argv[1])
                #from resources.lib.handler.pluginHandler import cPluginHandler
                #__handle__ = cPluginHandler().getPluginHandle()

                liz=xbmcgui.ListItem('Voir la bande annonce', iconImage="DefaultVideo.png")
                liz.setInfo( type="Video", infoLabels={ "Title": 'nom' } )
                liz.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=__handle__,url=video,listitem=liz)
                xbmcplugin.endOfDirectory(__handle__)
    
    return
