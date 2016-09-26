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
from resources.lib.config import cConfig
import re, urllib
import urllib2


SITE_IDENTIFIER = 'filmenstreaminghd_com'
SITE_NAME = 'filmenstreaminghd'
SITE_DESC = 'Films/Series/Animes en streaming'


URL_MAIN = 'http://www.filmenstreaminghd.com'


MOVIE_MOVIE = (URL_MAIN + '/films', 'showMovies')
MOVIE_NEWS = (URL_MAIN + '/derniers-ajoutes' , 'showMovies')
MOVIE_HD = (URL_MAIN + '/1080p-films', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + '/films-populaires/', 'showMovies')
#MOVIE_COMMENTS = (URL_MAIN + 'les-plus-commentes/', 'showMovies')
#MOVIE_NOTES = (URL_MAIN + '/films-populaires/', 'showMovies')
MOVIE_GENRES = ('http://venom', 'showGenre')

SERIE_SERIES = (URL_MAIN + '/series-tv', 'showMovies')
SERIE_GENRES = ('http://venom', 'showGenreS')
#SERIE_NEWS = (URL_MAIN + 'tv-series/', 'showMovies')

ANIM_ANIMS = (URL_MAIN +'/animes', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'




#-------------------------------------------------
#Partie speciale pour contourner le DNS ban

#import httplib
#import socket

#def MyResolver(host):
#    if host == 'frenchstream.tv':
#        return '154.46.33.11'
#    else:
#        return host
#
#class MyHTTPConnection(httplib.HTTPConnection):
#    def connect(self):
#        self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)
#
#class MyHTTPHandler(urllib2.HTTPHandler):
#    def http_open(self,req):
#        return self.do_open(MyHTTPConnection,req)
#        
#def GetHtmlViaDns(url,postdata = None):
#    opener = urllib2.build_opener(MyHTTPHandler)
#    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
#    urllib2.install_opener(opener)
#
#    f = urllib2.urlopen(url,postdata)
#    sHtmlContent = f.read()
#    f.close()
#    
#    return sHtmlContent
        
#---------------------------------------------------




def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Vues', 'films.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Commentés', 'films.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les mieux Notés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films Qualités', 'films.png', oOutputParameterHandler)
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '?s='+sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre():
    oGui = cGui()
    #oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',URL_MAIN+ '/action'] )
    liste.append( ['Animation',URL_MAIN + '/animation'] )
    liste.append( ['Aventure',URL_MAIN + '/aventure'] )
    liste.append( ['Biographie',URL_MAIN + '/biographie'] )
    liste.append( ['Comédie',URL_MAIN + '/comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/comedie-dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + '/documentaire'] )
    liste.append( ['Drame',URL_MAIN + '/drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/epouvante-horreur'] )
    liste.append( ['Familial',URL_MAIN + '/familial'] )
    liste.append( ['Fantastique',URL_MAIN + '/fantastique'] )
    liste.append( ['Histoire',URL_MAIN + '/histoire'] )
    liste.append( ['Musical',URL_MAIN + '/musical'] )
    liste.append( ['Mystère',URL_MAIN + '/mystere'] )
    liste.append( ['Policier',URL_MAIN + '/policier-crime'] )
    liste.append( ['Romance',URL_MAIN + '/romance'] )
    liste.append( ['Sciense Fiction',URL_MAIN + '/science-fiction'] )
    liste.append( ['Thriller',URL_MAIN + '/thriller'] )
    liste.append( ['Western',URL_MAIN + '/western'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
    
def showGenreS():
    oGui = cGui()
    #oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',URL_MAIN+ '/action-series'] )    
    liste.append( ['Action-Aventure',URL_MAIN + '/action-adventure-series'] )
    liste.append( ['Animation',URL_MAIN + '/animation-series'] )
    liste.append( ['Aventure',URL_MAIN + '/aventure-series'] )
    liste.append( ['Biographie',URL_MAIN + '/biographie-series'] )    
    liste.append( ['Comédie',URL_MAIN + '/comedie-series'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/comedie-dramatique-series'] )
    liste.append( ['Documentaire',URL_MAIN + '/documentaire-series'] )
    liste.append( ['Drame',URL_MAIN + '/drame-series'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/epouvante-horreur-series'] )
    liste.append( ['Familial',URL_MAIN + '/familial-series'] )
    liste.append( ['Fantastique',URL_MAIN + '/fantastique-series'] )
    liste.append( ['Histoire',URL_MAIN + '/histoire-series'] )
    liste.append( ['Musical',URL_MAIN + '/musical-series'] )
    liste.append( ['Mystère',URL_MAIN + '/mystere-series'] )
    liste.append( ['Policier',URL_MAIN + '/policier-crime-series'] )
    liste.append( ['Romance',URL_MAIN + '/romance-series'] )
    liste.append( ['Sciense Fiction',URL_MAIN + '/science-fiction-series'] )
    liste.append( ['Sciense Fiction - fantastique',URL_MAIN + '/science-Fiction-fantastique-series'] )
    liste.append( ['Thriller',URL_MAIN + '/thriller-series'] )
    liste.append( ['Western',URL_MAIN + '/western-series'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showQlt():
    oGui = cGui()
    #oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['1080p',URL_MAIN + '/1080p-films'] )   
    liste.append( ['720p',URL_MAIN + '/720p-films'] )
    # liste.append( ['BDRip',URL_MAIN + 'qualites/BDRip/'] )
    # liste.append( ['BRRip',URL_MAIN + 'qualites/BRRip/'] )
    # liste.append( ['CAMRip',URL_MAIN + 'qualites/CAMRip/'] )
    # liste.append( ['DVDRip',URL_MAIN + 'qualites/DVDRip/'] )
    # liste.append( ['DVDSCR',URL_MAIN + 'qualites/DVDSCR/'] )
    # liste.append( ['HDRip',URL_MAIN + 'qualites/HDRip/'] )
    # liste.append( ['HDTV',URL_MAIN + 'qualites/HDTV/'] )
    # liste.append( ['PDTV',URL_MAIN + 'qualites/PDTV/'] )
    # liste.append( ['R6',URL_MAIN + 'qualites/R6/'] )
    # liste.append( ['TS MD',URL_MAIN + 'qualites/ts-md/'] )
    # liste.append( ['TVRip',URL_MAIN + 'qualites/TVRip/'] )
    # liste.append( ['VHSRip',URL_MAIN + 'qualites/VHSRip/'] )
    # liste.append( ['VOBRIP',URL_MAIN + 'qualites/VOBRIP/'] )
    # liste.append( ['WEB-DL',URL_MAIN + 'qualites/web-dl/'] )
    # liste.append( ['WEBRIP',URL_MAIN + 'qualites/WEBRIP/'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
        
    
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
            
    if sSearch:
        sUrl = sSearch.replace(' ','+')
        
        sDisp = oInputParameterHandler.getValue('disp')
       
        if (sDisp == 'search3'):#anime
            sUrl = sUrl + '&cat_id=45477'
        elif (sDisp == 'search2'):#serie
            sUrl = sUrl + '&cat_id=16989'
        elif (sDisp == 'search1'):#film
            sUrl = sUrl + '&cat_id=1'   
        else:#tout le reste
            sUrl = sUrl
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="film-k.+?<a href="([^<"]+)".+?<div class="kalite">([^<"]+).+?<img src="([^<"]+).+?<div class="baslik">([^<"]+).+?<div class="aciklama">([^<"]+)'
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
            
            sTitle = aEntry[3]
            if aEntry[1]:
                sTitle = sTitle + '[' + aEntry[1]  + '] ' 
            sCom = aEntry[4]
            sUrl2 = URL_MAIN + '/' + aEntry[0]
            sThumb = URL_MAIN + '/' + aEntry[2]
            
            
            sCom = cUtil().removeHtmlTags(sCom)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if '/series/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showMovies', sDisplayTitle,'', sThumb, sCom, oOutputParameterHandler)
            elif '/animes/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle,'', sThumb, sCom, oOutputParameterHandler)
            elif '/series-saison/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle,'', sThumb, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'films.png', sThumb, sCom, oOutputParameterHandler)           
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            import xbmc
            sUrl = re.sub('\/page-[0-9]','',sUrl)
            xbmc.log(sUrl+'/'+sNextPage)
            oOutputParameterHandler.addParameter('siteUrl', sUrl+'/'+sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #sHtmlContent = GetHtmlViaDns(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<li><a href="([^<>"]+?)" (?:class="active")*><i class="fa fa-film"><\/i>(.+?)<span><\/span><\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[1] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
def __checkForNextPage(sHtmlContent):
    
    sPattern = '<a class="sonraki-sayfa" href="(?:/.+?/|)(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False
    
  
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #sHtmlContent = GetHtmlViaDns(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    
    oParser = cParser()
    sPattern = '<a class="partsec" id="([^"]+)".+?</span>([^<]+)<span'
    #sPattern='<div id="burayaclass".+?onclick="getirframe\(\'(.+?)\',\'(.+?)\'\)".+?<div class="col-md-4.+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[1] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',  sUrl)
            oOutputParameterHandler.addParameter('sPid',  aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sPid = oInputParameterHandler.getValue('sPid')

    postdata = 'pid=' + sPid
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0' }
    request = urllib2.Request(sUrl,postdata,headers)
    reponse = urllib2.urlopen(request)
    sHtmlContent = reponse.read()
    reponse.close()
    
    # fh = open('D:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()
    
    sPattern = '<ifram[^<>]+? src=[\'"]([^\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl =  str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showHosters2():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #sHtmlContent = GetHtmlViaDns(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src="http://www.facebook.com/','')
    #sHtmlContent = sHtmlContent.replace('http://videomega.tv/validateemb.php','')
    #sHtmlContent = sHtmlContent.replace('src="http://frenchstream.org/','')
    
    sPattern = '(?:(?:<script type="text\/javascript")|(?:<ifram[^<>]+?)) src=[\'"](https*:[^\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #sHtmlContent = GetHtmlViaDns(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close() 
 
    sPattern = '<li style="[^<>]+?"><a href="([^<>"]+?)">(.+?)<\/a><\/li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle+' - ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
