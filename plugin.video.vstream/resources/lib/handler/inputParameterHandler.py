import urllib
import sys

class cInputParameterHandler:

    def __init__(self):          
            aParams = dict()
            if len(sys.argv)>=2 and len(sys.argv[2])>0:
                    aParams = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
          
            self.__aParams = aParams

    def getAllParameter(self):
            return self.__aParams

    def getValue(self, sParamName):
            if (self.exist(sParamName)):
                    sParamValue = self.__aParams[sParamName]                    
                    return urllib.unquote_plus(sParamValue)
            return False

    def exist(self, sParamName):
            return self.__aParams.has_key(sParamName)