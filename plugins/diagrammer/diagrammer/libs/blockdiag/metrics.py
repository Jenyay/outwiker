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

import copy
from collections import defaultdict

from blockdiag import noderenderer
from blockdiag.elements import DiagramNode
from blockdiag.utils import XY, Box, Size
from blockdiag.utils.fontmap import FontInfo, FontMap

cellsize = 8


class EdgeLines(object):
    def __init__(self):
        self.xy = None
        self.stroking = False
        self.polylines = []

    def moveTo(self, x, y=None):
        self.stroking = False
        if y is None:
            self.xy = x
        else:
            self.xy = XY(x, y)

    def lineTo(self, x, y=None):
        if y is None:
            elem = x
        else:
            elem = XY(x, y)

        if self.stroking is False:
            self.stroking = True
            polyline = []
            if self.xy:
                polyline.append(self.xy)
            self.polylines.append(polyline)

        if len(self.polylines[-1]) > 0:
            if self.polylines[-1][-1] == elem:
                return

        self.polylines[-1].append(elem)

    def lines(self):
        lines = []
        for line in self.polylines:
            start = line[0]
            for elem in list(line[1:]):
                lines.append((start, elem))
                start = elem

        return lines


class AutoScaler(object):
    def __init__(self, subject, scale_ratio):
        self.subject = subject
        self.scale_ratio = scale_ratio

    def __getattr__(self, name):
        ratio = self.scale_ratio
        return self.scale(getattr(self.subject, name), ratio)

    def __getitem__(self, name):
        ratio = self.scale_ratio
        return self.scale(self.subject[name], ratio)

    @classmethod
    def scale(cls, value, ratio):
        if not callable(value):
            return cls._scale(value, ratio)
        else:
            def _(*args, **kwargs):
                ret = value(*args, **kwargs)
                return cls._scale(ret, ratio)

            return _

    @classmethod
    def _scale(cls, value, ratio):
        if ratio == 1:
            return value

        klass = value.__class__
        if klass == XY:
            ret = XY(value.x * ratio, value.y * ratio)
        elif klass == Size:
            ret = Size(value.width * ratio, value.height * ratio)
        elif klass == Box:
            ret = Box(value[0] * ratio, value[1] * ratio,
                      value[2] * ratio, value[3] * ratio)
        elif klass == tuple:
            ret = tuple([cls.scale(x, ratio) for x in value])
        elif klass == list:
            ret = [cls.scale(x, ratio) for x in value]
        elif klass == EdgeLines:
            ret = EdgeLines()
            ret.polylines = cls.scale(value.polylines, ratio)
        elif klass == FontInfo:
            ret = FontInfo(value.familyname, value.path, value.size * ratio)
        elif klass == int:
            ret = value * ratio
        elif klass == str:
            ret = value
        else:
            ret = cls(value, ratio)

        return ret

    @property
    def original_metrics(self):
        return self.subject


