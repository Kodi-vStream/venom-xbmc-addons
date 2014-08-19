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

SITE_IDENTIFIER = 'chaine_tv'
SITE_NAME = 'Télévision en Stream'

URL_MAIN = 'http://venom'

def load():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    #liste.append( ['TF1 HD','http://smooth.wat.tv/DVR_ETF1/source/master.m3u8'] )
    #liste.append( ['TF1','http://ipm.iphone-tv.eu:1345/index.m3u8?c=tf1&auth=eaf1059aa96d27f815c3e96472ee5d1c72bfdb7b811030809665a71964c0f7d4'] )
    liste.append( ['France 2','http://ipm.iphone-tv.eu:1345/index.m3u8?c=fr2&auth=38d6e9c92f7fb39c793b65e4a2488b1473a0c2d81bf4f9a99c6a0dbb8af16739'] )
    liste.append( ['France 3','http://hls1.maiyo-tv.com/index.m3u8?c=fr_france3'] )
    liste.append( ['France 4','http://hls1.maiyo-tv.com/index.m3u8?c=fr_france4'] )
    liste.append( ['France 5','http://hls1.maiyo-tv.com/index.m3u8?c=fr_france5'] )
    liste.append( ['M6','http://hls1.maiyo-tv.com/index.m3u8?c=fr_m6'] )
    liste.append( ['6Ter','https://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/six_ter_hls_aes/six_ter_hls_aes_856.m3u8'] )
    liste.append( ['D8','http://hls-live-m1-l3.canal-plus.com/live/hls/d8-clair-v3-sd-andr7/and-sd-clair/index.m3u8'] )
    liste.append( ['W9','http://hls1.maiyo-tv.com/index.m3u8?c=fr_w9'] )
    liste.append( ['NRJ12','http://nrj-apple-live.adaptive.level3.net/apple/nrj/nrj/nrj12hi.m3u8'] )
    liste.append( ['D17','http://hls-live-m1-l3.canal-plus.com/live/hls/d17-clair-v3-sd-andr7/and-sd-clair/index.m3u8'] )
    liste.append( ['23','http://stream-l3-4.vty.dmcdn.net/04/dm/1/x13p3qi/live.isml/events(live-1407147536)/live-audio=128000.m3u8'] ) 
    liste.append( ['Rts Un','http://hls1.maiyo-tv.com/index.m3u8?c=fr_rtsun'] )
    liste.append( ['Rts Deux','http://hls1.maiyo-tv.com/index.m3u8?c=fr_rtsdeux'] )
    liste.append( ['TV5 Monde','http://ca-edge-5.cdn2.streamago.tv/streamagoedge/1924/817/chunklist_w797487548.m3u8'] )
    liste.append( ['National geographic','http://195.154.188.161/hls/nationalgeo.m3u8'] )  
    liste.append( ['RMC Découverte','http://wpc.6d40.edgecastcdn.net/806D40/Wowza3/live-origin/gtv213.stream/chunklist.m3u8'] )
    liste.append( ['Gulli','http://hls1.maiyo-tv.com/index.m3u8?c=fr_gulli'] )
    liste.append( ['ZouZous','http://medias2.francetv.fr/playlists/zouzous/zouzous_tablettes.m3u8'] )
    liste.append( ['BFM TV','http://bfmlive2-i.akamaihd.net/hls/live/214427/bfmtv/04.m3u8'] ) 
    liste.append( ['BFM Business','http://bfmlive-i.akamaihd.net/hls/live/214272/bfmbusiness/01.m3u8'] )
    liste.append( ['France24','http://tv.flux.france24.com/4684/02.m3u8'] )   
    liste.append( ['KTO','http://mobile.ktotv.com/live/KTO_Layer1.m3u8'] )
    liste.append( ['LaTele','http://rtmp.infomaniak.ch/livecast/latele/playlist.m3u8'] )
    liste.append( ['MenUpTv','http://videos.mensup.fr/mensuptv/live/01.m3u8'] )  
    liste.append( ['OuiTV','http://rtmp.infomaniak.ch/livecast/ouitv/playlist.m3u8'] )
    liste.append( ['PTC','http://media.rtc.be/vod/mp4:166597.mp4/hasbahca.m3u8'] )   
    liste.append( ['RougeTV','http://rtmp.infomaniak.ch/livecast/rougetv/playlist.m3u8'] )
    liste.append( ['RTC','http://media.webtvlive.eu/rtc/smil:live.smil/playlist.m3u8'] )
    liste.append( ['EuroNews','http://hd1.lsops.net/live/euronews_fr_340/.m3u8'] )  
    liste.append( ['LCP','http://vipwowza.yacast.net/lcplive/_definst_/mp4:lcplive_HVGA/playlist.m3u8'] )
    liste.append( ['L\'équipe21','http://chkg.tdf-cdn.com/5687/index.m3u8'] )
    liste.append( ['IDF1','http://stream7.idf1.yacast.net/iphone/idf1/live01/idf1_live01hd.m3u8'] )
    liste.append( ['Djing','http://cdn.djing.com/tv/live.m3u8'] )
    liste.append( ['Alsace 20','http://live.iphone.alsace20.fr/stream_multi.m3u8'] )
    liste.append( ['Itele','http://hls-live-m2-l3.canal-plus.com/live/hls/itele-clair-v3-sd-andr7/and-sd-clair/index.m3u8'] )

    
    

        
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
        oOutputParameterHandler.addParameter('siteTitle', str(sTitle))
        oGui.addDir(SITE_IDENTIFIER, 'play', sTitle, 'tv.png', oOutputParameterHandler)
       
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
    