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

from collections import defaultdict

from blockdiag import imagedraw, noderenderer
from blockdiag.metrics import AutoScaler, DiagramMetrics


class DiagramDraw(object):
    shadow_colors = defaultdict(lambda: (0, 0, 0))
    shadow_colors['PNG'] = (64, 64, 64)
    shadow_colors['PDF'] = (144, 144, 144)

    def __init__(self, _format, diagram, filename=None, **kwargs):
        self.format = _format.upper()
        self.diagram = diagram
        self.fill = kwargs.get('fill', (0, 0, 0))
        self.badgeFill = kwargs.get('badgeFill', 'pink')
        self.filename = filename
        self.shadow = self.shadow_colors[self.format.upper()]

        if self.format == 'PNG' and kwargs.get('antialias'):
            self.scale_ratio = 2
        else:
            self.scale_ratio = 1

        self.drawer = imagedraw.create(self.format, self.filename,
                                       filters=['linejump'],
                                       scale_ratio=self.scale_ratio,
                                       **kwargs)

        self.metrics = self.create_metrics(kwargs.get('basediagram', diagram),
                                           drawer=self.drawer,
                                           fontmap=kwargs.get('fontmap'))
        if self.scale_ratio == 2:
            self.metrics = AutoScaler(self.metrics,
                                      scale_ratio=self.scale_ratio)

        self.drawer.set_canvas_size(self.pagesize())
        self.drawer.set_options(jump_radius=self.metrics.cellsize / 2)

    def create_metrics(self, *args, **kwargs):
        return DiagramMetrics(*args, **kwargs)

    @property
    def nodes(self):
        for node in self.diagram.traverse_nodes():
            if node.drawable:
                yield node

    @property
    def groups(self):
        for group in self.diagram.traverse_groups(preorder=True):
            if not group.drawable:
                yield group

    @property
    def edges(self):
        edges = self.diagram.traverse_edges(preorder=True)
        for edge in (e for e in edges if e.style != 'none'):
            yield edge

    def pagesize(self, scaled=False):
        if scaled:
            metrics = self.metrics
        else:
            metrics = self.metrics.original_metrics

        width = self.diagram.colwidth
        height = self.diagram.colheight
        return metrics.pagesize(width, height)

    def draw(self, **kwargs):
        # switch metrics object during draw backgrounds
        temp, self.metrics = self.metrics, self.metrics.original_metrics
        self._draw_background()
        self.metrics = temp

        if self.scale_ratio > 1:
            pagesize = self.pagesize(scaled=True)
            self.drawer.resizeCanvas(pagesize)

        self._draw_elements(**kwargs)

    def _draw_background(self):
        # Draw node groups.
        for group in self.groups:
            if group.shape == 'box':
                box = self.metrics.group(group).marginbox
                if group.href and self.format == 'SVG':
                    drawer = self.drawer.anchor(group.href)
                else:
                    drawer = self.drawer

                drawer.rectangle(box, fill=group.color, filter='blur')

        # Drop node shadows.
        for node in self.nodes:
            if node.color != 'none' and self.diagram.shadow_style != 'none':
                r = noderenderer.get(node.shape)

                shape = r(node, self.metrics)
                if node.href and self.format == 'SVG':
                    drawer = self.drawer.anchor(node.href)
                else:
                    drawer = self.drawer

                shape.render(drawer, self.format,
                             fill=self.shadow, shadow=True,
                             style=self.diagram.shadow_style)

    def _draw_elements(self, **kwargs):
        for node in self.nodes:
            self.node(node, **kwargs)

        for edge in self.edges:
            self.edge(edge)

        for edge in self.edges:
            self.edge_label(edge)

        for group in self.groups:
            if group.shape == 'line':
                box = self.metrics.group(group).marginbox
                self.drawer.rectangle(box, fill='none', outline=group.color,
                                      style=group.style, thick=group.thick)

        for node in self.groups:
            self.group_label(node, **kwargs)

    def node(self, node, **kwargs):
        r = noderenderer.get(node.shape)
        shape = r(node, self.metrics)
        if node.href and self.format == 'SVG':
            drawer = self.drawer.anchor(node.href)
        else:
            drawer = self.drawer

        shape.render(drawer, self.format, fill=self.fill,
                     badgeFill=self.badgeFill)

    def group_label(self, group):
        m = self.metrics.group(group)
        font = self.metrics.font_for(group)

        if group.label and not group.separated:
            self.drawer.textarea(m.grouplabelbox, group.label, font=font,
                                 fill=group.textcolor)
        elif group.label:
            self.drawer.textarea(m.corebox, group.label, font=font,
                                 fill=group.textcolor)

    def edge(self, edge):
        metrics = self.metrics.edge(edge)

        for line in metrics.shaft.polylines:
            self.drawer.line(line, fill=edge.color, thick=edge.thick,
                             style=edge.style, jump=True)

        for head in metrics.heads:
            if edge.hstyle in ('generalization', 'aggregation'):
                self.drawer.polygon(head, outline=edge.color, fill='white')
            else:
                self.drawer.polygon(head, outline=edge.color, fill=edge.color)

    def edge_label(self, edge):
        if edge.label:
            metrics = self.metrics.edge(edge)

            font = self.metrics.font_for(edge)
            self.drawer.textarea(metrics.labelbox, edge.label, font=font,
                                 fill=edge.textcolor, outline=self.fill)

    def save(self, size=None):
        return self.drawer.save(self.filename, size, self.format)
