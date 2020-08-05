# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 9

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.comaddon import  VSlog

from resources.lib.config import GestionCookie
#[COLOR skyblue]Vkstream[/COLOR]'

bVSlog=True
SITE_IDENTIFIER = 'voirhd_co'
SITE_NAME = 'Voirhd'
SITE_DESC = 'Les Derniers Films et Series en Streaming HD'

URL_MAIN = 'https://voirhd.co/'
MOVIE_MOVIE = (URL_MAIN + 'films-1.html', 'showMovies')  #use -1.html instead of .html 

#add tags in  URL_MAIN (home page site)
tbox='#box'
tmoviestend='#moviestend'
tlastmovie='#lastmovie'
tseriestend='#seriestend'
tlastvf='#lastvf'
tlastvost='#lastvost' 



key_search_movies='#search_movies_#'
key_search_series='#search_series_#'
# globale

URL_SEARCH = (URL_MAIN + 'rechercher-', 'showMovies')
#URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
#URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

URL_SEARCH_MOVIES = (URL_SEARCH[0]+ key_search_movies, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0]+ key_search_series, 'showMovies')


MOVIE_TOP=(URL_MAIN + tbox,'showMovies')
MOVIE_VIEWS=(URL_MAIN + tmoviestend,'showMovies')
MOVIE_NEWS=(URL_MAIN + tlastmovie,'showMovies')

SERIE_VIEWS=(URL_MAIN+ tseriestend , 'showMovies')

#SERIE_NOTES =(URL_MAIN+ tseriestend , 'showMovies')
MOVIE_NOTES =(URL_MAIN+ tseriestend , 'showMovies')

#Tendance Series #tends
#Derniers episodes vf Ajoute #vf
#Derniers episodes VOSTFR Ajoute #vost

SERIE_SERIES = (URL_MAIN + 'serie-1.html', 'showMovies')
#https://voirhd.co/serie


SERIE_NEWS_EPISODE_VF=(URL_MAIN + tlastvf ,'showMovies')
SERIE_NEWS_EPISODE_VOST=(URL_MAIN + tlastvost ,'showMovies')
URL_IMAGE_VF='https://voirhd.co/image/vf.png'
URL_IMAGE_VOST='https://voirhd.co/image/vostfr.png'

FUNCTION_SEARCH = 'showMovies'


#URL_SEARCH_MOVIES = ('', 'showMovies')
#URL_SEARCH_SERIES = ('', 'showMovies')

#movies et series 
MOVIE_GENRES = (True, 'showGenres')
#SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films & Series (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Films ( Box Office )', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films ( Les plus populaires)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries ( Les plus populaires) ','series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODE_VF[1], 'Séries ( Derniers Episodes VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS_EPISODE_VOST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS_EPISODE_VOST[1], 'Séries ( Derniers Episodes VOST)', 'series.png', oOutputParameterHandler)

    
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    #oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    #####
  
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()


def showMoviesMenu():
    oGui = cGui()
   
    oGui.setEndOfDirectory()


def showSeriesMenu():
    oGui = cGui()

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        #showMovies(sSearchText)
        # ne sert car compliqué a refaire
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    # bug sur le site:les options genres ne marchent pas sur le site 
    # le resultat correpondra seulement a la derniere recherche effectuée
    # par exemple recherche 'indien' donnera :un idien ds la ville
    # retour  menu : genre : epouvante-horreur donneras = un indien ds la ville !!!!


    # on fait une recheche par mot clef genre en créant une url bidon pour la recherche
    # car celle ci n'as besoin que de 2 parametres en post avec url='https://voirhd.co/lien.php' 
    # addParameters('Search',search) et des cookies qui peuvent etres factices
    # réels cookies='_ga=GA1.2.15150117.1595311931; PHPSESSID=620726de603749aa430029aab71d2932; _gid=GA1.2.1226256096.1595849685'
    # suffisant cookies='PHPSESSID=1'
    
    # par contre il faut respecter la requete pour les page de resultat
    #https://voirhd.co/recherche-comedie.html ou -1.html
    #https://voirhd.co/recherche-comedie-2.html
    # on na aucun indice sur le next page seulement le max page
    
    liste = []
    
    listegenre=['Action','Animation','aventure','Biopic','Comedie','Comedie-musicale',
                'Documentaire','Drame','Epouvante-horreur','Famille','Fantastique','Guerre',
                'Opera','Policier','Romance','Science-fiction','Thriller']
    
    url1g= URL_MAIN+'recherche-'
    url2g='-0.html'           
    #URL_MAIN+'recherche-'+ mot_saisie_ds_recherche_site + '.html' # 
    
    for igenre in listegenre:
        liste.append([igenre, url1g + igenre + url2g  ])
        #liste.append([igenre, url1g + igenre ])
    
    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

