#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import re,urllib2,urllib

SITE_IDENTIFIER = 'megastream'
SITE_NAME = 'Mega-stream'
SITE_DESC = 'Films, Series, Animes HD'

URL_MAIN = 'http://mega-stream.fr/'

MOVIE_NEWS = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_film=0&tout_les_genres=none', 'showMovies')
MOVIE_MOVIE = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_film=0&tout_les_genres=none', 'showMovies')
MOVIE_HD = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_film=0&tout_les_genres=none&onlyHD=none', 'showMovies')
MOVIE_GENRES = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_film=0&genres[]=' , 'showGenreMovie')

SERIE_SERIES = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_series=0&tout_les_genres=none', 'showMovies')
SERIE_HD = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_series=0&tout_les_genres=none&onlyHD=none', 'showMovies')
SERIE_GENRES = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_series=0&genres[]=', 'showGenreSerie')

ANIM_ANIMS = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_mangas=0&tout_les_genres=none', 'showMovies')
ANIM_HD = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_mangas=0&tout_les_genres=none&onlyHD=none', 'showMovies')
ANIM_GENRES = (URL_MAIN +'fonctions/infinite_scroll.php?count_tiles_mangas=0&genres[]=', 'showGenreAnime')
 
URL_SEARCH = ('', 'resultSearch')
FUNCTION_SEARCH = 'resultSearch'
   
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://mega-stream.fr/fonctions/recherche.php')
    oOutputParameterHandler.addParameter('disp', 'search1')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de Film', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://mega-stream.fr/fonctions/recherche.php')
    oOutputParameterHandler.addParameter('disp', 'search2')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de Serie', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://mega-stream.fr/fonctions/recherche.php')
    oOutputParameterHandler.addParameter('disp', 'search3')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d Animes', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Tous Les Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Series HD', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_HD[0] )
    oGui.addDir(SITE_IDENTIFIER, ANIM_HD[1], 'Animes HD', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animes Genres', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText
        resultSearch(sSearchText)
        oGui.setEndOfDirectory()
        return
       
def showGenreMovie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action', sUrl + '2'] ) 
    liste.append( ['Action HD', sUrl + '2' + '&onlyHD=none'] )   
    liste.append( ['Animation', sUrl + '20'] )
    liste.append( ['Animation HD', sUrl + '20' + '&onlyHD=none'] )
    liste.append( ['Arts Martiaux', sUrl + '22'] )
    liste.append( ['Arts Martiaux HD', sUrl + '22' + '&onlyHD=none'] )
    liste.append( ['Aventure', sUrl + '7'] )
    liste.append( ['Aventure HD', sUrl + '7' + '&onlyHD=none'] )
    liste.append( ['Biopic', sUrl + '10'] )
    liste.append( ['Biopic HD', sUrl + '10' + '&onlyHD=none'] )
    liste.append( ['Comedie', sUrl + '3'] )
    liste.append( ['Comedie HD', sUrl + '3' + '&onlyHD=none'] )
    liste.append( ['Comedie Dramatique', sUrl + '16'] )
    liste.append( ['Comedie Dramatique HD', sUrl + '16' + '&onlyHD=none'] )
    liste.append( ['Comedie Musicale', sUrl + '24'] )
    liste.append( ['Comedie Musicale HD', sUrl + '24' + '&onlyHD=none'] )
    liste.append( ['Documentaire', sUrl + '18'] )
    liste.append( ['Documentaire HD', sUrl + '18' + '&onlyHD=none'] )    
    liste.append( ['Drame', sUrl + '9'] )
    liste.append( ['Drame HD', sUrl + '9' + '&onlyHD=none'] )
    liste.append( ['Epouvante Horreur', sUrl + '14'] )
    liste.append( ['Epouvante Horreur HD', sUrl + '14' + '&onlyHD=none'] )
    liste.append( ['Fantastique', sUrl + '11'] )
    liste.append( ['Fantastique HD', sUrl + '11' + '&onlyHD=none'] )
    liste.append( ['Famille', sUrl + '25'] )
    liste.append( ['Famille HD', sUrl + '25' + '&onlyHD=none'] )
    liste.append( ['Films de Noel', sUrl + '21'] )
    liste.append( ['Films de Noel HD', sUrl + '21' + '&onlyHD=none'] )
    liste.append( ['Guerre', sUrl + '17'] )
    liste.append( ['Guerre HD', sUrl + '17' + '&onlyHD=none'] )
    liste.append( ['Historique', sUrl + '27'] )
    liste.append( ['Historique HD', sUrl + '27' + '&onlyHD=none'] )
    liste.append( ['Horreur', sUrl + '153'] )
    liste.append( ['Horreur HD', sUrl + '153' + '&onlyHD=none'] )    
    liste.append( ['Musical', sUrl + '26'] )
    liste.append( ['Musical HD', sUrl + '26' + '&onlyHD=none'] )
    liste.append( ['Peplum', sUrl + '108'] ) 
    liste.append( ['Peplum HD', sUrl + '108' + '&onlyHD=none'] ) 
    liste.append( ['Policier', sUrl + '12'] )
    liste.append( ['Policier HD', sUrl + '12' + '&onlyHD=none'] )
    liste.append( ['Romance', sUrl + '15'] )
    liste.append( ['Romance HD', sUrl + '15' + '&onlyHD=none'] )
    liste.append( ['Science Fiction', sUrl + '4'] )
    liste.append( ['Science Fiction HD', sUrl + '4' + '&onlyHD=none'] )
    liste.append( ['Spectacles', sUrl + '23'] )
    liste.append( ['Spectacles HD', sUrl + '23' + '&onlyHD=none'] )
    liste.append( ['TV', sUrl + '133'] )
    liste.append( ['TV HD', sUrl + '133' + '&onlyHD=none'] )
    liste.append( ['Thriller', sUrl + '13'] )
    liste.append( ['Thriller HD', sUrl + '13' + '&onlyHD=none'] )
    liste.append( ['Western', sUrl + '19'] )
    liste.append( ['Western HD', sUrl + '19' + '&onlyHD=none'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showGenreSerie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action', sUrl + '2'] )    
    liste.append( ['Animation', sUrl + '20'] )
    liste.append( ['Arts Martiaux', sUrl + '22'] )
    liste.append( ['Aventure', sUrl + '7'] )
    liste.append( ['Biopic', sUrl + '10'] )
    liste.append( ['Biopic-2', sUrl + '113'] )
    liste.append( ['Comedie', sUrl + '3'] )
    liste.append( ['Comedie Dramatique', sUrl + '16'] )
    liste.append( ['Culture', sUrl + '102'] )
    liste.append( ['Dessin', sUrl + '94'] )
    liste.append( ['Divers', sUrl + '145'] )
    liste.append( ['Divertissement', sUrl + '137'] )
    liste.append( ['Documentaire', sUrl + '18'] )
    liste.append( ['Drame', sUrl + '9'] )
    liste.append( ['Epouvante Horreur', sUrl + '14'] )
    liste.append( ['Erotique', sUrl + '110'] )
    liste.append( ['Fantastique', sUrl + '11'] )
    liste.append( ['Famille', sUrl + '25'] )
    liste.append( ['Guerre', sUrl + '17'] )
    liste.append( ['Historique', sUrl + '27'] )
    liste.append( ['Judiciaire', sUrl + '158'] )
    liste.append( ['Medical', sUrl + '44'] )
    liste.append( ['Musical', sUrl + '26'] )
    liste.append( ['Mystere', sUrl + '87'] )
    liste.append( ['Paranormal', sUrl + '91'] )
    liste.append( ['Peplum', sUrl + '108'] ) 
    liste.append( ['Policier', sUrl + '12'] )
    liste.append( ['Romance', sUrl + '15'] )
    liste.append( ['Science Fiction', sUrl + '4'] )
    liste.append( ['Sentai', sUrl + '86'] )
    liste.append( ['Soap', sUrl + '104'] )
    liste.append( ['Spectacles', sUrl + '23'] )
    liste.append( ['Sports', sUrl + '80'] )
    liste.append( ['Tele-realite', sUrl + '57'] )
    liste.append( ['Thriller', sUrl + '13'] )
    liste.append( ['TV', sUrl + '133'] )
    liste.append( ['Western', sUrl + '19'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showGenreAnime():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action', sUrl + '2'] )    
    liste.append( ['Animation', sUrl + '20'] )
    liste.append( ['Arts Martiaux', sUrl + '22'] )
    liste.append( ['Aventure', sUrl + '7'] )
    liste.append( ['Comedie', sUrl + '3'] )
    liste.append( ['Drame', sUrl + '9'] )
    liste.append( ['Epouvante Horreur', sUrl + '14'] )
    liste.append( ['Fantastique', sUrl + '11'] )
    liste.append( ['Historique', sUrl + '27'] )
    liste.append( ['Horreur', sUrl + '153'] )
    liste.append( ['Mythe', sUrl + '82'] )
    liste.append( ['Policier', sUrl + '12'] )
    liste.append( ['Romance', sUrl + '15'] )
    liste.append( ['Science Fiction', sUrl + '4'] )
    liste.append( ['Sports', sUrl + '80'] )
    liste.append( ['Thriller', sUrl + '13'] )
    liste.append( ['Tragedie', sUrl + '155'] )
    
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
    
def resultSearch(sSearch):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
        
    sUrl = "http://mega-stream.fr/fonctions/recherche.php"
    sDisp = oInputParameterHandler.getValue('disp')
    
    #oInputParameterHandler.getAllParameter()

    post_data = {'searchValue' : sSearch,
                'smallSearch': 'false' }

    sMode = ''
    if sDisp == 'search2':
        post_data['cat_recherche'] = 'series'
        sMode = 'serie'
    elif sDisp == 'search3':
        post_data['cat_recherche'] = 'mangas'
        sMode = 'anime'
    else:
        post_data['cat_recherche'] = 'films'
        sMode = 'film'
        
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}
    
    req = urllib2.Request(sUrl , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()
    
    sPattern = 'href="(.+?)" style="background-image: url\((.+?)\);"><p>(.+?)<\/p>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            siteUrl = URL_MAIN + aEntry[0]
            sThumbnail = URL_MAIN + aEntry[1]
            sTitle = aEntry[2]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if sMode == 'serie':
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            elif sMode == 'anime':
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
      

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    #parsing des parametres pour convertir le GET en POST
    try:
        param = dict([item.split('=') for item in (sUrl.split('?')[1]).split('&')])
    except:
        param = {}
        
    #rajout des parametres fixes
    param['catLatBar'] = 'on'
    param['lat_bar_more_filters'] = 'dateSortie'
    
    #recuperation de la valeur filtre par genre ou tout_les_genres
    genre = sUrl.split('&')[1]
    
    #nettoyage url
    sUrl = sUrl.split('?')[0]
    
    #recuperation de la page en cours
    Spage = 0
    if 'count_tiles_film' in param:
        Spage = int(param['count_tiles_film'])
        sNextpage = 'count_tiles_film=' + str(Spage + 20)
    elif 'count_tiles_series' in param:
        Spage = int(param['count_tiles_series'])
        sNextpage = 'count_tiles_series=' + str(Spage + 20)
    elif 'count_tiles_mangas' in param:
        Spage = int(param['count_tiles_mangas'])
        sNextpage = 'count_tiles_mangas=' + str(Spage + 20)

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}

    req = urllib2.Request(sUrl , urllib.urlencode(param), headers)
    
    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()
    
    #fh = open('c:\\vm.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    oParser = cParser()
    
    #sPattern = '<a class="tile_film" href="(.+?)">.+?<img src="(.+?)"\/*>.+?<h3>(.+?)<\/h3><p>.+?<\/p><p>(.+?)<\/p><p class="tile_film_serie_resume">(.+?)<\/p><\/div><div class="bottomRight_ribbon_tile_film"><span id="spanRibbonFilm.+?">(.+?)<\/span><\/div>'
    sPattern = '<a class="tile_film" href="(.+?)">.+?<img src="(.+?)"\/*>.+?<h3>(.+?)<\/h3>.+?<p class="tile_film_serie_resume">(.+?)<.+?<span id="spanRibbonFilm[0-9]+">([^<>]+)*<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #sAnnee = aEntry[3]
            sQual = ''
            if aEntry[4]:
                sQual = aEntry[4]
            sCom = str(aEntry[3])
            sTitle = aEntry[2]+' [COLOR lightblue]' + sQual + '[/COLOR]'
            sThumbnail = URL_MAIN+str(aEntry[1])
            siteUrl = URL_MAIN+str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if 'count_tiles_series' in param:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
            elif 'count_tiles_mangas' in param:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        #Affichage page suivante
        sNextpage = sUrl + '?' + sNextpage + '&' + genre
        if 'onlyHD' in param:
           sNextpage = sNextpage + '&onlyHD=none'
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextpage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = '<p>(SAISON [0-9]+)<\/p>|<p class="episode_saison(?: episode_select)*" id="([0-9]+)">(Episode [0-9]+)<\/p>'
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        
        sSaison = ''
        
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[0]
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[0])+'[/COLOR]')
                
            else:
                sTitle = sMovieTitle + ' '+ sSaison + ' ' + aEntry[2]
                
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sId', aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showSerieHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()

def showSerieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sId = oInputParameterHandler.getValue('sId')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}
    post_data = {'episode_serie' : sId }
                                
    req = urllib2.Request('http://mega-stream.fr/lecteur_serie.php' , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()

    sPattern = 'class="checkShowlistVidQualite"\/>\s+<p>(.+?)<\/p>|<div class="vidQualite vidSelect" id="([0-9]+)">\s+<img class="video_langue_img" src="IMG\/flag\/(.+?).png"\/>\s+<p>(.+?)<\/p>'
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sLang = '[VOSTFR] '
            if 'France' in aEntry[2]:
                sLang = '[VF] '

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sId', str(sId))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[0])+'[/COLOR]')
                
            else:
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                
                sDisplayTitle = sLang + '[COLOR skyblue]' + aEntry[3]+ '[/COLOR] ' + sDisplayTitle
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sId', aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Getlink', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="checkShowlistVidQualite"\/>\s+<p>(.+?)<\/p>|<div class="vidQualite(?: vidSelect)*" id="([0-9]+)">\s+<img class="video_langue_img" src="IMG\/flag\/(.+?).png"\/>\s+<p>(.+?)<\/p>'
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sLang = '[VOSTFR] '
            if 'France' in aEntry[2]:
                sLang = '[VF] '

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+str(aEntry[0])+'[/COLOR]')
                
            else:
                sTitle = sLang + '[COLOR skyblue]' + aEntry[3]+ '[/COLOR] ' + sMovieTitle
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sId', aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'Getlink', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()
    
def Getlink():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sId = oInputParameterHandler.getValue('sId')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}
    
    post_data = {'vid' : sId}
                 
    req = urllib2.Request('http://mega-stream.fr/fonctions/video.php' , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()
    
    oParser = cParser()
    sPattern = 'src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult

    if (aResult[0] == True):
                
            sHosterUrl = str(aResult[1][0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
