#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#ressource https://wvv.vkstream.org/icon/logo.png


from resources.lib.gui.hoster import cHosterGui 
from resources.lib.gui.gui import cGui 
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler 
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.lib.comaddon import progress  #,VSlog  #,xbmc

SITE_IDENTIFIER = 'vkstream'
SITE_NAME = 'vkstream'      
SITE_DESC = 'Series en streaming, streaming HD, streaming VF, séries, récent' #description courte de votre source

URL_MAIN = 'https://wvv.vkstream.org/' 

SERIE_SERIES = (URL_MAIN + 'series/page/1', 'showMovies')
SERIE_GENRES = (True, 'showGenres') 
SERIE_NEWS = (URL_MAIN , 'showMovies')  # sur la page correspond à =' dernieres series en streaming'  ; ne contient pas les derniers episodes vf et vost du site
SERIE_VIEWS = (URL_MAIN + 'top-series/page/1', 'showMovies') 
SERIE_ANNEES = (True, 'showSerieYears')  

URL_SEARCH = (URL_MAIN + 'search?search=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load(): 
   
    oGui = cGui() 
    oOutputParameterHandler = cOutputParameterHandler() #appelle la fonction pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
       
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])   
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)     
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'annees.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory() 

def showSearch(): 
    oGui = cGui()
    
    sSearchText = oGui.showKeyBoard()       
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl)                    
        oGui.setEndOfDirectory()
        return


def showGenres():   
    oGui = cGui()   
    
    liste = []  
    liste.append( ['Action', URL_MAIN + 'series/genre/action_1'] )
    liste.append( ['Animation', URL_MAIN + 'series/genre/animation_1'] )
    liste.append( ['Aventure', URL_MAIN + 'series/genre/aventure_1'] )
    liste.append( ['Biopic', URL_MAIN + 'series/genre/biopic_1'] )   
    liste.append( ['Comédie', URL_MAIN + 'series/genre/comaedie_1'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'series/genre/comaedie-musicale_1'] )
    liste.append( ['Documentaire', URL_MAIN + 'series/genre/documentaire_1'] )
    liste.append( ['Drame', URL_MAIN + 'series/genre/drame_1'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'series/genre/epouvante-horreur_1'] )
    liste.append( ['Famille', URL_MAIN + 'series/genre/famille_1'] )
    liste.append( ['Fantastique', URL_MAIN + 'series/genre/fantastique_1'] )
    liste.append( ['Guerre', URL_MAIN + '/series/genre/guerre_1'] )
    liste.append( ['Policier', URL_MAIN + 'series/genre/policier_1'] )
    liste.append( ['Romance', URL_MAIN + 'series/genre/romance_1'] )
    liste.append( ['Science Fiction', URL_MAIN + 'series/genre/science-fiction_1'] )
    liste.append( ['Thriller', URL_MAIN + 'series/genre/thriller_1'] )
    liste.append( ['Western', URL_MAIN + 'series/genre/western_1'] )      
    liste.append( ['Divers', URL_MAIN + 'series/genre/divers_1'] )
    
    for sTitle, sUrl in liste: 

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()
    
    for i in reversed (range(1997, 2021)):  #avant 1997 peu de results
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee/' + Year+'_1')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()   
    
    if sSearch:     
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="item_larg">\s*<a href="([^"]+)".+?"([^"]+)">.+?<img src="([^"]+)"'        
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
            
            sTitle = aEntry[1]
            sUrl2 = aEntry[0]
            sThumb =aEntry[2]           
            if sThumb.startswith('/storage'):
                sThumb = URL_MAIN[:-1] + sThumb
            sDesc = '' 

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('sDesc', sDesc) 
            #oOutputParameterHandler.addParameter('referer', sUrl) # URL d'origine, parfois utile comme référence                        
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)          

        progress_.VSclose(progress_) 

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)
        
    if not sSearch:
        oGui.setEndOfDirectory()                            


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)"\s*rel="next"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
    return False


def showSerieSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')#ex:
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()      
    
    #  description 
    sPattern = 'colo_cont">.+?>([^>]*)<\/p>'# 3ms   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        sDesc= aResult[1][0]
        sDesc = ('[COLOR coral]%s[/COLOR] %s') % (' SYNOPSIS : \r\n\r\n', sDesc)# '\r\n' ? voir sur autre os retour de ligne
    else:
        sDesc= ''  
      
    sPattern = '<div class="item".+?"([^"]+)".+?"([^"]+)".+?<img src="([^"]+)".+?<h2>([^"]+)<.h2>'   #3ms
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #g1 urls  g2 titre(no use)   g3 thumb   g4 saison
    
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
                     
            sTitle=  sMovieTitle +' ' +aEntry[3]  #sTitle= aEntry[1] +'-'+ aEntry[3]  # attention mettre espace
            sUrl2 = aEntry[0]
        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showSerieSaisonsEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
    
    
def showSerieSaisonsEpisodes():
    oGui = cGui()
      
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"" href="([^"]*)".+?>([^>]*)<.+?ep_ar.+?span>([^<]*)<'
    oParser = cParser()        
    aResult = oParser.parse(sHtmlContent, sPattern)   
  
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sUrl = aEntry[0]
            sTitle =  sMovieTitle + ' ' + aEntry[1]+ aEntry[2]            
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)#modife1
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)                       
            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def seriesHosters():   
    oGui = cGui()                 
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()    
        
    sPattern = 'class="p-1 a_server.+?href=..([^>]*)\'.+?alt="([^"]*)".+?icon.([^"]*).png'
    #g1 url g2 host g3 vostfr vf
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    
    if (aResult[0] == True):
        
        for aEntry in aResult[1]:                                     
            
            if (str(aEntry[0]).find('streaming-video.html') >=0) :  # utilise parfois deux fois qload
                continue                       
                
            sHosterName= aEntry[1]
            sHosterUrl = URL_MAIN+aEntry[0]
            oHoster = cHosterGui().checkHoster(sHosterName)   
            QualityVideo=str(aEntry[2]).upper()      
            
            if (oHoster != False):                       
                sHosterName=sHosterName.lower()#                                   
                sMovieColorTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, QualityVideo)
                oHoster.setDisplayName(sMovieColorTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