#
def RequestHandlerSearch(searchs):
    oParser = cParser()
    sPattern='voirhd.co.rechercher-([^ ]*)'
    aResult = oParser.parse(searchs, sPattern)

    if (aResult[0] == True):
        ssearch= aResult[1][0]
    else:
        ifVSlog('cannnot parse ')
        ifVSlog('sPattern '+sPattern)
        return False,'none'

    scookies='PHPSESSID=fakecookies'#marche
    scookies='PHPSESSID=620726de603749aa430029aab71d2932'
    scookies='PHPSESSID=1'
    req2 = 'https://voirhd.co/lien.php'

    #req3='https://voirhd.co.bidon/films.html'#marche
    oRequestHandler = cRequestHandler(req2)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('Search',ssearch)
    #oRequestHandler.addHeaderEntry('Referer', req1)
    oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')  # 
    oRequestHandler.addHeaderEntry('Cookie', scookies)
    sHtmlContent = oRequestHandler.request()
    
    if ssearch in sHtmlContent : ##on degrossi en  gros pour eviter de parser des resultats douteux de la page
        return True, sHtmlContent
        #ifVSlog('Find')
    else:
        return False,'none'
    return

def RequestHandlerGenre(searchs):
    
    ifVSlog('#')
    ifVSlog('RequestHandlerGenre ')
    ifVSlog('url' + searchs)
    #search=re.search('recherche-([^-]*)', searchs).group(1)
    oParser = cParser()
    sPattern='recherche-([^-]*)'
    aResult = oParser.parse(searchs, sPattern)

    if (aResult[0] == True):
        ssearch= aResult[1][0]
    else:
        ifVSlog('cannnot parse ')
        ifVSlog('sPattern '+sPattern)
        return False,'none'

    ifVSlog('result parese' + ssearch)
    
    
    scookies='PHPSESSID=620726de603749aa430029aab71d2932'
    scookies='PHPSESSID=1'
    req2 = 'https://voirhd.co/lien.php'
    #req3='https://voirhd.co.bidon/films.html'#marche
    oRequestHandler = cRequestHandler(req2)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('Search',ssearch)
    #oRequestHandler.addHeaderEntry('Referer', req1)
    oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')  # 
    oRequestHandler.addHeaderEntry('Cookie', scookies)
    sHtmlContent = oRequestHandler.request()
    return True, sHtmlContent


def RequestHandlerSearch2(searchs):
    # requete pour recupere les vrais cookie au cas ou
    # voir class GestionCookie() pour sauvegarder
    ifVSlog('#')
    ifVSlog('TestSearch')
    ifVSlog(searchs)
    oParser = cParser()
    sPattern='voirhd.co.rechercher-([^ ]*)'
    aResult = oParser.parse(searchs, sPattern)

    if (aResult[0] == True):
        ssearch= aResult[1][0]
    else:
        ifVSlog('cannnot parse ')
        ifVSlog('sPattern '+sPattern)
        return False,'none'
    
    #req 1 juste pour recupere cookie 
    req1='https://voirhd.co/' # ou autre url valide
    
    #scookies='_ga=GA1.2.15150117.1595311931; PHPSESSID=620726de603749aa430029aab71d2932; _gid=GA1.2.1226256096.1595849685'
    
    scookies=''
    
    ifVSlog('request1 ='+req1)
    oRequestHandler = cRequestHandler(req1)
    oRequestHandler.request()
    sHeader1=oRequestHandler.getResponseHeader()
    #cookies = getcookie(sHeader)
    bfindcookie=False
    cookiesfind=''
    for iheader in sHeader1:
        ifVSlog(str(iheader))
        if iheader == 'set-cookie':
            scook = sHeader1.getheader('set-cookie')               
            #GestionCookie().SaveCookie('voirhd_co', scook)
            ifVSlog('cook = '+scook)
            scook= scook.split(';') 
            scook1= scook[0]
            cookiesfind=scook1
            #ifVSlog('cook1 = '+scook1)
            #scook2 =scook[1]            
            #ifVSlog('cook2 = '+scook2)
            bfindcookie=True
            break  
        
    #ifVSlog('bfind'+str(bfindcookie)) 
    
    if bfindcookie:
        scookies=cookiesfind
    else:
        return False,'none'
        
    req2 = 'https://voirhd.co/lien.php'
    #req3='https://voirhd.co.bidon/films.html'
    oRequestHandler = cRequestHandler(req2)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('Search',ssearch)
    #oRequestHandler.addHeaderEntry('Referer', req1)
    oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')  # 
    oRequestHandler.addHeaderEntry('Cookie', scookies)
    sHtmlContent = oRequestHandler.request()
    
    if ssearch in sHtmlContent : ##on degrossi en  gros pour eviter de parser des resultats douteux de la page
        return True, sHtmlContent
        #ifVSlog('Find')
    else:
        return False,'none'
    return
 
