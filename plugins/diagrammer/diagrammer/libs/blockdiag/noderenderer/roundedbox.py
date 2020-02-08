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

from blockdiag.imagedraw.simplesvg import pathdata
from blockdiag.noderenderer import install_renderer
from blockdiag.noderenderer.base import NodeShape
from blockdiag.utils import XY, Box


class RoundedBox(NodeShape):
    def render_shape(self, drawer, _, **kwargs):
        # draw background
        self.render_shape_background(drawer, **kwargs)

        # draw outline
        box = self.metrics.cell(self.node).box
        if not kwargs.get('shadow'):
            if self.node.background:
                drawer.image(box, self.node.background)

            self.render_shape_outline(drawer, **kwargs)

    def render_shape_outline(self, drawer, **kwargs):
        m = self.metrics.cell(self.node)
        r = self.metrics.cellsize
        box = m.box

        lines = [(XY(box[0] + r, box[1]), XY(box[2] - r, box[1])),
                 (XY(box[2], box[1] + r), XY(box[2], box[3] - r)),
                 (XY(box[0] + r, box[3]), XY(box[2] - r, box[3])),
                 (XY(box[0], box[1] + r), XY(box[0], box[3] - r))]
        for line in lines:
            drawer.line(line, fill=self.node.linecolor, style=self.node.style)

        r2 = r * 2
        arcs = [(Box(box[0], box[1], box[0] + r2, box[1] + r2), 180, 270),
                (Box(box[2] - r2, box[1], box[2], box[1] + r2), 270, 360),
                (Box(box[2] - r2, box[3] - r2, box[2], box[3]), 0, 90),
                (Box(box[0], box[3] - r2, box[0] + r2, box[3]), 90, 180)]
        for arc in arcs:
            drawer.arc(arc[0], arc[1], arc[2],
                       fill=self.node.linecolor, style=self.node.style)

    def render_shape_background(self, drawer, **kwargs):
        fill = kwargs.get('fill')

        m = self.metrics.cell(self.node)
        r = self.metrics.cellsize

        box = m.box
        ellipses = [Box(box[0], box[1], box[0] + r * 2, box[1] + r * 2),
                    Box(box[2] - r * 2, box[1], box[2], box[1] + r * 2),
                    Box(box[0], box[3] - r * 2, box[0] + r * 2, box[3]),
                    Box(box[2] - r * 2, box[3] - r * 2, box[2], box[3])]

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
                               outline=self.node.color)

        rects = [Box(box[0] + r, box[1], box[2] - r, box[3]),
                 Box(box[0], box[1] + r, box[2], box[3] - r)]
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
        box = self.metrics.cell(self.node).box
        r = self.metrics.cellsize

        if kwargs.get('shadow'):
            box = self.shift_shadow(box)

        path = pathdata(box[0] + r, box[1])
        path.line(box[2] - r, box[1])
        path.ellarc(r, r, 0, 0, 1, box[2], box[1] + r)
        path.line(box[2], box[3] - r)
        path.ellarc(r, r, 0, 0, 1, box[2] - r, box[3])
        path.line(box[0] + r, box[3])
        path.ellarc(r, r, 0, 0, 1, box[0], box[3] - r)
        path.line(box[0], box[1] + r)
        path.ellarc(r, r, 0, 0, 1, box[0] + r, box[1])

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
            drawer.path(path, fill="none",
                        outline=self.node.linecolor, style=self.node.style)
        else:
            drawer.path(path, fill=self.node.color,
                        outline=self.node.linecolor, style=self.node.style)


def setup(self):
    install_renderer('roundedbox', RoundedBox)
