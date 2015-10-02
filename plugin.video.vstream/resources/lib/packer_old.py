#
# Unpacker for Dean Edward's p.a.c.k.e.r, a part of javascript beautifier
# by Einar Lielmanis <einar@jsbeautifier.org>
#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#
# usage:
#
# if detect(some_string):
#     unpacked = unpack(some_string)
#

"""Unpacker for Dean Edward's p.a.c.k.e.r"""

import re,urllib2
import string

PRIORITY = 1

class cPacker():
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,')

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        if 'letwatch' in source:
            payload, symtab, radix, count = self._filterargs2(source)
        else :
            payload, symtab, radix, count = self._filterargs(source)

        if count != len(symtab):
            raise self.UnpackingError('Malformed p.a.c.k.e.r. symtab.')

        try:
            
            unbase = Unbaser(radix)
        except TypeError:
            raise self.UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word  = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return self._replacestrings(source)

    def _cleanstr(self, str):
        str = str.strip()
        if str.find("decodeURIComponent") == 0:
            str = re.sub(r"^decodeURIComponent\s*\(\s*('|\")", "", str);
            str = re.sub(r"('|\")\s*\)$", "", str);
            str = urllib2.unquote(str)
        else:
            if str.find("\"") == 0:
                str = re.sub(r"(^\")|(\"$)|(\".*?\")", "", str);
            elif str.find("'") == 0:
                str = re.sub(r"(^')|('$)|('.*?')", "", str);

        return str

    def _filterargs(self, source):
        """decode openload"""

        juicer = (r"}\s*\(\s*([^,]*)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\((.*?)\).split\((.*?)\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return self._cleanstr(a[0]), self._cleanstr(a[3]).split(self._cleanstr(a[4])), int(a[1]), int(a[2])
            except ValueError:
                raise self.UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise self.UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')
        
    def _filterargs2(self, source):
        """Decode letwatch"""
        juicers = [ (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('\|'\), *(\d+), *(.*)\)\)"),
                    (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('\|'\)"),
                  ]
        for juicer in juicers:
            args = re.search(juicer, source, re.DOTALL)
            if args:
                a = args.groups()
                try:
                    return a[0], a[3].split('|'), int(a[1]), int(a[2])
                except ValueError:
                    raise self.UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise self.UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')



    def _replacestrings(self, source):
        """Strip string lookup table (list) and replace values in source."""
        match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

        if match:
            varname, strings = match.groups()
            startpoint = len(match.group(0))
            lookup = strings.split('","')
            variable = '%s[%%d]' % varname
            for index, value in enumerate(lookup):
                source = source.replace(variable % index, '"%s"' % value)
            return source[startpoint:]
        return source
        
    def UnpackingError(Exception):
    #Badly packed source or general error.#
        print Exception
        pass


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET  = {
        36 : '0123456789abcdefghijklmnopqrstuvwxyz',
        52 : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP',
        54 : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQR',
        62 : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95 : (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
              '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base


        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for
                    index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret