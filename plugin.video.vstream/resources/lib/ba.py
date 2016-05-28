#-*- coding: utf-8 -*-
#Venom.
from resources.lib.handler.requestHandler import cRequestHandler
import re
import xbmc

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
            xbmc.log(url)
            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % list[0]
            
            xbmc.executebuiltin('PlayMedia('+ url + ')')
              
        return
