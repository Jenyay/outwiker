# -*- coding: utf-8 -*-

from collections import defaultdict
from blockdiag.tests.utils import BuilderTestCase


class TestBuilderNode(BuilderTestCase):
    def test_single_node_diagram(self):
        diagram = self.build('single_node.diag')

        self.assertEqual(1, len(diagram.nodes))
        self.assertEqual(0, len(diagram.edges))
        self.assertEqual('A', diagram.nodes[0].label)
        self.assertEqual((0, 0), diagram.nodes[0].xy)

    def test_node_shape_diagram(self):
        expected = {'A': 'box', 'B': 'roundedbox', 'C': 'diamond',
                    'D': 'ellipse', 'E': 'note', 'F': 'cloud',
                    'G': 'mail', 'H': 'beginpoint', 'I': 'endpoint',
                    'J': 'minidiamond', 'K': 'flowchart.condition',
                    'L': 'flowchart.database', 'M': 'flowchart.input',
                    'N': 'flowchart.loopin', 'O': 'flowchart.loopout',
                    'P': 'actor', 'Q': 'flowchart.terminator', 'R': 'textbox',
                    'S': 'dots', 'T': 'none', 'U': 'square', 'V': 'circle',
                    'Z': 'box'}
        diagram = self.build('node_shape.diag')
        self.assertNodeShape(diagram, expected)

    def test_node_shape_namespace_diagram(self):
        diagram = self.build('node_shape_namespace.diag')
        self.assertNodeShape(diagram, {'A': 'flowchart.condition',
                                       'B': 'condition',
                                       'Z': 'box'})

    def test_node_has_multilined_label_diagram(self):
        diagram = self.build('node_has_multilined_label.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'Z': (0, 1)})
        self.assertNodeLabel(diagram, {'A': "foo\nbar", 'Z': 'Z'})

    def test_quoted_node_id_diagram(self):
        diagram = self.build('quoted_node_id.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), "'A'": (1, 0),
                                    'B': (2, 0), 'Z': (0, 1)})

    def test_node_id_includes_dot_diagram(self):
        diagram = self.build('node_id_includes_dot.diag')
        self.assertNodeXY(diagram, {'A.B': (0, 0), 'C.D': (1, 0),
                                    'Z': (0, 1)})

    def test_multiple_nodes_definition_diagram(self):
        diagram = self.build('multiple_nodes_definition.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (0, 1),
                                    'Z': (0, 2)})
        self.assertNodeColor(diagram, {'A': (255, 0, 0), 'B': (255, 0, 0),
                                       'Z': (255, 255, 255)})

    def test_multiple_node_relation_diagram(self):
        diagram = self.build('multiple_node_relation.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (1, 1), 'D': (2, 0),
                                    'Z': (0, 2)})

    def test_node_attribute(self):
        labels = {'A': 'B', 'B': 'double quoted', 'C': 'single quoted',
                  'D': '\'"double" quoted\'', 'E': '"\'single\' quoted"',
                  'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I',
                  'J': 'Hello', 'K': 'K'}
        colors = {'A': (255, 0, 0), 'B': (255, 255, 255), 'C': (255, 0, 0),
                  'D': (255, 0, 0), 'E': (255, 0, 0), 'F': (255, 255, 255),
                  'G': (255, 255, 255), 'H': (255, 255, 255),
                  'I': (255, 255, 255), 'J': (255, 255, 255),
                  'K': (255, 255, 255)}
        textcolors = defaultdict(lambda: (0, 0, 0))
        textcolors['F'] = (255, 0, 0)
        linecolors = defaultdict(lambda: (0, 0, 0))
        linecolors['I'] = (255, 0, 0)
        numbered = defaultdict(lambda: None)
        numbered['E'] = '1'
        stacked = defaultdict(lambda: False)
        stacked['G'] = True
        fontsize = defaultdict(lambda: None)
        fontsize['H'] = 16
        orientations = defaultdict(lambda: 'horizontal')
        orientations['J'] = 'vertical'
        backgrounds = defaultdict(lambda: None)
        backgrounds['K'] = ('src/blockdiag/tests/diagrams/'
                            'debian-logo-256color-palettealpha.png')

        diagram = self.build('node_attribute.diag')
        self.assertNodeLabel(diagram, labels)
        self.assertNodeColor(diagram, colors)
        self.assertNodeTextColor(diagram, textcolors)
        self.assertNodeLineColor(diagram, linecolors)
        self.assertNodeNumbered(diagram, numbered)
        self.assertNodeStacked(diagram, stacked)
        self.assertNodeFontsize(diagram, fontsize)
        self.assertNodeLabel_Orientation(diagram, orientations)
        self.assertNodeBackground(diagram, backgrounds)

    def test_node_height_diagram(self):
        diagram = self.build('node_height.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (2, 1),
                                    'E': (1, 1), 'Z': (0, 2)})

    def test_branched_diagram(self):
        diagram = self.build('branched.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'D': (1, 1),
                                    'E': (2, 1), 'Z': (0, 2)})

    def test_multiple_parent_node_diagram(self):
        diagram = self.build('multiple_parent_node.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (0, 2), 'D': (1, 2),
                                    'E': (0, 1), 'Z': (0, 3)})

    def test_twin_multiple_parent_node_diagram(self):
        diagram = self.build('twin_multiple_parent_node.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (0, 1), 'D': (1, 1),
                                    'E': (0, 2), 'Z': (0, 3)})

    def test_flowable_node_diagram(self):
        diagram = self.build('flowable_node.diag')
        self.assertNodeXY(diagram, {'A': (0, 0), 'B': (1, 0),
                                    'C': (2, 0), 'Z': (0, 1)})

    def test_plugin_autoclass_diagram(self):
        diagram = self.build('plugin_autoclass.diag')
        self.assertNodeXY(diagram, {'A_emphasis': (0, 0),
                                    'B_emphasis': (1, 0),
                                    'C': (1, 1)})
        self.assertNodeStyle(diagram, {'A_emphasis': 'dashed',
                                       'B_emphasis': 'dashed',
                                       'C': None})
        self.assertNodeColor(diagram, {'A_emphasis': (255, 0, 0),
                                       'B_emphasis': (255, 0, 0),
                                       'C': (255, 255, 255)})

    def test_plugin_attributes_diagram(self):
        diagram = self.build('plugin_attributes.diag')
        self.assertNodeTest_Attr1(diagram, {'A': "1", 'B': None})
        self.assertNodeTest_Attr2(diagram, {'A': "2", 'B': None})
        self.assertNodeTest_Attr3(diagram, {'A': "3", 'B': None})
