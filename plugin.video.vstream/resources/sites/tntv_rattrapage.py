#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import util 
import re,unicodedata

SITE_IDENTIFIER = 'tntv_rattrapage'
SITE_NAME = 'Tn tv rattrapage'
SITE_DESC = 'Replay TV'

URL_MAIN = 'http://tntv-rattrapage.overblog.com'

REPLAYTV_NEWS = ('http://tntv-rattrapage.overblog.com/', 'showMovies')
REPLAYTV_REPLAYTV = ('xyz', 'showGenre')

URL_SEARCH = (URL_MAIN + 'search/','showMovies')

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Nouvelles Emissions', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'xyz')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Emissions par Catégories', 'tv.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText+'/'
 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    
    if sUrl == 'xyz':
        liste.append( ['Chaines','1'] )
        liste.append( ['Telerealites','2'] )
        liste.append( ['Divertissement','3'] )
        liste.append( ['Info et magazine','4'] )
        liste.append( ['Sport','5'] )
        liste.append( ['Serie VF','http://tntv-rattrapage.overblog.com/tag/series%20vf/'] )
        liste.append( ['Serie VOSTFR','http://tntv-rattrapage.overblog.com/tag/series%20vostfr/'] )
               
        for sTitle,sUrl2 in liste:
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            if not sUrl2.startswith('http'):
                oGui.addDir(SITE_IDENTIFIER, 'showGenre', sTitle, 'genres.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
    else:
        
        oRequestHandler = cRequestHandler(URL_MAIN)
        sHtmlContent = oRequestHandler.request()

        sPattern = ''
        
        if sUrl == '1':
            sPattern = 'class="NavElement-link" href="#">Cat..gories<\/a>(.+?)class="NavElement-link" href="#">Archives<\/a>'
        if sUrl == '2':
            sPattern = 'class="NavElement-link" href="#">T..l..r..alit..s<\/a>(.+?)class="NavElement-link" href="#">Divertissement<\/a>'
        if sUrl == '3':
            sPattern = 'class="NavElement-link" href="#">Divertissement<\/a>(.+?)class="NavElement-link" href="#">Infos et Magazine<\/a>'
        if sUrl == '4':
            sPattern = 'class="NavElement-link" href="#">Infos et Magazine<\/a>(.+?)class="NavElement-link" href="#">Sport<\/a>'
        if sUrl == '5':
            sPattern = 'class="NavElement-link" href="#">Sport<\/a>(.+?)class="NavElement-link" href="\/tag\/archive">Les int..grales<\/a>'
                
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            tmp = aResult[1][0]
            sPattern = 'class="NavElement-link" href="(.+?)">(.+?)<\/a>'
            oParser = cParser()
            aResult = oParser.parse(tmp, sPattern)
        
        if (aResult[0] == True):

            for aEntry in aResult[1]:
                sTitle = aEntry[1]
                sUrl = aEntry[0]
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    sUrl = sUrl.replace(' ','%20')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="PostPreview-coverImage" src="(.+?)" alt="(.+?)".+?<p class="PostPreview-snippet">(.+?)</p>.+?<a class="PostPreview-link" href="(.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = util.createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = unicode(aEntry[1], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            sTitle = sTitle.encode( "utf-8")
            
            #Reformatage
            sTitle = re.sub('[0-9:]{5} \| ([0-9-]{8}) \|','[\\1]', sTitle)
            
            sMovieTitle = sTitle#re.sub('(\[.*\])','', str.strip(aEntry[1]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[3]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))


            if not '[direct]' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showHoster', sTitle, '', aEntry[0], aEntry[2], oOutputParameterHandler)
            
        util.finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'class="ob-page ob-page-current ".+?href="(.+?)".+?class="ob-page ob-page-link ob-page-next"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return str(URL_MAIN) + aResult[1][0]

    return False
    
def showHoster():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    sPattern = '<a (?:sl-processed="1" )*(?:class="episode-number" )*href="#itsthetable1" on[cC]lick="(.+?)_player\( *\'(.+?)\' *\);">(?:<span class="ep-numb">(.+?)<\/span>)*'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'exashare' in aEntry[0]:
                sUrl = 'http://www.exashare.com/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'flashx' in aEntry[0]:
                sUrl = 'http://www.flashx.tv/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'youwatch' in aEntry[0]:
                sUrl = 'http://youwatch.org/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'streamin2' in aEntry[0]:
                sUrl = 'http://streamin.to/embed-' + str(aEntry[1]) + '-624x360.html'

            if 'vodlocker' in aEntry[0]:
                sUrl = 'http://vodlocker.com/embed-' + str(aEntry[1]) + '-624x360.html'
                
            sTitle = sMovieTitle
            if aEntry[2]:
                sTitle = sTitle + 'Ep ' + aEntry[2]

            sHosterUrl = sUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         

    oGui.setEndOfDirectory()