class DiagramMetrics(object):
    cellsize = cellsize
    edge_layout = 'normal'
    node_padding = 4
    line_spacing = 2
    shadow_offset = XY(3, 6)
    page_margin = XY(0, 0)
    page_padding = [0, 0, 0, 0]
    node_width = cellsize * 16
    node_height = cellsize * 5
    span_width = cellsize * 8
    span_height = cellsize * 5

    def __init__(self, diagram, drawer=None, fontmap=None):
        self.drawer = drawer

        if diagram.node_width is not None:
            self.node_width = diagram.node_width

        if diagram.node_height is not None:
            self.node_height = diagram.node_height

        if diagram.span_width is not None:
            self.span_width = diagram.span_width

        if diagram.span_height is not None:
            self.span_height = diagram.span_height

        if fontmap is not None:
            self.fontmap = fontmap
        else:
            self.fontmap = FontMap()

        if diagram.page_padding is not None:
            self.page_padding = diagram.page_padding

        if diagram.edge_layout is not None:
            self.edge_layout = diagram.edge_layout

        # setup spreadsheet
        sheet = self.spreadsheet = SpreadSheetMetrics(self)
        nodes = [n for n in diagram.traverse_nodes() if n.drawable]

        node_width = self.node_width
        for x in range(diagram.colwidth):
            widths = [n.width for n in nodes if n.xy.x == x]
            if widths:
                width = max(n or node_width for n in widths)
                sheet.set_node_width(x, width)

        node_height = self.node_height
        for y in range(diagram.colheight):
            heights = [n.height for n in nodes if n.xy.y == y]
            if heights:
                height = max(n or node_height for n in heights)
                sheet.set_node_height(y, height)

    @property
    def original_metrics(self):
        return self

    def shift(self, x, y):
        metrics = copy.copy(self)
        metrics.spreadsheet = copy.copy(self.spreadsheet)
        metrics.spreadsheet.metrics = metrics
        metrics.page_margin = XY(x, y)

        return metrics

    def textsize(self, string, font=None, width=65535):
        return self.drawer.textsize(string, font, maxwidth=width)

    def node(self, node):
        renderer = noderenderer.get(node.shape)

        if hasattr(renderer, 'render'):
            return renderer(node, self)
        else:
            return self.cell(node)

    def cell(self, node, use_padding=True):
        return self.spreadsheet.node(node, use_padding)

    def group(self, group):
        return self.spreadsheet.node(group, use_padding=False)

    def edge(self, edge):
        if self.edge_layout == 'flowchart':
            if edge.node1.group.orientation == 'landscape':
                return FlowchartLandscapeEdgeMetrics(edge, self)
            else:
                return FlowchartPortraitEdgeMetrics(edge, self)
        else:
            if edge.node1.group.orientation == 'landscape':
                return LandscapeEdgeMetrics(edge, self)
            else:
                return PortraitEdgeMetrics(edge, self)

    def font_for(self, element):
        return self.fontmap.find(element)

    def pagesize(self, width, height):
        return self.spreadsheet.pagesize(width, height)


class SubMetrics(object):
    def __getattr__(self, name):
        # avoid recursion-error on Python 2.6
        if 'metrics' not in self.__dict__:
            raise AttributeError()

        return getattr(self.metrics, name)


class SpreadSheetMetrics(SubMetrics):
    def __init__(self, metrics):
        self.metrics = metrics
        self.node_width = defaultdict(lambda: metrics.node_width)
        self.node_height = defaultdict(lambda: metrics.node_height)
        self.span_width = defaultdict(lambda: metrics.span_width)
        self.span_height = defaultdict(lambda: metrics.span_height)

    def set_node_width(self, x, width):
        if (width is not None and 0 < width and
           (x not in self.node_width or self.node_width[x] < width)):
            self.node_width[x] = width

    def set_node_height(self, y, height):
        if (height is not None and 0 < height and
           (y not in self.node_height or self.node_height[y] < height)):
            self.node_height[y] = height

    def set_span_width(self, x, width):
        if (width is not None and 0 < width and
           (x not in self.span_width or self.span_width[x] < width)):
            self.span_width[x] = width

    def add_span_width(self, x, width):
        self.span_width[x] += width

    def set_span_height(self, y, height):
        if (height is not None and 0 < height and
           (y not in self.span_height or self.span_height[y] < height)):
            self.span_height[y] = height

    def add_span_height(self, y, height):
        self.span_height[y] += height

    def node(self, node, use_padding=True):
        x1, y1 = self._node_topleft(node, use_padding)
        x2, y2 = self._node_bottomright(node, use_padding)

        return NodeMetrics(self.metrics, x1, y1, x2, y2)

    def _node_topleft(self, node, use_padding=True):
        x, y = node.xy
        margin = self.page_margin
        padding = self.page_padding

        node_width = sum(self.node_width[i] for i in range(x))
        node_height = sum(self.node_height[i] for i in range(y))
        span_width = sum(self.span_width[i] for i in range(x + 1))
        span_height = sum(self.span_height[i] for i in range(y + 1))

        if use_padding:
            width = node.width or self.metrics.node_width
            xdiff = (self.node_width[x] - width) // 2
            if xdiff < 0:
                xdiff = 0

            height = node.height or self.metrics.node_height
            ydiff = (self.node_height[y] - height) // 2
            if ydiff < 0:
                ydiff = 0
        else:
            xdiff = 0
            ydiff = 0

        x1 = margin.x + padding[3] + node_width + span_width + xdiff
        y1 = margin.y + padding[0] + node_height + span_height + ydiff

        return XY(x1, y1)

    def _node_bottomright(self, node, use_padding=True):
        x = node.xy.x + node.colwidth - 1
        y = node.xy.y + node.colheight - 1
        margin = self.page_margin
        padding = self.page_padding

        node_width = sum(self.node_width[i] for i in range(x + 1))
        node_height = sum(self.node_height[i] for i in range(y + 1))
        span_width = sum(self.span_width[i] for i in range(x + 1))
        span_height = sum(self.span_height[i] for i in range(y + 1))

        if use_padding:
            width = node.width or self.metrics.node_width
            xdiff = (self.node_width[x] - width) // 2
            if xdiff < 0:
                xdiff = 0

            height = node.height or self.metrics.node_height
            ydiff = (self.node_height[y] - height) // 2
            if ydiff < 0:
                ydiff = 0
        else:
            xdiff = 0
            ydiff = 0

        x2 = margin.x + padding[3] + node_width + span_width - xdiff
        y2 = margin.y + padding[0] + node_height + span_height - ydiff

        return XY(x2, y2)

    def pagesize(self, width, height):
        margin = self.metrics.page_margin
        padding = self.metrics.page_padding

        dummy = DiagramNode(None)
        dummy.xy = XY(width - 1, height - 1)
        x, y = self._node_bottomright(dummy, use_padding=False)
        x_span = self.span_width[width]
        y_span = self.span_height[height]
        return Size(x + margin.x + padding[1] + x_span,
                    y + margin.y + padding[2] + y_span)


