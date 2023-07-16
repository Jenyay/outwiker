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

import os
import re
from base64 import b64encode

from PIL.Image import Image

from blockdiag.imagedraw import base as _base
from blockdiag.imagedraw.simplesvg import (a, defs, desc, ellipse, filter, g,
                                           image, path, pathdata, polygon,
                                           rect, svg, svgclass, text, title)
from blockdiag.imagedraw.utils import memoize
from blockdiag.imagedraw.utils.ellipse import endpoints as ellipse_endpoints
from blockdiag.utils import XY, Box, images, is_Pillow_available

feGaussianBlur = svgclass('feGaussianBlur')


def rgb(color):
    if isinstance(color, tuple):
        color = 'rgb(%d,%d,%d)' % color

    return color


def style(name):
    if name == 'blur':
        value = "filter:url(#filter_blur)"
    elif name == 'transp-blur':
        value = "filter:url(#filter_blur);opacity:0.7;fill-opacity:1"
    else:
        value = None

    return value


def dasharray(pattern, thick):
    if thick is None:
        thick = 1

    if pattern == 'dotted':
        value = 2 * thick
    elif pattern == 'dashed':
        value = 4 * thick
    elif pattern == 'none':
        value = "%d %d" % (0, 65535 * thick)
    elif re.search(r'^\d+(,\d+)*$', pattern or ""):
        lengths = [int(n) * thick for n in pattern.split(",")]
        value = " ".join(str(n) for n in lengths)
    else:
        value = None

    return value


def drawing_params(kwargs):
    params = {}

    if 'style' in kwargs:
        params['stroke_dasharray'] = dasharray(kwargs.get('style'),
                                               kwargs.get('thick'))

    if 'filter' in kwargs:
        params['style'] = style(kwargs.get('filter'))

    return params


