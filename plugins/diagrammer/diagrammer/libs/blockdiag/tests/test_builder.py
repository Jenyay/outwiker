# -*- coding: utf-8 -*-

from blockdiag.tests.utils import BuilderTestCase


class TestBuilder(BuilderTestCase):
    def test_diagram_attributes(self):
        diagram = self.build('diagram_attributes.diag')

        self.assertEqual(160, diagram.node_width)
        self.assertEqual(160, diagram.node_height)
        self.assertEqual(32, diagram.span_width)
        self.assertEqual(32, diagram.span_height)
        self.assertEqual((128, 128, 128), diagram.linecolor)       # gray
        self.assertEqual('diamond', diagram.nodes[0].shape)
        self.assertEqual('dotted', diagram.nodes[0].style)
        self.assertEqual((255, 0, 0), diagram.nodes[0].color)      # red
        self.assertEqual((0, 128, 0), diagram.nodes[0].textcolor)  # green
        self.assertEqual(16, diagram.nodes[0].fontsize)
        self.assertEqual((0, 0, 255), diagram.nodes[1].color)      # blue
        self.assertEqual((0, 128, 0), diagram.nodes[1].textcolor)  # green
        self.assertEqual(16, diagram.nodes[1].fontsize)

        self.assertEqual((128, 128, 128), diagram.edges[0].color)  # gray
        self.assertEqual((0, 128, 0), diagram.edges[0].textcolor)  # green
        self.assertEqual(16, diagram.edges[0].fontsize)

    def test_diagram_attributes_order_diagram(self):
        diagram = self.build('diagram_attributes_order.diag')
        self.assertNodeColor(diagram, {'A': (255, 0, 0), 'B': (255, 0, 0)})
        self.assertNodeLineColor(diagram, {'A': (255, 0, 0), 'B': (255, 0, 0)})

    def test_circular_ref_to_root_diagram(self):
        diagram = self.build('circular_ref_to_root.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1),
                                    'Z': (0, 2)})

    def test_circular_ref_diagram(self):
        diagram = self.build('circular_ref.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1),
                                    'Z': (0, 2)})

    def test_circular_ref2_diagram(self):
        diagram = self.build('circular_ref2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (3, 0),
                                    'E': (3, 1), 'F': (4, 0),
                                    'Z': (0, 2)})

    def test_circular_ref_and_parent_node_diagram(self):
        diagram = self.build('circular_ref_and_parent_node.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (2, 1),
                                    'Z': (0, 2)})

    def test_labeled_circular_ref_diagram(self):
        diagram = self.build('labeled_circular_ref.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (2, 0),
                                    'C': (1, 0), 'Z': (0, 1)})

    def test_twin_forked_diagram(self):
        diagram = self.build('twin_forked.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 2), 'D': (2, 0),
                                    'E': (3, 0), 'F': (3, 1),
                                    'G': (4, 1), 'Z': (0, 3)})

    def test_skipped_edge_diagram(self):
        diagram = self.build('skipped_edge.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'Z': (0, 1)})

    def test_circular_skipped_edge_diagram(self):
        diagram = self.build('circular_skipped_edge.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'Z': (0, 1)})

    def test_triple_branched_diagram(self):
        diagram = self.build('triple_branched.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (0, 2), 'D': (1, 0),
                                    'Z': (0, 3)})

    def test_twin_circular_ref_to_root_diagram(self):
        diagram = self.build('twin_circular_ref_to_root.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'Z': (0, 2)})

    def test_twin_circular_ref_diagram(self):
        diagram = self.build('twin_circular_ref.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (1, 1),
                                    'Z': (0, 2)})

    def test_skipped_circular_diagram(self):
        diagram = self.build('skipped_circular.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 1),
                                    'C': (2, 0), 'Z': (0, 2)})

    def test_skipped_twin_circular_diagram(self):
        diagram = self.build('skipped_twin_circular.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 1), 'D': (2, 2),
                                    'E': (3, 0), 'Z': (0, 3)})

    def test_nested_skipped_circular_diagram(self):
        diagram = self.build('nested_skipped_circular.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 1), 'D': (3, 2),
                                    'E': (4, 1), 'F': (5, 0),
                                    'G': (6, 0), 'Z': (0, 3)})

    def test_self_ref_diagram(self):
        diagram = self.build('self_ref.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'Z': (0, 1)})

    def test_diagram_orientation_diagram(self):
        diagram = self.build('diagram_orientation.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (0, 2), 'D': (1, 2),
                                    'Z': (2, 0)})

    def test_nested_group_orientation2_diagram(self):
        diagram = self.build('nested_group_orientation2.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'C': (0, 2), 'D': (1, 2),
                                    'E': (2, 2), 'F': (2, 3),
                                    'Z': (3, 0)})

    def test_slided_children_diagram(self):
        diagram = self.build('slided_children.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (1, 3),
                                    'E': (2, 3), 'F': (3, 2),
                                    'G': (2, 1), 'H': (4, 1)})

    def test_non_rhombus_relation_height_diagram(self):
        diagram = self.build('non_rhombus_relation_height.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (0, 1),
                                    'E': (0, 2), 'F': (1, 2),
                                    'G': (1, 3), 'H': (2, 3),
                                    'I': (2, 4), 'J': (1, 5),
                                    'K': (2, 5), 'Z': (0, 6)})

    def test_define_class_diagram(self):
        diagram = self.build('define_class.diag')
        self.assertNodeColor(diagram, {'A': (255, 0, 0),
                                       'B': (255, 255, 255),
                                       'C': (255, 255, 255)})
        self.assertNodeStyle(diagram, {'A': 'dashed', 'B': None, 'C': None})
        self.assertEdgeColor(diagram, {('A', 'B'): (255, 0, 0),
                                       ('B', 'C'): (0, 0, 0)})
        self.assertEdgeStyle(diagram, {('A', 'B'): 'dashed',
                                       ('B', 'C'): None})
