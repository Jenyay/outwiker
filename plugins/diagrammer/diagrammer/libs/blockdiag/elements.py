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

import copy
import os
import re

from blockdiag import noderenderer, plugins
from blockdiag.utils import XY, images, unquote, urlutil, uuid
from blockdiag.utils.logging import warning


class Base(object):
    basecolor = (255, 255, 255)
    textcolor = (0, 0, 0)
    fontfamily = None
    fontsize = None
    style = None
    int_attrs = ['colwidth', 'colheight', 'fontsize']

    @classmethod
    def set_default_color(cls, color):
        cls.basecolor = images.color_to_rgb(color)

    @classmethod
    def set_default_style(cls, style):
        cls.style = style

    @classmethod
    def set_default_text_color(cls, color):
        cls.textcolor = images.color_to_rgb(color)

    @classmethod
    def set_default_fontfamily(cls, fontfamily):
        cls.fontfamily = fontfamily

    @classmethod
    def set_default_fontsize(cls, fontsize):
        cls.fontsize = int(fontsize)

    @classmethod
    def clear(cls):
        cls.basecolor = (255, 255, 255)
        cls.textcolor = (0, 0, 0)
        cls.fontfamily = None
        cls.fontsize = None
        cls.style = None

    def duplicate(self):
        return copy.copy(self)

    def set_attribute(self, attr):
        name = attr.name
        value = unquote(attr.value)

        if name == 'class':
            if value in Diagram.classes:
                klass = Diagram.classes[value]
                self.set_attributes(klass.attrs)
            else:
                msg = "Unknown class: %s" % value
                raise AttributeError(msg)
        elif hasattr(self, "set_%s" % name):
            getattr(self, "set_%s" % name)(value)
        elif name in self.int_attrs:
            setattr(self, name, int(value))
        elif hasattr(self, name) and not callable(getattr(self, name)):
            setattr(self, name, value)
        else:
            class_name = self.__class__.__name__
            msg = "Unknown attribute: %s.%s" % (class_name, attr.name)
            raise AttributeError(msg)

    def set_attributes(self, attrs):
        for attr in attrs:
            self.set_attribute(attr)

    def set_style(self, value):
        if re.search(r'^(?:none|solid|dotted|dashed|\d+(,\d+)*)$', value, re.I):
            self.style = value.lower()
        else:
            class_name = self.__class__.__name__
            msg = "unknown %s style: %s" % (class_name, value)
            raise AttributeError(msg)


class Element(Base):
    namespace = {}
    int_attrs = Base.int_attrs + ['width', 'height']

    @classmethod
    def get(cls, elemid):
        if not elemid:
            elemid = uuid.generate()

        unquote_id = unquote(elemid)
        if unquote_id not in cls.namespace:
            obj = cls(elemid)
            cls.namespace[unquote_id] = obj

        return cls.namespace[unquote_id]

    @classmethod
    def clear(cls):
        super(Element, cls).clear()
        cls.namespace = {}
        cls.basecolor = (255, 255, 255)
        cls.textcolor = (0, 0, 0)

    def __init__(self, elemid):
        self.id = unquote(elemid)
        self.label = ''
        self.xy = XY(0, 0)
        self.group = None
        self.drawable = False
        self.order = 0
        self.color = self.basecolor
        self.width = None
        self.height = None
        self.colwidth = 1
        self.colheight = 1
        self.stacked = False

    def __repr__(self):
        _format = "<%s '%s' %s %dx%d at 0x%08x>"
        params = (self.__class__.__name__, self.id, str(self.xy),
                  self.colwidth, self.colheight, id(self))
        return _format % params

    def set_color(self, color):
        self.color = images.color_to_rgb(color)

    def set_textcolor(self, color):
        self.textcolor = images.color_to_rgb(color)


