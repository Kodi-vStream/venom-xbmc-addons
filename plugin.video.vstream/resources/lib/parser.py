# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re


class cParser:

    def parseSingleResult(self, sHtmlContent, sPattern):
        aMatches = re.compile(sPattern).findall(sHtmlContent)
        if (len(aMatches) == 1):
            aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
            return True, aMatches[0]
        return False, aMatches

    def __replaceSpecialCharacters(self, sString):
        """ /!\ pas les mêmes tirets, tiret moyen et cadratin."""
        return sString.replace('\r', '').replace('\n', '').replace('\t', '').replace('\\/', '/').replace('&amp;', '&')\
                      .replace('&#039;', "'").replace('&#8211;', '-').replace('&#8212;', '-').replace('&eacute;', 'é')\
                      .replace('&acirc;', 'â').replace('&ecirc;', 'ê').replace('&icirc;', 'î').replace('&ocirc;', 'ô')\
                      .replace('&hellip;', '...').replace('&quot;', '"').replace('&gt;', '>').replace('&egrave;', 'è')\
                      .replace('&ccedil;', 'ç').replace('&laquo;', '<<').replace('&raquo;', '>>').replace('\xc9', 'E')\
                      .replace('&ndash;', '-').replace('&eacute;', 'é').replace('&agrave;', 'à').replace('&lt;', '<')\
                      .replace('&rsquo;', "'").replace('&lsquo;', '\'').replace('&nbsp;', '').replace('&#8217;', "'")\
                      .replace('&#8230;', '...').replace('&#8242;', "'").replace('&#884;', '\'')\
                      .replace('&#038;', '&').replace('–', '-').replace('—', '-')

    def parse(self, sHtmlContent, sPattern, iMinFoundValue=1):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)

        # extrait la page html après retraitement vStream
        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        if (len(aMatches) >= iMinFoundValue):
            return True, aMatches
        return False, aMatches

    def replace(self, sPattern, sReplaceString, sValue):
        return re.sub(sPattern, sReplaceString, sValue)

    def escape(self, sValue):
        return re.escape(sValue)

    def getNumberFromString(self, sValue):
        if '/0-9/' in sValue:
            sPattern = '/0-9.+?(\d+)'
        else:
            sPattern = '\d+'
        aMatches = re.findall(sPattern, sValue)
        if (len(aMatches) > 0):
            return aMatches[0]
        return 0

    def titleParse(self, sHtmlContent, sPattern):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE)
        try:
            [m.groupdict() for m in aMatches.finditer(sHtmlContent)]
            return m.groupdict()
        except:
            return {'title': sHtmlContent}

    def abParse(self, sHtmlContent, start, end, startoffset=0):
        # usage oParser.abParse(sHtmlContent, 'start', 'end')
        # startoffset (int) décale le début pour ne pas prendre en compte start dans le résultat final si besoin
        # la fin est recherchée forcement après le début
        # usage2 oParser.abParse(sHtmlContent, 'start', 'end', 6)
        # ex youtube.py
        
        startIdx = sHtmlContent.find(start)
        endIdx = sHtmlContent[startoffset + startIdx : ].find(end)
        return sHtmlContent[startoffset + startIdx : startoffset + startIdx + endIdx]
