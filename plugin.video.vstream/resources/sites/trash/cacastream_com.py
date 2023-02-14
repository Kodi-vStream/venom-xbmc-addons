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
import urllib2,urllib,re
import unicodedata,htmlentitydefs
import time

#Si vous créer une source et la déposer dans le dossier sites elle seras directement visible sous xbmc

SITE_IDENTIFIER = 'cacastream_com'
SITE_NAME = 'Cacastream.com'
SITE_DESC = 'Series/Films/Animes en streaming'

URL_MAIN = 'http://www.cacastream.com' # url de votre source

#definis les url pour les catégories principale ceci et automatique si la deffition et présente elle seras afficher.
MOVIE_NEWS = ('http://www.cacastream.com/films-en-streaming.html', 'showMovies')
SERIE_SERIES = ('http://www.cacastream.com/series-en-streaming.html', 'showAlpha')
ANIM_ANIMS = ('http://www.cacastream.com/mangas-en-streaming.html', 'showAlpha')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

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


def _DecryptProtectStream(url):

    videoId = re.findall('protect-stream\.com\/PS_DL_([A-Za-z0-9\\-_]+)',url )
    #print(videoId[0])
    
    oRequestHandler = cRequestHandler("http://www.protect-stream.com/w.php?u=" + videoId[0])
    sHtmlContent = oRequestHandler.request();
    
    cheap = re.findall('var k=\"([^<>\"]*?)\";' , sHtmlContent)
    
    if not cheap:
        return ''
    
    #Need to wait
    time.sleep( 10 )
    
    query_args = { 'k': cheap[0] }
    data = urllib.urlencode(query_args)
    headers = {'User-Agent' : 'Mozilla 5.10'}
    url = 'http://www.protect-stream.com/secur.php'
    request = urllib2.Request(url,data,headers)
      
    try: 
        reponse = urllib2.urlopen(request)
    except URLError, e:
        print e.read()
        print e.reason
      
    html = reponse.read()
    
    DecryptedUrl = re.findall('href=\"(http[^<>\"]*?)\"' , html)
    
    if DecryptedUrl:
        return DecryptedUrl[0]
        
    return False


def load(): #function charger automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #apelle la function pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortis du parametres siteUrl oublier pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Liste Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Liste Animes', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Liste Films' , 'series.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        showMovies(str(sSearchText))
        oGui.setEndOfDirectory()
        return  
    
   
def showAlpha(sLettre = ''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sLettre = oInputParameterHandler.getValue('sLettre')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    if not sLettre:
        for i in range(0,27) :
            cConfig().updateDialog(dialog, 27)
            if dialog.iscanceled():
                break
            
            sTitle = chr(64+i)
            if sTitle == '@':
                sTitle = '[0-9]'
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sLettre', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addTV(SITE_IDENTIFIER, 'showAlpha','[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]','', '', '', oOutputParameterHandler)
    else:
        
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();

        sPattern = 'font-size:10px;font-weight:bold;" href="([^<]+)" class="b">(' + str(sLettre) + '.*?)<\/a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            total = len(aResult[1])
            dialog = cConfig().createDialog(SITE_NAME)
        
            for aEntry in aResult[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break
                    
                sTitle = aEntry[1]
                
                #Unicode convertion
                sTitle = unicode(sTitle,'iso-8859-1')
                sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')
                sTitle = unescape(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + '/' + str(aEntry[0]) )
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode',sTitle,'', '', '', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
   
  
def showMovies(sSearch = ''):
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)
        
        sDisp = oInputParameterHandler.getValue('disp')
        #print sSearch
        
        if (sDisp == 'search3'):#anime
            url = 'http://www.cacastream.com/rechercher-un-manga.html'
            query_args = { 'searchm': str(sSearch) }
        elif (sDisp == 'search2'):#serie
            url = 'http://www.cacastream.com/rechercher-une-serie.html'
            query_args = { 'searchs': str(sSearch) }
        else:
            url = 'http://www.cacastream.com/rechercher-un-film.html'
            query_args = { 'searchf': str(sSearch) }
            
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}    

        request = urllib2.Request(url,data,headers)
      
        try: 
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
      
        sHtmlContent = reponse.read()
        
        sPattern = '<div onmouseover=.+?<img src=([^<]+) border.+?font-size:14px>([^<]+)<.font>.+?<i>(.+?)<.i>(?:.|\n)+?<a href="([^<]+)" class='
        #sPattern = '<div onmouseover=.+?<img src=([^<]+) border.+?font-size:14px>([^<]+)<.font>.+?Synopsis : <.b> <i>(.+?)<.i>(.|\n)+?<a href="([^<]+)" class='

    else:
        
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();
   
        sPattern = 'Tip\(\'<center><b>(.+?)<.b>.+?Synopsis : <.b> <i>(.+?)<.i>(?:.|\n)+?<a href="(.+?)"><img src="(.+?)" alt'
    
    #fh = open('c:\\serie.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult
    
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            if sSearch:
                sTitle = aEntry[1]
                sThumb = str(aEntry[0])
                sCom = aEntry[2]
                sUrl2 = str(URL_MAIN)+ '/' + str(aEntry[3])
            else:
                sTitle = aEntry[0]
                sThumb = str(aEntry[3])
                sCom = aEntry[1]
                sUrl2 = str(URL_MAIN)+ '/' + str(aEntry[2])
            
            #Nettoyage titre
            sTitle = unicode(sTitle, errors='replace')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            #Nettoyage commentaires
            sCom = unicode(sCom, 'iso-8859-1')#converti en unicode
            sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
            sCom = unescape(sCom) #decode html
            sCom = re.sub('<.*?>', '', sCom)#remove html tags
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            
            if ('-episode-' in sUrl2):
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, sCom, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showListHosters', sTitle, '', sThumb, sCom, oOutputParameterHandler)

 
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            #print sNextPage
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()
    
