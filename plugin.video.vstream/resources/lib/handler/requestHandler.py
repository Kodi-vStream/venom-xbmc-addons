import urllib
import urllib2


class cRequestHandler:
    REQUEST_TYPE_GET = 0
    REQUEST_TYPE_POST = 1
      
    def __init__(self, sUrl):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__aParamaters = {}
        self.__aHeaderEntries = []
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self.__cType = cType

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        aHeader = {sHeaderKey : sHeaderValue}
        self.__aHeaderEntries.append(aHeader)

    def addParameters(self, sParameterKey, mParameterValue):
        self.__aParamaters[sParameterKey] = mParameterValue

    def getResponseHeader(self):
        return self.__sResponseHeader

    # url after redirects
    def getRealUrl(self):
        return self.__sRealUrl;

    def request(self):
        self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest()

    def getRequestUri(self):
        return self.__sUrl + '?' + urllib.urlencode(self.__aParamaters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        self.addHeaderEntry('Accept-Language', 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self):
        sParameters = urllib.urlencode(self.__aParamaters)

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        if (len(sParameters) > 0):
            oRequest = urllib2.Request(self.__sUrl, sParameters)
        else:
            oRequest = urllib2.Request(self.__sUrl)

        for aHeader in self.__aHeaderEntries:                
                for sHeaderKey, sHeaderValue in aHeader.items():
                    oRequest.add_header(sHeaderKey, sHeaderValue)

	try:
		oResponse = urllib2.urlopen(oRequest)               
	except:
		for aHeader in self.__aHeaderEntries:
                    for sHeaderKey, sHeaderValue in aHeader.items():
                        oRequest.add_header(sHeaderKey, sHeaderValue)
		oResponse = urllib2.urlopen(oRequest)

	sContent = oResponse.read()
        if (self.__bRemoveNewLines == True):
            sContent = sContent.replace("\n","")
            sContent = sContent.replace("\r\t","")

        if (self.__bRemoveBreakLines == True):
            sContent = sContent.replace("&nbsp;","")

        self.__sResponseHeader = oResponse.info()
        self.__sRealUrl = oResponse.geturl()
        
        oResponse.close()
	return sContent

    def getHeaderLocationUrl(self):        
        opened = urllib.urlopen(self.__sUrl)
        return opened.geturl()


