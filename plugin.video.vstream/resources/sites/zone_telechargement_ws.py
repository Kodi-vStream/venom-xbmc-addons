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
import random


#from resources.lib.dl_deprotect import DecryptDlProtect

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = { 'User-Agent' : UA }

SITE_IDENTIFIER = 'zone_telechargement_ws'
SITE_NAME = '[COLOR violet]Zone-Telechargement.ws[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = 'https://www.zone-telechargement.ws/'

URL_SEARCH = (URL_MAIN, 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'nouveaute/', 'showMovies') # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies') # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies') # films en 3D
MOVIE_HD = (URL_MAIN + 'films-bluray-hd/', 'showMovies') # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'x265-x264-hdlight/', 'showMovies') # films en x265 et x264
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-4k/', 'showMovies') # films en 4K
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies') # films VOSTFR

MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies') # dessins animes

SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies') # serie VOSTFR

ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')

DOC_DOCS = (URL_MAIN + 'documentaires-gratuit/', 'showMovies') # docs
SPORT_SPORTS = (URL_MAIN + 'sport/', 'showMovies') # sports
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies') # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies') # dernieres spectacles
CONCERT_NEWS = (URL_MAIN + 'concerts/', 'showMovies') # dernieres concerts
AUTOFORM_VID = (URL_MAIN + 'autoformations-videos/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Blu-rays (720p & 1080p)', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films 3D', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (x265 & x264)', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films 4K', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANIME[1], 'Dessins Animés', 'animes.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF (Derniers ajouts)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries VOSTFR (Derniers ajouts)', 'series_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés VF', 'animes_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés VOSTFR', 'animes_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_NEWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPECT_NEWS[1], 'Spectacles', 'star.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre(basePath):
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + basePath + '?genrelist[]=1'] )
    liste.append( ['Animation',URL_MAIN +  basePath + '?genrelist[]=2'] )
    liste.append( ['Arts Martiaux',URL_MAIN +  basePath + '?genrelist[]=3'] )
    liste.append( ['Aventure',URL_MAIN +  basePath + '?genrelist[]=4'] )
    liste.append( ['Biopic',URL_MAIN +  basePath + '?genrelist[]=5'] )
    liste.append( ['Comédie Dramatique',URL_MAIN +  basePath + '?genrelist[]=7'] )
    liste.append( ['Comédie Musicale',URL_MAIN +  basePath + '?genrelist[]=8'] )
    liste.append( ['Comédie',URL_MAIN +  basePath + '?genrelist[]=9'] )
    liste.append( ['Divers',URL_MAIN +  basePath + '?genrelist[]=10'] )
    liste.append( ['Documentaires',URL_MAIN +  basePath + '?genrelist[]=11'] )
    liste.append( ['Drame',URL_MAIN +  basePath + '?genrelist[]=12'] )
    liste.append( ['Epouvante Horreur',URL_MAIN +  basePath + '?genrelist[]=13'] )
    liste.append( ['Espionnage',URL_MAIN +  basePath + '?genrelist[]=14'] )
    liste.append( ['Famille',URL_MAIN +  basePath + '?genrelist[]=15'] )
    liste.append( ['Fantastique',URL_MAIN +  basePath + '?genrelist[]=16'] )
    liste.append( ['Guerre',URL_MAIN +  basePath + '?genrelist[]=17'] )
    liste.append( ['Historique',URL_MAIN +  basePath + '?genrelist[]=18'] )
    liste.append( ['Musical',URL_MAIN +  basePath + '?genrelist[]=19'] )
    liste.append( ['Péplum',URL_MAIN +  basePath + '?genrelist[]=6'] )
    liste.append( ['Policier',URL_MAIN +  basePath + '?genrelist[]=20'] )
    liste.append( ['Romance',URL_MAIN +  basePath + '?genrelist[]=21'] )
    liste.append( ['Science Fiction',URL_MAIN +  basePath + '?genrelist[]=22'] )
    liste.append( ['Thriller',URL_MAIN +  basePath + '?genrelist[]=23'] )
    liste.append( ['Western',URL_MAIN +  basePath + '?genrelist[]=24'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    bGlobal_Search = False
    if sSearch:

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch=sSearch.replace(URL_SEARCH[0],'')

        query_args = ( ( 'do' , 'search' ) , ('subaction' , 'search' ) , ('story' , sSearch ) , ('titleonly' , '3' ))
        data = urllib.urlencode(query_args)
        request = urllib2.Request(URL_SEARCH[0],data,headers)
        sPattern = '<div style="height:[0-9]{3}px;"> *<a href="([^"]+)" *><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<div class="[^"]+?" style="[^"]+?"> *<a href="[^"]+?" *> ([^<]+?)<'

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        request = urllib2.Request(sUrl,None,headers)
        sPattern = '<div style="height:[0-9]{3}px;"> *<a href="([^"]+)"><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<div class="[^"]+?" style="[^"]+?"> *<a href="[^"]+?"> ([^<]+?)<'

    reponse = urllib2.urlopen(request)
    sHtmlContent = reponse.read()
    #xbmc.log(sHtmlContent)
    reponse.close()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            sTitle = str(aEntry[2])
            sUrl2 = aEntry[0]

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch,sTitle) == 0:
                    continue

            if 'http' in aEntry[1]:
                sThumbnail=aEntry[1]
            else:
                sThumbnail=URL_MAIN+aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            if '-series' in sUrl2 or '-animes' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)



        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="navigation" align="center" >.+?<a href="([^"]+)">Suivant</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        #print aResult
        return aResult[1][0]

    return False