class SVGImageDrawElement(_base.ImageDraw):
    self_generative_methods = ['group', 'anchor']
    supported_path = True
    baseline_text_rendering = True

    def __init__(self, svg, parent=None):
        self.svg = svg

    def path(self, pd, **kwargs):
        fill = kwargs.get('fill')
        outline = kwargs.get('outline')

        p = path(pd, fill=rgb(fill), stroke=rgb(outline),
                 **drawing_params(kwargs))
        self.svg.addElement(p)

    def rectangle(self, box, **kwargs):
        thick = kwargs.get('thick')
        fill = kwargs.get('fill', 'none')
        outline = kwargs.get('outline')

        r = rect(box.x, box.y, box.width, box.height,
                 fill=rgb(fill), stroke=rgb(outline),
                 stroke_width=thick, **drawing_params(kwargs))
        self.svg.addElement(r)

    @memoize
    def textlinesize(self, string, font, **kwargs):
        if is_Pillow_available():
            if not hasattr(self, '_pil_drawer'):
                from blockdiag.imagedraw import png
                self._pil_drawer = png.ImageDrawEx(None)

            return self._pil_drawer.textlinesize(string, font)
        else:
            from blockdiag.imagedraw.utils import textsize
            return textsize(string, font)

    def text(self, point, string, font, **kwargs):
        fill = kwargs.get('fill')

        size = self.textlinesize(string, font)
        point = point.shift(size.width / 2)
        t = text(point.x, point.y, string, fill=rgb(fill),
                 font_family=font.generic_family, font_size=font.size,
                 font_weight=font.weight, font_style=font.style,
                 text_anchor='middle', textLength=size.width)
        self.svg.addElement(t)

    def textarea(self, box, string, font, **kwargs):
        if 'rotate' in kwargs and kwargs['rotate'] != 0:
            self.rotated_textarea(box, string, font, **kwargs)
        else:
            lines = self.textfolder(box, string, font, **kwargs)

            if kwargs.get('outline'):
                outline = kwargs.get('outline')
                self.rectangle(lines.outlinebox, fill='white', outline=outline)

            rendered = False
            for string, point in lines.lines:
                self.text(point, string, font, **kwargs)
                rendered = True

            if not rendered and font.size > 0:
                _font = font.duplicate()
                _font.size = int(font.size * 0.8)
                self.textarea(box, string, _font, **kwargs)

    def rotated_textarea(self, box, string, font, **kwargs):
        angle = int(kwargs['rotate']) % 360
        del kwargs['rotate']

        if angle in (90, 270):
            _box = Box(box[0], box[1],
                       box[0] + box.height, box[1] + box.width)
            if angle == 90:
                _box = _box.shift(x=box.width)
            elif angle == 270:
                _box = _box.shift(y=box.height)
        elif angle == 180:
            _box = Box(box[2], box[3],
                       box[2] + box.width, box[3] + box.height)
        else:
            _box = Box(box[0], box[1],
                       box[0] + box.width, box[1] + box.height)

        rotate = "rotate(%d,%d,%d)" % (angle, _box[0], _box[1])
        group = g(transform="%s" % rotate)
        self.svg.addElement(group)

        elem = SVGImageDrawElement(group, self)
        elem.textarea(_box, string, font, **kwargs)

    def line(self, points, **kwargs):
        fill = kwargs.get('fill')
        thick = kwargs.get('thick')

        pd = pathdata(points[0].x, points[0].y)
        for pt in points[1:]:
            pd.line(pt.x, pt.y)

        p = path(pd, fill="none", stroke=rgb(fill),
                 stroke_width=thick, **drawing_params(kwargs))
        self.svg.addElement(p)

    def arc(self, box, start, end, **kwargs):
        fill = kwargs.get('fill')

        w = box.width / 2
        h = box.height / 2

        if start > end:
            end += 360

        endpoints = ellipse_endpoints(1, w, h, start, end)
        pt1 = XY(box.x + w + round(endpoints[0].x, 0),
                 box.y + h + round(endpoints[0].y, 0))
        pt2 = XY(box.x + w + round(endpoints[1].x, 0),
                 box.y + h + round(endpoints[1].y, 0))

        if end - start > 180:
            largearc = 1
        else:
            largearc = 0

        pd = pathdata(pt1[0], pt1[1])
        pd.ellarc(w, h, 0, largearc, 1, pt2[0], pt2[1])
        p = path(pd, fill="none", stroke=rgb(fill),
                 **drawing_params(kwargs))
        self.svg.addElement(p)

    def ellipse(self, box, **kwargs):
        fill = kwargs.get('fill')
        outline = kwargs.get('outline')

        w = box.width / 2
        h = box.height / 2
        pt = box.center

        e = ellipse(pt.x, pt.y, w, h, fill=rgb(fill),
                    stroke=rgb(outline), **drawing_params(kwargs))
        self.svg.addElement(e)

    def polygon(self, points, **kwargs):
        fill = kwargs.get('fill')
        outline = kwargs.get('outline')

        pg = polygon(points, fill=rgb(fill), stroke=rgb(outline),
                     **drawing_params(kwargs))
        self.svg.addElement(pg)

    def image(self, box, url):
        if hasattr(url, 'read'):
            url = "data:;base64," + str(b64encode(url.read()))
        else:
            if isinstance(url, Image):
                ext = None
            else:
                ext = os.path.splitext(url)[1].lower()

            if ext not in ('.jpg', '.png', '.gif'):
                stream = None
                try:
                    stream = images.open(url, mode='png')
                    url = "data:;base64," + str(b64encode(stream.read()))
                except IOError:
                    url = None
                finally:
                    if stream:
                        stream.close()

        im = image(url, box.x1, box.y1, box.width, box.height)
        self.svg.addElement(im)

    def anchor(self, url):
        a_node = a(url)
        a_node.add_attribute('xlink:href', url)
        self.svg.addElement(a_node)

        return SVGImageDrawElement(a_node, self)

    def group(self):
        group = g()
        self.svg.addElement(group)

        return SVGImageDrawElement(group, self)


class SVGImageDraw(SVGImageDrawElement):
    def __init__(self, filename, **kwargs):
        super(SVGImageDraw, self).__init__(None)

        self.filename = filename
        self.options = kwargs
        self.set_canvas_size((0, 0))

    def set_canvas_size(self, size):
        self.svg = svg(0, 0, size[0], size[1], **self.options)
        uri = 'http://www.inkscape.org/namespaces/inkscape'
        self.svg.add_attribute('xmlns:inkspace', uri)
        uri = 'http://www.w3.org/1999/xlink'
        self.svg.add_attribute('xmlns:xlink', uri)

        # inkspace's Gaussian filter
        if self.options.get('style') != 'blur':
            fgb = feGaussianBlur(id='feGaussianBlur3780', stdDeviation=4.2)
            fgb.add_attribute('inkspace:collect', 'always')
            f = filter(-0.07875, -0.252, 1.1575, 1.504, id='filter_blur')
            f.add_attribute('inkspace:collect', 'always')
            f.addElement(fgb)
            d = defs(id='defs_block')
            d.addElement(f)
            self.svg.addElement(d)

        self.svg.addElement(title('blockdiag'))
        self.svg.addElement(desc(self.options.get('code')))

    def save(self, filename, size, _format):
        # Ignore format parameter; compatibility for ImageDrawEx.

        if filename:
            self.filename = filename

        if size:
            self.svg.attributes['width'] = size[0]
            self.svg.attributes['height'] = size[1]

        image = self.svg.to_xml()

        if self.filename:
            open(self.filename, 'wb').write(image.encode('utf-8'))

        return image


def setup(self):
    from blockdiag.imagedraw import install_imagedrawer
    install_imagedrawer('svg', SVGImageDraw)
