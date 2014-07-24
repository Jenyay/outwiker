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

from blockdiag import plugins


class NodeAttributes(plugins.NodeHandler):
    def __init__(self, diagram, **kwargs):
        super(NodeAttributes, self).__init__(diagram, **kwargs)

        node_klass = diagram._DiagramNode
        for name, label in kwargs.items():
            if label is None:
                label = name
            if name not in node_klass.desctable:
                node_klass.desctable.insert(-1, name)

            node_klass.attrname[name] = label
            if not hasattr(node_klass, name):
                setattr(node_klass, name, None)


def setup(self, diagram, **kwargs):
    plugins.install_node_handler(NodeAttributes(diagram, **kwargs))