def showMovies(sSearch=''):
    oGui = cGui()
    
    
    #bVSlog('search'+ str(sSearch))
    #oGui.setEndOfDirectory()
    #return
    
    bSearchMovie=False
    bSearchSerie=False
    
    
    if sSearch:
        sUrl = sSearch
        ifVSlog('Control url if key in sSearch :'  +sUrl)
        
        if key_search_movies in sUrl :
            sUrl=str(sUrl).replace( key_search_movies , '')
            #ifVSlog('Globale Search movies:' + sUrl)
            bSearchMovie=True
            
        if key_search_series in sUrl :
            sUrl=str(sUrl).replace( key_search_series , '')
            #ifVSlog('Globale Search serie:' + sUrl)
            bSearchSerie=True
    
        ifVSlog('sSearch='  + sUrl + '; SearchMovie?='+ str(bSearchMovie)+'; SearchSerie?='+ str( bSearchSerie) )
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    #scookies='PHPSESSID=620726de603749aa430029aab71d2932'
    
    #oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')  # 
    #oRequestHandler.addHeaderEntry('Cookie', scookies)
    #oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    #oRequestHandler.addHeaderEntry('Accept', '*/*')
    #oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    #oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')

    sPattern = 'class="short-images-link".+?img src="([^"]+)".+?short-link"><a href="([^"]+)".+?>([^<]+)</a>'
    
    ifVSlog('#')
    ifVSlog('start showMovies () : Url request = '+ sUrl )
    
    #pattern home page #
    if sUrl ==URL_MAIN + tbox : #1 etape
        sPattern='Film Box Office.*?Tendance Films'   
    if sUrl == URL_MAIN + tmoviestend : #1 etape
        sPattern='Tendance Films.+?Dernier Films ajout'
    if sUrl == URL_MAIN + tlastmovie :  #url  thumb title
        sPattern='<li class="TPostMv">.+?ref="([^"]*).+?src="([^"]*).+?alt="([^"]+)'
    if sUrl == URL_MAIN + tseriestend :  #1 etape
        sPattern='Tendance Series.+?start jaded serie'
    if sUrl == URL_MAIN+ tlastvf : #url title ex 'max s1s2'  thumb flag https://voirhd.co/image/vf.png
        sPattern='<a  href="([^"]*)".+?<span >([^<]*)<.+?src="image.vf.png'
    if sUrl == URL_MAIN+ tlastvost :
        sPattern='<a  href="([^"]*)".+?<span >([^<]*)<.+?src="image.vostfr.png'
    
    if  URL_MAIN +'films' in sUrl :
        # url quality  lang  thumb  title.replace('  ','')
        sPattern='class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?Langhds.([^"]*).+?src="([^"]*).+?alt="([^"]*)'
    if  URL_MAIN +'serie' in sUrl :
        #url   nbredesaison thumb title
        sPattern='class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?src="([^"]*).+?alt="([^"]*)'
    
    if  URL_MAIN +'recherche' in sUrl : #meme que serie mais a tester
        #url   nbredesaison thumb title
        sPattern='class="TPostMv.+?ref="([^"]*).+?Qlty">([^<]*).+?src="([^"]*).+?alt="([^"]*)'
    
    
    #ifVSlog('select 3 choice for html') 
    if sSearch:
        ifVSlog('01 if sSearch') 
    #if  URL_MAIN +'recherche' in sUrl :
        sbool,sHtmlContent=RequestHandlerSearch(sUrl)
        if sbool==False:
            ifVSlog('error sSearch')
            oGui.setEndOfDirectory()
            return
    
    elif URL_MAIN +'recherche' in sUrl : # 1 seule recherche pour genre if  genre-0.html 
        
        surl=str(sUrl).replace('.html', '')
        snumber = re.search('([0-9]+)$',surl).group(1)
        
        ifVSlog('snumber '+snumber )
        if snumber =='0' :
            ifVSlog('02 if recherhe in url and snum=0') 
            ifVSlog('snumber '+snumber )
            sbool,sHtmlContent=RequestHandlerGenre(sUrl)
            
            sUrl=surl.replace('0', '1.html') # genre-0.html / genre-1.html l : same result req need for next page
            ifVSlog(sUrl)
        else:
            ifVSlog('03 if recherhe in url and snum!=0') 
            ifVSlog(sUrl)
            oRequestHandler = cRequestHandler(sUrl)
            #oParser = cParser()
            sHtmlContent = oRequestHandler.request()
              
    else:
        ifVSlog('04 else') 
        oRequestHandler = cRequestHandler(sUrl)
        #oParser = cParser()
        sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        
        ifVSlog('')
        ifVSlog('Failed Pattern with url = '+sUrl )
        ifVSlog(sPattern )

    if (aResult[0] == True):
        total = len(aResult[1])
       

        for aEntry in aResult[1]:
            
            sQual=''
            sLang=''
            # a enlever
            sUrl2=''
            sTitle ='' 
            sThumb ='' 
 
            #parse home page 
            if sUrl == URL_MAIN + tbox  or sUrl == URL_MAIN + tmoviestend or sUrl == URL_MAIN + tseriestend :
                ifVSlog('Home Page')
                ifVSlog('aEntry = '+ aEntry)
                shtml=str(aEntry)
                #url2 thumb title
                sPattern1='<div class=.item.>.+?ref=.([^"]*).+?src=.([^"]*).+?alt=.([^"]+)' 
                oParser2 = cParser()
                aResult2 = oParser2.parse(shtml,sPattern1 )
                ifVSlog(' result aEntry2  ='+ str(aResult2 ))
                if (aResult2[0] == False):
                    oGui.addText(SITE_IDENTIFIER)
                    ifVSlog('Failed Pattern with url = '+sUrl )
                    ifVSlog(sPattern1 )
                if (aResult2[0] == True):
                    ifVSlog('result'+str(len(aResult2[1])))
                    for aEntry in aResult2[1]:
                        sUrl2=aEntry[0]
                        sThumb =aEntry[1]
                        sTitle =aEntry[2]

                        if sThumb.startswith('poster'):
                            sThumb = URL_MAIN + sThumb
                        ifVSlog('aEntry'+ str(aEntry))
                        ifVSlog('sUrl2 =' +sUrl2)
                        ifVSlog('sThumb =' +sThumb)
                        ifVSlog('sTitle =' + sTitle)
                
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oOutputParameterHandler.addParameter('sLang', sLang)
                        oOutputParameterHandler.addParameter('sQual', sQual)
                        if URL_MAIN +'serie' in sUrl2 :
                            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
                        else:
                            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)
                
                oGui.setEndOfDirectory()
                return       
            
            # else no home page
            if sUrl == URL_MAIN+ tlastmovie :##url  thumb title
                sUrl2=aEntry[0]
                sThumb =aEntry[1]
                sTitle =aEntry[2]
                sdisplayTitle=sTitle
              
            if sUrl == URL_MAIN+ tlastvf :##url title ex 'the lost S1E1'  thumb flag https://voirhd.co/image/vf.png
                sUrl2=aEntry[0]
                sThumb =URL_IMAGE_VF
                sTitle =str(aEntry[1]).replace('  ','') + ' ( VF )'
                sdisplayTitle=sTitle

            if sUrl == URL_MAIN+ tlastvost :
                sUrl2=aEntry[0]
                sThumb =URL_IMAGE_VOST
                sTitle =str(aEntry[1]).replace('  ','') +  ' ( VOST )'
                sdisplayTitle=sTitle

            if  URL_MAIN +'films' in sUrl : # url quality  lang  thumb  title.replace('  ','')
                sUrl2=aEntry[0]
                sTitle = str(aEntry[4]).replace(' ','')
                sThumb = aEntry[3]
                sQual  = aEntry[1]
                sLang= aEntry[2]
                sdisplayTitle=sTitle
            
            if  URL_MAIN +'serie' in sUrl :#url   nbredesaison thumb title
                
                tagsaison=aEntry[1]
                if '1' in tagsaison:
                    tagsaison=tagsaison.replace('Saisons','Saison') 
                    
                sUrl2=aEntry[0]
                sTitle = aEntry[3] 
                sThumb = aEntry[2]
                sdisplayTitle=sTitle + ' [' + tagsaison + ']'
            
            if  URL_MAIN +'recherche' in sUrl :#url   qualit thumb title
                sUrl2=aEntry[0]
                sTitle = aEntry[3]
                sThumb = aEntry[2]
                sdisplayTitle=sTitle +' ['+aEntry[1]+']'
                if 'serie' in sUrl2:
                    sdisplayTitle=sTitle + ' : Serie '+ '['+aEntry[1]+']' 
                else:
                    sdisplayTitle=sTitle + ' : Film '+ '['+aEntry[1]+']' 
                    
            if bSearchMovie :
                if 'serie' in sUrl2 :
                    continue
                else:
                    sdisplayTitle= sdisplayTitle.replace(': Film ', '')
            if bSearchSerie :
                if 'films' in sUrl2 :
                    continue
                else :
                    sdisplayTitle= sdisplayTitle.replace(': Serie ', '')
            ##  
            
            
            
            
            ####

            if sThumb.startswith('poster'):
                sThumb = URL_MAIN + sThumb
        
            ifVSlog('aEntry'+ str(aEntry))
            ifVSlog('sUrl2 =' +sUrl2)
            ifVSlog('sThumb =' +sThumb)
            ifVSlog('sTitle =' + sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sQual', sQual)
            
            if (URL_MAIN +'serie' in sUrl2 ) and sUrl != URL_MAIN+ tlastvf and sUrl != URL_MAIN+ tlastvost:
                ifVSlog('ADDTV; showSaisons' + sUrl2)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sdisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            
            elif sUrl == URL_MAIN+ tlastvf or sUrl == URL_MAIN+ tlastvost :
                ifVSlog('ADDTV ; showLink' + sUrl2)
                oGui.addTV(SITE_IDENTIFIER, 'showLink', sdisplayTitle, 'serie.png', sThumb, '', oOutputParameterHandler)
            else:
                ifVSlog('ADDMOVIE ; showLink' + sUrl2)
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sdisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        
    if not sSearch:   
        
        bNextPage,urlnext,number,numbermax = __checkForNextPage(sHtmlContent,sUrl)
        if (bNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlnext)
          
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + '/'+ numbermax+' >>>[/COLOR]', oOutputParameterHandler)

    
        oGui.setEndOfDirectory()
