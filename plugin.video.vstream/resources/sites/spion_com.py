#-*- coding: utf-8 -*-
#Par jojotango
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code
#from resources.lib.util import cUtil #outils pouvant etre utiles
 
 
SITE_IDENTIFIER = 'spion_com'
SITE_NAME = 'Spi0n.com'
SITE_DESC = 'Toute l\'actualité insolite du web est chaque jour sur Spi0n.com'
 
URL_MAIN = 'http://www.spi0n.com/'
 
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NETS = (URL_MAIN, 'showMovies')
NETS_NEWS = (URL_MAIN, 'showMovies')
NETS_GENRES = (True, 'showGenre')
 
# True : Contenu Censuré | False : Contenu Non Censuré
SPION_CENSURE = True   
                         
 
def load(): 
    oGui = cGui() 
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0]) 
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Videos Nouveautes', 'news.png', oOutputParameterHandler)  
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Videos Genres', 'genres.png', oOutputParameterHandler)
               
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return
 
 
def showGenre():
    oGui = cGui()
  
    liste = []
    liste.append( ['Actualite', URL_MAIN + 'actualite/'] )
    liste.append( ['Animaux', URL_MAIN + 'animaux/'] )
    liste.append( ['Art', URL_MAIN + 'art-technique/'] )
    liste.append( ['Danse', URL_MAIN + 'danse/'] )
    liste.append( ['Experience', URL_MAIN + 'experiences/'] )
    liste.append( ['Fake', URL_MAIN + 'fake-trucage/'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre-militaire/'] )
    liste.append( ['Humour', URL_MAIN + 'humour-comedie/'] )
    liste.append( ['Internet', URL_MAIN + 'siteweb-internet/'] )
    liste.append( ['Jeux Video', URL_MAIN + 'jeuxvideo-consoles/'] )
    liste.append( ['Musique', URL_MAIN + 'musique/'] ) 
    liste.append( ['Non Classe', URL_MAIN + 'non-classe'] )
    liste.append( ['Owned', URL_MAIN + 'owned/'] )
    liste.append( ['Pub', URL_MAIN + 'publicite-marque/'] )
    liste.append( ['Santé', URL_MAIN + 'sante-corps/'] )  
    liste.append( ['Sport', URL_MAIN + 'sport/'] )
    liste.append( ['Technologie', URL_MAIN + 'technologie-innovations/'] )
    liste.append( ['Transport', URL_MAIN + 'auto-transport/'] )
    liste.append( ['TV & Cinema', URL_MAIN + 'tv-cinema/'] )
    liste.append( ['WTF?!', URL_MAIN + 'wtf/'] )
    liste.append( ['Zapping', URL_MAIN + 'zapping-web/'] )
                 
    if SPION_CENSURE == False:
        liste.append( ['NSFW (+18)', URL_MAIN + 'notsafeforwork/'] )
        liste.append( ['Trash (+18)', URL_MAIN + 'trash-gore/'] )          
                 
    for sTitle,sUrl in liste:
         
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler) 
               
    oGui.setEndOfDirectory()
         
 
def showMovies(sSearch = ''):
    oGui = cGui()
     
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '')\
                               .replace('</span>', '')
     
    sPattern = '<span class="image_shadow_container fl"><a href="([^<]+)" title="([^<]+)"><img src="(.+?)"'
    #- ([^<]+) je veux cette partie de code mais y a une suite
    #- .+? je ne veux pas cette partie et peu importe ce qu'elle contient
    #- (.+?) je veux cette partie et c'est la fin
     
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
         
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
             
            sUrl    = str(aEntry[0]) 
            sTitle  = str(aEntry[1])
            sPoster = str(aEntry[2])
             
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumbnail', sPoster)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sPoster,
                          '', oOutputParameterHandler)
             
        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]',
                        'next.png',  oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
 
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="yellow fl"><a href="([^<]+)">.+?</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
     
    if aResult[0] == False:
        sPattern = '<span class="current">.+?href="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        return aResult[1][0]
 
    return False
     
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() 
    sUrl = oInputParameterHandler.getValue('siteUrl') 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
     
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')\
                               .replace('<iframe src=\'http://creative.rev2pub.com','') 
 
    oParser = cParser()
    sPattern = '<p style=".+?"><iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
     
    if SPION_CENSURE:
        if 'content="Trash"' in sHtmlContent or 'content="NSFW"' in sHtmlContent:
            aResult = list(aResult)
            aResult[0] = False
            txt = '[COLOR khaki]Pour activer le contenu (+18) mettre '\
                    '"SPION_CENSURE = False" dans '\
                    '/.kodi/addons/plugin.video.vstream/resources/sites/spion_com.py'\
                    '[/COLOR]'
            oGui.addDir(SITE_IDENTIFIER, '', txt, '', cOutputParameterHandler())
             
    if (aResult[0] == True):
        for aEntry in aResult[1]:
             
            sHosterUrl = str(aEntry)
            # Certains URL "dailymotion" sont écrits : //www.dailymotion.com
            if sHosterUrl[:4] != 'http:':                
                sHosterUrl = 'http:' + sHosterUrl     
                 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
             
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                 
    oGui.setEndOfDirectory()