def showMoviesLinks():
    #xbmc.log('mode film')

    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sUrl

    oParser = cParser()

    sCom=''
    #Affichage du menu
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]' + 'Qualités disponibles pour ce film :' + '[/COLOR]')

    #on recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?"> *Qualité (.+?)<\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]

        sTitle = sMovieTitle + ' [COLOR skyblue]' + sQual + '[/COLOR]'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
        oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' [COLOR skyblue]' + aEntry[1] + aEntry[2] + '[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN[:-1] + aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeriesLinks():
    #xbmc.log('mode serie')

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #cConfig().log(sUrl)

    oParser = cParser()

    #Mise àjour du titre
    sPattern = 'content="Telecharger (.+?)Qualité [^\|]+?\| [^\|]+?\| (.+?)       la serie'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        sMovieTitle = aResult[1][0][0]+aResult[1][0][1]

    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    #on recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0]

    sDisplayTitle = cUtil().DecoTitle(sMovieTitle) + ' [COLOR skyblue]' + sQual + '[/COLOR]'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    #sPattern1 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<'
    sPattern1 = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)
    #print aResult1

    if (aResult1[0] == True):
        total = len(aResult1[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult1[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sDisplayTitle = cUtil().DecoTitle(sMovieTitle) + ' [COLOR skyblue]' + aEntry[1] + aEntry[2] + '[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'telecharger-series' + aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    #on regarde si dispo d'autres saisons
    sHtmlContent2 = CutSais(sHtmlContent)
    #sPattern2 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<'
    sPattern2 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)<\/span><span style="color:#.{6}">([^<]+)<\/b><\/span>'

    aResult2 = oParser.parse(sHtmlContent2, sPattern2)
    #print aResult2

    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Autres Saisons disponibles pour cette série :[/COLOR]')

        for aEntry in aResult2[1]:

            sTitle = '[COLOR skyblue]' + aEntry[1] + aEntry[2] + aEntry[3] + aEntry[4] + '[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'telecharger-series' + aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumbnail, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():# recherche et affiche les hotes
    #xbmc.log('showHosters')

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    #xbmc.log(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #Fonction pour recuperer uniquement les liens
    #sHtmlContent = Cutlink(sHtmlContent)

    #Si ca ressemble aux lien premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        oParser = cParser()
        sPattern = '<font color=red>([^<]+?)</font>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)
        #print sHtmlContent
    oParser = cParser()

    sPattern = '<font color=red>([^<]+?)</font>|<div style="font-weight:bold;[^"]+?">([^>]+?)</div></b><b><a target="_blank" href="([^<>"]+?)">Télécharger<\/a>|>\[(Liens Premium) \]<|<span style="color:#FF0000">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #xbmc.log(str(aResult))
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                if ('Interchangeables' not in aEntry[0]):
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            #elif aEntry[1]:
                #oOutputParameterHandler = cOutputParameterHandler()
                #oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                #oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                #oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                #if 'Télécharger' in aEntry[1]:
                    #oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[1])+'[/COLOR]')
                #else:
                    #oGui.addText(SITE_IDENTIFIER, '[COLOR red]'+str(aEntry[1])+'[/COLOR]')

            else:
                sTitle = '[COLOR skyblue]' + aEntry[1] + '[/COLOR] ' + sMovieTitle
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[2])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeriesHosters():# recherche et affiche les hotes
    #xbmc.log('showSeriesHosters')

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Fonction pour recuperer uniquement les liens
    #sHtmlContent = Cutlink(sHtmlContent)

    #Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent or 'premium' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)

    oParser = cParser()

    sPattern = '<div style="font-weight:bold;color:[^"]+?">([^<]+)</div>|<a target="_blank" href="([^"]+?)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            #print aEntry
            if dialog.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                if 'Télécharger' in aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + str(aEntry[0]) + '[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            else:
                sName = aEntry[2]
                sName = sName.replace('Télécharger','')
                sName = sName.replace('pisodes','pisode')

                sTitle = sMovieTitle + ' ' + sName
                sDisplayTitle = cUtil().DecoTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def Display_protected_link():
    #xbmc.log('Display_protected_link')
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()

    #cConfig().log(sUrl)

    #Ne marche pas
    if (False):
        code = {
            '123455600123455602123455610123455615': 'http://uptobox.com/',
            '1234556001234556071234556111234556153': 'http://turbobit.net/',
            '123455600123455605123455615': 'http://ul.to/',
            '123455600123455608123455610123455615': 'http://nitroflare.com/',
            '123455601123455603123455610123455615123455617': 'https://1fichier.com/?',
            '123455600123455606123455611123455615': 'http://rapidgator.net/'
        }

        for k in code:
            match = re.search(k+'(.+)$', sUrl)
            if match:
                sHosterUrl = code[k] + match.group(1)
                sHosterUrl = sHosterUrl.replace('123455615', '/')
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sTitle = sMovieTitle
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                oGui.setEndOfDirectory()
                return

    #Est ce un lien dl-protect ?
    if 'dl-protecte' in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="(.+?)">'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            oDialog = cConfig().createDialogOK('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl])

    #print aResult_dlprotect

    if (aResult_dlprotecte[0]):

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry
            #print sHosterUrl

            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + str(episode)

            episode+=1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()

