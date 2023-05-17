# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# S09 update 02/11/2020
return False # 0212020 Site HS depuis plus de 1 moi
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'voirhd_co'
SITE_NAME = 'Voir HD'
SITE_DESC = 'Films et Series en streaming hd'

URL_MAIN = 'https://voirhd.co/'
MOVIE_MOVIE = (URL_MAIN + 'films-1.html', 'showMovies')  # use -1.html instead of .html

# add tags in URL_MAIN       : Home page site :
tbox = '#box'                # Film Box Office
tmoviestend = '#moviestend'  # Tendance Films
tlastmovie = '#lastmovie'    # Dernier Films ajoutés
tseriestend = '#seriestend'  # Tendance Series
tlastvf = '#lastvf'          # Derniers episodes vf Ajouté # épisode pas de desc : normal
tlastvost = '#lastvost'      # Derniers episodes VOSTFR Ajoute  #
# recherche : key pour différencier le type de recherche
key_search_movies = '#search_movies_#'
key_search_series = '#search_series_#'
# recherche globale
URL_SEARCH = (URL_MAIN + 'rechercher-', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + key_search_series, 'showMovies')
# recherche interne
MY_SEARCH_MOVIES = (True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = (True, 'MyshowSearchSerie')
# genre : movies et series (pas de difference) on indique film ou serie dans le resultat
MOVIE_GENRES = (True, 'showGenres')

MOVIE_TOP = (URL_MAIN + tbox, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + tmoviestend, 'showMovies')
MOVIE_NEWS = (URL_MAIN + tlastmovie, 'showMovies')

SERIE_VIEWS = (URL_MAIN + tseriestend, 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie-1.html', 'showMovies')  # or https://voirhd.co/serie
SERIE_NEWS_EPISODE_VF = (URL_MAIN + tlastvf, 'showMovies')
SERIE_NEWS_EPISODE_VOST = (URL_MAIN + tlastvost, 'showMovies')

URL_IMAGE_VF = 'https://voirhd.co/image/vf.png'
URL_IMAGE_VOST = 'https://voirhd.co/image/vostfr.png'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Series (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesMenu', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesMenu', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesMenu():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Films (Box Office)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus populaires)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesMenu():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus populaires)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODE_VF[1], 'Séries (Derniers Episodes VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODE_VOST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODE_VOST[1], 'Séries (Derniers Episodes VOST)', 'series.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        # sSearchText.replace(' ', '-') recherche plus précise mais plus risquée
        sUrl = URL_SEARCH[0] + key_search_series + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    # bug sur le site:les options genres ne marchent pas
    # on fait une recheche par mot clef genre  pour la recherche
    # URL_MAIN+'recherche-'+ mot_saisie_ds_recherche_site + '-0.html'
    # ** url2g :'-0' pour valider la premiere requete  RequestHandlerGenre
    # result RequestHandlerGenre : '-1' neccessaire apres pour le next page

    liste = []
    listegenre = ['Action', 'Animation', 'aventure', 'Biopic', 'Comedie', 'Comedie-musicale',
                  'Documentaire', 'Drame', 'Epouvante-horreur', 'Famille', 'Fantastique', 'Guerre',
                  'Policier', 'Romance', 'Science-fiction', 'Thriller']

    url1g = URL_MAIN + 'recherche-'
    url2g = '-0.html'  # **

    for igenre in listegenre:
        liste.append([igenre, url1g + igenre + url2g])

    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def RequestHandlerSearch(searchs):
    oParser = cParser()
    sPattern = 'voirhd.co.rechercher-([^ ]*)'
    aResult = oParser.parse(searchs, sPattern)
    sHtmlContent = ''
    if aResult[0]:
        ssearch= aResult[1][0]
    else:
        return False, sHtmlContent, 'Erreur'

    sCookies = 'PHPSESSID=1'
    req2 = 'https://voirhd.co/lien.php'
    oRequestHandler = cRequestHandler(req2)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('Search', ssearch)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Cookie', sCookies)
    sHtmlContent = oRequestHandler.request()

    if not sHtmlContent:
        return False, sHtmlContent, 'Erreur de requete'

    if ssearch in sHtmlContent:  # on degrossi en  gros pour eviter de parser des resultats
        return True, sHtmlContent, ' Requete ok'
    else:
        return False, sHtmlContent, 'Recherche : Aucun resultat'


def RequestHandlerGenre(searchs):

    oParser = cParser()
    sPattern = 'recherche-([^-]*)'
    aResult = oParser.parse(searchs, sPattern)

    if aResult[0]:
        ssearch = aResult[1][0]
    else:
        return False, 'none'

    sCookies = 'PHPSESSID=1'
    req2 = 'https://voirhd.co/lien.php'
    oRequestHandler = cRequestHandler(req2)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('Search', ssearch)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Cookie', sCookies)
    sHtmlContent = oRequestHandler.request()
    return True, sHtmlContent


def showMovies(sSearch=''):
    oGui = cGui()

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        sUrl = sSearch
        if key_search_movies in sUrl:
            sUrl = str(sUrl).replace(key_search_movies, '')
            bSearchMovie = True

        if key_search_series in sUrl:
            sUrl = str(sUrl).replace(key_search_series, '')
            bSearchSerie = True
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    sPattern = 'class="short-images-link".+?img src="([^"]+)".+?short-link"><a href="([^"]+)".+?>([^<]+)</a>'
    # pattern home page
    # 2 etapes /ou utiliser s=s[s.find(sStart):s.find(sEnd))
    if sUrl == URL_MAIN + tbox:  # etape 1/2
        sPattern = 'Film Box Office.*?Tendance Films'  # < 5ms regex101
    if sUrl == URL_MAIN + tmoviestend:  # etape 1/2
        sPattern = 'Tendance Films.+?Dernier Films ajout'
    if sUrl == URL_MAIN + tseriestend:  # etape 1/2
        sPattern = 'Tendance Series.+?start jaded serie'
    # normale ; 1 etape
    if sUrl == URL_MAIN + tlastmovie:  # url  thumb title
        sPattern = '<li class="TPostMv">.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]+)'
    if sUrl == URL_MAIN + tlastvf:  # url title ex 'max s1s2'  thumb flag https://voirhd.co/image/vf.png
        sPattern = '<a  href="([^"]*)".+?<span >([^<]*)<.+?src="image.vf.png'
    if sUrl == URL_MAIN + tlastvost:
        sPattern = '<a  href="([^"]*)".+?<span >([^<]*)<.+?src="image.vostfr.png'
    # else home page
    if URL_MAIN + 'films' in sUrl:
        # url quality  lang  thumb  title.replace('  ', '')
        sPattern = 'class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?Langhds.([^"]*).+?src="([^"]*).+?alt="([^"]*)'
    if URL_MAIN + 'serie' in sUrl:
        # url   nbredesaison thumb title
        sPattern = 'class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?src="([^"]*).+?alt="([^"]*)'
    if URL_MAIN + 'recherche' in sUrl:  # meme que serie mais a tester
        # url   nbredesaison thumb title
        sPattern = 'class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?src="([^"]*).+?alt="([^"]*)'

    if sSearch:
        sbool, sHtmlContent, mes = RequestHandlerSearch(sUrl)
        if sbool == False:
            oGui.addText(SITE_IDENTIFIER, mes)
            return

    elif URL_MAIN + 'recherche' in sUrl:  # 1 seule RequestHandlerGenre() if  genre-0.html
        surl = str(sUrl).replace('.html', '')
        snumber = re.search('([0-9]+)$', surl).group(1)
        if snumber == '0':
            sbool, sHtmlContent = RequestHandlerGenre(sUrl)
            sUrl = surl.replace('0', '1.html')  # genre-0.html / genre-1.html l : '-1' need for next page
        else:
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        if (URL_MAIN + 'rechercher' in sUrl) and '<div class="divrecher">' in sHtmlContent:
            oGui.addText(SITE_IDENTIFIER, 'Recherche : Aucun resultat')
        # erreur interne qui peu etre cause par mauvais liens du site mais aussi le programme
        elif '<title>404 Not Found</title>' in sHtmlContent:
            oGui.addText(SITE_IDENTIFIER, ' request failed : ')
        else:
            oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_1 = progress().VScreate(SITE_NAME)
        bclosedprogress_1 = False

        for aEntry in aResult[1]:
            progress_1.VSupdate(progress_1, total)
            if progress_1.iscanceled():
                break

            sQual = ''
            sLang = ''
            sUrl2 = ''
            sTitle = ''
            sThumb = ''
            # parse home page
            # etape 2/2
            if sUrl == URL_MAIN + tbox or sUrl == URL_MAIN + tmoviestend or sUrl == URL_MAIN + tseriestend:
                progress_1.VSclose(progress_1)
                bclosedprogress_1 = True
                shtml = str(aEntry)
                sPattern1 = '<div class=.item.>.+?ref=.([^"]*).+?src=.([^"]*).+?alt=.([^"]+)'  # url2 thumb title
                oParser2 = cParser()
                aResult2 = oParser2.parse(shtml, sPattern1)
                if (aResult2[0] == False):
                    oGui.addText(SITE_IDENTIFIER)

                if (aResult2[0] == True):
                    total = len(aResult2[1])
                    progress_2 = progress().VScreate(SITE_NAME)

                    for aEntry in aResult2[1]:
                        progress_2.VSupdate(progress_2, total)
                        if progress_2.iscanceled():
                            break

                        sUrl2 = aEntry[0]
                        sThumb = aEntry[1]
                        sTitle = aEntry[2]
                        if sThumb.startswith('poster'):
                            sThumb = URL_MAIN + sThumb

                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('sLang', sLang)
                        oOutputParameterHandler.addParameter('sQual', sQual)
                        if URL_MAIN + 'serie' in sUrl2:
                            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
                        else:
                            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

                    progress_2.VSclose(progress_2)

                oGui.setEndOfDirectory()
                return

            if sUrl == URL_MAIN + tlastmovie:  # url  thumb title
                sUrl2 = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sDisplayTitle = sTitle

            if sUrl == URL_MAIN + tlastvf:  # url title ex 'the lost S1E1'  thumb flag https://voirhd.co/image/vf.png
                sUrl2 = aEntry[0]
                sThumb = URL_IMAGE_VF
                sTitle = str(aEntry[1]).replace('  ', '') + ' (VF)'
                sDisplayTitle = sTitle

            if sUrl == URL_MAIN + tlastvost:
                sUrl2 = aEntry[0]
                sThumb = URL_IMAGE_VOST
                sTitle = str(aEntry[1]).replace('  ', '') + ' (VOST)'
                sDisplayTitle = sTitle

            # else no home page
            if URL_MAIN + 'films' in sUrl:  # url quality  lang  thumb  title.replace('  ', '')
                sUrl2 = aEntry[0]
                sTitle = str(aEntry[4]).replace('  ', '')
                sThumb = aEntry[3]
                sQual = aEntry[1]
                sLang = aEntry[2]
                sDisplayTitle = sTitle

            if URL_MAIN + 'serie' in sUrl:  # url   nbredesaison thumb title
                tagsaison = aEntry[1]
                if '1' in tagsaison:
                    tagsaison = tagsaison.replace('Saisons', 'Saison')
                sUrl2 = aEntry[0]
                sTitle = aEntry[3]
                sThumb = aEntry[2]
                sDisplayTitle = sTitle + ' [' + tagsaison + ']'

            if URL_MAIN + 'recherche' in sUrl:  # url   qualit thumb title
                sUrl2 = aEntry[0]
                sTitle = aEntry[3]
                sThumb = aEntry[2]
                # sDisplayTitle = sTitle + ' [' + aEntry[1] + ']' non use
                if 'serie' in sUrl2:
                    sDisplayTitle = sTitle + ' : Serie ' + '[' + aEntry[1] + ']'
                else:
                    sDisplayTitle = sTitle + ' : Film ' + '[' + aEntry[1] + ']'

            if bSearchMovie:
                if 'serie' in sUrl2:
                    continue
                else:
                    sDisplayTitle = sDisplayTitle.replace(': Film ', '')

            if bSearchSerie:
                if 'films' in sUrl2:
                    continue
                else:
                    sDisplayTitle = sDisplayTitle.replace(': Serie ', '')

            sThumb = sThumb.replace(' ','%20')
            if sThumb.startswith('poster'):
                sThumb = URL_MAIN + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sQual', sQual)

            if (URL_MAIN + 'serie' in sUrl2) and sUrl != URL_MAIN + tlastvf and sUrl != URL_MAIN + tlastvost:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif sUrl == URL_MAIN + tlastvf or sUrl == URL_MAIN + tlastvost:
                oGui.addTV(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'serie.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        if not bclosedprogress_1:
            progress_1.VSclose(progress_1)

    if not sSearch:
        bNextPage, urlnext, number, numbermax = __checkForNextPage(sHtmlContent, sUrl)
        if (bNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlnext)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + '/' + numbermax + ' >>>[/COLOR]', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent, sUrl):

    inumbermax = 0
    if URL_MAIN + 'films' in sUrl:
        sPattern = 'voirhd.co.films-([\d]*).html'
    elif URL_MAIN + 'serie' in sUrl:
        sPattern = 'voirhd.co.serie-([\d]*).html'
    elif URL_MAIN + 'recherche' in sUrl:
        sPattern = 'voirhd.co.recherche-.+?-([\d]*).html'
    elif '#' in sUrl:
        return False, 'none', 'none', 'none'  # normal sUrl == URL_MAIN+ #tag pas besoin de page suivante
    else:
        return False, 'none', 'none', 'none'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        return False, 'none', 'none', 'none'
    if aResult[0]:
        for aEntry in aResult[1]:
            snumber = str(aEntry)
            try:
                intnumber = int(snumber)
                if intnumber > inumbermax:
                    inumbermax = intnumber
            except:
                pass
        snumbermax = str(inumbermax)

    surl = str(sUrl).replace('.html', '')
    snumber = re.search('([0-9]+)$', surl).group(1)

    if snumber != '0':
        inumber = int(snumber)
        inewnumber = inumber + 1
        if inewnumber > inumbermax:
            return False, 'none', 'none', 'none'
        snewnumber = str(inewnumber)
        snewnumber_html = snewnumber + '.html'
        sUrlnext = surl.replace(snumber, snewnumber_html)  # genre-0.html / genre-1.html l : same result req need for next page
        return True, sUrlnext, snewnumber, snumbermax

    return False, 'none', 'none', 'none'


def showSaisons():

    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sQual = ''
    sYear = ''
    sDesc, sQual, sYear = GetHtmlInfo(sDesc, sQual, sYear, sHtmlContent)

    # url  saisontitle ex   href="serie + (-Norsemen-saison-3-1598.html)    (Norsemen saison 3)
    sPattern = 'div class="col-sm-3.+?href="serie([^"]*).+?<div class="serietitre">.*?<span>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in reversed(aResult[1]):
            sUrl2 = URL_MAIN + 'serie' + aEntry[0]
            # c'est tjrs le meme titre
            sTitle = aEntry[1]
            sTitleDisplay = sTitle

            if sQual:
                sTitleDisplay = sTitleDisplay + ' [' + sQual + ']'
            if sYear and sYear not in sTitle:  # doublon (2020)
                sTitleDisplay = sTitleDisplay + ' (' + sYear + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle )
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sQual', sQual)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'ShowEpisodes', sTitleDisplay, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sQual = oInputParameterHandler.getValue('sQual')
    sYear = oInputParameterHandler.getValue('sYear')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')  # contient num saison

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # url numeroEpisode
    sPattern = 'streaming" href=".([^"]*).*?right"><.span>([^<]*)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sTitleDisplay = sMovieTitle + ' Episode' + aEntry[1]  # saison en odre drecroissant
            if sQual:
                sTitleDisplay = sTitleDisplay + ' [' + sQual + ']'
            if sYear and sYear not in sMovieTitle:
                sTitleDisplay = sTitleDisplay + ' (' + sYear + ')'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sQual', sQual)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitleDisplay, '', sThumb, sDesc, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showLink():

    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sLang = oInputParameterHandler.getValue('sLang')
    sQual = oInputParameterHandler.getValue('sQual')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if (sThumb):
        if sThumb == URL_IMAGE_VF or sThumb == URL_IMAGE_VOST:
            try:
                sThumb = URL_MAIN + re.search('class="postere.+?.+?src="([^"]*)', sHtmlContent).group(1)
            except:
                pass

    sDesc, sQual, sYear = GetHtmlInfo(sDesc, sQual, sYear, sHtmlContent)

    b_ADD_MENU_VF = True
    b_ADD_MENU_VOSTFR = True
    b_ADD_MENU_DL = True

    iposVF = str(sHtmlContent).find('class="typevf">VF </h3>')
    if iposVF > 0:
        b_ADD_MENU_VF = False

    iposVOSTFR = str(sHtmlContent).find('class="typevf">VOSTFR')
    if iposVOSTFR > 0:
        b_ADD_MENU_VOSTFR = False

    iposDL = str(sHtmlContent).find('liens telechargement</a>')
    if iposDL > 0:
        b_ADD_MENU_DL = False

    sPattern = '<button.+?lectt.+?src="([^"]*)"style="'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        if '<title>404 Not Found</title>' in sHtmlContent:  # erreur interne du site sur lien donnée par hd.co
            oGui.addText(SITE_IDENTIFIER, ' request failed : voirhd.co no update is database')
        elif iposVF == -1 or iposVOSTFR == -1:  # index DL tjrs trouvé
            oGui.addText(SITE_IDENTIFIER, 'Aucun lien trouvé pour ' + sMovieTitle)
        else:
            oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in aResult[1]:
            url = str(aEntry)

            if 'rapidgator.net' in url or 'filerio' in url:  # pas de hoster premium
                continue

            sUrl2 = url.replace('.html.html', '.html')
            shosturl = sUrl2.replace('www.', '')  # https://www.flashx.pw/
            try:  # http and https
                sHost = re.search('http.*?\/\/([^.]*)', shosturl).group(1)
                sHost = sHost.upper()
            except:
                sHost = sUrl2
                pass

            sTitleDisplay = sMovieTitle
            if sQual:
                sTitleDisplay = sTitleDisplay + ' [' + sQual + ']'
            if sLang:
                sTitleDisplay = sTitleDisplay + ' (' + sLang.upper() + ')'
            if sYear and sYear not in sMovieTitle:
                sTitleDisplay = sTitleDisplay + ' (' + sYear + ')'
            sTitleDisplay = '%s  [COLOR coral]%s[/COLOR]' % (sTitleDisplay, sHost)

            iposurl = str(sHtmlContent).find(sUrl2 .replace('.html', ''))
            if iposurl == -1:
                pass
            if not b_ADD_MENU_VF:
                if iposurl > iposVF:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]STREAMING VF : [/COLOR]')
                    b_ADD_MENU_VF = True
            if not b_ADD_MENU_VOSTFR:
                if iposurl > iposVOSTFR:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]STREAMING VOSTFR : [/COLOR]')
                    b_ADD_MENU_VOSTFR = True
            if not b_ADD_MENU_DL:
                if iposurl > iposDL:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR skyblue]LIENS DE TELECHARGEMENT : [/COLOR]')
                    b_ADD_MENU_DL = True

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('refUrl', sUrl)
            oOutputParameterHandler.addParameter('sUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitleDisplay, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sUrl)
    if (oHoster):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)
    # else:
        # oGui.addText(SITE_IDENTIFIER, 'Host inconnu ' + sUrl)
    oGui.setEndOfDirectory()


def GetHtmlInfo(sDesc, sQual, sYear, sHtmlContent):
    oParser = cParser()

    if (not sDesc):
        sDesc = ''  # ne sert a rien ? mais on est sure pas d'erreur return
        sPattern = 'fsynopsis.+?<p>([^<]*)<.p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = str(aResult[1][0]).replace('  ', '')
    if (not sQual):
        sQual = ''
        sPattern = 'finfo-title">Qualité.*?title.+?streaming">([^<]*)<.a'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sQual = str(aResult[1][0])
    if (not sYear):
        sYear = ''
        sPattern = 'Année.+?voirhd.co.recherche-([\d]*)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sYear = str(aResult[1][0])

    return sDesc, sQual, sYear
