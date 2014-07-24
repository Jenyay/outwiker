# -*- coding: utf-8 -*-

from blockdiag.tests.utils import BuilderTestCase


class TestBuilderGroup(BuilderTestCase):
    def test_nested_groups_diagram(self):
        diagram = self.build('nested_groups.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'Z': (0, 2)})

    def test_nested_groups_and_edges_diagram(self):
        diagram = self.build('nested_groups_and_edges.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (2, 0), 'Z': (0, 1)})

    def test_empty_group_diagram(self):
        diagram = self.build('empty_group.diag')
        self.assertNodeXY(diagram, {'Z': (0, 0)})

    def test_empty_nested_group_diagram(self):
        diagram = self.build('empty_nested_group.diag')
        self.assertNodeXY(diagram, {'Z': (0, 0)})

    def test_empty_group_declaration_diagram(self):
        diagram = self.build('empty_group_declaration.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'Z': (0, 1)})

    def test_simple_group_diagram(self):
        diagram = self.build('simple_group.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'Z': (0, 2)})

    def test_group_declare_as_node_attribute_diagram(self):
        diagram = self.build('group_declare_as_node_attribute.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1),
                                    'E': (2, 2), 'Z': (0, 3)})

    def test_group_attribute(self):
        diagram = self.build('group_attribute.diag')
        groups = list(diagram.traverse_groups())
        self.assertEqual(1, len(groups))
        self.assertEqual((255, 0, 0), groups[0].color)
        self.assertEqual('line', groups[0].shape)

    def test_merge_groups_diagram(self):
        diagram = self.build('merge_groups.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (0, 1), 'D': (1, 1),
                                    'Z': (0, 2)})

    def test_node_attribute_and_group_diagram(self):
        diagram = self.build('node_attribute_and_group.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'Z': (0, 1)})
        self.assertNodeLabel(diagram, {'A': 'foo', 'B': 'bar',
                                       'C': 'baz', 'Z': 'Z'})
        self.assertNodeColor(diagram, {'A': (255, 0, 0), 'B': '#888888',
                                       'C': (0, 0, 255), 'Z': (255, 255, 255)})

    def test_group_sibling_diagram(self):
        diagram = self.build('group_sibling.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 2), 'D': (2, 0),
                                    'E': (2, 1), 'F': (2, 2),
                                    'Z': (0, 3)})

    def test_group_order_diagram(self):
        diagram = self.build('group_order.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'Z': (0, 2)})

    def test_group_order2_diagram(self):
        diagram = self.build('group_order2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (2, 1),
                                    'E': (1, 2), 'F': (2, 2),
                                    'Z': (0, 3)})

    def test_group_order3_diagram(self):
        diagram = self.build('group_order3.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1),
                                    'E': (1, 2), 'Z': (0, 3)})

    def test_group_children_height_diagram(self):
        diagram = self.build('group_children_height.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (2, 0), 'F': (2, 2),
                                    'Z': (0, 3)})

    def test_group_children_order_diagram(self):
        diagram = self.build('group_children_order.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (2, 0), 'F': (2, 1),
                                    'G': (2, 2), 'Z': (0, 3)})

    def test_group_children_order2_diagram(self):
        diagram = self.build('group_children_order2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (2, 1), 'F': (2, 0),
                                    'G': (2, 2), 'Z': (0, 3)})

    def test_group_children_order3_diagram(self):
        diagram = self.build('group_children_order3.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (2, 0), 'F': (2, 1),
                                    'G': (2, 2), 'Q': (0, 3),
                                    'Z': (0, 4)})

    def test_group_children_order4_diagram(self):
        diagram = self.build('group_children_order4.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (2, 0), 'Z': (0, 3)})

    def test_node_in_group_follows_outer_node_diagram(self):
        diagram = self.build('node_in_group_follows_outer_node.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'Z': (0, 1)})

    def test_group_id_and_node_id_are_not_conflicted_diagram(self):
        diagram = self.build('group_id_and_node_id_are_not_conflicted.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (0, 1), 'D': (1, 1),
                                    'Z': (0, 2)})

    def test_outer_node_follows_node_in_group_diagram(self):
        diagram = self.build('outer_node_follows_node_in_group.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'Z': (0, 1)})

    def test_large_group_and_node_diagram(self):
        diagram = self.build('large_group_and_node.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (1, 3), 'F': (2, 0),
                                    'Z': (0, 4)})

    def test_large_group_and_node2_diagram(self):
        diagram = self.build('large_group_and_node2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (3, 0),
                                    'E': (4, 0), 'F': (5, 0),
                                    'Z': (0, 1)})

    def test_large_group_and_two_nodes_diagram(self):
        diagram = self.build('large_group_and_two_nodes.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (1, 2),
                                    'E': (1, 3), 'F': (2, 0),
                                    'G': (2, 1), 'Z': (0, 4)})

    def test_group_height_diagram(self):
        diagram = self.build('group_height.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1),
                                    'E': (1, 2), 'Z': (0, 3)})

    def test_multiple_groups_diagram(self):
        diagram = self.build('multiple_groups.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (0, 2), 'D': (0, 3),
                                    'E': (1, 0), 'F': (1, 1),
                                    'G': (1, 2), 'H': (2, 0),
                                    'I': (2, 1), 'J': (3, 0),
                                    'Z': (0, 4)})

    def test_multiple_nested_groups_diagram(self):
        diagram = self.build('multiple_nested_groups.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'Z': (0, 2)})

    def test_group_works_node_decorator_diagram(self):
        diagram = self.build('group_works_node_decorator.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (3, 0), 'D': (2, 0),
                                    'E': (1, 1), 'Z': (0, 2)})

    def test_nested_groups_work_node_decorator_diagram(self):
        diagram = self.build('nested_groups_work_node_decorator.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'Z': (0, 2)})

    def test_reversed_multiple_groups_diagram(self):
        diagram = self.build('reverse_multiple_groups.diag')
        self.assertNodeXY(diagram, {'A': (3, 0), 'B': (3, 1),
                                    'C': (3, 2), 'D': (3, 3),
                                    'E': (2, 0), 'F': (2, 1),
                                    'G': (2, 2), 'H': (1, 0),
                                    'I': (1, 1), 'J': (0, 0),
                                    'Z': (0, 4)})

    def test_group_and_skipped_edge_diagram(self):
        diagram = self.build('group_and_skipped_edge.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (3, 0),
                                    'E': (1, 1), 'Z': (0, 2)})

    def test_group_orientation_diagram(self):
        diagram = self.build('group_orientation.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (2, 1),
                                    'Z': (0, 2)})

    def test_nested_group_orientation_diagram(self):
        diagram = self.build('nested_group_orientation.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (1, 0), 'Z': (0, 2)})
