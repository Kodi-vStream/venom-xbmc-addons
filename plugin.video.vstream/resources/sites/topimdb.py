#-*- coding: utf-8 -*-
#Venom.
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
import urllib, unicodedata, re
import xbmcgui
import xbmc
#import sqlalchemy
 
try:    import json
except: import simplejson as json
 
SITE_IDENTIFIER = 'topimdb'
SITE_NAME = '[COLOR orange]Top 1000 IMDb[/COLOR]'
SITE_DESC = 'Base de donnÃ©es video.'
 
#doc de l'api http://docs.themoviedb.apiary.io/
 
URL_MAIN = 'http://imdb.com'
 
#API_KEY = '92ab39516970ab9d86396866456ec9b6'
#API_VERS = '3'
#API_URL = URL_MAIN+API_VERS
 
URL_SEARCH = (URL_MAIN + '/search/title?groups=top_1000&sort=user_rating,desc&start=%s', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
 
 
MOVIE_WORLD = (URL_MAIN + '/search/title?groups=top_1000&sort=user_rating,desc&start=1', 'showMovies')
MOVIE_FR = (URL_MAIN + '/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&languages=fr|1&sort=moviemeter,asc&count=50&start=1', 'showMovies')
 
POSTER_URL = 'https://ia.media-imdb.com/images/m/'
#FANART_URL = 'https://image.tmdb.org/t/p/w780/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'
#FANART_URL = 'https://image.tmdb.org/t/p/original/'
               
        #runtime = ''
        #runtime_match = re.search(r'<span class="runtime">(.+?) mins\.</span>', item, flags=(re.DOTALL | re.MULTILINE))
        #if runtime_match:
            #runtime = int(runtime_match.group(1)) * 60
       
 
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
   
#https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6
 
#<views>551,504,503,508,515,50,51,500,550,560,501,572,573,574,570,571,505,511</views>
#viewmode = 500 Film
#viewmode = 503 Film + Information
#viewmode = 50  Liste
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = 'http://imdb.com/search/title?groups=top_1000&sort=user_rating,desc&start=%s'+sSearchText
        #sUrl = 'http://%s.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&languages=fr|1&sort=moviemeter,asc&count=40&start=%s', 'showMovies')
 
        resultSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showPage():
    oGui = cGui()
 
    sSearchNum = oGui.showNumBoard()
   
    if (sSearchNum):
 
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrlbase')
        sMaxPage = oInputParameterHandler.getValue('MaxPage')
       
        sSearchNum = str(sSearchNum)
       
        if int(sSearchNum) > int (sMaxPage):
            sSearchNum = sMaxPage
           
        sUrl = sUrl + str(sSearchNum)
       
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
 
def load():
    oGui = cGui()
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'Top Films Mondial', 'films.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FR[1], 'Top Films Francais', 'films.png', oOutputParameterHandler)
 
 
    oGui.setEndOfDirectory()
 
 
def showMovies(sSearch = ''):
    oGui = cGui()
   
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequestHandler.request()
        #oRequestHandler = cRequestHandler(sUrl)
        #sHtmlContent = oRequestHandler.request()
        #sHtmlContent = sHtmlContent.replace('<span class="runtime">', '').replace('</span>','')
   
    fh = open('c:\\test.txt', "w")
    fh.write(sHtmlContent)
    fh.close()
 
    #sPattern = '<td class="number">(.*?)<\/td>.*?class="image">.*?<a href=".+?" title=".+?"><img src="(.*?)" alt="(.*?)" title=".*?".*?<a href="([^<]+)">.*?<\/a>'
    sPattern = '<span class="lister-item-index unbold text-primary">([^<]+)<\/span> *<a href="([^"]+)">([^<]+)<\/a>.+?src="([^"]+)"'  
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
               
            sTitle = unicode(aEntry[0], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            sTitle = unescape(str(aEntry[2]))
            sTitle = sTitle.encode( "utf-8")
            sNumber = aEntry[0].replace('<td class="number">', '').replace('</td>', '')
            #sRuntime = aEntry[0].replace('<span class="runtime">', '').replace('</span>', '')            
            sTitle = '[COLOR azure]'+sNumber+'[/COLOR] ' + aEntry[2]
            sMovieTitle=re.sub('(\[.*\])','', sTitle)
            sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)
            sTitle2=re.sub('(.*)(\[.*\])','\\1 [COLOR azure]\\2[/COLOR]', sTitle)
           
 
            #sCom = unicode(aEntry[3], 'utf-8')#converti en unicode
            #sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
            #sCom = unescape(sCom)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', ('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[1], '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
     
def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<>"]+?)">Next&nbsp;»<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
 
    return False
 
def showHosters():
 
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
   
    sExtraTitle = ''
    #si c'est une serie
    if sUrl != 'none':
        sExtraTitle = sUrl.split('|')[1]
        sMovieTitle = sUrl.split('|')[0]
     
    #nettoyage du nom pr la recherche
    #print 'avant ' + sMovieTitle
    sMovieTitle = unicode(sMovieTitle, 'utf-8')#converti en unicode pour aider aux convertions
    sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sMovieTitle = sMovieTitle.encode("utf-8").lower() #on repasse en utf-8
   
    sMovieTitle = re.sub('\(.+?\)',' ', sMovieTitle) #vire les tags entre parentheses
   
    #modif venom si le titre comporte un - il doit le chercher
    sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle) #vire les caracteres a la con qui peuvent trainer
   
    sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)',' ', sMovieTitle) #vire les articles
 
    sMovieTitle = re.sub(' +',' ',sMovieTitle) #vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +
    #print 'apres ' + sMovieTitle
 
    dialog3 = xbmcgui.Dialog()
    ret = dialog3.select('Recherche',['V stream','zone_telechargement','film_streaming','kepliz','Movieshd'])
 
    if ret == 0:
        VstreamSearch(sMovieTitle)
    elif ret == 1:
        zone_telechargementSearch(sMovieTitle)
    elif ret == 2:
        film_streamingSearch(sMovieTitle + sExtraTitle)
    elif ret == 3:
        keplizSearch(sMovieTitle + sExtraTitl)
    elif ret == 4:
        movieshdSearch(sMovieTitle + sExtraTitle)
        
