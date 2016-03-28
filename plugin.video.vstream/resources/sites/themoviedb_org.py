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

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = '[COLOR orange]TheMovieDB[/COLOR]'
SITE_DESC = 'Base de données video.'

#doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = 'https://api.themoviedb.org/'

API_KEY = '92ab39516970ab9d86396866456ec9b6'
API_VERS = '3'
API_URL = URL_MAIN+API_VERS

POSTER_URL = 'https://image.tmdb.org/t/p/w396'
#FANART_URL = 'https://image.tmdb.org/t/p/w780/'
FANART_URL = 'https://image.tmdb.org/t/p/w1280'
#FANART_URL = 'https://image.tmdb.org/t/p/original/'


#https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6

#<views>551,504,503,508,515,50,51,500,550,560,501,572,573,574,570,571,505,511</views>
#viewmode = 500 Film
#viewmode = 503 Film + Information
#viewmode = 50  Liste


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Populaires', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films en salle', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films les mieux notés', 'notes.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/genre/movie/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreMovie', 'Films Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/tv/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries Populaires', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/tv/on_the_air')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries a la tv', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/tv/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries les mieux notés', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/genre/tv/list')
    oGui.addDir(SITE_IDENTIFIER, 'showGenreTV', 'Séries Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/person/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showActors', 'Acteurs Populaires', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche de film', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche de serie', 'series.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = API_URL+'/search/movie?query=' + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
        
def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = API_URL+'/search/tv?query=' + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
        
def showGenreMovie():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    
    sHtmlContent = oRequestHandler.request(); 
    result = json.loads(sHtmlContent)       

    total = len(sHtmlContent)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")
            sUrl = API_URL+'/genre/'+str(sId)+'/movies'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()

def showGenreTV():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    
    sHtmlContent = oRequestHandler.request(); 
    result = json.loads(sHtmlContent)       

    total = len(sHtmlContent)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")
            #sUrl = API_URL+'/genre/'+str(sId)+'/tv'
            sUrl = API_URL+'/discover/tv?with_genres=' + str(sId)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', str(sTitle), 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
        

def showMovies(sSearch = ''):
    
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        sUrl = sSearch

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oGui = cGui()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    oRequestHandler.addParameters('page', iPage)

    sHtmlContent = oRequestHandler.request();
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)

    if (total > 0):
        for i in result['results']:
            sId, sTitle, sOtitle, sThumbnail, sFanart = i['id'], i['title'], i['original_title'], i['poster_path'], i['backdrop_path']
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = ''

            sTitle = sTitle.encode("utf-8")
            if sFanart:
                sFanart = FANART_URL+sFanart
            else : sFanart = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('disp', 'search1')
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            
            oGui.addMovieDB(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, sFanart, oOutputParameterHandler)
            
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page '+str(iNextPage)+' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

            
    #test pr chnagement mode
    xbmc.executebuiltin('Container.SetViewMode(500)')
    #bmcgui.ListItem.select(1)        
            
    oGui.setEndOfDirectory()
    
    
def showSeries(sSearch=''):
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        sUrl = sSearch

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oGui = cGui()

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    oRequestHandler.addParameters('page', iPage)

    sHtmlContent = oRequestHandler.request();
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)
    #print result['results']
    if (total > 0):
        for i in result['results']:
            sId, sTitle, sOtitle, sThumbnail, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else:
                sThumbnail = '' 
                
            if sFanart:
                sFanart = FANART_URL+sFanart
            else : sFanart = ''

            sTitle = sTitle.encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sId', str(sId))
            oOutputParameterHandler.addParameter('sFanart', str(sFanart))
            
            oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesSaison', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)
            
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Page '+str(iNextPage)+' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #test pr chnagement mode
    xbmc.executebuiltin('Container.SetViewMode(500)')         
            
    oGui.setEndOfDirectory()

def showSeriesSaison():
    
    oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
    sId = oInputParameterHandler.getValue('sId')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    
    sUrl = API_URL+'/tv/' + sId
    
    oGui = cGui()
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')

    sHtmlContent = oRequestHandler.request()
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)
    #print result['results']
    if (total > 0):
        for i in result['seasons']:
            
            sdate, sNbreEp, sIdSeason, sThumbnail, SSeasonNum = i['air_date'], i['episode_count'], i['id'], i['poster_path'], i['season_number']
            
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = '' 

            sTitle = 'Saison ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sSeason', str(SSeasonNum))
            oOutputParameterHandler.addParameter('sFanart', str(sFanart))            
            
            oGui.addTVDB(SITE_IDENTIFIER, 'showSeriesEpisode', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)
            

    #test pr chnagement mode
    xbmc.executebuiltin('Container.SetViewMode(500)')         
            
    oGui.setEndOfDirectory() 
    