def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Qualités également disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Saisons également disponibles pour cette saison:</h3>(.+?)<h3>Qualités également disponibles pour cette saison:</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    return ''

def CutNonPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = 'Lien Premium(.+?)Publie le '
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

    #si l'ordre a été chnage ou si il ya un probleme
    if 'dl-protect.com' not in res:
        sPattern = '(?i) par .{1,2}pisode(.+?)$'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            sHtmlContent = aResult[1][0]
    else:
        sHtmlContent = res

    #Si ca marche pas on renvois le code complet
    return sHtmlContent

def DecryptDlProtecte(url):

    cConfig().log('DecryptDlProtecte : ' + url)

    if not (url):
        return ''

    #url=url.replace('https','http')

    headersBase = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Referer' : url ,
    #'Origin' : 'https://www.dl-protecte.com',
    'Accept' : 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
    #'Pragma' : '',
    #'Accept-Charset' : ''
    }
    
    url2 = 'https://www.dl-protecte.org/php/Qaptcha.jquery.php'

    #Make random key
    s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@";
    RandomKey = ''.join(random.choice(s) for i in range(32))

    query_args = ( ( 'action' , 'qaptcha' ) , ('qaptcha_key' , RandomKey ) )
    data = urllib.urlencode(query_args)

    #Creation Header
    headers1 = dict(headersBase)
    headers1.update({'X-Requested-With':'XMLHttpRequest'})
    headers1.update({'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'})

    #Requete
    request = urllib2.Request(url2,data,headers1)
    try:
        reponse = urllib2.urlopen(request,timeout = 5)
    except urllib2.URLError, e:
        cGui().showInfo("Erreur", 'Site Dl-Protecte HS' , 5)
        cConfig().log( e.read() )
        cConfig().log( e.reason )
        return ''
    except urllib2.HTTPError, e:
        cGui().showInfo("Erreur", 'Site Dl-Protecte HS' , 5)
        cConfig().log( e.read() )
        cConfig().log( e.reason )
        return ''
    except timeout:
        cConfig().log('timeout')
        cGui().showInfo("Erreur", 'Site Dl-Protecte HS' , 5)
        return ''

    sHtmlContent = reponse.read()
    
    #cConfig().log( 'result'  + str(sHtmlContent))

    #Recuperatioen et traitement cookies ???
    cookies=reponse.info()['Set-Cookie']
    c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',cookies)
    if not c2:
        cConfig().log( 'Probleme de cookies' )
        return ''
    cookies = ''
    for cook in c2:
        cookies = cookies + cook[0] + '=' + cook[1] + ';'
        
    #cConfig().log( 'Cookie'  + str(cookies))

    reponse.close()

    if not '"error":false' in sHtmlContent:
        cConfig().log( 'Captcha rate' )
        cConfig().log( sHtmlContent )
        return

    #Creation Header
    headers2 = dict(headersBase)

    #tempo pas necessaire
    #cGui().showInfo("Patientez", 'Decodage en cours' , 2)
    #xbmc.sleep(1000)

    #Ancienne methode avec POST
    #query_args = ( ( 'YnJYHKk4xYUUu4uWQdxxuH@JEJ2yrmJS' , '' ) , ('submit' , 'Valider' ) )
    #data = urllib.urlencode(query_args)

    #Nouvelle methode avec multipart
    #multipart_form_data = { RandomKey : '', 'submit' : 'Valider'  }
    
    import string
    _BOUNDARY_CHARS = string.digits + string.ascii_letters
    boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    
    multipart_form_data = { RandomKey : '', 'submit' : 'Valider' }
    data, headersMulti = encode_multipart(multipart_form_data, {},boundary)
    headers2.update(headersMulti)
    #cConfig().log( 'header 2'  + str(headersMulti))
    #cConfig().log( 'data 2'  + str(data))

    #rajout des cookies
    headers2.update({'Cookie': cookies})

    #Modifications
    headers2.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

    #cConfig().log( str(headers2) )

    #Requete
    request = urllib2.Request(url,data,headers2)
    try:
        reponse = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.read()
        print e.reason

    sHtmlContent = reponse.read()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    reponse.close()

    return sHtmlContent

#******************************************************************************
#from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/

"""Encode multipart form data to upload files via POST."""

def encode_multipart(fields, files, boundary=None):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    import mimetypes
    import random
    import string

    _BOUNDARY_CHARS = string.digits + string.ascii_letters

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))
    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)