def __checkForNextPage(sHtmlContent,sUrl):
    
    # difficile de trouver en parsant la page max ,et  l'url next qui changent à chaque 
    # ou qui n'est pas mises en evidence dans la page
    # méthode  bourrin ;
    # on cherche toutes les occurances de page qui index
    # puis on augmente  l'indice de la page
    
    ifVSlog('checkForNextPage')
    ifVSlog(sUrl)
    inumbermax=0
    if  URL_MAIN +'films' in sUrl :    
        sPattern = 'voirhd.co.films-([\d]*).html'#
    elif  URL_MAIN +'serie' in sUrl :
        sPattern = 'voirhd.co.serie-([\d]*).html'   #                                 
    elif  URL_MAIN +'recherche' in sUrl :
        sPattern = 'voirhd.co.recherche-.+?-([^.]*).html' 
        sPattern = 'voirhd.co.recherche-.+?-([\d]*).html' 
    elif '#' in sUrl :
        return False,'none','none','none' #  normal sUrl == URL_MAIN+ #tag pas besoin de page suivante
    else:
        ifVSlog(' select pattern failed ') 
        return False,'none','none','none' 
        
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        ifVSlog('Failed Pattern with url = '+sUrl )
        ifVSlog(sPattern )
        return False,'none','none','none'  
    if (aResult[0] == True):
        ifVSlog('result = '+str(len(aResult[1])))
        ifVSlog('spattern = '+sPattern)
        for aEntry in aResult[1]:
            VSlog(str(aEntry))
            snumber=str(aEntry)
            try:
                intnumber=int(snumber)
                if intnumber>inumbermax:
                    inumbermax=intnumber
            except:
                ifVSlog('error parse to int' + snumber)
                pass  
            #ifVSlog(snumber)  
        snumbermax=str(inumbermax) # ok deja parsé
        ifVSlog('max='+str(inumbermax))        
    
    
    surl=str(sUrl).replace('.html', '')
    snumber = re.search('([0-9]+)$',surl).group(1)   
    ifVSlog('#snumber ='+snumber )
    if snumber !='0' :
        inumber=int(snumber)
        inewnumber=inumber+1
        ifVSlog(' new number '+str(inewnumber))
        if inewnumber>inumbermax:  
            ifVSlog(' newnumber > find max :    newnumber =' +str(inewnumber))
            return False,'none','none','none' 
        snewnumber=str(inewnumber)
        snewnumber_html=snewnumber+'.html'
        sUrlnext=surl.replace(snumber, snewnumber_html) # genre-0.html / genre-1.html l : same result req need for next page
        ifVSlog(' find next url:' +str(sUrlnext))
        
        return True ,sUrlnext, snewnumber,snumbermax
    
    else:
        ifVSlog(' snumber == 0')
        
    
    return False,'none','none','none' 