def showSeriesEpisode():
    
    oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
    sId = oInputParameterHandler.getValue('sId')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sFanart = oInputParameterHandler.getValue('sFanart')
    
    
    sUrl = API_URL+'/tv/' + sId + '/season/' + sSeason
    
    oGui = cGui()
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')

    sHtmlContent = oRequestHandler.request()
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)
    #print result['results']
    if (total > 0):
        for i in result['episodes']:
            
            #sId, sTitle, sOtitle, sThumbnail, sFanart = i['id'], i['name'], i['original_name'], i['poster_path'], i['backdrop_path']
            sdate, sIdEp, sEpNumber, sName, sThumbnail, SResume = i['air_date'], i['id'], i['episode_number'], i['name'], i['still_path'], i['overview']
            
            sName = sName.encode("utf-8")
            if sName == '':
                sName = sMovieTitle
            
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = ''

            sTitle = '[COLOR coral]S' + sSeason + 'E' + str(sEpNumber) + '[/COLOR] - ' + sName

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('disp', 'search2')
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sEpisode', str(sEpNumber))
            
            oGui.addTVDB(SITE_IDENTIFIER, 'showHosters', sTitle, 'series.png', sThumbnail, sFanart, oOutputParameterHandler)
            

    #test pr chnagement mode
    xbmc.executebuiltin('Container.SetViewMode(50)')         
            
    oGui.setEndOfDirectory()
    
  
    
def showActors():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    oRequestHandler.addParameters('page', iPage)

    sHtmlContent = oRequestHandler.request();
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)

    if (total > 0):
        for i in result['results']:
            #print i['name']
            sName, sThumbnail = i['name'], i['profile_path']
            
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = ''
                    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail)) 
            
            sName = sName.encode('utf-8')
            
            oGui.addMovieDB(SITE_IDENTIFIER, 'showActors', '[COLOR red]'+str(sName)+'[/COLOR]', '', sThumbnail, '', oOutputParameterHandler)

            for e in i['known_for']:
                try:                     
                    sTitle = unicodedata.normalize('NFKD', e['title']).encode('ascii','ignore')
                    
                except: sTitle = "Aucune information"
                sId = e['id']
                try:
                    sFanart = FANART_URL+e['backdrop_path']
                except:
                    sFanart = ''
                                                                
                try:
                    sThumbnail = POSTER_URL+e['poster_path']
                except: 
                    sThumbnail = ''

                #sTitle = sTitle.encode("utf-8")

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('disp', 'none')
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                
                oGui.addMovieDB(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sFanart, oOutputParameterHandler)
                
            
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showActors', '[COLOR teal]Page '+str(iNextPage)+' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span><a class='page-numbers' href='([^<]+)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    

def showHosters():

    oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')
      
    #nettoyage du nom pr la recherche
    #print 'avant ' + sMovieTitle
    sMovieTitle = unicode(sMovieTitle, 'utf-8')#converti en unicode pour aider aux convertions
    sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sMovieTitle = sMovieTitle.encode("utf-8").lower() #on repasse en utf-8
    #modif venom si le titre comporte un - il doit le chercher
    #sMovieTitle = re.sub(r'[^(\w| )]', ' ', sMovieTitle) #vire les caracteres a la con qui peuvent trainer
    sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)',' ', sMovieTitle) #vire les articles
    sMovieTitle = re.sub('\(.+?\)',' ', sMovieTitle) #vire les parentheses
    sMovieTitle = re.sub(' +',' ',sMovieTitle) #vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +
    #print 'apres ' + sMovieTitle
    
    sExtraTitle = ''
    #si c'est une serie
    if sSeason and sEpisode:
        sExtraTitle = ' S' + "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpisode)
        
    dialog3 = xbmcgui.Dialog()
    ret = dialog3.select('Selectionner un Moteur de Recherche',['Vstream (Fiable mais plus complexe)','Alluc (Simple mais resultats non garantis)'])

    if ret == 0:
        VstreamSearch(sMovieTitle)
    elif ret == 1:
        AllucSearch(sMovieTitle + sExtraTitle)
        
        


def VstreamSearch(sMovieTitle):
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #Type de recherche
    sDisp = oInputParameterHandler.getValue('disp')
    
    oHandler = cRechercheHandler()
    oHandler.setText(sMovieTitle)
    oHandler.setDisp(sDisp)
    aPlugins = oHandler.getAvailablePlugins()
                
    oGui.setEndOfDirectory()
    
def AllucSearch(sMovieTitle):
    oGui = cGui()
    
    exec "from resources.sites import alluc_ee as search"
    sUrl = 'http://www.alluc.ee/stream/lang%3Afr+' + sMovieTitle 
    searchUrl = "search.%s('%s')" % ('showMovies', sUrl)
    exec searchUrl
    
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