class NodeMetrics(SubMetrics):
    def __init__(self, metrics, x1, y1, x2, y2):
        self.metrics = metrics
        self._box = Box(x1, y1, x2, y2)

    def __getattr__(self, name):
        if hasattr(self._box, name):
            return getattr(self._box, name)
        else:
            return getattr(self.metrics, name)

    def __getitem__(self, key):
        return self.box[key]

    @property
    def box(self):
        return self._box

    @property
    def marginbox(self):
        return Box(self._box.x1 - self.span_width // 8,
                   self._box.y1 - self.span_height // 4,
                   self._box.x2 + self.span_width // 8,
                   self._box.y2 + self.span_height // 4)

    @property
    def corebox(self):
        return Box(self._box.x1 + self.node_padding,
                   self._box.y1 + self.node_padding,
                   self._box.x2 - self.node_padding * 2,
                   self._box.y2 - self.node_padding * 2)

    @property
    def grouplabelbox(self):
        return Box(self._box.x1, self._box.y1 - self.span_height // 2,
                   self._box.x2, self._box.y1)


class EdgeMetrics(SubMetrics):
    def __init__(self, edge, metrics):
        self.metrics = metrics
        self.edge = edge

    @property
    def headshapes(self):
        pass

    @property
    def _shaft(self):
        pass

    @property
    def heads(self):
        heads = []
        head1, head2 = self.headshapes

        if head1:
            heads.append(self._head(self.edge.node1, head1))

        if head2:
            heads.append(self._head(self.edge.node2, head2))

        return heads

    def _head(self, node, direct):
        head = []
        cell = self.cellsize
        node = self.node(node)

        if direct == 'up':
            xy = node.bottom
            head.append(XY(xy.x, xy.y + 1))
            head.append(XY(xy.x - cell // 2, xy.y + cell))
            head.append(XY(xy.x, xy.y + cell * 2))
            head.append(XY(xy.x + cell // 2, xy.y + cell))
            head.append(XY(xy.x, xy.y + 1))
        elif direct == 'down':
            xy = node.top
            head.append(XY(xy.x, xy.y - 1))
            head.append(XY(xy.x - cell // 2, xy.y - cell))
            head.append(XY(xy.x, xy.y - cell * 2))
            head.append(XY(xy.x + cell // 2, xy.y - cell))
            head.append(XY(xy.x, xy.y - 1))
        elif direct == 'right':
            xy = node.left
            head.append(XY(xy.x - 1, xy.y))
            head.append(XY(xy.x - cell, xy.y - cell // 2))
            head.append(XY(xy.x - cell * 2, xy.y))
            head.append(XY(xy.x - cell, xy.y + cell // 2))
            head.append(XY(xy.x - 1, xy.y))
        elif direct == 'left':
            xy = node.right
            head.append(XY(xy.x + 1, xy.y))
            head.append(XY(xy.x + cell, xy.y - cell // 2))
            head.append(XY(xy.x + cell * 2, xy.y))
            head.append(XY(xy.x + cell, xy.y + cell // 2))
            head.append(XY(xy.x + 1, xy.y))
        elif direct == 'rup':
            xy = node.bottom
            head.append(XY(xy.x, xy.y + cell))
            head.append(XY(xy.x - cell, xy.y + 1))
            head.append(XY(xy.x, xy.y + 1 * 2))
            head.append(XY(xy.x + cell, xy.y + 1))
            head.append(XY(xy.x, xy.y + cell))
        elif direct == 'rdown':
            xy = node.top
            head.append(XY(xy.x, xy.y - cell))
            head.append(XY(xy.x - cell, xy.y - 1))
            head.append(XY(xy.x, xy.y - 1 * 2))
            head.append(XY(xy.x + cell, xy.y - 1))
            head.append(XY(xy.x, xy.y - cell))
        elif direct == 'rright':
            xy = node.left
            head.append(XY(xy.x - cell, xy.y))
            head.append(XY(xy.x - 1, xy.y - cell))
            head.append(XY(xy.x - 1 * 2, xy.y))
            head.append(XY(xy.x - 1, xy.y + cell))
            head.append(XY(xy.x - cell, xy.y))
        elif direct == 'rleft':
            xy = node.right
            head.append(XY(xy.x + cell, xy.y))
            head.append(XY(xy.x + 1, xy.y - cell))
            head.append(XY(xy.x + 1 * 2, xy.y))
            head.append(XY(xy.x + 1, xy.y + cell))
            head.append(XY(xy.x + cell, xy.y))

        if self.edge.hstyle not in ('composition', 'aggregation'):
            head.pop(2)

        return head

    @property
    def shaft(self):
        cell = self.cellsize
        lines = self._shaft
        head1, head2 = self.headshapes

        if head1:
            pt = lines.polylines[0].pop(0)
            if head1 == 'up':
                lines.polylines[0].insert(0, XY(pt.x, pt.y + cell))
            elif head1 == 'right':
                lines.polylines[0].insert(0, XY(pt.x - cell, pt.y))
            elif head1 == 'left':
                lines.polylines[0].insert(0, XY(pt.x + cell, pt.y))
            elif head1 == 'down':
                lines.polylines[0].insert(0, XY(pt.x, pt.y - cell))
            elif head1 == 'rup':
                lines.polylines[0].insert(0, XY(pt.x, pt.y + cell))
            elif head1 == 'rright':
                lines.polylines[0].insert(0, XY(pt.x - cell, pt.y))
            elif head1 == 'rleft':
                lines.polylines[0].insert(0, XY(pt.x + cell, pt.y))
            elif head1 == 'rdown':
                lines.polylines[0].insert(0, XY(pt.x, pt.y - cell))

        if head2:
            pt = lines.polylines[-1].pop()
            if head2 == 'up':
                lines.polylines[-1].append(XY(pt.x, pt.y + cell))
            elif head2 == 'right':
                lines.polylines[-1].append(XY(pt.x - cell, pt.y))
            elif head2 == 'left':
                lines.polylines[-1].append(XY(pt.x + cell, pt.y))
            elif head2 == 'down':
                lines.polylines[-1].append(XY(pt.x, pt.y - cell))
            elif head2 == 'rup':
                lines.polylines[-1].append(XY(pt.x, pt.y + cell))
            elif head2 == 'rright':
                lines.polylines[-1].append(XY(pt.x - cell, pt.y))
            elif head2 == 'rleft':
                lines.polylines[-1].append(XY(pt.x + cell, pt.y))
            elif head2 == 'rdown':
                lines.polylines[-1].append(XY(pt.x, pt.y - cell))

        return lines

    @property
    def labelbox(self):
        pass


class LandscapeEdgeMetrics(EdgeMetrics):
    @property
    def headshapes(self):
        heads = []
        _dir = self.edge.direction

        if self.edge.dir in ('back', 'both'):
            if _dir in ('left-up', 'left', 'same',
                        'right-up', 'right', 'right-down'):
                heads.append('left')
            elif _dir == 'up':
                if self.edge.skipped:
                    heads.append('left')
                else:
                    heads.append('down')
            elif _dir in ('left-down', 'down'):
                if self.edge.skipped:
                    heads.append('left')
                else:
                    heads.append('up')

            if self.edge.hstyle in ('manyone', 'manymany'):
                heads[-1] = 'r' + heads[-1]
        else:
            heads.append(None)

        if self.edge.dir in ('forward', 'both'):
            if _dir in ('right-up', 'right', 'right-down'):
                heads.append('right')
            elif _dir == 'up':
                heads.append('up')
            elif _dir in ('left-up', 'left', 'left-down', 'down', 'same'):
                heads.append('down')

            if self.edge.hstyle in ('onemany', 'manymany'):
                heads[-1] = 'r' + heads[-1]
        else:
            heads.append(None)

        return heads

    @property
    def _shaft(self):
        span = XY(self.span_width, self.span_height)
        _dir = self.edge.direction

        node1 = self.node(self.edge.node1)
        cell1 = self.cell(self.edge.node1, use_padding=False)
        node2 = self.node(self.edge.node2)
        cell2 = self.cell(self.edge.node2, use_padding=False)

        shaft = EdgeLines()
        if _dir == 'right':
            shaft.moveTo(node1.right)

            if self.edge.skipped:
                shaft.lineTo(cell1.right.x + span.x // 2, cell1.right.y)
                shaft.lineTo(cell1.right.x + span.x // 2,
                             cell1.bottomright.y + span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4,
                             cell2.bottomright.y + span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4, cell2.left.y)

            shaft.lineTo(node2.left)

        elif _dir == 'right-up':
            shaft.moveTo(node1.right)

            if self.edge.skipped:
                shaft.lineTo(cell1.right.x + span.x // 2, cell1.right.y)
                shaft.lineTo(cell1.right.x + span.x // 2,
                             cell2.bottomleft.y + span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4,
                             cell2.bottomleft.y + span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4, cell2.left.y)
            else:
                shaft.lineTo(cell2.left.x - span.x // 4, cell1.right.y)
                shaft.lineTo(cell2.left.x - span.x // 4, cell2.left.y)

            shaft.lineTo(node2.left)

        elif _dir == 'right-down':
            shaft.moveTo(node1.right)
            shaft.lineTo(cell1.right.x + span.x // 2, cell1.right.y)

            if self.edge.skipped:
                shaft.lineTo(cell1.right.x + span.x // 2,
                             cell2.topleft.y - span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4,
                             cell2.topleft.y - span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4, cell2.left.y)
            else:
                shaft.lineTo(cell1.right.x + span.x // 2, cell2.left.y)

            shaft.lineTo(node2.left)

        elif _dir == 'up':
            if self.edge.skipped:
                shaft.moveTo(node1.right)
                shaft.lineTo(cell1.right.x + span.x // 4, cell1.right.y)
                shaft.lineTo(cell1.right.x + span.x // 4,
                             cell2.bottom.y + span.y // 2)
                shaft.lineTo(cell2.bottom.x, cell2.bottom.y + span.y // 2)
            else:
                shaft.moveTo(node1.top)

            shaft.lineTo(node2.bottom)

        elif _dir in ('left-up', 'left', 'same'):
            shaft.moveTo(node1.right)
            shaft.lineTo(cell1.right.x + span.x // 4, cell1.right.y)
            shaft.lineTo(cell1.right.x + span.x // 4,
                         cell2.top.y - span.y // 2 + span.y // 8)
            shaft.lineTo(cell2.top.x,
                         cell2.top.y - span.y // 2 + span.y // 8)
            shaft.lineTo(node2.top)

        elif _dir == 'left-down':
            if self.edge.skipped:
                shaft.moveTo(node1.right)
                shaft.lineTo(cell1.right.x + span.x // 2, cell1.right.y)
                shaft.lineTo(cell1.right.x + span.x // 2,
                             cell2.top.y - span.y // 2)
                shaft.lineTo(cell2.top.x, cell2.top.y - span.y // 2)
            else:
                shaft.moveTo(node1.bottom)
                shaft.lineTo(cell1.bottom.x,
                             cell2.top.y - span.y // 2)
                shaft.lineTo(cell2.top.x, cell2.top.y - span.y // 2)

            shaft.lineTo(node2.top)

        elif _dir == 'down':
            if self.edge.skipped:
                shaft.moveTo(node1.right)
                shaft.lineTo(cell1.right.x + span.x // 2, cell1.right.y)
                shaft.lineTo(cell1.right.x + span.x // 2,
                             cell2.top.y - span.y // 2 + span.y // 8)
                shaft.lineTo(cell2.top.x,
                             cell2.top.y - span.y // 2 + span.y // 8)
            else:
                shaft.moveTo(node1.bottom)

            shaft.lineTo(node2.top)

        return shaft

    @property
    def labelbox(self):
        span = XY(self.span_width, self.span_height)
        node = XY(self.node_width, self.node_height)

        _dir = self.edge.direction
        node1 = self.cell(self.edge.node1, use_padding=False)
        node2 = self.cell(self.edge.node2, use_padding=False)

        if _dir == 'right':
            if self.edge.skipped:
                box = Box(node1.bottomright.x + span.x,
                          node1.bottomright.y,
                          node2.bottomleft.x - span.x,
                          node2.bottomleft.y + span.y // 2)
            else:
                box = Box(node1.topright.x, node1.topright.y - span.y // 8,
                          node2.left.x, node2.left.y - span.y // 8)

        elif _dir == 'right-up':
            box = Box(node2.left.x - span.x, node1.top.y - node.y // 2,
                      node2.bottomleft.x, node1.top.y)

        elif _dir == 'right-down':
            box = Box(node1.right.x, node2.topleft.y - span.y // 8,
                      node1.right.x + span.x, node2.left.y - span.y // 8)

        elif _dir in ('up', 'left-up', 'left', 'same'):
            if self.edge.node2.xy.y < self.edge.node1.xy.y:
                box = Box(node1.topright.x - span.x // 2 + span.x // 4,
                          node1.topright.y - span.y // 2,
                          node1.topright.x + span.x // 2 + span.x // 4,
                          node1.topright.y)
            else:
                box = Box(node1.top.x + span.x // 4,
                          node1.top.y - span.y,
                          node1.topright.x + span.x // 4,
                          node1.topright.y - span.y // 2)

        elif _dir in ('left-down', 'down'):
            box = Box(node2.top.x + span.x // 4,
                      node2.top.y - span.y,
                      node2.topright.x + span.x // 4,
                      node2.topright.y - span.y // 2)

        # shrink box
        box = Box(box[0] + span.x // 8, box[1],
                  box[2] - span.x // 8, box[3])

        return box


class PortraitEdgeMetrics(EdgeMetrics):
    @property
    def headshapes(self):
        heads = []
        _dir = self.edge.direction

        if self.edge.dir in ('back', 'both'):
            if _dir == 'right':
                if self.edge.skipped:
                    heads.append('up')
                else:
                    heads.append('left')
            elif _dir in ('up', 'right-up', 'same'):
                heads.append('up')
            elif _dir in ('left-up', 'left'):
                heads.append('left')
            elif _dir in ('left-down', 'down', 'right-down'):
                if self.edge.skipped:
                    heads.append('left')
                else:
                    heads.append('up')

            if self.edge.hstyle in ('manyone', 'manymany'):
                heads[-1] = 'r' + heads[-1]
        else:
            heads.append(None)

        if self.edge.dir in ('forward', 'both'):
            if _dir == 'right':
                if self.edge.skipped:
                    heads.append('down')
                else:
                    heads.append('right')
            elif _dir in ('up', 'right-up', 'same'):
                heads.append('down')
            elif _dir in ('left-up', 'left',
                          'left-down', 'down', 'right-down'):
                heads.append('down')

            if self.edge.hstyle in ('onemany', 'manymany'):
                heads[-1] = 'r' + heads[-1]
        else:
            heads.append(None)

        return heads

    @property
    def _shaft(self):
        span = XY(self.span_width, self.span_height)
        _dir = self.edge.direction

        node1 = self.node(self.edge.node1)
        cell1 = self.cell(self.edge.node1, use_padding=False)
        node2 = self.node(self.edge.node2)
        cell2 = self.cell(self.edge.node2, use_padding=False)

        shaft = EdgeLines()
        if _dir in ('up', 'right-up', 'same', 'right'):
            if _dir == 'right' and not self.edge.skipped:
                shaft.moveTo(node1.right)
                shaft.lineTo(node2.left)
            else:
                shaft.moveTo(node1.bottom)
                shaft.lineTo(cell1.bottom.x, cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.right.x + span.x // 4,
                             cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.right.x + span.x // 4,
                             cell2.top.y - span.y // 2 + span.y // 8)
                shaft.lineTo(cell2.top.x,
                             cell2.top.y - span.y // 2 + span.y // 8)
                shaft.lineTo(node2.top)

        elif _dir == 'right-down':
            shaft.moveTo(node1.bottom)
            shaft.lineTo(cell1.bottom.x, cell1.bottom.y + span.y // 2)

            if self.edge.skipped:
                shaft.lineTo(cell2.left.x - span.x // 2,
                             cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.topleft.x - span.x // 2,
                             cell2.topleft.y - span.y // 2)
                shaft.lineTo(cell2.top.x, cell2.top.y - span.y // 2)
            else:
                shaft.lineTo(cell2.top.x, cell1.bottom.y + span.y // 2)

            shaft.lineTo(node2.top)

        elif _dir in ('left-up', 'left', 'same'):
            shaft.moveTo(node1.right)
            shaft.lineTo(cell1.right.x + span.x // 4, cell1.right.y)
            shaft.lineTo(cell1.right.x + span.x // 4,
                         cell2.top.y - span.y // 2 + span.y // 8)
            shaft.lineTo(cell2.top.x,
                         cell2.top.y - span.y // 2 + span.y // 8)
            shaft.lineTo(node2.top)

        elif _dir == 'left-down':
            shaft.moveTo(node1.bottom)

            if self.edge.skipped:
                shaft.lineTo(cell1.bottom.x, cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.right.x + span.x // 2,
                             cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.right.x + span.x // 2,
                             cell2.top.y - span.y // 2)
            else:
                shaft.lineTo(cell1.bottom.x, cell2.top.y - span.y // 2)

            shaft.lineTo(cell2.top.x, cell2.top.y - span.y // 2)
            shaft.lineTo(node2.top)

        elif _dir == 'down':
            shaft.moveTo(node1.bottom)

            if self.edge.skipped:
                shaft.lineTo(cell1.bottom.x, cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell1.right.x + span.x // 2,
                             cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.right.x + span.x // 2,
                             cell2.top.y - span.y // 2)
                shaft.lineTo(cell2.top.x, cell2.top.y - span.y // 2)

            shaft.lineTo(node2.top)

        return shaft

    @property
    def labelbox(self):
        span = XY(self.span_width, self.span_height)

        _dir = self.edge.direction
        node1 = self.cell(self.edge.node1, use_padding=False)
        node2 = self.cell(self.edge.node2, use_padding=False)

        if _dir == 'right':
            if self.edge.skipped:
                box = Box(node1.bottomright.x + span.x,
                          node1.bottomright.y,
                          node2.bottomleft.x - span.x,
                          node2.bottomleft.y + span.y // 2)
            else:
                box = Box(node1.topright.x, node1.topright.y - span.y // 8,
                          node2.left.x, node2.left.y - span.y // 8)

        elif _dir == 'right-up':
            box = Box(node2.left.x - span.x, node2.left.y,
                      node2.bottomleft.x, node2.bottomleft.y)

        elif _dir == 'right-down':
            box = Box(node2.topleft.x, node2.topleft.y - span.y // 2,
                      node2.top.x, node2.top.y)

        elif _dir in ('up', 'left-up', 'left', 'same'):
            if self.edge.node2.xy.y < self.edge.node1.xy.y:
                box = Box(node1.topright.x - span.x // 2 + span.x // 4,
                          node1.topright.y - span.y // 2,
                          node1.topright.x + span.x // 2 + span.x // 4,
                          node1.topright.y)
            else:
                box = Box(node1.top.x + span.x // 4,
                          node1.top.y - span.y,
                          node1.topright.x + span.x // 4,
                          node1.topright.y - span.y // 2)

        elif _dir == 'down':
            box = Box(node2.top.x + span.x // 4,
                      node2.top.y - span.y // 2,
                      node2.topright.x + span.x // 4,
                      node2.topright.y)

        elif _dir == 'left-down':
            box = Box(node1.bottomleft.x, node1.bottomleft.y,
                      node1.bottom.x, node1.bottom.y + span.y // 2)

        # shrink box
        box = Box(box[0] + span.x // 8, box[1],
                  box[2] - span.x // 8, box[3])

        return box


class FlowchartLandscapeEdgeMetrics(LandscapeEdgeMetrics):
    @property
    def headshapes(self):
        heads = []

        if self.edge.direction == 'right-down':
            if self.edge.dir in ('back', 'both'):
                if self.edge.hstyle in ('manyone', 'manymany'):
                    heads.append('rup')
                else:
                    heads.append('up')
            else:
                heads.append(None)

            if self.edge.dir in ('forward', 'both'):
                if self.edge.hstyle in ('onemany', 'manymany'):
                    heads.append('rright')
                else:
                    heads.append('right')
            else:
                heads.append(None)
        else:
            heads = super(FlowchartLandscapeEdgeMetrics, self).headshapes

        return heads

    @property
    def _shaft(self):
        if self.edge.direction == 'right-down':
            span = XY(self.span_width, self.span_height)
            node1 = self.node(self.edge.node1)
            cell1 = self.cell(self.edge.node1, use_padding=False)
            node2 = self.node(self.edge.node2)
            cell2 = self.cell(self.edge.node2, use_padding=False)

            shaft = EdgeLines()
            shaft.moveTo(node1.bottom)

            if self.edge.skipped:
                shaft.lineTo(cell1.bottom.x, cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4,
                             cell1.bottom.y + span.y // 2)
                shaft.lineTo(cell2.left.x - span.x // 4, cell2.left.y)
            else:
                shaft.lineTo(cell1.bottom.x, cell2.left.y)

            shaft.lineTo(node2.left)
        else:
            shaft = super(FlowchartLandscapeEdgeMetrics, self)._shaft

        return shaft

    @property
    def labelbox(self):
        _dir = self.edge.direction
        if _dir == 'right':
            span = XY(self.span_width, self.span_height)
            cell1 = self.cell(self.edge.node1, use_padding=False)
            cell2 = self.cell(self.edge.node2, use_padding=False)

            if self.edge.skipped:
                box = Box(cell1.bottom.x, cell1.bottom.y,
                          cell1.bottomright.x,
                          cell1.bottomright.y + span.y // 2)
            else:
                box = Box(cell1.bottom.x, cell2.left.y - span.y // 2,
                          cell1.bottom.x, cell2.left.y)
        else:
            box = super(FlowchartLandscapeEdgeMetrics, self).labelbox

        return box


class FlowchartPortraitEdgeMetrics(PortraitEdgeMetrics):
    @property
    def headshapes(self):
        heads = []

        if self.edge.direction == 'right-down':
            if self.edge.dir in ('back', 'both'):
                if self.edge.hstyle in ('manyone', 'manymany'):
                    heads.append('left')
                else:
                    heads.append('left')
            else:
                heads.append(None)

            if self.edge.dir in ('forward', 'both'):
                if self.edge.dir in ('onemany', 'manymany'):
                    heads.append('rdown')
                else:
                    heads.append('down')
            else:
                heads.append(None)
        else:
            heads = super(FlowchartPortraitEdgeMetrics, self).headshapes

        return heads

    @property
    def _shaft(self):
        if self.edge.direction == 'right-down':
            span = XY(self.span_width, self.span_height)
            node1 = self.node(self.edge.node1)
            cell1 = self.cell(self.edge.node1, use_padding=False)
            node2 = self.node(self.edge.node2)
            cell2 = self.cell(self.edge.node2, use_padding=False)

            shaft = EdgeLines()
            shaft.moveTo(node1.right)

            if self.edge.skipped:
                shaft.lineTo(cell1.right.x + span.x * 3 // 4,
                             cell1.right.y)
                shaft.lineTo(cell1.right.x + span.x * 3 // 4,
                             cell2.topleft.y - span.y // 2)
                shaft.lineTo(cell2.top.x, cell2.top.y - span.y // 2)
            else:
                shaft.lineTo(cell2.top.x, cell1.right.y)

            shaft.lineTo(node2.top)
        else:
            shaft = super(FlowchartPortraitEdgeMetrics, self)._shaft

        return shaft

    @property
    def labelbox(self):
        _dir = self.edge.direction
        span = XY(self.span_width, self.span_height)
        cell1 = self.cell(self.edge.node1, use_padding=False)
        cell2 = self.cell(self.edge.node2, use_padding=False)

        if _dir == 'down':
            box = Box(cell2.topleft.x, cell2.top.y - span.y // 2,
                      cell2.top.x, cell2.top.y)
        elif _dir == 'right':
            if self.edge.skipped:
                box = Box(cell1.bottom.x, cell1.bottom.y,
                          cell1.bottomright.x,
                          cell1.bottomright.y + span.y // 2)
            else:
                box = Box(cell1.bottom.x, cell2.left.y - span.y // 2,
                          cell1.bottom.x, cell2.left.y)
        else:
            box = super(FlowchartPortraitEdgeMetrics, self).labelbox

        return box
