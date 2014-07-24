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

from blockdiag.noderenderer import install_renderer
from blockdiag.noderenderer.base import NodeShape
from blockdiag.utils import XY, Box


class EndPoint(NodeShape):
    def __init__(self, node, metrics=None):
        super(EndPoint, self).__init__(node, metrics)

        m = metrics.cell(node)

        self.radius = metrics.cellsize
        self.center = m.center
        self.textbox = Box(m.top.x, m.top.y, m.right.x, m.right.y)
        self.textalign = 'left'
        self.connectors = [XY(self.center.x, self.center.y - self.radius),
                           XY(self.center.x + self.radius, self.center.y),
                           XY(self.center.x, self.center.y + self.radius),
                           XY(self.center.x - self.radius, self.center.y)]

    def render_shape(self, drawer, _, **kwargs):
        fill = kwargs.get('fill')

        # draw outer circle
        r = self.radius
        box = Box(self.center.x - r, self.center.y - r,
                  self.center.x + r, self.center.y + r)
        if kwargs.get('shadow'):
            box = self.shift_shadow(box)
            if kwargs.get('style') == 'blur':
                drawer.ellipse(box, fill=fill, outline=fill,
                               filter='transp-blur')
            else:
                drawer.ellipse(box, fill=fill, outline=fill)
        else:
            drawer.ellipse(box, fill='white', outline=self.node.linecolor,
                           style=self.node.style)

        # draw inner circle
        box = Box(self.center.x - r / 2, self.center.y - r / 2,
                  self.center.x + r / 2, self.center.y + r / 2)
        if not kwargs.get('shadow'):
            if self.node.color == self.node.basecolor:
                color = self.node.linecolor
            else:
                color = self.node.color

            drawer.ellipse(box, fill=color, outline=self.node.linecolor,
                           style=self.node.style)


def setup(self):
    install_renderer('endpoint', EndPoint)
