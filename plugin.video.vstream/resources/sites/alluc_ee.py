#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
import re

SITE_IDENTIFIER = 'alluc_ee'
SITE_NAME = '[COLOR orange]Alluc.ee[/COLOR]'
SITE_DESC = 'Moteur de recherche alluc'

URL_MAIN = 'http://www.alluc.ee/'

URL_SEARCH = (URL_MAIN + 'stream/lang%3Afr+', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

# def Decrypt(string,key):

    # import base64
    # import math

    # s = base64.b64decode(string)
    # i = 0
    # sResult = ''
    # while i < len(s):
        # sChar = s[i:i + 1]
        # sKeyChar = key[int(i%len(key)):int(i%len(key) + 1)]
        # sChar = int(math.floor(ord(sChar) - ord(sKeyChar)))
        # sChar = chr(sChar)
        # sResult = sResult + sChar
        # i = i + 1

    # return sResult

def showMovies(sSearch = ''):
    if sSearch:
      sUrl = sSearch
      sSearch = sSearch.replace(' ','+')

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oGui = cGui()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<div class="ifabh clickable" onclick="window.location','')

    #first scan to optimise
    #sPattern = 'onclick="window\.location(.+?)(?:<div class="clickable|<br\/>)'
    sPattern = '<div class="search-result-thumbnail">.*?<img.+?src="//.+?/(thumbnail/[^"]+)".+?class="forstar.+?>([^<]+)</a>.+?<a title="(.+?)".+?href="/([^"]+)".+?<img.+?title="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sthumb = aEntry[0]
            sHost = aEntry[1]
            sCom = aEntry[2]
            sUrl = aEntry[3]
            sFlag = aEntry[4]

            # if len(sthumb) < 2:
                # sthumb = 'put1debug'
            # else:
            sthumb = URL_MAIN + sthumb

            sTitle = re.sub('l\/(.+?)\/.+$','\\1',sUrl)

            sUrl = URL_MAIN + sUrl

            sLang = 'FR'
            if 'vostfr' in sCom or 'vostfr' in sUrl:
                sLang = 'VOSTFR'

            sQual = 'SD'
            if 'HD' in sCom or 'HD' in sUrl:
                sQual = 'HD'

            sDisplaytitle = '[COLOR coral]' + sHost + '[/COLOR] ' + '[B](' + sLang + '/' + sQual + ')[/B] ' + sTitle

            #ne pas l'afficher si host special
            if sHost not in 'freakshare.com':
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sthumb))
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplaytitle, '', sthumb,'', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    sNextPage = __checkForNextPage(sHtmlContent)
    if (sNextPage != False):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a rel="" href="\/([^<>"]+?)"(?: rel=\'next\')*>Next<\/a><\/li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    sHosterUrl = ''
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = "<div class=\"linktitleurl\">.+?decrypt\('(.+?)', *'(.+?)' *\)\)"
    aResult = re.search(sPattern,sHtmlContent,re.DOTALL)
    if aResult:
        sHosterUrl = decrypt(aResult.group(1),aResult.group(2))
        if sHosterUrl:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()

def strrev(r):
    return r[::-1] 
   
def hta(r):
    e = ""
    o = 0
    while o < len(r):
        e += chr(int(r[o:o+2],16))
        o += 2
    return e

def strswpcs(r): 
    t = ""
    e = 0
    while e < len(r):
        f = re.search('[A-Za-z]+',r[e])
        if not f:
            t += r[e]
            e += 1
            continue
        else:    
            t += f.group().upper() if f.group().islower() else f.group().lower()
            e += 1
    return t

    
def decrypt(r, t):
    import math
    import base64

    e = ""
    o = r[0: 3]
    r = r[3:]
    
    if (o == "36f"):
        r = strrev(base64.b64decode(r))
    elif (o == "fc0"):
        r = hta(strrev(r))
    elif (o == "663"): 
        r = base64.b64decode(strrev(r))
    elif (o == "53a"):
        r = base64.b64decode(strswpcs(r))
        
    s = 0
    while s < len(r):
        n = r[s:s+1]
        a = t[s%len(t) - 1: 1]
        n = int(math.floor(ord(n) - ord(a)))
        n = chr(n)
        e += n
        s += 1
    return e
