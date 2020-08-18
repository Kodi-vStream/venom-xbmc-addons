# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import string
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress #,VSlog

SITE_IDENTIFIER = 'toro'
SITE_NAME = 'Toro'
SITE_DESC = 'Films et Séries en Streaming'

URL_MAIN = 'https://ww2.torostreaming.com/' #  URL_MAIN = 'https://vf.torostreaming.com/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
key_search_movies ='#searchsomemovies'
key_search_series ='#searchsomeseries'
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')

MOVIE_GENRES = (URL_MAIN + 'genre/', 'showGenres')
SERIE_GENRES = (URL_MAIN + 'genre/', 'showGenres')
# home page
MOVIE_VIEWS=('reqmovies', 'showViews')
SERIE_VIEWS=('reqseries', 'showViews')
#EPISODE_VIEWS = (URL_MAIN, 'showViews')

# recherche variables internes
MY_SEARCH_MOVIES = (True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = (True, 'MyshowSearchSerie')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')

MOVIE_LIST = (True, 'showAlpha')  # voir pour global

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')

# old code ; pas compris; : SERIE_NEWS[0] avec fct showGenres ?
#SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')

# on active/ ou non la recherche des hostes pour l'affichage des noms
# si le hoste n'est pas précisé (serveur)..on en profite pour filtré
# les hosts rejeté par vstream
bFindLinkServer = True

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films & Séries (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Tous les films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les  plus vus)', 'views.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Toutes les séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (les plus vues)', 'views.png', oOutputParameterHandler)

    # old code SERIE_GENRES[1] non mis dans le menu
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Films & Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_series + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + key_search_movies + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    #sPattern = '<li class="cat-item cat-item-.+?href="([^"]+)">([^<]+)</a>([^<]+)<'  # old ne marche plus
    sPattern = 'class="cat-item.+?ref="([^"]*)">([^<]*)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    listalpha = list(string.ascii_lowercase)
    liste = []
    url= URL_MAIN + 'lettre/'

    liste.append(['0-9', URL_MAIN + 'lettre/0-9/'])
    for s in listalpha:
        liste.append([s.upper(), url + s + '/'])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'ShowList', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def ShowList():
    oGui = cGui()
    
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    dic_sdesc = {}
    sPattern ='class="Num">.+?<strong>([^<]+).+?>.+?Dur">([^<]*).+?href=".+?">([^<]*)'  # title durée genre
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sgenre = ''
            sdur = ''
            if aEntry[1]:
                sdur = '\r\n' + '[COLOR skyblue]Durée :[/COLOR] ' + aEntry[1]
            aEntry2 = aEntry[2].replace(' ', '').replace('&amp;', '&').replace('&', ' & ')
            if aEntry2:
                sgenre = '[COLOR skyblue]Genre :[/COLOR] ' + aEntry2
            dic_sdesc[aEntry[0]] =  sgenre + sdur

    #sPattern = 'class="Num">.+?href="([^"]+)".+?src="([^"]+)".+?<strong>([^<]+)<.+?<td>([^<]+)' # old hs
    sPattern = 'class="Num">.+?href="([^"]+)".+?src="([^"]+)".+?<strong>([^<]+).+?>([\d]+)<'  # url thumb title year

    
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\d+', '/w342', aEntry[1])  # meilleur resolution pour les thumbs venant de tmdb
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            sTitle = aEntry[2]
            sYear = aEntry[3]
            s = sTitle
            if 'serie' in sUrl2:
                s = s + ' [Serie] '
            else:
                s = s + ' [Film] '
            sDesc = ''
            if sTitle in dic_sdesc:
                sDesc = dic_sdesc[sTitle]

            sDisplayTitle = s + ' (' + sYear + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if 'series-/' in sUrl2 or '/serie-' in sUrl2 or '/serie/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)  # normal no desc
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        bnextpage, urlnext, pagination = __checkForNextPage(sHtmlContent)
        if (bnextpage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlnext)
            oGui.addNext(SITE_IDENTIFIER, 'ShowList', '[COLOR teal]Page ' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showViews():
    oGui = cGui()

    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    # VSlog(' showViews() '+ sUrl)

    req = URL_MAIN + 'wp-admin/admin-ajax.php'
    pdata = 'action=action_changue_post_by&type=%23Views&posttype='

    if sUrl == 'reqmovies':
        pdata = pdata + 'movies'
    if sUrl == 'reqseries':
        pdata = pdata + 'series'

    oRequestHandler = cRequestHandler(req)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addParametersLine(pdata)
    sHtmlContent = oRequestHandler.request()

    # descriptions écourtées
    dic_sdesc = {}
    sPattern = '<.div>\s*<h2 class="Title">([^<]*).+?class="Descr.+?<p([^<]*)<.p'  # <p([^<]*) / need <p not<p> 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            aentry1 = aEntry[1]
            if 'class=' in aentry1:
                aentry1 = ''
            aentry1 = aentry1.replace('>', '')  # <p'>desc..'
            dic_sdesc[aEntry[0]] = aentry1 + ' ...'

    sPattern = 'class="TPost .+?href="([^"]+)".+?data-src="([^"]+)".+?title">([^<]+).+?Date">([^<]+)' # old pattern changement  year
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
            sThumb = re.sub('/w\d+', '/w342', aEntry[1])  # meilleur resolution pour les thumbs venant de tmdb
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDesc = ''
            if sTitle in dic_sdesc:  # ok python 3,  has_key ko python 3
                sDesc = dic_sdesc[sTitle]

            sDisplayTitle = sTitle + ' (' + sYear + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if '/series/' in sUrl2 or '/serie-' in sUrl2 or '/serie/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
        sUrl = sUrl.replace('%20', '+')  # pas utile
        if key_search_movies in sUrl:
            sUrl = str(sUrl).replace(key_search_movies, '')
            bSearchMovie = True

        if key_search_series in sUrl:
            sUrl = str(sUrl).replace(key_search_series, '')
            bSearchSerie = True

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # descriptions écourtées
    dic_sdesc = {}
    sPattern = '<.div>\s*<h2 class="Title">([^<]*).+?class="Descr.+?<p([^<]*)<.p'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            aentry1 = aEntry[1]
            if 'class=' in aentry1:
                aentry1 = ''
            aentry1 = aentry1.replace('>', '') 
            dic_sdesc[aEntry[0]] = aentry1 + ' ...'

    # url title thumb year
    sPattern = 'class="TPost .+?href="([^"]+)".+?data-src="([^"]+)".+?title">([^<]+).+?Date">([^<]+)'
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
            if bSearchMovie:
                if 'serie' in sUrl2:
                    continue
            if bSearchSerie:
                if not 'serie' in sUrl2:
                    continue
            sThumb = re.sub('/w\d+', '/w342', aEntry[1])  # meilleur resolution pour les thumbs venant de tmdb
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDesc = ''
            if sTitle in dic_sdesc:
                sDesc = dic_sdesc[sTitle]
            s = sTitle
            if 'genre' in sUrl:
                if 'serie' in sUrl2:
                    s = s + ' [Serie] '
                else:
                    s = s + ' [Film] '
                    
            sDisplayTitle = s + ' (' + sYear + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/series/' in sUrl2 or '/serie-' in sUrl2 or '/serie/' in sUrl2:  # or  just 'serie'
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        bnextpage, urlnext, pagination = __checkForNextPage(sHtmlContent)
        if (bnextpage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlnext)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    urlnext = ''
    ipagemax = ''
    ipagenext = ''
    spagination = ''
    bad = 'bad'
    oParser = cParser()
    sPattern = '([^"]*)"><i class="fa-arrow-right'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        urlnext = aResult[1][0]
        try:
            ipagenext = re.search('page/([0-9]+)/', urlnext).group(1)
        except:
            spagination = 'Next '
            return True, urlnext, spagination # on tente comme meme
            pass
    else:
        return False, bad, bad
    if 'class="extend.' in sHtmlContent:
        sPattern = 'class="extend.+?href.+?>([^<]*)'  # case 123...14
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            ipagemax = aResult[1][0]
    else: 
        sPattern = '<a class="page-link.+?page.+?">([\d]+)<.a>\s*<a href="([^"]*)"><i class="fa-arrow-right'  # case 123...14
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            ipagemax = aResult[1][0][0]
    if ipagenext:
        spagination = str(ipagenext)
        if ipagemax:
            spagination = spagination + '/' + str(ipagemax)
    if urlnext:
            return True, urlnext, spagination
    return False, bad, bad


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc= oInputParameterHandler.getValue('sDesc')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    SaveDesc = ''
    if sDesc != False or sDesc != '':
        SaveDesc = sDesc
    sDesc = ''
    sPattern = 'class="Descri.+?<p>([^<]*)<.p'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = aResult[1][0].replace('<br />', ' ')
    else:
        sDesc = SaveDesc

    sPattern = '<div class="Title"><a href="([^"]*).+?Saison.+?>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in reversed(aResult[1]):
            sUrl2 = aEntry[0]
            sSaison = 'Saison ' + aEntry[1]
            sTitle = ("%s %s %s") % (sMovieTitle, ' (' + sYear + ')' , sSaison)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addEpisode(SITE_IDENTIFIER, 'ShowEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    numbersaison = ''
    try:
        numbersaison = re.search('saison.+?([\d]+)', sUrl ).group(1)
    except:
        pass

    if not sDesc:
            sDesc = ''

    # en cas d'erreur on prevoit un deuxieme pattern (meme si pas encore vu d'erreur)
    # numepisode url thumb title
    sPattern = 'class="Viewed">.*?class="Num">([^<]*).+?ref="([^"]*).+?src="([^"]*).*?episode.*?">([^<]*)'  # ok mais rique sipas d'info
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        # oGui.addText(SITE_IDENTIFIER)
        pass

    if (aResult[0] == True):
        savesDesc = sDesc
        for aEntry in aResult[1]:
            snum = aEntry[0]
            sUrl2 =  aEntry[1]
            sThumb = re.sub('/w\d+', '/w342', aEntry[2])  # meilleur resolution pour les thumbs venant de tmdb
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb
            if not 'Épisode' in aEntry[3]:
                sDesc = '[COLOR skyblue]' + 'Episode ' + snum + ' : ' + aEntry[3] + '[/COLOR]'  + '\r\n' + savesDesc
            else:
                sDesc = '[COLOR skyblue]' + aEntry[3].replace('É', 'E' ) + ' : [/COLOR]' + '\r\n' + savesDesc

            sDisplaytitle =  sMovieTitle + ' Saison ' + numbersaison + ' Episode ' + snum + ' (' + sYear + ')'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
        return
    
    sPattern = 'class="Viewed">.*?class="Num">([^<]*).+?ref="([^"]*)'  #numepisode url
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            snum = aEntry[0]
            sUrl2 =  aEntry[1]

            sDisplaytitle =  sMovieTitle + ' Saison ' + numbersaison + ' Episode ' + snum + ' (' + sYear + ')' 

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplaytitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')
    #VSlog('showLinks() url = ' + sUrl)
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    SaveDesc=''
    if sDesc != False or sDesc != '':
        SaveDesc = sDesc
    if '/film/' in sUrl:  # pour les films desc incomplete
        sDesc = ''
        sPattern = 'class="Description"><p>(.+?)</p>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('<br />', ' ')
        else:
            sDesc = SaveDesc

    #  parametres movie et serie pour les deux types de requete
    trtype = '&trtype=1'
    ajaxtyp = '&typ=movie'
    if 'serie' in sUrl:
        trtype = '&trtype=2'
        ajaxtyp = '&typ=episode'

    # des liens DL peuvent se trouver dans le menu reservé aux liens streaming
    # et vice versa
    sPattern = '<li data-typ=".+?data-key="([^"]*).+?data-id="([^"]*).+?AAIco-dns">([^<]*)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    sPattern2 = '<div class="OptionBx on">.+?AAIco-dns">([^<]*).+?ref="([^"]*)'
    oParser2 = cParser()
    aResult2 = oParser2.parse(sHtmlContent, sPattern2)

    total = 0
    bcreatedPogress = False
    if (aResult[0] == True):
        total = len(aResult[1])
    if (aResult2[0] == True):
        total = total + len(aResult2[1])
    if (aResult[0] == False):
        if not 'class="OptionBx' in sHtmlContent:  # on verifie alors si liens stream et en meme temps si liens DL
            oGui.addText(SITE_IDENTIFIER, 'NO LINK : ' + sMovieTitle)
        # else: normal
    if (aResult[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]LIENS STREAMING : [/COLOR]')
        bcreatedPogress = True
        progress_ = progress().VScreate('Update links')
        i = 0
        sHost = ''
        progressmes = ''
        for aEntry in aResult[1]:
            if bcreatedPogress:
                pr= progressmes + ' :  ' + sHost
                progress_.VSupdate(progress_, total, '    ' + pr )
                if progress_.iscanceled():
                    break
            i = i + 1
            sTrembedKey = aEntry[0]
            sId = aEntry[1]
            sHost = aEntry[2]
            if sHost == 'Server' or sHost == '':
                sHost = 'Serveur : ' + str(i)
            # ne donne pas tjrs le vrai lien
            # https://ww2.torostreaming.com/?trembed=0&trid=98210&trtype=2
            sUrl3 = URL_MAIN + '?trembed=' + sTrembedKey + '&trid=' + sId  + trtype

            # il faut faire une requete admin-ajax.php ( 2 requetes ds le hoster)
            # ex post : action=action_player_change&id=40497&key=0&typ=movie
            pData = 'action=action_player_change&id=' + sId  + '&key=' + sTrembedKey + ajaxtyp
            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'

            # bFindLinkServer=True : on veut connaitre les hosts des serveur  inconnus
            if ( 'Serveur' in sHost ) and bFindLinkServer:
                # req1
                oRequestHandler = cRequestHandler(sUrl2)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addParametersLine(pData)
                sHtmlContent2 = oRequestHandler.request()
                sPattern = 'src="([^"]+)"'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if (aResult[0] == True):
                    sUrl3 = aResult[1][0]
                # req2
                bresult, progressmes, sHosterUrl, sHost = FindHost(sUrl3)
                if not bresult:
                    # oGui.addText(SITE_IDENTIFIER, '[COLOR red] link not available : [/COLOR]')
                    # pass
                    continue

                sHost = str(sHost).capitalize()
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

            # on connait le nom du host on se contente de l'afficher  ;(meme si parfois autre)
            # ou si bFindLinkServer= False on se contente des noms que la page veux bien nous fournir
            else:
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('Referer', sUrl)
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('siteUrldefault', sUrl3)
                oOutputParameterHandler.addParameter('pData', pData)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters2', sTitle, sThumb, sDesc, oOutputParameterHandler)


    if (aResult2[0] == False):

        if bcreatedPogress:
            progress_.VSclose(progress_)
        # fonctionnement normal: pas de hoster dl
        # on presume que le mots 'liens' existe uniquement pour le texte lié
        # à la présentation des hosters de telechargement ( pas tjrs vrai )
        if  'liens' in sHtmlContent:
            oGui.addText(SITE_IDENTIFIER)
            #VSlog('error pattern dl') # on a du faire une erreur de pattern
        # VSlog('pas de liens dl')
    if (aResult2[0] == True):
        if not bcreatedPogress:
            progress_ = progress().VScreate(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]LIENS DE TELECHARGEMENT : [/COLOR]')
        i = 0
        for aEntry in aResult2[1]:
            if bcreatedPogress:
                pr = progressmes + ' :  ' + sHost
                progress_.VSupdate(progress_, total, '    ' + pr )
                if progress_.iscanceled():
                    break
            i = i + 1
            sHost = aEntry[0]  # serveur ou nom host
            sUrl2 = aEntry[1]
            if sHost == 'Server' or sHost == '':
                sHost = 'Serveur : ' + str(i)
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            sUrl3 = sUrl2  # pas de  req1 admin-ajax.php (voir cas rare où on a un lien stream : req2 donne t'il alors chaque fois le bon hst ? )

            if ('Serveur' in sHost ) and bFindLinkServer:
                bresult, progressmes, sHosterUrl, sHost = FindHost(sUrl3)
                if not bresult:
                    oGui.addText(SITE_IDENTIFIER, progressmes )  # on met une indication juste pour les dl
                    #pass
                    continue

                sHost=str(sHost).capitalize()
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)
            else:
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('Referer', sUrl)
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('siteUrldefault', sUrl3)
                oOutputParameterHandler.addParameter('pData', pData)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters2', sTitle, sThumb, sDesc, oOutputParameterHandler)

        pr = progressmes + ' : ' + sHost
        progress_.VSupdate(progress_, total , '    ' + pr )
        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHosterUrl = sUrl
    # VSlog('sHosterUrl' + sHosterUrl)
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHosters2():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    siteUrldefault = oInputParameterHandler.getValue('siteUrldefault')
    sUrlReferer = oInputParameterHandler.getValue('Referer')
    pData = oInputParameterHandler.getValue('pData')
    # req1
    if 'admin-ajax.php' in sUrl:  
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParametersLine(pData)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'src="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUrl2 = aResult[1][0]
        else:
            sUrl2 = siteUrldefault  # on échoue, à default on fait une requete qui sera valide vers un host (souvent upbox)
    else:
        #VSlog('no admin-ajax.php siteUrldefault = ' + siteUrldefault)
        sUrl2 = siteUrldefault  #  pour les liens tel siteUrldefault=siteUrl
    
    # req2 :  on recupere en meme temps real url pour les liens DL
    # le fichier sHtmlContent peu etre vide mais pas getrealurl , à reverifier
    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request()
    RealUrl = oRequestHandler.getRealUrl()
    if  not URL_MAIN in RealUrl:
        bvalide , hostname = ValideUrl(RealUrl)
        if not bvalide:
            oGui.addText(SITE_IDENTIFIER,'Security : ' + hostname + ' is disabled')
            oGui.setEndOfDirectory()
            return
        
        oHoster = cHosterGui().checkHoster(RealUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, RealUrl, sThumb)
            oGui.setEndOfDirectory()
            return
    else:
        pass

    if  not sHtmlContent:
        oGui.addText(SITE_IDENTIFIER, 'Toro Link : Blank Page')
        oGui.setEndOfDirectory()
        return
    
    sPattern = 'src="([^"]+)"'  # liens stream
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHosterUrl = aResult[1][0]
        bvalide , hostname = ValideUrl(sHosterUrl)
        if not bvalide:
            oGui.addText(SITE_IDENTIFIER,'Security : ' + hostname + ' is disabled')
            oGui.setEndOfDirectory()
            return
        # VSlog('sHosterUrl' + sHosterUrl)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        # VSlog('echec pattern liens stream')
        pass

    oGui.setEndOfDirectory()


def FindHost(sUrl): #  req2
    mes = ''
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent2 = oRequestHandler.request()
    RealUrl = oRequestHandler.getRealUrl()
    if  not URL_MAIN in RealUrl:
        bvalide, hostname = ValideUrl(RealUrl)
        if not bvalide:
            mes = '[COLOR salmon]Invalide Host[/COLOR]'
            return False, mes, RealUrl, hostname
        mes = ' Valide Host  '
        return True, mes, RealUrl, hostname
    else:
        pass

    if  not sHtmlContent2:
        mes = '[COLOR salmon]Link refer to blank Page [/COLOR]'
        return False, mes, sUrl, sUrl 
    else:
        # liens stream
        sPattern = 'src="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent2, sPattern)
        if (aResult[0] == True):
            sHosterUrl = aResult[1][0]
        else:
            mes = '[COLOR salmon]NO FOUND     [/COLOR] '
            return False, mes ,sUrl ,sUrl
        bvalide , hostname = ValideUrl(sHosterUrl)
        if not bvalide:
            mes ='[COLOR salmon]Invalide Host[/COLOR]'
            return False, mes, sHosterUrl, hostname
        mes = 'Valide Host  '
        return True, mes, sHosterUrl, hostname


def ValideUrl(Url):
    # hosters non securisés rejetés par vstream ...
    list_blackhoster = ['openload', 'streamango', 'verystream']
    sHost = ''
    if 'ok.ru' in Url:
        sHost  = 'ok ru'
        return True, sHost
    if 'embed.mystream' in Url:
        sHost = 'mystream'
        return True, sHost
    try:
        sHost = re.search('http.*?\/\/([^.]*)', Url).group(1)
        sHost = str(sHost).lower()
    except:
        #VSlog('ValideUrl : exception on url : ' + Url)
        return True, Url  # à revoir sinon

    if sHost in list_blackhoster:
        return False, sHost
    return True, sHost
