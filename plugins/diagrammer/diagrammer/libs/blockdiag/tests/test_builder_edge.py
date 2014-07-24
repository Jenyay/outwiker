# -*- coding: utf-8 -*-

from blockdiag.tests.utils import BuilderTestCase, capture_stderr


class TestBuilderEdge(BuilderTestCase):
    def test_diagram_attributes(self):
        diagram = self.build('diagram_attributes.diag')
        self.assertEqual(2, len(diagram.nodes))
        self.assertEqual(1, len(diagram.edges))

    def test_single_edge_diagram(self):
        diagram = self.build('single_edge.diag')
        self.assertEqual(2, len(diagram.nodes))
        self.assertEqual(1, len(diagram.edges))

        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0)})
        self.assertNodeLabel(diagram, {'A': 'A', 'B': 'B'})

    def test_two_edges_diagram(self):
        diagram = self.build('two_edges.diag')
        self.assertEqual(3, len(diagram.nodes))
        self.assertEqual(2, len(diagram.edges))

        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0), 'C': (2, 0)})

    def test_edge_shape(self):
        diagram = self.build('edge_shape.diag')
        self.assertEdgeDir(diagram, {('A', 'B'): 'none',
                                     ('B', 'C'): 'forward',
                                     ('C', 'D'): 'back',
                                     ('D', 'E'): 'both'})

    def test_edge_attribute(self):
        diagram = self.build('edge_attribute.diag')
        self.assertEdgeDir(diagram, {('A', 'B'): 'forward',
                                     ('B', 'C'): 'forward',
                                     ('C', 'D'): 'forward',
                                     ('D', 'E'): 'none',
                                     ('E', 'F'): 'both',
                                     ('F', 'G'): 'forward'})
        self.assertEdgeColor(diagram, {('A', 'B'): (255, 0, 0),  # red
                                       ('B', 'C'): (255, 0, 0),  # red
                                       ('C', 'D'): (255, 0, 0),  # red
                                       ('D', 'E'): (0, 0, 0),
                                       ('E', 'F'): (255, 0, 0),  # red
                                       ('F', 'G'): (0, 0, 0)})
        self.assertEdgeThick(diagram, {('A', 'B'): None,
                                       ('B', 'C'): None,
                                       ('C', 'D'): None,
                                       ('D', 'E'): None,
                                       ('E', 'F'): None,
                                       ('F', 'G'): 3})

    def test_folded_edge_diagram(self):
        diagram = self.build('folded_edge.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (0, 1),
                                    'E': (0, 2), 'F': (1, 1),
                                    'Z': (0, 3)})

    def test_skipped_edge_right_diagram(self):
        diagram = self.build('skipped_edge_right.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('A', 'C'): True,
                                         ('B', 'C'): False})

    def test_skipped_edge_rightdown_diagram(self):
        diagram = self.build('skipped_edge_rightdown.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('A', 'C'): True,
                                         ('A', 'D'): False,
                                         ('B', 'C'): False,
                                         ('B', 'D'): False})

    def test_skipped_edge_up_diagram(self):
        diagram = self.build('skipped_edge_up.diag')
        self.assertEdgeSkipped(diagram, {('C', 'A'): True})

    def test_skipped_edge_down_diagram(self):
        diagram = self.build('skipped_edge_down.diag')
        self.assertEdgeSkipped(diagram, {('A', 'C'): True})

    def test_skipped_edge_leftdown_diagram(self):
        diagram = self.build('skipped_edge_leftdown.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('B', 'C'): False,
                                         ('B', 'D'): False,
                                         ('C', 'G'): True,
                                         ('F', 'G'): False})

    @capture_stderr
    def test_skipped_edge_flowchart_rightdown_diagram(self):
        diagram = self.build('skipped_edge_flowchart_rightdown.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('A', 'C'): False,
                                         ('A', 'D'): True,
                                         ('C', 'D'): False})

    @capture_stderr
    def test_skipped_edge_flowchart_rightdown2_diagram(self):
        diagram = self.build('skipped_edge_flowchart_rightdown2.diag')
        self.assertEdgeSkipped(diagram, {('B', 'C'): False,
                                         ('A', 'C'): True})

    def test_skipped_edge_portrait_right_diagram(self):
        diagram = self.build('skipped_edge_portrait_right.diag')
        self.assertEdgeSkipped(diagram, {('A', 'C'): True})

    def test_skipped_edge_portrait_rightdown_diagram(self):
        diagram = self.build('skipped_edge_portrait_rightdown.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('A', 'C'): False,
                                         ('A', 'E'): True,
                                         ('B', 'D'): False,
                                         ('C', 'E'): False})

    def test_skipped_edge_portrait_leftdown_diagram(self):
        diagram = self.build('skipped_edge_portrait_leftdown.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('B', 'C'): False,
                                         ('D', 'C'): True,
                                         ('D', 'E'): False})

    def test_skipped_edge_portrait_down_diagram(self):
        diagram = self.build('skipped_edge_portrait_down.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('A', 'C'): True,
                                         ('B', 'C'): False})

    @capture_stderr
    def test_skipped_edge_portrait_flowchart_rightdown_diagram(self):
        diagram = self.build('skipped_edge_portrait_flowchart_rightdown.diag')
        self.assertEdgeSkipped(diagram, {('A', 'B'): False,
                                         ('A', 'C'): False,
                                         ('A', 'D'): True,
                                         ('C', 'D'): False})

    @capture_stderr
    def test_skipped_edge_portrait_flowchart_rightdown2_diagram(self):
        diagram = self.build('skipped_edge_portrait_flowchart_rightdown2.diag')
        self.assertEdgeSkipped(diagram, {('B', 'C'): False,
                                         ('A', 'C'): True})
