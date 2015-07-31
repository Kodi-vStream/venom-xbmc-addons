#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
#from resources.lib.gui.gui import cGui
#from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
import xbmc
from datetime import datetime


SITE_IDENTIFIER = 'ePg'
SITE_NAME = 'epg'

d = datetime.now()
date = d.strftime("%d-%m-%Y")


class cePg:
    
    def get_url(self, sTitle):
        
        oRequestHandler = cRequestHandler(url_index)
        sHtmlContent = oRequestHandler.request();
        
        sPattern = '<li.*?><a href="([^<]+)"><img.+?</a></li>'
        sTitle = sTitle.replace(' ', '-').replace('HD', '').replace('SD', '')
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                #print sTitle
                if sTitle.lower() in aEntry.lower():
                    return "http://www.programme-tv.net"+aEntry
        else: 
            return False
    
        
    
    def get_epg(self, sTitle, sTime):
        #ce soir
        print sTime
        if sTime == 'direct':
            sUrl = 'http://playtv.fr/programmes-tv/en-direct/canalsat/'
        elif sTime == 'soir':
            sUrl = 'http://playtv.fr/programmes-tv/'+date+'/20h-23h/'
        else :
            sUrl = 'http://playtv.fr/programmes-tv/'+date+'/20h-23h/'
            
        print sUrl
            

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();
        text = ''
        
        sPattern = '<a class="channel-img".+?<img.+?alt="(.+?)".+?|<span class="start" title="(.+?)">(.+?)</span>.+?<span class="program-gender small">.+?<span>(.+?)</span>.+?<a href=".+?" title=".+?">(.+?)</a>'
        
          
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                #chaine
                if aEntry[0]:
                    text += "[COLOR red]"+aEntry[0]+"[/COLOR]\r"
                #heure
                if aEntry[2]:
                    text += "[B]"+aEntry[2]+"[/B] -"
                #duréé
                if aEntry[1]:
                    text += aEntry[1]+" : "
                #type
                if aEntry[3]:
                    text += "("+aEntry[3]+") "   

                #title
                if aEntry[4]:
                    text += "     [COLOR khaki][UPPERCASE]"+aEntry[4]+"[/UPPERCASE][/COLOR] "
                
                #retour line
                text += "\r\n"
                
            cConfig().TextBoxes(sTitle,text)
        else:
            cConfig().error('Impossible de trouver le guide tv')
            
    def get_oneepg(self, sTitle):
        
        sUrl = self.get_url(sTitle)
        if not sUrl:
            cConfig().showInfo('EPG', 'EPG introuvable')
            return
        
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request();
        sHtmlContent = sHtmlContent.replace('<br>', '')
        text = ''
        sPattern = '<div .*?class="broadcast">.+?<span class="hour">(.+?)</span>.+?<div class="programme">.+?<.+?class="title" title=".+?">(.+?)</.+?>.+?(?:<span class="subtitle">(.+?)</span>.+?|)<span class="type">(.+?)</span>'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                #hour
                text += "[B]"+aEntry[0]+"[/B] : "
                #type
                text += "[I]"+aEntry[3]+"[/I] - "
                #title
                text += "[COLOR khaki][UPPERCASE]"+aEntry[1]+"[/UPPERCASE][/COLOR] "
                #subtitle
                text += aEntry[2]
                
                #retour line
                text += "\r\n"
                
            return text
        else:
            return ''
