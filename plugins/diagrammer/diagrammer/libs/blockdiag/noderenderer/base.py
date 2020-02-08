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

from blockdiag.utils import XY, Box, images


class NodeShape(object):
    def __init__(self, node, metrics):
        self.node = node
        self.metrics = metrics

        m = self.metrics.cell(self.node)
        self.textalign = 'center'
        self.connectors = [m.top, m.right, m.bottom, m.left]

        if node.icon is None:
            self.iconbox = None
            self.textbox = m.box
        else:
            image_size = images.get_image_size(node.icon)
            if image_size is None:
                iconsize = (0, 0)
            else:
                boundedbox = [metrics.node_width // 2, metrics.node_height]
                iconsize = images.calc_image_size(image_size, boundedbox)

            vmargin = (metrics.node_height - iconsize[1]) // 2
            self.iconbox = Box(m.topleft.x,
                               m.topleft.y + vmargin,
                               m.topleft.x + iconsize[0],
                               m.topleft.y + vmargin + iconsize[1])

            self.textbox = Box(self.iconbox[2], m.top.y,
                               m.bottomright.x, m.bottomright.y)

    def render(self, drawer, _format, **kwargs):
        if self.node.stacked and not kwargs.get('stacked'):
            node = self.node.duplicate()
            node.label = ""
            node.background = ""
            for i in range(2, 0, -1):
                # use original_metrics FORCE
                r = self.metrics.original_metrics.cellsize // 2 * i
                metrics = self.metrics.shift(r, r)

                self.__class__(node, metrics).render(drawer, _format,
                                                     stacked=True, **kwargs)

        if hasattr(self, 'render_vector_shape') and _format == 'SVG':
            self.render_vector_shape(drawer, _format, **kwargs)
        else:
            self.render_shape(drawer, _format, **kwargs)

        self.render_icon(drawer, **kwargs)
        self.render_label(drawer, **kwargs)
        self.render_number_badge(drawer, **kwargs)

    def render_icon(self, drawer, **kwargs):
        if self.node.icon is not None and kwargs.get('shadow') is not True:
            drawer.image(self.iconbox, self.node.icon)

    def render_shape(self, drawer, _, **kwargs):
        pass

    def render_label(self, drawer, **kwargs):
        if not kwargs.get('shadow'):
            font = self.metrics.font_for(self.node)
            drawer.textarea(self.textbox, self.node.label, font,
                            rotate=self.node.rotate,
                            fill=self.node.textcolor, halign=self.textalign,
                            line_spacing=self.metrics.line_spacing,
                            orientation=self.node.label_orientation)

    def render_number_badge(self, drawer, **kwargs):
        if self.node.numbered is not None and kwargs.get('shadow') is None:
            badgeFill = kwargs.get('badgeFill')

            xy = self.metrics.cell(self.node).topleft
            r = self.metrics.cellsize * 3 // 2

            box = Box(xy.x - r, xy.y - r, xy.x + r, xy.y + r)
            font = self.metrics.font_for(self.node)
            drawer.ellipse(box, outline=self.node.linecolor, fill=badgeFill)
            drawer.textarea(box, self.node.numbered, font,
                            rotate=self.node.rotate,
                            fill=self.node.textcolor)

    @property
    def top(self):
        return self.connectors[0]

    @property
    def left(self):
        return self.connectors[3]

    @property
    def right(self):
        point = self.connectors[1]
        if self.node.stacked:
            point = XY(point.x + self.metrics.cellsize, point.y)
        return point

    @property
    def bottom(self):
        point = self.connectors[2]
        if self.node.stacked:
            point = XY(point.x, point.y + self.metrics.cellsize)
        return point

    def shift_shadow(self, value):
        xdiff = self.metrics.shadow_offset.x
        ydiff = self.metrics.shadow_offset.y

        if isinstance(value, XY):
            ret = XY(value.x + xdiff, value.y + ydiff)
        elif isinstance(value, Box):
            ret = Box(value.x1 + xdiff, value.y1 + ydiff,
                      value.x2 + xdiff, value.y2 + ydiff)
        elif isinstance(value, (list, tuple)):
            ret = [self.shift_shadow(x) for x in value]

        return ret
