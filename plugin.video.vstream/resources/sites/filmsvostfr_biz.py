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
import re,urllib,urllib2
 
SITE_IDENTIFIER = 'filmsvostfr_biz'
SITE_NAME = 'Filmsvostfr'
SITE_DESC = 'Films/Série/Animé'
 
URL_MAIN = 'http://www.filmsvostfr.cc/'

MOVIE_MOVIES = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_MOVIES = (URL_MAIN + 'series-en-streaming', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series-en-streaming', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_ANIMS = (URL_MAIN + 'animes-en-streaming', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes-en-streaming', 'showMovies')
ANIM_GENRES = (True, 'showAnimGenres')
  
URL_SEARCH = (URL_MAIN + 'recherche.htm?q=', 'showMovies')
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIES[1], 'Films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovieGenres', 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showMovieGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Aventure',URL_MAIN + '3_1_aventure.html'] )
    liste.append( ['Action',URL_MAIN + '1_1_action.html'] )
    liste.append( ['Comédie',URL_MAIN + '4_1_comedie.html'] )
    liste.append( ['Drame',URL_MAIN + '5_1_drame.html'] )
    liste.append( ['Animation',URL_MAIN + '2_1_animation.html'] )
    liste.append( ['Arts Martiaux',URL_MAIN + '24_1_arts-martiaux.html'] )
    liste.append( ['Thriller',URL_MAIN + '11_1_thriller.html'] )
    liste.append( ['Biopic',URL_MAIN + '13_1_biopic.html'] )
    liste.append( ['Policier',URL_MAIN + '8_1_policier.html'] )
    liste.append( ['Romance',URL_MAIN + '9_1_romance.html'] )
    liste.append( ['Comédie dramatique',URL_MAIN + '22_1_comedie-dramatique.html'] )
    liste.append( ['Documentaire',URL_MAIN + '15_1_documentaire.html'] )
    liste.append( ['Science Fiction',URL_MAIN + '10_1_science-fiction.html'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '6_1_epouvante-horreur.html'] )
    liste.append( ['Western',URL_MAIN + '19_1_western.html'] )
    liste.append( ['Espionnage',URL_MAIN + '12_1_espionnage.html'] )
    liste.append( ['Fantastique',URL_MAIN + '7_1_fantastique.html'] )  
    liste.append( ['Guerre',URL_MAIN + '21_1_guerre.html'] )
    liste.append( ['Historique',URL_MAIN + '23_1_historique.html'] )
    liste.append( ['Musical',URL_MAIN + '16_1_musical.html'] )
    liste.append( ['Divers',URL_MAIN + '14_1_divers.html'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '17_1_comedie_musicale.html'] )
    liste.append( ['Famille',URL_MAIN + '18_1_famille.html'] )
    liste.append( ['Peplum',URL_MAIN + '20_1_peplum.html'] )
    liste.append( ['Erotique',URL_MAIN + '25_1_erotique.html'] )
    liste.append( ['Bollywood',URL_MAIN + '26_1_bollywood.html'] )
    liste.append( ['Opéra',URL_MAIN + '27_1_opera.html'] )
    liste.append( ['Concert',URL_MAIN + '28_1_concert.html'] )
    liste.append( ['Non Classé',URL_MAIN + '26_1_bollywood.html'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Aventure',URL_MAIN + 'series/aventure.html'] )
    liste.append( ['Action',URL_MAIN + 'series/action.html'] )
    liste.append( ['Comédie',URL_MAIN + 'series/comedie.html'] )
    liste.append( ['Drame',URL_MAIN + 'series/drame.html'] )
    liste.append( ['Animation',URL_MAIN + 'series/animation.html'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'series/arts-martiaux.html'] )
    liste.append( ['Thriller',URL_MAIN + 'series/thriller.html'] )
    liste.append( ['Biopic',URL_MAIN + 'series/biopic.html'] )
    liste.append( ['Policier',URL_MAIN + 'series/policier.html'] )
    liste.append( ['Romance',URL_MAIN + 'series/romance.html'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'series/comedie-dramatique.html'] )
    liste.append( ['Documentaire',URL_MAIN + 'series/documentaire.html'] )
    liste.append( ['Science Fiction',URL_MAIN + 'series/science-fiction.html'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'series/epouvante-horreur.html'] )
    liste.append( ['Western',URL_MAIN + 'series/western.html'] )
    liste.append( ['Espionnage',URL_MAIN + 'series/espionnage.html'] )
    liste.append( ['Fantastique',URL_MAIN + 'series/fantastique.html'] )  
    liste.append( ['Guerre',URL_MAIN + 'series/guerre.html'] )
    liste.append( ['Historique',URL_MAIN + 'series/historique.html'] )
    liste.append( ['Musical',URL_MAIN + 'series/musical.html'] )
    liste.append( ['Divers',URL_MAIN + 'series/divers.html'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'series/comedie_musicale.html'] )
    liste.append( ['Famille',URL_MAIN + 'series/famille.html'] )
    
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showAnimGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Aventure',URL_MAIN + 'animes/aventure.html'] )
    liste.append( ['Action',URL_MAIN + 'animes/action.html'] )
    liste.append( ['Comédie',URL_MAIN + 'animes/comedie.html'] )
    liste.append( ['Drame',URL_MAIN + 'animes/drame.html'] )
    liste.append( ['Animation',URL_MAIN + 'animes/animation.html'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'animes/arts-martiaux.html'] )
    liste.append( ['Thriller',URL_MAIN + 'animes/thriller.html'] )
    liste.append( ['Biopic',URL_MAIN + 'animes/biopic.html'] )
    liste.append( ['Policier',URL_MAIN + 'animes/policier.html'] )
    liste.append( ['Romance',URL_MAIN + 'animes/romance.html'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'animes/comedie-dramatique.html'] )
    liste.append( ['Documentaire',URL_MAIN + 'animes/documentaire.html'] )
    liste.append( ['Science Fiction',URL_MAIN + 'animes/science-fiction.html'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'animes/epouvante-horreur.html'] )
    liste.append( ['Western',URL_MAIN + 'animes/western.html'] )
    liste.append( ['Espionnage',URL_MAIN + 'animes/espionnage.html'] )
    liste.append( ['Fantastique',URL_MAIN + 'animes/fantastique.html'] )  
    liste.append( ['Guerre',URL_MAIN + 'animes/guerre.html'] )
    liste.append( ['Historique',URL_MAIN + 'animes/historique.html'] )
    liste.append( ['Musical',URL_MAIN + 'animes/musical.html'] )
    liste.append( ['Divers',URL_MAIN + 'animes/divers.html'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'animes/comedie_musicale.html'] )
    liste.append( ['Famille',URL_MAIN + 'animes/famille.html'] )
    
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'animes_genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:
        sUrl = sSearch
        # UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
                                         
        # oRequestHandler = cRequestHandler(URL_MAIN +'search.php')
        # oRequestHandler.setRequestType(1)
        # oRequestHandler.addHeaderEntry('User-Agent' , UA)
        # oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # oRequestHandler.addHeaderEntry('Accept' , 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        # oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        # oRequestHandler.addHeaderEntry('Referer','http://www.filmsvostfr.co/search.php')
        
        # oRequestHandler.addParameters( 't' , sSearch)
        # oRequestHandler.addParameters( 'R_token' , 'U7OJA8L3qwr9DuqYANPWI9k3hGXqoSTp6DdaUuDi')
        
        # sHtmlContent = oRequestHandler.request()


        # sUrl = 'http://www.filmsvostfr.co/search.php'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'format-video hentry item-video">.+?<img src="(.+?)".+?<a href="([^<>"]+?)".+?<b>(.+?)<\/b>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle)
            try:
                sTitle = sTitle.encode("utf-8")
            except:
                pass

            sUrl = aEntry[1]
            sThumbnail = aEntry[0]
            if not sThumbnail.startswith('http'): 
               sThumbnail = URL_MAIN + sThumbnail

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if '/serie-' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)
            elif '/anime-' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            if '/serie-' in sUrl or  '/anime-' in sUrl:
                sNextPage = __checkForNextPage2(sHtmlContent)
            else:
                sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<>']+?)' rel='nofollow' class=\"last\">suiv »<\/a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]
 
    return False
    
def __checkForNextPage2(sHtmlContent):
    sPattern = "<span class=\"courante\">.+?<a href='(.+?)' rel='nofollow'>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
 
    return False
 
def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    #resume
    sCom= ''
    if '/anime-' in sUrl:
        sPattern = '<span>Synopsis.+?<\/span><span>([^<]+)<\/span><\/p>'
    else:
        sPattern = '<span>Résumé.+?<\/span><span>([^<]+)<\/span><\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sCom = aResult[1][0]

    sPattern = '<span>(.aison *\d+.+?)<\/span>'
    sPattern = sPattern + '|href="([^"]+)">(épisode.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    SaisonNum = '0'
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[0]:
                SaisonNum = oParser.getNumberFromString(aEntry[0])
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]Saison ' + SaisonNum + '[/COLOR]')
            else:
                if 'aison' in sMovieTitle:
                    sTitle = sMovieTitle + aEntry[2]
                else:
                    sTitle = sMovieTitle + ' S' + SaisonNum + aEntry[2]
                    
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                sUrl = 'http://www.filmsvostfr.cc' + aEntry[1]
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('HD streaming', '').replace('télécharger sur ','')
    oParser = cParser()

    sPattern = '<img src="(\/images\/video-coming-soon\.jpg)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        oGui.addText2(SITE_IDENTIFIER,'[COLOR crimson]' + 'Vidéo bientôt disponible' + '[/COLOR]')

    #resume
    sCom= ''
    sPattern = '<span class="synopsis">([^<]+)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sCom = aResult[1][0]

    sPattern = '<a href="([^"]+)" target="filmPlayer" class="ilink sinactive" rel="nofollow" title="([^"]+)">.+?<span class="langue(.+?)"><\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0].replace('p=watchers','p=30').replace('p=16do','p=16').replace('p=the23eo','p=23') #a del si correction sur le site
            sHost = aEntry[1]
            sLang = aEntry[2].replace(' ','')
            #sTitle = ('[COLOR coral]' + '[' + sLang + ']' + '[/COLOR]' + ' ' + sMovieTitle + ' ' + '(' + sHost + ')')
            sTitle = '%s [%s] (%s)' % (sMovieTitle, sLang, sHost)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #evite redirection vers fausse video hs
    if 'filmsvostfr.vip' in sUrl:
        sHost = 'www.filmsvostfr.vip'
    elif 'voirstream.org' in sUrl:
        sHost = 'www.voirstream.org'
    
    if 'filmsvostfr.vip' in sUrl or 'voirstream.org' in sUrl:   
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        headers = {'User-Agent': UA ,
                   'Host' : sHost,
                   'Referer': URL_MAIN ,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-Type': 'text/html; charset=utf-8'}

        request = urllib2.Request(sUrl,None,headers)
        reponse = urllib2.urlopen(request)
        repok = reponse.read()
        reponse.close()

        vUrl = re.search('url=([^"]+)"', repok)
        if vUrl:   
           sHosterUrl = vUrl.group(1)
           if 'uptobox' in sHosterUrl:
               sHosterUrl = re.sub(r'(http://www\.filmsvostfr.+?/uptoboxlink\.php\?link=)', 'http://uptobox.com/' ,sHosterUrl)
           elif '1fichier' in sHosterUrl:
               sHosterUrl = re.sub(r'(http://www\.filmsvostfr.+?/1fichierlink\.php\?link=)', 'https://1fichier.com/?' ,sHosterUrl)

    else:
        sHosterUrl = sUrl

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
         sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
         oHoster.setDisplayName(sDisplayTitle)
         oHoster.setFileName(sMovieTitle)
         cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    cHosterGui().plusHoster(oGui)

    oGui.setEndOfDirectory()