class DiagramNode(Element):
    shape = 'box'
    int_attrs = Element.int_attrs + ['rotate']
    linecolor = (0, 0, 0)
    label_orientation = 'horizontal'
    desctable = []
    attrname = {}

    @classmethod
    def set_default_shape(cls, shape):
        cls.shape = shape

    @classmethod
    def set_default_linecolor(cls, color):
        cls.linecolor = images.color_to_rgb(color)

    @classmethod
    def clear(cls):
        super(DiagramNode, cls).clear()
        cls.shape = 'box'
        cls.linecolor = (0, 0, 0)
        cls.label_orientation = 'horizontal'
        cls.desctable = ['numbered', 'label', 'description']
        cls.attrname = dict(numbered='No', label='Name',
                            description='Description')

    def __init__(self, elemid):
        super(DiagramNode, self).__init__(elemid)

        self.label = unquote(elemid) or ''
        self.numbered = None
        self.icon = None
        self.background = None
        self.description = None
        self.rotate = 0
        self.drawable = True
        self.href = None

        plugins.fire_node_event(self, 'created')

    def set_attribute(self, attr):
        if plugins.fire_node_event(self, 'attr_changing', attr):
            super(DiagramNode, self).set_attribute(attr)
            plugins.fire_node_event(self, 'attr_changed', attr)

    def set_linecolor(self, color):
        self.linecolor = images.color_to_rgb(color)

    def set_shape(self, value):
        if noderenderer.get(value):
            self.shape = value
        else:
            msg = "unknown node shape: %s" % value
            raise AttributeError(msg)

    def set_icon(self, value):
        if urlutil.isurl(value) or os.path.isfile(value):
            self.icon = value
        else:
            warning("icon image not found: %s", value)

    def set_background(self, value):
        if urlutil.isurl(value) or os.path.isfile(value):
            self.background = value
        else:
            warning("background image not found: %s", value)

    def set_stacked(self, _):
        self.stacked = True

    def set_label_orientation(self, value):
        value = value.lower()
        if value in ('horizontal', 'vertical'):
            self.label_orientation = value
        else:
            msg = "unknown label orientation: %s" % value
            raise AttributeError(msg)

    def to_desctable(self):
        attrs = []
        for name in self.desctable:
            value = getattr(self, name)
            if value is None:
                attrs.append("")
            else:
                attrs.append(value)

        return attrs


class NodeGroup(Element):
    basecolor = (243, 152, 0)

    @classmethod
    def clear(cls):
        super(NodeGroup, cls).clear()
        cls.basecolor = (243, 152, 0)

    def __init__(self, elemid):
        super(NodeGroup, self).__init__(elemid)

        self.level = 0
        self.separated = False
        self.shape = 'box'
        self.thick = 3
        self.nodes = []
        self.edges = []
        self.icon = None
        self.orientation = 'landscape'
        self.href = None

    def duplicate(self):
        copied = super(NodeGroup, self).duplicate()
        copied.nodes = []
        copied.edges = []

        return copied

    def parent(self, level):
        if self.level < level:
            return None

        group = self
        while group.level != level:
            group = group.group

        return group

    def is_parent(self, other):
        parent = self.parent(other.level)
        return parent == other

    def traverse_nodes(self, preorder=False):
        for node in self.nodes:
            if isinstance(node, NodeGroup):
                if preorder:
                    yield node

                for subnode in node.traverse_nodes(preorder=preorder):
                    yield subnode

                if not preorder:
                    yield node
            else:
                yield node

    def traverse_edges(self, preorder=False):
        if preorder:
            for edge in self.edges:
                yield edge

        for group in self.traverse_groups(preorder):
            for edge in group.traverse_edges(preorder):
                yield edge

        if not preorder:
            for edge in self.edges:
                yield edge

    def traverse_groups(self, preorder=False):
        for node in self.traverse_nodes(preorder=preorder):
            if isinstance(node, NodeGroup):
                yield node

    def fixiate(self, fixiate_nodes=False):
        if self.separated:
            self.colwidth = 1
            self.colheight = 1

            return
        elif len(self.nodes) > 0:
            self.colwidth = max(x.xy.x + x.colwidth for x in self.nodes)
            self.colheight = max(x.xy.y + x.colheight for x in self.nodes)

        for node in self.nodes:
            if fixiate_nodes:
                node.xy = XY(self.xy.x + node.xy.x,
                             self.xy.y + node.xy.y)

            if isinstance(node, NodeGroup):
                node.fixiate(fixiate_nodes)

    def update_order(self):
        for i, node in enumerate(self.nodes):
            node.order = i

    def set_orientation(self, value):
        value = value.lower()
        if value in ('landscape', 'portrait'):
            self.orientation = value
        else:
            msg = "unknown diagram orientation: %s" % value
            raise AttributeError(msg)

    def set_shape(self, value):
        value = value.lower()
        if value in ('box', 'line'):
            self.shape = value
        else:
            msg = "unknown group shape: %s" % value
            raise AttributeError(msg)


