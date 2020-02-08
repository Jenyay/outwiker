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

from blockdiag import parser
from blockdiag.elements import Diagram, DiagramEdge, DiagramNode, NodeGroup
from blockdiag.plugins import fire_node_event
from blockdiag.utils import XY, unquote
from blockdiag.utils.compat import cmp_to_key


class DiagramTreeBuilder:
    def build(self, tree, config):
        self.config = config
        self.diagram = Diagram()
        self.instantiate(self.diagram, tree)
        for subgroup in self.diagram.traverse_groups():
            if len(subgroup.nodes) == 0:
                subgroup.group.nodes.remove(subgroup)

        self.bind_edges(self.diagram)
        self.fire_node_event('build_finished')
        return self.diagram

    def fire_node_event(self, event_type):
        for node in self.diagram.nodes:
            if node.drawable:
                fire_node_event(node, event_type)

    def is_related_group(self, group1, group2):
        if group1.is_parent(group2) or group2.is_parent(group1):
            return True
        else:
            return False

    def belong_to(self, node, group):
        if node.group and node.group.level > group.level:
            override = False
        else:
            override = True

        if node.group and node.group != group and override:
            if not self.is_related_group(node.group, group):
                msg = "could not belong to two groups: %s" % node.id
                raise RuntimeError(msg)

            old_group = node.group

            parent = group.parent(old_group.level + 1)
            if parent:
                if parent in old_group.nodes:
                    old_group.nodes.remove(parent)

                index = old_group.nodes.index(node)
                old_group.nodes.insert(index + 1, parent)

            old_group.nodes.remove(node)
            node.group = None

        if node.group is None:
            node.group = group

            if node not in group.nodes:
                group.nodes.append(node)

    def instantiate(self, group, tree):
        for stmt in tree.stmts:
            # Translate Node having group attribute to Group
            if isinstance(stmt, parser.Node):
                group_attr = [a for a in stmt.attrs if a.name == 'group']
                if group_attr:
                    group_id = group_attr[-1]
                    stmt.attrs.remove(group_id)

                    if group_id.value != group.id:
                        stmt = parser.Group(group_id.value, [stmt])

            # Instantiate statements
            if isinstance(stmt, parser.Node):
                node = DiagramNode.get(stmt.id)
                node.set_attributes(stmt.attrs)
                self.belong_to(node, group)

            elif isinstance(stmt, parser.Edge):
                from_nodes = [DiagramNode.get(n) for n in stmt.from_nodes]
                to_nodes = [DiagramNode.get(n) for n in stmt.to_nodes]

                for node in from_nodes + to_nodes:
                    self.belong_to(node, group)

                for node1 in from_nodes:
                    for node2 in to_nodes:
                        edge = DiagramEdge.get(node1, node2)
                        edge.set_dir(stmt.edge_type)
                        edge.set_attributes(stmt.attrs)

            elif isinstance(stmt, parser.Group):
                subgroup = NodeGroup.get(stmt.id)
                subgroup.level = group.level + 1
                self.belong_to(subgroup, group)
                self.instantiate(subgroup, stmt)

            elif isinstance(stmt, parser.Attr):
                group.set_attribute(stmt)

            elif isinstance(stmt, parser.Extension):
                if stmt.type == 'class':
                    name = unquote(stmt.name)
                    Diagram.classes[name] = stmt
                elif stmt.type == 'plugin':
                    self.diagram.set_plugin(stmt.name, stmt.attrs,
                                            config=self.config)

            elif isinstance(stmt, parser.Statements):
                self.instantiate(group, stmt)

        group.update_order()
        return group

    def bind_edges(self, group):
        for node in group.nodes:
            if isinstance(node, DiagramNode):
                group.edges += DiagramEdge.find(node)
            else:
                self.bind_edges(node)


