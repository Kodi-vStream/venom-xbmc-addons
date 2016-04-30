#-*- coding: utf-8 -*-
#From chataigne73

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


SITE_IDENTIFIER = 'zone_telechargement_com' 
SITE_NAME = '[COLOR violet]Zone-telechargement[/COLOR]' 
SITE_DESC = '' 

URL_MAIN = 'http://www.zone-telechargement.com/'

URL_SEARCH_MOVIES = (URL_MAIN + 'films-gratuit.html?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'telecharger-series.html?q=', 'showMovies')
URL_SEARCH = (URL_MAIN + 'index.php?q=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

#MOVIE_NEWS = (URL_MAIN + 'films/dvdrip-bdrip/?showby=month', 'showMovies') # films nouveautés
MOVIE_NEWS = (URL_MAIN + 'films-gratuit.html', 'showMovies') # films nouveautés
MOVIE_EXCLUS = (URL_MAIN + 'exclus.html', 'showMovies') # exclus (films populaires)
MOVIE_VIEWS = (URL_MAIN + 'films-gratuit.html?tab=all&orderby_by=popular&orderby_order=desc', 'showMovies') # films + vus
MOVIE_NOTES = (URL_MAIN + 'films-gratuit.html?tab=all&orderby_by=rating&orderby_order=desc', 'showMovies') # films mieux notés
MOVIE_3D = (URL_MAIN + 'films-bluray-3d.html?periodlist[]=2010&periodlist[]=2000&periodlist[]=1990&hf=1', 'showMovies') # films en 3D
MOVIE_HDLIGHT = (URL_MAIN + 'x265-x264-hdlight.html', 'showMovies') # films en x265 et x264

MOVIE_GENRES = (True, 'showGenre')
#MOVIE_VF = (URL_MAIN + 'langues/french', 'showMovies') # films VF
MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies') # films VOSTFR
MOVIE_ANIME = (URL_MAIN + 'dessins-animes.html', 'showMovies') # dessins animes

SERIE_VF = (URL_MAIN + 'series-vf.html', 'showMovies') # serie VF
SERIE_VOSTFR = (URL_MAIN + 'series-vostfr.html', 'showMovies') # serie VOSTFR

ANIM_VFS = (URL_MAIN + 'animes-vf.html', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr.html', 'showMovies')

BLURAY_NEWS = (URL_MAIN + 'films-bluray-hd.html', 'showMovies') # derniers Blu-Rays
#SERIE_GENRE = (True, 'showGenre')
DOCU_NEWS = (URL_MAIN + 'documentaires-gratuit.html', 'showMovies') # derniers docu
TV_NEWS = (URL_MAIN + 'emissions-tv.html', 'showMovies') # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles.html', 'showMovies') # dernieres spectacles


def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de films', 'search.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche de series', 'search.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers Films ajoutes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', BLURAY_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, BLURAY_NEWS[1], 'Derniers Blu-rays ajoutes', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus vus', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les mieux notes', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films 3D', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films x265/x264', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Dessins Animes', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF[1], 'Dernieres Séries VF ajoutees', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'Dernieres Series VOSTFR ajoutées', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animes VOSTFR', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOCU_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Deniers Documentaires', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Dernieres Emissions TV', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Derniers Spectacles', 'films.png', oOutputParameterHandler)

    
    oGui.setEndOfDirectory() 

def showSearchMovies(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText +'&tab=all&orderby_by=popular&orderby_order=desc&displaychangeto=thumb'
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return  
    
def showSearchSeries(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_SERIES[0] + sSearchText +'&tab=all&orderby_by=popular&orderby_order=desc&displaychangeto=thumb'
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre(): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=1'] )
    liste.append( ['Animation',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=2'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=3'] )
    liste.append( ['Aventure',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=4'] )
    liste.append( ['Biopic',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=5'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=7'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=8'] )
    liste.append( ['Comedie',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=9'] )
    liste.append( ['Divers',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=10'] )
    liste.append( ['Documentaires',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=11'] )
    liste.append( ['Drame',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=12'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=13'] ) 
    liste.append( ['Espionnage',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=14'] )
    liste.append( ['Famille',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=15'] )
    liste.append( ['Fantastique',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=16'] )  
    liste.append( ['Guerre',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=17'] )
    liste.append( ['Historique',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=18'] )
    liste.append( ['Musical',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=19'] )
    liste.append( ['Peplum',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=6'] )
    liste.append( ['Policier',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=20'] )
    liste.append( ['Romance',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=21'] )
    liste.append( ['Science Fiction',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=22'] )
    liste.append( ['Thriller',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=23'] )
    liste.append( ['Western',URL_MAIN + 'films-dvdrip-bdrip.html?genrelist[]=24'] )
                
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
    
    if (aResult[0] == True):
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
        if (sNextPage != False):
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

    if (aResult[0] == True):
        #print aResult
        return aResult[1][0]
        
    return False

    
def showLinks():

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    print sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #Bon ici, grosse bataille, c'est un film ou une serie ?
    #On peut utiliser l'url redirigée ou cette astuce en test
    
    if 'infos_film.png' in sHtmlContent:
        showMoviesLinks(sHtmlContent)
    else:
        showSeriesLinks(sHtmlContent)
    
    return

    
def showMoviesLinks(sHtmlContent):
    print 'mode film'
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
        
    sPattern = '(http:\/\/www\.zone-telechargement\.com\/engine\/ba\.php\?id=[0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sBA = aResult[1][0]
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sUrl',sBA)
        oOutputParameterHandler.addParameter('sMovieTitle', 'Bande annonce')
        oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
        oGui.addMovie(SITE_IDENTIFIER, 'ShowBA', 'Bande annonce', '', sThumbnail, '', oOutputParameterHandler)
    
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles pour ce film :[/COLOR]')
    
    #on recherche d'abord la qualité courante
    sPattern = '<b>(?:<strong>)*Qualité (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    
    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]

    sTitle = sMovieTitle +  ' - [COLOR skyblue]' + sQual +'[/COLOR]'
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)
    
    #on regarde si dispo dans d'autres qualités
    sPattern = '<a title="Téléchargez.+?en (.+?)" href="(.+?)"><button class="button_subcat"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[0]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeriesLinks(sHtmlContent):
    print 'mode serie'
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
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
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addMovie(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
    
    #on regarde si dispo dans d'autres qualités
    sPattern1 = '<a title="Téléchargez.+?en ([^"]+?)" href="([^"]+?)"><button class="button_subcat"'
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
            oOutputParameterHandler.addParameter('sUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)            
    
    #on regarde si dispo d'autres saisons
    
    sPattern2 = '<a title="Téléchargez[^"]+?" href="([^"]+?)"><button class="button_subcat" style="font-size: 12px;height: 26px;width:190px;color:666666;letter-spacing:0.05em">([^<]+?)</button>'
    aResult2 = oParser.parse(sHtmlContent, sPattern2)
    #print aResult2
    
    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Saisons aussi disponibles pour cette série :[/COLOR]')
    
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
    sUrl = oInputParameterHandler.getValue('sUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    print sUrl
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #Fonction pour recuperer uniquement les liens
    sHtmlContent = Cutlink(sHtmlContent)
    #Si ca ressemble aux lien premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)
    
    oParser = cParser()
    
    sPattern = '<span style="color:#.{6}">([^>]+?)<\/span>(?:.(?!color))+?<a href="([^<>"]+?)" target="_blank">Télécharger<\/a>|>\[(Liens Premium) \]<|<span style="color:#FF0000">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
        
    if (aResult[0] == True):
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
                if 'Télécharger' in aEntry[2]:
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
                oOutputParameterHandler.addParameter('sUrl', aEntry[1])
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
    sUrl = oInputParameterHandler.getValue('sUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    #Fonction pour recuperer uniquement les liens
    sHtmlContent = Cutlink(sHtmlContent)
    #Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)
   
    oParser = cParser()
    
    sPattern = '<a href="([^"]+?)" target="_blank">([^<]+)<\/a>|<span style="color:#.{6}">([^<]+)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
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
                if 'Télécharger' in aEntry[2]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[2])+'[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]'+str(aEntry[2])+'[/COLOR]')
            else:
                sName = aEntry[1]
                sName = sName.replace('Télécharger','')
                sName = sName.replace('pisodes','pisode')
                
                sTitle = sMovieTitle + ' ' + sName
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', aEntry[0])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
   
            cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()
        
def Display_protected_link():
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('sUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()
    
    import xbmc
    xbmc.log(sUrl)
    
    #Est ce un lien dl-protect ?
    if 'dl-protect' in sUrl:
        sHtmlContent = DecryptDlProtect(sUrl)
        
        if sHtmlContent:
            sPattern_dlprotect = '><a href="(.+?)" target="_blank">'
            aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)
            
        else:
            oDialog = cConfig().createDialogOK('Desole, probleme de captcha.\n Veuillez un rentrer au un directement sur le site, le temps de reparer')
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
    
def Cutlink(sHtmlContent):
    oParser = cParser()
    sPattern = '<img src="http:\/\/www\.zone-telechargement\.com\/prez\/style\/v1\/liens\.png"(.+?)<div class="divinnews"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    
    return ''
    
def CutNonPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?i)Liens* Premium(.+?)Publié le '
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
    #print aResult
    if (aResult[0]):
        return aResult[1][0]

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
