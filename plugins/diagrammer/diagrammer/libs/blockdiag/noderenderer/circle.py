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

from blockdiag.noderenderer import install_renderer
from blockdiag.noderenderer.base import NodeShape
from blockdiag.utils import XY, Box


class Circle(NodeShape):
    def __init__(self, node, metrics=None):
        super(Circle, self).__init__(node, metrics)

        cell = metrics.cell(node)
        r = min(cell.box.width, cell.box.height) // 2 + \
            metrics.cellsize // 2
        pt = metrics.cell(node).center
        self.connectors = [XY(pt.x, pt.y - r),  # top
                           XY(pt.x + r, pt.y),  # right
                           XY(pt.x, pt.y + r),  # bottom
                           XY(pt.x - r, pt.y)]  # left
        self.textbox = Box(pt.x - r, pt.y - r, pt.x + r, pt.y + r)

    def render_shape(self, drawer, _, **kwargs):
        fill = kwargs.get('fill')

        # draw outline
        if kwargs.get('shadow'):
            box = self.shift_shadow(self.textbox)
            if kwargs.get('style') == 'blur':
                drawer.ellipse(box, fill=fill, outline=fill,
                               filter='transp-blur')
            else:
                drawer.ellipse(box, fill=fill, outline=fill)
        elif self.node.background:
            drawer.ellipse(self.textbox, fill=self.node.color,
                           outline=self.node.color)
            drawer.image(self.textbox, self.node.background)
            drawer.ellipse(self.textbox, fill="none",
                           outline=self.node.linecolor, style=self.node.style)
        else:
            drawer.ellipse(self.textbox, fill=self.node.color,
                           outline=self.node.linecolor, style=self.node.style)


def setup(self):
    install_renderer('circle', Circle)
