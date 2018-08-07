#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, dialog, VSlog, addon

import urllib, re, urllib2
import random

#from resources.lib.dl_deprotect import DecryptDlProtect

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = { 'User-Agent' : UA }

SITE_IDENTIFIER = 'zone_telechargement_ws'
SITE_NAME = '[COLOR violet]Zone-Telechargement[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_HOST = 'https://zone-telechargement1.org/'


def GetURL_MAIN():
    ADDON = addon()
    MemorisedHost = ''
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Sources = oInputParameterHandler.getValue('function')

    # z = oInputParameterHandler.getAllParameter()
    # VSlog(z)

    # quand vstream load tous les sites on passe >> globalSources
    # quand vstream load a partir du menu home on passe >> callplugin
    # quand l'url ne contient pas celle déjà enregistrer dans settings et que c'est pas dlprotect on active.
    if not (Sources == 'callpluging' or Sources == 'globalSources' ) and not ADDON.getSetting('ZT')[6:] in sUrl and not 'dl-protect1.com' in sUrl:
        oRequestHandler = cRequestHandler(URL_HOST)
        sHtmlContent = oRequestHandler.request()
        MemorisedHost = oRequestHandler.getRealUrl()
        ADDON.setSetting('ZT',MemorisedHost)

        VSlog("ZT url  >> " + str(MemorisedHost) + ' sauvgarder >> '+ ADDON.getSetting('ZT'))

        return ADDON.getSetting('ZT')
    else:
        # si pas de zt dans settings on récup l'url une fois dans le site
        if not ADDON.getSetting('ZT') and not (Sources == 'callpluging' or Sources == 'globalSources' ):
            oRequestHandler = cRequestHandler(URL_HOST)
            sHtmlContent = oRequestHandler.request()
            MemorisedHost = oRequestHandler.getRealUrl()
            ADDON.setSetting('ZT',MemorisedHost)

            VSlog("ZT url vide  >> " + str(MemorisedHost) + ' sauvgarder >> '+ ADDON.getSetting('ZT'))

            return ADDON.getSetting('ZT')
        else:
            VSlog("ZT pas besoin d'url")
            return ADDON.getSetting('ZT')

URL_MAIN = GetURL_MAIN()

URL_DECRYPT =  ''

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN  + 'index.php?', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'nouveaute/', 'showMovies') # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies') # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies') # films en 3D
MOVIE_HD = (URL_MAIN + 'films-bluray-hd/', 'showMovies') # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'x265-x264-hdlight/', 'showMovies') # films en x265 et x264
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies') # films VOSTFR
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-4k/', 'showMovies') # films "4k"

MOVIE_GENRES = (URL_MAIN , 'showGenre')

MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies') # dessins animes

SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies') # serie VOSTFR

ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires-gratuit/', 'showMovies') # docs
DOC_DOCS = ('http://', 'load')

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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Blu-rays (720p & 1080p)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films 3D', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (x265 & x264)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films 4k', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANIME[1], 'Dessins Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF (Derniers ajouts)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries VOSTFR (Derniers ajouts)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés VF', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés VOSTFR', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

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

