#-*- coding: utf-8 -*-
#Venom.mino60.TmpName
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
SITE_DESC = 'Base de données video.'
 
 
URL_MAIN = 'http://imdb.com'
 
#URL_SEARCH = (URL_MAIN + '/find?ref_=nv_sr_fn&s=all&q=%s', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
               

       
 
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
 
MOVIE_WORLD = (URL_MAIN + '/search/title?groups=top_1000&sort=user_rating,desc&start=1', 'showMovies')
#MOVIE_TOP_ACTORS = (URL_MAIN + '/list/ls050274118/', 'showActors')
MOVIE_TOP250 = (URL_MAIN + '/search/title?count=100&groups=top_250', 'showMovies')
MOVIE_TOP2016 = (URL_MAIN + '/search/title?year=2016,2016&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2015 = (URL_MAIN + '/search/title?year=2015,2015&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2014 = (URL_MAIN + '/search/title?year=2014,2014&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2013 = (URL_MAIN + '/search/title?year=2013,2013&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2012 = (URL_MAIN + '/search/title?year=2012,2012&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2011 = (URL_MAIN + '/search/title?year=2011,2011&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2010 = (URL_MAIN + '/search/title?year=2010,2010&title_type=feature&explore=languages', 'showMovies')


POSTER_URL = 'https://ia.media-imdb.com/images/m/'
#FANART_URL = 'https://image.tmdb.org/t/p/w780/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'
#FANART_URL = 'https://image.tmdb.org/t/p/original/'
   
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = 'http://imdb.com/search/title?groups=top_1000&sort=user_rating,desc&start=%s'+sSearchText
        #sUrl = 'http://%s.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&languages=fr|1&sort=moviemeter,asc&count=40&start=%s', 'showMovies')
 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
 
def load():
    oGui = cGui()
   
    #inutile
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'Top Films Mondial', 'films.png', oOutputParameterHandler)
 
    #inutile
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP_ACTORS[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP_ACTORS[1], 'Top Acteurs', 'films.png', oOutputParameterHandler)
      
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP250[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP250[1], 'Top 250', 'films.png', oOutputParameterHandler)
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2016[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2016[1], 'Top Films 2016', 'films.png', oOutputParameterHandler)
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2015[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2015[1], 'Top Films 2015', 'films.png', oOutputParameterHandler)
         
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2014[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2014[1], 'Top Films 2014', 'films.png', oOutputParameterHandler)
         
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2013[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2013[1], 'Top Films 2013', 'films.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2012[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2012[1], 'Top Films 2012', 'films.png', oOutputParameterHandler)
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2011[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2011[1], 'Top Films 2011', 'films.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2010[1], 'Top Films 2010', 'films.png', oOutputParameterHandler)

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
    
    #sPattern = 'class="lister-item.*?<img\salt="(.*?)".*?loadlate="(.*?\.jpg)".*?class="lister-item-index.*?>(.*?)</span>.*?class="lister-item-year.*?>\((\d+)\)</span.*?title="Users rated this (.*?\/10)'
    
    sPattern  ='class="lister-item-image.+?<img\salt="([^"]+)".+?loadlate="([^"]+)".+?class="lister-item-index.+?>([^<]+)</span>.+?class="lister-item-year.+?>([^<]+)</span.+?title="Users rated this(.+?)-'
		

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
            #sTitle = unescape(str(aEntry[1]))
            #sTitle = sTitle.encode( "utf-8")

            sTitle = ('[COLOR azure]%s [/COLOR]%s [COLOR beige]%s [/COLOR][COLOR fuchsia]%s[/COLOR]') % (aEntry[2], aEntry[0], aEntry[3], aEntry[4])
            sMovieTitle=re.sub('(\[.*\])','', sTitle)
            sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)
            sTitle2=re.sub('(.*)(\[.*\])','\\1 [COLOR orange]\\2[/COLOR]', sTitle)
            sThumbnail = aEntry[1].replace('UX67', 'UX328').replace('UY98', 'UY492').replace('67','0').replace('98','0')
            
            #sCom = unicode(aEntry[3], 'utf-8')#converti en unicode
            #sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
            #sCom = unescape(sCom)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', ('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            #oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
       
     
def __checkForNextPage(sHtmlContent):
    sPattern = '<a\shref="([^"]+?)"class="lister-page-next'
      
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    
    if (aResult[0] == True):
        sUrl = ('%s/search/title%s')% (URL_MAIN, aResult[1][0])
        return sUrl
 
    return False

    
def showHosters():

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    sExtraTitle = ''

    sMovieTitle = unicode(sMovieTitle, 'utf-8')#converti en unicode pour aider aux convertions
    sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sMovieTitle = sMovieTitle.encode("utf-8").lower() #on repasse en utf-8

    sMovieTitle = urllib.quote(sMovieTitle)
    
    sMovieTitle = re.sub('\(.+?\)',' ', sMovieTitle) #vire les tags entre parentheses
    
    #modif venom si le titre comporte un - il doit le chercher
    sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle) #vire les caracteres a la con qui peuvent trainer
    
    
    sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)',' ', sMovieTitle) #vire les articles

    sMovieTitle = re.sub(' +',' ',sMovieTitle)
    

    dialog3 = xbmcgui.Dialog()
    ret = dialog3.select('Selectionner un Moteur de Recherche',['Vstream (Fiable mais plus complexe)','Alluc (Simple mais resultats non garantis)'])

    if ret == 0:
        VstreamSearch(sMovieTitle)
    elif ret == 1:
        #AllucSearch(sMovieTitle + sExtraTitle)
        #modif test préfére les accent supprimer é = e
        sMovieTitle = sMovieTitle.replace('%C3%A9','e').replace('%C3%A0','a')
        AllucSearch(sMovieTitle + sExtraTitle)

def VstreamSearch(sMovieTitle):
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oHandler = cRechercheHandler()
    oHandler.setText(sMovieTitle)
    #oHandler.setDisp(sDisp)
    aPlugins = oHandler.getAvailablePlugins()
                
    oGui.setEndOfDirectory()
    
def AllucSearch(sMovieTitle):
    oGui = cGui()
    
    exec "from resources.sites import alluc_ee as search"
    sUrl = 'http://www.alluc.ee/stream/lang%3Afr+' + sMovieTitle
    #xbmc.log(str(sUrl))
    searchUrl = "search.%s('%s')" % ('showMovies', sUrl)
    exec searchUrl
    
    oGui.setEndOfDirectory()
    
    