def __checkForNextPage(sHtmlContent):
    sPattern = '<td width="124" class="page_tab"><a href="(.+?)" class="b">Page Suivante<.a><.td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def showEpisode():
    oGui = cGui() #ouvre l'affichage

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #print sUrl
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    oParser = cParser()
    
    #image
    sPattern = '<div class="tvshow_image">.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        sThumbnail = aResult[1][0]
    else :
        sThumbnail = ''
    
    #commentaire
    sPattern = '<span class="infos01">Synopsis : <\/span>(.+?)<\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        sCom = aResult[1][0]
        #Nettoyage commentaires
        sCom = unicode(sCom, 'iso-8859-1')#converti en unicode
        sCom = unicodedata.normalize('NFD', sCom).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
        sCom = unescape(sCom) #decode html
        sCom = re.sub('<.*?>', '', sCom)#remove html tags
        
    else :
        sCom = ''
    
    #liens par saisons
    sPattern = '(?:<a name="s[0-9]+" >(Saison.+?)<\/a>)|(?:<a class="e" href="(.+?)">(.+?)<\/a>)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #si pas trouvé par episode
    if not aResult[0]:
        sPattern = '(ABXY)*<a (class)="e" href="(.+?episode.+?html)">(.+?)<\/a>'
        aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
    
    if aResult[0]:
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[2]
            
            #Nettoyage titre
            sTitle = unicode(sTitle, errors='replace')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))

                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', '[COLOR red]'+ aEntry[0] +'[/COLOR]', '', sThumbnail, '', oOutputParameterHandler)
            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + '/' + aEntry[1])
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

                oGui.addTV(SITE_IDENTIFIER, 'showListHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        oGui.setEndOfDirectory()
    

def showListHosters():
    oGui = cGui() #ouvre l'affichage

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    print sUrl
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    sPattern = '(?:<a href="(http:..www.protect-stream.com.+?)" target="_blank" class="b"><b><span class="(.+?)">(.+?)<\/span>)|(?:<a href="mylink\.php\?v=(.+?)&rang=.+?&lecteur=(.+?)" class="b" target="mesliens">)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult
    
    if aResult[0]:
        #on bride car trop de resultat
        aResultMax = aResult[1]
        if len(aResultMax) > 100:
            aResultMax = aResultMax[:100]
        total = len(aResultMax)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResultMax:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #1 er cas
            sHost = str(aEntry[2])
            sUrl = aEntry[0]
            
            #2 eme cas
            if aEntry[3]:
                sHost = str(aEntry[4])
                sUrl = 'http://www.protect-stream.com/PS_DL_' + str(aEntry[3])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', '[COLOR red]['+ sHost +'][/COLOR] ' + sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)#dialog
            
        oGui.setEndOfDirectory() #ferme l'affichage
        
        
def showHosters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #on decrypte le seul lien present
    cConfig().showInfo('Decryptage', 'Please wait 10s')
    aResult = _DecryptProtectStream(sUrl)
    
    if (aResult):

        sHosterUrl = str(aResult)

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
            
    oGui.setEndOfDirectory()
    
