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
import unicodedata



SITE_IDENTIFIER = 'dpstream_net_Serie'
SITE_NAME = 'DPStream.net (Series)'
SITE_DESC = 'Series en streaming'

URL_MAIN = 'http://www.dpstream.net/'


ANIM_ANIMS = ('ABCDEF', 'showAnimAlpha')
SERIE_SERIES = ('ABCDEF', 'showSeriesAlpha')

URL_SEARCH = ('', 'showSeries')
FUNCTION_SEARCH = 'showSeries'

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
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'animes nouveautés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'serie nouveautés', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showSeries(str(sSearchText))
        oGui.setEndOfDirectory()
        return  
    

def showAnimAlpha(sLettre = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    if 'ABCDEF' in sUrl:
        for i in range(0,27) :
            cConfig().updateDialog(dialog, 27)
            if dialog.iscanceled():
                break
            
            sTitle = chr(64+i)
            if sTitle == '@':
                sTitle = '[0-9]'
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesAlpha','[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]','', '', '', oOutputParameterHandler)
    else:
        sLettre = sUrl
        sUrl = 'http://www.dpstream.net/liste-mangas-en-streaming.html'

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();

        sPattern = '<a class="b" href="([^<]+)">(' + str(sLettre) + '.+?)<.a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        print aResult
        
        if (aResult[0] == True):
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
                oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN)+  str(aEntry[0]) )
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters',sTitle,'', '', '', oOutputParameterHandler)
   
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
 
    
def showSeriesAlpha(sLettre = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    if 'ABCDEF' in sUrl:
        for i in range(0,27) :
            cConfig().updateDialog(dialog, 27)
            if dialog.iscanceled():
                break
            
            sTitle = chr(64+i)
            if sTitle == '@':
                sTitle = '[0-9]'
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesAlpha','[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]','', '', '', oOutputParameterHandler)
    else:
        sLettre = sUrl
        sUrl = 'http://www.dpstream.net/liste-series-en-streaming.html'

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();

        sPattern = '<a class="b" href="([^<]+)">(' + str(sLettre) + '.+?)<.a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        print aResult
        
        if (aResult[0] == True):
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
                oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN)+  str(aEntry[0]) )
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters',sTitle,'', '', '', oOutputParameterHandler)
   
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
    
def showSeries(sSearch = ''):
    oGui = cGui() #ouvre l'affichage
    
    if sSearch:
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)

        print sSearch
        query_args = { 'recherchem': str(sSearch) }
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = 'http://www.dpstream.net/liste-series-en-streaming.html'
        request = urllib2.Request(url,data,headers)
        #fh = open('c:\\test.txt', "w")
      
        try: 
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
      
        html = reponse.read()
      
        #fh = open('c:\\test.txt', "w")
        #fh.write(html)
        #fh.close()
      
        sHtmlContent = html

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') # recupere l'url sortis en parametre
    
        oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
        sHtmlContent = oRequestHandler.request(); #requete aussi    
        
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
 
    sPattern = '<h1 style="text-align:left;">\n*<a class="t" href="([^<]+)" id=".+?">(.+?)<.a>\n*<.h1>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[1]
            
            #not found better way
            sTitle = unicode(sTitle, errors='replace')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN)+str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            #oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0])) #sortis du poster

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', '', '', oOutputParameterHandler)
            #addTV pour sortir les serie tv (identifiant, function, titre, icon, poster, description, sortis parametre)
 
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        #print sNextPage
        if (sNextPage != False):
            sNextPage = str(URL_MAIN)+sNextPage
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc

    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage
    
def __checkForNextPage(sHtmlContent): #cherche la page suivante
    sPattern = 'GetId\(.pageplus1.\).href = .(.+?).;'
    # .+? je ne veut pas cette partis et peux importe ceux qu'elle contient
    #- (.+?) je veut cette partis et c'est la fin
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult #affiche le result dans le log naviguer un peux sur votre source pour voir si tous ce passe bien
    if (aResult[0] == True):
        return aResult[1][0]

    return False
 
