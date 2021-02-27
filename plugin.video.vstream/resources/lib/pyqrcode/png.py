#!/usr/bin/env python
# encoding=utf-8
# flake8: noqa
#
# png.py - PNG encoder/decoder in pure Python
#
# Copyright (C) 2015 Pavel Zlatovratskii <scondo@mail.ru>
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
# Portions Copyright (C) 2009 David Jones <drj@pobox.com>
# And probably portions Copyright (C) 2006 Nicko van Someren <nicko@nicko.org>
#
# Original concept by Johann C. Rocholl.
#
# LICENCE (MIT)
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

"""
Pure Python PNG Reader/Writer

This Python module implements support for PNG images (see PNG
specification at http://www.w3.org/TR/2003/REC-PNG-20031110/ ). It reads
and writes PNG files with all allowable bit depths
(1/2/4/8/16/24/32/48/64 bits per pixel) and colour combinations:
greyscale (1/2/4/8/16 bit); RGB, RGBA, LA (greyscale with alpha) with
8/16 bits per channel; colour mapped images (1/2/4/8 bit).
Adam7 interlacing is supported for reading and
writing.  A number of optional chunks can be specified (when writing)
and understood (when reading): ``tRNS``, ``bKGD``, ``gAMA``.

For help, type ``import png; help(png)`` in your python interpreter.

A good place to start is the :class:`Reader` and :class:`Writer`
classes.

Requires Python 2.3.  Best with Python 2.6 and higher.  Installation is
trivial, but see the ``README.txt`` file (with the source distribution)
for details.

This file can also be used as a command-line utility to convert
`Netpbm <http://netpbm.sourceforge.net/>`_ PNM files to PNG, and the
reverse conversion from PNG to PNM. The interface is similar to that
of the ``pnmtopng`` program from Netpbm.  Type ``python png.py --help``
at the shell prompt for usage and a list of options.

A note on spelling and terminology
----------------------------------

Generally British English spelling is used in the documentation.  So
that's "greyscale" and "colour".  This not only matches the author's
native language, it's also used by the PNG specification.

The major colour models supported by PNG (and hence by this module) are:
greyscale, RGB, greyscale--alpha, RGB--alpha.  These are sometimes
referred to using the abbreviations: L, RGB, LA, RGBA.  In this case
each letter abbreviates a single channel: *L* is for Luminance or Luma
or Lightness which is the channel used in greyscale images; *R*, *G*,
*B* stand for Red, Green, Blue, the components of a colour image; *A*
stands for Alpha, the opacity channel (used for transparency effects,
but higher values are more opaque, so it makes sense to call it
opacity).

A note on formats
-----------------

When getting pixel data out of this module (reading) and presenting
data to this module (writing) there are a number of ways the data could
be represented as a Python value.  Generally this module uses one of
three formats called "flat row flat pixel", "boxed row flat pixel", and
"boxed row boxed pixel".  Basically the concern is whether each pixel
and each row comes in its own little tuple (box), or not.

Consider an image that is 3 pixels wide by 2 pixels high, and each pixel
has RGB components:

Boxed row flat pixel::

  iter([R,G,B, R,G,B, R,G,B],
       [R,G,B, R,G,B, R,G,B])

Each row appears as its own sequence, but the pixels are flattened so
that three values for one pixel simply follow the three values for
the previous pixel.  This is the most common format used, because it
provides a good compromise between space and convenience.
Row sequence supposed to be compatible with 'buffer' protocol in
addition to standard sequence methods so 'buffer()' can be used to
get fast per-byte access.
All rows are contained in iterable or iterable-compatible container.
(use 'iter()' to ensure)

Flat row flat pixel::

  [R,G,B, R,G,B, R,G,B,
   R,G,B, R,G,B, R,G,B]

The entire image is one single giant sequence of colour values.
Generally an array will be used (to save space), not a list.

Boxed row boxed pixel::

  list([ (R,G,B), (R,G,B), (R,G,B) ],
       [ (R,G,B), (R,G,B), (R,G,B) ])

Each row appears in its own list, but each pixel also appears in its own
tuple.  A serious memory burn in Python.

In all cases the top row comes first, and for each row the pixels are
ordered from left-to-right.  Within a pixel the values appear in the
order, R-G-B-A (or L-A for greyscale--alpha).

There is a fourth format, mentioned because it is used internally,
is close to what lies inside a PNG file itself, and has some support
from the public API.  This format is called packed.  When packed,
each row is a sequence of bytes (integers from 0 to 255), just as
it is before PNG scanline filtering is applied.  When the bit depth
is 8 this is essentially the same as boxed row flat pixel; when the
bit depth is less than 8, several pixels are packed into each byte;
when the bit depth is 16 (the only value more than 8 that is supported
by the PNG image format) each pixel value is decomposed into 2 bytes
(and `packed` is a misnomer).  This format is used by the
:meth:`Writer.write_packed` method.  It isn't usually a convenient
format, but may be just right if the source data for the PNG image
comes from something that uses a similar format (for example, 1-bit
BMPs, or another PNG file).

And now, my famous members
--------------------------
"""

from array import array
import itertools
import logging
import math
# http://www.python.org/doc/2.4.4/lib/module-operator.html
import operator
import datetime
import time
import struct
import sys
import zlib
# http://www.python.org/doc/2.4.4/lib/module-warnings.html
import warnings

try:
    from functools import reduce
except ImportError:
    # suppose to get there on python<2.7 where reduce is only built-in function
    pass

try:
    from itertools import imap as map
except ImportError:
    # On Python 3 there is no imap, but map works like imap instead
    pass

__version__ = "0.1.3"
__all__ = ['png_signature', 'Image', 'Reader', 'Writer',
           'Error', 'FormatError', 'ChunkError',
           'Filter', 'register_extra_filter',
           'write_chunks', 'from_array', 'parse_mode',
           'read_pam_header', 'read_pnm_header', 'write_pnm',
           'PERCEPTUAL', 'RELATIVE_COLORIMETRIC', 'SATURATION',
           'ABSOLUTE_COLORIMETRIC']


# The PNG signature.
# http://www.w3.org/TR/PNG/#5PNG-file-signature
png_signature = struct.pack('8B', 137, 80, 78, 71, 13, 10, 26, 10)

_adam7 = ((0, 0, 8, 8),
          (4, 0, 8, 8),
          (0, 4, 4, 8),
          (2, 0, 4, 4),
          (0, 2, 2, 4),
          (1, 0, 2, 2),
          (0, 1, 1, 2))
# registered keywords
# http://www.w3.org/TR/2003/REC-PNG-20031110/#11keywords
_registered_kw = ('Title', 'Author', 'Description', 'Copyright', 'Software',
                  'Disclaimer', 'Warning', 'Source', 'Comment',
                  'Creation Time')


# rendering intent
PERCEPTUAL = 0
RELATIVE_COLORIMETRIC = 1
SATURATION = 2
ABSOLUTE_COLORIMETRIC = 3


def group(s, n):
    """Repack iterator items into groups"""
    # See http://www.python.org/doc/2.6/library/functions.html#zip
    return list(zip(*[iter(s)] * n))


def _rel_import(module, tgt):
    """Using relative import in both Python 2 and Python 3"""
    try:
        exec("from ." + module + " import " + tgt, globals(), locals())
    except SyntaxError:
        # On Python < 2.5 relative import cause syntax error
        exec("from " + module + " import " + tgt, globals(), locals())
    except (ValueError, SystemError):
        # relative import in non-package, try absolute
        exec("from " + module + " import " + tgt, globals(), locals())
    return eval(tgt)


try:
    next
except NameError:
    def next(it):
        """trivial `next` emulation"""
        return it.next()
try:
    bytes
except NameError:
    bytes = str


# Define a bytearray_to_bytes() function.
# The definition of this function changes according to what
# version of Python we are on.
def bytearray_to_bytes(src):
    """Default version"""
    return bytes(src)


def newHarray(length=0):
    """fast init by length"""
    return array('H', [0]) * length


# bytearray is faster than array('B'), so we prefer to use it
# where available.
try:
    # bytearray exists (>= Python 2.6).
    newBarray = bytearray
    copyBarray = bytearray
except NameError:
    # bytearray does not exist. We're probably < Python 2.6 (the
    # version in which bytearray appears).
    def bytearray(src=tuple()):
        """Bytearray-like array"""
        return array('B', src)

    def newBarray(length=0):
        """fast init by length"""
        return array('B', [0]) * length

    if hasattr(array, '__copy__'):
        # a bit faster if possible
        copyBarray = array.__copy__
    else:
        copyBarray = bytearray

    def bytearray_to_bytes(row):
        """
        Convert bytearray to bytes.

        Recal that `row` will actually be an ``array``.
        """
        return row.tostring()


# Python 3 workaround
try:
    basestring
except NameError:
    basestring = str

# Conditionally convert to bytes.  Works on Python 2 and Python 3.
try:
    bytes('', 'ascii')

    def strtobytes(x):
        return bytes(x, 'iso8859-1')

    def bytestostr(x):
        return str(x, 'iso8859-1')
except (NameError, TypeError):
    # We get NameError when bytes() does not exist (most Python
    # 2.x versions), and TypeError when bytes() exists but is on
    # Python 2.x (when it is an alias for str() and takes at most
    # one argument).
    strtobytes = str
    bytestostr = str

zerobyte = strtobytes(chr(0))

try:
    set
except NameError:
    from sets import Set as set


def interleave_planes(ipixels, apixels, ipsize, apsize):
    """
    Interleave (colour) planes, e.g. RGB + A = RGBA.

    Return an array of pixels consisting of the `ipsize` elements of
    data from each pixel in `ipixels` followed by the `apsize` elements
    of data from each pixel in `apixels`.  Conventionally `ipixels`
    and `apixels` are byte arrays so the sizes are bytes, but it
    actually works with any arrays of the same type.  The returned
    array is the same type as the input arrays which should be the
    same type as each other.
    """
    itotal = len(ipixels)
    atotal = len(apixels)
    newtotal = itotal + atotal
    newpsize = ipsize + apsize
    # Set up the output buffer
    # See http://www.python.org/doc/2.4.4/lib/module-array.html#l2h-1356
    out = array(ipixels.typecode)
    # It's annoying that there is no cheap way to set the array size :-(
    out.extend(ipixels)
    out.extend(apixels)
    # Interleave in the pixel data
    for i in range(ipsize):
        out[i:newtotal:newpsize] = ipixels[i:itotal:ipsize]
    for i in range(apsize):
        out[i + ipsize:newtotal:newpsize] = apixels[i:atotal:apsize]
    return out


def peekiter(iterable):
    """Return first row and also iterable with same items as original"""
    it = iter(iterable)
    one = next(it)

    def gen():
        """Generator that returns first and proxy other items from source"""
        yield one
        while True:
            yield next(it)
    return (one, gen())


def check_palette(palette):
    """
    Check a palette argument (to the :class:`Writer` class) for validity.

    Returns the palette as a list if okay; raises an exception otherwise.
    """
    # None is the default and is allowed.
    if palette is None:
        return None

    p = list(palette)
    if not (0 < len(p) <= 256):
        raise ValueError("a palette must have between 1 and 256 entries")
    seen_triple = False
    for i, t in enumerate(p):
        if len(t) not in (3, 4):
            raise ValueError(
                "palette entry %d: entries must be 3- or 4-tuples." % i)
        if len(t) == 3:
            seen_triple = True
        if seen_triple and len(t) == 4:
            raise ValueError(
                "palette entry %d: all 4-tuples must precede all 3-tuples" % i)
        for x in t:
            if int(x) != x or not(0 <= x <= 255):
                raise ValueError(
                    "palette entry %d: values must be integer: 0 <= x <= 255" % i)
    return p


def check_sizes(size, width, height):
    """
    Check that these arguments, in supplied, are consistent.

    Return a (width, height) pair.
    """
    if not size:
        return width, height

    if len(size) != 2:
        raise ValueError(
            "size argument should be a pair (width, height)")
    if width is not None and width != size[0]:
        raise ValueError(
            "size[0] (%r) and width (%r) should match when both are used."
            % (size[0], width))
    if height is not None and height != size[1]:
        raise ValueError(
            "size[1] (%r) and height (%r) should match when both are used."
            % (size[1], height))
    return size


def check_color(c, greyscale, which):
    """
    Checks that a colour argument is the right form.

    Returns the colour
    (which, if it's a bar integer, is "corrected" to a 1-tuple).
    For transparent or background options.
    """
    if c is None:
        return c
    if greyscale:
        try:
            len(c)
        except TypeError:
            c = (c,)
        if len(c) != 1:
            raise ValueError("%s for greyscale must be 1-tuple" %
                             which)
        if not isinteger(c[0]):
            raise ValueError(
                "%s colour for greyscale must be integer" % which)
    else:
        if not (len(c) == 3 and
                isinteger(c[0]) and
                isinteger(c[1]) and
                isinteger(c[2])):
            raise ValueError(
                "%s colour must be a triple of integers" % which)
    return c


