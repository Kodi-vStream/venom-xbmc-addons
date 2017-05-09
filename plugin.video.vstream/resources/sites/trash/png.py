#!/usr/bin/env python
#
#***********************************************************************************
#
# This file is a light version
# For the full file go to https://github.com/jcrocholl/pypng/blob/master/lib/png.py
#
#***********************************************************************************
#
#
# png.py - PNG encoder in pure Python
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Contributors (alphabetical):
# Nicko van Someren <nicko@nicko.org>
#
# Changelog (recent first):
# 2006-06-17 Nicko: Reworked into a class, faster interlacing.
# 2006-06-17 Johann: Very simple prototype PNG decoder.
# 2006-06-17 Nicko: Test suite with various image generators.
# 2006-06-17 Nicko: Alpha-channel, grey-scale, 16-bit/plane support.
# 2006-06-15 Johann: Scanline iterator interface for large input files.
# 2006-06-09 Johann: Very simple prototype PNG encoder.


"""
Pure Python PNG Reader/Writer

This is an implementation of a subset of the PNG specification at
http://www.w3.org/TR/2003/REC-PNG-20031110 in pure Python. It reads
and writes PNG files with 8/16/24/32/48/64 bits per pixel (greyscale,
RGB, RGBA, with 8 or 16 bits per layer), with a number of options. For
help, type "import png; help(png)" in your python interpreter.

This file can also be used as a command-line utility to convert PNM
files to PNG. The interface is similar to that of the pnmtopng program
from the netpbm package. Type "python png.py --help" at the shell
prompt for usage and a list of options.
"""


__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'


import sys
import zlib
import struct
import math
from array import array


_adam7 = ((0, 0, 8, 8),
          (4, 0, 8, 8),
          (0, 4, 4, 8),
          (2, 0, 4, 4),
          (0, 2, 2, 4),
          (1, 0, 2, 2),
          (0, 1, 1, 2))



class Error(Exception):
    pass


class _readable:
    """
    A simple file-like interface for strings and arrays.
    """

    def __init__(self, buf):
        self.buf = buf
        self.offset = 0

    def read(self, n):
        r = self.buf[self.offset:self.offset+n]
        if isinstance(r, array):
            r = r.tostring()
        self.offset += n
        return r


