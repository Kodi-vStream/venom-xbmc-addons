#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui #system de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #system de recherche pour l'hote
from resources.lib.gui.gui import cGui #system d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #system d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entrer des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortis des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code
from resources.lib.util import cUtil
import urllib2,urllib,re
import xbmcgui
import unicodedata,htmlentitydefs

from resources.lib.cloudflare import CloudflareBypass
 
SITE_IDENTIFIER = 'series_en_streaming_tv'
SITE_NAME = 'Series-en-streaming.tv'
SITE_DESC = 'Serie en streaming'
 
URL_MAIN = 'http://www.series-en-streaming.tv/'

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = ('http://www.series-en-streaming.tv/liste/', 'AlphaSearch')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def CleanTitle(title):
    title = cUtil().unescape(title)
    title = cUtil().removeHtmlTags(title)
    try:
        #title = unicode(title, 'utf-8')
        title = unicode(title, 'iso-8859-1')
    except:
        pass
    title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore')
    
    return title.encode( "utf-8")

def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series Nouveautés', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series Liste complete', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    for i in range(0,27) :
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break
        
        if (i < 1):
            sTitle = '[0-9]'
        else:
            sTitle = chr(64+i)
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://www.series-en-streaming.tv/liste/')
        oOutputParameterHandler.addParameter('sLetter', sTitle)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]', 'genres.png', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
        
def AlphaDisplay():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sLetter = oInputParameterHandler.getValue('sLetter')

    sHtmlContent = CloudflareBypass().GetHtml(sUrl)
    
    oParser = cParser()
    sPattern = '<a href=\'(http:\/\/www\.series-en-streaming\.tv\/serie\/.+?)\'>(' + sLetter + '[^<>]+?)<\/a><br>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = CleanTitle(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addTV(SITE_IDENTIFIER, 'ShowSaisons', sTitle, '', '','', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
        
        oGui.setEndOfDirectory()

        

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch :
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    #print sUrl

    sHtmlContent = CloudflareBypass().GetHtml(sUrl)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
   
    oParser = cParser()
    sPattern = "<a href='([^'<>]+?)' data-original-title='' title=''><img src='([^'<>]+?)' width='100%' height='100%' title='' data-original-title=''><h3 data-original-title='' title=''>(.+?)<\/h3>"
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        
        SpecHead = CloudflareBypass().GetHeadercookie(sUrl)
        
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sThumb = aEntry[1]
            if URL_MAIN in sThumb:
                sThumb = sThumb + SpecHead
            #print sThumb
           
            #not found better way
            #sTitle = unicode(sTitle,'iso-8859-1')
            #sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore').decode("unicode_escape")
            #sTitle = sTitle.encode( "utf-8")
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            sTitle = CleanTitle(aEntry[2])
            
            #sDisplayTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
 
            oGui.addTV(SITE_IDENTIFIER, 'ShowSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    if not sSearch:
        oGui.setEndOfDirectory()
   
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sHtmlContent = CloudflareBypass().GetHtml(sUrl)

    #sPattern = "<a target='playerFrame' href='([^<>]+?)'>(?:<img src='([^<>]+?)'><\/a>)*"
    sPattern = "href='([^<>]+?)'.+?>(?:<img src='([^<>]+?)'><\/a>)*"
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

            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if aEntry[1]:
                if 'VOSTFR' in aEntry[1]:
                    sMovieTitle = '[VOSTFR] ' + sTitle
                else:
                    sMovieTitle =  '[VF] ' + sTitle
        
            if (oHoster != False):         
                try:
                    oHoster.setHD(sHosterUrl)
                except: pass
                    
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)

                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
   
def ShowSaisons():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    sHtmlContent = CloudflareBypass().GetHtml(sUrl)
   
    oParser = cParser()
    sPattern = '<a href="([^<>]+?)" class="seasonLink">([^<>]+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sTitle = sMovieTitle + ' Saison ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
 
            oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory()
    
def showEpisode():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHtmlContent = CloudflareBypass().GetHtml(sUrl)
    
    #sHtmlContent = sHtmlContent.replace('\n','')
    sHtmlContent = sHtmlContent.replace("'",'"')
   
    oParser = cParser()
    #sPattern = "<a class='various' data-fancybox-type='iframe' href='(.+?)' > *(.+?)<\/a>\t*<\/h3>\t*(.+?)<br>"
    sPattern = ';" src="(.+?)" class="img-responsive">.+?<a class="various" data-fancybox-type="iframe" href="(.+?)" *> *(.+?)<\/a>\t*<\/h3>\t*(.+?)<br>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    #print aResult
   
    if (aResult[0] == True):
        
        SpecHead = CloudflareBypass().GetHeadercookie(sUrl)
        
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sTitle = sMovieTitle + ' ' + aEntry[2]
            sThumb = aEntry[0]
            if URL_MAIN in sThumb:
                sThumb = sThumb + SpecHead        
            sCom = aEntry[3]
                        
            sDisplayTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
 
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sCom, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory()
