# !/usr/bin/python
# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

"""
    Modified version from

    Copyright (C) 2016 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import string

from resources.lib.util import Quote, Unquote


class JSUnfuck(object):
    numbers = None
    words = {
        "(![]+[])": "false",
        "([]+{})": "[object Object]",
        "(!![]+[])": "true",
        "([][[]]+[])": "undefined",
        "(+{}+[])": "NaN",
        "([![]]+[][[]])": "falseundefined",
        "([][f+i+l+t+e+r]+[])": "function filter() { [native code] }",
        "(!![]+[][f+i+l+t+e+r])": "truefunction filter() { [native code] }",
        "(+![]+([]+[])[c+o+n+s+t+r+u+c+t+o+r])": "0function String() { [native code] }",
        "(+![]+[![]]+([]+[])[c+o+n+s+t+r+u+c+t+o+r])": "0falsefunction String() { [native code] }",
        "([]+[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +l+o+c+a+t+i+o+n)())": "https://123movies.to",
        "([]+[])[f+o+n+t+c+o+l+o+r]()": '<font color="undefined"></font>',
        "(+(+!![]+e+1+0+0+0)+[])": "Infinity",
        "(+[![]]+[][f+i+l+t+e+r])": 'NaNfunction filter() { [native code] }',
        '(+[![]]+[+(+!+[]+(!+[]+[])[3]+[1]+[0]+[0]+[0])])': 'NaNInfinity',
        '([]+[])[i+t+a+l+i+c+s]()': '<i></i>',
        '[[]][c+o+n+c+a+t]([[]])+[]': ',',
        '([][f+i+l+l]+[])': 'function fill() {    [native code]}',
        '(!![]+[][f+i+l+l])': 'truefunction fill() {    [native code]}',
        '((+[])[c+o+n+s+t+r+u+c+t+o+r]+[])': 'function Number() {[native code]}  _display:45:1',
        '(+(+!+[]+[1]+e+[2]+[0])+[])': '1.1e+21',
        '([]+[])[c+o+n+s+t+r+u+c+t+o+r][n+a+m+e]': 'S+t+r+i+n+g',
        '([][e+n+t+r+i+e+s]()+[])': '[object Array Iterator]',
        '([]+[])[l+i+n+k](")': '<a href="&quot;"></a>',
        '(![]+[0])[i+t+a+l+i+c+s]()': '<i>false0</i>',
        # dummy to force array dereference
        'DUMMY1': '6p',
        'DUMMY2': '2x',
        'DUMMY3': '%3C',
        'DUMMY4': '%5B',
        'DUMMY5': '6q',
        'DUMMY6': '4h',
    }

    uniqs = {
        '[t+o+S+t+r+i+n+g]': 1,
        '[][f+i+l+t+e+r][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +e+s+c+a+p+e)()': 2,
        '[][f+i+l+t+e+r][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +u+n+e+s+c+a+p+e)()': 3,
        '[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +e+s+c+a+p+e)()': 2,
        '[][s+o+r+t][c+o+n+s+t+r+u+c+t+o+r](r+e+t+u+r+n+ +u+n+e+s+c+a+p+e)()': 3,
    }

    def __init__(self, js):
        self.js = js

    def decode(self, replace_plus=True):
        while True:
            start_js = self.js
            self.repl_words(self.words)
            self.repl_numbers()
            self.repl_arrays(self.words)
            self.repl_uniqs(self.uniqs)
            if start_js == self.js:
                break

        if replace_plus:
            self.js = self.js.replace('+', '')
        self.js = re.sub('\[[A-Za-z]*\]', '', self.js)
        self.js = re.sub('\[(\d+)\]', '\\1', self.js)

        # foutu ici pr le moment
        self.js = self.js.replace('(+)', '0')
        self.js = self.js.replace('(+!!)', '1')

        return self.js

    def repl_words(self, words):
        while True:
            start_js = self.js
            for key, value in sorted(words.items(), key=lambda x: len(x[0]), reverse=True):
                self.js = self.js.replace(key, value)

            if self.js == start_js:
                break

    def repl_arrays(self, words):
        for word in sorted(words.values(), key=lambda x: len(x), reverse=True):
            for index in range(0, 100):
                try:
                    repl = word[index]
                    self.js = self.js.replace('%s[%d]' % (word, index), repl)
                except:
                    pass

    def repl_numbers(self):
        if self.numbers is None:
            self.numbers = self.__gen_numbers()

        while True:
            start_js = self.js
            for key, value in sorted(self.numbers.items(), key=lambda x: len(x[0]), reverse=True):
                self.js = self.js.replace(key, value)

            if self.js == start_js:
                break

    def repl_uniqs(self, uniqs):
        for key, value in uniqs.items():
            if key in self.js:
                if value == 1:
                    self.__handle_tostring()
                elif value == 2:
                    self.__handle_escape(key)
                elif value == 3:
                    self.__handle_unescape(key)

    def __handle_tostring(self):
        for match in re.finditer('(\d+)\[t\+o\+S\+t\+r\+i\+n\+g\](\d+)', self.js):
            repl = to_base(match.group(1), match.group(2))
            self.js = self.js.replace(match.group(0), repl)

    def __handle_escape(self, key):
        while True:
            start_js = self.js
            offset = self.js.find(key) + len(key)
            if self.js[offset] == '(' and self.js[offset + 2] == ')':
                c = self.js[offset + 1]
                self.js = self.js.replace('%s(%s)' % (key, c), Quote(c))

            if start_js == self.js:
                break

    def __handle_unescape(self, key):
        start = 0
        while True:
            start_js = self.js
            offset = self.js.find(key, start)
            if offset == -1:
                break

            offset += len(key)
            expr = ''
            extra = ''
            last_c = self.js[offset - 1]
            abort = False
            for i, c in enumerate(self.js[offset:]):
                extra += c
                if c == ')':
                    break
                elif (i > 0 and c == '(') or (c == '[' and last_c != '+'):
                    abort = True
                    break
                elif c == '%' or c in string.hexdigits:
                    expr += c
                last_c = c

            if not abort:
                self.js = self.js.replace(key + extra, Unquote(expr))

                if start_js == self.js:
                    break
            else:
                start = offset

    def __gen_numbers(self):
        n = {'(+[]+[])': '0', '(+![]+([]+[]))': '0', '[+[]]': '[0]',
             '(+!![]+[])': '1', '[+!+[]]': '[1]', '[+!![]]': '[1]',
             '[+!+[]+[+[]]]': '[10]', '+(1+1)': '11', '(+20)': '20'}

        for i in range(2, 20):
            key = '+!![]' * (i - 1)
            key = '!+[]' + key
            n['(' + key + ')'] = str(i)
            key += '+[]'
            n['(' + key + ')'] = str(i)
            n['[' + key + ']'] = '[' + str(i) + ']'

        for i in range(2, 10):
            key = '!+[]+' * (i - 1) + '!+[]'
            n['(' + key + ')'] = str(i)
            n['[' + key + ']'] = '[' + str(i) + ']'

            key = '!+[]' + '+!![]' * (i - 1)
            n['[' + key + ']'] = '[' + str(i) + ']'

        for i in range(0, 10):
            key = '(+(+!+[]+[%d]))' % (i)
            n[key] = str(i + 10)
            key = '[+!+[]+[%s]]' % (i)
            n[key] = '[' + str(i + 10) + ']'

        for tens in range(2, 10):
            for ones in range(0, 10):
                key = '!+[]+' * (tens) + '[%d]' % (ones)
                n['(' + key + ')'] = str(tens * 10 + ones)
                n['[' + key + ']'] = '[' + str(tens * 10 + ones) + ']'

        for hundreds in range(1, 10):
            for tens in range(0, 10):
                for ones in range(0, 10):
                    key = '+!+[]' * hundreds + '+[%d]+[%d]))' % (tens, ones)
                    if hundreds > 1:
                        key = key[1:]
                    key = '(+(' + key
                    n[key] = str(hundreds * 100 + tens * 10 + ones)
        return n


def to_base(n, base, digits="0123456789abcdefghijklmnopqrstuvwxyz"):
    n, base = int(n), int(base)
    if n < base:
        return digits[n]
    else:
        return to_base(n // base, base, digits).lstrip(digits[0]) + digits[n % base]