class DiagramLayoutManager:
    def __init__(self, diagram):
        self.diagram = diagram

        self.circulars = []
        self.heightRefs = []
        self.coordinates = []

    def run(self):
        if isinstance(self.diagram, Diagram):
            for group in self.diagram.traverse_groups():
                self.__class__(group).run()

        self.edges = DiagramEdge.find_by_level(self.diagram.level)
        self.do_layout()
        self.diagram.fixiate()

        if self.diagram.orientation == 'portrait':
            self.rotate_diagram()

    def rotate_diagram(self):
        for node in self.diagram.traverse_nodes():
            node.xy = XY(node.xy.y, node.xy.x)
            node.colwidth, node.colheight = (node.colheight, node.colwidth)

            if isinstance(node, NodeGroup):
                if node.orientation == 'portrait':
                    node.orientation = 'landscape'
                else:
                    node.orientation = 'portrait'

        xy = (self.diagram.colheight, self.diagram.colwidth)
        self.diagram.colwidth, self.diagram.colheight = xy

    def do_layout(self):
        self.detect_circulars()

        self.set_node_xpos()
        self.adjust_node_order()

        height = 0
        for node in self.diagram.nodes:
            if node.xy.x == 0:
                self.set_node_ypos(node, height)
                height = max(xy.y for xy in self.coordinates) + 1

    def get_related_nodes(self, node, parent=False, child=False):
        uniq = {}
        for edge in self.edges:
            if edge.folded:
                continue

            if parent and edge.node2 == node:
                uniq[edge.node1] = 1
            elif child and edge.node1 == node:
                uniq[edge.node2] = 1

        related = []
        for uniq_node in uniq.keys():
            if uniq_node == node:
                pass
            elif uniq_node.group != node.group:
                pass
            else:
                related.append(uniq_node)

        related.sort(key=lambda x: x.order)
        return related

    def get_parent_nodes(self, node):
        return self.get_related_nodes(node, parent=True)

    def get_child_nodes(self, node):
        return self.get_related_nodes(node, child=True)

    def detect_circulars(self):
        for node in self.diagram.nodes:
            if not [x for x in self.circulars if node in x]:
                self.detect_circulars_sub(node, [node])

        # remove part of other circular
        for c1 in self.circulars[:]:
            for c2 in self.circulars:
                intersect = set(c1) & set(c2)

                if c1 != c2 and set(c1) == intersect:
                    if c1 in self.circulars:
                        self.circulars.remove(c1)
                    break

                if c1 != c2 and intersect:
                    if c1 in self.circulars:
                        self.circulars.remove(c1)
                    self.circulars.remove(c2)
                    self.circulars.append(c1 + c2)
                    break

    def detect_circulars_sub(self, node, parents):
        for child in self.get_child_nodes(node):
            if child in parents:
                i = parents.index(child)
                if parents[i:] not in self.circulars:
                    self.circulars.append(parents[i:])
            else:
                self.detect_circulars_sub(child, parents + [child])

    def is_circular_ref(self, node1, node2):
        for circular in self.circulars:
            if node1 in circular and node2 in circular:
                parents = []
                for node in circular:
                    for parent in self.get_parent_nodes(node):
                        if parent not in circular:
                            parents.append(parent)

                for parent in sorted(parents, key=lambda x: x.order):
                    children = self.get_child_nodes(parent)
                    if node1 in children and node2 in children:
                        if circular.index(node1) > circular.index(node2):
                            return True
                    elif node2 in children:
                        return True
                    elif node1 in children:
                        return False
                else:
                    if circular.index(node1) > circular.index(node2):
                        return True

        return False

    def set_node_xpos(self, depth=0):
        for node in self.diagram.nodes:
            if node.xy.x != depth:
                continue

            for child in self.get_child_nodes(node):
                if self.is_circular_ref(node, child):
                    pass
                elif node == child:
                    pass
                elif child.xy.x > node.xy.x + node.colwidth:
                    pass
                else:
                    child.xy = XY(node.xy.x + node.colwidth, 0)

        depther_node = [x for x in self.diagram.nodes if x.xy.x > depth]
        if len(depther_node) > 0:
            self.set_node_xpos(depth + 1)

    def adjust_node_order(self):
        for node in list(self.diagram.nodes):
            parents = self.get_parent_nodes(node)
            if len(set(parents)) > 1:
                for i in range(1, len(parents)):
                    node1 = parents[i - 1]
                    node2 = parents[i]

                    if node1.xy.x == node2.xy.x:
                        idx1 = self.diagram.nodes.index(node1)
                        idx2 = self.diagram.nodes.index(node2)

                        if idx1 < idx2:
                            self.diagram.nodes.remove(node2)
                            self.diagram.nodes.insert(idx1 + 1, node2)
                        else:
                            self.diagram.nodes.remove(node1)
                            self.diagram.nodes.insert(idx2 + 1, node1)

            children = self.get_child_nodes(node)
            if len(set(children)) > 1:
                for i in range(1, len(children)):
                    node1 = children[i - 1]
                    node2 = children[i]

                    idx1 = self.diagram.nodes.index(node1)
                    idx2 = self.diagram.nodes.index(node2)

                    if node1.xy.x == node2.xy.x:
                        if idx1 < idx2:
                            self.diagram.nodes.remove(node2)
                            self.diagram.nodes.insert(idx1 + 1, node2)
                        else:
                            self.diagram.nodes.remove(node1)
                            self.diagram.nodes.insert(idx2 + 1, node1)
                    elif self.is_circular_ref(node1, node2):
                        pass
                    else:
                        if node1.xy.x < node2.xy.x:
                            self.diagram.nodes.remove(node2)
                            self.diagram.nodes.insert(idx1 + 1, node2)
                        else:
                            self.diagram.nodes.remove(node1)
                            self.diagram.nodes.insert(idx2 + 1, node1)

            if isinstance(node, NodeGroup):
                children = self.get_child_nodes(node)
                if len(set(children)) > 1:
                    while True:
                        exchange = 0

                        for i in range(1, len(children)):
                            node1 = children[i - 1]
                            node2 = children[i]

                            idx1 = self.diagram.nodes.index(node1)
                            idx2 = self.diagram.nodes.index(node2)
                            ret = self.compare_child_node_order(node,
                                                                node1, node2)

                            if ret > 0 and idx1 < idx2:
                                self.diagram.nodes.remove(node1)
                                self.diagram.nodes.insert(idx2 + 1, node1)
                                exchange += 1

                        if exchange == 0:
                            break

        self.diagram.update_order()

    def compare_child_node_order(self, parent, node1, node2):
        def compare(x, y):
            x = x.duplicate()
            y = y.duplicate()
            while x.node1 == y.node1 and x.node1.group is not None:
                x.node1 = x.node1.group
                y.node1 = y.node1.group

            # cmp x.node1.order and y.node1.order
            if x.node1.order < y.node1.order:
                return -1
            elif x.node1.order == y.node1.order:
                return 0
            else:
                return 1

        edges = (DiagramEdge.find(parent, node1) +
                 DiagramEdge.find(parent, node2))
        edges.sort(key=cmp_to_key(compare))
        if len(edges) == 0:
            return 0
        elif edges[0].node2 == node2:
            return 1
        else:
            return -1

    def mark_xy(self, xy, width, height):
        for w in range(width):
            for h in range(height):
                self.coordinates.append(XY(xy.x + w, xy.y + h))

    def set_node_ypos(self, node, height=0):
        for x in range(node.colwidth):
            for y in range(node.colheight):
                xy = XY(node.xy.x + x, height + y)
                if xy in self.coordinates:
                    return False
        node.xy = XY(node.xy.x, height)
        self.mark_xy(node.xy, node.colwidth, node.colheight)

        def cmp(x, y):
            if x.xy.x < y.xy.y:
                return -1
            elif x.xy.x == y.xy.y:
                return 0
            else:
                return 1

        count = 0
        children = self.get_child_nodes(node)
        children.sort(key=cmp_to_key(cmp))

        grandchild = 0
        for child in children:
            if self.get_child_nodes(child):
                grandchild += 1

        prev_child = None
        for child in children:
            if child.id in self.heightRefs:
                pass
            elif node.xy.x >= child.xy.x:
                pass
            else:
                if isinstance(node, NodeGroup):
                    parent_height = self.get_parent_node_ypos(node, child)
                    if parent_height and parent_height > height:
                        height = parent_height

                if (prev_child and grandchild > 1 and
                   (not self.is_rhombus(prev_child, child))):
                    coord = [p.y for p in self.coordinates if p.x > child.xy.x]
                    if coord and max(coord) >= node.xy.y:
                        height = max(coord) + 1

                while True:
                    if self.set_node_ypos(child, height):
                        child.xy = XY(child.xy.x, height)
                        self.mark_xy(child.xy, child.colwidth, child.colheight)
                        self.heightRefs.append(child.id)

                        count += 1
                        break
                    else:
                        if count == 0:
                            return False

                        height += 1

                height += 1
                prev_child = child

        return True

    def is_rhombus(self, node1, node2):
        ret = False
        while True:
            if node1 == node2:
                ret = True
                break

            child1 = self.get_child_nodes(node1)
            child2 = self.get_child_nodes(node2)

            if len(child1) != 1 or len(child2) != 1:
                break
            elif node1.xy.x > child1[0].xy.x or node2.xy.x > child2[0].xy.x:
                break
            else:
                node1 = child1[0]
                node2 = child2[0]

        return ret

    def get_parent_node_ypos(self, parent, child):
        heights = []
        for e in DiagramEdge.find(parent, child):
            y = parent.xy.y

            node = e.node1
            while node != parent:
                y += node.xy.y
                node = node.group

            heights.append(y)

        if heights:
            return min(heights)
        else:
            return None


