#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser

from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import progress, VSlog
from resources.lib.util import cUtil
import re, unicodedata, urllib, urllib2


SITE_IDENTIFIER = 'iptv_gratuit'
SITE_NAME = 'IptvGratuit'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://iptvgratuit.com/'
IPTV_WOLRD = URL_MAIN + 'iptv-world/'
IPTV_FRANCE = URL_MAIN + 'iptv-france/'
IPTV_ESPAGNE = URL_MAIN + 'iptv-espagne/'
IPTV_ITALIE = URL_MAIN + 'iptv-italie/'
IPTV_BELGIQUE = URL_MAIN + 'iptv-belgique/'
IPTV_SUISSE = URL_MAIN + 'iptv-suisse/'
IPTV_CANADA = URL_MAIN + 'iptv-canada/'
IPTV_ANGLETERRE = URL_MAIN + 'iptv-uk/'
IPTV_ALLEMAGNE = URL_MAIN + 'iptv-allemagne/'
IPTV_USA = URL_MAIN + 'iptv-usa/'
IPTV_TURK = URL_MAIN + 'iptv-turk/'
IPTV_ARABIC = URL_MAIN + 'iptv-arabic/'
IPTV_SPORT = URL_MAIN + 'iptv-sport/'
IPTV_VOD = URL_MAIN + 'iptv-vod/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_WOLRD)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste mondial', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_FRANCE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste France', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ESPAGNE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Espagne', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ITALIE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Italie', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_BELGIQUE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Belgique', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_SUISSE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Suisse', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_CANADA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Canada', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ANGLETERRE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Anglaise', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ALLEMAGNE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Allemande', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_USA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste USA', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_TURK)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Turque', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ARABIC)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Arabe', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_SPORT)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste SPORT', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_VOD)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste VOD', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
       

def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'listes.png', oOutputParameterHandler)
            
        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    # oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sPattern = 'class="next page-numbers" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showAllPlaylist():#On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<a class="more-link" title="(.+?)".+?href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sTitletest = ''
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[0]
            sUrl2 = aEntry[1]
            
            if (sTitle == sTitletest):
                continue
            else:
                sTitletest = sTitle
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)
            
        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
    
def showAllPlaylist2():#On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHtmlContent = getHtml(sUrl)

    sUrl2 = getDownloadLink(sHtmlContent)

    for url in sUrl2:

        if 'download' in url:
            VSlog('Redirect')
            url = getRealLink(url)
            oGui.addText(SITE_IDENTIFIER, url)
        else:
            oGui.addText(SITE_IDENTIFIER, 'rien')
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)


    oGui.setEndOfDirectory()
