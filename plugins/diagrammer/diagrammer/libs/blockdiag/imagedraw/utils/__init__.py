# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import math
import unicodedata
from functools import wraps

from blockdiag.utils import Size


def is_zenkaku(char):
    """Detect given character is Japanese ZENKAKU character"""
    char_width = unicodedata.east_asian_width(char)
    return char_width in "WFA"


def zenkaku_len(string):
    """Count Japanese ZENKAKU characters from string"""
    return len([x for x in string if is_zenkaku(x)])


def hankaku_len(string):
    """Count non Japanese ZENKAKU characters from string"""
    return len([x for x in string if not is_zenkaku(x)])


def string_width(string):
    """Measure rendering width of string.
       Count ZENKAKU-character as 2-point and non ZENKAKU-character as 1-point
    """
    widthmap = {'Na': 1, 'N': 1, 'H': 1, 'W': 2, 'F': 2, 'A': 2}
    return sum(widthmap[unicodedata.east_asian_width(c)] for c in string)


def textsize(string, font):
    """Measure rendering size (width and height) of line.
       Returned size will not be exactly as rendered text size,
       Because this method does not use fonts to measure size.
    """
    width = (zenkaku_len(string) * font.size +
             hankaku_len(string) * font.size * 0.55)

    return Size(int(math.ceil(width)), font.size)


def memoize(fn):
    fn.cache = {}

    @wraps(fn)
    def func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in fn.cache:
            fn.cache[key] = fn(*args, **kwargs)

        return fn.cache[key]

    return func
