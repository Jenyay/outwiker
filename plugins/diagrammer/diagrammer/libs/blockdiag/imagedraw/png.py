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

from __future__ import division

import math
import re
from functools import partial, wraps
from itertools import tee

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from blockdiag.imagedraw import base
from blockdiag.imagedraw.utils import memoize
from blockdiag.imagedraw.utils.ellipse import dots as ellipse_dots
from blockdiag.utils import XY, Box, Size, images
from blockdiag.utils.fontmap import FontMap, parse_fontpath
from blockdiag.utils.myitertools import istep, stepslice


# to support pillow < 9.1.0
if not hasattr(Image, 'Resampling'):
    from enum import IntEnum

    class Resampling(IntEnum):
        NEAREST = 0
        BOX = 4
        BILINEAR = 2
        HAMMING = 5
        BICUBIC = 3
        LANCZOS = 1

    Image.Resampling = Resampling


def point_pairs(xylist):
    iterable = iter(xylist)
    for pt in iterable:
        if isinstance(pt, int):
            yield (pt, next(iterable))
        else:
            yield pt


def line_segments(xylist):
    p1, p2 = tee(point_pairs(xylist))
    next(p2)
    return zip(p1, p2)


def dashize_line(line, length):
    pt1, pt2 = line
    if pt1[0] == pt2[0]:  # holizonal
        if pt1[1] > pt2[1]:
            pt2, pt1 = line

        r = stepslice(range(round(pt1[1]), round(pt2[1])), length)
        for y1, y2 in istep(n for n in r):
            yield [(pt1[0], y1), (pt1[0], y2)]

    elif pt1[1] == pt2[1]:  # vertical
        if pt1[0] > pt2[0]:
            pt2, pt1 = line

        r = stepslice(range(round(pt1[0]), round(pt2[0])), length)
        for x1, x2 in istep(n for n in r):
            yield [(x1, pt1[1]), (x2, pt1[1])]
    else:  # diagonal
        if pt1[0] > pt2[0]:
            pt2, pt1 = line

        # DDA (Digital Differential Analyzer) Algorithm
        locus = []
        m = float(pt2[1] - pt1[1]) / float(pt2[0] - pt1[0])
        x = pt1[0]
        y = pt1[1]

        while x <= pt2[0]:
            locus.append((int(x), int(round(y))))
            x += 1
            y += m

        for p1, p2 in istep(stepslice(locus, length)):
            yield (p1, p2)


def style2cycle(style, thick):
    if thick is None:
        thick = 1

    if style == 'dotted':
        length = [2 * thick, 2 * thick]
    elif style == 'dashed':
        length = [4 * thick, 4 * thick]
    elif style == 'none':
        length = [0, 65535 * thick]
    elif re.search(r'^\d+(,\d+)*$', style or ""):
        length = [int(n) * thick for n in style.split(',')]
    else:
        length = None

    return length


def ttfont_for(font):
    if font.path:
        path, index = parse_fontpath(font.path)
        if index:
            ttfont = ImageFont.truetype(path, font.size, index=index)
        else:
            ttfont = ImageFont.truetype(path, font.size)
    else:
        ttfont = None

    return ttfont


