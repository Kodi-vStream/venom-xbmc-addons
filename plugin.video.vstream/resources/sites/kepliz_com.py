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
import urllib2,urllib,re
#import xbmcgui
import unicodedata,htmlentitydefs
 
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz.com'
SITE_DESC = 'Film en streaming'
 
ACCEUILPATTERN  = ''#non utilisé
FILMPATTERN = '<div class="article-content"><p style="text-align: center;"><img src="(.+?)" border.+?<p style="text-align: left;">([^<>]+?)<\/p>'
URL_MAIN = 'http://www.kepliz.com/gthy44bv8gf7h8dfs04vf54fsd87/'
SEARCHPATTERN = '<fieldset> *<div> *<b><a *href="\/gthy44bv8gf7h8dfs04vf54fsd87\/(.+?)" *>(.+?)<\/a><\/b>'
NORMALPATTERN = '<span style="list-style-type:none;" >.+? href="\/gthy44bv8gf7h8dfs04vf54fsd87\/(.+?)">(.+?)<\/a>'
NEXTPAGEPATTERN = '<span class="pagenav">[0-9]+<.span><.li><li><a title=".+?" href="\/gthy44bv8gf7h8dfs04vf54fsd87\/(.+?)" class="pagenav">'
FRAMEPATTERN = 'KEPLIZpluginsphp\("player1",{link:"(.+?)"}\);'
POSTURL = URL_MAIN + 'plugins/ty4h5fdgdf8df021f578cv1v5g4fsdg8d7/plugins/KEPLIZpluginsphp.php'
HOSTPATTERN = '"link":"([^"]+?)","label":"([^"]+?)"'

#pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenre')

DOC_DOCS = (URL_MAIN + 'index.php?option=com_content&view=category&id=26', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
 
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
 
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + 'index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=' + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showGenre():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'index.php?option=com_content&view=category&id=1'] )
    liste.append( ['Aventure',URL_MAIN + 'index.php?option=com_content&view=category&id=4'] )
    liste.append( ['Comedie',URL_MAIN + 'index.php?option=com_content&view=category&id=6'] )
    liste.append( ['Drame',URL_MAIN + 'index.php?option=com_content&view=category&id=7'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'index.php?option=com_content&view=category&id=9'] ) 
    liste.append( ['Fantastique',URL_MAIN + 'index.php?option=com_content&view=category&id=8'] )  
    liste.append( ['Policier',URL_MAIN + 'index.php?option=com_content&view=category&id=10'] )
    liste.append( ['Science Fiction',URL_MAIN + 'index.php?option=com_content&view=category&id=11'] )
    liste.append( ['Thriller',URL_MAIN + 'index.php?option=com_content&view=category&id=12'] )
    liste.append( ['Animation',URL_MAIN + 'index.php?option=com_content&view=category&id=2'] )
    liste.append( ['Documentaires',URL_MAIN + 'index.php?option=com_content&view=category&id=26'] )  
    liste.append( ['Spectacle',URL_MAIN + 'index.php?option=com_content&view=category&id=3'] ) 
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showMovies(sSearch = ''):
    oGui = cGui()
 
    if sSearch :
        sUrl = sSearch
        sPattern = SEARCHPATTERN
    else :
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = NORMALPATTERN
        # if (sUrl == URL_MAIN) :
            # sPattern = NORMALPATTERN
        # else:
            # sPattern = NORMALPATTERN
   
    #print sUrl
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sTitle2 = aEntry[1]
            sTitle2 = re.sub('<font color="#[0-9]{6}" *><i>HD<\/i><\/font>', '[HD]',sTitle2)
            sUrl2 = aEntry[0]
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            sDisplayTitle = cUtil().DecoTitle(sTitle2)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle2))
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = NEXTPAGEPATTERN
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return str(URL_MAIN) + aResult[1][0]
 
    return False
 
def showHosters():
    oGui = cGui()
   
    sThumb = ''
    sComm = ''
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    sPattern = FILMPATTERN
    aResult = oParser.parse(sHtmlContent, sPattern)
       
    sThumb = aResult[1][0][0]
    sComm = unescape(aResult[1][0][1])
 
    sHtmlContent = sHtmlContent.replace('\r','')
   
    sPattern = FRAMEPATTERN
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sLink', aResult[1][0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sDisplayTitle, sThumb, sThumb, sComm, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory()
   
def showHostersLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLink = oInputParameterHandler.getValue('sLink')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
    headers = {'User-Agent': UA ,
               'Host' : 'kepliz.com',
               'Referer': sUrl,
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding' : 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    
    post_data = {'link' : sLink}
    
    req = urllib2.Request(POSTURL , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    
    oParser = cParser()
    sPattern = HOSTPATTERN
    aResult = oParser.parse(data, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break


            sLink = aEntry[0]
            Squality = aEntry[1]
            sTitle = sMovieTitle.replace(' [HD]','')
            sTitle = '[' + Squality + '] ' + sTitle
           
            sHosterUrl = str(sLink)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
            cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