class DiagramEdge(Base):
    basecolor = (0, 0, 0)
    namespace = {}

    @classmethod
    def get(cls, node1, node2):
        if node1 not in cls.namespace:
            cls.namespace[node1] = {}

        if node2 not in cls.namespace[node1]:
            obj = cls(node1, node2)
            cls.namespace[node1][node2] = obj

        return cls.namespace[node1][node2]

    @classmethod
    def find(cls, node1, node2=None):
        if node1 is None and node2 is None:
            return cls.find_all()
        elif isinstance(node1, NodeGroup):
            edges = cls.find(None, node2)
            edges = (e for e in edges if e.node1.group.is_parent(node1))
            return [e for e in edges if not e.node2.group.is_parent(node1)]
        elif isinstance(node2, NodeGroup):
            edges = cls.find(node1, None)
            edges = (e for e in edges if e.node2.group.is_parent(node2))
            return [e for e in edges if not e.node1.group.is_parent(node2)]
        elif node1 is None:
            return [e for e in cls.find_all() if e.node2 == node2]
        else:
            if node1 not in cls.namespace:
                return []

            if node2 is None:
                return cls.namespace[node1].values()

            if node2 not in cls.namespace[node1]:
                return []

        return cls.namespace[node1][node2]

    @classmethod
    def find_all(cls):
        for v1 in cls.namespace.values():
            for v2 in v1.values():
                yield v2

    @classmethod
    def find_by_level(cls, level):
        edges = []
        for e in cls.find_all():
            edge = e.duplicate()
            skips = 0

            if edge.node1.group.level < level:
                skips += 1
            else:
                while edge.node1.group.level != level:
                    edge.node1 = edge.node1.group

            if edge.node2.group.level < level:
                skips += 1
            else:
                while edge.node2.group.level != level:
                    edge.node2 = edge.node2.group

            if skips == 2:
                continue

            edges.append(edge)

        return edges

    @classmethod
    def clear(cls):
        super(DiagramEdge, cls).clear()
        cls.namespace = {}
        cls.basecolor = (0, 0, 0)

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.crosspoints = []
        self.skipped = 0

        self.label = None
        self.description = None
        self.dir = 'forward'
        self.color = self.basecolor
        self.hstyle = None
        self.folded = None
        self.thick = None

    def __repr__(self):
        _format = "<%s '%s' %s - '%s' %s at 0x%08x>"
        params = (self.__class__.__name__, self.node1.id, self.node1.xy,
                  self.node2.id, self.node2.xy, id(self))
        return _format % params

    def set_dir(self, value):
        value = value.lower()
        if value in ('back', 'both', 'none', 'forward'):
            self.dir = value
        elif value == '-<':
            self.dir = 'forward'
            self.hstyle = 'onemany'
        elif value == '>-':
            self.dir = 'back'
            self.hstyle = 'manyone'
        elif value == '>-<':
            self.dir = 'both'
            self.hstyle = 'manymany'
        elif value == '->':
            self.dir = 'forward'
        elif value == '<-':
            self.dir = 'back'
        elif value == '<->':
            self.dir = 'both'
        elif value == '--':
            self.dir = 'none'
        else:
            msg = "unknown edge dir: %s" % value
            raise AttributeError(msg)

    def set_color(self, color):
        self.color = images.color_to_rgb(color)

    def set_hstyle(self, value):
        value = value.lower()
        if value in ('generalization', 'composition', 'aggregation'):
            self.hstyle = value
        elif value == 'oneone':
            self.dir = 'none'
            self.hstyle = value
        elif value == 'onemany':
            self.dir = 'forward'
            self.hstyle = value
        elif value == 'manyone':
            self.dir = 'back'
            self.hstyle = value
        elif value == 'manymany':
            self.dir = 'both'
            self.hstyle = value
        else:
            msg = "unknown edge hstyle: %s" % value
            raise AttributeError(msg)

    def set_folded(self, _):
        self.folded = True

    def set_nofolded(self, _):
        self.folded = False

    def set_thick(self, _):
        self.thick = 3

    @property
    def direction(self):
        node1 = self.node1.xy
        node2 = self.node2.xy

        if node1.x > node2.x:
            if node1.y > node2.y:
                _dir = 'left-up'
            elif node1.y == node2.y:
                _dir = 'left'
            else:
                _dir = 'left-down'
        elif node1.x == node2.x:
            if node1.y > node2.y:
                _dir = 'up'
            elif node1.y == node2.y:
                _dir = 'same'
            else:
                _dir = 'down'
        else:
            if node1.y > node2.y:
                _dir = 'right-up'
            elif node1.y == node2.y:
                _dir = 'right'
            else:
                _dir = 'right-down'

        return _dir

    def to_desctable(self):
        label = "%s -> %s" % (self.node1.label, self.node2.label)
        return [label, self.description]


