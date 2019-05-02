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


class NoneShape(NodeShape):
    def __init__(self, node, metrics=None):
        super(NoneShape, self).__init__(node, metrics)

        p = metrics.cell(node).center
        self.connectors = [p, p, p, p]

    def render_label(self, drawer, **kwargs):
        pass

    def render_shape(self, drawer, _, **kwargs):
        pass


def setup(self):
    install_renderer('none', NoneShape)
