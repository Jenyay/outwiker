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

import re

from blockdiag.utils import XY, Box, Size


def splitlabel(string):
    """Split text to lines as generator.
       Every line will be stripped.
       If text includes characters "\n", treat as line separator.
    """
    string = re.sub(r'^\s*', '', string)
    string = re.sub(r'\s*$', '', string)
    string = re.sub(r'\xa5', '\\\\', string)
    string = re.sub('(\\\\){2}', '\x00', string)
    string = re.sub('\\\\n', '\n', string)
    for line in string.splitlines():
        yield re.sub('\x00', '\\\\', line).strip()


def splittext(metrics, text, bound, measure='width'):
    folded = []
    if text == '':
        folded.append(' ')

    for i in range(len(text), 0, -1):
        textsize = metrics.textsize(text[0:i])

        if getattr(textsize, measure) <= bound:
            folded.append(text[0:i])
            if text[i:]:
                folded += splittext(metrics, text[i:], bound, measure)
            break

    return folded


def truncate_text(metrics, text, bound, measure='width'):
    for i in range(len(text), 0, -1):
        textsize = metrics.textsize(text[0:i] + ' ...')

        if getattr(textsize, measure) <= bound:
            return text[0:i] + ' ...'

    return text


def get(*args, **kwargs):
    if kwargs.get('orientation') == 'vertical':
        return VerticalTextFolder(*args, **kwargs)
    else:
        return HorizontalTextFolder(*args, **kwargs)


class VerticalTextFolder(object):
    def __init__(self, drawer, box, string, font, **kwargs):
        self.drawer = drawer
        self.box = box
        self.string = string
        self.font = font
        self.scale = 1
        self.halign = kwargs.get('halign', 'center')
        self.valign = kwargs.get('valign', 'center')
        self.padding = kwargs.get('padding', 8)
        self.line_spacing = kwargs.get('line_spacing', 2)

        if kwargs.get('adjustBaseline'):
            self.adjustBaseline = True
        else:
            self.adjustBaseline = False

        self._result = self._lines()

    def textsize(self, text, scaled=False):
        if isinstance(text, str):
            size = [self.drawer.textlinesize(c, self.font) for c in text]
            width = max(s.width for s in size)
            height = (sum(s.height for s in size) +
                      self.line_spacing * (len(text) - 1))

            textsize = Size(width, height)
        else:
            if text:
                size = [self.textsize(s) for s in text]
                height = max(s.height for s in size)
                width = (sum(s.width for s in size) +
                         self.line_spacing * (len(text) - 1))

                textsize = Size(width, height)
            else:
                textsize = Size(0, 0)

        if scaled:
            textsize = Size(textsize.width * self.scale,
                            textsize.height * self.scale)

        return textsize

    @property
    def lines(self):
        textsize = self.textsize(self._result, scaled=True)

        dx, _ = self.box.get_padding_for(textsize, halign=self.halign,
                                         padding=self.padding)

        width = self.box.width - dx + self.line_spacing
        base_xy = XY(self.box.x1, self.box.y1)
        for string in self._result:
            textsize = self.textsize(string, scaled=True)
            _, dy = self.box.get_padding_for(textsize, valign=self.valign,
                                             padding=self.line_spacing)

            height = dy
            width -= textsize.width + self.line_spacing
            for char in string:
                charsize = self.textsize(char, scaled=True)

                if self.adjustBaseline:
                    draw_xy = base_xy.shift(width, height + charsize.height)
                else:
                    draw_xy = base_xy.shift(width, height)

                yield char, draw_xy

                height += charsize.height + self.line_spacing

    @property
    def outlinebox(self):
        corners = []
        for string, xy in self.lines:
            textsize = self.textsize(string)
            width = textsize[0] * self.scale
            height = textsize[1] * self.scale

            if self.adjustBaseline:
                xy = XY(xy.x, xy.y - textsize[1])

            corners.append(xy)
            corners.append(XY(xy.x + width, xy.y + height))

        if corners:
            box = Box(min(p.x for p in corners) - self.padding,
                      min(p.y for p in corners) - self.line_spacing,
                      max(p.x for p in corners) + self.padding,
                      max(p.y for p in corners) + self.line_spacing)
        else:
            box = Box(self.box[0], self.box[1], self.box[0], self.box[1])

        return box

    def _lines(self):
        lines = []
        measure = 'height'
        maxwidth, maxheight = self.box.size

        width = 0
        finished = False
        for line in splitlabel(self.string):
            for folded in splittext(self, line, maxheight, measure):
                textsize = self.textsize(folded)

                if width + textsize.width + self.line_spacing < maxwidth:
                    lines.append(folded)
                    width += textsize.width + self.line_spacing
                elif len(lines) > 0:
                    lines[-1] = truncate_text(self, lines[-1],
                                              maxheight, measure)
                    finished = True
                    break

            if finished:
                break

        return lines


