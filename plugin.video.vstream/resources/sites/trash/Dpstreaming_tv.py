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
from resources.lib.util import cUtil
import re, urllib, urllib2
import xbmcgui,xbmc
#from time import time
#from base64 import urlsafe_b64encode
import htmlentitydefs,unicodedata
 
SITE_IDENTIFIER = 'dpstreaming_tv'
SITE_NAME = 'DPStreaming.tv'
SITE_DESC = 'Streaming ou Telechargement films series mangas gratuitement et sans limite'
 
URL_MAIN = 'http://dpstreaming.tv/'
 
MOVIE_NEWS = ('http://dpstreaming.tv/category/films/', 'showMovies')
MOVIE_VIEWS = ('http://dpstreaming.tv/category/films-en-exclus/', 'showMovies')
SERIE_SERIES = ('http://dpstreaming.tv/category/series-tv/', 'showMovies')
ANIM_ANIMS = ('http://dpstreaming.tv/category/mangas/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
REPLAYTV_REPLAYTV = ('http://dpstreaming.tv/category/emissions-tv/', 'showMovies')
SPORT_SPORTS = ('http://dpstreaming.tv/category/sport/', 'showMovies')
DOC_DOCS = ('http://dpstreaming.tv/category/films/documentaire/', 'showMovies')
 
URL_SEARCH = ('http://dpstreaming.tv/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
 
#Cette fonction n'est pas encore utilisÃ©e, servira le jour ou dl-protect re-activera le captcha
# def get_response(img):
    # try:
        # img = xbmcgui.ControlImage(450, 0, 400, 130, img)
        # wdlg = xbmcgui.WindowDialog()
        # wdlg.addControl(img)
        # wdlg.show()
        # #xbmc.sleep(3000)
        # kb = xbmc.Keyboard('', 'Type the letters in the image', False)
        # kb.doModal()
        # if (kb.isConfirmed()):
            # solution = kb.getText()
            # if solution == '':
                # raise Exception('You must enter text in the image to access video')
            # else:
                # return solution
        # else:
            # raise Exception('Captcha Error')
    # finally:
        # wdlg.close()
 
       
def DecryptDlProtect(url):
    if not (url): return ''
   
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Referer' : url ,
    'Host' : 'www.dl-protect.com',
    #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-gb, en;q=0.9',
    'Pragma' : '',
    'Accept-Charset' : '',
    }
   
    request = urllib2.Request(url,None,headers)
    try:
        reponse = urllib2.urlopen(request)
    except URLError, e:
        print e.read()
        print e.reason
       
    sHtmlContent = reponse.read()
   
    #Recuperatioen et traitement cookies ???
    cookies=reponse.info()['Set-Cookie']
    c2 = re.findall('__cfduid=(.+?); .+? cu=(.+?);.+?PHPSESSID=(.+?);',cookies)
    cookies = '__cfduid=' + str(c2[0][0]) + ';cu=' + str(c2[0][1]) + ';PHPSESSID=' + str(c2[0][2])
   
    reponse.close()
       
    key = re.findall('input name="key" value="(.+?)"',sHtmlContent)
   
    #Ce parametre ne sert pas encore pour le moment
    #mstime = int(round(time() * 1000))
    b64time = ''#"_" + urlsafe_b64encode(str(mstime)).replace("=", "%3D")
 
    if 'Please click on continue to see' in sHtmlContent:
        #tempo necessaire
        xbmc.sleep(1000)
       
        query_args = ( ('submitform' , '' ) , ( 'key' , key[0] ) , ('i' , b64time ), ( 'submitform' , 'Continuer')  )
        data = urllib.urlencode(query_args)
        #print data
       
        #rajout des cookies
        headers.update({'Cookie': cookies})
        #print headers
 
        request = urllib2.Request(url,data,headers)
 
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
           
        sHtmlContent = reponse.read()
       
        reponse.close()
       
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
   
    return sHtmlContent
       
 
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
       
       
       
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films NouveautÃ©s', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vus', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showAZ', 'Series A-Z', 'az.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Mangas', 'animes.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Replay tv', 'tv.png', oOutputParameterHandler)
   
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://dpstreaming.tv/?s='+sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["0-9","http://dpstreaming.tv/category/series-tv/0-9/"] )
    liste.append( ["A-B-C","http://dpstreaming.tv/category/series-tv/a-b-c/"] )
    liste.append( ["D-E-F","http://dpstreaming.tv/category/series-tv/d-e-f/"] )
    liste.append( ["G-H-I","http://dpstreaming.tv/category/series-tv/g-h-i/"] )
    liste.append( ["J-K-L","http://dpstreaming.tv/category/series-tv/j-k-l/"] )
    liste.append( ["M-N-O","http://dpstreaming.tv/category/series-tv/m-n-o/"] )
    liste.append( ["P-Q-R","http://dpstreaming.tv/category/series-tv/p-q-r/"] )
    liste.append( ["S-T-U","http://dpstreaming.tv/category/series-tv/s-t-u/"] )
    liste.append( ["V-W-X-Y-Z","http://dpstreaming.tv/category/series-tv/v-w-x-y-z/"] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'az.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
   
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://dpstreaming.tv/category/films/action/'] )
    liste.append( ['Animation','http://dpstreaming.tv/category/films/animation/'] )
    liste.append( ['Arts Martiaux','http://dpstreaming.tv/category/films/arts-martiaux/'] )
    liste.append( ['Aventure','http://dpstreaming.tv/category/films/aventure-films/'] )
    liste.append( ['Biopic','http://dpstreaming.tv/category/films/biopic/'] )
    liste.append( ['Comedie','http://dpstreaming.tv/category/films/comedie/'] )
    liste.append( ['Comedie Dramatique','http://dpstreaming.tv/category/films/comedie-dramatique/'] )
    liste.append( ['Documentaire','http://dpstreaming.tv/category/films/documentaire/'] )
    liste.append( ['Drame','http://dpstreaming.tv/category/films/drame/'] )
    liste.append( ['Espionnage','http://dpstreaming.tv/category/films/espionnage/'] )  
    liste.append( ['Famille','http://dpstreaming.tv/category/films/famille/'] )
    liste.append( ['Fantastique','http://dpstreaming.tv/category/films/fantastique/'] )
    liste.append( ['Guerre','http://dpstreaming.tv/category/films/guerre/'] )
    liste.append( ['Historique','http://dpstreaming.tv/category/films/historique/'] )
    liste.append( ['Horreur','http://dpstreaming.tv/category/films/horreur/'] )
    liste.append( ['Musical','http://dpstreaming.tv/category/films/musical/'] )
    liste.append( ['Policier','http://dpstreaming.tv/category/films/policier/'] )
    liste.append( ['Romance','http://dpstreaming.tv/category/films/romance/'] )
    liste.append( ['Science-Fiction','http://dpstreaming.tv/category/films/science-fiction/'] )
    liste.append( ['Spectacle','http://dpstreaming.tv/category/films/spectacle/'] )
    liste.append( ['Thriller','http://dpstreaming.tv/category/films/thriller/'] )
    liste.append( ['Western','http://dpstreaming.tv/category/films/western/'] )
    liste.append( ['VOSTFR','http://dpstreaming.tv/category/films/vostfr-films/'] )
    liste.append( ['Bluray','http://dpstreaming.tv/category/films/bluray-1080p-720p/'] )
    liste.append( ['Bluray 3D','http://dpstreaming.tv/category/films/bluray-3d/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
 
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('[Streaming]', '').replace('[Telecharger]', '')
    sPattern = '<img width=".+?" height=".+?" src="([^<]+)" class="postim wp-post-image".+?<h2><a href="([^<]+)" rel="bookmark" .+?>([^<]+)</a></h2></div>.+?<p>(.+?)</p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
       
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = unicode(aEntry[2], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")
           
            sMovieTitle=re.sub('(\[.*\])','', sTitle)
           
            sTitle=re.sub('(.*)(\[.*\])','\\1 [COLOR azure]\\2[/COLOR]', sTitle)
           
 
            sCom = unicode(aEntry[3], 'utf-8')#converti en unicode
            sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
            sCom = unescape(sCom)
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
           
            #Mange et Series fonctionnent pareil
            if '/series-tv/' in sUrl or 'saison' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)
            elif '/mangas/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)
       
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    #Nettoyage du code, a simplifier, mais je trouve pas ce qui ne va pas
    sHtmlContent = sHtmlContent.decode('utf-8',"replace")
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sHtmlContent = sHtmlContent.encode('utf-8')#On remet en utf-8
   
    sHtmlContent = sHtmlContent.replace('<strong>Telechargement VOSTFR','').replace('<strong>Telechargement VF','').replace('<strong>Telechargement','')
    sHtmlContent = sHtmlContent.replace('<a href="http://www.multiup.org','')
    sHtmlContent = sHtmlContent.replace('<iframe src="http://ads.affbuzzads.com','')
    sHtmlContent = sHtmlContent.replace('<iframe src="//ads.ad-center.com','')
 
    #sPattern = '<span style="color: #33cccc;"><strong>([^<]+)|>(Episode[^<]{2,12})<(?!\/a>)(.+?)(?:<.p|<br|<.div)'
    sPattern = '<span style="color: #33cccc;"><strong>([^<]+)|>(Episode[^<]{2,12})<(?!\/a>)(.{0,10}a href="http.+?)(?:<.p|<br|<.div)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    #astuce en cas d'episode unique
    if (aResult[0] == False):
        #oGui.setEndOfDirectory()
        showHosters()
        return;
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sTitle = sMovieTitle+' - '+aEntry[1]
               
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
 
    return False
   
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="http://ads.affbuzzads.com','')
    sHtmlContent = sHtmlContent.replace('<iframe src="//ads.ad-center.com','')
 
    sPattern = '<a.+? (:?data-blogger-es="")>.+?</a>|<iframe src="([^<]+)" frameborder'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[1][0][0] == 'data-blogger-es=""'):
        showSeries()
               
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sHosterUrl = str(aEntry[1])
 
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
       
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
   
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oParser = cParser()
   
    liste = False
   
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
   
 
    if 'dl-protect.com' in sUrl:
        sPattern = 'href="([^<]+)" target="_blank.+?>(.+?)<.a>'
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
           
            UrlList =''
            vid_list = []
            hoster_list = []
     
            if len(aResult[1]) > 1:
                for i in aResult[1]:
                    vid_list.extend([i[0]])
                    hoster_list.extend([i[1]])
            if len(aResult[1]) == 1:
                UrlList = aResult[1][0][0]
            else:
                result = xbmcgui.Dialog().select('Choose a link list', hoster_list)
                if result != -1:
                    UrlList = vid_list[result]
 
            if (UrlList):  
                sHtmlContent = DecryptDlProtect(UrlList)
                if sHtmlContent:
                   
                    sPattern = '<br .><a href="(.+?)" target="_blank">http:.+?<.a>'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    liste = True
            else:
                return
    else:
        sPattern = 'href="([^<]+)" target="_blank".+?</a>'
        aResult = oParser.parse(sUrl, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        index = 1
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = sMovieTitle
            if liste:
                sTitle = sTitle + ' (' + str(index) + ') '
                index = index + 1
            #print aEntry
            sHosterUrl = str(aEntry)
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
