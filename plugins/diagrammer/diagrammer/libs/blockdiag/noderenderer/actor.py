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
from blockdiag.utils import XY, Box, Size


class Actor(NodeShape):
    def __init__(self, node, metrics=None):
        super(Actor, self).__init__(node, metrics)

        m = metrics.cell(node)
        if node.label:
            font = metrics.font_for(self.node)
            textsize = metrics.textsize(node.label, font)
            shortside = min(m.width, m.height - textsize.height)
        else:
            textsize = Size(0, 0)
            shortside = min(m.width, m.height)

        r = self.radius = shortside // 8  # radius of actor's head
        self.center = metrics.cell(node).center

        self.connectors[0] = XY(self.center.x, self.center.y - r * 9 // 2)
        self.connectors[1] = XY(self.center.x + r * 4, self.center.y)
        self.connectors[2] = XY(self.center.x,
                                self.center.y + r * 4 + textsize.height)
        self.connectors[3] = XY(self.center.x - r * 4, self.center.y)

        self.textbox = Box(m.left.x,
                           self.center.y + r * 4,
                           m.right.x,
                           self.connectors[2].y)

    def head_part(self):
        r = self.radius * 3 // 2
        pt = self.metrics.cell(self.node).center.shift(y=-self.radius * 3)
        return Box(pt.x - r, pt.y - r, pt.x + r, pt.y + r)

    def body_part(self):
        r = self.radius
        m = self.metrics.cell(self.node)

        bodyC = m.center
        neckWidth = r * 2 // 3  # neck size
        arm = r * 4  # arm length
        armWidth = r
        bodyWidth = r * 2 // 3  # half of body width
        bodyHeight = r
        legXout = r * 7 // 2  # toe outer position
        legYout = bodyHeight + r * 3
        legXin = r * 2  # toe inner position
        legYin = bodyHeight + r * 3

        return [XY(bodyC.x + neckWidth, bodyC.y - r * 2),
                XY(bodyC.x + neckWidth, bodyC.y - armWidth),  # neck end
                XY(bodyC.x + arm, bodyC.y - armWidth),
                XY(bodyC.x + arm, bodyC.y),  # right arm end
                XY(bodyC.x + bodyWidth, bodyC.y),   # right body end
                XY(bodyC.x + bodyWidth, bodyC.y + bodyHeight),
                XY(bodyC.x + legXout, bodyC.y + legYout),
                XY(bodyC.x + legXin, bodyC.y + legYin),

                XY(bodyC.x, bodyC.y + (bodyHeight * 2)),  # body bottom center

                XY(bodyC.x - legXin, bodyC.y + legYin),
                XY(bodyC.x - legXout, bodyC.y + legYout),
                XY(bodyC.x - bodyWidth, bodyC.y + bodyHeight),
                XY(bodyC.x - bodyWidth, bodyC.y),  # left body end
                XY(bodyC.x - arm, bodyC.y),
                XY(bodyC.x - arm, bodyC.y - armWidth),
                XY(bodyC.x - neckWidth, bodyC.y - armWidth),  # left arm end
                XY(bodyC.x - neckWidth, bodyC.y - r * 2)]

    def render_shape(self, drawer, _, **kwargs):
        fill = kwargs.get('fill')

        # draw body part
        body = self.body_part()
        if kwargs.get('shadow'):
            body = self.shift_shadow(body)
            if kwargs.get('style') == 'blur':
                drawer.polygon(body, fill=fill, filter='transp-blur')
            else:
                drawer.polygon(body, fill=fill)
        else:
            drawer.polygon(body, fill=self.node.color,
                           outline=self.node.linecolor, style=self.node.style)

        # draw head part
        head = self.head_part()
        if kwargs.get('shadow'):
            head = self.shift_shadow(head)
            if kwargs.get('style') == 'blur':
                drawer.ellipse(head, fill=fill, outline=self.node.linecolor,
                               filter='transp-blur')
            else:
                drawer.ellipse(head, fill=fill, outline=self.node.linecolor)
        else:
            drawer.ellipse(head, fill=self.node.color,
                           outline=self.node.linecolor, style=self.node.style)


def setup(self):
    install_renderer('actor', Actor)
