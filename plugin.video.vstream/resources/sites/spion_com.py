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
 
MOVIE_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN + 'page/1/', 'showMovies')
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
    liste.append( ['Actualite', URL_MAIN + 'category/actualite/page/1/'] )
    liste.append( ['Animaux', URL_MAIN + 'category/animaux/page/1/'] )
    liste.append( ['Art', URL_MAIN + 'category/art-technique/page/1/'] )
    liste.append( ['Danse', URL_MAIN + 'category/danse/page/1/'] )
    liste.append( ['Experience', URL_MAIN + 'category/experiences/'] )
    liste.append( ['Fake', URL_MAIN + 'category/fake-trucage/page/1/'] )
    liste.append( ['Guerre', URL_MAIN + 'category/guerre-militaire/page/1/'] )
    liste.append( ['Humour', URL_MAIN + 'category/humour-comedie/page/1/'] )
    liste.append( ['Internet', URL_MAIN + 'category/siteweb-internet/page/1/'] )
    liste.append( ['Jeux Video', URL_MAIN + 'category/jeuxvideo-consoles/page/1/'] )
    liste.append( ['Musique', URL_MAIN + 'category/musique/page/1/'] ) 
    liste.append( ['Non Classe', URL_MAIN + 'category/non-classe/page/1/'] )
    liste.append( ['Owned', URL_MAIN + 'category/owned/page/1/'] )
    liste.append( ['Pub', URL_MAIN + 'category/publicite-marque/page/1/'] )
    liste.append( ['Santé', URL_MAIN + 'category/sante-corps/page/1/'] )  
    liste.append( ['Sport', URL_MAIN + 'category/sport/page/1/'] )
    liste.append( ['Technologie', URL_MAIN + 'category/technologie-innovations/page/1/'] )
    liste.append( ['Transport', URL_MAIN + 'category/auto-transport/'] )
    liste.append( ['TV & Cinema', URL_MAIN + 'category/tv-cinema/page/1/'] )
    liste.append( ['WTF?!', URL_MAIN + 'category/wtf/page/1/'] )
    liste.append( ['Zapping', URL_MAIN + 'category/zapping-web/page/1/'] )
                 
    if SPION_CENSURE == False:
        liste.append( ['NSFW (+18)', URL_MAIN + 'category/notsafeforwork/page/1/'] )
        liste.append( ['Trash (+18)', URL_MAIN + 'category/trash-gore/page/1/'] )          
                 
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
     
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '')
     
    sPattern = 'class="post clearfix">.+?<img src="([^<>"]+?)".+?<a href="([^<>"]+?)" rel="bookmark" title="([^"<>]+?)">'
     
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
         
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
             
            sUrlp    = str(aEntry[1]) 
            sTitle  = str(aEntry[2])
            sPoster = str(aEntry[0])
             
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlp) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumbnail', sPoster)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sPoster,'', oOutputParameterHandler)
             
        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sUrl)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]',
                        'next.png',  oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
 
 
def __checkForNextPage(sUrl):
    oParser = cParser()
    sPattern = 'page\/([0-9]+)\/'
    aResult = oParser.parse(sUrl, sPattern)
    
    print sUrl
    print aResult
 
    if (aResult[0] == True):
        page = int(aResult[1][0]) + 1
        return URL_MAIN + 'page/' + str(page) + '/'
 
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
                               .replace('<iframe src=\'http://creative.rev2pub.com','')\
                               .replace('dai.ly','www.dailymotion.com/video')\
                               .replace('youtu.be/','www.youtube.com/watch?v=')
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
    
    if (aResult[0] == False):
        sPattern = '<div class="video_tabs"><a href="([^<>"]+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
             
    if (aResult[0] == True):
        for aEntry in aResult[1]:
             
            sHosterUrl = str(aEntry)
            # Certains URL "dailymotion" sont écrits : //www.dailymotion.com
            if sHosterUrl[:4] != 'http':
                sHosterUrl = 'http:' + sHosterUrl     
                 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
             
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                 
    oGui.setEndOfDirectory()
