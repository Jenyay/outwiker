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
from io import StringIO


def _escape(s):
    if not isinstance(s, str):
        s = str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _quote(s):
    return '"%s"' % _escape(s).replace('"', "&quot;")


class base(object):
    def __init__(self, *args, **kwargs):
        self.text = None
        self.elements = []
        self.attributes = {}
        for key, value in kwargs.items():
            self.add_attribute(key, value)

    def add_attribute(self, key, value):
        setter = 'set_%s' % key
        if hasattr(self, setter):
            getattr(self, setter)(value)
        else:
            key = re.sub('_', '-', key)
            self.attributes[key] = value

    def addElement(self, element):
        self.elements.append(element)

    def set_text(self, text):
        self.text = text

    def to_xml(self, io, level=0):
        clsname = self.__class__.__name__
        indent = '  ' * level

        io.write('%s<%s' % (indent, clsname))
        for key in sorted(self.attributes):
            value = self.attributes[key]
            if value is not None:
                io.write(' %s=%s' % (_escape(key), _quote(value)))

        if self.elements == []:
            if self.text is not None:
                io.write(">%s</%s>\n" % (_escape(self.text), clsname))
            else:
                io.write(" />\n")
        elif self.elements:
            if self.text is not None:
                io.write(">%s\n" % (_escape(self.text),))
            else:
                io.write(">\n")

            for e in self.elements:
                e.to_xml(io, level + 1)
            io.write('%s</%s>\n' % (indent, clsname))


class element(base):
    def __init__(self, x, y, width=None, height=None, *args, **kwargs):
        super(element, self).__init__(*args, **kwargs)
        self.attributes['x'] = x
        self.attributes['y'] = y
        if width is not None:
            self.attributes['width'] = width
        if height is not None:
            self.attributes['height'] = height


class svg(base):
    def __init__(self, x, y, width, height, **kwargs):
        if kwargs.get('noviewbox'):
            super(svg, self).__init__(width=(width - x), height=(height - y))
        else:
            viewbox = "%d %d %d %d" % (x, y, width, height)
            super(svg, self).__init__(viewBox=viewbox)

        self.nodoctype = kwargs.get('nodoctype', False)
        self.add_attribute('xmlns', 'http://www.w3.org/2000/svg')

    def to_xml(self):
        io = StringIO()

        if not self.nodoctype:
            url = "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"
            io.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            io.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "%s">\n' % url)

        super(svg, self).to_xml(io)

        return io.getvalue()


class title(base):
    def __init__(self, _title):
        super(title, self).__init__(text=_title)


class desc(base):
    def __init__(self, _title):
        super(desc, self).__init__(text=_title)


class text(element):
    def __init__(self, x, y, _text, **kwargs):
        super(text, self).__init__(x, y, text=_text, **kwargs)


class rect(element):
    pass


class ellipse(base):
    def __init__(self, cx, cy, rx, ry, **kwargs):
        super(ellipse, self).__init__(cx=cx, cy=cy, rx=rx, ry=ry, **kwargs)


class image(element):
    def __init__(self, uri, x, y, width, height, **kwargs):
        super(image, self).__init__(x, y, width, height, **kwargs)
        self.add_attribute('xlink:href', uri)


class polygon(base):
    def __init__(self, points, **kwargs):
        xylist = " ".join('%d,%d' % pt for pt in points)
        super(polygon, self).__init__(points=xylist, **kwargs)


class path(base):
    def __init__(self, data, **kwargs):
        super(path, self).__init__(d=data, **kwargs)


class pathdata:
    def __init__(self, x=None, y=None):
        self.path = []
        if x is not None and y is not None:
            self.move(x, y)

    def closepath(self):
        self.path.append('z')

    def move(self, x, y):
        self.path.append('M %s %s' % (x, y))

    def relmove(self, x, y):
        self.path.append('m %s %s' % (x, y))

    def line(self, x, y):
        self.path.append('L %s %s' % (x, y))

    def relline(self, x, y):
        self.path.append('l %s %s' % (x, y))

    def hline(self, x):
        self.path.append('H%s' % (x,))

    def relhline(self, x):
        self.path.append('h%s' % (x,))

    def vline(self, y):
        self.path.append('V%s' % (y,))

    def relvline(self, y):
        self.path.append('v%s' % (y,))

    def bezier(self, x1, y1, x2, y2, x, y):
        self.path.append('C%s,%s %s,%s %s,%s' % (x1, y1, x2, y2, x, y))

    def relbezier(self, x1, y1, x2, y2, x, y):
        self.path.append('c%s,%s %s,%s %s,%s' % (x1, y1, x2, y2, x, y))

    def smbezier(self, x2, y2, x, y):
        self.path.append('S%s,%s %s,%s' % (x2, y2, x, y))

    def relsmbezier(self, x2, y2, x, y):
        self.path.append('s%s,%s %s,%s' % (x2, y2, x, y))

    def qbezier(self, x1, y1, x, y):
        self.path.append('Q%s,%s %s,%s' % (x1, y1, x, y))

    def qrelbezier(self, x1, y1, x, y):
        self.path.append('q%s,%s %s,%s' % (x1, y1, x, y))

    def smqbezier(self, x, y):
        self.path.append('T%s %s' % (x, y))

    def relsmqbezier(self, x, y):
        self.path.append('t%s %s' % (x, y))

    def ellarc(self, rx, ry, xrot, laf, sf, x, y):
        self.path.append('A%s,%s %s %s %s %s %s' %
                         (rx, ry, xrot, laf, sf, x, y))

    def relellarc(self, rx, ry, xrot, laf, sf, x, y):
        self.path.append('a%s,%s %s %s %s %s %s' %
                         (rx, ry, xrot, laf, sf, x, y))

    def __repr__(self):
        return ' '.join(self.path)


class defs(base):
    pass


class g(base):
    pass


class a(base):
    pass


class filter(element):
    def __init__(self, x, y, width, height, **kwargs):
        super(filter, self).__init__(x, y, width, height, **kwargs)


def svgclass(name):
    """ svg class generating function """
    return type(name, (base,), {})
