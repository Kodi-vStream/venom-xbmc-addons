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
import urllib, urllib2
import re, os, time
import xbmc,xbmcgui,xbmcaddon

SITE_IDENTIFIER = 'ddl_island_su'
SITE_NAME = '[COLOR violet]DDL-Island[/COLOR]'
SITE_DESC = 'DDL Island'
URL_MAIN = 'http://www.ddl-island.su/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'movieSearch', 'Recherche films', 'search.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche séries', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def movieSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_MAIN+'recherche.php?categorie=99&fastr_type=ddl&find=' + urllib.quote(sSearchText)
        showMovies(sUrl)

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_MAIN+'recherche.php?categorie=98&fastr_type=ddl&find=' + urllib.quote(sSearchText)
        showMovies(sUrl)

def showMovies(sUrl=None, page=1):
    oGui = cGui()
    if sUrl == None:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('sUrl')
        page = oInputParameterHandler.getValue('page')

    searchUrl = sUrl
    oRequestHandler = cRequestHandler(sUrl+'&start='+str(page))
    sHtmlContent = oRequestHandler.request()

    sPattern = '(<div class="fiche_listing">.+?titre_fiche"><img src=".+?".+?>(.+?)<.+?<\/div>)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        for aEntry in aResult[1]:
            entry = aEntry[0]

            # Entry title
            sQuality = ''
            result = re.search('Qualité : (.+?)<', entry)
            if result:
                sQuality = result.group(1)

            sTitle = str(aEntry[1])
            sDisplaytitle = sTitle.strip(' []-')
            if sQuality:
                sDisplaytitle = '[COLOR blue][' + sQuality + '][/COLOR] ' + sDisplaytitle

            # HD?
            result = re.search('hd.png"', entry)
            if result:
                sDisplaytitle = '[COLOR blue][HD][/COLOR]' + sDisplaytitle

            # Entry URL
            sUrl = ''
            result = re.search('href="(http:\/\/.+?).html"', entry)
            if result:
                sUrl = result.group(1)

            # Thumb
            sThumb = ''
            result = re.search('<img src="(.+?)"', entry)
            if result:
                sThumb = result.group(1)

            if sUrl:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumb))
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, '', sThumb,'', oOutputParameterHandler)

    nextPage = 'start=%d"' % (int(page)+1)
    result = re.search(nextPage, sHtmlContent)
    if result:
        oOutputParameterHandler.addParameter('sUrl', str(searchUrl))
        oOutputParameterHandler.addParameter('page', str(int(page)+1))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<TR><TD COLSPAN=(.+?)<tr>(<td bg.+?)<\/tr>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        for aEntry in aResult[1]:
            entry = aEntry[0]
            title = ''
            labels = ['720p', '1080p', 'ac3', 'truefrench', 'x265']
            for label in labels:
                result = re.search(label+'.png', entry)
                if result:
                    title += ' - ' + label.upper()

            blockTitle = sTitle
            result = re.search('15px;\'>-(.+?)<', entry)

            if result:
                blockTitle = result.group(1)
            blockTitle = blockTitle.strip(' []-')
            oGui.addText(SITE_IDENTIFIER, blockTitle + '[COLOR teal]'+title+'[/COLOR]')

            sProvider = '<li(.+?)<span class=\'providers (.+?)\'(.+?)href=\'(.+?)\'(.+?)</li>'
            aProviders = oParser.parse(aEntry[1], sProvider)
            if aProviders[0] == True:
                for aProvider in aProviders[1]:
                    provider = aProvider[1].title()
                    protected = aProvider[3]
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', str(protected))
                    oOutputParameterHandler.addParameter('thumb', str(sThumbnail))
                    oOutputParameterHandler.addParameter('provider', str(provider))
                    oGui.addMisc(SITE_IDENTIFIER, 'showProtected', '[COLOR blue]'+provider+'[/COLOR]', '', '','', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showProtected():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    thumb = oInputParameterHandler.getValue('thumb')
    provider = oInputParameterHandler.getValue('provider')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url = captcha(sUrl)
    oHoster = cHosterGui().checkHoster(url)
    if oHoster != False:
        oHoster.setDisplayName(provider)
        cHosterGui().showHoster(oGui, oHoster, url, thumb)
        oGui.setEndOfDirectory()

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))

def captcha(url):
    # Other-ing the URL
    result = re.search('/([^/]+?)$', url)
    if result:
        url = 'http://protect.ddl-island.su/other?id='+result.group(1)

    # Sending the request
    request = urllib2.Request('http://protect.ddl-island.su/securimage/securimage_show.php?'+str(time.time()))
    response = urllib2.urlopen(request,timeout = 5)

    cookies = response.info()['Set-Cookie']
    c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',cookies)
    cookies = ''
    for cook in c2:
        cookies = cookies + cook[0] + '=' + cook[1]+ ';'
    cookies = cookies.strip()

    png = response.read()
    response.close()

    name = 'captcha-%s.png' % time.time()
    filename  = os.path.join(PathCache, name)
    o = open(filename, 'w')
    o.write(png)
    o.close()

    img = xbmcgui.ControlImage(450, 0, 400, 130, filename)
    wdlg = xbmcgui.WindowDialog()
    wdlg.addControl(img)
    wdlg.show()
    kb = xbmc.Keyboard('', 'Recopiez le code', False)
    kb.doModal()
    if kb.isConfirmed():
        captcha = kb.getText()

        headers = {
            'Cookie': cookies,
            'Content-Type' : 'application/x-www-form-urlencoded'
            }

        request = urllib2.Request(url, 'submit=Submit form&captcha_code='+captcha, headers)
        response = urllib2.urlopen(request,timeout = 5)
        html = response.read()
        response.close()

        result = re.search('<td><a href="(.+?)"', html)
        if result:
            return result.group(1)
    return ''
