# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#Ovni-crea
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser  
from resources.lib.comaddon import progress, VSlog, xbmc, xbmcgui, addon
# from resources.lib.util import cUtil  # outils pouvant etre utiles
import json
import xbmc
import xbmcaddon
import xbmcvfs
import requests


ADDON = addon()
URL_HOST = ADDON.getSetting('urlmain_alldebrid')


SITE_IDENTIFIER = 'alldebrid'
SITE_NAME = '[COLOR violet]Alldebrid[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

ALL_ALL = (URL_HOST + 'links/', 'showLiens')
ALL_MAGNETS = (URL_HOST + 'magnets/', 'showMagnets')
ALL_INFORMATION = ('https://alldebrid.fr', 'showInfo')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_ALL[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_ALL[1], 'Liens', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_MAGNETS[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_MAGNETS[1], 'Magnets', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_INFORMATION[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_INFORMATION[1], 'Information sur les hébergeurs ', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLiens(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')
    VSlog(sHtmlContent)

    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

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
            sUrl2 = sUrl + aEntry[0]
            VSlog(sUrl2)
            sThumb = ''
            #sLang = aEntry[3]
            #sQual = aEntry[4]
            #sHoster = aEntry[5]
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)  
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)    
            oOutputParameterHandler.addParameter('sDesc', sDesc)  
            oOutputParameterHandler.addParameter('referer', sUrl)  
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle , '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)  

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)  # cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showLiens', '[COLOR teal]Page ' + str(number) + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()  


def __checkForNextPage(sHtmlContent):  
    oParser = cParser()
    sPattern = '<div class="navigation".+? <span.+? <a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showMagnets():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')
    VSlog(sHtmlContent)

    # Pattern servant à retrouver les éléments dans la page
    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[0]
            sUrl2 = sUrl + aEntry[1]
            #VSlog(sUrl2)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            if 'mp4' and 'avi' and 'mkv' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle , 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showseriesHoster', sTitle , 'movies.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
    
def showseriesHoster(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')
    VSlog(sHtmlContent)

    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

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
            sUrl2 = sUrl + aEntry[0]
            VSlog(sUrl2)
            sThumb = ''
            #sLang = aEntry[3]
            #sQual = aEntry[4]
            #sHoster = aEntry[5]
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)  
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)    
            oOutputParameterHandler.addParameter('sDesc', sDesc)  
            oOutputParameterHandler.addParameter('referer', sUrl)  
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle , '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)  

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)  # cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showseriesHoster', '[COLOR teal]Page ' + str(number) + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory() 


def showHosters():  
    oGui = cGui()  
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')  
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')  
    #sThumb = oInputParameterHandler.getValue('sThumb')  
    #referer = oInputParameterHandler.getValue('referer')
                    
    sHosterUrl = sUrl
    VSlog(sHosterUrl)
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sMovieTitle)
        
    oGui.setEndOfDirectory()  # fin
    
def showInfo(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)

    sPattern = '<li class="([^"]+)">.+?<i alt=".+?" title="([^"]+)".+?</li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sDisponible = aEntry[0].replace('downloaders_available', 'Disponible').replace('downloaders_unavailable', 'Non Disponible')
            sHebergeur = aEntry[1]
            
            sDisplayTitle = ('%s (%s)') % (sHebergeur, sDisponible)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            
            oGui.addText(SITE_IDENTIFIER, sDisplayTitle)
                    

        progress_.VSclose(progress_)  

        oGui.setEndOfDirectory()  