def VstreamSearch(sMovieTitle):
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #Type de recherche
    sDisp = oInputParameterHandler.getValue('disp')

    if not(sDisp):
        sDisp = 'search1'
        if sUrl != 'none':
            sDisp = 'search2'
    
    oHandler = cRechercheHandler()
    oHandler.setText(sMovieTitle)
    oHandler.setDisp(sDisp)
    aPlugins = oHandler.getAvailablePlugins()
                
    oGui.setEndOfDirectory()        
 
def zone_telechargementSearch(sMovieTitle):
    oGui = cGui()
   
    exec "from resources.sites import zone_telechargement_com as search"
    sSearchText = oGui.showKeyBoard()
    #title = (_("Enter search criteria")), text = searchTitle, is_dialog=True)
 
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)    
        sUrl = ('(http://www.film-streaming.co/' + sMovieTitle)
        searchUrl = "search.php?movie=", ('resultSearch', sUrl)
    exec "searchUrl"
   
    oGui.setEndOfDirectory()
 
 
def film_streamingSearch(sMovieTitle):
    oGui = cGui()
   
    exec "from resources.sites import film_streaming_co as search"
    #sSearchText = oGui.showKeyBoard()
    #title = (_("Enter search criteria")), text = searchTitle, is_dialog=True)
 
   # if (sSearchText != False):
        #sSearchText = cUtil().urlEncode(sSearchText)    
    sUrl = ('(http://www.film-streaming.co/' + sMovieTitle)
    sUrl = URL_SEARCH[0] + sSearchText
    resultSearch(sUrl)        
    searchUrl = "search.php?movie=", ('resultSearch', sUrl)
    exec "searchUrl"
   
    oGui.setEndOfDirectory()
   
 
 
def keplizSearch(sMovieTitle):
    oGui = cGui()
   
    exec "from resources.sites import kepliz_com as search"
    sSearchText = oGui.showKeyBoard()
    #title = (_("Enter search criteria")), text = searchTitle, is_dialog=True)
 
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)    
        sUrl = ('(http://www.film-streaming.co/' + sMovieTitle)
        searchUrl = "search.php?movie=", ('resultSearch', sUrl)
    exec "searchUrl"
   
    oGui.setEndOfDirectory()
 
 
def movieshdSearch(sMovieTitle):
    oGui = cGui()
   
    exec "from resources.sites import movieshd.tv as search"
    sSearchText = oGui.showKeyBoard()
    #title = (_("Enter search criteria")), text = searchTitle, is_dialog=True)
 
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)    
        sUrl = ('(http://www.film-streaming.co/' + sMovieTitle)
        searchUrl = "search.php?movie=", ('resultSearch', sUrl)
    exec "searchUrl"
   
    oGui.setEndOfDirectory()
           
def addMoviedb(sId, sFunction, sLabel, sIcon, sThumbnail, fanart, oOutputParameterHandler = ''):
   
    #addMoviedb(oGui, SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sFanart, oOutputParameterHandler)
    oGui = cGui()
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(sId)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    #oGuiElement.setIcon(sIcon)
    oGuiElement.setMeta(0)
    #oGuiElement.setThumbnail(sThumbnail)
    #oGuiElement.setFanart(fanart)
   
    #cGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.addFolder(oGuiElement, oOutputParameterHandler, False)
