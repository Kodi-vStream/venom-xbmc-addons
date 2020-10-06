# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
try:
    import htmlentitydefs
    import urllib
    import urllib2

except ImportError:
    import html.entities as htmlentitydefs
    import urllib.parse as urllib
    import urllib.request as urllib2

import unicodedata
import re
# function util n'utilise pas xbmc, xbmcgui, xbmcaddon ect...

class cUtil:
    # reste a transformer la class en fonction distante.

    def CheckOrd(self, label):
        count = 0
        try:
            label = label.lower()
            label = label.strip()
            label = unicode(label, 'utf-8')
            label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore')
            for i in label:
                count += ord(i)
        except:
            pass

        return count

    def CheckOccurence(self, str1, str2):
        ignoreListe = ['3d', 'la', 'le', 'les', 'un', 'une', 'de', 'des', 'du', 'en', 'a', 'au', 'aux', 'the', 'in', 'and', 'mais', 'ou', 'no', 'dr', 'contre', 'qui',
                       'et', 'donc', 'or', 'ni', 'ne', 'pas', 'car', 'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles', 'i', 'you', 'he', 'she', 'we', 'they']

        str1 = str1.replace('+', ' ').replace('%20', ' ').replace(':', ' ').replace('-', ' ')
        str2 = str2.replace(':', ' ').replace('-', ' ')
        str1 = self.CleanName(str1)
        str2 = self.CleanName(str2)

        i = 0
        list2 = str2.split(' ')     # Comparaison mot à mot
        for part in str1.split(' '):
            if part in ignoreListe: # Mots à ignorer
                continue
            if len(part) == 1:      # Ignorer une seule lettre
                continue
            if part in list2:
                i += 1              # Nombre de mots correspondants
        return i

    def removeHtmlTags(self, sValue, sReplace=''):
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

    def DecoTitle2(self, string):

        # on vire ancienne deco en cas de bug
        string = re.sub('\[\/*COLOR.*?\]', '', str(string))

        # pr les tag Crochet
        string = re.sub('([\[].+?[\]])',' [COLOR coral]\\1[/COLOR] ', string)
        # pr les tag parentheses
        string = re.sub('([\(](?![0-9]{4}).{1,7}[\)])', ' [COLOR coral]\\1[/COLOR] ', string)
        # pr les series
        string = self.FormatSerie(string)
        string = re.sub('(?i)(.*) ((?:[S|E][0-9\.\-\_]+){1,2})', '\\1 [COLOR coral]\\2[/COLOR] ', string)

        # vire doubles espaces
        string = re.sub(' +', ' ', string)

        return string

    def unescape(self, text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == '&#':
                # character reference
                try:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
                except NameError:
                    if text[:3] == '&#x':
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
                except NameError:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])

            return text  # leave as is
        return re.sub('&#?\w+;', fixup, text)

    def CleanName(self, name):
        # vire accent et '\'
        try:
            name = unicode(name, 'utf-8')  # converti en unicode pour aider aux convertions
        except:
            pass

        try:
            name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('unicode_escape')
            name = name.encode('utf-8') #on repasse en utf-8
        except TypeError:
            #name = unicodedata.normalize('NFKD', name.decode("utf-8")).encode('ASCII', 'ignore')
            pass

        #on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee, '')

        # vire tag
        name = re.sub('[\(\[].+?[\)\]]', '', name)
        # les apostrophes remplacer par des espaces
        name = name.replace("'", " ")
        # vire caractere special
        # name = re.sub('[^a-zA-Z0-9 ]', '', name)
        name = re.sub('[^a-zA-Z0-9 : -]', '', name)
        # tout en minuscule
        name = name.lower()
        # vire espace debut et fin
        name = name.strip()
        # vire espace double au milieu
        name = re.sub(' +', ' ', name)

        # on remet l'annee
        if annee:
            name = name + ' ' + annee

        return name

    def FormatSerie(self, string):

        # vire doubles espaces
        string = re.sub(' +', ' ', string)

        # vire espace a la fin
        if string.endswith(' '):
            string = string[:-1]

        # vire espace au debut
        if string.startswith(' '):
            string = string[1:]

        # convertion unicode
        try:
            string = string.decode('utf-8')
        except AttributeError:
            pass

        SXEX = ''
        m = re.search('(?i)(\wpisode ([0-9\.\-\_]+))', string, re.UNICODE)
        if m:
            # ok y a des episodes
            string = string.replace(m.group(1), '')
            # SXEX + '%02d' % int(m.group(2))
            SXEX = m.group(2)
            if len(SXEX) < 2:
                SXEX = '0' + SXEX
            SXEX = 'E' + SXEX

            # pr les saisons
            m = re.search('(?i)(s(?:aison )*([0-9]+))', string)
            if m:
                string = string.replace(m.group(1), '')
                SXEX = 'S' + '%02d' % int(m.group(2)) + SXEX
            string = string + ' ' + SXEX

        else:
            # pas d'episode mais y a t il des saisons ?
            m = re.search('(?i)(s(?:aison )*([0-9]+))(?:$| )', string)
            if m:
                string = string.replace(m.group(1), '')
                SXEX = 'S' + '%02d' % int(m.group(2))

                string = string + ' ' + SXEX

        # reconvertion utf-8
        return string.encode('utf-8')

    def EvalJSString(self, s):
        s = s.replace(' ', '')
        try:
            s = s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0')
            s = re.sub(r'(\([^()]+)\+\[\]\)', '(\\1)*10)', s)  # si le bloc fini par +[] >> *10
            s = re.sub(r'\[([^\]]+)\]', 'str(\\1)', s)
            if s[0] == '+':
                s = s[1:]
            val = int(eval(s))
            return val
        except:
            return 0


"""
# ***********************
# Fonctions lights
# ***********************
# Pour les avoirs
# from resources.lib import util
# puis util.VSlog('test')
"""


def Unquote(sUrl):
    return urllib.unquote(sUrl)


def Quote(sUrl):
    return urllib.quote(sUrl)


def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)


def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)


def QuoteSafe(sUrl):
    return urllib.quote(sUrl, safe=':/')


def urlEncode(sUrl):
    return urllib.urlencode(sUrl)


def Noredirection():
    class NoRedirection(urllib2.HTTPErrorProcessor):
        def http_response(self, request, response):
            return response

        https_response = http_response

    opener = urllib2.build_opener(NoRedirection)
    return opener

# deprecier utiliser comaddon dialog()
# def updateDialogSearch(dialog, total, site):
#     global COUNT
#     COUNT += 1
#     iPercent = int(float(COUNT * 100) / total)
#     dialog.update(iPercent, 'Chargement: ' + str(site))


# def VStranslatePath(location):
#     # ex util.VStranslatePath('special://logpath/') > http://kodi.wiki/view/Special_protocol
#     # d'apres Kodi ne doit pas etre utiliser sur les special://
#     return xbmc.translatePath(location).decode('utf-8')


def GetGooglUrl(url):
    if 'http://goo.gl' in url:
        try:
            headers = {'User-Agent': 'Mozilla 5.10', 'Host': 'goo.gl', 'Connection': 'keep-alive'}
            request = urllib2.Request(url, None, headers)
            reponse = urllib2.urlopen(request)
            url = reponse.geturl()
        except:
            pass
    return url
