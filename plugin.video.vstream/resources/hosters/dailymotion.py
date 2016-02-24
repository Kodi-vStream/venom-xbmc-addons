from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import xbmcgui, urllib2 , re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DailyMotion'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def setHD(self, sHD):
        if 'hd' in sHD:
            self.__sHD = 'HD'
        else: 
            self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def getPluginIdentifier(self):
        return 'dailymotion'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "?([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl;
        
    def __getKey(self):
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'fkzd="(.+?)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.','%2E')
            return aResult

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://dai.ly/', '')
        self.__sUrl = self.__sUrl.replace('http://www.dailymotion.com/', '')
        self.__sUrl = self.__sUrl.replace('embed/', '')
        self.__sUrl = self.__sUrl.replace('video/', '')
        self.__sUrl = self.__sUrl.replace('sequence/', '')
        self.__sUrl = self.__sUrl.replace('swf/', '')
        self.__sUrl = 'http://www.dailymotion.com/embed/video/' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        url=[]
        qua=[]
        
        #oRequest = cRequestHandler(self.__sUrl)
        #sHtmlContent = oRequest.request()
        
        request = urllib2.Request(self.__sUrl)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        request.add_header('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        request.add_header('Cookie', "ff=off") #supprime le filtre parental
          
        try: 
            reponse = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print e.read()
            print e.reason
            
        sHtmlContent = reponse.read()
        reponse.close()

        sHtmlContent=sHtmlContent.replace("\/","\\")
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        #print self.__sUrl
        
        oParser = cParser()
        
        sPattern =  '"live_rtsp_url":"(.+?)"'    
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url.append(aResult[1][0])
            qua.append('live')

        sPattern =  '"stream_h264_hd1080_url":"(.+?)"'    
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url.append(aResult[1][0])
            qua.append('1080p')

        sPattern =  '"stream_h264_hd_url":"(.+?)"'    
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url.append(aResult[1][0])
            qua.append('720p')
   
        sPattern =  '"stream_h264_hq_url":"(.+?)"'         
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url.append(aResult[1][0])
            qua.append('high')
               
        sPattern =  '"stream_h264_url":"(.+?)"'           
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url.append(aResult[1][0])
            qua.append('low')

        sPattern =  '"stream_h264_ld_url":"(.+?)"'           
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url.append(aResult[1][0])
            qua.append('low 2')

        aResult = re.findall(r'{"type":"application\\x-mpegURL","url":"(.+?)"}', sHtmlContent)
        if (aResult):
            url.append(aResult[0])
            qua.append('Live')

        #pattern plus generaliste
        aResult = re.findall(r'"([0-9]+)":\[{"type":"video\\mp4","url":"(.+?)"}]', sHtmlContent)
        if (aResult):
            for aEntry in aResult:
                url.append(aEntry[1])
                qua.append(str(aEntry[0]) + 'p')

 
        if (url):
            cConfig().showInfo(self.__sDisplayName, 'Streaming')
             
            dialog2 = xbmcgui.Dialog()
            ret = dialog2.select('Select Quality',qua)
            if (ret > -1):
                return True, url[ret]
            else:
                return False, False
        else:
            cConfig().showInfo(self.__sDisplayName, 'Fichier introuvable')
            return False, False
        
        return False, False
