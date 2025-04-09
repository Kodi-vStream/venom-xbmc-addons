# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'direct_stream'
SITE_NAME = 'Direct-StreamFR'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


SPORT_SPORTS = (True, 'load')
SPORT_TV = ('lecteur/', 'showTV')


# chaines
channels = [
    
    ['DAZN 1', [57, 'https://cdn.sincroguia.tv/uploads/images/e/q/k/xdazn1.jpg.pagespeed.ic.oaUemASdvr.jpg']],
    ['DAZN 2', [58, 'https://cdn.sincroguia.tv/uploads/images/g/8/t/xdazn2.jpg.pagespeed.ic.SKK2xVfOfw.jpg']],
    ['DAZN 3', [73, 'https://cdn.sincroguia.tv/uploads/images/7/9/t/xdazn3.jpg.pagespeed.ic.BXBiZkQLdS.jpg']],
    
    ['bein Sports 1', [8, 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_1_Australia.png']],
    ['bein Sports 2', [9, 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_2_Australia.png']],
    ['bein Sports 3', [11, 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_3_Australia.png']],

    ['Canal+', [40, 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG']],
    ['Canal+ Foot', [6, 'https://upload.wikimedia.org/wikipedia/fr/3/3b/C%2B_Foot.png']],
    ['Canal+ Sport', [12, 'https://frembed.xyz/logo/channels/canal-plus-sport.png']],
    ['Canal+ Sport 1', [74, 'https://frembed.xyz/logo/channels/canal-plus-sport-1-min.png']],
    ['Canal+ Sport 2', [75, 'https://frembed.xyz/logo/channels/canal-plus-sport-2.png']],
    ['Canal+ Sport 3', [76, 'https://frembed.xyz/logo/channels/canal-plus-sport-3.png']],
    ['Canal+ Sport 4', [77, 'https://frembed.xyz/logo/channels/canal-plus-sport-4.png']],
    ['Canal+ Sport 5', [78, 'https://frembed.xyz/logo/channels/canal-plus-sport-5-min.png']],
    ['Canal+ sport 360', [5, 'https://upload.wikimedia.org/wikipedia/fr/1/11/C%2B_Sport_360.png']],

    ['eurosport 1', [14, 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg']],
    ['eurosport 2', [15, 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg']],

    ['RMC Sport 1', [1, 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1']],
    ['RMC Sport 2', [2, 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1']],
    ['RMC Sport 3', [4, 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT3_PNG_500x500px.png?w=500&ssl=1']],

    ['Automoto', [68, 'https://moto-station.com/wp-content/uploads/2021/05/05/Automoto-La-Chaine-logo_0.png.jpg']],

    ['L\'equipe', [71, 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png']],
    ['L\'equipe Live 1', [79, 'https://frembed.xyz/logo/channels/lequipe-live-1-min.png']],
    ['L\'equipe Live 2', [80, 'https://frembed.xyz/logo/channels/lequipe-live-2-min.png']],
    ]


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines', 'tv.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    for sDisplayTitle, value in channels:
        sUrl = 'api/player.php?id=%d' % value[0]
        sThumb = value[1]
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oParser = cParser()
    oHosterGui = cHosterGui()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, 'file: "([^"]+)')

    if aResult[0]:
        sHosterUrl = aResult[1][0]
        
        # redirection de lien
        oRequestHandler = cRequestHandler(sHosterUrl)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        sHtmlContent = oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()

        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            sHosterUrl += "|Referer=" + URL_MAIN
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

