# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp, NamedTemporaryFile
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir


class GraphBuilderTest (unittest.TestCase):
    def setUp(self):
        dirlist = ["../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self._defaultWidth = '700'
        self._defaultHeight = '300'

        self.path = mkdtemp (prefix='Абырвалг абыр')
        self.wikiroot = WikiDocument.create (self.path)
        self.page = WikiPageFactory().create (self.wikiroot, "Страница 1", [])
        Application.wikiroot = None


    def tearDown (self):
        self.loader.clear()
        Application.wikiroot = None
        removeDir (self.path)


    def testEmpty (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {}
        content = ''
        page = None

        builder = GraphBuilder(params, content, page)
        graph = builder.graph

        self.assertEqual (graph.getProperty ('width', 0), self._defaultWidth)
        self.assertEqual (graph.getProperty ('height', 0), self._defaultHeight)

        self.assertEqual (graph.getProperty ('Width', 0), self._defaultWidth)
        self.assertEqual (graph.getProperty ('HEIGHT', 0), self._defaultHeight)

        self.assertIsNotNone (graph.getObject ('curve'))
        self.assertIsNotNone (graph.getObject ('curve1'))


    def testGraphProperties (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'width': 100,
            'height': 150,
            'render': 'highchart',


            # invalid values
            'pane': 'Бла-бла-бла',
            'abyrvalg': 'Абырвалг',
            'Абырвалг': 'Главрыба',
            'qwerty.qw': 42,
            'qwerty.qw.sss': 42,
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertEqual (graph.getProperty ('width', 0), 100)
        self.assertEqual (graph.getProperty ('height', 0), 150)
        self.assertEqual (graph.getProperty ('render', ''), 'highchart')

        self.assertEqual (graph.getProperty ('abyrvalg', None), 'Абырвалг')
        self.assertEqual (graph.getProperty ('Абырвалг', None), 'Главрыба')


    def testCurvesCount_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2': 'Абырвалг',
            'curve3': 'Абырвалг',
            'curve23sdf': ''
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNone (graph.getObject ('curve2'))
        self.assertIsNone (graph.getObject ('curve3'))
        self.assertIsNone (graph.getObject ('curve23sdf'))


    def testCurvesCount_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.property': 'Абырвалг',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject ('curve'))
        self.assertIsNotNone (graph.getObject ('curve1'))


    def testCurvesCount_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve1.property': 'Абырвалг',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject ('curve'))
        self.assertIsNotNone (graph.getObject ('curve1'))


    def testCurvesCount_04 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2.property': 'Абырвалг',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject ('curve'))
        self.assertIsNotNone (graph.getObject ('curve1'))
        self.assertIsNotNone (graph.getObject ('curve2'))


    def testCurvesCount_05 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2.property': 'Абырвалг',
            'curve10.property': 'Абырвалг10',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject ('curve'))
        self.assertIsNotNone (graph.getObject ('curve10'))
        self.assertEqual (graph.getObject ('curve10').getProperty ('property', None),
                          'Абырвалг10')


    def testCurveProperties_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.property': 'Абырвалг',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')
        curve1 = graph.getObject ('curve1')

        self.assertEqual (curve, curve1)
        self.assertEqual (curve.getProperty ('property', None), 'Абырвалг')

        self.assertEqual (curve.getProperty ('xcol', 42), None)
        self.assertEqual (curve.getProperty ('ycol', 42), None)
        self.assertEqual (curve.getProperty ('data', 42), None)


    def testCurveData_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.data.colsep': ',',
            'curve.data.coltype1': 'datetime',
            'curve.data.coltype3': 'float',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        self.assertIsNotNone (curve)
        self.assertIsNone (curve.getProperty ('data', 'xxx'))

        data = curve.getObject ('data')
        self.assertIsNotNone (data)

        self.assertEqual (data.getProperty ('colsep', None), ',')
        self.assertEqual (data.getProperty ('coltype1', None), 'datetime')
        self.assertEqual (data.getProperty ('coltype3', None), 'float')


    def testCurveData_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {}
        content = '''123
456
789'''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [['123'], ['456'], ['789']])


    def testCurveData_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {}
        content = '''123    111
456    222
789    333'''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [['123', '111'], ['456', '222'], ['789', '333']])


    def testCurveAttachData_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        data = '''123
456
789'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            'curve.data': 'Attach:{}'.format (attachname),
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [['123'], ['456'], ['789']])


    def testCurveAttachData_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        data = '''123
456
789'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            'curve.data': attachname,
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [['123'], ['456'], ['789']])


    def testCurveAttachData_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.data': 'invalid_fname.txt',
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [])


    def testCurveAttachData_04 (self):
        from datagraph.graphbuilder import GraphBuilder
        data = '''123    111
456    222
789    333'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            'curve.data': 'Attach:{}'.format (attachname),
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [['123', '111'], ['456', '222'], ['789', '333']])


    def testCurveAttach_invalid_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.data': 'Attach:invalid_fname.txt',
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject ('curve')

        curveData = curve.getObject ('data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [])


    def testCurves_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 1)


    def testCurves_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.data': 'Attach:fname.txt'
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 1)


    def testCurves_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve1.data': 'Attach:fname.txt'
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 1)


    def testCurves_04 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2.data': 'Attach:fname.txt'
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 2)


    def testCurves_05 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2.title': 'curve2',
            'curve1.title': 'curve1',
            'curve6.title': 'curve6',
            'curve3.title': 'curve3',
        }
        content = ''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 4)
        self.assertEqual (curves[0].getProperty ('title', ''), 'curve1')
        self.assertEqual (curves[1].getProperty ('title', ''), 'curve2')
        self.assertEqual (curves[2].getProperty ('title', ''), 'curve3')
        self.assertEqual (curves[3].getProperty ('title', ''), 'curve6')


    def testAxis_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'x.min': '1.5',
            'y.max': '2.5',
            'x.title': 'Абырвалг',
            'y.type': 'datetime',
        }
        content = ''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        xaxis = graph.getObject ('x')
        yaxis = graph.getObject ('y')

        self.assertIsNotNone (xaxis)
        self.assertIsNotNone (yaxis)

        self.assertEqual (xaxis.getProperty ('min', None), '1.5')
        self.assertEqual (yaxis.getProperty ('max', None), '2.5')
        self.assertEqual (xaxis.getProperty ('title', None), 'Абырвалг')
        self.assertEqual (yaxis.getProperty ('type', None), 'datetime')


    def _saveDataAndAttach (self, page, data):
        fname = None
        with NamedTemporaryFile ('w', delete=False) as tempfile:
            tempfile.write (data)
            tempfile.flush()
            fname = tempfile.name

        Attachment(page).attach ([fname])
        name = os.path.basename (fname)
        os.remove (fname)

        return name
