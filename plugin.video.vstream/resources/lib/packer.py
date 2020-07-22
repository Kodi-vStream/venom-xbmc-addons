# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

#
# Modified version From https://github.com/Kodi-vStream/venom-xbmc-addons
#
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

import re

from resources.lib.util import Unquote


class cPacker():
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,')

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = self._filterargs(source)

        # correction pour eviter bypass
        if (len(symtab) > count) and (count > 0):
            del symtab[count:]
        if (len(symtab) < count) and (count > 0):
            symtab.append('BUGGED')

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return self._replacestrings(source)

    def _cleanstr(self, str):
        str = str.strip()
        if str.find("function") == 0:
            pattern = (r"=\"([^\"]+).*}\s*\((\d+)\)")
            args = re.search(pattern, str, re.DOTALL)
            if args:
                a = args.groups()
                def openload_re(match):
                    c = match.group(0)
                    b = ord(c) + int(a[1])
                    return chr(b if (90 if c <= "Z" else 122) >= b else b - 26)

                str = re.sub(r"[a-zA-Z]", openload_re, a[0])
                str = Unquote(str)

        elif str.find("decodeURIComponent") == 0:
            str = re.sub(r"(^decodeURIComponent\s*\(\s*('|\"))|(('|\")\s*\)$)", "", str)
            str = Unquote(str)
        elif str.find("\"") == 0:
            str = re.sub(r"(^\")|(\"$)|(\".*?\")", "", str)
        elif str.find("'") == 0:
            str = re.sub(r"(^')|('$)|('.*?')", "", str)

        return str

    def _filterargs(self, source):
        """Juice from a source file the four args needed by decoder."""

        source = source.replace(',[],',',0,')

        juicer = (r"}\s*\(\s*(.*?)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\((.*?)\).split\((.*?)\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return self._cleanstr(a[0]), self._cleanstr(a[3]).split(self._cleanstr(a[4])), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        juicer = (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('(.*?)'\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return a[0], a[3].split(a[4]), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')

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
    # Badly packed source or general error.#
    print(Exception)
    pass


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base

        # Error not possible, use 36 by defaut
        if base == 0:
            base = 36

        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
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