class Diagram(NodeGroup):
    _DiagramNode = DiagramNode
    _DiagramEdge = DiagramEdge
    _NodeGroup = NodeGroup

    classes = {}
    shadow_style = 'blur'
    linecolor = (0, 0, 0)
    int_attrs = (NodeGroup.int_attrs +
                 ['node_width', 'node_height', 'span_width', 'span_height'])

    @classmethod
    def clear(cls):
        super(Diagram, cls).clear()
        cls.shadow_style = 'blur'
        cls.linecolor = (0, 0, 0)
        cls.classes = {}

    def __init__(self):
        super(Diagram, self).__init__(None)

        self.config = None
        self.node_width = None
        self.node_height = None
        self.span_width = None
        self.span_height = None
        self.page_padding = None
        self.edge_layout = None

    def set_plugin(self, name, attrs, **kwargs):
        kwargs.update(dict([str(unquote(attr.name)), unquote(attr.value)]
                           for attr in attrs))
        plugins.load([name], diagram=self, **kwargs)

    def set_plugins(self, value, **kwargs):
        modules = [name.strip() for name in value.split(',')]
        plugins.load(modules, diagram=self, **kwargs)

    def set_default_shape(self, value):
        if noderenderer.get(value):
            DiagramNode.set_default_shape(value)
        else:
            msg = "unknown node shape: %s" % value
            raise AttributeError(msg)

    def set_default_label_orientation(self, value):
        value = value.lower()
        if value in ('horizontal', 'vertical'):
            DiagramNode.label_orientation = value
        else:
            msg = "unknown label orientation: %s" % value
            raise AttributeError(msg)

    def set_default_text_color(self, color):
        warning("default_text_color is obsoleted; use default_textcolor")
        self.set_default_textcolor(color)

    def set_default_textcolor(self, color):
        self.textcolor = images.color_to_rgb(color)
        self._DiagramNode.set_default_text_color(self.textcolor)
        self._NodeGroup.set_default_text_color(self.textcolor)
        self._DiagramEdge.set_default_text_color(self.textcolor)

    def set_default_node_color(self, color):
        color = images.color_to_rgb(color)
        self._DiagramNode.set_default_color(color)

    def set_default_node_style(self, value):
        if re.search(r'^(?:none|solid|dotted|dashed|\d+(,\d+)*)$', value, re.I):
            self._DiagramNode.set_default_style(value)
        else:
            msg = "unknown node style: %s" % value
            raise AttributeError(msg)

    def set_default_line_color(self, color):
        warning("default_line_color is obsoleted; use default_linecolor")
        self.set_default_linecolor(color)

    def set_default_linecolor(self, color):
        self.linecolor = images.color_to_rgb(color)
        self._DiagramNode.set_default_linecolor(self.linecolor)
        self._DiagramEdge.set_default_color(self.linecolor)

    def set_default_group_color(self, color):
        color = images.color_to_rgb(color)
        self._NodeGroup.set_default_color(color)

    def set_shape_namespace(self, value):
        noderenderer.set_default_namespace(value)

    def set_default_fontfamily(self, fontfamily):
        self._DiagramNode.set_default_fontfamily(fontfamily)
        self._NodeGroup.set_default_fontfamily(fontfamily)
        self._DiagramEdge.set_default_fontfamily(fontfamily)

    def set_default_fontsize(self, fontsize):
        self._DiagramNode.set_default_fontsize(fontsize)
        self._NodeGroup.set_default_fontsize(fontsize)
        self._DiagramEdge.set_default_fontsize(fontsize)

    def set_shadow_style(self, value):
        value = value.lower()
        if value in ('solid', 'blur', 'none'):
            self.shadow_style = value
        else:
            msg = "unknown shadow style: %s" % value
            raise AttributeError(msg)

    def set_edge_layout(self, value):
        value = value.lower()
        if value in ('normal', 'flowchart'):
            warning("edge_layout is very experimental feature!")

            self.edge_layout = value
        else:
            msg = "unknown edge layout: %s" % value
            raise AttributeError(msg)

    def set_fontsize(self, value):
        warning("fontsize is obsoleted; use default_fontsize")
        self.set_default_fontsize(int(value))
