from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
import time
import random

class cStatistic:

    STATISTIC_URL = 'http://www.google-analytics.com/__utm.gif'
    STATISTIC_ID = 'UA-11805303-2'

    def callStartPlugin(self, sPluginName):
        oConfig = cConfig()
        bStatistic = oConfig.getSetting('statistic')
      
        if (bStatistic == 'False'):
            return;
	
        try:
            oRequestHandler = cRequestHandler(self.STATISTIC_URL)

            oRequestHandler.addParameters('utmac', self.STATISTIC_ID)

            rndX = random.randint(1, 99999999-10000000)+10000000
            rndY = random.randint(1, 999999999-100001000)+100000000
	    ts1 = float(time.time())
            ts2 = float(time.time())
            ts3 = float(time.time())
            ts4 = float(time.time())
            ts5 = float(time.time())

            sUtmccValue = '__utma=' + str(rndY) + '.' + str(rndX) + '.' + str(ts1) + '.' + str(ts2) + '.' + str(ts3) + '; '
            sUtmccValue = sUtmccValue + '+__utmz=' + str(rndY) + '.' + str(ts4) + '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
            oRequestHandler.addParameters('utmcc', sUtmccValue)
	    #oRequestHandler.addParameters('aip', '1') # anonymizeIp

            oRequestHandler.addParameters('utmcs', 'UTF-8')
            oRequestHandler.addParameters('utmdt', 'Plugin Activity')
            oRequestHandler.addParameters('utmfl', '10.1 r102')
            oRequestHandler.addParameters('utmhid', '1549554730')
            oRequestHandler.addParameters('utmhn', 'code.google.com')
            oRequestHandler.addParameters('utmje', '0')
            oRequestHandler.addParameters('utmn', '771768122')
            oRequestHandler.addParameters('utmp', '/p/xbmc-xstream-plugin/w/list?plugin=' + str(sPluginName))
            oRequestHandler.addParameters('utmr', '-')
            oRequestHandler.addParameters('utmsc', '24-bit')
            oRequestHandler.addParameters('utmsr', '1920x1080')
            oRequestHandler.addParameters('utmu', 'qAAg')
            oRequestHandler.addParameters('utmul', 'de')
            oRequestHandler.addParameters('utmwv', '4.8.6')
                       
            oRequestHandler.request()
        except Exception, e:
            return

      

