#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog
from resources.sites.freebox import play__
from resources.lib.util import Quote

from resources.lib.packer import cPacker

import re, base64, requests

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channelstream'
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

    #Double Iframe a passer.
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

    sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern2, sHtmlContent2)

    if aResult:
        str2 = aResult[0]
        if not str2.endswith(';'):
            str2 = str2 + ';'

        strs = cPacker().unpack(str2)

    # Code source https://github.com/yannisKalt/Kodi_Remote_Manager/blob/master/addons/plugin.video.PLsportowo/resources/lib/mydecode.py
    mainurlliczbacdurl=re.findall('url:\s*window\.atob\((.+?)\).slice\((.+?)\)\s*\+\s*window.atob\((.+?)\)',strs)[0]
    mainurl=mainurlliczbacdurl[0]
    liczba=mainurlliczbacdurl[1]
    cdurl=mainurlliczbacdurl[2]
    mainurlpattern=(mainurl+"""\=['"](.+?)['"]""")
    liczbapattern=(liczba+'\=(\d+)')
    cdurlpattern=(cdurl+"""\=['"](.+?)['"]""")
    
    murl=re.findall(mainurlpattern,strs)[0]
    licz=re.findall(liczbapattern,strs)[0]
    curl=re.findall(cdurlpattern,strs)[0]

    d1=(base64.b64decode(murl))[int(licz):]

    d2=base64.b64decode(curl)
    basurl='https://telerium.tv'
    
    m3url=re.findall('{if\(esMobiliar\){(.+?)=.+?};function',strs)[0]
    m3url=base64.b64decode(re.findall(m3url+"""=['"](.+?)['"]""",strs)[0])

    speechx=re.findall("""}else\{(.+?)\=dameVuelta\((.+?)\[(.+?)]\);""",strs)[0][2]
    
    sppech = re.findall(speechx+'=(.+?)([-+])(.+?);',strs)[0]
    reg1 = sppech[0]+'=(.+?)([-+])(.+?);'
    reg2 = sppech[2]+'=(.+?)([-+])(.+?);'
    
    ob1 =re.compile(reg1).findall(strs)
    ob2 =re.compile(reg2).findall(strs)
    
    ob11 = re.compile('var '+ob1[0][0]+'=(.+?);').findall(strs)
    ob12 = re.compile('var '+ob1[0][2]+'=(.+?);').findall(strs)
    
    ob21 = re.compile('var '+ob2[0][0]+'=(.+?);').findall(strs)
    ob22 = re.compile('var '+ob2[0][2]+'=(.+?);').findall(strs)
    
    
    obliczob1 = eval('%s%s%s'%(ob11[0],ob1[0][1],ob12[0]))
    obliczob2 = eval('%s%s%s'%(ob21[0],ob2[0][1],ob22[0]))
    spech = eval('%s%s%s'%(obliczob1,sppech[1],obliczob2))

    try:
        d1 = d1.decode('utf-8')
        d2 = d2.decode('utf-8')
    except:
        pass

    nxturl=basurl+d1+d2

    realtoken = getRealToken(nxturl, iframeURL1, spech)

    try:
        m3url = m3url.decode("utf-8")
    except:
        pass

    sHosterUrl = 'https:'+m3url+realtoken

    sHosterUrl+='|User-Agent='+UA+'&Referer='+Quote(iframeURL1)+'&Sec-Fetch-Mode=cors&Origin=https://telerium.tv'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oOutputParameterHandler.addParameter('sThumbnail', sThumb)

    #oGui.addDirectTV(SITE_IDENTIFIER, 'play__', track.title, 'tv.png' , sRootArt + '/tv/' + sThumb, oOutputParameterHandler)

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
    oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def getRealToken(link, referer,spech):
    cookies = {
        'ChorreameLaJa': '100',
        'setVolumeSize': '100',
        'NoldoTres': '100',
    }
    
    cookies = {
        'elVolumen': '100',
    }
    
    headers = {
        'Host': 'telerium.tv',
        'User-Agent': UA,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': referer,
    }
    
    realResp = requests.get(link, headers=headers,cookies=cookies,verify=False).content#[1:-1]
    
    realResp=re.findall('"(.+?)"',str(realResp))[spech]  

    return realResp[::-1]   
