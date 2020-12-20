# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 39


from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import cUtil

from resources.lib.util import QuotePlus
from resources.lib.tmdb import cTMDb
import re
import string
import unicodedata


MOVIE_NO_VSTREAM = (True, 'load')

SITE_IDENTIFIER = 'cine974'
SITE_NAME = 'Cine974'
SITE_DESC = 'Voir les meilleurs films en version française'
MOVIE_NO_VSTREAM = (True, 'load')
URL_MAIN = 'https://www.cine974.com/'


type_year ='year'
type_pays ='pays'
type_genre ='genre'
URL_MENU = URL_MAIN + 'recherche/'

MOVIE_MOVIE = (URL_MAIN + 'streaming/', 'showMoviesStream') # video complete: pas re recherche mais menu home

MOVIE_BA = (URL_MAIN + 'bandes-annonces/films/', 'showMoviesBA')
SERIES_BA = (URL_MAIN + 'bandes-annonces/series/', 'showMoviesBA')
#ANIME_BA = (URL_MAIN + 'bandes-annonces/animes/', 'showMovies')  # lien hs
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_PAYS = (True, 'showPays')

URL_SEARCH = (URL_MAIN + 'recherche/?q=', 'showMovies') # films et series
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


MOVIE_SEARCH = (True, 'MyshowSearchMovie')
SERIES_SEARCH = (True, 'MyshowSearchSerie')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Série', 'search.png', oOutputParameterHandler)
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SEARCH[1], 'Recheche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SEARCH[1], 'Recherche Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BA[1], 'Films (B.A)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_BA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_BA[1], 'Séries (B.A)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Videos Complètes)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Années)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Pays)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'ShowMenuTop', 'Films (Top)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'ShowMenuBoxOffice', 'Films (Box Office)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'ShowMenuNetflix', 'Netflix ', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def ShowMenuBoxOffice():


    oGui = cGui()
    listey = ['2019', '2018', '2017','2016',]

    sUrl = URL_MAIN + 'films/boxoffice-par-annee/'
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Box office : Meilleur film de chaque année', 'Films.png', oOutputParameterHandler)

    for y in listey:

        sTitle = 'Box office ' + y.capitalize()
        sUrl = URL_MAIN + 'films/boxoffice/' + y + '/'
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'Films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowMenuTop():
  
    oGui = cGui()
    listey = ['2020', '2019', '2017', '2016', '2015', '2014'
                  , '2010-2019', '2000-2009', '1990-1999', '1980-1989'
                  ]

    sUrl = URL_MAIN + 'films/top/?p=1&nb=100'
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Top 100', 'Films.png', oOutputParameterHandler)

    for y in listey:

        sTitle = 'Top ' + y.capitalize()
        sUrl = URL_MAIN + 'films/top/' + y
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'Films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowMenuNetflix():
    
    #https://www.cine974.com/series/netflix/?tri=annee
    oGui = cGui()
    listegenre = ['annee', 'note', 'titre' ]

    for igenre in listegenre:
        sTitle = 'Série (' + igenre.capitalize() + ')'
        sUrl = URL_MAIN + 'series/netflix/?tri=' + igenre
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series.png', oOutputParameterHandler)

    listegenre = ['date-de-sortie', 'note', 'titre']

    for igenre in listegenre:
        sTitle = 'Films  (' + igenre.capitalize() + ')'
        if 'date-de-sortie' in igenre:
            sTitle = 'Films (Annee)'

        sUrl = URL_MAIN + 'films/netflix/?tri=' + igenre
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText +'&typeQ=serie'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + '&typeQ=film'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + '&typeQ=tout'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showYears():
    oGui = cGui()
    for i in reversed(range(1970, 2021)):
        sYear = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + sYear + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showGenres():

    oGui = cGui()
    list_listgenre = GetShowType(type_genre)

    for liste in list_listgenre:
        url = liste[1]
        sTitle = liste[0] 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', url)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showPays():
    oGui = cGui()

    list_pays = GetShowType(type_pays)

    for liste in list_pays:
        url = liste[1]
        sTitle = liste[0]
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', url)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def GetShowType(type):


    if type == type_genre:
        seltype = 'genre'
        url1 = URL_MAIN + 'films/genre/'
    if type == type_pays:
        seltype  = 'nationalite'
        url1 = URL_MAIN + 'films/nationalite/'

    sPattern = '<a href=".films.' + seltype + '.([^"]+)".+?class="nuage.+?">([^<]+)'

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MENU)
    sHtmlContent = oRequestHandler.request()
    list_short = ['Catastrophe', 'Cinéma de montagne', 'Live-action'] # 1 seul film
    dic_type = {}

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):

        for aEntry in aResult[1]:
            title = aEntry[1].strip()
            if not title or title in list_short:
                continue
            dic_type[title] = url1 + aEntry[0]

    dic_type= sorted(dic_type.items(), key = lambda valuetitle: valuetitle[0])
    return dic_type


