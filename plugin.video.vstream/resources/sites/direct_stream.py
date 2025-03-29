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
    
    ['DAZN 1', [57, 'https://miguia.tv/channels/big_329@2x.png']],
    ['DAZN 2', [58, 'https://cdn.sincroguia.tv/uploads/images/g/8/t/xdazn2.jpg.pagespeed.ic.SKK2xVfOfw.jpg']],
    
    ['bein Sports 1', [8, 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_1_Australia.png']],
    ['bein Sports 2', [9, 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_2_Australia.png']],
    ['bein Sports 3', [11, 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_3_Australia.png']],

    ['Canal+', [40, 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG']],
    ['Canal+ Foot', [6, 'https://upload.wikimedia.org/wikipedia/fr/3/3b/C%2B_Foot.png']],
    ['Canal+ sport 360', [5, 'https://upload.wikimedia.org/wikipedia/fr/1/11/C%2B_Sport_360.png']],
    ['Canal+ Sports', [12, 'https://matchpint-cdn.matchpint.cloud/shared/imagenes/channels/284_logo_1599851988.png']],

    ['eurosport 1', [14, 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg']],
    ['eurosport 2', [15, 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg']],

    ['RMC Sport 1', [1, 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1']],
    ['RMC Sport 2', [2, 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1']],
    ['RMC SPORT 3', [4, 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT3_PNG_500x500px.png?w=500&ssl=1']],

    ['L\'equipe TV', [71, 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png']],
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
        sUrl = 'player.php?id=%d' % value[0]
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
        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

