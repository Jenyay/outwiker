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

import copy
import os
import re
from collections import namedtuple

from blockdiag.utils.config import ConfigParser
from blockdiag.utils.logging import warning


def parse_fontpath(path):
    if path is None:
        return (None, None)

    match = re.search(r'^(.*):(\d)$', path)
    if match:
        return (match.group(1), int(match.group(2)))
    else:
        return (path, None)


class FontInfo(object):
    def __init__(self, family, path, size):
        self.path = path
        self.size = int(size)

        family = self._parse(family)
        self.name = family[0]
        self.generic_family = family[1]
        self.weight = family[2]
        self.style = family[3]

    def __repr__(self):
        return ("<FontInfo familyname=%r size=%r>" %
                (self.familyname, self.size))

    @property
    def familyname(self):
        if self.name:
            name = self.name + "-"
        else:
            name = ''

        if self.generic_family == 'sans-serif':
            generic_family = 'sansserif'
        else:
            generic_family = self.generic_family

        if self.weight == 'bold':
            return "%s%s-%s" % (name, generic_family, self.weight)
        else:
            return "%s%s-%s" % (name, generic_family, self.style)

    def _parse(self, familyname):
        pattern = '^(?:(.*)-)?' + \
                  '(serif|sansserif|monospace|fantasy|cursive)' + \
                  '(?:-(normal|bold|italic|oblique))?$'

        match = re.search(pattern, familyname or '')
        if match is None:
            msg = 'Unknown font family: %s' % familyname
            raise AttributeError(msg)

        name = match.group(1) or ''
        generic_family = match.group(2)
        style = match.group(3) or ''

        if generic_family == 'sansserif':
            generic_family = 'sans-serif'

        if style == 'bold':
            weight = 'bold'
            style = 'normal'
        elif style in ('italic', 'oblique'):
            weight = 'normal'
            style = style
        else:
            weight = 'normal'
            style = 'normal'

        return [name, generic_family, weight, style]

    def duplicate(self):
        return copy.copy(self)


class FontMap(object):
    BASE_FONTSIZE = 11
    fontsize = BASE_FONTSIZE
    default_fontfamily = 'sansserif'

    def __init__(self, filename=None):
        self.fonts = {}
        self.aliases = {}

        if filename:
            self._parse_config(filename)
        self.set_default_font(None)

    def set_default_fontfamily(self, fontfamily):
        self.default_fontfamily = fontfamily
        self.set_default_font(None)

    def _parse_config(self, conffile):
        config = ConfigParser()

        if hasattr(conffile, 'read'):
            config.read_file(conffile)
        elif os.path.isfile(conffile):
            config.read(conffile)
        else:
            msg = "fontmap file is not found: %s" % conffile
            raise RuntimeError(msg)

        if config.has_section('fontmap'):
            for name, path in config.items('fontmap'):
                self.append_font(name, path)

        if config.has_section('fontalias'):
            for name, family in config.items('fontalias'):
                self.aliases[name] = family

    def set_default_font(self, path):
        if path is None and self.find() is not None:
            return

        self.append_font(self.default_fontfamily, path)

    def append_font(self, fontfamily, path):
        _path, _ = parse_fontpath(path)
        if path is None or os.path.isfile(_path):
            font = FontInfo(fontfamily, path, self.fontsize)
            self.fonts[font.familyname] = font
        else:
            warning('fontfile `%s` is not found: %s', fontfamily, path)

    def _regulate_familyname(self, name):
        return FontInfo(name, None, self.BASE_FONTSIZE).familyname.lower()

    def find(self, element=None):
        fontfamily = getattr(element, 'fontfamily', None) or \
            self.default_fontfamily
        fontfamily = self.aliases.get(fontfamily, fontfamily)
        fontsize = getattr(element, 'fontsize', None) or self.fontsize

        name = self._regulate_familyname(fontfamily)
        if name in self.fonts:
            font = self.fonts[name].duplicate()
            font.size = fontsize
        elif element is not None:
            warning("Unknown fontfamily: %s", fontfamily)
            elem = namedtuple('Font', 'fontsize')(fontsize)
            font = self.find(elem)
        else:
            font = None

        return font