def showMoviesBA(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # urlmp4 thumb title url2 date durée
    sPattern = 'movieurl="([^"]+).+?poster="([^"]+).+?title="([^"]+).+?<h4><a href="([^"]+).+?<.h4>([^<]+).+?(\d\d:\d\d)'
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

            sUrlvideo = aEntry[0]
            sThumb =  aEntry[1]
            sTitle = aEntry[2]
            sUrl2 =  aEntry[3]
            sDesc = aEntry[5]

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sDesc = ('[COLOR yellow]%s[/COLOR] %s') % ('Durée : ', sDesc)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sUrlvideo', sUrlvideo)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowDescriptionBA', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'ShowDescriptionBA', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalide, sNextPage, pagination = __checkForNextPage(sHtmlContent, sUrl)
        if (bvalide ):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMoviesBA', '[COLOR teal]' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def ShowDescriptionBA():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sUrlvideo = oInputParameterHandler.getValue('sUrlvideo')
    sTitle = sMovieTitle
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = 'meta\s*itemprop="description.+?content="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]==True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrlvideo)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addLink(SITE_IDENTIFIER, 'showDirect', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesStream(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(' ', '+').replace('%20', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # thumb title url2 genre
    sPattern = '<div class="section_post_left">.+?img src="([^"]+).+?alt="([^"]+).+?<a href="([^"]+).+?class="event_date">([^<]+)'
    
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

            sThumb = aEntry[0]
            sTitle = aEntry[1]
            sUrl2 = aEntry[2]
            sDesc = aEntry[3]

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            
            sDesc= ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Genre :', sDesc)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)


            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showLinksStream', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinksStream', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalide, sNextPage, pagination = __checkForNextPage(sHtmlContent, sUrl)
        if (bvalide ):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMoviesStream', '[COLOR teal]' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showLinksStream():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sPattern = 'class="synopsis">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]
    else:
        sPattern = 'class="synopsis">.+?">([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] and len(aResult[1][0].strip()) > 0:
            sDesc = aResult[1][0]

    if sDesc:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', sDesc)


    sPattern = 'iframe.+?src="([^"]+)" frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl2 = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sUrl2)
        if (oHoster != False):
            sHost = oHoster.getDisplayName()
        else:
            sHost = 'Link'

        sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('siteReferer', sUrl)
        oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):


    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url thumb alt
    #clearfix"> ou clearfix"  > 
    sPattern = '<li class="clearfix".+?<a href="([^"]*)".+?(?:data-original|img src)="([^"]*).+?alt="([^"]*)'
    
    if 'films/boxoffice-par-annee/' in sUrl:
        # thum alt url (autres pattern compatible non bloquant)
        sPattern = '<li class="clearfix">.+?(?:data-original|img src)="([^"]*).+?alt="([^"]*).+?<a href="([^"]*)'

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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            if 'films/boxoffice-par-annee/' in sUrl: #
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
                if '#' in sUrl2:
                    sUrl2 = sUrl2.split('#')[0]

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showLinksMovie', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinksMovie', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bvalide, sNextPage, pagination = __checkForNextPage(sHtmlContent, sUrl)
        if (bvalide ):

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showLinksMovie():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    # Code A Revoir pour trouver liens

    sHtmlContent2 = ''
    sUrl2 = ''

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
 
    sPattern = 'class="synopsis">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]

    if not sDesc:
        #class="synopsis">.+?(?:<\/p><\/p>|<div class="section m_top_50">)
        sPattern = 'class="synopsis">(.+?)(?:<\/p><\/p>|<div class="section m_top_50">)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cleanDesc(aResult[1][0])
        
    if sDesc:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', sDesc)

    valide_url=[] # pour les  mp4 qui se repetent tres souvent mais pas toujours


    sPattern = '\/(\d+)\/$'
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        idvideo= aResult[1][0]
        urlold = '/' + idvideo +'/'
        urlvideo= sUrl.replace(urlold , '/medias' + urlold)
        
    #if urlvideo not in sHtmlContent: # normalement pas vu
            #oGui.addText(SITE_IDENTIFIER, 'le lien video n _existe pas')

    
    
    if urlvideo in sHtmlContent:
        
        
        oRequestHandler = cRequestHandler(urlvideo)
        #movieurl="([^"]+)
        sPattern = 'movieurl="([^"]+)'
        aResult = oParser.parse(sHtmlContent2, sPattern)
       
        if (aResult[0] == True):
            if len(aResult[1][0]) == 1:
                sUrl2 = aResult[1][0]

                bvalid, url = Getidmp4(sUrl2)
                if bvalid:
                    if url not in valide_url: # tjrs vrai c'est le prmier
                        valide_url.append(url)

                        oHoster = cHosterGui().checkHoster(sUrl2)
                        if (oHoster != False):
                            sHost = oHoster.getDisplayName()
                        else:
                            sHost = 'Link '

                        sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost)
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('siteReferer', sUrl)
                        oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

            if len(aResult[1][0]) > 1:

                sPattern = 'movieurl="([^"]+)".+?<div>Bande-annonce([^<]+)'
                aResult2 = oParser.parse(sHtmlContent2, sPattern)
                if (aResult2[0] == True):
                    for aEntry in aResult2[1]:
                        sUrl2 = aEntry[0]

                        slang = aEntry[1].strip()
                        oHoster = cHosterGui().checkHoster(sUrl2)
                        if (oHoster != False):
                            sHost = oHoster.getDisplayName()
                        else:
                            sHost = ' Link'

                        if slang:
                            sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle + ' ' + slang, sHost)
                        else:
                            sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost)

                        bvalid ,url = Getidmp4(sUrl2)
                        if bvalid:
                            if url in valide_url:
                                continue
                            else:
                                valide_url.append(url)


                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('siteReferer', sUrl)
                        oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)
     

    # lien existant mais souvent en double
    sPattern = '<source\s*src="([^"]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sUrl2 = aResult[1][0]
        #oGui.addText(SITE_IDENTIFIER, 'Hoster type mp4 in shtm')
        oHoster = cHosterGui().checkHoster(sUrl2)
        if (oHoster != False):
            sHost = oHoster.getDisplayName()
        else:
            sHost = 'Link'

        sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost)
        
        bvalid, url = Getidmp4(sUrl2)
        if bvalid:
            if url not in valide_url:
                valide_url.append(url)# nesert a rienya pu apres
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('siteReferer', sUrl)
                oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

    #  pas vu de lien url /medias/
    sPattern = 'iframe.+?src="([^"]+)" frameborder'# youtube
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if (aResult[0] == True):

        oGui.addText(SITE_IDENTIFIER, 'Hoster type youtube in shtml ')

        sUrl2 = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sUrl2)
        if (oHoster != False):
            sHost = oHoster.getDisplayName()
        else:
            sHost = 'Link'

        sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('siteReferer', sUrl)
        
        oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

    # url /medias/ # youtube
    if sHtmlContent2:
        sPattern = 'iframe.+?src="([^"]+)" frameborder'
        aResult = oParser.parse(sHtmlContent2, sPattern)

        if (aResult[0] == True):
            
            sUrl2 = aResult[1][0]
            oHoster = cHosterGui().checkHoster(sUrl2)
            if (oHoster != False):
                sHost = oHoster.getDisplayName()
            else:
                sHost = 'Link'

            sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost + ' #1')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteReferer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

    # on a rien on cherche ailleurs
    if  not sUrl2:
        
        metatype = 'movie'
        if '/serie/' in sUrl:
            metatype = 'serie'
        sUrl2 ,sinfo = geturlba(sTitle, metatype)
        
        if  sUrl2:
            oHoster = cHosterGui().checkHoster(sUrl2)
            if (oHoster != False):
                sHost = oHoster.getDisplayName() + sinfo
            else:
                sHost = ' Link' + sinfo

            sDisplayName = '%s  [COLOR coral]%s[/COLOR]' % (sTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteReferer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayName, sThumb, sDesc, oOutputParameterHandler)

        
        else:
            sDisplayTitle =  sTitle + ' [Pas de video]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            #oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteReferer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'showDirect', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def Getidmp4(url):
    oParser = cParser()
    sPattern = '([^\/]+\.mp4)'
    aResult = oParser.parse(url, sPattern)
    if (aResult[0] == True):
        return True, aResult[1][0]

    return False, False