class ImageDrawExBase(base.ImageDraw):
    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.transparency = kwargs.get('transparency')
        self.bgcolor = kwargs.get('color', (256, 256, 256))
        self._image = None
        self.draw = None

        if kwargs.get('parent'):
            self.scale_ratio = kwargs.get('parent').scale_ratio
        else:
            self.scale_ratio = kwargs.get('scale_ratio', 1)

        self.set_canvas_size(Size(1, 1))  # This line make textsize() workable

    def paste(self, image, pt, mask=None):
        self._image.paste(image, pt, mask)
        self.draw = ImageDraw.Draw(self._image)

    def set_canvas_size(self, size):
        if self.transparency:
            mode = 'RGBA'
        else:
            mode = 'RGB'

        self._image = Image.new(mode, size, self.bgcolor)

        # set transparency to background
        if self.transparency:
            alpha = Image.new('L', size, 1)
            self._image.putalpha(alpha)

        self.draw = ImageDraw.Draw(self._image)

    def resizeCanvas(self, size):
        self._image = self._image.resize(size, Image.Resampling.LANCZOS)
        self.draw = ImageDraw.Draw(self._image)

    def arc(self, box, start, end, **kwargs):
        style = kwargs.get('style')
        if 'style' in kwargs:
            del kwargs['style']
        if 'thick' in kwargs:
            del kwargs['thick']

        if style:
            while start > end:
                end += 360

            cycle = style2cycle(style, kwargs.get('width'))
            for pt in ellipse_dots(box, cycle, start, end):
                self.draw.line([pt, pt], fill=kwargs['fill'])
        else:
            self.draw.arc(box.to_integer_point(), start, end, **kwargs)

    def ellipse(self, box, **kwargs):
        if 'filter' in kwargs:
            del kwargs['filter']

        style = kwargs.get('style')
        if 'style' in kwargs:
            del kwargs['style']

        if style:
            if kwargs.get('fill') != 'none':
                kwargs2 = dict(kwargs)
                if 'outline' in kwargs2:
                    del kwargs2['outline']
                self.draw.ellipse(box, **kwargs2)

            if 'outline' in kwargs:
                kwargs['fill'] = kwargs['outline']
                del kwargs['outline']

            cycle = style2cycle(style, kwargs.get('width'))
            for pt in ellipse_dots(box, cycle):
                self.draw.line([pt, pt], fill=kwargs['fill'])
        else:
            if kwargs.get('fill') == 'none':
                del kwargs['fill']

            self.draw.ellipse(box.to_integer_point(), **kwargs)

    def line(self, xy, **kwargs):
        if 'jump' in kwargs:
            del kwargs['jump']
        if 'thick' in kwargs:
            if kwargs['thick'] is not None:
                kwargs['width'] = kwargs['thick']
            del kwargs['thick']

        style = kwargs.get('style')
        if kwargs.get('fill') == 'none':
            pass
        elif (style in ('dotted', 'dashed', 'none') or
              re.search(r'^\d+(,\d+)*$', style or "")):
            self.dashed_line(xy, **kwargs)
        else:
            if 'style' in kwargs:
                del kwargs['style']

            self.draw.line(xy, **kwargs)

    def dashed_line(self, xy, **kwargs):
        style = kwargs.get('style')
        del kwargs['style']

        cycle = style2cycle(style, kwargs.get('width'))
        for line in line_segments(xy):
            for subline in dashize_line(line, cycle):
                self.line(subline, **kwargs)

    def rectangle(self, box, **kwargs):
        thick = kwargs.get('thick', self.scale_ratio)
        fill = kwargs.get('fill')
        outline = kwargs.get('outline')
        style = kwargs.get('style')

        if thick == 1:
            d = 0
        else:
            d = int(math.ceil(thick / 2.0))

        if fill and fill != 'none':
            self.draw.rectangle(box, fill=fill)

        x1, y1, x2, y2 = box
        lines = (((x1, y1), (x2, y1)), ((x1, y2), (x2, y2)),  # horizonal
                 ((x1, y1 - d), (x1, y2 + d)),  # vettical (left)
                 ((x2, y1 - d), (x2, y2 + d)))  # vertical (right)

        for line in lines:
            self.line(line, fill=outline, width=thick, style=style)

    def polygon(self, xy, **kwargs):
        if 'filter' in kwargs:
            del kwargs['filter']

        if kwargs.get('fill') != 'none':
            kwargs2 = dict(kwargs)

            if 'style' in kwargs2:
                del kwargs2['style']
            if 'outline' in kwargs2:
                del kwargs2['outline']
            self.draw.polygon(xy, **kwargs2)

        if kwargs.get('outline'):
            kwargs['fill'] = kwargs['outline']
            del kwargs['outline']
            self.line(xy, **kwargs)

    @property
    def textfolder(self):
        textfolder = super(ImageDrawExBase, self).textfolder
        return partial(textfolder, scale=self.scale_ratio)

    @memoize
    def textlinesize(self, string, font):
        ttfont = ttfont_for(font)
        if ttfont is None:
            if hasattr(self.draw, 'textbbox'):
                left, top, right, bottom = self.draw.textbbox((0, 0), string)
                size = (right - left, bottom - top)
            else:
                size = self.draw.textsize(string, font=None)

            font_ratio = font.size * 1.0 / FontMap.BASE_FONTSIZE
            size = Size(int(size[0] * font_ratio),
                        int(size[1] * font_ratio))
        else:
            if hasattr(ttfont, 'getbbox'):
                left, top, right, bottom = ttfont.getbbox(string)
                size = Size(right - left, bottom - top)
            else:
                size = Size(*ttfont.getsize(string))

        return size

    def text(self, xy, string, font, **kwargs):
        fill = kwargs.get('fill')
        ttfont = ttfont_for(font)

        if ttfont is None:
            if self.scale_ratio == 1 and font.size == FontMap.BASE_FONTSIZE:
                self.draw.text(xy, string, fill=fill)
            else:
                if hasattr(self.draw, 'textbbox'):
                    left, top, right, bottom = self.draw.textbbox((0, 0), string)
                    size = (right - left, bottom - top)
                else:
                    size = self.draw.textsize(string)
                image = Image.new('RGBA', size)
                draw = ImageDraw.Draw(image)
                draw.text((0, 0), string, fill=fill)
                del draw

                basesize = (size[0] * self.scale_ratio,
                            size[1] * self.scale_ratio)
                text_image = image.resize(basesize, Image.Resampling.LANCZOS)
                self.paste(text_image, xy, text_image)
        else:
            if hasattr(ttfont, 'getbbox'):
                left, top, right, bottom = ttfont.getbbox(string)
                size = (right - left, bottom - top)
            else:
                size = ttfont.getsize(string)

            # Generate mask to support BDF(bitmap font)
            mask = Image.new('1', size)
            draw = ImageDraw.Draw(mask)
            draw.text((0, 0), string, fill='white', font=ttfont)

            # Rendering text
            filler = Image.new('RGB', size, fill)
            self.paste(filler, xy, mask)

    def textarea(self, box, string, font, **kwargs):
        if 'rotate' in kwargs and kwargs['rotate'] != 0:
            angle = 360 - int(kwargs['rotate']) % 360
            del kwargs['rotate']

            if angle in (90, 270):
                _box = Box(0, 0, box.height, box.width)
            else:
                _box = box

            text = ImageDrawEx(None, parent=self, transparency=True)
            text.set_canvas_size(_box.size)
            textbox = Box(0, 0, _box.width, _box.height)
            text.textarea(textbox, string, font, **kwargs)

            filler = Image.new('RGB', box.size, kwargs.get('fill'))

            mask = text._image.rotate(angle, expand=True)
            if mask.size != filler.size:
                # Image.rotate(expand=True) of Pillow earlier than
                # 3.3.0 (including 2.x) returns image object with
                # unexpected size: for example, rotating 10x20 by 270
                # causes not 20x10 but 21x11.
                # Therefore, crop rotated image in order to make it
                # match against size of "filler".
                mask = mask.crop((0, 0, box.width, box.height))

            self.paste(filler, box.topleft, mask)
            return

        lines = self.textfolder(box, string, font, **kwargs)

        if kwargs.get('outline'):
            outline = kwargs.get('outline')
            self.rectangle(lines.outlinebox, fill='white', outline=outline)

        rendered = False
        for string, xy in lines.lines:
            self.text(xy, string, font, **kwargs)
            rendered = True

        if not rendered and font.size > 0:
            _font = font.duplicate()
            _font.size = int(font.size * 0.8)
            self.textarea(box, string, _font, **kwargs)

    def image(self, box, url):
        if not box.width or not box.height:
            # resizing image into "0 width and/or height" is meaningless
            return

        try:
            image = images.open(url, mode='pillow')

            # resize image.
            w = min([box.width, image.size[0] * self.scale_ratio])
            h = min([box.height, image.size[1] * self.scale_ratio])
            image.thumbnail((w, h), Image.Resampling.LANCZOS)

            # centering image.
            w, h = image.size
            if box.width > w:
                x = box[0] + (box.width - w) // 2
            else:
                x = box[0]

            if box.height > h:
                y = box[1] + (box.height - h) // 2
            else:
                y = box[1]

            if image.mode == 'P':
                # convert P to RGBA to masking transparent pixels
                image = image.convert('RGBA')

            if image.mode == 'RGBA':
                self.paste(image, (round(x), round(y)), mask=image)
            else:
                self.paste(image, (round(x), round(y)))
        except IOError:
            pass

    def save(self, filename, size, _format):
        if filename:
            self.filename = filename

        if size is None:
            x = int(self._image.size[0] / self.scale_ratio)
            y = int(self._image.size[1] / self.scale_ratio)
            size = (x, y)

        self._image.thumbnail(size, Image.Resampling.LANCZOS)

        if self.filename:
            self._image.save(self.filename, _format)
            image = None
        else:
            from io import BytesIO
            tmp = BytesIO()
            self._image.save(tmp, _format)
            image = tmp.getvalue()

        return image


