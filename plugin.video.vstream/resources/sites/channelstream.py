# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re
import requests
import json


from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.sites.freebox import play__  # A garder, appel implicite
from resources.lib.util import Quote
from datetime import datetime, timedelta

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channel Stream'
SITE_DESC = 'iptv'

URL_MAIN = 'https://channelstream.me'

TV_FRENCH = (URL_MAIN + "/chaine-tv.php", 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    oGui = cGui()

    liste = []
    liste.append(['Généralistes', 'Chaîne de télévision généraliste', 'tv.png'])
    liste.append(['Cinéma', 'Chaîne consacrée aux Film', 'films.png'])
    liste.append(['Sport', 'Chaîne Sportive', 'sport.png'])
    liste.append(['Science et Nature', 'Chaîne axés sur les sciences', 'buzz.png'])


    for sTitle, sFiltre, sIcon in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', TV_FRENCH[0])
        oOutputParameterHandler.addParameter('sFiltre', sFiltre)
        oGui.addDir(SITE_IDENTIFIER, TV_FRENCH[1], sTitle, sIcon, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sFiltre = oInputParameterHandler.getValue('sFiltre')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, sFiltre, '<!-- Type Chaîne -->')
    sPattern = 'location.href = \'\.(.+?)\'.+?src=\'(.+?)\'.+?<div align="center">(.+?)</div>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if not "+18" in str(aEntry[2]):
                sTitle = aEntry[2]
                sUrl2 = URL_MAIN + aEntry[0]
                sThumb = URL_MAIN + '/' + aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    

    # Double Iframe a passer.
    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)".+?</iframe>'
    iframeURL = oParser.parse(sHtmlContent, sPattern)[1][0]

    oRequestHandler = cRequestHandler(iframeURL)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe src="([^"]+)".+?</iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if not aResult[1]:    # Pas de flux
        oGui.setEndOfDirectory()
        return
    
    iframeURL1 = aResult[1][0]

    oRequestHandler = cRequestHandler(iframeURL1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', iframeURL)
    sHtmlContent2 = oRequestHandler.request()

    sPattern2 = 'var\s+cid[^\'"]+[\'"]{1}([0-9]+)'
    aResult = re.findall(sPattern2, sHtmlContent2)

    if aResult:
        str2 = aResult[0]
        datetoken = int(getTimer()) * 1000
        
        jsonUrl = 'https://telerium.tv/streams/'+str2+'/'+str(datetoken)+'.json'
        tokens = getRealTokenJson(jsonUrl,iframeURL1)
        m3url = tokens['url']
        nxturl = 'https://telerium.tv' + tokens['tokenurl']
        
    realtoken = getRealTokenJson(nxturl, iframeURL1)[10][::-1]
    
    try:
        m3url = m3url.decode("utf-8")
    except:
        pass

    sHosterUrl = 'https:' + m3url + realtoken

    sHosterUrl += '|User-Agent=' + UA + '&Referer=' + Quote(iframeURL1) + '&Sec-Fetch-Mode=cors&Origin=https://telerium.tv'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oOutputParameterHandler.addParameter('sThumbnail', sThumb)

    # oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + sThumb, oOutputParameterHandler)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('play__')
    oGuiElement.setTitle(sTitle)
    oGuiElement.setFileName(sTitle)
    oGuiElement.setIcon('tv.png')
    oGuiElement.setMeta(0)
    oGuiElement.setThumbnail(sThumb)
    oGuiElement.setDirectTvFanart()
    oGuiElement.setCat(6)

    oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
    oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
    oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')
    oGui.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getRealTokenJson(link, referer):
    cookies = {'ChorreameLaJa': '100',
               'setVolumeSize': '100',
               'NoldoTres': '100'}

    cookies = {'elVolumen': '100',
               '__ga':'100'}

    headers = {'Host': 'telerium.tv',
               'User-Agent': UA,
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': referer}

    realResp = requests.get(link, headers=headers, cookies=cookies, verify=False).content  # [1:-1]

    return json.loads(realResp)

def getTimer():
    datenow = datetime.utcnow().replace(second=0, microsecond=0)
    datenow = datenow + timedelta(days=1)
    epoch = datetime(1970, 1, 1)
        
    return (datenow - epoch).total_seconds() // 1