def showGenre():
    oGui = cGui()


    liste = []
    liste.append( ['Action', URL_MAIN + 'genres/action/'] )
    liste.append( ['Animation', URL_MAIN + 'genres/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'genres/martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'genres/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'genres/biographie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'genres/dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'genres/musicale/'] )
    liste.append( ['Comédie', URL_MAIN + 'genres/comedie/'] )
    liste.append( ['Divers', URL_MAIN + 'genres/divers/'] )
    liste.append( ['Documentaires', URL_MAIN + 'genres/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'genres/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'genres/epouvante/'] )
    liste.append( ['Espionnage', URL_MAIN + 'genres/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'genres/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genres/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genres/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'genres/historique/'] )
    liste.append( ['Musical', URL_MAIN + 'genres/musical/'] )
    liste.append( ['Péplum', URL_MAIN + 'genres/peplum/'] )
    liste.append( ['Policier', URL_MAIN + 'genres/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'genres/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genres/science/'] )
    liste.append( ['Thriller', URL_MAIN + 'genres/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genres/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)

        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    Nextpagesearch = oInputParameterHandler.getValue('Nextpagesearch')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bGlobal_Search = False

    if Nextpagesearch:
        sSearch = sUrl

    if sSearch:

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch=sSearch.replace(URL_SEARCH[0],'')

        if Nextpagesearch:
            query_args = (('do', 'search'), ('subaction', 'search') ,('search_start', Nextpagesearch),('story', sSearch) , ('titleonly', '3') )
        else:
            query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '3'))

        #sPattern = '<a href="(.+?)" *><img class=".+?" src="(.+?)".+?\s*<.+?>\s*<div style=".+?">\s*<.+?>\s*<div style=".+?"><div class=".+?">\s*<div class=".+?\s*<a href=".+?" *>(.+?)<'
        sPattern = '<a href="(.+?)" *><img class="mainimg.+?src="(.+?)"(?:.|\s)+?<a href=".+?" *>(.+?)<'

        data = urllib.urlencode(query_args)

        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addParameters('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = oParser.abParse(sHtmlContent,'de la recherche','Nous contacter')

    else:
        #sPattern = '<div style="height:[0-9]{3}px;"> *<a href="([^"]+)"><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<div class="[^"]+?" style="[^"]+?"> *<a href="[^"]+?"> ([^<]+?)<'
        sPattern = '<div style="height:[0-9]{3}px;">\s*<a href="([^"]+)"><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<a href="[^"]+" *>([^<]+)<'
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()


    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[2])
            #on vire le tiret des series
            sTitle = sTitle.replace(' - Saison', ' Saison')
            sDisplayTitle = sTitle
            #nettoyage du titre
            sTitle = sTitle.replace('[COMPLETE]', '').replace('[Complete]', '')
            sUrl2 = str(aEntry[0]).replace('https','http')

            #traite les qualités
            liste = ['4k', '1080p', '720p', 'bdrip', 'hdrip', 'dvdrip', 'cam-md']
            for i in liste:
                if i in sUrl2:
                    sDisplayTitle = ('%s [%s]') % (sTitle, i.upper())

            #Si recherche et trop de resultat, on nettoye
            #31/12/17 Ne fonctionne plus ?
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch, sTitle) == 0:
                    continue

            sThumb = str(aEntry[1])
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if 'films-gratuit' in sUrl2 or '4k' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = '<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSearch)
                oOutputParameterHandler.addParameter('Nextpagesearch', aResult[1][0])
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if Nextpagesearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="navigation" align="center" >.+?<a href="([^"]+)">Suivant</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showMoviesLinks():
    #VSlog('mode film')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    #Affichage du menu
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + 'Qualités disponibles pour ce film :' + '[/COLOR]')

    #on recherche d'abord la qualité courante
    sPattern = '<div style=".+?">.+?Qualité (.+?) [|] (.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]
        sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sQual)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN[:-1] + str(aEntry[0])
            sQual = str(aEntry[1])
            sLang = str(aEntry[2])
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeriesLinks():
    #VSlog('mode serie')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Mise àjour du titre
    sPattern = '<meta name="description" content="Telecharger (.+?)Qualité.+?\|[^\|](.+?) Episode .+?\|[^\|](.+?)      la serie'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        sMovieTitle = aResult[1][0][0] + aResult[1][0][1] + aResult[1][0][2]

    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    #on recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0]

    sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual.replace('|',''))

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)
    #print aResult1

    if (aResult1[0] == True):
        total = len(aResult1[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult1[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + 'telecharger-series' + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    #on regarde si dispo d'autres saisons
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)<\/span><span style="color:#.{6}">([^<]+)<\/b><\/span>'

    aResult2 = oParser.parse(sHtmlContent2, sPattern2)
    #print aResult2

    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Autres Saisons disponibles pour cette série :[/COLOR]')

        for aEntry in aResult2[1]:

            sUrl = URL_MAIN + 'telecharger-series' + str(aEntry[0])
            sTitle = '[COLOR skyblue]' + aEntry[1] + aEntry[2] + aEntry[3] + aEntry[4] + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    #VSlog('showHosters')
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n', ''))
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

    sPattern = '<font color=red>([^<]+?)</font>|<div style="font-weight:bold.+?">([^>]+?)</div></b><b><a target="_blank" href="([^<>"]+?)">T.+?charger<\/a>|>\[(Liens Premium) \]<|<span style="color:#FF0000">(.+?)</div></b><b><a target="_blank" href=href="https://([^"]+)/([^"]+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                if ('Interchangeables' not in aEntry[0]):
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            #elif aEntry[1]:
                #oOutputParameterHandler = cOutputParameterHandler()
                #oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                #oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                #oOutputParameterHandler.addParameter('sThumb', str(sThumb))
                #if 'Télécharger' in aEntry[1]:
                    #oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[1])+'[/COLOR]')
                #else:
                    #oGui.addText(SITE_IDENTIFIER, '[COLOR red]'+str(aEntry[1])+'[/COLOR]')

            else:

                sTitle = '[COLOR skyblue]' + aEntry[1] + '[/COLOR] ' + sMovieTitle
                URL_DECRYPT = aEntry[3]
                oOutputParameterHandler = cOutputParameterHandler()
                if sUrl.startswith('http'):
                    oOutputParameterHandler.addParameter('siteUrl', aEntry[2].replace('https','http'))
                else:
                    sUrl2 = 'http://' + str(aEntry[3]) + '/' + str(aEntry[4])
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)

                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeriesHosters():
    #VSlog('showSeriesHosters')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Fonction pour recuperer uniquement les liens
    #sHtmlContent = Cutlink(sHtmlContent)

    #Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent or 'premium' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)


    sPattern = '<div style="font-weight:bold;color:[^"]+?">([^<]+)</div>|<a target="_blank" href="https://([^"]+)/([^"]+?)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                if 'Télécharger' in aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + str(aEntry[0]) + '[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            else:
                sName = str(aEntry[3])
                sName = sName.replace('Télécharger', '')
                sName = sName.replace('pisodes', 'pisode')
                sUrl2 = 'http://' + aEntry[1] +  '/' + aEntry[2]

                sTitle = sMovieTitle + ' ' + sName
                URL_DECRYPT = aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showStreamingHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def Display_protected_link():
    #VSlog('Display_protected_link')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

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
            match = re.search(k + '(.+)$', sUrl)
            if match:
                sHosterUrl = code[k] + match.group(1)
                sHosterUrl = sHosterUrl.replace('123455615', '/')
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                oGui.setEndOfDirectory()
                return

    #Est ce un lien dl-protect ?
    if URL_DECRYPT in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="(.+?)">'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            oDialog = dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    #print aResult_dlprotecte

    if (aResult_dlprotecte[0]):

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry
            #print sHosterUrl

            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + str(episode)


            episode+=1

            if 'stream' in str(sHosterUrl):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showStreamingHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Saisons.+?galement disponibles pour cette saison:</h3>(.+?)<h3>Qualit.+?galement disponibles pour cette saison:</h3>'
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
    sPattern = '(?i) par .{1,2}pisode(.+?)$'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sHtmlContent = aResult[1][0]

    #Si ca marche pas on renvois le code complet
    return sHtmlContent

def DecryptDlProtecte(url):

    VSlog('DecryptDlProtecte : ' + url)
    dialogs = dialog()

    if not (url):
        return ''

    #url=url.replace('https','http')

    headersBase = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Referer' : url,
    #'Origin' : 'https://www.dl-protecte.com',
    'Accept' : 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
    #'Pragma' : '',
    #'Accept-Charset' : ''
    }

    #url2 = 'https://www.dl-protecte.org/php/Qaptcha.jquery.php'
    #url2 = 'https://www.protect-zt.com/php/Qaptcha.jquery.php'
    url2 = 'https://' + url.split('/')[2] + '/php/Qaptcha.jquery.php'

    #VSlog(url2)

    #Make random key
    s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@";
    RandomKey = ''.join(random.choice(s) for i in range(32))

    query_args = ( ('action' , 'qaptcha') , ('qaptcha_key' , RandomKey) )
    data = urllib.urlencode(query_args)

    #Creation Header
    headers1 = dict(headersBase)
    headers1.update({'X-Requested-With':'XMLHttpRequest'})
    headers1.update({'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'})

    #Requete
    request = urllib2.Request(url2, data, headers1)
    try:
        reponse = urllib2.urlopen(request, timeout = 5)
    except urllib2.URLError, e:
        dialogs.VSinfo("Site Dl-Protecte HS", "Erreur", 5)
        VSlog( e.read() )
        VSlog( e.reason )
        return ''
    except urllib2.HTTPError, e:
        dialogs.VSinfo("Site Dl-Protecte HS", "Erreur", 5)
        VSlog( e.read() )
        VSlog( e.reason )
        return ''
    except timeout:
        VSlog('timeout')
        dialogs.VSinfo("Site Dl-Protecte HS", "Erreur", 5)
        return ''

    sHtmlContent = reponse.read()

    #VSlog( 'result'  + str(sHtmlContent))

    #Recuperatioen et traitement cookies ???
    cookies=reponse.info()['Set-Cookie']
    c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);', cookies)
    if not c2:
        VSlog( 'Probleme de cookies')
        return ''
    cookies = ''
    for cook in c2:
        cookies = cookies + cook[0] + '=' + cook[1] + ';'

    #VSlog( 'Cookie'  + str(cookies))

    reponse.close()

    if not '"error":false' in sHtmlContent:
        VSlog('Captcha rate')
        VSlog(sHtmlContent)
        return

    #Creation Header
    headers2 = dict(headersBase)

    #tempo pas necessaire
    #cGui().showInfo("Patientez", 'Décodage en cours', 2)
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
    data, headersMulti = encode_multipart(multipart_form_data, {}, boundary)
    headers2.update(headersMulti)
    #VSlog( 'header 2'  + str(headersMulti))
    #VSlog( 'data 2'  + str(data))

    #rajout des cookies
    headers2.update({'Cookie': cookies})

    #Modifications
    headers2.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

    #VSlog( str(headers2) )

    #Requete
    request = urllib2.Request(url, data, headers2)
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

def encode_multipart(fields, files, boundary = None):
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
