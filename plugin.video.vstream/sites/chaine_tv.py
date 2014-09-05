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
SITE_DESC = 'Regarder la télévision française'

URL_MAIN = 'http://venom'

def load():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    #liste.append( ['TF1 HD','http://smooth.wat.tv/DVR_ETF1/source/master.m3u8'] )
    #liste.append( ['TF1','http://ipm.iphone-tv.eu:1345/index.m3u8?c=tf1&auth=eaf1059aa96d27f815c3e96472ee5d1c72bfdb7b811030809665a71964c0f7d4'] )
    liste.append( ['2','France 2','http://dt3zwsgl95oj4.cloudfront.net/live2/france2.smil/playlist.m3u8'] )
    liste.append( ['3','France 3','http://dt3zwsgl95oj4.cloudfront.net/live2/france3.smil/playlist.m3u8'] )
    liste.append( ['5','France 5','http://dt3zwsgl95oj4.cloudfront.net/live2/france5.smil/playlist.m3u8'] )
    liste.append( ['6','M6','https://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/m6_hls_aes/m6_hls_aes_856.m3u8'] )
    liste.append( ['7','Arte','http://frlive.artestras.cshls.lldns.net/artestras/contrib/frlive/frlive_925.m3u8'] )
    liste.append( ['8','D8','http://hls-live-m1-l3.canal-plus.com/live/hls/d8-clair-v3-sd-andr7/and-sd-clair/index.m3u8'] )
    liste.append( ['9','W9','https://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/w9_hls_aes/w9_hls_aes_856.m3u8'] )
    liste.append( ['12','NRJ12','http://nrj-apple-live.adaptive.level3.net/apple/nrj/nrj/nrj12hi.m3u8'] )
    liste.append( ['14','France 4','http://dt3zwsgl95oj4.cloudfront.net/live2/france4.smil/playlist.m3u8'] )
    liste.append( ['17','D17','http://hls-live-m1-l3.canal-plus.com/live/hls/d17-clair-v3-sd-andr7/and-sd-clair/index.m3u8'] )
    #liste.append( ['23','TV5 Monde','http://ca-edge-5.cdn2.streamago.tv/streamagoedge/1924/817/chunklist_w797487548.m3u8'] )
    liste.append( ['26','RTL9','http://dt3zwsgl95oj4.cloudfront.net/live2/rtl9.smil/playlist.m3u8'] )
    liste.append( ['27','AB1','http://dt3zwsgl95oj4.cloudfront.net/live2/ab1.smil/playlist.m3u8'] )
    liste.append( ['29','6Ter','https://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/six_ter_hls_aes/six_ter_hls_aes_856.m3u8'] )
    #liste.append( ['6Ter','http://sslhls.m6tv.cdn.sfr.net/hls-live/livepkgr/_definst_/six_ter_hls_aes/six_ter_hls_aes_856.m3u8'] )
    liste.append( ['31','Numéro 23','http://stream-l3-4.vty.dmcdn.net/17/dm/1/x13p3qi/live.isml/live.m3u8'] ) 
    liste.append( ['37','France O','http://dt3zwsgl95oj4.cloudfront.net/live2/franceo.smil/playlist.m3u8'] )  
    liste.append( ['52','Itele','http://hls-live-m2-l3.canal-plus.com/live/hls/itele-clair-v3-sd-andr7/and-sd-clair/index.m3u8'] )
    liste.append( ['53','BFM TV','http://bfmlive2-i.akamaihd.net/hls/live/214427/bfmtv/04.m3u8'] ) 
    liste.append( ['54','EuroNews','http://hd1.lsops.net/live/euronews_fr_340/.m3u8'] ) 
    liste.append( ['56','France24','http://tv.flux.france24.com/4684/02.m3u8'] ) 
    liste.append( ['57','LCP','http://vipwowza.yacast.net/lcplive/_definst_/mp4:lcplive_HVGA/playlist.m3u8'] )
    liste.append( ['58','KTO','http://mobile.ktotv.com/live/KTO_Layer1.m3u8'] )
    liste.append( ['59','BFM Business','http://bfmlive-i.akamaihd.net/hls/live/214272/bfmbusiness/01.m3u8'] ) 
    liste.append( ['67','Gulli','http://vipwowza.yacast.net/gulli_live/_definst_/mp4:gulli_850/playlist.m3u8'] )
    liste.append( ['NC','ZouZous','http://medias2.francetv.fr/playlists/zouzous/zouzous_tablettes.m3u8'] )
    #liste.append( ['95','Alsace 20','http://live.iphone.alsace20.fr/stream_multi.m3u8'] )
    liste.append( ['96','IDF1','http://stream7.idf1.yacast.net/iphone/idf1/live01/idf1_live01hd.m3u8'] )
    liste.append( ['117','Action','http://dt3zwsgl95oj4.cloudfront.net/live2/action.smil/playlist.m3u8'] )
    liste.append( ['118','Ciné FX','http://dt3zwsgl95oj4.cloudfront.net/live2/cinefx.smil/playlist.m3u8'] )
    liste.append( ['119','Polar','http://dt3zwsgl95oj4.cloudfront.net/live2/cinepolar.smil/playlist.m3u8'] )
    liste.append( ['132','National geographic','http://195.154.188.161/hls/nationalgeo.m3u8'] )
    liste.append( ['138','RMC Découverte','rtmp://vipwowza.yacast.net/rmc_decouverte_rtmp//live'] )
    liste.append( ['143','Escales','http://dt3zwsgl95oj4.cloudfront.net/live2/escales.smil/playlist.m3u8'] )
    liste.append( ['145','Animaux','http://dt3zwsgl95oj4.cloudfront.net/live2/animaux.smil/playlist.m3u8'] )
    liste.append( ['146','Encyclo','http://dt3zwsgl95oj4.cloudfront.net/live2/encyclo.smil/playlist.m3u8'] )
    liste.append( ['148','Chasse et Pêche','http://dt3zwsgl95oj4.cloudfront.net/live2/chasseetpeche.smil/playlist.m3u8'] )
    liste.append( ['158','ABMoteurs','http://dt3zwsgl95oj4.cloudfront.net/live2/abmoteurs.smil/playlist.m3u8'] )
    liste.append( ['215','Mangas','http://dt3zwsgl95oj4.cloudfront.net/live2/mangas.smil/playlist.m3u8'] )
    liste.append( ['NC','Cartoon Network','http://ipm.iphone-tv.eu:1345/index.m3u8?c=cn&auth=82b883ca804dc5ee2c02643590646629106ad07f185bfb4514ecd2df2496e5b8'] )
    liste.append( ['NC','Lucky Jack TV','http://dt3zwsgl95oj4.cloudfront.net/live2/luckyjack.smil/playlist.m3u8'] )
    liste.append( ['NC','LaTele','http://rtmp.infomaniak.ch/livecast/latele/playlist.m3u8'] )
    liste.append( ['NC','MenUpTv','http://videos.mensup.fr/mensuptv/live/01.m3u8'] )  
    liste.append( ['NC','OuiTV','http://rtmp.infomaniak.ch/livecast/ouitv/playlist.m3u8'] )
    liste.append( ['NC','PTC','http://media.rtc.be/vod/mp4:166597.mp4/hasbahca.m3u8'] )   
    liste.append( ['NC','RougeTV','http://rtmp.infomaniak.ch/livecast/rougetv/playlist.m3u8'] )
    liste.append( ['NC','RTC','http://media.webtvlive.eu/rtc/smil:live.smil/playlist.m3u8'] )
    liste.append( ['NC','L\'équipe21','http://chkg.tdf-cdn.com/5687/index.m3u8'] )
    #liste.append( ['L\'Equipe 21','http://chkg.tdf-cdn.com/5687/02.m3u8'] )
    liste.append( ['NC','Djing','http://cdn.djing.com/tv/live.m3u8'] )
    liste.append( ['372','DorcelTV','http://dt3zwsgl95oj4.cloudfront.net/live2/dorceltv.smil/playlist.m3u8'] )
    liste.append( ['371','XXL','http://dt3zwsgl95oj4.cloudfront.net/live2/xxl.smil/playlist.m3u8'] )

     
    for sNum, sTitle,sUrl in liste:
        sTitle = sNum+' : '+sTitle
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
    