def check_time(value):
    """Convert time from most popular representations to datetime"""
    if value is None:
        return None
    if isinstance(value, (time.struct_time, tuple)):
        return value
    if isinstance(value, datetime.datetime):
        return value.timetuple()
    if isinstance(value, datetime.date):
        res = datetime.datetime.utcnow()
        res.replace(year=value.year, month=value.month, day=value.day)
        return res.timetuple()
    if isinstance(value, datetime.time):
        return datetime.datetime.combine(datetime.date.today(),
                                         value).timetuple()
    if isinteger(value):
        # Handle integer as timestamp
        return time.gmtime(value)
    if isinstance(value, basestring):
        if value.lower() == 'now':
            return time.gmtime()
        # TODO: parsinng some popular strings
    raise ValueError("Unsupported time representation:" + repr(value))


def popdict(src, keys):
    """
    Extract all keys (with values) from `src` dictionary as new dictionary

    values are removed from source dictionary.
    """
    new = {}
    for key in keys:
        if key in src:
            new[key] = src.pop(key)
    return new


class Error(Exception):

    """Generic PurePNG error"""

    def __str__(self):
        return self.__class__.__name__ + ': ' + ' '.join(self.args)


class FormatError(Error):

    """
    Problem with input file format.

    In other words, PNG file does
    not conform to the specification in some way and is invalid.
    """


class ChunkError(FormatError):

    """Error in chunk handling"""