class Reader:
    """
    PNG decoder in pure Python.
    """

    def __init__(self, _guess=None, **kw):
        """
        Create a PNG decoder object.

        The constructor expects exactly one keyword argument. If you
        supply a positional argument instead, it will guess the input
        type. You can choose among the following arguments:
        filename - name of PNG input file
        file - object with a read() method
        pixels - array or string with PNG data

        """
        if ((_guess is not None and len(kw) != 0) or
            (_guess is None and len(kw) != 1)):
            raise TypeError("Reader() takes exactly 1 argument")

        if _guess is not None:
            if isinstance(_guess, array):
                kw["pixels"] = _guess
            elif isinstance(_guess, str):
                kw["filename"] = _guess
            elif isinstance(_guess, file):
                kw["file"] = _guess

        if "filename" in kw:
            self.file = file(kw["filename"], "rb")
        elif "file" in kw:
            self.file = kw["file"]
        elif "pixels" in kw:
            self.file = _readable(kw["pixels"])
        else:
            raise TypeError("expecting filename, file or pixels array")

    def read_chunk(self):
        """
        Read a PNG chunk from the input file, return tag name and data.
        """
        # http://www.w3.org/TR/PNG/#5Chunk-layout
        try:
            data_bytes, tag = struct.unpack('!I4s', self.file.read(8))
        except struct.error:
            raise ValueError('Chunk too short for header')
        data = self.file.read(data_bytes)
        if len(data) != data_bytes:
            raise ValueError('Chunk %s too short for required %i data octets'
                             % (tag, data_bytes))
        checksum = self.file.read(4)
        if len(checksum) != 4:
            raise ValueError('Chunk %s too short for checksum', tag)
        verify = zlib.crc32(tag)
        verify = zlib.crc32(data, verify)
        verify = struct.pack('!i', verify)
        if checksum != verify:
            # print repr(checksum)
            (a, ) = struct.unpack('!I', checksum)
            (b, ) = struct.unpack('!I', verify)
            raise ValueError("Checksum error in %s chunk: 0x%X != 0x%X"
                             % (tag, a, b))
        return tag, data

    def _reconstruct_sub(self, offset, xstep, ystep):
        """
        Reverse sub filter.
        """
        pixels = self.pixels
        a_offset = offset
        offset += self.psize * xstep
        if xstep == 1:
            for index in range(self.psize, self.row_bytes):
                x = pixels[offset]
                a = pixels[a_offset]
                pixels[offset] = (x + a) & 0xff
                offset += 1
                a_offset += 1
        else:
            byte_step = self.psize * xstep
            for index in range(byte_step, self.row_bytes, byte_step):
                for i in range(self.psize):
                    x = pixels[offset + i]
                    a = pixels[a_offset + i]
                    pixels[offset + i] = (x + a) & 0xff
                offset += self.psize * xstep
                a_offset += self.psize * xstep

    def _reconstruct_up(self, offset, xstep, ystep):
        """
        Reverse up filter.
        """
        pixels = self.pixels
        b_offset = offset - (self.row_bytes * ystep)
        if xstep == 1:
            for index in range(self.row_bytes):
                x = pixels[offset]
                b = pixels[b_offset]
                pixels[offset] = (x + b) & 0xff
                offset += 1
                b_offset += 1
        else:
            for index in range(0, self.row_bytes, xstep * self.psize):
                for i in range(self.psize):
                    x = pixels[offset + i]
                    b = pixels[b_offset + i]
                    pixels[offset + i] = (x + b) & 0xff
                offset += self.psize * xstep
                b_offset += self.psize * xstep

    def _reconstruct_average(self, offset, xstep, ystep):
        """
        Reverse average filter.
        """
        pixels = self.pixels
        a_offset = offset - (self.psize * xstep)
        b_offset = offset - (self.row_bytes * ystep)
        if xstep == 1:
            for index in range(self.row_bytes):
                x = pixels[offset]
                if index < self.psize:
                    a = 0
                else:
                    a = pixels[a_offset]
                if b_offset < 0:
                    b = 0
                else:
                    b = pixels[b_offset]
                pixels[offset] = (x + ((a + b) >> 1)) & 0xff
                offset += 1
                a_offset += 1
                b_offset += 1
        else:
            for index in range(0, self.row_bytes, self.psize * xstep):
                for i in range(self.psize):
                    x = pixels[offset+i]
                    if index < self.psize:
                        a = 0
                    else:
                        a = pixels[a_offset + i]
                    if b_offset < 0:
                        b = 0
                    else:
                        b = pixels[b_offset + i]
                    pixels[offset + i] = (x + ((a + b) >> 1)) & 0xff
                offset += self.psize * xstep
                a_offset += self.psize * xstep
                b_offset += self.psize * xstep

    def _reconstruct_paeth(self, offset, xstep, ystep):
        """
        Reverse Paeth filter.
        """
        pixels = self.pixels
        a_offset = offset - (self.psize * xstep)
        b_offset = offset - (self.row_bytes * ystep)
        c_offset = b_offset - (self.psize * xstep)
        # There's enough inside this loop that it's probably not worth
        # optimising for xstep == 1
        for index in range(0, self.row_bytes, self.psize * xstep):
            for i in range(self.psize):
                x = pixels[offset+i]
                if index < self.psize:
                    a = c = 0
                    b = pixels[b_offset+i]
                else:
                    a = pixels[a_offset+i]
                    b = pixels[b_offset+i]
                    c = pixels[c_offset+i]
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
                pixels[offset+i] = (x + pr) & 0xff
            offset += self.psize * xstep
            a_offset += self.psize * xstep
            b_offset += self.psize * xstep
            c_offset += self.psize * xstep

    # N.B. PNG files with 'up', 'average' or 'paeth' filters on the
    # first line of a pass are legal. The code above for 'average'
    # deals with this case explicitly. For up we map to the null
    # filter and for paeth we map to the sub filter.

    def reconstruct_line(self, filter_type, first_line, offset, xstep, ystep):
        """
        Reverse the filtering for a scanline.
        """
        # print >> sys.stderr, "Filter type %s, first_line=%s" % (
        #                      filter_type, first_line)
        filter_type += (first_line << 8)
        if filter_type == 1 or filter_type == 0x101 or filter_type == 0x104:
            self._reconstruct_sub(offset, xstep, ystep)
        elif filter_type == 2:
            self._reconstruct_up(offset, xstep, ystep)
        elif filter_type == 3 or filter_type == 0x103:
            self._reconstruct_average(offset, xstep, ystep)
        elif filter_type == 4:
            self._reconstruct_paeth(offset, xstep, ystep)
        return

    def deinterlace(self, scanlines):
        """
        Read pixel data and remove interlacing.
        """
        # print >> sys.stderr, ("Reading interlaced, w=%s, r=%s, planes=%s," +
        #     " bpp=%s") % (self.width, self.height, self.planes, self.bps)
        a = array('B')
        self.pixels = a
        # Make the array big enough
        temp = scanlines[0:self.width*self.height*self.psize]
        a.extend(temp)
        source_offset = 0
        for xstart, ystart, xstep, ystep in _adam7:
            # print >> sys.stderr, "Adam7: start=%s,%s step=%s,%s" % (
            #     xstart, ystart, xstep, ystep)
            filter_first_line = 1
            for y in range(ystart, self.height, ystep):
                if xstart >= self.width:
                    continue
                filter_type = scanlines[source_offset]
                source_offset += 1
                if xstep == 1:
                    offset = y * self.row_bytes
                    a[offset:offset+self.row_bytes] = \
                        scanlines[source_offset:source_offset + self.row_bytes]
                    source_offset += self.row_bytes
                else:
                    # Note we want the ceiling of (width - xstart) / xtep
                    row_len = self.psize * (
                        (self.width - xstart + xstep - 1) / xstep)
                    offset = y * self.row_bytes + xstart * self.psize
                    end_offset = (y+1) * self.row_bytes
                    skip = self.psize * xstep
                    for i in range(self.psize):
                        a[offset+i:end_offset:skip] = \
                            scanlines[source_offset + i:
                                      source_offset + row_len:
                                      self.psize]
                    source_offset += row_len
                if filter_type:
                    self.reconstruct_line(filter_type, filter_first_line,
                                          offset, xstep, ystep)
                filter_first_line = 0
        return a

    def read_flat(self, scanlines):
        """
        Read pixel data without de-interlacing.
        """
        a = array('B')
        self.pixels = a
        offset = 0
        source_offset = 0
        filter_first_line = 1
        for y in range(self.height):
            filter_type = scanlines[source_offset]
            source_offset += 1
            a.extend(scanlines[source_offset: source_offset + self.row_bytes])
            if filter_type:
                self.reconstruct_line(filter_type, filter_first_line,
                                      offset, 1, 1)
            filter_first_line = 0
            offset += self.row_bytes
            source_offset += self.row_bytes
        return a

    def read(self):
        """
        Read a simple PNG file, return width, height, pixels and image metadata

        This function is a very early prototype with limited flexibility
        and excessive use of memory.
        """
        signature = self.file.read(8)
        if (signature != struct.pack("8B", 137, 80, 78, 71, 13, 10, 26, 10)):
            raise Error("PNG file has invalid header")
        compressed = []
        image_metadata = {}
        while True:
            try:
                tag, data = self.read_chunk()
            except ValueError, e:
                raise Error('Chunk error: ' + e.args[0])

            # print >> sys.stderr, tag, len(data)
            if tag == 'IHDR': # http://www.w3.org/TR/PNG/#11IHDR
                (width, height, bits_per_sample, color_type,
                 compression_method, filter_method,
                 interlaced) = struct.unpack("!2I5B", data)
                bps = bits_per_sample / 8
                if bps == 0:
                    raise Error("unsupported pixel depth")
                if bps > 2 or bits_per_sample != (bps * 8):
                    raise Error("invalid pixel depth")
                if color_type == 0:
                    greyscale = True
                    has_alpha = False
                    planes = 1
                elif color_type == 2:
                    greyscale = False
                    has_alpha = False
                    planes = 3
                elif color_type == 4:
                    greyscale = True
                    has_alpha = True
                    planes = 2
                elif color_type == 6:
                    greyscale = False
                    has_alpha = True
                    planes = 4
                else:
                    raise Error("unknown PNG colour type %s" % color_type)
                if compression_method != 0:
                    raise Error("unknown compression method")
                if filter_method != 0:
                    raise Error("unknown filter method")
                self.bps = bps
                self.planes = planes
                self.psize = bps * planes
                self.width = width
                self.height = height
                self.row_bytes = width * self.psize
            elif tag == 'IDAT': # http://www.w3.org/TR/PNG/#11IDAT
                compressed.append(data)
            elif tag == 'bKGD':
                if greyscale:
                    image_metadata["background"] = struct.unpack("!1H", data)
                else:
                    image_metadata["background"] = struct.unpack("!3H", data)
            elif tag == 'tRNS':
                if greyscale:
                    image_metadata["transparent"] = struct.unpack("!1H", data)
                else:
                    image_metadata["transparent"] = struct.unpack("!3H", data)
            elif tag == 'gAMA':
                image_metadata["gamma"] = (
                    struct.unpack("!L", data)[0]) / 100000.0
            elif tag == 'IEND': # http://www.w3.org/TR/PNG/#11IEND
                break
        scanlines = array('B', zlib.decompress(''.join(compressed)))
        if interlaced:
            pixels = self.deinterlace(scanlines)
        else:
            pixels = self.read_flat(scanlines)
        image_metadata["greyscale"] = greyscale
        image_metadata["has_alpha"] = has_alpha
        image_metadata["bytes_per_sample"] = bps
        image_metadata["interlaced"] = interlaced
        return width, height, pixels, image_metadata