class HorizontalTextFolder(object):
    def __init__(self, drawer, box, string, font, **kwargs):
        self.drawer = drawer
        self.box = box
        self.string = string
        self.font = font
        self.scale = 1
        self.halign = kwargs.get('halign', 'center')
        self.valign = kwargs.get('valign', 'center')
        self.padding = kwargs.get('padding', 8)
        self.line_spacing = kwargs.get('line_spacing', 2)

        if kwargs.get('adjustBaseline'):
            self.adjustBaseline = True
        else:
            self.adjustBaseline = False

        self._result = self._lines()

    def textsize(self, text, scaled=False):
        if isinstance(text, str):
            textsize = self.drawer.textlinesize(text, self.font)
        else:
            if text:
                size = [self.textsize(s) for s in text]
                width = max(s.width for s in size)
                height = (sum(s.height for s in size) +
                          self.line_spacing * (len(text) - 1))

                textsize = Size(width, height)
            else:
                textsize = Size(0, 0)

        if scaled:
            textsize = Size(textsize.width * self.scale,
                            textsize.height * self.scale)

        return textsize

    @property
    def lines(self):
        textsize = self.textsize(self._result, scaled=True)

        _, dy = self.box.get_padding_for(textsize, valign=self.valign,
                                         padding=self.line_spacing)

        height = dy
        base_xy = XY(self.box.x1, self.box.y1)
        for string in self._result:
            textsize = self.textsize(string, scaled=True)
            dx, _ = self.box.get_padding_for(textsize, halign=self.halign,
                                             padding=self.padding)

            if self.adjustBaseline:
                draw_xy = base_xy.shift(dx, height + textsize.height)
            else:
                draw_xy = base_xy.shift(dx, height)

            yield string, draw_xy

            height += textsize.height + self.line_spacing

    @property
    def outlinebox(self):
        corners = []
        for string, xy in self.lines:
            textsize = self.textsize(string)
            width = textsize[0] * self.scale
            height = textsize[1] * self.scale

            if self.adjustBaseline:
                xy = XY(xy.x, xy.y - textsize[1])

            corners.append(xy)
            corners.append(XY(xy.x + width, xy.y + height))

        if corners:
            box = Box(min(p.x for p in corners) - self.padding,
                      min(p.y for p in corners) - self.line_spacing,
                      max(p.x for p in corners) + self.padding,
                      max(p.y for p in corners) + self.line_spacing)
        else:
            box = Box(self.box[0], self.box[1], self.box[0], self.box[1])

        return box

    def _lines(self):
        lines = []
        measure = 'width'
        maxwidth, maxheight = self.box.size

        height = 0
        finished = False
        for line in splitlabel(self.string):
            for folded in splittext(self, line, maxwidth, measure):
                textsize = self.textsize(folded)

                if height + textsize.height + self.line_spacing < maxheight:
                    lines.append(folded)
                    height += textsize.height + self.line_spacing
                else:
                    if len(lines) > 0:
                        lines[-1] = truncate_text(self, lines[-1],
                                                  maxwidth, measure)

                    finished = True
                    break

            if finished:
                break

        return lines
