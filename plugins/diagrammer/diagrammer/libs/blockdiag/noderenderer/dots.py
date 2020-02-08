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


class Dots(NodeShape):
    def render_label(self, drawer, **kwargs):
        pass

    def render_shape(self, drawer, _, **kwargs):
        if kwargs.get('shadow'):
            return

        m = self.metrics
        center = m.cell(self.node).center
        dots = [center]
        if self.node.group.orientation == 'landscape':
            pt = XY(center.x, center.y - m.node_height / 2)
            dots.append(pt)

            pt = XY(center.x, center.y + m.node_height / 2)
            dots.append(pt)
        else:
            pt = XY(center.x - m.node_width / 3, center.y)
            dots.append(pt)

            pt = XY(center.x + m.node_width / 3, center.y)
            dots.append(pt)

        r = m.cellsize / 2
        for dot in dots:
            box = Box(dot.x - r, dot.y - r, dot.x + r, dot.y + r)
            drawer.ellipse(box, fill=self.node.linecolor,
                           outline=self.node.linecolor)


def setup(self):
    install_renderer('dots', Dots)