class BaseFilter(object):

    """
    Basic methods of filtering and other byte manipulations

    This part can be compile with Cython (see README.cython)
    Private methods are declared as 'cdef' (unavailable from python)
    for this compilation, so don't just rename it.
    """

    def __init__(self, bitdepth=8):
        if bitdepth > 8:
            self.fu = bitdepth // 8
        else:
            self.fu = 1

    def __undo_filter_sub(self, scanline):
        """Undo sub filter."""
        ai = 0
        # Loops starts at index fu.
        for i in range(self.fu, len(scanline)):
            x = scanline[i]
            a = scanline[ai]  # result
            scanline[i] = (x + a) & 0xff  # result
            ai += 1

    def __do_filter_sub(self, scanline, result):
        """Sub filter."""
        ai = 0
        for i in range(self.fu, len(result)):
            x = scanline[i]
            a = scanline[ai]
            result[i] = (x - a) & 0xff
            ai += 1

    def __undo_filter_up(self, scanline):
        """Undo up filter."""
        previous = self.prev
        for i in range(len(scanline)):
            x = scanline[i]
            b = previous[i]
            scanline[i] = (x + b) & 0xff  # result

    def __do_filter_up(self, scanline, result):
        """Up filter."""
        previous = self.prev
        for i in range(len(result)):
            x = scanline[i]
            b = previous[i]
            result[i] = (x - b) & 0xff

    def __undo_filter_average(self, scanline):
        """Undo average filter."""
        ai = -self.fu
        previous = self.prev
        for i in range(len(scanline)):
            x = scanline[i]
            if ai < 0:
                a = 0
            else:
                a = scanline[ai]  # result
            b = previous[i]
            scanline[i] = (x + ((a + b) >> 1)) & 0xff  # result
            ai += 1

    def __do_filter_average(self, scanline, result):
        """Average filter."""
        ai = -self.fu
        previous = self.prev
        for i in range(len(result)):
            x = scanline[i]
            if ai < 0:
                a = 0
            else:
                a = scanline[ai]
            b = previous[i]
            result[i] = (x - ((a + b) >> 1)) & 0xff
            ai += 1

    def __undo_filter_paeth(self, scanline):
        """Undo Paeth filter."""
        ai = -self.fu
        previous = self.prev
        for i in range(len(scanline)):
            x = scanline[i]
            if ai < 0:
                pr = previous[i]  # a = c = 0
            else:
                a = scanline[ai]  # result
                c = previous[ai]
                b = previous[i]
                pa = abs(b - c)  # b
                pb = abs(a - c)  # 0
                pc = abs(a + b - c - c)  # b
                if pa <= pb and pa <= pc:  # False
                    pr = a
                elif pb <= pc:  # True
                    pr = b
                else:
                    pr = c
            scanline[i] = (x + pr) & 0xff  # result
            ai += 1

    def __do_filter_paeth(self, scanline, result):
        """Paeth filter."""
        # http://www.w3.org/TR/PNG/#9Filter-type-4-Paeth
        ai = -self.fu
        previous = self.prev
        for i in range(len(result)):
            x = scanline[i]
            if ai < 0:
                pr = previous[i]  # a = c = 0
            else:
                a = scanline[ai]
                c = previous[ai]
                b = previous[i]
                pa = abs(b - c)
                pb = abs(a - c)
                pc = abs(a + b - c - c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
            result[i] = (x - pr) & 0xff
            ai += 1

    def undo_filter(self, filter_type, line):
        """
        Undo the filter for a scanline.

        `scanline` is a sequence of bytes that does not include
        the initial filter type byte.

        The scanline will have the effects of filtering removed.
        Scanline modified inplace and also returned as result.
        """
        assert 0 <= filter_type <= 4
        # For the first line of a pass, synthesize a dummy previous line.
        if self.prev is None:
            self.prev = newBarray(len(line))
            # Also it's possible to switch some filters to easier
            if filter_type == 2:  # "up"
                filter_type = 0
            elif filter_type == 4:  # "paeth"
                filter_type = 1

        # Call appropriate filter algorithm.
        # 0 - do nothing
        if filter_type == 1:
            self.__undo_filter_sub(line)
        elif filter_type == 2:
            self.__undo_filter_up(line)
        elif filter_type == 3:
            self.__undo_filter_average(line)
        elif filter_type == 4:
            self.__undo_filter_paeth(line)

        # This will not work writing cython attributes from python
        # Only 'cython from cython' or 'python from python'
        self.prev[:] = line[:]
        return line

    def _filter_scanline(self, filter_type, line, result):
        """
        Apply a scanline filter to a scanline.

        `filter_type` specifies the filter type (0 to 4)
        'line` specifies the current (unfiltered) scanline as a sequence
        of bytes;
        """
        assert 0 <= filter_type < 5
        if self.prev is None:
            # We're on the first line.  Some of the filters can be reduced
            # to simpler cases which makes handling the line "off the top"
            # of the image simpler.  "up" becomes "none"; "paeth" becomes
            # "left" (non-trivial, but true). "average" needs to be handled
            # specially.
            if filter_type == 2:  # "up"
                filter_type = 0
            elif filter_type == 3:
                self.prev = newBarray(len(line))
            elif filter_type == 4:  # "paeth"
                filter_type = 1

        if filter_type == 1:
            self.__do_filter_sub(line, result)
        elif filter_type == 2:
            self.__do_filter_up(line, result)
        elif filter_type == 3:
            self.__do_filter_average(line, result)
        elif filter_type == 4:
            self.__do_filter_paeth(line, result)

    # Todo: color conversion functions should be moved
    # to a separate part in future
    def convert_la_to_rgba(self, row, result):
        """Convert a grayscale image with alpha to RGBA."""
        for i in range(len(row) // 3):
            for j in range(3):
                result[(4 * i) + j] = row[2 * i]
            result[(4 * i) + 3] = row[(2 * i) + 1]

    def convert_l_to_rgba(self, row, result):
        """
        Convert a grayscale image to RGBA.

        This method assumes the alpha channel in result is already
        correctly initialized.
        """
        for i in range(len(row) // 3):
            for j in range(3):
                result[(4 * i) + j] = row[i]

    def convert_rgb_to_rgba(self, row, result):
        """
        Convert an RGB image to RGBA.

        This method assumes the alpha channel in result is already
        correctly initialized.
        """
        for i in range(len(row) // 3):
            for j in range(3):
                result[(4 * i) + j] = row[(3 * i) + j]


iBaseFilter = BaseFilter  # 'i' means 'internal'
try:
    BaseFilter = _rel_import('pngfilters', 'BaseFilter')
except:
    # Whatever happens we could use internal part
    if not(sys.exc_info()[0] is ImportError):
        logging.error("Error during import of compiled filters!")
        logging.error(sys.exc_info()[1])
        logging.error("Fallback to pure python mode!")
    BaseFilter = iBaseFilter


class Writer(object):

    """PNG encoder in pure Python."""

    def __init__(self, width=None, height=None,
                 greyscale=False,
                 alpha=False,
                 bitdepth=8,
                 palette=None,
                 transparent=None,
                 background=None,
                 gamma=None,
                 compression=None,
                 interlace=False,
                 chunk_limit=2 ** 20,
                 filter_type=None,
                 icc_profile=None,
                 icc_profile_name="ICC Profile",
                 **kwargs
                 ):
        """
        Create a PNG encoder object.

        Arguments:

        width, height
          Image size in pixels, as two separate arguments.
        greyscale
          Input data is greyscale, not RGB.
        alpha
          Input data has alpha channel (RGBA or LA).
        bitdepth
          Bit depth: from 1 to 16.
        palette
          Create a palette for a colour mapped image (colour type 3).
        transparent
          Specify a transparent colour (create a ``tRNS`` chunk).
        background
          Specify a default background colour (create a ``bKGD`` chunk).
        gamma
          Specify a gamma value (create a ``gAMA`` chunk).
        compression
          zlib compression level: 0 (none) to 9 (more compressed);
          default: -1 or None.
        interlace
          Create an interlaced image.
        chunk_limit
          Write multiple ``IDAT`` chunks to save memory.
        filter_type
          Enable and specify PNG filter
        icc_profile
          Write ICC Profile
        icc_profile_name
          Name for ICC Profile

        Extra keywords:
            text
                see :meth:`set_text`
            modification_time
                see :meth:`set_modification_time`
            resolution
                see :meth:`set_resolution`

        The image size (in pixels) can be specified either by using the
        `width` and `height` arguments, or with the single `size`
        argument.  If `size` is used it should be a pair (*width*,
        *height*).

        `greyscale` and `alpha` are booleans that specify whether
        an image is greyscale (or colour), and whether it has an
        alpha channel (or not).

        `bitdepth` specifies the bit depth of the source pixel values.
        Each source pixel value must be an integer between 0 and
        ``2**bitdepth-1``.  For example, 8-bit images have values
        between 0 and 255.  PNG only stores images with bit depths of
        1,2,4,8, or 16.  When `bitdepth` is not one of these values,
        the next highest valid bit depth is selected, and an ``sBIT``
        (significant bits) chunk is generated that specifies the
        original precision of the source image.  In this case the
        supplied pixel values will be rescaled to fit the range of
        the selected bit depth.

        The details of which bit depth / colour model combinations the
        PNG file format supports directly, are somewhat arcane
        (refer to the PNG specification for full details).  Briefly:
        "small" bit depths (1,2,4) are only allowed with greyscale and
        colour mapped images; colour mapped images cannot have bit depth
        16.

        For colour mapped images (in other words, when the `palette`
        argument is specified) the `bitdepth` argument must match one of
        the valid PNG bit depths: 1, 2, 4, or 8.  (It is valid to have a
        PNG image with a palette and an ``sBIT`` chunk, but the meaning
        is slightly different; it would be awkward to press the
        `bitdepth` argument into service for this.)

        The `palette` option, when specified, causes a colour mapped image
        to be created: the PNG colour type is set to 3; `greyscale` must not
        be set; `alpha` must not be set; `transparent` must not be set;
        the bit depth must be 1, 2, 4, or 8.
        When a colour mapped image is created, the pixel values
        are palette indexes and the `bitdepth` argument specifies the size
        of these indexes (not the size of the colour values in the palette).

        The palette argument value should be a sequence of 3- or
        4-tuples.  3-tuples specify RGB palette entries; 4-tuples
        specify RGBA palette entries.  If both 4-tuples and 3-tuples
        appear in the sequence then all the 4-tuples must come
        before all the 3-tuples.  A ``PLTE`` chunk is created; if there
        are 4-tuples then a ``tRNS`` chunk is created as well.  The
        ``PLTE`` chunk will contain all the RGB triples in the same
        sequence; the ``tRNS`` chunk will contain the alpha channel for
        all the 4-tuples, in the same sequence.  Palette entries
        are always 8-bit.

        If specified, the `transparent` and `background` parameters must
        be a tuple with three integer values for red, green, blue, or
        a simple integer (or singleton tuple) for a greyscale image.

        If specified, the `gamma` parameter must be a positive number
        (generally, a `float`).  A ``gAMA`` chunk will be created.
        Note that this will not change the values of the pixels as
        they appear in the PNG file, they are assumed to have already
        been converted appropriately for the gamma specified.

        The `compression` argument specifies the compression level to
        be used by the ``zlib`` module.  Values from 1 to 9 specify
        compression, with 9 being "more compressed" (usually smaller
        and slower, but it doesn't always work out that way).  0 means
        no compression.  -1 and ``None`` both mean that the default
        level of compession will be picked by the ``zlib`` module
        (which is generally acceptable).

        If `interlace` is true then an interlaced image is created
        (using PNG's so far only interace method, *Adam7*).  This does
        not affect how the pixels should be presented to the encoder,
        rather it changes how they are arranged into the PNG file.
        On slow connexions interlaced images can be partially decoded
        by the browser to give a rough view of the image that is
        successively refined as more image data appears.

        .. note ::

          Enabling the `interlace` option requires the entire image
          to be processed in working memory.

        `chunk_limit` is used to limit the amount of memory used whilst
        compressing the image.  In order to avoid using large amounts of
        memory, multiple ``IDAT`` chunks may be created.

        `filter_type` is number or name of filter type for better compression
        see http://www.w3.org/TR/PNG/#9Filter-types for details
        It's also possible to use adaptive strategy for choosing filter type
        per row. Predefined strategies are `sum` and `entropy`.
        Custom strategies can be added with :meth:`register_extra_filter` or
        be callable passed with this argument.
        (see more at :meth:`register_extra_filter`)
        """
        width, height = check_sizes(kwargs.pop('size', None),
                                    width, height)

        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than zero")
        if not isinteger(width) or not isinteger(height):
            raise ValueError("width and height must be integers")
        # http://www.w3.org/TR/PNG/#7Integers-and-byte-order
        if width > 2**32 - 1 or height > 2**32 - 1:
            raise ValueError("width and height cannot exceed 2**32-1")

        if alpha and transparent is not None:
            raise ValueError(
                "transparent colour not allowed with alpha channel")

        if 'bytes_per_sample' in kwargs and not bitdepth:
            warnings.warn('please use bitdepth instead of bytes_per_sample',
                          DeprecationWarning)
            if kwargs['bytes_per_sample'] not in (0.125, 0.25, 0.5, 1, 2):
                raise ValueError(
                    "bytes per sample must be .125, .25, .5, 1, or 2")
            bitdepth = int(8 * kwargs.pop('bytes_per_sample'))

        if 'resolution' not in kwargs and 'physical' in kwargs:
            kwargs['resolution'] = kwargs.pop('physical')
            warnings.warn('please use resolution instead of physilcal',
                          DeprecationWarning)

        if not isinteger(bitdepth) or bitdepth < 1 or 16 < bitdepth:
            raise ValueError("bitdepth (%r) must be a postive integer <= 16" %
                             bitdepth)

        if filter_type is None:
            filter_type = 0
        elif isinstance(filter_type, basestring):
            str_ftype = str(filter_type).lower()
            filter_names = {'none': 0,
                            'sub': 1,
                            'up': 2,
                            'average': 3,
                            'paeth': 4}
            if str_ftype in filter_names:
                filter_type = filter_names[str_ftype]
        self.filter_type = filter_type

        self.rescale = None
        self.palette = check_palette(palette)
        if self.palette:
            if bitdepth not in (1, 2, 4, 8):
                raise ValueError("with palette bitdepth must be 1, 2, 4, or 8")
            if transparent is not None:
                raise ValueError("transparent and palette not compatible")
            if alpha:
                raise ValueError("alpha and palette not compatible")
            if greyscale:
                raise ValueError("greyscale and palette not compatible")
        else:
            # No palette, check for sBIT chunk generation.
            if alpha or not greyscale:
                if bitdepth not in (8, 16):
                    targetbitdepth = (8, 16)[bitdepth > 8]
                    self.rescale = (bitdepth, targetbitdepth)
                    bitdepth = targetbitdepth
                    del targetbitdepth
            else:
                assert greyscale
                assert not alpha
                if bitdepth not in (1, 2, 4, 8, 16):
                    if bitdepth > 8:
                        targetbitdepth = 16
                    elif bitdepth == 3:
                        targetbitdepth = 4
                    else:
                        assert bitdepth in (5, 6, 7)
                        targetbitdepth = 8
                    self.rescale = (bitdepth, targetbitdepth)
                    bitdepth = targetbitdepth
                    del targetbitdepth

        if bitdepth < 8 and (alpha or not greyscale and not self.palette):
            raise ValueError(
                "bitdepth < 8 only permitted with greyscale or palette")
        if bitdepth > 8 and self.palette:
            raise ValueError(
                "bit depth must be 8 or less for images with palette")

        self.transparent = check_color(transparent, greyscale, 'transparent')
        self.background = check_color(background, greyscale, 'background')
        # At the moment the `planes` argument is ignored;
        # its purpose is to act as a dummy so that
        # ``Writer(x, y, **info)`` works, where `info` is a dictionary
        # returned by Reader.read and friends.
        # Ditto for `colormap` and `maxval`.
        popdict(kwargs, ('planes', 'colormap', 'maxval'))

        for ex_kw in ('text', 'resolution', 'modification_time',
                      'rendering_intent', 'white_point', 'rgb_points'):
            getattr(self, 'set_' + ex_kw)(kwargs.pop(ex_kw, None))
        # Keyword text support
        kw_text = popdict(kwargs, _registered_kw)
        if kw_text:
            kw_text.update(self.text)
            self.set_text(kw_text)

        if kwargs:
            warnings.warn("Unknown writer args: " + str(kwargs))

        # It's important that the true boolean values (greyscale, alpha,
        # colormap, interlace) are converted to bool because Iverson's
        # convention is relied upon later on.
        self.width = width
        self.height = height
        self.gamma = gamma
        self.icc_profile = icc_profile
        if icc_profile:
            if not icc_profile_name:
                raise Error("ICC profile shoud have a name")
            else:
                self.icc_profile_name = strtobytes(icc_profile_name)
        self.greyscale = bool(greyscale)
        self.alpha = bool(alpha)
        self.bitdepth = int(bitdepth)
        self.compression = compression
        self.chunk_limit = chunk_limit
        self.interlace = bool(interlace)

        colormap = bool(self.palette)
        self.color_type = 4 * self.alpha + 2 * (not greyscale) + 1 * colormap
        assert self.color_type in (0, 2, 3, 4, 6)

        self.color_planes = (3, 1)[self.greyscale or colormap]
        self.planes = self.color_planes + self.alpha

    def set_text(self, text=None, **kwargs):
        """Add textual information.

        All pairs in dictionary will be written, but keys should be latin-1;
        registered keywords could be used as arguments.

        When called more than once overwrite exist data.
        """
        if text is None:
            text = {}
        text.update(popdict(kwargs, _registered_kw))
        if 'Creation Time' in text and\
                not isinstance(text['Creation Time'], (basestring, bytes)):
            text['Creation Time'] = datetime.datetime(
                *(check_time(text['Creation Time'])[:6])).isoformat()
        self.text = text

    def set_modification_time(self, modification_time=True):
        """
        Add time to be written as last modification time

        When called after initialisation configure to use
        time of writing file
        """
        if (isinstance(modification_time, basestring) and
                modification_time.lower() == 'write') or\
                modification_time is True:
            self.modification_time = True
        else:
            self.modification_time = check_time(modification_time)

    def set_resolution(self, resolution=None):
        """
        Add physical pixel dimensions

        `resolution` supposed two be tuple of two parameterts: pixels per unit
        and unit type; unit type may be omitted
        pixels per unit could be simple integer or tuple of (ppu_x, ppu_y)
        Also possible to use all three parameters im row

        * resolution = ((1, 4), )  # wide pixels (4:1) without unit specifier
        * resolution = (300, 'inch')  # 300dpi in both dimensions
        * resolution = (4, 1, 0)  # tall pixels (1:4) without unit specifier
        """
        if resolution is None:
            self.resolution = None
            return
        # All in row
        if len(resolution) == 3:
            self.resolution = ((resolution[0], resolution[1]), resolution[2])
            return
        # Ensure length and convert all false to 0 (no unit)
        if len(resolution) == 1 or not resolution[1]:
            resolution = (resolution[0], 0)
        # Single dimension
        if isinstance(resolution[0], float) or isinteger(resolution[0]):
            resolution = ((resolution[0], resolution[0]), resolution[1])
        # Unit conversion
        if resolution[1] in (1, 'm', 'meter'):
            resolution = (resolution[0], 1)
        elif resolution[1] in ('i', 'in', 'inch'):
            resolution = ((int(resolution[0][0] / 0.0254 + 0.5),
                           int(resolution[0][1] / 0.0254 + 0.5)), 1)
        elif resolution[1] in ('cm', 'centimeter'):
            resolution = ((resolution[0][0] * 100,
                           resolution[0][1] * 100), 1)
        self.resolution = resolution

    def set_rendering_intent(self, rendering_intent):
        """Set rendering intent variant for sRGB chunk"""
        if rendering_intent not in (None,
                                    PERCEPTUAL,
                                    RELATIVE_COLORIMETRIC,
                                    SATURATION,
                                    ABSOLUTE_COLORIMETRIC):
            raise FormatError('Unknown redering intent')
        self.rendering_intent = rendering_intent

    def set_white_point(self, white_point, point2=None):
        """Set white point part of cHRM chunk"""
        if isinstance(white_point, float) and isinstance(point2, float):
            white_point = (white_point, point2)
        self.white_point = white_point

    def set_rgb_points(self, rgb_points, *args):
        """Set rgb points part of cHRM chunk"""
        if not args:
            self.rgb_points = rgb_points
        # separate tuples
        elif len(args) == 2:
            self.rgb_points = (rgb_points, args[0], args[1])
        # separate numbers
        elif len(args) == 5:
            self.rgb_points = ((rgb_points, args[0]),
                               (args[1], args[2]),
                               (args[3], args[4]))

    def __write_palette(self, outfile):
        """
        Write``PLTE`` and if necessary a ``tRNS`` chunk to.

        This method should be called only from ``write_idat`` method
        or chunk order will be ruined.
        """
        p = bytearray()
        t = bytearray()

        for x in self.palette:
            p.extend(x[0:3])
            if len(x) > 3:
                t.append(x[3])

        write_chunk(outfile, 'PLTE', bytearray_to_bytes(p))
        if t:
            # tRNS chunk is optional. Only needed if palette entries
            # have alpha.
            write_chunk(outfile, 'tRNS', bytearray_to_bytes(t))

    def __write_srgb(self, outfile):
        """
        Write colour reference information: gamma, iccp etc.

        This method should be called only from ``write_idat`` method
        or chunk order will be ruined.
        """
        if self.rendering_intent is not None and self.icc_profile is not None:
            raise FormatError("sRGB(via rendering_intent) and iCCP could not"
                              "be present simultaneously")
        # http://www.w3.org/TR/PNG/#11sRGB
        if self.rendering_intent is not None:
            write_chunk(outfile, 'sRGB',
                        struct.pack("B", int(self.rendering_intent)))
        # http://www.w3.org/TR/PNG/#11cHRM
        if (self.white_point is not None and self.rgb_points is None) or\
                (self.white_point is None and self.rgb_points is not None):
            logging.warn("White and RGB points should be both specified to"
                         " write cHRM chunk")
            self.white_point = None
            self.rgb_points = None
        if (self.white_point is not None and self.rgb_points is not None):
            data = (self.white_point[0], self.white_point[1],
                    self.rgb_points[0][0], self.rgb_points[0][1],
                    self.rgb_points[1][0], self.rgb_points[1][1],
                    self.rgb_points[2][0], self.rgb_points[2][1],
                    )
            write_chunk(outfile, 'cHRM',
                        struct.pack("!8L",
                                    *[int(round(it * 1e5)) for it in data]))
        # http://www.w3.org/TR/PNG/#11gAMA
        if self.gamma is not None:
            write_chunk(outfile, 'gAMA',
                        struct.pack("!L", int(round(self.gamma * 1e5))))
        # http://www.w3.org/TR/PNG/#11iCCP
        if self.icc_profile is not None:
            write_chunk(outfile, 'iCCP',
                        self.icc_profile_name + zerobyte +
                        zerobyte +
                        zlib.compress(self.icc_profile, self.compression))

    def __write_text(self, outfile):
        """
        Write text information into file

        This method should be called only from ``write_idat`` method
        or chunk order will be ruined.
        """
        for k, v in self.text.items():
            if not isinstance(v, bytes):
                try:
                    international = False
                    v = v.encode('latin-1')
                except UnicodeEncodeError:
                    international = True
                    v = v.encode('utf-8')
            else:
                international = False
            if not isinstance(k, bytes):
                k = strtobytes(k)
            if international:
                # No compress, language tag or translated keyword for now
                write_chunk(outfile, 'iTXt', k + zerobyte +
                            zerobyte + zerobyte +
                            zerobyte + zerobyte + v)
            else:
                write_chunk(outfile, 'tEXt', k + zerobyte + v)

    def write(self, outfile, rows):
        """
        Write a PNG image to the output file.

        `rows` should be an iterable that yields each row in boxed row
        flat pixel format. The rows should be the rows of the original
        image, so there should be ``self.height`` rows of ``self.width *
        self.planes`` values.  If `interlace` is specified (when
        creating the instance), then an interlaced PNG file will
        be written.  Supply the rows in the normal image order;
        the interlacing is carried out internally.

        .. note ::

          Interlacing will require the entire image to be in working
          memory.
        """
        if self.interlace:
            fmt = 'BH'[self.bitdepth > 8]
            a = array(fmt, itertools.chain(*rows))
            return self.write_array(outfile, a)
        else:
            nrows = self.write_passes(outfile, rows)
            if nrows != self.height:
                raise ValueError(
                    "rows supplied (%d) does not match height (%d)" %
                    (nrows, self.height))

    def write_passes(self, outfile, rows, packed=False):
        """
        Write a PNG image to the output file.

        Most users are expected to find the :meth:`write` or
        :meth:`write_array` method more convenient.

        The rows should be given to this method in the order that
        they appear in the output file.  For straightlaced images,
        this is the usual top to bottom ordering, but for interlaced
        images the rows should have already been interlaced before
        passing them to this function.

        `rows` should be an iterable that yields each row.  When
        `packed` is ``False`` the rows should be in boxed row flat pixel
        format; when `packed` is ``True`` each row should be a packed
        sequence of bytes.
        """
        self.write_idat(outfile, self.idat(rows, packed))
        return self.irows

    def write_idat(self, outfile, idat_sequence):
        """
        Write png with IDAT to file

        `idat_sequence` should be iterable that produce IDAT chunks
        compatible with `Writer` configuration.
        """
        # http://www.w3.org/TR/PNG/#5PNG-file-signature
        outfile.write(png_signature)

        # http://www.w3.org/TR/PNG/#11IHDR
        write_chunk(outfile, 'IHDR',
                    struct.pack("!2I5B", self.width, self.height,
                                self.bitdepth, self.color_type,
                                0, 0, self.interlace))
        # See :chunk:order
        self.__write_srgb(outfile)
        # See :chunk:order
        # http://www.w3.org/TR/PNG/#11sBIT
        if self.rescale:
            write_chunk(outfile, 'sBIT',
                        struct.pack('%dB' % self.planes,
                                    *[self.rescale[0]] * self.planes))
        # :chunk:order: Without a palette (PLTE chunk), ordering is
        # relatively relaxed.  With one, gamma info must precede PLTE
        # chunk which must precede tRNS and bKGD.
        # See http://www.w3.org/TR/PNG/#5ChunkOrdering
        if self.palette:
            self.__write_palette(outfile)

        # http://www.w3.org/TR/PNG/#11tRNS
        if self.transparent is not None:
            if self.greyscale:
                write_chunk(outfile, 'tRNS',
                            struct.pack("!1H", *self.transparent))
            else:
                write_chunk(outfile, 'tRNS',
                            struct.pack("!3H", *self.transparent))

        # http://www.w3.org/TR/PNG/#11bKGD
        if self.background is not None:
            if self.greyscale:
                write_chunk(outfile, 'bKGD',
                            struct.pack("!1H", *self.background))
            else:
                write_chunk(outfile, 'bKGD',
                            struct.pack("!3H", *self.background))
        # http://www.w3.org/TR/PNG/#11pHYs
        if self.resolution is not None:
            write_chunk(outfile, 'pHYs',
                        struct.pack("!IIB",
                                    self.resolution[0][0],
                                    self.resolution[0][1],
                                    self.resolution[1]))
        # http://www.w3.org/TR/PNG/#11tIME
        if self.modification_time is not None:
            if self.modification_time is True:
                self.modification_time = check_time('now')
            write_chunk(outfile, 'tIME',
                        struct.pack("!H5B", *(self.modification_time[:6])))
        # http://www.w3.org/TR/PNG/#11textinfo
        if self.text:
            self.__write_text(outfile)
        for idat in idat_sequence:
            write_chunk(outfile, 'IDAT', idat)
        # http://www.w3.org/TR/PNG/#11IEND
        write_chunk(outfile, 'IEND')

    def idat(self, rows, packed=False):
        """Generator that produce IDAT chunks from rows"""
        # http://www.w3.org/TR/PNG/#11IDAT
        if self.compression is not None:
            compressor = zlib.compressobj(self.compression)
        else:
            compressor = zlib.compressobj()

        filt = Filter(self.bitdepth * self.planes,
                      self.interlace, self.height)
        data = bytearray()

        def byteextend(rowbytes):
            """Default extending data with bytes. Applying filter"""
            data.extend(filt.do_filter(self.filter_type, rowbytes))

        # Choose an extend function based on the bitdepth.  The extend
        # function packs/decomposes the pixel values into bytes and
        # stuffs them onto the data array.
        if self.bitdepth == 8 or packed:
            extend = byteextend
        elif self.bitdepth == 16:
            def extend(sl):
                """Decompose into bytes before byteextend"""
                fmt = '!%dH' % len(sl)
                byteextend(bytearray(struct.pack(fmt, *sl)))
        else:
            # Pack into bytes
            assert self.bitdepth < 8
            # samples per byte
            spb = 8 // self.bitdepth

            def extend(sl):
                """Pack into bytes before byteextend"""
                a = bytearray(sl)
                # Adding padding bytes so we can group into a whole
                # number of spb-tuples.
                l = float(len(a))
                extra = math.ceil(l / float(spb)) * spb - l
                a.extend([0] * int(extra))
                # Pack into bytes
                l = group(a, spb)
                l = [reduce(lambda x, y: (x << self.bitdepth) + y, e)
                     for e in l]
                byteextend(l)
        if self.rescale:
            oldextend = extend
            factor = \
                float(2**self.rescale[1] - 1) / float(2**self.rescale[0] - 1)

            def extend(sl):
                """Rescale before extend"""
                oldextend([int(round(factor * x)) for x in sl])

        # Build the first row, testing mostly to see if we need to
        # changed the extend function to cope with NumPy integer types
        # (they cause our ordinary definition of extend to fail, so we
        # wrap it).  See
        # http://code.google.com/p/pypng/issues/detail?id=44
        enumrows = enumerate(rows)
        del rows

        # :todo: Certain exceptions in the call to ``.next()`` or the
        # following try would indicate no row data supplied.
        # Should catch.
        i, row = next(enumrows)
        try:
            # If this fails...
            extend(row)
        except:
            # ... try a version that converts the values to int first.
            # Not only does this work for the (slightly broken) NumPy
            # types, there are probably lots of other, unknown, "nearly"
            # int types it works for.
            def wrapmapint(f):
                return lambda sl: f([int(x) for x in sl])
            extend = wrapmapint(extend)
            del wrapmapint
            extend(row)

        for i, row in enumrows:
            extend(row)
            if len(data) > self.chunk_limit:
                compressed = compressor.compress(
                    bytearray_to_bytes(data))
                if len(compressed):
                    yield compressed
                # Because of our very witty definition of ``extend``,
                # above, we must re-use the same ``data`` object.  Hence
                # we use ``del`` to empty this one, rather than create a
                # fresh one (which would be my natural FP instinct).
                del data[:]
        if len(data):
            compressed = compressor.compress(bytearray_to_bytes(data))
        else:
            compressed = bytes()
        flushed = compressor.flush()
        if len(compressed) or len(flushed):
            yield compressed + flushed
        self.irows = i + 1

    def write_array(self, outfile, pixels):
        """
        Write an array in flat row flat pixel format as a PNG file on
        the output file.  See also :meth:`write` method.
        """

        if self.interlace:
            self.write_passes(outfile, self.array_scanlines_interlace(pixels))
        else:
            self.write_passes(outfile, self.array_scanlines(pixels))

    def write_packed(self, outfile, rows):
        """
        Write PNG file to `outfile`.

        The pixel data comes from `rows` which should be in boxed row
        packed format.  Each row should be a sequence of packed bytes.

        Technically, this method does work for interlaced images but it
        is best avoided.  For interlaced images, the rows should be
        presented in the order that they appear in the file.

        This method should not be used when the source image bit depth
        is not one naturally supported by PNG; the bit depth should be
        1, 2, 4, 8, or 16.
        """
        if self.rescale:
            raise Error("write_packed method not suitable for bit depth %d" %
                        self.rescale[0])
        return self.write_passes(outfile, rows, packed=True)

    def convert_pnm(self, infile, outfile):
        """
        Convert a PNM file containing raw pixel data into a PNG file
        with the parameters set in the writer object.  Works for
        (binary) PGM, PPM, and PAM formats.
        """
        if self.interlace:
            pixels = array('B')
            pixels.fromfile(infile,
                            (self.bitdepth / 8) * self.color_planes *
                            self.width * self.height)
            self.write_passes(outfile, self.array_scanlines_interlace(pixels))
        else:
            self.write_passes(outfile, self.file_scanlines(infile))

    def convert_ppm_and_pgm(self, ppmfile, pgmfile, outfile):
        """
        Convert a PPM and PGM file containing raw pixel data into a
        PNG outfile with the parameters set in the writer object.
        """
        pixels = array('B')
        pixels.fromfile(ppmfile,
                        (self.bitdepth / 8) * self.color_planes *
                        self.width * self.height)
        apixels = array('B')
        apixels.fromfile(pgmfile,
                         (self.bitdepth / 8) *
                         self.width * self.height)
        pixels = interleave_planes(pixels, apixels,
                                   (self.bitdepth / 8) * self.color_planes,
                                   (self.bitdepth / 8))
        if self.interlace:
            self.write_passes(outfile, self.array_scanlines_interlace(pixels))
        else:
            self.write_passes(outfile, self.array_scanlines(pixels))

    def file_scanlines(self, infile):
        """
        Generates boxed rows in flat pixel format, from the input file.

        It assumes that the input file is in a "Netpbm-like"
        binary format, and is positioned at the beginning of the first
        pixel.  The number of pixels to read is taken from the image
        dimensions (`width`, `height`, `planes`) and the number of bytes
        per value is implied by the image `bitdepth`.
        """

        # Values per row
        vpr = self.width * self.planes
        row_bytes = vpr
        if self.bitdepth > 8:
            assert self.bitdepth == 16
            row_bytes *= 2
            fmt = '>%dH' % vpr

            def line():
                return array('H', struct.unpack(fmt, infile.read(row_bytes)))
        else:
            def line():
                scanline = array('B', infile.read(row_bytes))
                return scanline
        for _ in range(self.height):
            yield line()

    def array_scanlines(self, pixels):
        """
        Generates boxed rows (flat pixels) from flat rows (flat pixels)
        in an array.
        """
        # Values per row
        vpr = self.width * self.planes
        stop = 0
        for _ in range(self.height):
            start = stop
            stop = start + vpr
            yield pixels[start:stop]

    def array_scanlines_interlace(self, pixels):
        """
        Generator for interlaced scanlines from an array.

        `pixels` is the full source image in flat row flat pixel format.
        The generator yields each scanline of the reduced passes in turn, in
        boxed row flat pixel format.
        """
        # http://www.w3.org/TR/PNG/#8InterlaceMethods
        # Array type.
        fmt = 'BH'[self.bitdepth > 8]
        # Value per row
        vpr = self.width * self.planes
        for xstart, ystart, xstep, ystep in _adam7:
            if xstart >= self.width:
                continue
            # Pixels per row (of reduced image)
            ppr = int(math.ceil((self.width - xstart) / float(xstep)))
            # number of values in reduced image row.
            row_len = ppr * self.planes
            for y in range(ystart, self.height, ystep):
                if xstep == 1:
                    offset = y * vpr
                    yield pixels[offset:offset + vpr]
                else:
                    row = array(fmt)
                    # There's no easier way to set the length of an array
                    row.extend(pixels[0:row_len])
                    offset = y * vpr + xstart * self.planes
                    end_offset = (y + 1) * vpr
                    skip = self.planes * xstep
                    for i in range(self.planes):
                        row[i::self.planes] = \
                            pixels[offset + i:end_offset:skip]
                    yield row


def write_chunk(outfile, tag, data=bytes()):
    """Write a PNG chunk to the output file, including length and checksum."""
    # http://www.w3.org/TR/PNG/#5Chunk-layout
    outfile.write(struct.pack("!I", len(data)))
    tag = strtobytes(tag)
    outfile.write(tag)
    outfile.write(data)
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 0xFFFFFFFF
    outfile.write(struct.pack("!I", checksum))


def write_chunks(out, chunks):
    """Create a PNG file by writing out the chunks."""
    out.write(png_signature)
    for chunk in chunks:
        write_chunk(out, *chunk)


class Filter(BaseFilter):
    def __init__(self, bitdepth=8, interlace=None, rows=None, prev=None):
        BaseFilter.__init__(self, bitdepth)
        if prev is None:
            self.prev = None
        else:
            self.prev = bytearray(prev)
        self.interlace = interlace
        self.restarts = []
        if self.interlace:
            for _, off, _, step in _adam7:
                self.restarts.append((rows - off - 1 + step) // step)

    def filter_all(self, line):
        """Doing all filters for specified line

        return filtered lines as list
        For using with adaptive filters
        """
        lines = [None] * 5
        for filter_type in range(5):  # range save more than 'optimised' order
            res = copyBarray(line)
            self._filter_scanline(filter_type, line, res)
            res.insert(0, filter_type)
            lines[filter_type] = res
        return lines

    adapt_methods = {}

    def adaptive_filter(self, strategy, line):
        """
        Applying non-standart filters (e.g. adaptive selection)

        `strategy` may be one of following types:

        - string - find and use strategy with this name
        - dict - find and use strategy by field 'name' of this dict
          and use it with this dict as configuration
        - callable - use this callable as strategy with empty dict as cfg
          check :meth:`register_extra_filter` for documentation)

        `line` specifies the current (unfiltered) scanline as a sequence
        of bytes;
        """
        if isinstance(strategy, (basestring, bytes)):
            strategy = {'name': str(strategy)}
        if isinstance(strategy, dict):
            cfg = strategy
            strategy = Filter.adapt_methods.get(cfg['name'])
        else:
            cfg = {}
        if strategy is None:
            raise Error("Adaptive strategy not found")
        else:
            return strategy(line, cfg, self)

    def do_filter(self, filter_type, line):
        """
        Applying filter, caring about prev line, interlacing etc.

        `filter_type` may be integer to apply basic filter or
        adaptive strategy with dict
        (`name` is reqired field, others may tune strategy)
        """
        # Recall that filtering algorithms are applied to bytes,
        # not to pixels, regardless of the bit depth or colour type
        # of the image.

        line = bytearray(line)
        if isinstance(filter_type, int):
            res = bytearray(line)
            self._filter_scanline(filter_type, line, res)
            res.insert(0, filter_type)  # Add filter type as the first byte
        else:
            res = self.adaptive_filter(filter_type, line)
        self.prev = line
        if self.restarts:
            self.restarts[0] -= 1
            if self.restarts[0] == 0:
                del self.restarts[0]
                self.prev = None
        return res


def register_extra_filter(selector, name):
    """
    Register adaptive filter selection strategy for futher usage.

    `selector` - callable like ``def(line, cfg, filter_obj)``

    - line - line for filtering
    - cfg - dict with optional tuning
    - filter_obj - instance of this class to get context or apply base filters

    callable should return chosen line

    `name` - name which may be used later to recall this strategy
    """
    Filter.adapt_methods[str(name)] = selector


# Two basic adaptive strategies
def adapt_sum(line, cfg, filter_obj):
    """Determine best filter by sum of all row values"""
    lines = filter_obj.filter_all(line)
    res_s = [sum(it) for it in lines]
    r = res_s.index(min(res_s))
    return lines[r]


register_extra_filter(adapt_sum, 'sum')


def adapt_entropy(line, cfg, filter_obj):
    """Determine best filter by dispersion of row values"""
    lines = filter_obj.filter_all(line)
    res_c = [len(set(it)) for it in lines]
    r = res_c.index(min(res_c))
    return lines[r]


register_extra_filter(adapt_entropy, 'entropy')


def parse_mode(mode, default_bitdepth=None):
    """Parse PIL-style mode and return tuple (grayscale, alpha, bitdeph)"""
    # few special cases
    if mode == 'P':
        # Don't know what is pallette
        raise Error('Unknown colour mode:' + mode)
    elif mode == '1':
        # Logical
        return (True, False, 1)
    elif mode == 'I':
        # Integer
        return (True, False, 16)
    # here we go
    if mode.startswith('L'):
        grayscale = True
        mode = mode[1:]
    elif mode.startswith('RGB'):
        grayscale = False
        mode = mode[3:]
    else:
        raise Error('Unknown colour mode:' + mode)

    if mode.startswith('A'):
        alpha = True
        mode = mode[1:]
    else:
        alpha = False

    bitdepth = default_bitdepth
    if mode.startswith(';'):
        mode = mode[1:]
    if mode:
        try:
            bitdepth = int(mode)
        except (TypeError, ValueError):
            raise Error('Unsupported bitdepth mode:' + mode)
    return (grayscale, alpha, bitdepth)


def from_array(a, mode=None, info=None):
    """
    Create a PNG :class:`Image` object from a 2- or 3-dimensional array.

    One application of this function is easy PIL-style saving:
    ``png.from_array(pixels, 'L').save('foo.png')``.

    .. note :

      The use of the term *3-dimensional* is for marketing purposes
      only.  It doesn't actually work.  Please bear with us.  Meanwhile
      enjoy the complimentary snacks (on request) and please use a
      2-dimensional array.

    Unless they are specified using the *info* parameter, the PNG's
    height and width are taken from the array size.  For a 3 dimensional
    array the first axis is the height; the second axis is the width;
    and the third axis is the channel number.  Thus an RGB image that is
    16 pixels high and 8 wide will use an array that is 16x8x3.  For 2
    dimensional arrays the first axis is the height, but the second axis
    is ``width*channels``, so an RGB image that is 16 pixels high and 8
    wide will use a 2-dimensional array that is 16x24 (each row will be
    8*3 = 24 sample values).

    *mode* is a string that specifies the image colour format in a
    PIL-style mode.  It can be:

    ``'L'``
      greyscale (1 channel)
    ``'LA'``
      greyscale with alpha (2 channel)
    ``'RGB'``
      colour image (3 channel)
    ``'RGBA'``
      colour image with alpha (4 channel)

    The mode string can also specify the bit depth (overriding how this
    function normally derives the bit depth, see below).  Appending
    ``';16'`` to the mode will cause the PNG to be 16 bits per channel;
    any decimal from 1 to 16 can be used to specify the bit depth.

    When a 2-dimensional array is used *mode* determines how many
    channels the image has, and so allows the width to be derived from
    the second array dimension.

    The array is expected to be a ``numpy`` array, but it can be any
    suitable Python sequence.  For example, a list of lists can be used:
    ``png.from_array([[0, 255, 0], [255, 0, 255]], 'L')``.  The exact
    rules are: ``len(a)`` gives the first dimension, height;
    ``len(a[0])`` gives the second dimension; ``len(a[0][0])`` gives the
    third dimension, unless an exception is raised in which case a
    2-dimensional array is assumed.  It's slightly more complicated than
    that because an iterator of rows can be used, and it all still
    works.  Using an iterator allows data to be streamed efficiently.

    The bit depth of the PNG is normally taken from the array element's
    datatype (but if *mode* specifies a bitdepth then that is used
    instead).  The array element's datatype is determined in a way which
    is supposed to work both for ``numpy`` arrays and for Python
    ``array.array`` objects.  A 1 byte datatype will give a bit depth of
    8, a 2 byte datatype will give a bit depth of 16.  If the datatype
    does not have an implicit size, for example it is a plain Python
    list of lists, as above, then a default of 8 is used.

    The *info* parameter is a dictionary that can be used to specify
    metadata (in the same style as the arguments to the
    :class:`png.Writer` class).  For this function the keys that are
    useful are:

    height
      overrides the height derived from the array dimensions and allows
      *a* to be an iterable.
    width
      overrides the width derived from the array dimensions.
    bitdepth
      overrides the bit depth derived from the element datatype (but
      must match *mode* if that also specifies a bit depth).

    Generally anything specified in the
    *info* dictionary will override any implicit choices that this
    function would otherwise make, but must match any explicit ones.
    For example, if the *info* dictionary has a ``greyscale`` key then
    this must be true when mode is ``'L'`` or ``'LA'`` and false when
    mode is ``'RGB'`` or ``'RGBA'``.
    """
    # typechecks *info* to some extent.
    if info is None:
        info = {}
    else:
        info = dict(info)

    # Syntax check mode string.
    parsed_mode = parse_mode(mode)
    grayscale, alpha, bitdepth = parsed_mode

    # Colour format.
    if 'greyscale' in info:
        if bool(info['greyscale']) != grayscale:
            raise Error("info['greyscale'] should match mode.")
    info['greyscale'] = grayscale
    if 'alpha' in info:
        if bool(info['alpha']) != alpha:
            raise Error("info['alpha'] should match mode.")
    info['alpha'] = alpha

    # Get bitdepth from *mode* if possible.
    if bitdepth:
        if info.get('bitdepth') and bitdepth != info['bitdepth']:
            raise Error("mode bitdepth (%d) should match info bitdepth (%d)." %
                        (bitdepth, info['bitdepth']))
        info['bitdepth'] = bitdepth

    planes = (3, 1)[grayscale] + alpha
    if 'planes' in info:
        if info['planes'] != planes:
            raise Error("info['planes'] should match mode.")

    # Dimensions.
    if 'size' in info:
        info['width'], info['height'] = check_sizes(info.get('size'),
                                                    info.get('width'),
                                                    info.get('height'))
    if 'height' not in info:
        try:
            l = len(a)
        except TypeError:
            raise Error(
                "len(a) does not work, supply info['height'] instead.")
        info['height'] = l

    # In order to work out whether we the array is 2D or 3D we need its
    # first row, which requires that we take a copy of its iterator.
    # We may also need the first row to derive width and bitdepth.
    row, a = peekiter(a)
    try:
        row[0][0]
        threed = True
        testelement = row[0]
    except (IndexError, TypeError):
        threed = False
        testelement = row
    if 'width' not in info:
        if threed:
            width = len(row)
        else:
            width = len(row) // planes
        info['width'] = width

    # Not implemented yet
    assert not threed

    if 'bitdepth' not in info:
        try:
            dtype = testelement.dtype
            # goto the "else:" clause.  Sorry.
        except AttributeError:
            try:
                # Try a Python array.array.
                bitdepth = 8 * testelement.itemsize
            except AttributeError:
                # We can't determine it from the array element's
                # datatype, use a default of 8.
                bitdepth = 8
        else:
            # If we got here without exception, we now assume that
            # the array is a numpy array.
            if dtype.kind == 'b':
                bitdepth = 1
            else:
                bitdepth = 8 * dtype.itemsize
        info['bitdepth'] = bitdepth

    for thing in ('width', 'height', 'bitdepth', 'greyscale', 'alpha'):
        assert thing in info
    return Image(a, info)


# So that refugee's from PIL feel more at home.  Not documented.
fromarray = from_array


class Image(object):

    """
    A PNG image.

    You can create an :class:`Image` object from
    an array of pixels by calling :meth:`png.from_array`.  It can be
    saved to disk with the :meth:`save` method.
    """

    def __init__(self, rows, info):
        """The constructor is not public.  Please do not call it."""
        self.rows = rows
        self.info = info

    def save(self, file):
        """
        Save the image to *file*.

        If *file* looks like an open file
        descriptor then it is used, otherwise it is treated as a
        filename and a fresh file is opened.

        In general, you can only call this method once; after it has
        been called the first time and the PNG image has been saved, the
        source data will have been streamed, and cannot be streamed
        again.
        """
        w = Writer(**self.info)

        try:
            file.write

            def close(): pass
        except AttributeError:
            file = open(file, 'wb')

            def close(): file.close()

        try:
            w.write(file, self.rows)
        finally:
            close()


class _readable(object):

    """A simple file-like interface for strings and arrays."""

    def __init__(self, buf):
        self.buf = buf
        self.offset = 0

    def read(self, n):
        """Read `n` chars from buffer"""
        r = self.buf[self.offset:self.offset + n]
        if isinstance(r, array):
            r = r.tostring()
        self.offset += n
        return r


class Reader(object):

    """PNG decoder in pure Python."""

    def __init__(self, _guess=None, **kw):
        """
        Create a PNG decoder object.

        The constructor expects exactly one keyword argument. If you
        supply a positional argument instead, it will guess the input
        type. You can choose among the following keyword arguments:

        filename
          Name of input file (a PNG file).
        file
          A file-like object (object with a read() method).
        bytes
          ``array`` or ``string`` with PNG data.
        """
        if ((_guess is not None and len(kw) != 0) or
                (_guess is None and len(kw) != 1)):
            raise TypeError("Reader() takes exactly 1 argument")

        # Will be the first 8 bytes, later on.  See validate_signature.
        self.signature = None
        self.transparent = None
        self.text = {}
        # A pair of (len, chunk_type) if a chunk has been read but its data and
        # checksum have not (in other words the file position is just
        # past the 4 bytes that specify the chunk type).  See preamble
        # method for how this is used.
        self.atchunk = None

        if _guess is not None:
            if isinstance(_guess, array):
                kw["bytes"] = _guess
            elif isinstance(_guess, str):
                kw["filename"] = _guess
            elif hasattr(_guess, 'read'):
                kw["file"] = _guess

        if "filename" in kw:
            self.file = open(kw["filename"], "rb")
        elif "file" in kw:
            self.file = kw["file"]
        elif "bytes" in kw:
            self.file = _readable(kw["bytes"])
        else:
            raise TypeError("expecting filename, file or bytes array")

    def chunk(self, seek=None, lenient=False):
        """
        Read the next PNG chunk from the input file

        returns a (*chunk_type*, *data*) tuple. *chunk_type* is the chunk's
        type as a byte string (all PNG chunk types are 4 bytes long).
        *data* is the chunk's data content, as a byte string.

        If the optional `seek` argument is
        specified then it will keep reading chunks until it either runs
        out of file or finds the chunk_type specified by the argument.  Note
        that in general the order of chunks in PNGs is unspecified, so
        using `seek` can cause you to miss chunks.

        If the optional `lenient` argument evaluates to `True`,
        checksum failures will raise warnings rather than exceptions.
        """
        self.validate_signature()
        while True:
            # http://www.w3.org/TR/PNG/#5Chunk-layout
            if not self.atchunk:
                self.atchunk = self.chunklentype()
            length, chunk_type = self.atchunk
            self.atchunk = None
            data = self.file.read(length)
            if len(data) != length:
                raise ChunkError('Chunk %s too short for required %i octets.'
                                 % (chunk_type, length))
            checksum = self.file.read(4)
            if len(checksum) != 4:
                raise ChunkError('Chunk %s too short for checksum.',
                                 chunk_type)
            if seek and chunk_type != seek:
                continue
            verify = zlib.crc32(strtobytes(chunk_type))
            verify = zlib.crc32(data, verify)
            # Whether the output from zlib.crc32 is signed or not varies
            # according to hideous implementation details, see
            # http://bugs.python.org/issue1202 .
            # We coerce it to be positive here (in a way which works on
            # Python 2.3 and older).
            verify &= 2**32 - 1
            verify = struct.pack('!I', verify)
            if checksum != verify:
                (a, ) = struct.unpack('!I', checksum)
                (b, ) = struct.unpack('!I', verify)
                message = "Checksum error in %s chunk: 0x%08X != 0x%08X." %\
                    (chunk_type, a, b)
                if lenient:
                    warnings.warn(message, RuntimeWarning)
                else:
                    raise ChunkError(message)
            return chunk_type, data

    def chunks(self):
        """Return an iterator that will yield each chunk as a
        (*chunktype*, *content*) pair.
        """
        while True:
            t, v = self.chunk()
            yield t, v
            if t == 'IEND':
                break

    def deinterlace(self, raw):
        """
        Read raw pixel data, undo filters, deinterlace, and flatten.

        Return in flat row flat pixel format.
        """
        # Values per row (of the target image)
        vpr = self.width * self.planes

        # Make a result array, and make it big enough.  Interleaving
        # writes to the output array randomly (well, not quite), so the
        # entire output array must be in memory.
        if self.bitdepth > 8:
            a = newHarray(vpr * self.height)
        else:
            a = newBarray(vpr * self.height)
        source_offset = 0
        filt = Filter(self.bitdepth * self.planes)
        for xstart, ystart, xstep, ystep in _adam7:
            if xstart >= self.width:
                continue
            # The previous (reconstructed) scanline.  None at the
            # beginning of a pass to indicate that there is no previous
            # line.
            filt.prev = None
            # Pixels per row (reduced pass image)
            ppr = int(math.ceil((self.width - xstart) / float(xstep)))
            # Row size in bytes for this pass.
            row_size = int(math.ceil(self.psize * ppr))
            for y in range(ystart, self.height, ystep):
                filter_type = raw[source_offset]
                scanline = raw[source_offset + 1:source_offset + row_size + 1]
                source_offset += (row_size + 1)
                if filter_type not in (0, 1, 2, 3, 4):
                    raise FormatError('Invalid PNG Filter Type.'
                                      '  See http://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters .')
                filt.undo_filter(filter_type, scanline)
                # Convert so that there is one element per pixel value
                flat = self.serialtoflat(scanline, ppr)
                if xstep == 1:
                    assert xstart == 0
                    offset = y * vpr
                    a[offset:offset + vpr] = flat
                else:
                    offset = y * vpr + xstart * self.planes
                    end_offset = (y + 1) * vpr
                    skip = self.planes * xstep
                    for i in range(self.planes):
                        a[offset + i:end_offset:skip] = \
                            flat[i::self.planes]
        return a

    def iterboxed(self, rows):
        """
        Iterator that yields each scanline in boxed row flat pixel format.

        `rows` should be an iterator that yields the bytes of
        each row in turn.
        """
        def asvalues(raw):
            """
            Convert a row of raw bytes into a flat row.

            Result may or may not share with argument
            """
            if self.bitdepth == 8:
                return raw
            if self.bitdepth == 16:
                raw = bytearray_to_bytes(raw)
                return array('H', struct.unpack('!%dH' % (len(raw) // 2), raw))
            assert self.bitdepth < 8
            width = self.width
            # Samples per byte
            spb = 8 // self.bitdepth
            out = newBarray()
            mask = 2 ** self.bitdepth - 1
            #                                      reversed range(spb)
            shifts = [self.bitdepth * it for it in range(spb - 1, -1, -1)]
            for o in raw:
                out.extend([mask & (o >> i) for i in shifts])
            return out[:width]

        return map(asvalues, rows)

    def serialtoflat(self, raw, width=None):
        """Convert serial format (byte stream) pixel data to flat row
        flat pixel.
        """
        if self.bitdepth == 8:
            return raw
        if self.bitdepth == 16:
            raw = bytearray_to_bytes(raw)
            return array('H',
                         struct.unpack('!%dH' % (len(raw) // 2), raw))
        assert self.bitdepth < 8
        if width is None:
            width = self.width
        # Samples per byte
        spb = 8 // self.bitdepth
        out = newBarray()
        mask = 2**self.bitdepth - 1
        #                                      reversed range(spb)
        shifts = [self.bitdepth * it for it in range(spb - 1, -1, -1)]
        l = width
        for o in raw:
            out.extend([(mask & (o >> s)) for s in shifts][:l])
            l -= spb
            if l <= 0:
                l = width
        return out

    def iterstraight(self, raw):
        """
        Iterator that undoes the effect of filtering

        Yields each row in serialised format (as a sequence of bytes).
        Assumes input is straightlaced.  `raw` should be an iterable
        that yields the raw bytes in chunks of arbitrary size.
        """

        # length of row, in bytes (with filter)
        rb_1 = self.row_bytes + 1
        a = bytearray()
        filt = Filter(self.bitdepth * self.planes)
        for some in raw:
            a.extend(some)
            offset = 0
            while len(a) >= rb_1 + offset:
                filter_type = a[offset]
                if filter_type not in (0, 1, 2, 3, 4):
                    raise FormatError('Invalid PNG Filter Type.'
                                      '  See http://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters .')
                scanline = a[offset + 1:offset + rb_1]
                filt.undo_filter(filter_type, scanline)
                yield scanline
                offset += rb_1
            del a[:offset]

        if len(a) != 0:
            # :file:format We get here with a file format error:
            # when the available bytes (after decompressing) do not
            # pack into exact rows.
            raise FormatError(
                'Wrong size for decompressed IDAT chunk.')
        assert len(a) == 0

    def validate_signature(self):
        """If signature (header) has not been read then read and validate it"""
        if self.signature:
            return
        self.signature = self.file.read(8)
        if self.signature != png_signature:
            raise FormatError("PNG file has invalid signature.")

    def preamble(self, lenient=False):
        """
        Extract the image metadata

        Extract the image metadata by reading the initial part of
        the PNG file up to the start of the ``IDAT`` chunk.  All the
        chunks that precede the ``IDAT`` chunk are read and either
        processed for metadata or discarded.

        If the optional `lenient` argument evaluates to `True`, checksum
        failures will raise warnings rather than exceptions.
        """
        self.validate_signature()
        while True:
            if not self.atchunk:
                self.atchunk = self.chunklentype()
                if self.atchunk is None:
                    raise FormatError(
                        'This PNG file has no IDAT chunks.')
            if self.atchunk[1] == 'IDAT':
                return
            self.process_chunk(lenient=lenient)

    def chunklentype(self):
        """Reads just enough of the input to determine the next
        chunk's length and type, returned as a (*length*, *chunk_type*) pair
        where *chunk_type* is a string.  If there are no more chunks, ``None``
        is returned.
        """
        x = self.file.read(8)
        if not x:
            return None
        if len(x) != 8:
            raise FormatError(
                'End of file whilst reading chunk length and type.')
        length, chunk_type = struct.unpack('!I4s', x)
        chunk_type = bytestostr(chunk_type)
        if length > 2**31 - 1:
            raise FormatError('Chunk %s is too large: %d.' % (chunk_type,
                                                              length))
        return length, chunk_type

    def process_chunk(self, lenient=False):
        """
        Process the next chunk and its data.

        If the optional `lenient` argument evaluates to `True`,
        checksum failures will raise warnings rather than exceptions.
        """
        chunk_type, data = self.chunk(lenient=lenient)
        method = '_process_' + chunk_type
        m = getattr(self, method, None)
        if m:
            m(data)

    def _process_IHDR(self, data):
        # http://www.w3.org/TR/PNG/#11IHDR
        if len(data) != 13:
            raise FormatError('IHDR chunk has incorrect length.')
        (self.width, self.height, self.bitdepth, self.color_type,
         self.compression, self.filter,
         self.interlace) = struct.unpack("!2I5B", data)

        check_bitdepth_colortype(self.bitdepth, self.color_type)

        if self.compression != 0:
            raise Error("unknown compression method %d" % self.compression)
        if self.filter != 0:
            raise FormatError("Unknown filter method %d,"
                              " see http://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters ."
                              % self.filter)
        if self.interlace not in (0, 1):
            raise FormatError("Unknown interlace method %d,"
                              " see http://www.w3.org/TR/2003/REC-PNG-20031110/#8InterlaceMethods ."
                              % self.interlace)

        # Derived values
        # http://www.w3.org/TR/PNG/#6Colour-values
        colormap = bool(self.color_type & 1)
        greyscale = not (self.color_type & 2)
        alpha = bool(self.color_type & 4)
        color_planes = (3, 1)[greyscale or colormap]
        planes = color_planes + alpha

        self.colormap = colormap
        self.greyscale = greyscale
        self.alpha = alpha
        self.color_planes = color_planes
        self.planes = planes
        self.psize = float(self.bitdepth) / float(8) * planes
        if int(self.psize) == self.psize:
            self.psize = int(self.psize)
        self.row_bytes = int(math.ceil(self.width * self.psize))
        # Stores PLTE chunk if present, and is used to check
        # chunk ordering constraints.
        self.plte = None
        # Stores tRNS chunk if present, and is used to check chunk
        # ordering constraints.
        self.trns = None
        # Stores sbit chunk if present.
        self.sbit = None
        # If an sRGB chunk is present, rendering intent is updated
        self.rendering_intent = None

    def _process_PLTE(self, data):
        # http://www.w3.org/TR/PNG/#11PLTE
        if self.plte:
            warnings.warn("Multiple PLTE chunks present.")
        self.plte = data
        if len(data) % 3 != 0:
            raise FormatError(
                "PLTE chunk's length should be a multiple of 3.")
        if len(data) > (2**self.bitdepth) * 3:
            raise FormatError("PLTE chunk is too long.")
        if len(data) == 0:
            raise FormatError("Empty PLTE is not allowed.")

    def _process_bKGD(self, data):
        try:
            if self.colormap:
                if not self.plte:
                    warnings.warn(
                        "PLTE chunk is required before bKGD chunk.")
                self.background = struct.unpack('B', data)
            else:
                self.background = struct.unpack("!%dH" % self.color_planes,
                                                data)
        except struct.error:
            raise FormatError("bKGD chunk has incorrect length.")

    def _process_tRNS(self, data):
        # http://www.w3.org/TR/PNG/#11tRNS
        self.trns = data
        if self.colormap:
            if not self.plte:
                warnings.warn("PLTE chunk is required before tRNS chunk.")
            else:
                if len(data) > len(self.plte) / 3:
                    # Was warning, but promoted to Error as it
                    # would otherwise cause pain later on.
                    raise FormatError("tRNS chunk is too long.")
        else:
            if self.alpha:
                raise FormatError(
                    "tRNS chunk is not valid with colour type %d." %
                    self.color_type)
            try:
                self.transparent = \
                    struct.unpack("!%dH" % self.color_planes, data)
            except struct.error:
                raise FormatError("tRNS chunk has incorrect length.")

    def _process_gAMA(self, data):
        try:
            self.gamma = struct.unpack("!L", data)[0] / 100000.0
        except struct.error:
            raise FormatError("gAMA chunk has incorrect length.")

    def _process_iCCP(self, data):
        i = data.index(zerobyte)
        self.icc_profile_name = data[:i]
        compression = data[i:i + 1]
        # TODO: Raise FormatError
        assert (compression == zerobyte)
        self.icc_profile = zlib.decompress(data[i + 2:])

    def _process_sBIT(self, data):
        self.sbit = data
        if (self.colormap and len(data) != 3 or
                not self.colormap and len(data) != self.planes):
            raise FormatError("sBIT chunk has incorrect length.")

    def _process_sRGB(self, data):
        self.rendering_intent, = struct.unpack('B', data)

    def _process_cHRM(self, data):
        if len(data) != struct.calcsize("!8L"):
            raise FormatError("cHRM chunk has incorrect length.")
        white_x, white_y, red_x, red_y, green_x, green_y, blue_x, blue_y = \
            tuple([value / 100000.0 for value in struct.unpack("!8L", data)])
        self.white_point = white_x, white_y
        self.rgb_points = (red_x, red_y), (green_x, green_y), (blue_x, blue_y)

    def _process_tEXt(self, data):
        # http://www.w3.org/TR/PNG/#11tEXt
        i = data.index(zerobyte)
        keyword = data[:i]
        try:
            keyword = str(keyword, 'latin-1')
        except:
            pass
        self.text[keyword] = data[i + 1:].decode('latin-1')

    def _process_zTXt(self, data):
        # http://www.w3.org/TR/PNG/#11zTXt
        i = data.index(zerobyte)
        keyword = data[:i]
        try:
            keyword = str(keyword, 'latin-1')
        except:
            pass
        # TODO: Raise FormatError
        assert data[i:i + 1] == zerobyte
        text = zlib.decompress(data[i + 2:]).decode('latin-1')
        self.text[keyword] = text

    def _process_iTXt(self, data):
        # http://www.w3.org/TR/PNG/#11iTXt
        i = data.index(zerobyte)
        keyword = data[:i]
        try:
            keyword = str(keyword, 'latin-1')
        except:
            pass
        if (data[i:i + 1] != zerobyte):
            # TODO: Support for compression!!
            return
        # TODO: Raise FormatError
        assert (data[i + 1:i + 2] == zerobyte)
        data_ = data[i + 3:]
        i = data_.index(zerobyte)
        # skip language tag
        data_ = data_[i + 1:]
        i = data_.index(zerobyte)
        # skip translated keyword
        data_ = data_[i + 1:]
        self.text[keyword] = data_.decode('utf-8')

    def _process_pHYs(self, data):
        # http://www.w3.org/TR/PNG/#11pHYs
        ppux, ppuy, unit = struct.unpack('!IIB', data)
        self.resolution = ((ppux, ppuy), unit)

    def _process_tIME(self, data):
        # http://www.w3.org/TR/PNG/#11tIME
        fmt = "!H5B"
        if len(data) != struct.calcsize(fmt):
            raise FormatError("tIME chunk has incorrect length.")
        self.last_mod_time = struct.unpack(fmt, data)

    def idat(self, lenient=False):
        """Iterator that yields all the ``IDAT`` chunks as strings."""
        while True:
            try:
                chunk_type, data = self.chunk(lenient=lenient)
            except ValueError:
                e = sys.exc_info()[1]
                raise ChunkError(e.args[0])
            if chunk_type == 'IEND':
                # http://www.w3.org/TR/PNG/#11IEND
                break
            if chunk_type != 'IDAT':
                continue
            # chunk_type == 'IDAT'
            # http://www.w3.org/TR/PNG/#11IDAT
            if self.colormap and not self.plte:
                warnings.warn("PLTE chunk is required before IDAT chunk")
            yield data

    def idatdecomp(self, lenient=False, max_length=0):
        """Iterator that yields decompressed ``IDAT`` strings."""
        # Currently, with no max_length paramter to decompress, this
        # routine will do one yield per IDAT chunk.  So not very
        # incremental.
        d = zlib.decompressobj()
        # Each IDAT chunk is passed to the decompressor, then any
        # remaining state is decompressed out.
        for data in self.idat(lenient):
            # :todo: add a max_length argument here to limit output
            # size.
            yield bytearray(d.decompress(data))
        yield bytearray(d.flush())

    def read(self, lenient=False):
        """
        Read the PNG file and decode it.

        Returns (`width`, `height`, `pixels`, `metadata`).

        May use excessive memory.

        `pixels` are returned in boxed row flat pixel format.

        If the optional `lenient` argument evaluates to True,
        checksum failures will raise warnings rather than exceptions.
        """
        self.preamble(lenient=lenient)
        raw = self.idatdecomp(lenient)

        if self.interlace:
            raw = bytearray(itertools.chain(*raw))
            arraycode = 'BH'[self.bitdepth > 8]
            # Like :meth:`group` but producing an array.array object for
            # each row.
            pixels = map(lambda *row: array(arraycode, row),
                         *[iter(self.deinterlace(raw))] * self.width * self.planes)
        else:
            pixels = self.iterboxed(self.iterstraight(raw))
        meta = dict()
        for attr in 'greyscale alpha planes bitdepth interlace'.split():
            meta[attr] = getattr(self, attr)
        meta['size'] = (self.width, self.height)
        for attr in ('gamma', 'transparent', 'background', 'last_mod_time',
                     'icc_profile', 'icc_profile_name', 'resolution', 'text',
                     'rendering_intent', 'white_point', 'rgb_points'):
            a = getattr(self, attr, None)
            if a is not None:
                meta[attr] = a
        if self.plte:
            meta['palette'] = self.palette()
        return self.width, self.height, pixels, meta

    def read_flat(self):
        """
        Read a PNG file and decode it into flat row flat pixel format.

        Returns (*width*, *height*, *pixels*, *metadata*).

        May use excessive memory.

        `pixels` are returned in flat row flat pixel format.

        See also the :meth:`read` method which returns pixels in the
        more stream-friendly boxed row flat pixel format.
        """
        x, y, pixel, meta = self.read()
        arraycode = 'BH'[meta['bitdepth'] > 8]
        pixel = array(arraycode, itertools.chain(*pixel))
        return x, y, pixel, meta

    def palette(self, alpha='natural'):
        """
        Returns a palette that is a sequence of 3-tuples or 4-tuples

        Synthesizing it from the ``PLTE`` and ``tRNS`` chunks.  These
        chunks should have already been processed (for example, by
        calling the :meth:`preamble` method).  All the tuples are the
        same size: 3-tuples if there is no ``tRNS`` chunk, 4-tuples when
        there is a ``tRNS`` chunk.  Assumes that the image is colour type
        3 and therefore a ``PLTE`` chunk is required.

        If the `alpha` argument is ``'force'`` then an alpha channel is
        always added, forcing the result to be a sequence of 4-tuples.
        """
        if not self.plte:
            raise FormatError(
                "Required PLTE chunk is missing in colour type 3 image.")
        plte = group(bytearray(self.plte), 3)
        if self.trns or alpha == 'force':
            trns = bytearray(self.trns or strtobytes(''))
            trns.extend([255] * (len(plte) - len(trns)))
            plte = list(map(operator.add, plte, group(trns, 1)))
        return plte

    def asDirect(self):
        """Returns the image data as a direct representation of an
        ``x * y * planes`` array.  This method is intended to remove the
        need for callers to deal with palettes and transparency
        themselves.  Images with a palette (colour type 3)
        are converted to RGB or RGBA; images with transparency (a
        ``tRNS`` chunk) are converted to LA or RGBA as appropriate.
        When returned in this format the pixel values represent the
        colour value directly without needing to refer to palettes or
        transparency information.

        Like the :meth:`read` method this method returns a 4-tuple:

        (*width*, *height*, *pixels*, *meta*)

        This method normally returns pixel values with the bit depth
        they have in the source image, but when the source PNG has an
        ``sBIT`` chunk it is inspected and can reduce the bit depth of
        the result pixels; pixel values will be reduced according to
        the bit depth specified in the ``sBIT`` chunk (PNG nerds should
        note a single result bit depth is used for all channels; the
        maximum of the ones specified in the ``sBIT`` chunk.  An RGB565
        image will be rescaled to 6-bit RGB666).

        The *meta* dictionary that is returned reflects the `direct`
        format and not the original source image.  For example, an RGB
        source image with a ``tRNS`` chunk to represent a transparent
        colour, will have ``planes=3`` and ``alpha=False`` for the
        source image, but the *meta* dictionary returned by this method
        will have ``planes=4`` and ``alpha=True`` because an alpha
        channel is synthesized and added.

        *pixels* is the pixel data in boxed row flat pixel format (just
        like the :meth:`read` method).

        All the other aspects of the image data are not changed.
        """
        self.preamble()
        # Simple case, no conversion necessary.
        if not self.colormap and not self.trns and not self.sbit:
            return self.read()

        x, y, pixels, meta = self.read()

        if self.colormap:
            meta['colormap'] = False
            meta['alpha'] = bool(self.trns)
            meta['bitdepth'] = 8
            meta['planes'] = 3 + bool(self.trns)
            plte = self.palette()

            def iterpal(pixels):
                for row in pixels:
                    row = [plte[i] for i in row]
                    yield bytearray(itertools.chain(*row))
            pixels = iterpal(pixels)
        elif self.trns:
            # It would be nice if there was some reasonable way
            # of doing this without generating a whole load of
            # intermediate tuples.  But tuples does seem like the
            # easiest way, with no other way clearly much simpler or
            # much faster.  (Actually, the L to LA conversion could
            # perhaps go faster (all those 1-tuples!), but I still
            # wonder whether the code proliferation is worth it)
            it = self.transparent
            maxval = 2**meta['bitdepth'] - 1
            planes = meta['planes']
            meta['alpha'] = True
            meta['planes'] += 1
            if meta['bitdepth'] > 8:
                def wrap_array(row):
                    return array('H', row)
            else:
                wrap_array = bytearray

            def itertrns(pixels):
                for row in pixels:
                    # For each row we group it into pixels, then form a
                    # characterisation vector that says whether each
                    # pixel is opaque or not.  Then we convert
                    # True/False to 0/maxval (by multiplication),
                    # and add it as the extra channel.
                    row = group(row, planes)
                    opa = [maxval * (it != i) for i in row]
                    opa = zip(opa)  # convert to 1-tuples
                    yield wrap_array(itertools.chain(*list(map(operator.add,
                                                               row, opa))))
            pixels = itertrns(pixels)
        targetbitdepth = None
        if self.sbit:
            sbit = struct.unpack('%dB' % len(self.sbit), self.sbit)
            targetbitdepth = max(sbit)
            if targetbitdepth > meta['bitdepth']:
                raise Error('sBIT chunk %r exceeds bitdepth %d' %
                            (sbit, self.bitdepth))
            if min(sbit) <= 0:
                raise Error('sBIT chunk %r has a 0-entry' % sbit)
            if targetbitdepth == meta['bitdepth']:
                targetbitdepth = None
        if targetbitdepth:
            shift = meta['bitdepth'] - targetbitdepth
            meta['bitdepth'] = targetbitdepth

            def itershift(pixels):
                for row in pixels:
                    yield array('BH'[targetbitdepth > 8],
                                [it >> shift for it in row])
            pixels = itershift(pixels)
        return x, y, pixels, meta

    def asFloat(self, maxval=1.0):
        """Return image pixels as per :meth:`asDirect` method, but scale
        all pixel values to be floating point values between 0.0 and
        *maxval*.
        """
        x, y, pixels, info = self.asDirect()
        sourcemaxval = 2**info['bitdepth'] - 1
        del info['bitdepth']
        info['maxval'] = float(maxval)
        factor = float(maxval) / float(sourcemaxval)

        def iterfloat():
            for row in pixels:
                yield [factor * it for it in row]
        return x, y, iterfloat(), info

    def _as_rescale(self, get, targetbitdepth):
        """Helper used by :meth:`asRGB8` and :meth:`asRGBA8`."""
        width, height, pixels, meta = get()
        maxval = 2**meta['bitdepth'] - 1
        targetmaxval = 2**targetbitdepth - 1
        factor = float(targetmaxval) / float(maxval)
        meta['bitdepth'] = targetbitdepth

        def iterscale(rows):
            for row in rows:
                yield array('BH'[targetbitdepth > 8],
                            [int(round(x * factor)) for x in row])
        if maxval == targetmaxval:
            return width, height, pixels, meta
        else:
            if 'transparent' in meta:
                transparent = meta['transparent']
                if isinstance(transparent, tuple):
                    transparent = tuple(list(
                                        iterscale((transparent,))
                                        )[0])
                else:
                    transparent = tuple(list(
                                        iterscale(((transparent,),))
                                        )[0])[0]
                meta['transparent'] = transparent
            return width, height, iterscale(pixels), meta

    def asRGB8(self):
        """
        Return the image data as an RGB pixels with 8-bits per sample.

        This is like the :meth:`asRGB` method except that
        this method additionally rescales the values so that they
        are all between 0 and 255 (8-bit).  In the case where the
        source image has a bit depth < 8 the transformation preserves
        all the information; where the source image has bit depth
        > 8, then rescaling to 8-bit values loses precision.  No
        dithering is performed.  Like :meth:`asRGB`, an alpha channel
        in the source image will raise an exception.

        This function returns a 4-tuple:
        (*width*, *height*, *pixels*, *metadata*).
        *width*, *height*, *metadata* are as per the
        :meth:`read` method.

        *pixels* is the pixel data in boxed row flat pixel format.
        """
        return self._as_rescale(self.asRGB, 8)

    def asRGBA8(self):
        """
        Return the image data as RGBA pixels with 8-bits per sample.

        This method is similar to :meth:`asRGB8` and
        :meth:`asRGBA`:  The result pixels have an alpha channel, *and*
        values are rescaled to the range 0 to 255.  The alpha channel is
        synthesized if necessary (with a small speed penalty).
        """
        return self._as_rescale(self.asRGBA, 8)

    def asRGB(self):
        """
        Return image as RGB pixels.

        RGB colour images are passed through unchanged;
        greyscales are expanded into RGB  triplets
        (there is a small speed overhead for doing this).

        An alpha channel in the source image will raise an exception.

        The return values are as for the :meth:`read` method
        except that the *metadata* reflect the returned pixels, not the
        source image.  In particular, for this method
        ``metadata['greyscale']`` will be ``False``.
        """
        width, height, pixels, meta = self.asDirect()
        if meta['alpha']:
            raise Error("will not convert image with alpha channel to RGB")
        if not meta['greyscale']:
            return width, height, pixels, meta
        meta['greyscale'] = False
        newarray = (newBarray, newHarray)[meta['bitdepth'] > 8]

        def iterrgb():
            for row in pixels:
                a = newarray(3 * width)
                for i in range(3):
                    a[i::3] = row
                yield a
        return width, height, iterrgb(), meta

    def asRGBA(self):
        """
        Return image as RGBA pixels.

        Greyscales are expanded into RGB triplets;
        an alpha channel is synthesized if necessary.
        The return values are as for the :meth:`read` method
        except that the *metadata* reflect the returned pixels, not the
        source image.  In particular, for this method
        ``metadata['greyscale']`` will be ``False``, and
        ``metadata['alpha']`` will be ``True``.
        """
        width, height, pixels, meta = self.asDirect()
        if meta['alpha'] and not meta['greyscale']:
            return width, height, pixels, meta
        maxval = 2**meta['bitdepth'] - 1
        if meta['bitdepth'] > 8:
            def newarray():
                return array('H', [maxval] * 4 * width)
        else:
            def newarray():
                return bytearray([maxval] * 4 * width)

        # Not best way, but we have only array of bytes accelerated now
        if meta['bitdepth'] <= 8:
            filt = BaseFilter()
        else:
            filt = iBaseFilter()

        if meta['alpha'] and meta['greyscale']:
            # LA to RGBA
            def convert():
                for row in pixels:
                    # Create a fresh target row, then copy L channel
                    # into first three target channels, and A channel
                    # into fourth channel.
                    a = newarray()
                    filt.convert_la_to_rgba(row, a)
                    yield a
        elif meta['greyscale']:
            # L to RGBA
            def convert():
                for row in pixels:
                    a = newarray()
                    filt.convert_l_to_rgba(row, a)
                    yield a
        else:
            assert not meta['alpha'] and not meta['greyscale']
            # RGB to RGBA

            def convert():
                for row in pixels:
                    a = newarray()
                    filt.convert_rgb_to_rgba(row, a)
                    yield a
        meta['alpha'] = True
        meta['greyscale'] = False
        return width, height, convert(), meta


def check_bitdepth_colortype(bitdepth, colortype):
    """
    Check that `bitdepth` and `colortype` are both valid,
    and specified in a valid combination. Returns if valid,
    raise an Exception if not valid.
    """
    if bitdepth not in (1, 2, 4, 8, 16):
        raise FormatError("invalid bit depth %d" % bitdepth)
    if colortype not in (0, 2, 3, 4, 6):
        raise FormatError("invalid colour type %d" % colortype)
    # Check indexed (palettized) images have 8 or fewer bits
    # per pixel; check only indexed or greyscale images have
    # fewer than 8 bits per pixel.
    if colortype & 1 and bitdepth > 8:
        raise FormatError(
            "Indexed images (colour type %d) cannot"
            " have bitdepth > 8 (bit depth %d)."
            " See http://www.w3.org/TR/2003/REC-PNG-20031110/#table111 ."
            % (bitdepth, colortype))
    if bitdepth < 8 and colortype not in (0, 3):
        raise FormatError("Illegal combination of bit depth (%d)"
                          " and colour type (%d)."
                          " See http://www.w3.org/TR/2003/REC-PNG-20031110/#table111 ."
                          % (bitdepth, colortype))


def isinteger(x):
    """Check if `x` is platform native integer"""
    try:
        return int(x) == x
    except (TypeError, ValueError):
        return False


# === Legacy Version Support ===

# In order to work on Python 2.3 we fix up a recurring annoyance involving
# the array type.  In Python 2.3 an array cannot be initialised with an
# array, and it cannot be extended with a list (or other sequence).
# Both of those are repeated issues in the code.  Whilst I would not
# normally tolerate this sort of behaviour, here we "shim" a replacement
# for array into place (and hope no-one notices).  You never read this.

try:
    array('B').extend([])
    array('B', array('B'))
except TypeError:
    # Expect to get here on Python 2.3
    class _array_shim(array):
        true_array = array

        def __new__(cls, typecode, init=None):
            super_new = super(_array_shim, cls).__new__
            it = super_new(cls, typecode)
            if init is None:
                return it
            it.extend(init)
            return it

        def extend(self, extension):
            super_extend = super(_array_shim, self).extend
            if isinstance(extension, self.true_array):
                return super_extend(extension)
            if not isinstance(extension, (list, str)):
                # Convert to list.  Allows iterators to work.
                extension = list(extension)
            return super_extend(self.true_array(self.typecode, extension))
    array = _array_shim

    # Original array initialisation is faster but multiplication change class
    def newBarray(length=0):
        return array('B', [0] * length)

    def newHarray(length=0):
        return array('H', [0] * length)

# === Command Line Support ===

def read_pam_header(infile):
    """
    Read (the rest of a) PAM header.

    `infile` should be positioned
    immediately after the initial 'P7' line (at the beginning of the
    second line).  Returns are as for `read_pnm_header`.
    """
    # Unlike PBM, PGM, and PPM, we can read the header a line at a time.
    header = dict()
    while True:
        l = infile.readline().strip()
        if l == strtobytes('ENDHDR'):
            break
        if not l:
            raise EOFError('PAM ended prematurely')
        if l[0] == strtobytes('#'):
            continue
        l = l.split(None, 1)
        if l[0] not in header:
            header[l[0]] = l[1]
        else:
            header[l[0]] += strtobytes(' ') + l[1]

    required = ['WIDTH', 'HEIGHT', 'DEPTH', 'MAXVAL']
    required = [strtobytes(x) for x in required]
    WIDTH, HEIGHT, DEPTH, MAXVAL = required
    present = [x for x in required if x in header]
    if len(present) != len(required):
        raise Error('PAM file must specify WIDTH, HEIGHT, DEPTH, and MAXVAL')
    width = int(header[WIDTH])
    height = int(header[HEIGHT])
    depth = int(header[DEPTH])
    maxval = int(header[MAXVAL])
    if (width <= 0 or
        height <= 0 or
        depth <= 0 or
            maxval <= 0):
        raise Error(
            'WIDTH, HEIGHT, DEPTH, MAXVAL must all be positive integers')
    return 'P7', width, height, depth, maxval


def read_pnm_header(infile, supported=('P5', 'P6')):
    """
    Read a PNM header, returning (format,width,height,depth,maxval).

    `width` and `height` are in pixels.  `depth` is the number of
    channels in the image; for PBM and PGM it is synthesized as 1, for
    PPM as 3; for PAM images it is read from the header.  `maxval` is
    synthesized (as 1) for PBM images.
    """
    # Generally, see http://netpbm.sourceforge.net/doc/ppm.html
    # and http://netpbm.sourceforge.net/doc/pam.html
    supported = [strtobytes(x) for x in supported]

    # Technically 'P7' must be followed by a newline, so by using
    # rstrip() we are being liberal in what we accept.  I think this
    # is acceptable.
    type = infile.read(3).rstrip()
    if type not in supported:
        raise NotImplementedError('file format %s not supported' % type)
    if type == strtobytes('P7'):
        # PAM header parsing is completely different.
        return read_pam_header(infile)
    # Expected number of tokens in header (3 for P4, 4 for P6)
    expected = 4
    pbm = ('P1', 'P4')
    if type in pbm:
        expected = 3
    header = [type]

    # We have to read the rest of the header byte by byte because the
    # final whitespace character (immediately following the MAXVAL in
    # the case of P6) may not be a newline.  Of course all PNM files in
    # the wild use a newline at this point, so it's tempting to use
    # readline; but it would be wrong.
    def getc():
        c = infile.read(1)
        if not c:
            raise Error('premature EOF reading PNM header')
        return c

    c = getc()
    while True:
        # Skip whitespace that precedes a token.
        while c.isspace():
            c = getc()
        # Skip comments.
        while c == '#':
            while c not in '\n\r':
                c = getc()
        if not c.isdigit():
            raise Error('unexpected character %s found in header' % c)
        # According to the specification it is legal to have comments
        # that appear in the middle of a token.
        # This is bonkers; I've never seen it; and it's a bit awkward to
        # code good lexers in Python (no goto).  So we break on such
        # cases.
        token = bytes()
        while c.isdigit():
            token += c
            c = getc()
        # Slight hack.  All "tokens" are decimal integers, so convert
        # them here.
        header.append(int(token))
        if len(header) == expected:
            break
    # Skip comments (again)
    while c == '#':
        while c not in '\n\r':
            c = getc()
    if not c.isspace():
        raise Error('expected header to end with whitespace, not %s' % c)

    if type in pbm:
        # synthesize a MAXVAL
        header.append(1)
    depth = (1, 3)[type == strtobytes('P6')]
    return header[0], header[1], header[2], depth, header[3]


def write_pnm(file, width, height, pixels, meta):
    """Write a Netpbm PNM/PAM file."""
    bitdepth = meta['bitdepth']
    maxval = 2**bitdepth - 1
    # Rudely, the number of image planes can be used to determine
    # whether we are L (PGM), LA (PAM), RGB (PPM), or RGBA (PAM).
    planes = meta['planes']
    # Can be an assert as long as we assume that pixels and meta came
    # from a PNG file.
    assert planes in (1, 2, 3, 4)
    if planes in (1, 3):
        if 1 == planes:
            # PGM
            # Could generate PBM if maxval is 1, but we don't (for one
            # thing, we'd have to convert the data, not just blat it
            # out).
            fmt = 'P5'
        else:
            # PPM
            fmt = 'P6'
        header = '%s %d %d %d\n' % (fmt, width, height, maxval)
    if planes in (2, 4):
        # PAM
        # See http://netpbm.sourceforge.net/doc/pam.html
        if 2 == planes:
            tupltype = 'GRAYSCALE_ALPHA'
        else:
            tupltype = 'RGB_ALPHA'
        header = ('P7\nWIDTH %d\nHEIGHT %d\nDEPTH %d\nMAXVAL %d\n'
                  'TUPLTYPE %s\nENDHDR\n' %
                  (width, height, planes, maxval, tupltype))
    file.write(strtobytes(header))
    # Values per row
    vpr = planes * width
    # struct format
    fmt = '>%d' % vpr
    if maxval > 0xff:
        fmt = fmt + 'H'
    else:
        fmt = fmt + 'B'
    for row in pixels:
        file.write(struct.pack(fmt, *row))
    file.flush()


def color_triple(color):
    """
    Convert a command line colour value to a RGB triple of integers.
    FIXME: Somewhere we need support for greyscale backgrounds etc.
    """
    if color.startswith('#') and len(color) == 4:
        return (int(color[1], 16),
                int(color[2], 16),
                int(color[3], 16))
    if color.startswith('#') and len(color) == 7:
        return (int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16))
    elif color.startswith('#') and len(color) == 13:
        return (int(color[1:5], 16),
                int(color[5:9], 16),
                int(color[9:13], 16))


def _add_common_options(parser):
    """Call *parser.add_option* for each of the options that are
    common between this PNG--PNM conversion tool and the gen
    tool.
    """
    parser.add_option("-i", "--interlace",
                      default=False, action="store_true",
                      help="create an interlaced PNG file (Adam7)")
    parser.add_option("-t", "--transparent",
                      action="store", type="string", metavar="#RRGGBB",
                      help="mark the specified colour as transparent")
    parser.add_option("-b", "--background",
                      action="store", type="string", metavar="#RRGGBB",
                      help="save the specified background colour")
    parser.add_option("-g", "--gamma",
                      action="store", type="float", metavar="value",
                      help="save the specified gamma value")
    parser.add_option("-c", "--compression",
                      action="store", type="int", metavar="level",
                      help="zlib compression level (0-9)")
    return parser
