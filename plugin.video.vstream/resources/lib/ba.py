#-*- coding: utf-8 -*-
#Venom.
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
import re

SITE_IDENTIFIER = 'cBA'
SITE_NAME = 'BA'

class cShowBA:

    def __init__(self):
        self.search =''

    def SetSearch(self,search):
        self.search = search.replace(' ','+')
        self.search =  self.search + '+bande+annonce'
    
    def SearchBA(self):
        self.url = 'https://www.youtube.com/results?q=' + self.search + '&sp=EgIYAQ%253D%253D'
        
        oRequestHandler = cRequestHandler(self.url)
        sHtmlContent = oRequestHandler.request()

        list = re.findall('<a href="\/watch\?v=([^"<>]+)" class=',sHtmlContent)
        if list:
            url = 'http://www.youtube.com/watch?v=' + list[0]
            exec "from resources.hosters.youtube import cHoster" 
            hote = cHoster()
            hote.setUrl(url)
            api_call = hote.getMediaLink()[1]
            if not api_call:
                return
                
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(self.search.replace('+',' '))
            oGuiElement.setMediaUrl(api_call)
            oGuiElement.setThumbnail(oGuiElement.getIcon())
            
            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()

        return
