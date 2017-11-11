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
import base64
SITE_IDENTIFIER = 'alluc_ee'
SITE_NAME = '[COLOR orange]Alluc.ee[/COLOR]'
SITE_DESC = 'Moteur de recherche alluc'

URL_MAIN = 'http://www.alluc.ee/'

URL_SEARCH = (URL_MAIN + 'stream/lang%3Afr+', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
headers = { 'User-Agent' : UA }
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

def Decrypt(string,key):

    import base64
    import math

    s = base64.b64decode(string)
    i = 0
    sResult = ''
    while i < len(s):
        sChar = s[i:i + 1]
        sKeyChar = key[int(i%len(key)):int(i%len(key) + 1)]
        sChar = int(math.floor(ord(sChar) - ord(sKeyChar)))
        sChar = chr(sChar)
        sResult = sResult + sChar
        i = i + 1

    return sResult

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
        import urllib,urllib2
        post_data = {}
        bb = base64.b64decode(jscode) 
        bb = bb + 'console.log(decrypt("'+aResult.group(1)+'","'+aResult.group(2)+'"));'

        post_data['code'] = bb
        post_data['execute'] = 'on'
        post_data['private'] = 'on'
        post_data['lang'] = 'javascript/node-0.10.29'
        post_data['submit'] = 'Submit'
        request = urllib2.Request('https://eval.in/',urllib.urlencode(post_data),headers)
        reponse = urllib2.urlopen(request)
        sHtmlContent = reponse.read()
        reponse.close()
        
        sPattern = '<h2>Program Output<\/h2>.+?<pre>(.+?)<\/pre>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHosterUrl = aResult[1][0]
           
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
#code encoder en base64    
jscode="ZnVuY3Rpb24gYmFzZTY0X2RlY29kZShyKSB7DQogIHZhciBlOw0KICB2YXIgbjsNCiAgdmFyIGk7DQogIHZhciB0Ow0KICB2YXIgYTsNCiAgdmFyIGQ7DQogIHZhciBvID0gIkFCQ0RFRkdISUpLTE1OT1BRUlNUVVZXWFlaYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXowMTIzNDU2Nzg5Ky89IjsNCiAgdmFyIGYgPSAwOw0KICB2YXIgaCA9IDA7DQogIHZhciBjID0gW107DQogIGlmICghcikgew0KICAgIHJldHVybiByOw0KICB9DQogIHIgKz0gIiI7DQogIGRvIHsNCiAgICBlID0gKGQgPSBvLmluZGV4T2Yoci5jaGFyQXQoZisrKSkgPDwgMTggfCBvLmluZGV4T2Yoci5jaGFyQXQoZisrKSkgPDwgMTIgfCAodCA9IG8uaW5kZXhPZihyLmNoYXJBdChmKyspKSkgPDwgNiB8IChhID0gby5pbmRleE9mKHIuY2hhckF0KGYrKykpKSkgPj4gMTYgJiAyNTU7DQogICAgbiA9IGQgPj4gOCAmIDI1NTsNCiAgICBpID0gMjU1ICYgZDsNCiAgICBjW2grK10gPSA2NCA9PSB0ID8gU3RyaW5nLmZyb21DaGFyQ29kZShlKSA6IDY0ID09IGEgPyBTdHJpbmcuZnJvbUNoYXJDb2RlKGUsIG4pIDogU3RyaW5nLmZyb21DaGFyQ29kZShlLCBuLCBpKTsNCiAgfSB3aGlsZSAoZiA8IHIubGVuZ3RoKTsNCiAgcmV0dXJuIGMuam9pbigiIikucmVwbGFjZSgvXDArJC8sICIiKTsNCn0NCmZ1bmN0aW9uIG9yZChyKSB7DQogIHZhciB0ID0gciArICIiOw0KICB2YXIgZSA9IHQuY2hhckNvZGVBdCgwKTsNCiAgaWYgKGUgPj0gNTUyOTYgJiYgNTYzMTkgPj0gZSkgew0KICAgIHZhciBvID0gZTsNCiAgICByZXR1cm4gMSA9PT0gdC5sZW5ndGggPyBlIDogMTAyNCAqIChvIC0gNTUyOTYpICsgKHQuY2hhckNvZGVBdCgxKSAtIDU2MzIwKSArIDY1NTM2Ow0KICB9DQogIHJldHVybiBlOw0KfQ0KZnVuY3Rpb24gaHRhKHIpIHsNCiAgdmFyIHQgPSByLnRvU3RyaW5nKCk7DQogIHZhciBlID0gIiI7DQogIHZhciBvID0gMDsNCiAgZm9yICg7byA8IHQubGVuZ3RoO28gKz0gMikgew0KICAgIGUgKz0gU3RyaW5nLmZyb21DaGFyQ29kZShwYXJzZUludCh0LnN1YnN0cihvLCAyKSwgMTYpKTsNCiAgfQ0KICByZXR1cm4gZTsNCn0NCmZ1bmN0aW9uIHN0cnJldihyKSB7DQogIHJldHVybiByLnNwbGl0KCIiKS5yZXZlcnNlKCkuam9pbigiIik7DQp9DQpmdW5jdGlvbiBzdHJzd3BjcyhyKSB7DQogIHZhciB0ID0gIiI7DQogIHZhciBlID0gMDsNCiAgZm9yICg7ZSA8IHIubGVuZ3RoO2UrKykgew0KICAgIHQgKz0gcltlXS5tYXRjaCgvXltBLVphLXpdJC8pID8gcltlXSA9PT0gcltlXS50b0xvd2VyQ2FzZSgpID8gcltlXS50b1VwcGVyQ2FzZSgpIDogcltlXS50b0xvd2VyQ2FzZSgpIDogcltlXTsNCiAgfQ0KICByZXR1cm4gdDsNCn0NCmZ1bmN0aW9uIGRlY3J5cHQociwgdCkgew0KICB2YXIgZSA9ICIiOw0KICB2YXIgbyA9IHIuc3Vic3RyaW5nKDAsIDMpOw0KICByID0gci5zdWJzdHJpbmcoMyk7DQogIGlmICgiMzZmIiA9PSBvKSB7DQogICAgciA9IHN0cnJldihiYXNlNjRfZGVjb2RlKHIpKTsNCiAgfSBlbHNlIHsNCiAgICBpZiAoImZjMCIgPT0gbykgew0KICAgICAgciA9IGh0YShzdHJyZXYocikpOw0KICAgIH0gZWxzZSB7DQogICAgICBpZiAoIjY2MyIgPT0gbykgew0KICAgICAgICByID0gYmFzZTY0X2RlY29kZShzdHJyZXYocikpOw0KICAgICAgfSBlbHNlIHsNCiAgICAgICAgaWYgKCI1M2EiID09IG8pIHsNCiAgICAgICAgICByID0gYmFzZTY0X2RlY29kZShzdHJzd3BjcyhyKSk7DQogICAgICAgIH0NCiAgICAgIH0NCiAgICB9DQogIH0NCiAgdmFyIHMgPSAwOw0KICBzID0gMDsNCiAgZm9yICg7cyA8IHIubGVuZ3RoO3MrKykgew0KICAgIHZhciBuID0gci5zdWJzdHIocywgMSk7DQogICAgdmFyIGEgPSB0LnN1YnN0cihzICUgdC5sZW5ndGggLSAxLCAxKTsNCiAgICBuID0gTWF0aC5mbG9vcihvcmQobikgLSBvcmQoYSkpOw0KICAgIGUgKz0gbiA9IFN0cmluZy5mcm9tQ2hhckNvZGUobik7DQogIH0NCiAgcmV0dXJuIGU7DQp9"
