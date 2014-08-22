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
from resources.lib.player import cPlayer
import re, urllib2

SITE_IDENTIFIER = 'freebox'
SITE_NAME = 'Freebox'
SITE_DESC = 'Regarder la télévision freebox | Uniquement pour les abonnés free'

URL_MAIN = 'http://mafreebox.freebox.fr/freeboxtv/playlist.m3u'

def load():
    oGui = cGui()
    
    list = []
    chaine = None
    num=None
    liste = urllib2.urlopen(URL_MAIN)

    for i in liste:
        ligne = i.strip()
        ligne=re.sub(r'#EXTVLCOPT.*',r'',ligne)
        if ligne:
            if chaine:
                list.append( (num,chaine,ligne) )              
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', ligne)
                oOutputParameterHandler.addParameter('siteTitle', str(chaine))
                oGui.addDir(SITE_IDENTIFIER, 'play', chaine, 'tv.png', oOutputParameterHandler)
                chaine=None
            if ligne[:7]=="#EXTINF":
                line=ligne.split(" - ")
                chaine = line[-1]
                num=int(line[0].split(",")[-1])
  
    oGui.setEndOfDirectory()
    
def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('siteTitle')
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sTitle)
    oGuiElement.setMediaUrl(sUrl)

    oPlayer = cPlayer()
    oPlayer.clearPlayList()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return
        
    oGui.setEndOfDirectory()
    