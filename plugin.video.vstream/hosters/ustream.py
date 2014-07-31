from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from hosters.hoster import iHoster
import logger

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Ustream.tv'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName

    def getPluginIdentifier(self):
        return 'ustream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
	oRequestHandler = cRequestHandler(self.__sUrl)
	sHtmlContent = oRequestHandler.request()

	sAmfUrl = self.__getAmfUrl(sHtmlContent)
	logger.info('amf: ' + str(sAmfUrl))
	if (sAmfUrl == False):
	    return False, ''
	
	oRequestHandler = cRequestHandler(sAmfUrl)
	oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
	sAmfContent = oRequestHandler.request()

	sRtmp = self.__getRtmp(sAmfContent)
	logger.info('rtmp: ' + str(sRtmp))
	if (sRtmp == False):
	    return False, ''
	
	sTcUrl = self.__getTcUrl(sAmfContent)
	logger.info('tcurl: ' + str(sTcUrl))
	if (sTcUrl == False):
	    return False, ''
	
	sPlayPath = self.__getPlayPath(sAmfContent)
	logger.info('playpath: ' + str(sPlayPath))
	if (sPlayPath == False):
	    return False, ''

	sPageUrl = self.__getPageUrl()
	logger.info('pageurl: ' + str(sPageUrl))
	if (sPageUrl == False):
	    return False, ''
	
	sApp = self.__getApp(sTcUrl)
	logger.info('app: ' + str(sApp))
	if (sApp == False):
	    return False, ''
	
	sSwf = self.__getSwf(sHtmlContent)
	logger.info('swf: ' + str(sSwf))
	if (sSwf == False):
	    return False, ''
	
	sMediaLink = sRtmp + ' app=' + sApp + ' pageUrl=' + sPageUrl + ' swfUrl=' + sSwf + ' playpath=' + sPlayPath + ' live=true' + ' tcUrl=' + sTcUrl
	logger.info('medialink: ' + str(sMediaLink))
	
	return True, sMediaLink

    def __getAmfUrl(self, sHtmlContent):
	sPattern = "channelid: '(.*?)'"

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	if (aResult[0] == True):
	    sChannelId = aResult[1][0]	    
	    return 'http://cdngw.ustream.tv/Viewer/getStream/1/' + str(sChannelId) +'.amf'

	return False


    def __getRtmp(self, sHtmlContent):
	sPattern = 'fmsUrl\W\W\S(.+?)\x00'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	if (aResult[0] == True):
	    sTemp = aResult[1][0]
	    sTemp = sTemp.replace('/ustreamVideo', ':1935/ustreamVideo') + '/'
	    return sTemp

	return False

    def __getTcUrl(self, sHtmlContent):
	sPattern = 'fmsUrl\W\W\S(.+?)\x00'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	if (aResult[0] == True):
	    sTemp = aResult[1][0]
	    sTemp = sTemp.replace('/ustreamVideo', ':1935/ustreamVideo')
	    return sTemp

	return False

    def __getPlayPath(self, sHtmlContent):
	# immer streams/live   ignore result from amf
	return 'streams/live'

	sPattern = 'streamName\W\W\W(.+?)\x00'
	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	if (aResult[0] == True):	    
	    return aResult[1][0]

	return False


    def __getApp(self, sUrl):
	sTemp = sUrl.replace('rtmp://', '')
	aSplit = sTemp.split('/')
	
	if (len(aSplit) > 1):	    
	    return str(aSplit[1]) + '/' + str(aSplit[2])
	return False

    def __getPageUrl(self):
	return self.__sUrl

    def __getSwf(self, sHtmlContent):
	sPattern = 'movie: "([^"]+)"'
	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	if (aResult[0] == True):
	    sTemp = str(aResult[1][0])
	    aTemp = sTemp.split('.swf?')	    
	    return str(aTemp[0]) + '.swf'

	return False