class EdgeLayoutManager(object):
    def __init__(self, diagram):
        self.diagram = diagram

    @property
    def groups(self):
        if self.diagram.separated:
            seq = self.diagram.nodes
        else:
            seq = self.diagram.traverse_groups(preorder=True)

        for group in seq:
            if not group.drawable:
                yield group

    @property
    def nodes(self):
        if self.diagram.separated:
            seq = self.diagram.nodes
        else:
            seq = self.diagram.traverse_nodes()

        for node in seq:
            if node.drawable:
                yield node

    @property
    def edges(self):
        for edge in (e for e in self.diagram.edges if e.style != 'none'):
            yield edge

        for group in self.groups:
            for edge in (e for e in group.edges if e.style != 'none'):
                yield edge

    def run(self):
        for edge in self.edges:
            _dir = edge.direction

            if edge.node1.group.orientation == 'landscape':
                if _dir == 'right':
                    r = range(edge.node1.xy.x + 1, edge.node2.xy.x)
                    for x in r:
                        xy = (x, edge.node1.xy.y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
                elif _dir == 'right-up':
                    r = range(edge.node1.xy.x + 1, edge.node2.xy.x)
                    for x in r:
                        xy = (x, edge.node1.xy.y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
                elif _dir == 'right-down':
                    if self.diagram.edge_layout == 'flowchart':
                        r = range(edge.node1.xy.y, edge.node2.xy.y)
                        for y in r:
                            xy = (edge.node1.xy.x, y + 1)
                            nodes = [x for x in self.nodes if x.xy == xy]
                            if len(nodes) > 0:
                                edge.skipped = 1

                    r = range(edge.node1.xy.x + 1, edge.node2.xy.x)
                    for x in r:
                        xy = (x, edge.node2.xy.y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
                elif _dir in ('left-down', 'down'):
                    r = range(edge.node1.xy.y + 1, edge.node2.xy.y)
                    for y in r:
                        xy = (edge.node1.xy.x, y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
                elif _dir == 'up':
                    r = range(edge.node2.xy.y + 1, edge.node1.xy.y)
                    for y in r:
                        xy = (edge.node1.xy.x, y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
            else:
                if _dir == 'right':
                    r = range(edge.node1.xy.x + 1, edge.node2.xy.x)
                    for x in r:
                        xy = (x, edge.node1.xy.y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
                elif _dir in ('left-down', 'down'):
                    r = range(edge.node1.xy.y + 1, edge.node2.xy.y)
                    for y in r:
                        xy = (edge.node1.xy.x, y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1
                elif _dir == 'right-down':
                    if self.diagram.edge_layout == 'flowchart':
                        r = range(edge.node1.xy.x, edge.node2.xy.x)
                        for x in r:
                            xy = (x + 1, edge.node1.xy.y)
                            nodes = [x for x in self.nodes if x.xy == xy]
                            if len(nodes) > 0:
                                edge.skipped = 1

                    r = range(edge.node1.xy.y + 1, edge.node2.xy.y)
                    for y in r:
                        xy = (edge.node2.xy.x, y)
                        nodes = [x for x in self.nodes if x.xy == xy]
                        if len(nodes) > 0:
                            edge.skipped = 1


class ScreenNodeBuilder:
    @classmethod
    def build(cls, tree, config=None, layout=True):
        DiagramNode.clear()
        DiagramEdge.clear()
        NodeGroup.clear()
        Diagram.clear()

        return cls(tree, config, layout).run()

    def __init__(self, tree, config, layout):
        self.diagram = DiagramTreeBuilder().build(tree, config)
        self.config = config
        self.layout = layout

    def run(self):
        if self.layout:
            DiagramLayoutManager(self.diagram).run()
            self.diagram.fixiate(True)

        EdgeLayoutManager(self.diagram).run()

        return self.diagram


class SeparateDiagramBuilder(ScreenNodeBuilder):
    @property
    def _groups(self):
        # Store nodes and edges of subgroups
        nodes = {self.diagram: self.diagram.nodes}
        edges = {self.diagram: self.diagram.edges}
        levels = {self.diagram: self.diagram.level}
        for group in self.diagram.traverse_groups():
            nodes[group] = group.nodes
            edges[group] = group.edges
            levels[group] = group.level

        groups = {}
        orders = {}
        for node in self.diagram.traverse_nodes():
            groups[node] = node.group
            orders[node] = node.order

        for group in self.diagram.traverse_groups():
            yield group

            # Restore nodes, groups and edges
            for g in nodes:
                g.nodes = nodes[g]
                g.edges = edges[g]
                g.level = levels[g]

            for n in groups:
                n.group = groups[n]
                n.order = orders[n]
                n.xy = XY(0, 0)
                n.colwidth = 1
                n.colheight = 1
                n.separated = False

            for edge in DiagramEdge.find_all():
                edge.skipped = False
                edge.crosspoints = []

        yield self.diagram

    def _filter_edges(self, edges, parent, level):
        filtered = {}
        for e in edges:
            if e.node1.group.is_parent(parent):
                if e.node1.group.level > level:
                    e = e.duplicate()
                    if isinstance(e.node1, NodeGroup):
                        e.node1 = e.node1.parent(level + 1)
                    else:
                        e.node1 = e.node1.group.parent(level + 1)
            else:
                continue

            if e.node2.group.is_parent(parent):
                if e.node2.group.level > level:
                    e = e.duplicate()
                    if isinstance(e.node2, NodeGroup):
                        e.node2 = e.node2.parent(level + 1)
                    else:
                        e.node2 = e.node2.group.parent(level + 1)
            else:
                continue

            filtered[(e.node1, e.node2)] = e

        return filtered.values()

    def run(self):
        for i, group in enumerate(self._groups):
            base = self.diagram.duplicate()
            base.level = group.level - 1

            # bind edges on base diagram (outer the group)
            edges = (DiagramEdge.find(None, group) +
                     DiagramEdge.find(group, None))
            base.edges = self._filter_edges(edges, self.diagram, group.level)

            # bind edges on target group (inner the group)
            subgroups = group.traverse_groups()
            edges = sum([g.edges for g in subgroups], group.edges)
            group.edges = []
            for e in self._filter_edges(edges, group, group.level):
                if isinstance(e.node1, NodeGroup) and e.node1 == e.node2:
                    pass
                else:
                    group.edges.append(e)

            # clear subgroups in the group
            for g in group.nodes:
                if isinstance(g, NodeGroup):
                    g.nodes = []
                    g.edges = []
                    g.separated = True

            # pick up nodes to base diagram
            nodes1 = [e.node1 for e in DiagramEdge.find(None, group)]
            nodes1.sort(key=lambda x: x.order)
            nodes2 = [e.node2 for e in DiagramEdge.find(group, None)]
            nodes2.sort(key=lambda x: x.order)

            nodes = nodes1 + [group] + nodes2
            for i, n in enumerate(nodes):
                n.order = i
                if n not in base.nodes:
                    base.nodes.append(n)
                    n.group = base

            if isinstance(group, Diagram):
                base = group

            DiagramLayoutManager(base).run()
            base.fixiate(True)
            EdgeLayoutManager(base).run()

            yield base
