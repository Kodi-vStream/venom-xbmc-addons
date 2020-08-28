# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import base64
import re
import requests
import json


from resources.lib.comaddon import progress, VSlog
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.sites.freebox import play__
from resources.lib.util import Quote
from datetime import datetime, timedelta

#import web_pdb;

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channel Stream'
SITE_DESC = 'iptv'

URL_MAIN = 'https://channelstream.me'

TV_FRENCH = (URL_MAIN + "/chaine-tv.php", 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TV_FRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, TV_FRENCH[1], 'Chaine Francaise', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>', '')

    sPattern = 'location.href = \'\.(.+?)\'.+?src=\'(.+?)\'.+?<div align="center">(.+?)</div>'

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

            if not str(aEntry[2]) == "Dorcel TV":
                sTitle = aEntry[2]
                sUrl2 = URL_MAIN + aEntry[0]
                sThumb = URL_MAIN + '/' + aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addDir(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, oOutputParameterHandler)

        progress_.VSclose(progress_)

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
    iframeURL1 = oParser.parse(sHtmlContent, sPattern)[1][0]

    oRequestHandler = cRequestHandler(iframeURL1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', iframeURL)
    sHtmlContent2 = oRequestHandler.request()

    sPattern2 = 'var cid = \'([0-9]+)\';'
    aResult = re.findall(sPattern2, sHtmlContent2)
    #VSlog(sHtmlContent2)



    if aResult:
        str2 = aResult[0]
        VSlog(str2)
        datetoken = int(getTimer()) * 1000
        
        jsonUrl = 'https://telerium.tv/streams/'+str2+'/'+str(datetoken)+'.json'
        VSlog(jsonUrl)
        tokens = getRealTokenJson(jsonUrl,iframeURL1)
        m3url = tokens['url']
        nxturl = 'https://telerium.tv' + tokens['tokenurl']
          #web_pdb.set_trace()

        
    realtoken = getRealTokenJson(nxturl, iframeURL1)[10][::-1]
    
    #web_pdb.set_trace()

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

    #web_pdb.set_trace()
    
    return json.loads(realResp)

def getTimer():
    datenow = datetime.utcnow().replace(second=0, microsecond=0)
    datenow = datenow + timedelta(days=1)
    epoch = datetime(1970, 1, 1)
        
    return (datenow - epoch).total_seconds() // 1
