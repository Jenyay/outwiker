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

from blockdiag.imagedraw.simplesvg import pathdata
from blockdiag.noderenderer import install_renderer
from blockdiag.noderenderer.base import NodeShape
from blockdiag.utils import Box


class Cloud(NodeShape):
    def __init__(self, node, metrics=None):
        super(Cloud, self).__init__(node, metrics)

        pt = metrics.cell(node).topleft
        rx = (self.node.width or self.metrics.node_width) // 12
        ry = (self.node.height or self.metrics.node_height) // 5
        self.textbox = Box(pt.x + rx * 2, pt.y + ry,
                           pt.x + rx * 11, pt.y + ry * 4)

    def render_shape(self, drawer, _, **kwargs):
        # draw background
        self.render_shape_background(drawer, **kwargs)

        if not kwargs.get('shadow') and self.node.background:
            drawer.image(self.textbox, self.node.background)

    def render_shape_background(self, drawer, **kwargs):
        fill = kwargs.get('fill')

        m = self.metrics.cell(self.node)
        pt = m.topleft
        rx = (self.node.width or self.metrics.node_width) // 12
        ry = (self.node.height or self.metrics.node_height) // 5

        ellipses = [Box(pt.x + rx * 2, pt.y + ry,
                        pt.x + rx * 5, pt.y + ry * 3),
                    Box(pt.x + rx * 4, pt.y,
                        pt.x + rx * 9, pt.y + ry * 2),
                    Box(pt.x + rx * 8, pt.y + ry,
                        pt.x + rx * 11, pt.y + ry * 3),
                    Box(pt.x + rx * 9, pt.y + ry * 2,
                        pt.x + rx * 13, pt.y + ry * 4),
                    Box(pt.x + rx * 8, pt.y + ry * 2,
                        pt.x + rx * 11, pt.y + ry * 5),
                    Box(pt.x + rx * 5, pt.y + ry * 2,
                        pt.x + rx * 8, pt.y + ry * 5),
                    Box(pt.x + rx * 2, pt.y + ry * 2,
                        pt.x + rx * 5, pt.y + ry * 5),
                    Box(pt.x + rx * 0, pt.y + ry * 2,
                        pt.x + rx * 4, pt.y + ry * 4)]

        for e in ellipses:
            if kwargs.get('shadow'):
                e = self.shift_shadow(e)
                if kwargs.get('style') == 'blur':
                    drawer.ellipse(e, fill=fill, outline=fill,
                                   filter='transp-blur')
                else:
                    drawer.ellipse(e, fill=fill, outline=fill)
            else:
                drawer.ellipse(e, fill=self.node.color,
                               outline=self.node.linecolor,
                               style=self.node.style)

        rects = [Box(pt.x + rx * 2, pt.y + ry * 2,
                     pt.x + rx * 11, pt.y + ry * 4),
                 Box(pt.x + rx * 4, pt.y + ry,
                     pt.x + rx * 9, pt.y + ry * 2)]
        for rect in rects:
            if kwargs.get('shadow'):
                rect = self.shift_shadow(rect)
                if kwargs.get('style') == 'blur':
                    drawer.rectangle(rect, fill=fill, outline=fill,
                                     filter='transp-blur')
                else:
                    drawer.rectangle(rect, fill=fill, outline=fill)
            else:
                drawer.rectangle(rect, fill=self.node.color,
                                 outline=self.node.color)

    def render_vector_shape(self, drawer, _, **kwargs):
        fill = kwargs.get('fill')

        # create pathdata
        m = self.metrics.cell(self.node)
        rx = (self.node.width or self.metrics.node_width) // 12
        ry = (self.node.height or self.metrics.node_height) // 5

        pt = m.topleft
        if kwargs.get('shadow'):
            pt = self.shift_shadow(pt)

        path = pathdata(pt.x + rx * 2, pt.y + ry * 2)
        path.ellarc(rx * 2, ry, 0, 0, 1, pt.x + rx * 4, pt.y + ry)
        path.ellarc(rx * 2, ry * 3 // 4, 0, 0, 1, pt.x + rx * 9, pt.y + ry)
        path.ellarc(rx * 2, ry, 0, 0, 1, pt.x + rx * 11, pt.y + ry * 2)
        path.ellarc(rx * 2, ry, 0, 0, 1, pt.x + rx * 11, pt.y + ry * 4)
        path.ellarc(rx * 2, ry * 5 // 2, 0, 0, 1, pt.x + rx * 8, pt.y + ry * 4)
        path.ellarc(rx * 2, ry * 5 // 2, 0, 0, 1, pt.x + rx * 5, pt.y + ry * 4)
        path.ellarc(rx * 2, ry * 5 // 2, 0, 0, 1, pt.x + rx * 2, pt.y + ry * 4)
        path.ellarc(rx * 2, ry, 0, 0, 1, pt.x + rx * 2, pt.y + ry * 2)

        # draw outline
        if kwargs.get('shadow'):
            if kwargs.get('style') == 'blur':
                drawer.path(path, fill=fill, outline=fill,
                            filter='transp-blur')
            else:
                drawer.path(path, fill=fill, outline=fill)
        elif self.node.background:
            drawer.path(path, fill=self.node.color, outline=self.node.color)
            drawer.image(self.textbox, self.node.background)
            drawer.path(path, fill="none", outline=self.node.linecolor,
                        style=self.node.style)
        else:
            drawer.path(path, fill=self.node.color,
                        outline=self.node.linecolor, style=self.node.style)


def setup(self):
    install_renderer('cloud', Cloud)
