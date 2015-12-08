#-*- coding: utf-8 -*-
import re

class cParser:

    def parseSingleResult(self, sHtmlContent, sPattern):     
	aMatches = re.compile(sPattern).findall(sHtmlContent)
	if (len(aMatches) == 1):
                aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
		return True, aMatches[0]
        return False, aMatches

    def __replaceSpecialCharacters(self, sString):
        return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'")

    def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
        if (len(aMatches) >= iMinFoundValue):                
            return True, aMatches
        return False, aMatches

    def replace(self, sPattern, sReplaceString, sValue):
         return re.sub(sPattern, sReplaceString, sValue)

    def escape(self, sValue):
        return re.escape(sValue)
    
    def getNumberFromString(self, sValue):
        sPattern = "\d+"
        aMatches = re.findall(sPattern, sValue)
        if (len(aMatches) > 0):
            return aMatches[0]
        return 0


