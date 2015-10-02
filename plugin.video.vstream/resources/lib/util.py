import re
import urllib
import xbmc
import xbmcgui
import htmlentitydefs

class cUtil:

    def removeHtmlTags(self, sValue, sReplace = ''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)


    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)

        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if (iSeconds < 10):
            iSeconds = '0' + str(iSeconds)

        if (iMinutes < 10):
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def urlDecode(self, sUrl):
        return urllib.unquote(sUrl)

    def urlEncode(self, sUrl):
        return urllib.quote(sUrl)

    def unquotePlus(self, sUrl):
        return urllib.unquote_plus(sUrl)

    def quotePlus(self, sUrl):
        return urllib.quote_plus(sUrl)
        
    def dialog(self, sName):
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sName)
        return oDialog
        
    def DecoTitle(self, string):
        #pr les tag
        string = re.sub('([\[\(](?![0-9]{4}).{1,7}[\)\]])',' [COLOR coral]\\1[/COLOR] ', str(string))
        #pr les episodes
        SXEX = ''
        m = re.search('(?i)(.pisode ([0-9]+))', string)
        if m:
            string = string.replace(m.group(1),'')
            SXEX = 'E' + "%02d" % int(m.group(2))
            
            #pr les saisons
            m = re.search('(?i)(saison ([0-9]+))', string)
            if m:
                string = string.replace(m.group(1),'')
                SXEX = 'S' + "%02d" % int(m.group(2)) + SXEX
            
            string = re.sub(' +',' ',string)
            string = string + ' [COLOR coral] ' + SXEX + '[/COLOR] '
        
        else:
            string = re.sub('(?i)(.*)(saison [0-9]+)','\\1 [COLOR coral]\\2[/COLOR] ', str(string))
            
        return string

    def unescape(self,text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)
            
            
