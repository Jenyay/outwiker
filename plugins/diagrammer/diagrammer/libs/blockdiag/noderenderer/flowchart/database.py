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
from blockdiag.utils import XY, Box


class Database(NodeShape):
    def __init__(self, node, metrics=None):
        super(Database, self).__init__(node, metrics)

        m = self.metrics.cell(self.node)
        r = self.metrics.cellsize
        self.textbox = Box(m.topleft.x, m.topleft.y + r * 3 // 2,
                           m.bottomright.x, m.bottomright.y - r // 2)

    def render_shape(self, drawer, _, **kwargs):
        # draw background
        self.render_shape_background(drawer, **kwargs)

        # draw background image
        if self.node.background:
            drawer.image(self.textbox, self.node.background)

    def render_shape_background(self, drawer, **kwargs):
        fill = kwargs.get('fill')

        m = self.metrics.cell(self.node)
        r = self.metrics.cellsize
        box = m.box

        ellipse = Box(box[0], box[3] - r * 2, box[2], box[3])
        if kwargs.get('shadow'):
            ellipse = self.shift_shadow(ellipse)
            if kwargs.get('style') == 'blur':
                drawer.ellipse(ellipse, fill=fill, outline=fill,
                               filter='transp-blur')
            else:
                drawer.ellipse(ellipse, fill=fill, outline=fill)
        else:
            drawer.ellipse(ellipse, fill=self.node.color,
                           outline=self.node.linecolor, style=self.node.style)

        rect = Box(box[0], box[1] + r, box[2], box[3] - r)
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

        ellipse = Box(box[0], box[1], box[2], box[1] + r * 2)
        if kwargs.get('shadow'):
            ellipse = self.shift_shadow(ellipse)
            if kwargs.get('style') == 'blur':
                drawer.ellipse(ellipse, fill=fill, outline=fill,
                               filter='transp-blur')
            else:
                drawer.ellipse(ellipse, fill=fill, outline=fill)
        else:
            drawer.ellipse(ellipse, fill=self.node.color,
                           outline=self.node.linecolor, style=self.node.style)

        # line both side
        lines = [(XY(box[0], box[1] + r), XY(box[0], box[3] - r)),
                 (XY(box[2], box[1] + r), XY(box[2], box[3] - r))]
        for line in lines:
            if not kwargs.get('shadow'):
                drawer.line(line, fill=self.node.linecolor,
                            style=self.node.style)

    def render_vector_shape(self, drawer, _, **kwargs):
        fill = kwargs.get('fill')

        m = self.metrics.cell(self.node)
        r = self.metrics.cellsize
        width = self.metrics.node_width

        box = m.box
        if kwargs.get('shadow'):
            box = self.shift_shadow(box)

        path = pathdata(box[0], box[1] + r)
        path.ellarc(width // 2, r, 0, 0, 1, box[2], box[1] + r)
        path.line(box[2], box[3] - r)
        path.ellarc(width // 2, r, 0, 0, 1, box[0], box[3] - r)
        path.line(box[0], box[1] + r)

        # draw outline
        if kwargs.get('shadow'):
            if kwargs.get('style') == 'blur':
                drawer.path(path, fill=fill, outline=fill,
                            filter='transp-blur')
            else:
                drawer.path(path, fill=fill, outline=fill)
        elif self.node.background:
            drawer.path(path, fill=self.node.color,
                        outline=self.node.color)
            drawer.image(self.textbox, self.node.background)
            drawer.path(path, fill="none",
                        outline=self.node.linecolor, style=self.node.style)
        else:
            drawer.path(path, fill=self.node.color,
                        outline=self.node.linecolor, style=self.node.style)

        # draw cap of cylinder
        if not kwargs.get('shadow'):
            path = pathdata(box[2], box[1] + r)
            path.ellarc(width // 2, r, 0, 0, 1, box[0], box[1] + r)
            drawer.path(path, fill=self.node.color,
                        outline=self.node.linecolor, style=self.node.style)


def setup(self):
    install_renderer('flowchart.database', Database)