def __checkForNextPage(sHtmlContent, sUrl):

    imax = 0
    nexturl = ''
    numbernext = ''
    numbermax = ''
    pagination = 'Next'
    oParser = cParser()

    if 'p=' in sUrl:  
        sPattern = '(https:.+?p=)'
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            nexturl = aResult[1][0]
    else:
        if 'netflix/?tri' in sUrl:
            nexturl= sUrl + '&p='
        else: # BA - stream - genre année movie
            nexturl= sUrl + '?p='

    sPattern = '(\d+)"><i class="fa fa-angle-right">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        numbernext = aResult[1][0]

    if numbernext and nexturl:
        nexturl = nexturl + numbernext

    sPattern = '\?p=(\d+)' # un peu au pif
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aresult in aResult[1]:
            scurrentmax = aresult
            icurentmax = int(scurrentmax)
            if icurentmax > imax:
                imax = icurentmax
                numbermax = scurrentmax

    if numbernext:
        pagination = 'Page' + numbernext
        if numbermax :
            pagination = pagination + '/' + numbermax

    if nexturl:
        return True, nexturl, pagination

    return False, '', ''


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    siteReferer = oInputParameterHandler.getValue('siteReferer')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', siteReferer)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'url=([^"]+)'
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


def showDirect():
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    siteReferer = oInputParameterHandler.getValue('siteReferer')
    sDesc = oInputParameterHandler.getValue('sDesc')

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def geturlba(title, metatype):

        titleyoutube = title + ' trailer'
        url = ''
        year = ''
        meta = cTMDb().get_meta(metatype, title, year)
        if 'trailer' in meta and meta['trailer']:
            url = meta['trailer']
            if '=' in url:
                id = url.split('=')[1]
                url = 'http://www.youtube.com/watch?v=' + id
                return url, ' #2'
            else:
                url = ''

        if not url:
            requrl = 'https://www.youtube.com/results?q=' + QuotePlus( titleyoutube ) + '&sp=EgIYAQ%253D%253D'
            oRequestHandler = cRequestHandler(requrl)
            sHtmlContent = oRequestHandler.request()

            listResult = re.findall('"url":"\/watch\?v=([^"]+)"', sHtmlContent)
            if listResult: # normalement liens jamais vides
                url = 'http://www.youtube.com/watch?v=' + listResult[0]

            sPattern = '"title":{"runs":\[{"text":"([^"]+).+?"url":"\/watch\?v=([^"]+)' # un peu au pif
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            i = 0
            list_title = []
            list_url = []
            urlyoutube = 'http://www.youtube.com/watch?v='
            if (aResult[0] == False):
                return url, '(pas de video)'

            if (aResult[0] == True):
                for aresult in aResult[1]:
                    list_title.append (aresult[0])
                    list_url.append(urlyoutube + aresult[1])
                    title = aresult[0]
                    url1 = urlyoutube + aresult[1]
                    i = 1 + i
                    if i == 10:
                        break

                return list_url[0], '# Find : ' + list_title[0]

        if not url:# jamais atteint
            return url, '# (pas de video) : '


def cleanDesc(sdesc):

    oParser = cParser()
    sPattern = '(<.+?>)'
    aResult = oParser.parse(sdesc, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sdesc = sdesc.replace(aEntry, '')

    return sdesc
