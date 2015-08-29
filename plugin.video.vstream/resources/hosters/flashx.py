from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2
import xbmcgui

#meme code que vodlocker

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'FlashX'
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

    def getPluginIdentifier(self):
        return 'flashx'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://((?:www.|play.)?flashx.tv)/(?:embed-)?([0-9a-zA-Z/-]+)(?:.html)?"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        urlhash = re.search('([a-zA-Z0-9]+)(?:-+[0-9]+[xX]+[0-9]+)', media_id)
        if urlhash:
            media_id = urlhash.group(1)
        return 'http://www.flashx.tv/player-%s.html' % media_id

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        sId = self.__getIdFromUrl(self.__sUrl)
        #web_url = self.__getUrl(sId)
        
        web_url = 'http://www.flashx.tv/player-%s.html' % sId

        headers = {
        'Host' : 'www.flashx.tv',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer':'http://embed.flashx.tv/embed.php?c=b03lgzlufx06&w=710&h=360',
        }
        
        smil = ''
        api_call = ''

        request = urllib2.Request(web_url,None,headers)
      
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
            

        html = reponse.read()
          
        #fh = open('c:\\test.txt', "w")
        #fh.write(html)
        #fh.close()
        
        swfurl = 'http://static.flashx.tv/player6/jwplayer.flash.swf'
        r = re.search('"(http://.+?\.smil)"', html)
        
        if r:
            smil = r.group(1)
        else:
            r = re.search('\|smil\|+(.+?)\|sources\|', html)
            if r:
                smil = 'http://flashx.tv/' + r.group(1) + '.smil'

        if smil:

            request = urllib2.Request(smil,None,headers)
      
            try: 
                reponse = urllib2.urlopen(request)
            except URLError, e:
                print e.read()
                print e.reason
            
            html = reponse.read()
            
            r = re.search('<meta base="(rtmp://.*?flashx\.tv:[0-9]+/)(.+/)".*/>', html, re.DOTALL)
            if r:
                rtmp = r.group(1)
                app = r.group(2)
                sources = re.compile('<video src="(.+?)" height="(.+?)" system-bitrate="(.+?)" width="(.+?)".*/>').findall(html)
                vid_list = []
                url_list = []
                best = 0
                quality = 0
                if sources:
                    #print sources
                    #return
                    if len(sources) > 1:
                        for index, video in enumerate(sources):
                            if int(video[1]) > quality: best = index
                            quality = int(video[1])
                            vid_list.extend(['FlashX - %sp' % quality])
                            url_list.extend([video[0]])
                if len(sources) == 1:
                    vid_sel = sources[0][0]
                else:
                    result = xbmcgui.Dialog().select('Choose a link', vid_list)
                    if result != -1: vid_sel = url_list[result]
                    else: return self.unresolvable(code=0, msg='No link selected')

                if vid_sel:
                    api_call = '%s app=%s playpath=%s swfUrl=%s pageUrl=%s swfVfy=true' % (rtmp, app, vid_sel, swfurl, web_url)


        if (api_call):
            return True, api_call
            
        return False, False
        
        
