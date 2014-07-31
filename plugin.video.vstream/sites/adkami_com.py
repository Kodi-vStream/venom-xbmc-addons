#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re,string

SITE_IDENTIFIER = 'adkami_com'
SITE_NAME = 'adkami.com'

URL_MAIN = 'http://www.adkami.com'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.adkami.com/video?recherche=&version=1&type2=0')
    __createMenuEntry(oGui, 'showMovies', 'Animés VF', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.adkami.com/video?recherche=&version=2&type2=0')
    __createMenuEntry(oGui, 'showMovies', 'Animés VOSTFR', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('type2', 0)
    oOutputParameterHandler.addParameter('title', 'Animés')
    __createMenuEntry(oGui, 'showLang', 'Animés A-Z', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('type2', 0)
    oOutputParameterHandler.addParameter('title', 'Animés')
    __createMenuEntry(oGui, 'showLanggenre', 'Animés Genre', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.adkami.com/video?recherche=&version=1&type2=1')
    __createMenuEntry(oGui, 'showMovies', 'Séries VF', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.adkami.com/video?recherche=&version=2&type2=1')
    __createMenuEntry(oGui, 'showMovies', 'Séries VOSTFR', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('type2', 1)
    oOutputParameterHandler.addParameter('title', 'Séries')
    __createMenuEntry(oGui, 'showLang', 'Séries A-Z', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('type2', 1)
    oOutputParameterHandler.addParameter('title', 'Séries')
    __createMenuEntry(oGui, 'showLanggenre', 'Séries Genre', '', '', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sThumbnail, sDesc, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setDescription(cUtil().removeHtmlTags(sDesc))
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
def showLang():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sType2 = oInputParameterHandler.getValue('type2')
    sTitle = oInputParameterHandler.getValue('title')
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('version', 0)
    oOutputParameterHandler.addParameter('type2', sType2)
    __createMenuEntry(oGui, 'showAZ', sTitle+' A-Z', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('version', 1)
    oOutputParameterHandler.addParameter('type2', sType2)
    __createMenuEntry(oGui, 'showAZ', sTitle+' A-Z VF', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('version', 2)
    oOutputParameterHandler.addParameter('type2', sType2)
    __createMenuEntry(oGui, 'showAZ', sTitle+' A-Z VOSTFR', '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
    
    
def showLanggenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sType2 = oInputParameterHandler.getValue('type2')
    sTitle = oInputParameterHandler.getValue('title')
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('version', 0)
    oOutputParameterHandler.addParameter('type2', sType2)
    __createMenuEntry(oGui, 'showGenre', sTitle+' Genre', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('version', 1)
    oOutputParameterHandler.addParameter('type2', sType2)
    __createMenuEntry(oGui, 'showGenre', sTitle+' Genre VF', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oOutputParameterHandler.addParameter('version', 2)
    oOutputParameterHandler.addParameter('type2', sType2)
    __createMenuEntry(oGui, 'showGenre', sTitle+' Genre VOSTFR', '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
        
def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sVersion = oInputParameterHandler.getValue('version')
    sType2 = oInputParameterHandler.getValue('type2')
    
    sUrl = 'http://www.adkami.com/video?recherche=&version='+str(sVersion)+'&type2='+str(sType2)+'#.'
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('AZ', '.')
    __createMenuEntry(oGui, 'showMoviesAZ', '.', '', '', oOutputParameterHandler)          
    for i in string.ascii_uppercase:
        sUrl = 'http://www.adkami.com/video?recherche=&version='+str(sVersion)+'&type2='+str(sType2)+'#'+i
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        __createMenuEntry(oGui, 'showMoviesAZ', i, '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
        
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sVersion = oInputParameterHandler.getValue('version')
    sType2 = oInputParameterHandler.getValue('type2')
 
    liste = []
    liste.append( ['Action','http://www.adkami.com/video?recherche=&genre3=1&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Aventure','http://www.adkami.com/video?recherche=&genre3=2&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Amour & Amitié','http://www.adkami.com/video?recherche=&genre3=3&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Combat','http://www.adkami.com/video?recherche=&genre3=4&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Comédie','http://www.adkami.com/video?recherche=&genre3=5&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Contes & Récits','http://www.adkami.com/video?recherche=&genre3=6&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Cyber & Mecha','http://www.adkami.com/video?recherche=&genre3=7&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Dark Fantasy','http://www.adkami.com/video?recherche=&genre3=8&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Drame','http://www.adkami.com/video?recherche=&genre3=9&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Ecchi','http://www.adkami.com/video?recherche=&genre3=10&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Educatif','http://www.adkami.com/video?recherche=&genre3=11&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Énigme & Policier','http://www.adkami.com/video?recherche=&genre3=12&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Épique & Héroique','http://www.adkami.com/video?recherche=&genre3=13&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Espace & Sci-Fiction','http://www.adkami.com/video?recherche=&genre3=14&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Familial & Jeunesse','http://www.adkami.com/video?recherche=&genre3=15&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Fantastique & Mythe','http://www.adkami.com/video?recherche=&genre3=16&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Hentai','http://www.adkami.com/video?recherche=&genre3=17&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Historique','http://www.adkami.com/video?recherche=&genre3=18&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Horreur','http://www.adkami.com/video?recherche=&genre3=19&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Magical Girl','http://www.adkami.com/video?recherche=&genre3=20&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Musical','http://www.adkami.com/video?recherche=&genre3=21&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Psychologique','http://www.adkami.com/video?recherche=&genre3=22&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Sport','http://www.adkami.com/video?recherche=&genre3=23&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Tranche de vie','http://www.adkami.com/video?recherche=&genre3=24&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Shôjo-Ai','http://www.adkami.com/video?recherche=&genre3=25&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Shônen-Ai','http://www.adkami.com/video?recherche=&genre3=26&type2='+str(sType2)+'&version='+str(sVersion)] )
    liste.append( ['Yaoi /BL','http://www.adkami.com/video?recherche=&genre3=27&type2='+str(sType2)+'&version='+str(sVersion)] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        __createMenuEntry(oGui, 'showMovies', sTitle, '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showMoviesAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sAZ = oInputParameterHandler.getValue('AZ')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = '<li><a href="([^<]+)">.+?<span class="bold">(.+?)</span></p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if len(sAZ)>0 and aEntry[1].upper()[0] == sAZ :

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
                __createMenuEntry(oGui, 'showEpisode', aEntry[1], '', '', oOutputParameterHandler)
            

    oGui.setEndOfDirectory()
    
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = '<li><a href="([^<]+)">.+?<span class="bold">(.+?)</span></p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:                

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
                __createMenuEntry(oGui, 'showEpisode', aEntry[1], '', '', oOutputParameterHandler)
            

    oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = '<li style.+?>(.+?)</li>|<li title=""><a href="([^<]+)">([^<]+)</a></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                __createMenuEntry(oGui, 'showEpisode', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', '', '', oOutputParameterHandler)
            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
                __createMenuEntry(oGui, 'showHosters', sMovieTitle+' - '+aEntry[2], '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();


    sPattern = '</div><iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl) 

    oGui.setEndOfDirectory()