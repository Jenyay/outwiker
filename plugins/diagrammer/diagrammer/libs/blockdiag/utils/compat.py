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

import sys
import codecs

if sys.version_info[0] == 2:
    string_types = (str, unicode)  # NOQA: pyflakes complains to unicode in py3
    from urllib import urlopen  # NOQA: exporting for common interface
else:
    string_types = (str,)
    from urllib.request import urlopen  # NOQA: exporting for common interface


def u(string):
    if sys.version_info[0] == 2:
        return unicode(string, "unicode_escape")  # NOQA: pyflakes complains to unicode in py3
    else:
        return string


# replace codecs.getreader
if sys.version_info[0] == 3:
    getreader = codecs.getreader

    def py3_getreader(encoding):
        return lambda stream, *args: getreader(encoding)(stream.buffer, *args)

    codecs.getreader = py3_getreader


def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K(object):
        __slots__ = ['obj']

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

        def __hash__(self):
            raise TypeError('hash not implemented')

    return K
