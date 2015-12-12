#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui #system de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #system de recherche pour l'hote
from resources.lib.gui.gui import cGui #system d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #system d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entrer des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortis des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code
from resources.lib.util import cUtil
import re

#from resources.lib.sucuri import SucurieBypass
import os,urllib2,urllib,xbmc,xbmcaddon,base64
 
SITE_IDENTIFIER = 'film_illimit_fr' #identifant nom de votre fichier remplacer les espaces et les . par _ aucun caractere speciale
SITE_NAME = 'Film Illimit' # nom que xbmc affiche
SITE_DESC = 'Films/Series HD en streaming' #description courte de votre source
 
URL_MAIN = 'http://xn--official-film-illimit-v5b.fr/' # url de votre source

MOVIE_NEWS = ('http://xn--official-film-illimit-v5b.fr/film-de-a-a-z/', 'showMovies')
MOVIE_MOVIE = (True, 'showAlpha')
MOVIE_GENRES = (True, 'showGenre')

#SERIE_SERIES = ('http://official-film-illimité.fr/serie-tv/', 'showMovies')
  
URL_SEARCH = ('http://xn--official-film-illimit-v5b.fr/?s=', 'showMovies')
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films A-Z', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films par Genres', 'genres.png', oOutputParameterHandler)
    
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries', 'series.png', oOutputParameterHandler)
    
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://xn--official-film-illimit-v5b.fr/?s='+sSearchText 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
            
   
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action','http://xn--official-film-illimit-v5b.fr/action-aventure/'] )
    liste.append( ['Animation','http://xn--official-film-illimit-v5b.fr/animation/'] )
    liste.append( ['Arts Martiaux','http://xn--official-film-illimit-v5b.fr/arts-martiaux/'] )
    liste.append( ['Biographie','http://xn--official-film-illimit-v5b.fr/biographique/'] )
    liste.append( ['Comedie','http://xn--official-film-illimit-v5b.fr/comedie/'] )
    liste.append( ['Drame','http://xn--official-film-illimit-v5b.fr/drame/'] )
    liste.append( ['Epouvante Horreur','http://xn--official-film-illimit-v5b.fr/epouvante-horreur/'] )
    liste.append( ['Fantastique','http://xn--official-film-illimit-v5b.fr/fantastique/'] )  
    liste.append( ['Famille','http://xn--official-film-illimit-v5b.fr/famille/'] )
    liste.append( ['Guerre','http://xn--official-film-illimit-v5b.fr/guerre/'] )
    liste.append( ['Policier','http://xn--official-film-illimit-v5b.fr/policier/'] )
    liste.append( ['Romance','http://xn--official-film-illimit-v5b.fr/romance/'] )
    liste.append( ['Science Fiction','http://xn--official-film-illimit-v5b.fr/science-fiction/'] )
    liste.append( ['Thriller/Suspense','http://xn--official-film-illimit-v5b.fr/thrillersuspense/'] )
    liste.append( ['720p/1080p','http://xn--official-film-illimit-v5b.fr/720p1080p/'] )
    liste.append( ['Mystère','http://xn--official-film-illimit-v5b.fr/mystere/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0,27) :
        cConfig().updateDialog(dialog, 27)
        if dialog.iscanceled():
            break
        
        sTitle = chr(64+i)
        sUrl = 'http://xn--official-film-illimit-v5b.fr/film-de-a-a-z/lettre-' + chr(96+i) + '/'
        
        if sTitle == '@':
            sTitle= '[0-9]'
            sUrl = 'http://xn--official-film-illimit-v5b.fr/film-de-a-a-z/0-9/'
          
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addTV(SITE_IDENTIFIER, 'showMovies','[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]','', '', '', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sSearch = sSearch.replace(' ','+')
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    sPattern = '<div class="item"><a href="([^<]+)">.+?<img src="(.+?)" alt="(.+?)" />.+?<span class="calidad2">(.+?)</span>'
    #sPattern = '<div class="item">.*<a href="([^<]+)">.+?<img src="(.+?)" alt="(.+?)" \/>.+?<span class="calidad2">(.+?)<\/span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
                
            sName = aEntry[2].replace(' en Streaming HD','')
            sName = sName.replace(' Streaming HD','')
            sName = cUtil().unescape(sName)
            try:
                sName = sName.encode("utf-8")
            except:
                pass
            
            sTitle = sName + ' [COLOR coral] ' + aEntry[3] + '[/COLOR]'
            sUrl = aEntry[0].replace('http://official-film-illimité.fr', 'http://xn--official-film-illimit-v5b.fr')
            sThumbnail = aEntry[1].replace('http://official-film-illimité.fr', 'http://xn--official-film-illimit-v5b.fr')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', sName)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            
            if re.match('.+?saison [0-9]+',sTitle,re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumbnail,'', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage
   
def __checkForNextPage(sHtmlContent): #cherche la page suivante
    sPattern = "<span class='current'>.+?</span><a rel='nofollow' class='page larger' href='(.+?)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        next = aResult[1][0].replace('http://official-film-illimité.fr', 'http://xn--official-film-illimit-v5b.fr')
        return next
 
    return False
 
def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    sHtmlContent = sHtmlContent.replace('<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<iframe.+?src="(.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):

        for aEntry in aResult[1]:
                
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
def serieHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    sHtmlContent = SucurieBypass().GetHtml(sUrl)

    sHtmlContent = sHtmlContent.replace('<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<div class="su-tabs-pane su-clearfix"><iframe src="(.+?)"[^<>]+?><\/iframe><\/div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        i = 1
        for aEntry in aResult[1]:
                
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            sTitle = sMovieTitle + 'episode ' + str(i)
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            i = i + 1
 
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
#***********************************************************************************************************************
#fusion fichier
#***********************************************************************************************************************
PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

class NoRedirection(urllib2.HTTPErrorProcessor):    
    def http_response(self, request, response):
        return response

class SucurieBypass(object):

    def __init__(self):
        self.state = False
        self.hostComplet = ''
        self.host = ''
        self.url = ''
                       
    def DeleteCookie(self,Domain):
        print 'Effacement cookies'
        file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        os.remove(os.path.join(PathCache,file))
        
    def SaveCookie(self,Domain,data):
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

        #save it
        file = open(Name,'w')
        file.write(data)

        file.close()
        
    def Readcookie(self,Domain):
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        
        try:
            file = open(Name,'r')
            data = file.read()
            file.close()
        except:
            return ''
        
        return data
          
    def DecryptCookie(self,htmlcontent):
        match = re.search("S\s*=\s*'([^']+)", htmlcontent)
        if match:
            s = base64.b64decode(match.group(1))
            s = s.replace(' ', '')
            s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
            s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
            s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
            s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
            s = re.sub(';location.reload\(\);', '', s)
            s = re.sub(r'\n', '', s)
            s = re.sub(r'document\.cookie', 'cookie', s)
            try:
                cookie = ''
                #print s
                exec(s)
                match = re.match('([^=]+)=(.*)', cookie)
                if match:
                    return match.group(1) + '=' + match.group(2)
            except:
                print 'Erreur decodage sucuri'
                
        return None
        
    #Return param for head
    def GetHeadercookie(self,url):
        #urllib.quote_plus()
        Domain = re.sub(r'https*:\/\/([^/]+)(\/*.*)','\\1',url)
        cook = self.Readcookie(Domain.replace('.','_'))
        if cook == '':
            return ''
            
        return '|' + urllib.urlencode({'User-Agent':UA,'Cookie': cook })   
     
    def CheckIfActive(self,html):
        if 'sucuri_cloudproxy_js' in html:
            return True
        return False
        
        
    def SetHeader(self):
        head=[]
        head.append(('User-Agent', UA))
        head.append(('Host' , self.host))
        head.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
        head.append(('Referer', self.url))
        head.append(('Content-Type', 'text/html; charset=utf-8'))
        head.append(('Accept-Encoding', 'identity'))
        return head
        
    def GetHtml(self,url):
        self.hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',url)
        self.host = re.sub(r'https*:\/\/','',self.hostComplet)
        self.url = url
                  
        #on cherche des precedents cookies
        cookies = self.Readcookie(self.host.replace('.','_'))

        htmlcontent = self.htmlrequest(url,cookies)

        if not self.CheckIfActive(htmlcontent):
            # ok pas de protection
            return htmlcontent
        
        #on cherche le nouveau cookie
        cookies = self.DecryptCookie(htmlcontent)
        if not cookies:
            print 'Erreur sucuri decodage'
            return ''
            
        print 'Protection Sucuri active'
        
        #on sauve le nouveau cookie
        self.SaveCookie(self.host.replace('.','_'),cookies)
        
        #et on recommence
        htmlcontent = self.htmlrequest(url,cookies)
        
        return htmlcontent
        
    def htmlrequest(self,url,cookies = ''):
        
        opener = urllib2.build_opener(NoRedirection)
        opener.addheaders = self.SetHeader()
        
        if cookies:
            opener.addheaders.append(('Cookie', cookies))
        
        response = opener.open(url)
        htmlcontent = response.read()
        response.close()
        
        if response.info().get('Content-Encoding') == 'gzip':
            print 'contenu zippe'
            import gzip
            from StringIO import StringIO
            buf = StringIO(htmlcontent)
            f = gzip.GzipFile(fileobj=buf)
            htmlcontent = f.read()
            
        return htmlcontent
