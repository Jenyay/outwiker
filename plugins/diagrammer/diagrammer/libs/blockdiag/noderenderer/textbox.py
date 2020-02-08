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
from blockdiag.utils import XY, Box, images


class TextBox(NodeShape):
    def __init__(self, node, metrics=None):
        super(TextBox, self).__init__(node, metrics)

        if self.node.background:
            size = images.get_image_size(self.node.background)
            size = images.calc_image_size(size, self.textbox.size)

            pt = self.textbox.center
            self.textbox = Box(pt.x - size[0] // 2, pt.y - size[1] // 2,
                               pt.x + size[0] // 2, pt.y + size[1] // 2)

            self.connectors[0] = XY(pt.x, self.textbox[1])
            self.connectors[1] = XY(self.textbox[2], pt.y)
            self.connectors[2] = XY(pt.x, self.textbox[3])
            self.connectors[3] = XY(self.textbox[0], pt.y)

        if self.node.icon:
            self.connectors[3] = XY(self.iconbox[0], pt.y)

    def render_shape(self, drawer, _, **kwargs):
        if not kwargs.get('shadow') and self.node.background:
            drawer.image(self.textbox, self.node.background)


def setup(self):
    install_renderer('textbox', TextBox)
