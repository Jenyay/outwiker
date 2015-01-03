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
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self._defaultWidth = '700'
        self._defaultHeight = '300'

        self.path = mkdtemp (prefix=u'Абырвалг абыр')
        self.wikiroot = WikiDocument.create (self.path)
        self.page = WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        Application.wikiroot = None


    def tearDown (self):
        self.loader.clear()
        Application.wikiroot = None
        removeDir (self.path)


    def testEmpty (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {}
        content = u''
        page = None

        builder = GraphBuilder(params, content, page)
        graph = builder.graph

        self.assertEqual (graph.getProperty (u'width', 0), self._defaultWidth)
        self.assertEqual (graph.getProperty (u'height', 0), self._defaultHeight)

        self.assertEqual (graph.getProperty (u'Width', 0), self._defaultWidth)
        self.assertEqual (graph.getProperty (u'HEIGHT', 0), self._defaultHeight)

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))


    def testGraphProperties (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'width': 100,
            u'height': 150,
            u'render': u'highchart',


            # invalid values
            u'pane': u'Бла-бла-бла',
            u'abyrvalg': u'Абырвалг',
            u'Абырвалг': u'Главрыба',
            u'qwerty.qw': 42,
            u'qwerty.qw.sss': 42,
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertEqual (graph.getProperty (u'width', 0), 100)
        self.assertEqual (graph.getProperty (u'height', 0), 150)
        self.assertEqual (graph.getProperty (u'render', u''), u'highchart')

        self.assertEqual (graph.getProperty (u'abyrvalg', None), u'Абырвалг')
        self.assertEqual (graph.getProperty (u'Абырвалг', None), u'Главрыба')


    def testCurvesCount_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2': u'Абырвалг',
            'curve3': u'Абырвалг',
            'curve23sdf': u''
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNone (graph.getObject (u'curve2'))
        self.assertIsNone (graph.getObject (u'curve3'))
        self.assertIsNone (graph.getObject (u'curve23sdf'))


    def testCurvesCount_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))


    def testCurvesCount_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve1.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))


    def testCurvesCount_04 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))
        self.assertIsNotNone (graph.getObject (u'curve2'))


    def testCurvesCount_05 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve2.property': u'Абырвалг',
            'curve10.property': u'Абырвалг10',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve10'))
        self.assertEqual (graph.getObject (u'curve10').getProperty (u'property', None),
                          u'Абырвалг10')


    def testCurveProperties_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'curve.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')
        curve1 = graph.getObject (u'curve1')

        self.assertEqual (curve, curve1)
        self.assertEqual (curve.getProperty (u'property', None), u'Абырвалг')

        self.assertEqual (curve.getProperty (u'xcol', 42), None)
        self.assertEqual (curve.getProperty (u'ycol', 42), None)
        self.assertEqual (curve.getProperty (u'data', 42), None)


    def testCurveData_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve.data.colsep': u',',
            u'curve.data.coltype1': u'datetime',
            u'curve.data.coltype3': u'float',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        self.assertIsNotNone (curve)
        self.assertIsNone (curve.getProperty (u'data', 'xxx'))

        data = curve.getObject (u'data')
        self.assertIsNotNone (data)

        self.assertEqual (data.getProperty (u'colsep', None), u',')
        self.assertEqual (data.getProperty (u'coltype1', None), u'datetime')
        self.assertEqual (data.getProperty (u'coltype3', None), u'float')


    def testCurveData_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {}
        content = u'''123
456
789'''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123'], [u'456'], [u'789']])


    def testCurveData_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {}
        content = u'''123    111
456    222
789    333'''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123', u'111'], [u'456', u'222'], [u'789', u'333']])


    def testCurveAttachData_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        data = u'''123
456
789'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            u'curve.data': 'Attach:{}'.format (attachname),
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123'], [u'456'], [u'789']])


    def testCurveAttachData_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        data = u'''123
456
789'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            u'curve.data': attachname,
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123'], [u'456'], [u'789']])


    def testCurveAttachData_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve.data': u'invalid_fname.txt',
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [])


    def testCurveAttachData_04 (self):
        from datagraph.graphbuilder import GraphBuilder
        data = u'''123    111
456    222
789    333'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            u'curve.data': 'Attach:{}'.format (attachname),
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123', u'111'], [u'456', u'222'], [u'789', u'333']])


    def testCurveAttach_invalid_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve.data': 'Attach:invalid_fname.txt',
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [])


    def testCurves_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 1)


    def testCurves_02 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve.data': u'Attach:fname.txt'
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 1)


    def testCurves_03 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve1.data': u'Attach:fname.txt'
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 1)


    def testCurves_04 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve2.data': u'Attach:fname.txt'
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 2)


    def testCurves_05 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            u'curve2.title': u'curve2',
            u'curve1.title': u'curve1',
            u'curve6.title': u'curve6',
            u'curve3.title': u'curve3',
        }
        content = u''
        page = self.page

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        curves = graph.getCurves()

        self.assertEqual (len (curves), 4)
        self.assertEqual (curves[0].getProperty (u'title', u''), u'curve1')
        self.assertEqual (curves[1].getProperty (u'title', u''), u'curve2')
        self.assertEqual (curves[2].getProperty (u'title', u''), u'curve3')
        self.assertEqual (curves[3].getProperty (u'title', u''), u'curve6')


    def testAxis_01 (self):
        from datagraph.graphbuilder import GraphBuilder
        params = {
            'x.min': u'1.5',
            'y.max': u'2.5',
            'x.title': u'Абырвалг',
            'y.type': u'datetime',
        }
        content = u''
        page = None

        builder = GraphBuilder (params, content, page)
        graph = builder.graph

        xaxis = graph.getObject (u'x')
        yaxis = graph.getObject (u'y')

        self.assertIsNotNone (xaxis)
        self.assertIsNotNone (yaxis)

        self.assertEqual (xaxis.getProperty (u'min', None), u'1.5')
        self.assertEqual (yaxis.getProperty (u'max', None), u'2.5')
        self.assertEqual (xaxis.getProperty (u'title', None), u'Абырвалг')
        self.assertEqual (yaxis.getProperty (u'type', None), u'datetime')


    def _saveDataAndAttach (self, page, data):
        with NamedTemporaryFile ('w') as tempfile:
            tempfile.write (data)
            tempfile.flush()

            Attachment(page).attach ([tempfile.name])
            name = os.path.basename (tempfile.name)

        return name