def showListHosters():
    oGui = cGui() #ouvre l'affichage

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl') # recupere l'url sortis en parametre
    print str(sUrl)
    oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request(); #requete aussi
    
    sPattern = 'alt="icone lecteur ([^<]+)".+?<.td>(.|\s)?<td><a class="b" href="([^<]+)">(.+?)<.a><.td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult
    if (aResult[0] == True):
        total = len(aResult[1]) #dialog
        dialog = cConfig().createDialog(SITE_NAME) #dialog
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
            #L'array affiche vos info dans l'orde de sPattern en commencant a 0
            sTitle = aEntry[3]
            
            #not found better way
            sTitle = unicode(sTitle, errors='replace')
            sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            #sTitle = '[COLOR teal][' + str(aEntry[0]) + '][/COLOR] ' + str(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN)+str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', '', '', oOutputParameterHandler)
            #addTV pour sortir les serie tv (identifiant, function, titre, icon, poster, description, sortis parametre)
                
            #il existe aussis addMisc(identifiant, function, titre, icon, poster, description, sortis parametre)
            #la difference et pour les metadonner serie, films ou sans
        cConfig().finishDialog(dialog)#dialog
            
        oGui.setEndOfDirectory() #ferme l'affichage
        
        
def showListHostersSerie():# recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entre de paramettre
    sUrl = oInputParameterHandler.getValue('siteUrl')  # apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #apelle le titre
    sThumbnail = oInputParameterHandler.getValue('sThumbnail') # apelle le poster
    #http://www.dpstream.net/serie-263-cosmos-1999-saison-1-episode-01-FR.html 
    sPattern = 'http:..www.dpstream.net.serie-([^<]+?)-.+?saison-([^<]+)-episode-([^<]+)-(.+?).html'
    oParser = cParser()
    resultat = oParser.parse(sUrl, sPattern)

    resultat = resultat[1][0]
    print sMovieTitle

    sUrl = "http://www.dpstream.net/fichiers/includes/inc_afficher_serie/changer_episode.php?changer_episod=1&id_serie=" + str(resultat[0]) + '&saison=' + str(resultat[1]) + "&episode=" + str(resultat[2]) + "&version=" + str(resultat[3])
    print sUrl
    
    oRequestHandler = cRequestHandler(sUrl) # envoye une requete a l'url
    sHtmlContent = oRequestHandler.request(); #requete aussi
    
    sPattern = '(<iframe.+?src="|<embed src=")([^<]+)(" width|<.embed>)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    print aResult
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sTitle = sMovieTitle
            sUrl = aEntry[1]

            sHosterUrl = str(sUrl)

            oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle) #nom affiche
                oHoster.setFileName(sMovieTitle) # idem
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                #affiche le lien (oGui, oHoster, url du lien, poster)
            
        oGui.setEndOfDirectory() #ferme l'affichage
    
 
def seriesHosters(): #cherche les episode de series
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
    
    print sUrl
    
    sPattern = '<h3 ? style="border-bottom:none;padding-bottom:0;" class=".+?">([^<]+)<.h3>|<a class="b" ?id="([^<]+)" href="(.+?)"(>Episode| onclick)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #sPattern2 = 'img src="([^<]+)" style=".+?"'
    #aResult2 = oParser.parse(sHtmlContent, sPattern)
    
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
                oGui.addDir(SITE_IDENTIFIER, 'seriesHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'films.png', oOutputParameterHandler)
            else:
                sMovieTitle2 = sMovieTitle + ' - ' + aEntry[1]
                print sMovieTitle2
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN)+str(aEntry[2]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle2))
                #oOutputParameterHandler.addParameter('sThumbnail', str(aResult2[1][]))
                oGui.addTV(SITE_IDENTIFIER, 'showListHostersSerie', sMovieTitle2, 'films.png','', '', oOutputParameterHandler)
      
                
    oGui.setEndOfDirectory()