def blurred(fn):
    PADDING = 16

    def get_shape_box(*args):
        if fn.__name__ == 'polygon':
            xlist = [pt.x for pt in args[0]]
            ylist = [pt.y for pt in args[0]]
            return Box(min(xlist), min(ylist), max(xlist), max(ylist))
        else:
            return args[0]

    def get_abs_coordinate(box, *args):
        dx = box.x1 - PADDING
        dy = box.y1 - PADDING
        if fn.__name__ == 'polygon':
            return [pt.shift(-dx, -dy) for pt in args[0]]
        else:
            return box.shift(-dx, -dy)

    def create_shadow(self, size, *args, **kwargs):
        drawer = ImageDrawExBase(self.filename, transparency=True)
        drawer.set_canvas_size(size)
        getattr(drawer, fn.__name__)(*args, **kwargs)

        for _ in range(15):
            drawer._image = drawer._image.filter(ImageFilter.SMOOTH_MORE)

        return drawer._image

    @wraps(fn)
    def func(self, *args, **kwargs):
        args = list(args)

        if kwargs.get('filter') not in ('blur', 'transp-blur'):
            return fn(self, *args, **kwargs)
        else:
            box = get_shape_box(*args)
            args[0] = get_abs_coordinate(box, *args)

            size = Size(box.width + PADDING * 2, box.height + PADDING * 2)
            shadow = create_shadow(self, size, *args, **kwargs)
            xy = XY(box.x1 - PADDING, box.y1 - PADDING)
            self.paste(shadow, xy, shadow)

    return func


class ImageDrawEx(ImageDrawExBase):
    @blurred
    def ellipse(self, box, **kwargs):
        super(ImageDrawEx, self).ellipse(box, **kwargs)

    @blurred
    def rectangle(self, box, **kwargs):
        super(ImageDrawEx, self).rectangle(box, **kwargs)

    @blurred
    def polygon(self, xy, **kwargs):
        super(ImageDrawEx, self).polygon(xy, **kwargs)


def setup(self):
    from blockdiag.imagedraw import install_imagedrawer
    install_imagedrawer('png', ImageDrawEx)