def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sDesc =''
    sPattern = 'fsynopsis"><p>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = str(aResult[1][0]).replace('  ', '')
    
    # url  saisontitle ex   href="serie+ (-Norsemen-saison-3-1598.html)    (Norsemen saison 3)
    sPattern = 'div class="col-sm-3.+?href="serie([^"]*).+?<div class="serietitre">.*?<span>([^<]*)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        
        for aEntry in reversed(aResult[1]):
            sUrl2 = URL_MAIN+'serie' +aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle )
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'ShowEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #contien num saison

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # url numeroEpisode
    sPattern = 'streaming" href=".([^"]*).*?right"><.span>([^<]*)'
    oParser = cParser()
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
            sTitle = sMovieTitle + ' Episode' +aEntry[1] #saison en odre drecroissant
            
            ifVSlog('ADD episode'+sUrl2 )
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sLang= oInputParameterHandler.getValue('sLang')
    sQual= oInputParameterHandler.getValue('sQual')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    if (sThumb):
        if sThumb==URL_IMAGE_VF or sThumb==URL_IMAGE_VOST:
            try:
                sThumb=URL_MAIN + re.search('class="postere.+?.+?src="([^"]*)',sHtmlContent ).group(1)
            except:
                pass  
    # desc films
    if (not sDesc):
        sPattern = 'fsynopsis"><p>([^<]*)'
        #resources.sites.a_voirhd_co.showLink
        #aResult = oParser.parseSingleResult(sHtmlContent, sPattern)
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = str(aResult[1][0]).replace('  ', '')
            #sDesc = sDesc.replace('#039;', '') # ne marche pas ?
           
          
    sPattern = '<button.+?lectt.+?src="([^"]*)"style="'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        ifVSlog(sHtmlContent)
        ifVSlog('')
        ifVSlog('Failed Pattern with url = '+sUrl )
        ifVSlog(sPattern )
    
    
    if (aResult[0] == True):
        ifVSlog( 'total host'+ str( len(aResult[1]) ) )
        
        for aEntry in aResult[1]:
            ##https:..([^.]*)
            ifVSlog( aEntry  )
            sUrl2 = aEntry.replace('.html.html','.html')
            shosturl=sUrl2.replace('www.','') #https://www.flashx.pw/
            try:#http and hhtps
                
                sHost= re.search('http.*?\/\/([^.]*)', shosturl).group(1)
            except:
                sHost=sUrl2
                pass

            #sHost = aEntry[1].capitalize()
            #sLang = aEntry[2].replace('/images/', '').replace('.png', '')
            #sQual = aEntry[3].replace('(', '').replace(')', '')
            sTitle=sMovieTitle
            if sQual : #or film #always with sLang.
                sTitle = '%s [%s] (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle, sQual, sLang.upper(), sHost)
            else:#serie
                sTitle = '%s  [COLOR coral]%s[/COLOR]' % (sMovieTitle, sHost)
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('refUrl', sUrl)
            oOutputParameterHandler.addParameter('sUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    refUrl = oInputParameterHandler.getValue('refUrl')
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl=sUrl
    
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def ifVSlog(log):
    if bVSlog:
        try:  # si no import VSlog from resources.lib.comaddon
            VSlog(str(log)) 
        except:
            pass


